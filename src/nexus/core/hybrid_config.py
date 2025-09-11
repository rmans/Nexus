"""Enhanced hybrid configuration system for Nexus."""

import json
import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from enum import Enum
from rich.console import Console

console = Console()

class Environment(Enum):
    """Supported environments."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"

class HybridConfigManager:
    """Enhanced configuration manager with hybrid loading and priority support."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize hybrid configuration manager.
        
        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root or Path.cwd()
        self.nexus_dir = self.project_root / ".nexus"
        self.configs_dir = self.project_root / "src" / "nexus" / "docs" / "configs"
        self._config = None
        self._environment = None
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get current configuration with all layers merged."""
        if self._config is None:
            self._config = self._load_hybrid_config()
        return self._config
    
    @property
    def environment(self) -> Environment:
        """Get current environment."""
        if self._environment is None:
            env_str = os.getenv('NEXUS_ENV', 'development')
            try:
                self._environment = Environment(env_str)
            except ValueError:
                console.print(f"⚠️  Unknown environment '{env_str}', using development", style="yellow")
                self._environment = Environment.DEVELOPMENT
        return self._environment
    
    def _load_hybrid_config(self) -> Dict[str, Any]:
        """Load configuration using hybrid approach with priority order."""
        config = {}
        
        # 1. Load main configuration (config.yaml in project root)
        main_config = self._load_main_config()
        if main_config:
            config = self._deep_merge(config, main_config)
        
        # 2. Load environment-specific configuration
        env_config = self._load_environment_config()
        if env_config:
            config = self._deep_merge(config, env_config)
        
        # 3. Load runtime configuration (.nexus/config.json)
        runtime_config = self._load_runtime_config()
        if runtime_config:
            config = self._deep_merge(config, runtime_config)
        
        # 4. Apply environment variable overrides
        env_overrides = self._load_environment_overrides()
        if env_overrides:
            config = self._deep_merge(config, env_overrides)
        
        return config
    
    def _load_main_config(self) -> Optional[Dict[str, Any]]:
        """Load main configuration from config.yaml."""
        config_file = self.project_root / "config.yaml"
        if not config_file.exists():
            return None
        
        try:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        except (yaml.YAMLError, IOError) as e:
            console.print(f"⚠️  Error loading main config: {e}", style="yellow")
            return None
    
    def _load_environment_config(self) -> Optional[Dict[str, Any]]:
        """Load environment-specific configuration."""
        env_file = self.configs_dir / "environments" / f"{self.environment.value}.yaml"
        if not env_file.exists():
            return None
        
        try:
            with open(env_file, 'r') as f:
                config = yaml.safe_load(f)
                
                # Handle extends directive
                if 'extends' in config:
                    extends_path = self.project_root / config['extends']
                    if extends_path.exists():
                        with open(extends_path, 'r') as f:
                            base_config = yaml.safe_load(f)
                            config = self._deep_merge(base_config, config)
                    del config['extends']
                
                return config
        except (yaml.YAMLError, IOError) as e:
            console.print(f"⚠️  Error loading environment config: {e}", style="yellow")
            return None
    
    def _load_runtime_config(self) -> Optional[Dict[str, Any]]:
        """Load runtime configuration from .nexus/config.json."""
        runtime_file = self.nexus_dir / "config.json"
        if not runtime_file.exists():
            return None
        
        try:
            with open(runtime_file, 'r') as f:
                config = json.load(f)
                # Extract runtime overrides if they exist
                return config.get('runtime_overrides', {})
        except (json.JSONDecodeError, IOError) as e:
            console.print(f"⚠️  Error loading runtime config: {e}", style="yellow")
            return None
    
    def _load_environment_overrides(self) -> Dict[str, Any]:
        """Load configuration overrides from environment variables."""
        overrides = {}
        
        # Map environment variables to config paths
        env_mappings = {
            'NEXUS_ENV': 'environment',
            'NEXUS_DEBUG': 'features.debug_mode',
            'NEXUS_LOG_LEVEL': 'logging.level',
            'NEXUS_MAX_PARALLEL': 'execution.max_parallel',
            'NEXUS_TIMEOUT': 'execution.timeout',
            'NEXUS_DOCS_DIR': 'directories.docs',
            'NEXUS_CACHE_DIR': 'directories.cache',
            'NEXUS_LOGS_DIR': 'directories.logs',
            'NEXUS_SERVER_HOST': 'server.host',
            'NEXUS_SERVER_PORT': 'server.port',
        }
        
        for env_var, config_path in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                self._set_nested_value(overrides, config_path, self._convert_env_value(value))
        
        # Handle feature flags (NEXUS_FEATURE_*)
        for key, value in os.environ.items():
            if key.startswith('NEXUS_FEATURE_'):
                feature_name = key[14:].lower()  # Remove 'NEXUS_FEATURE_' prefix
                self._set_nested_value(overrides, f'features.{feature_name}', self._convert_env_value(value))
        
        return overrides
    
    def _convert_env_value(self, value: str) -> Union[str, int, bool, List[str]]:
        """Convert environment variable string to appropriate type."""
        # Boolean conversion
        if value.lower() in ('true', 'yes', '1', 'on'):
            return True
        elif value.lower() in ('false', 'no', '0', 'off'):
            return False
        
        # Integer conversion
        try:
            return int(value)
        except ValueError:
            pass
        
        # List conversion (comma-separated)
        if ',' in value:
            return [item.strip() for item in value.split(',')]
        
        return value
    
    def _set_nested_value(self, config: Dict[str, Any], path: str, value: Any) -> None:
        """Set a nested value in configuration using dot notation."""
        keys = path.split('.')
        current = config
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries."""
        result = base.copy()
        
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key using dot notation."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value in runtime config."""
        runtime_file = self.nexus_dir / "config.json"
        runtime_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing runtime config
        if runtime_file.exists():
            try:
                with open(runtime_file, 'r') as f:
                    runtime_config = json.load(f)
            except (json.JSONDecodeError, IOError):
                runtime_config = {}
        else:
            runtime_config = {}
        
        # Ensure runtime_overrides exists
        if 'runtime_overrides' not in runtime_config:
            runtime_config['runtime_overrides'] = {}
        
        # Set the value
        self._set_nested_value(runtime_config['runtime_overrides'], key, value)
        
        # Save runtime config
        try:
            with open(runtime_file, 'w') as f:
                json.dump(runtime_config, f, indent=2)
        except IOError as e:
            console.print(f"❌ Error saving runtime config: {e}", style="red")
        
        # Invalidate cached config
        self._config = None
    
    def validate_config(self) -> List[str]:
        """Validate current configuration against schema."""
        errors = []
        
        # Load schema
        schema_file = self.configs_dir / "schemas" / "config.schema.json"
        if not schema_file.exists():
            errors.append("Configuration schema not found")
            return errors
        
        try:
            with open(schema_file, 'r') as f:
                schema = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            errors.append(f"Error loading schema: {e}")
            return errors
        
        # Basic validation (simplified - in production, use jsonschema library)
        required_fields = schema.get('required', [])
        for field in required_fields:
            if not self.get(field):
                errors.append(f"Missing required field: {field}")
        
        return errors
    
    def get_docs_dir(self) -> Path:
        """Get documentation directory path."""
        docs_dir = self.get('directories.docs', 'generated-docs')
        return self.project_root / docs_dir
    
    def get_cache_dir(self) -> Path:
        """Get cache directory path."""
        cache_dir = self.get('directories.cache', '.nexus/cache')
        return self.project_root / cache_dir
    
    def get_logs_dir(self) -> Path:
        """Get logs directory path."""
        logs_dir = self.get('directories.logs', '.nexus/logs')
        return self.project_root / logs_dir
    
    def get_templates_dir(self) -> Path:
        """Get templates directory path."""
        templates_dir = self.get('directories.templates', '.nexus/templates')
        return self.project_root / templates_dir
    
    def is_debug(self) -> bool:
        """Check if debug mode is enabled."""
        return self.get('features.debug_mode', False)
    
    def is_development(self) -> bool:
        """Check if current environment is development."""
        return self.environment == Environment.DEVELOPMENT
    
    def is_production(self) -> bool:
        """Check if current environment is production."""
        return self.environment == Environment.PRODUCTION
    
    def get_log_level(self) -> str:
        """Get current log level."""
        return self.get('logging.level', 'INFO')
    
    def get_max_parallel(self) -> int:
        """Get maximum parallel processes."""
        return self.get('execution.max_parallel', 4)
    
    def get_timeout(self) -> int:
        """Get execution timeout."""
        return self.get('execution.timeout', 300)
    
    def get_server_config(self) -> Dict[str, Any]:
        """Get server configuration."""
        return self.get('server', {
            'host': 'localhost',
            'port': 8000
        })
    
    def get_doc_formats(self) -> List[str]:
        """Get documentation formats."""
        return self.get('documentation.formats', ['markdown'])
    
    def get_auto_generate_docs(self) -> bool:
        """Check if documentation auto-generation is enabled."""
        return self.get('documentation.auto_generate', True)
    
    def get_features(self) -> Dict[str, bool]:
        """Get all feature flags."""
        return self.get('features', {})


# Global configuration instance
_config_manager = None

def get_config_manager() -> HybridConfigManager:
    """Get global configuration manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = HybridConfigManager()
    return _config_manager

def get_config() -> Dict[str, Any]:
    """Get current configuration."""
    return get_config_manager().config

def is_development() -> bool:
    """Check if current environment is development."""
    return get_config_manager().is_development()

def is_production() -> bool:
    """Check if current environment is production."""
    return get_config_manager().is_production()

def is_debug() -> bool:
    """Check if debug mode is enabled."""
    return get_config_manager().is_debug()

def get_docs_dir() -> Path:
    """Get documentation directory path."""
    return get_config_manager().get_docs_dir()

def get_templates_dir() -> Path:
    """Get templates directory path."""
    return get_config_manager().get_templates_dir()

def validate_config() -> List[str]:
    """Validate current configuration."""
    return get_config_manager().validate_config()
