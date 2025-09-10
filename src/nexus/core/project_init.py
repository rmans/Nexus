"""Project initialization module."""

import shutil
import json
from pathlib import Path
from rich.console import Console

console = Console()

class ProjectInitializer:
    """Initialize Nexus project using existing structure."""
    
    def __init__(self, docs_dir="nexus_docs", template=None):
        """Initialize the project initializer.
        
        Args:
            docs_dir: Name of the documentation directory to create
            template: Template to use for initialization
        """
        self.project_root = Path.cwd()
        self.docs_dir = docs_dir
        self.nexus_dir = self.project_root / ".nexus"
        self.cursor_dir = self.project_root / ".cursor"
        self.docs_path = self.project_root / docs_dir
        self.template = template
        
        # Get package root for templates
        import nexus
        if hasattr(nexus, '__file__') and nexus.__file__:
            self.package_root = Path(nexus.__file__).parent
        else:
            # Fallback for when __file__ is not available
            import os
            self.package_root = Path(os.path.dirname(os.path.abspath(__file__))).parent
    
    def initialize(self, force=False):
        """Initialize Nexus project.
        
        Args:
            force: Whether to overwrite existing configuration
        """
        console.print("🚀 Initializing Nexus project...", style="blue")
        
        # Check if already initialized
        if self.nexus_dir.exists() and not force:
            console.print("⚠️  Nexus already initialized. Use --force to overwrite.", style="yellow")
            return
        
        # Create directories
        self._create_directories()
        
        # Copy existing instructions
        self._install_instructions()
        
        # Copy existing commands as Cursor rules
        self._install_cursor_rules()
        
        # Create docs scaffold from existing generated-docs
        self._create_docs_scaffold()
        
        # Update gitignore
        self._update_gitignore()
        
        # Create config
        self._create_config()
        
        console.print("✅ Nexus initialization complete!", style="green")
        console.print(f"📁 Documentation directory: {self.docs_dir}/", style="blue")
        console.print("🎯 Cursor rules installed in .cursor/rules/", style="blue")
        console.print("📚 Instructions available in .nexus/instructions/", style="blue")
    
    def _create_directories(self):
        """Create necessary directories."""
        directories = [
            self.nexus_dir,
            self.cursor_dir / "rules",
            self.nexus_dir / "instructions",
            self.nexus_dir / "config",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        console.print("📁 Created directory structure", style="green")
    
    def _install_instructions(self):
        """Copy existing instructions to .nexus/."""
        source = self.package_root / "instructions"
        target = self.nexus_dir / "instructions"
        
        if source.exists():
            shutil.copytree(source, target, dirs_exist_ok=True)
            console.print("📦 Installed instructions", style="green")
        else:
            # Create basic instruction templates
            self._create_basic_instructions(target)
    
    def _create_basic_instructions(self, target_dir):
        """Create basic instruction templates."""
        instructions = {
            "code-review.md": """# Code Review Instruction

## Purpose
Guide AI assistants in conducting thorough code reviews.

## Checklist
- [ ] Code follows project style guidelines
- [ ] Functions are well-documented
- [ ] Error handling is appropriate
- [ ] Performance considerations addressed
- [ ] Security implications reviewed

## Review Process
1. Read through the entire change
2. Check for logical errors
3. Verify test coverage
4. Suggest improvements
5. Provide constructive feedback
""",
            "documentation.md": """# Documentation Instruction

## Purpose
Guide AI assistants in creating comprehensive documentation.

## Documentation Types
- API documentation
- User guides
- Technical specifications
- README files
- Code comments

## Best Practices
- Use clear, concise language
- Include examples
- Keep documentation up to date
- Use consistent formatting
- Add diagrams where helpful
""",
            "testing.md": """# Testing Instruction

## Purpose
Guide AI assistants in writing effective tests.

## Test Types
- Unit tests
- Integration tests
- End-to-end tests
- Performance tests

## Test Structure
- Arrange: Set up test data
- Act: Execute the code
- Assert: Verify results
- Cleanup: Reset state

## Best Practices
- Test edge cases
- Use descriptive test names
- Keep tests independent
- Mock external dependencies
- Aim for good coverage
"""
        }
        
        for filename, content in instructions.items():
            (target_dir / filename).write_text(content)
        
        console.print("📝 Created basic instruction templates", style="green")
    
    def _install_cursor_rules(self):
        """Copy existing commands as Cursor rules."""
        source = self.package_root / "commands"
        target = self.cursor_dir / "rules"
        
        if source.exists():
            target.mkdir(parents=True, exist_ok=True)
            for command_file in source.glob("*.md"):
                shutil.copy2(command_file, target / command_file.name)
            console.print("🎯 Installed Cursor rules", style="green")
        else:
            # Create basic Cursor rules
            self._create_basic_cursor_rules(target)
    
    def _create_basic_cursor_rules(self, target_dir):
        """Create basic Cursor rules."""
        rules = {
            "code-style.md": """# Code Style Rules

## Python Style
- Follow PEP 8 guidelines
- Use type hints for all functions
- Write docstrings for all public functions
- Use meaningful variable names
- Keep functions small and focused

## Documentation
- Use Google-style docstrings
- Include examples in docstrings
- Keep README files updated
- Document all public APIs

## Testing
- Write tests for all new functionality
- Use descriptive test names
- Aim for high test coverage
- Mock external dependencies
""",
            "security.md": """# Security Rules

## General Principles
- Never commit secrets or API keys
- Use environment variables for sensitive data
- Validate all user inputs
- Use secure coding practices
- Keep dependencies updated

## Data Handling
- Sanitize user inputs
- Use parameterized queries
- Encrypt sensitive data
- Implement proper access controls
- Log security events
""",
            "performance.md": """# Performance Rules

## Code Performance
- Profile before optimizing
- Use appropriate data structures
- Avoid unnecessary computations
- Cache expensive operations
- Use async/await where appropriate

## Database Performance
- Use indexes effectively
- Avoid N+1 queries
- Use connection pooling
- Monitor query performance
- Use pagination for large datasets
"""
        }
        
        for filename, content in rules.items():
            (target_dir / filename).write_text(content)
        
        console.print("🎯 Created basic Cursor rules", style="green")
    
    def _create_docs_scaffold(self):
        """Create docs scaffold from existing generated-docs structure."""
        # Use existing generated-docs structure as template
        doc_types = ["arch", "exec", "impl", "int", "prd", "rules", "task", "tests"]
        
        for doc_type in doc_types:
            target_dir = self.docs_path / doc_type
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Create index file
            index_file = target_dir / "index.md"
            index_content = f"""# {doc_type.upper()} Documents

*Generated {doc_type} documents will appear here*

## Overview
This directory contains {doc_type} documentation for the project.

## Files
*No {doc_type} documents yet*

## Usage
Use the `nexus generate-docs` command to create documentation in this directory.
"""
            index_file.write_text(index_content)
        
        # Create main README for docs
        docs_readme = self.docs_path / "README.md"
        docs_readme.write_text("""# Project Documentation

This directory contains generated documentation for the project.

## Structure
- `prd/` - Product Requirements Documents
- `arch/` - Architecture Documentation
- `impl/` - Implementation Details
- `int/` - Integration Documentation
- `exec/` - Execution Documentation
- `rules/` - Business Rules
- `task/` - Task Documentation
- `tests/` - Test Documentation

## Usage
Use `nexus generate-docs` to update documentation.
Use `nexus serve-docs` to view documentation locally.
""")
        
        console.print(f"📁 Created docs scaffold in {self.docs_dir}/", style="green")
    
    def _update_gitignore(self):
        """Add Nexus entries to .gitignore."""
        gitignore_path = self.project_root / ".gitignore"
        
        nexus_ignore_block = f"""
# Nexus system files (ignore - these are tooling)
.nexus/
.cursor/

# Keep {self.docs_dir}/ - this is project content that should be committed
# Add any generated files you want to ignore:
# {self.docs_dir}/generated/
# {self.docs_dir}/temp/
"""
        
        if gitignore_path.exists():
            current_content = gitignore_path.read_text()
            if ".nexus/" not in current_content:
                gitignore_path.write_text(current_content + nexus_ignore_block)
                console.print("📝 Updated .gitignore", style="green")
        else:
            gitignore_path.write_text(nexus_ignore_block.strip())
            console.print("📝 Created .gitignore", style="green")
    
    def _create_config(self):
        """Create project configuration."""
        config = {
            "nexus": {
                "version": "0.1.0",
                "docs_directory": self.docs_dir,
                "initialized": True,
                "cursor_integration": True,
                "template": self.template or "default"
            },
            "project": {
                "name": self.project_root.name,
                "type": "unknown",
                "description": "AI-assisted development project"
            },
            "documentation": {
                "auto_generate": True,
                "formats": ["markdown"],
                "include_types": ["prd", "arch", "impl", "int", "exec", "rules", "task", "tests"]
            }
        }
        
        config_file = self.nexus_dir / "config.json"
        config_file.write_text(json.dumps(config, indent=2))
        console.print("⚙️ Created configuration", style="green")
