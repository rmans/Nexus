"""Configuration management module."""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from rich.console import Console

console = Console()

class ConfigManager:
    """Manage Nexus project configuration."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize configuration manager.
        
        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root or Path.cwd()
        self.nexus_dir = self.project_root / ".nexus"
        self.config_file = self.nexus_dir / "config.json"
        self._config = None
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get current configuration."""
        if self._config is None:
            self._config = self.load_config()
        return self._config
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file.
        
        Returns:
            Configuration dictionary
        """
        if not self.config_file.exists():
            return self._get_default_config()
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            console.print(f"⚠️  Error loading config: {e}", style="yellow")
            return self._get_default_config()
    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Save configuration to file.
        
        Args:
            config: Configuration to save (uses current config if None)
        """
        if config is not None:
            self._config = config
        
        # Ensure nexus directory exists
        self.nexus_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
        except IOError as e:
            console.print(f"❌ Error saving config: {e}", style="red")
    
    def update_config(self, updates: Dict[str, Any]) -> None:
        """Update configuration with new values.
        
        Args:
            updates: Dictionary of updates to apply
        """
        current_config = self.config.copy()
        self._deep_update(current_config, updates)
        self.save_config(current_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config.copy()
        current = config
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
        self.save_config(config)
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration.
        
        Returns:
            Default configuration dictionary
        """
        return {
            "nexus": {
                "version": "0.1.0",
                "docs_directory": "nexus_docs",
                "initialized": False,
                "cursor_integration": True,
                "template": "default"
            },
            "project": {
                "name": self.project_root.name,
                "type": "unknown",
                "description": "AI-assisted development project"
            },
            "documentation": {
                "auto_generate": True,
                "formats": ["markdown"],
                "include_types": ["prd", "arch", "impl", "int", "exec", "rules", "task", "tests"],
                "output_dir": "nexus_docs"
            },
            "instructions": {
                "default_template": "basic",
                "auto_execute": False,
                "parallel_execution": False
            },
            "generation": {
                "templates_dir": ".nexus/templates",
                "output_formats": ["markdown", "html"],
                "include_code": True,
                "include_diagrams": True
            }
        }
    
    def _deep_update(self, base_dict: Dict[str, Any], update_dict: Dict[str, Any]) -> None:
        """Deep update dictionary.
        
        Args:
            base_dict: Base dictionary to update
            update_dict: Dictionary with updates
        """
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def is_initialized(self) -> bool:
        """Check if Nexus is initialized in this project.
        
        Returns:
            True if initialized, False otherwise
        """
        return self.nexus_dir.exists() and self.config_file.exists() and self.get("nexus.initialized", False)
    
    def get_docs_directory(self) -> Path:
        """Get documentation directory path.
        
        Returns:
            Path to documentation directory
        """
        docs_dir = self.get("nexus.docs_directory", "nexus_docs")
        return self.project_root / docs_dir
    
    def get_cursor_rules_dir(self) -> Path:
        """Get Cursor rules directory path.
        
        Returns:
            Path to Cursor rules directory
        """
        return self.project_root / ".cursor" / "rules"
    
    def get_instructions_dir(self) -> Path:
        """Get instructions directory path.
        
        Returns:
            Path to instructions directory
        """
        return self.nexus_dir / "instructions"
    
    def validate_config(self) -> list:
        """Validate current configuration.
        
        Returns:
            List of validation errors
        """
        errors = []
        
        # Check required fields
        required_fields = [
            "nexus.version",
            "nexus.docs_directory",
            "project.name"
        ]
        
        for field in required_fields:
            if not self.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Check if docs directory exists
        docs_dir = self.get_docs_directory()
        if not docs_dir.exists():
            errors.append(f"Documentation directory does not exist: {docs_dir}")
        
        # Check if Cursor rules directory exists
        cursor_rules = self.get_cursor_rules_dir()
        if not cursor_rules.exists():
            errors.append(f"Cursor rules directory does not exist: {cursor_rules}")
        
        return errors
