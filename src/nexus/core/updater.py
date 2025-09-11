"""Project update management for Nexus."""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Any
from rich.console import Console
from rich.prompt import Confirm
from .version import get_current_template_version, version_compare

console = Console()

class ProjectUpdater:
    """Handles updating Nexus project files to latest version."""
    
    # Get template version from centralized config
    CURRENT_TEMPLATE_VERSION = get_current_template_version()
    
    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        self.nexus_dir = self.project_root / ".nexus"
        self.config_file = self.nexus_dir / "config.json"
        
        # Get package resources
        try:
            import nexus
            if hasattr(nexus, '__file__') and nexus.__file__:
                self.package_root = Path(nexus.__file__).parent
            else:
                # Fallback for when __file__ is not available
                import os
                self.package_root = Path(os.path.dirname(os.path.abspath(__file__))).parent
        except ImportError:
            # Fallback if nexus module is not available
            import os
            self.package_root = Path(os.path.dirname(os.path.abspath(__file__))).parent
    
    def check_needs_update(self) -> bool:
        """Check if project files need updating."""
        if not self.config_file.exists():
            return False
            
        config = self._load_config()
        current_version = config.get("nexus", {}).get("template_version", "0.0.0")
        
        return version_compare(current_version, self.CURRENT_TEMPLATE_VERSION) < 0
    
    def update_project_files(self, force=False):
        """Update project files to latest version."""
        if not force and not self.check_needs_update():
            console.print("✅ Project files are already up to date", style="green")
            return
            
        if not force:
            console.print("🔄 Project files are outdated", style="yellow")
            if not Confirm.ask("Update project files to latest version?"):
                return
        
        console.print("📦 Updating Nexus project files...", style="blue")
        
        # Update template files
        self._update_cursor_rules()
        self._update_instructions()
        self._update_doc_scaffolds()
        
        # Update config
        self._update_config()
        
        console.print("✅ Project files updated successfully!", style="green")
    
    def _update_cursor_rules(self):
        """Update Cursor rules from latest templates."""
        cursor_rules_dir = self.project_root / ".cursor" / "rules"
        commands_source = self.package_root / "commands"
        
        if not commands_source.exists():
            return
            
        cursor_rules_dir.mkdir(parents=True, exist_ok=True)
        
        # Get all command files
        for command_file in commands_source.glob("*.md"):
            target_file = cursor_rules_dir / command_file.name
            shutil.copy2(command_file, target_file)
            
        console.print("📝 Updated Cursor rules", style="green")
    
    def _update_instructions(self):
        """Update instruction files."""
        instructions_target = self.nexus_dir / "instructions"
        instructions_source = self.package_root / "instructions"
        
        if not instructions_source.exists():
            return
            
        # Remove old instructions and copy new ones
        if instructions_target.exists():
            shutil.rmtree(instructions_target)
            
        shutil.copytree(instructions_source, instructions_target)
        console.print("📚 Updated instruction files", style="green")
    
    def _update_doc_scaffolds(self):
        """Update documentation scaffolds if new types were added."""
        # This is conservative - only adds new doc types, doesn't remove existing
        config = self._load_config()
        docs_dir = config.get("nexus", {}).get("docs_directory", "nexus_docs")
        docs_path = self.project_root / docs_dir
        
        # Current doc types (could be made configurable)
        doc_types = ["arch", "exec", "impl", "int", "prd", "rules", "task", "tests"]
        
        for doc_type in doc_types:
            doc_dir = docs_path / doc_type
            doc_dir.mkdir(parents=True, exist_ok=True)
            
            index_file = doc_dir / "index.md"
            if not index_file.exists():
                index_content = f"""# {doc_type.upper()} Documents

*Generated {doc_type} documents will appear here*

## Files
*No {doc_type} documents yet*
"""
                index_file.write_text(index_content)
                console.print(f"📁 Added {doc_type} documentation scaffold", style="cyan")
    
    def _update_config(self):
        """Update config with latest template version."""
        config = self._load_config()
        if "nexus" not in config:
            config["nexus"] = {}
        config["nexus"]["template_version"] = self.CURRENT_TEMPLATE_VERSION
        config["nexus"]["last_updated"] = self._get_current_timestamp()
        
        self.config_file.write_text(json.dumps(config, indent=2))
    
    def _load_config(self) -> Dict[str, Any]:
        """Load project configuration."""
        if self.config_file.exists():
            return json.loads(self.config_file.read_text())
        return {}
    
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp as ISO string."""
        from datetime import datetime
        return datetime.now().isoformat()


def check_project_needs_update() -> bool:
    """Convenience function to check if update is needed."""
    updater = ProjectUpdater()
    return updater.check_needs_update()
