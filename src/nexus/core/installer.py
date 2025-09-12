"""Nexus installer system with hybrid configuration support."""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.panel import Panel
from rich.table import Table

console = Console()

class NexusInstaller:
    """Comprehensive installer for Nexus with hybrid configuration support."""
    
    def __init__(self, target_dir: Optional[Path] = None, force: bool = False):
        """Initialize the installer.
        
        Args:
            target_dir: Target installation directory
            force: Force installation even if Nexus is already installed
        """
        self.target_dir = target_dir or self._get_default_install_dir()
        self.force = force
        self.nexus_dir = self.target_dir / "nexus"
        self.config_dir = self.nexus_dir / "configs"
        self.templates_dir = self.nexus_dir / "templates"
        self.examples_dir = self.nexus_dir / "examples"
        
        # Get package root
        import nexus
        if hasattr(nexus, '__file__') and nexus.__file__:
            self.package_root = Path(nexus.__file__).parent
        else:
            self.package_root = Path(__file__).parent.parent
    
    def install(self) -> bool:
        """Install Nexus with hybrid configuration system.
        
        Returns:
            True if installation successful, False otherwise
        """
        try:
            console.print("🚀 Installing Nexus with Hybrid Configuration System", style="bold blue")
            console.print("=" * 60)
            
            # Check if already installed
            if not self.force and self._is_installed():
                if not Confirm.ask("Nexus is already installed. Reinstall?"):
                    console.print("Installation cancelled.", style="yellow")
                    return False
            
            # Create installation plan
            plan = self._create_installation_plan()
            self._display_installation_plan(plan)
            
            if not Confirm.ask("Proceed with installation?"):
                console.print("Installation cancelled.", style="yellow")
                return False
            
            # Execute installation
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                self._execute_installation(progress)
            
            # Post-installation setup
            self._post_installation_setup()
            
            # Test configuration system
            self._test_configuration_system()
            
            # Display success message
            self._display_success_message()
            
            return True
            
        except Exception as e:
            console.print(f"❌ Installation failed: {e}", style="red")
            return False
    
    def _get_default_install_dir(self) -> Path:
        """Get default installation directory."""
        if sys.platform == "win32":
            return Path.home() / "AppData" / "Local" / "Nexus"
        elif sys.platform == "darwin":
            return Path.home() / "Library" / "Application Support" / "Nexus"
        else:
            return Path.home() / ".local" / "nexus"
    
    def _is_installed(self) -> bool:
        """Check if Nexus is already installed."""
        return self.nexus_dir.exists() and (self.nexus_dir / "config.yaml").exists()
    
    def _create_installation_plan(self) -> Dict[str, List[str]]:
        """Create installation plan."""
        return {
            "Directories": [
                str(self.nexus_dir),
                str(self.config_dir),
                str(self.config_dir / "environments"),
                str(self.config_dir / "templates"),
                str(self.config_dir / "schemas"),
                str(self.config_dir / "examples"),
                str(self.templates_dir),
                str(self.examples_dir),
            ],
            "Configuration Files": [
                "config.yaml (main configuration)",
                "environments/development.yaml",
                "environments/testing.yaml", 
                "environments/staging.yaml",
                "environments/production.yaml",
                "templates/config.template.yaml",
                "templates/logging.template.yaml",
                "templates/project.template.yaml",
                "schemas/config.schema.json",
                "schemas/environment.schema.json",
                ".env.example",
            ],
            "Discovery System": [
                "Discovery Engine (automatic code analysis)",
                "Code Analyzer (structure, dependencies, patterns)",
                "Synthesizer (insights and recommendations)",
                "Validator (result validation)",
                "Cache System (performance optimization)",
                "Report Manager (save, list, view reports)",
                "CLI Integration (nexus discover, nexus discovery commands)",
            ],
            "Documentation": [
                "README.md (main documentation)",
                "API_REFERENCE.md",
                "GETTING_STARTED.md",
                "PROJECT_STRUCTURE.md",
                "INSTALLER_CHECKLIST.md",
                "nexus_docs/ directory structure",
                "nexus_docs/discovery/ (Discovery reports)",
                "nexus_docs/arch/, exec/, impl/, int/, prd/, rules/, task/, tests/",
            ],
            "Examples": [
                "serve_example.py",
                "docs_example.py",
                "configuration_examples/",
                "discovery_example.py",
            ]
        }
    
    def _display_installation_plan(self, plan: Dict[str, List[str]]) -> None:
        """Display installation plan."""
        console.print("\n📋 Installation Plan:", style="bold")
        
        for category, items in plan.items():
            table = Table(title=category)
            table.add_column("Item", style="cyan")
            table.add_column("Status", style="green")
            
            for item in items:
                table.add_row(item, "Will be created")
            
            console.print(table)
    
    def _execute_installation(self, progress) -> None:
        """Execute the installation process."""
        # Create directories
        task1 = progress.add_task("Creating directories...", total=None)
        self._create_directories()
        progress.update(task1, completed=True)
        
        # Install configuration files
        task2 = progress.add_task("Installing configuration files...", total=None)
        self._install_configuration_files()
        progress.update(task2, completed=True)
        
        # Install documentation
        task3 = progress.add_task("Installing documentation...", total=None)
        self._install_documentation()
        progress.update(task3, completed=True)
        
        # Install examples
        task4 = progress.add_task("Installing examples...", total=None)
        self._install_examples()
        progress.update(task4, completed=True)
        
        # Create runtime directories
        task5 = progress.add_task("Setting up runtime environment...", total=None)
        self._setup_runtime_environment()
        progress.update(task5, completed=True)
    
    def _create_directories(self) -> None:
        """Create installation directories."""
        directories = [
            self.nexus_dir,
            self.config_dir,
            self.config_dir / "environments",
            self.config_dir / "templates",
            self.config_dir / "schemas",
            self.config_dir / "examples",
            self.templates_dir,
            self.examples_dir,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _install_configuration_files(self) -> None:
        """Install configuration files."""
        # Main configuration
        main_config = self.package_root.parent / "config.yaml"
        if main_config.exists():
            shutil.copy2(main_config, self.nexus_dir / "config.yaml")
        
        # Environment configurations
        env_source = self.package_root / "docs" / "configs" / "environments"
        if env_source.exists():
            env_target = self.config_dir / "environments"
            shutil.copytree(env_source, env_target, dirs_exist_ok=True)
        
        # Templates
        templates_source = self.package_root / "docs" / "configs" / "templates"
        if templates_source.exists():
            templates_target = self.config_dir / "templates"
            shutil.copytree(templates_source, templates_target, dirs_exist_ok=True)
        
        # Schemas
        schemas_source = self.package_root / "docs" / "configs" / "schemas"
        if schemas_source.exists():
            schemas_target = self.config_dir / "schemas"
            shutil.copytree(schemas_source, schemas_target, dirs_exist_ok=True)
        
        # Environment variables template
        env_example = self.package_root.parent / ".env.example"
        if env_example.exists():
            shutil.copy2(env_example, self.nexus_dir / ".env.example")
    
    def _install_documentation(self) -> None:
        """Install documentation files."""
        docs_source = self.package_root / "docs" / "readmes"
        if docs_source.exists():
            for doc_file in docs_source.glob("*.md"):
                shutil.copy2(doc_file, self.nexus_dir / doc_file.name)
        
        # Main README
        main_readme = self.package_root.parent / "README.md"
        if main_readme.exists():
            shutil.copy2(main_readme, self.nexus_dir / "README.md")
        
        # Create nexus_docs directory structure
        self._create_nexus_docs_structure()
    
    def _install_examples(self) -> None:
        """Install example files."""
        examples_source = self.package_root / "docs" / "configs" / "examples"
        if examples_source.exists():
            shutil.copytree(examples_source, self.examples_dir, dirs_exist_ok=True)
        
        # Install discovery example
        discovery_example_source = self.package_root / "docs" / "examples" / "discovery_example.py"
        if discovery_example_source.exists():
            discovery_example_target = self.examples_dir / "discovery_example.py"
            shutil.copy2(discovery_example_source, discovery_example_target)
            console.print("📁 Installed discovery example", style="green")
    
    def _create_nexus_docs_structure(self) -> None:
        """Create nexus_docs directory structure with discovery subdirectory."""
        # Use the target installation directory for docs
        docs_dir = self.nexus_dir / "nexus_docs"
        
        # Create main docs directory
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        # Create discovery subdirectory
        discovery_dir = docs_dir / "discovery"
        discovery_dir.mkdir(parents=True, exist_ok=True)
        
        # Create discovery index file
        discovery_index = discovery_dir / "index.md"
        if not discovery_index.exists():
            discovery_index_content = """# Discovery Reports

This directory contains Discovery System reports generated by Nexus.

## Report Naming Convention

Discovery reports follow the naming convention: `DISC-YYYY-MM-DD-Title.md`

- **DISC**: Prefix indicating Discovery System report
- **YYYY-MM-DD**: Date of analysis
- **Title**: Descriptive title of the analysis

## Available Reports

*No discovery reports yet*

## Usage

Generate discovery reports using:

```bash
# Basic discovery with report saving
nexus discover --save "Project Analysis"

# Deep analysis with report saving
nexus discover --deep --save "Deep Analysis Report"

# List all reports
nexus discovery list

# View specific report
nexus discovery view DISC-YYYY-MM-DD-Project-Analysis
```

## Report Formats

Each discovery report includes:
- **Markdown Summary**: Human-readable analysis summary
- **JSON Data**: Detailed structured data for integration
- **Context Data**: PRD-ready context information
- **Metadata**: Analysis timestamp, options, and configuration
"""
            discovery_index.write_text(discovery_index_content)
            console.print("📁 Created discovery reports directory", style="green")
        
        # Create standard documentation type directories
        doc_types = ["arch", "exec", "impl", "int", "prd", "rules", "task", "tests"]
        for doc_type in doc_types:
            doc_dir = docs_dir / doc_type
            doc_dir.mkdir(parents=True, exist_ok=True)
            
            # Create index file for each doc type
            index_file = doc_dir / "index.md"
            if not index_file.exists():
                index_content = f"""# {doc_type.upper()} Documents

*Generated {doc_type} documents will appear here*

## Files
*No {doc_type} documents yet*
"""
                index_file.write_text(index_content)
    
    def _setup_runtime_environment(self) -> None:
        """Set up runtime environment."""
        # Create .nexus directory structure
        nexus_runtime = self.nexus_dir / ".nexus"
        nexus_runtime.mkdir(exist_ok=True)
        
        # Create initial runtime config using fixed configuration system
        from nexus.core.hybrid_config import get_config, Environment, ConfigManager
        
        config = get_config()
        config_manager = ConfigManager(project_root=self.nexus_dir)
        
        runtime_config = {
            "nexus": {
                "version": config.project_version,
                "template_version": "1.0.0",
                "installed": True,
                "install_date": self._get_current_timestamp(),
                "install_path": str(self.nexus_dir),
                "environment": config.environment.value,
                "debug_mode": config.is_debug(),
                "hybrid_config_enabled": True
            },
            "runtime_overrides": {},
            "session": {
                "session_id": self._generate_session_id(),
                "user_preferences": {}
            },
            "configuration": {
                "hybrid_system": True,
                "main_config": str(self.nexus_dir / "config.yaml"),
                "configs_dir": str(self.nexus_dir / "configs"),
                "templates_dir": str(self.nexus_dir / "configs" / "templates"),
                "schemas_dir": str(self.nexus_dir / "configs" / "schemas"),
                "examples_dir": str(self.nexus_dir / "configs" / "examples")
            }
        }
        
        config_file = nexus_runtime / "config.json"
        with open(config_file, 'w') as f:
            json.dump(runtime_config, f, indent=2)
        
        # Create cache and logs directories
        (nexus_runtime / "cache").mkdir(exist_ok=True)
        (nexus_runtime / "logs").mkdir(exist_ok=True)
        (nexus_runtime / "instructions").mkdir(exist_ok=True)
        
        # Initialize the configuration system
        try:
            config_manager.initialize_project()
            console.print("✅ Configuration system initialized", style="green")
            
            # Validate configuration
            errors = config_manager.validate_config()
            if errors:
                console.print("⚠️ Configuration validation warnings:", style="yellow")
                for error in errors:
                    console.print(f"  - {error}", style="yellow")
            else:
                console.print("✅ Configuration validation passed", style="green")
                
        except Exception as e:
            console.print(f"⚠️ Warning: Could not initialize configuration system: {e}", style="yellow")
    
    def _post_installation_setup(self) -> None:
        """Post-installation setup tasks."""
        # Create symlink or add to PATH
        self._setup_command_line_access()
        
        # Create desktop shortcut (if GUI available)
        self._create_desktop_shortcut()
        
        # Set up auto-update mechanism
        self._setup_auto_update()
    
    def _setup_command_line_access(self) -> None:
        """Set up command line access."""
        # This would typically involve adding to PATH or creating symlinks
        # For now, we'll create a simple wrapper script
        wrapper_script = self.nexus_dir / "nexus"
        
        if sys.platform == "win32":
            wrapper_content = f"""@echo off
python "{self.package_root.parent}" %*
"""
            wrapper_script = self.nexus_dir / "nexus.bat"
        else:
            wrapper_content = f"""#!/bin/bash
python "{self.package_root.parent}" "$@"
"""
        
        with open(wrapper_script, 'w') as f:
            f.write(wrapper_content)
        
        if sys.platform != "win32":
            os.chmod(wrapper_script, 0o755)
    
    def _create_desktop_shortcut(self) -> None:
        """Create desktop shortcut (if GUI available)."""
        # This would create a desktop shortcut on supported platforms
        # Implementation would be platform-specific
        pass
    
    def _setup_auto_update(self) -> None:
        """Set up auto-update mechanism."""
        # Create update configuration
        update_config = {
            "auto_check": True,
            "check_interval": 86400,  # 24 hours
            "last_check": None,
            "update_channel": "stable"
        }
        
        update_file = self.nexus_dir / ".nexus" / "update_config.json"
        with open(update_file, 'w') as f:
            json.dump(update_config, f, indent=2)
    
    def _display_success_message(self) -> None:
        """Display installation success message."""
        success_panel = Panel(
            f"""🎉 Nexus Installation Complete!

Installation Directory: {self.nexus_dir}
Configuration Files: {self.config_dir}
Examples: {self.examples_dir}

Fixed Hybrid Configuration System:
✅ Main config: {self.nexus_dir}/config.yaml
✅ Environment configs: {self.config_dir}/environments/
✅ Templates & schemas: {self.config_dir}/templates/, {self.config_dir}/schemas/
✅ Runtime config: {self.nexus_dir}/.nexus/config.json
✅ Full API compatibility maintained

Discovery System:
🔍 Automatic code analysis and project understanding
📊 Language and framework detection
🏗️ Architectural pattern recognition
💡 Intelligent insights and recommendations
⚡ Caching system for performance
📄 Report management (save, list, view reports)
🎯 CLI integration (nexus discover, nexus discovery commands)

Next Steps:
1. Add {self.nexus_dir} to your PATH
2. Run 'nexus init-project' to create a new project
3. Run 'nexus discover' to analyze your codebase
4. Run 'nexus discover --save "Project Analysis"' to save reports
5. Run 'nexus discovery list' to view saved reports
6. Check 'nexus status' to verify installation
7. Read the documentation in {self.nexus_dir}/README.md
8. Explore configuration examples in {self.config_dir}/examples/

Discovery Commands:
• nexus discover [path] - Analyze project structure
• nexus discover --deep - Detailed analysis
• nexus discover --output json - JSON output
• nexus discover --cache - Use cached results
• nexus discover --save "Title" - Save discovery report
• nexus discovery list - List saved reports
• nexus discovery view REPORT_ID - View specific report

Examples:
• python {self.examples_dir}/discovery_example.py - Run discovery examples
• Check {self.examples_dir}/ for more examples

For help, run: nexus --help""",
            title="Installation Successful",
            border_style="green"
        )
        
        console.print(success_panel)
    
    def _test_configuration_system(self) -> None:
        """Test the configuration system after installation."""
        try:
            from nexus.core.hybrid_config import get_config, get_config_manager, is_debug, is_development
            
            console.print("🧪 Testing configuration system...", style="blue")
            
            # Test configuration loading
            config = get_config()
            config_manager = get_config_manager()
            
            # Test basic configuration access
            project_name = config.project_name
            environment = config.environment.value
            debug_mode = is_debug()
            dev_mode = is_development()
            
            # Test path helpers
            docs_dir = config_manager.get_docs_dir()
            cache_dir = config_manager.get_cache_dir()
            configs_dir = config_manager.get_configs_dir()
            
            # Test backwards compatibility
            old_docs_dir = config_manager.get_docs_directory()
            is_init = config_manager.is_initialized()
            
            console.print("✅ Configuration system test passed", style="green")
            console.print(f"  Project: {project_name} ({environment})")
            console.print(f"  Debug mode: {debug_mode}, Development: {dev_mode}")
            console.print(f"  Directories: docs={docs_dir}, cache={cache_dir}")
            console.print(f"  Backwards compatibility: {old_docs_dir == docs_dir}")
            
            # Test Discovery System
            console.print("🔍 Testing Discovery System...", style="blue")
            try:
                from nexus.core.discovery.engine import DiscoveryEngine
                from nexus.core.discovery.cache import DiscoveryCache
                
                # Test Discovery Engine initialization
                engine = DiscoveryEngine(config_manager)
                console.print("✅ Discovery Engine initialized successfully", style="green")
                
                # Test Discovery Cache
                cache = DiscoveryCache(cache_dir / "discovery")
                console.print("✅ Discovery Cache initialized successfully", style="green")
                
                console.print("✅ Discovery System test passed", style="green")
                
            except Exception as e:
                console.print(f"⚠️ Discovery System test failed: {e}", style="yellow")
            
        except Exception as e:
            console.print(f"⚠️ Configuration system test failed: {e}", style="yellow")
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp as ISO string."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        import uuid
        return str(uuid.uuid4())


def install_nexus(target_dir: Optional[Path] = None, force: bool = False) -> bool:
    """Install Nexus with hybrid configuration system.
    
    Args:
        target_dir: Target installation directory
        force: Force installation even if already installed
        
    Returns:
        True if installation successful, False otherwise
    """
    installer = NexusInstaller(target_dir=target_dir, force=force)
    return installer.install()


def uninstall_nexus(install_dir: Optional[Path] = None) -> bool:
    """Uninstall Nexus.
    
    Args:
        install_dir: Installation directory to remove
        
    Returns:
        True if uninstallation successful, False otherwise
    """
    if install_dir is None:
        installer = NexusInstaller()
        install_dir = installer.nexus_dir
    
    if not install_dir.exists():
        console.print("Nexus is not installed.", style="yellow")
        return True
    
    if not Confirm.ask(f"Remove Nexus installation from {install_dir}?"):
        console.print("Uninstallation cancelled.", style="yellow")
        return False
    
    try:
        shutil.rmtree(install_dir)
        console.print("✅ Nexus uninstalled successfully.", style="green")
        return True
    except Exception as e:
        console.print(f"❌ Uninstallation failed: {e}", style="red")
        return False


def check_installation() -> Dict[str, any]:
    """Check Nexus installation status.
    
    Returns:
        Dictionary with installation status information
    """
    installer = NexusInstaller()
    
    status = {
        "installed": installer._is_installed(),
        "install_dir": str(installer.nexus_dir),
        "config_dir": str(installer.config_dir),
        "version": None,
        "last_updated": None
    }
    
    if status["installed"]:
        # Try to get version info
        try:
            config_file = installer.nexus_dir / ".nexus" / "config.json"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    status["version"] = config.get("nexus", {}).get("version")
                    status["last_updated"] = config.get("nexus", {}).get("install_date")
        except Exception:
            pass
    
    return status


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Nexus Installer")
    parser.add_argument("--target-dir", type=Path, help="Target installation directory")
    parser.add_argument("--force", action="store_true", help="Force installation")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall Nexus")
    parser.add_argument("--check", action="store_true", help="Check installation status")
    
    args = parser.parse_args()
    
    if args.check:
        status = check_installation()
        console.print(json.dumps(status, indent=2))
    elif args.uninstall:
        uninstall_nexus(args.target_dir)
    else:
        install_nexus(args.target_dir, args.force)
