# Nexus Configuration System

This directory contains the detailed configuration structure for Nexus using a hybrid approach.

## Configuration Priority

Configuration is loaded in this order (later overrides earlier):

1. **Main Config** (`../../config.yaml`) - Core project settings
2. **Environment Config** (`environments/{env}.yaml`) - Environment-specific overrides  
3. **Runtime Config** (`../../.nexus/config.json`) - Runtime changes
4. **Environment Variables** (`NEXUS_*`) - System environment overrides

## Directory Structure

### `environments/`
Environment-specific configuration files that extend the main configuration:
- `development.yaml` - Development environment settings
- `testing.yaml` - Test environment settings  
- `staging.yaml` - Staging environment settings
- `production.yaml` - Production environment settings

### `templates/`
Configuration templates for creating new configuration files:
- `config.template.yaml` - Main configuration template
- `logging.template.yaml` - Logging configuration template
- `project.template.yaml` - Project-specific template

### `schemas/`
JSON schemas for configuration validation:
- `config.schema.json` - Main configuration schema
- `environment.schema.json` - Environment configuration schema

## Usage Examples

### Basic Configuration Access
```python
from nexus.core.config import get_config

config = get_config()
print(f"Environment: {config.environment.value}")
print(f"Log level: {config.log_level}")
```

### Environment-Specific Behavior
```python
from nexus.core.config import is_development, is_production

if is_development():
    enable_debug_features()
elif is_production():
    optimize_for_performance()
```

### Feature Flags
```python
config = get_config()
if config.features.get('experimental_features', False):
    enable_experimental_mode()
```

## Environment Variables

All configuration can be overridden with environment variables using the `NEXUS_` prefix:

- `NEXUS_ENV` - Set environment (development, testing, staging, production)
- `NEXUS_DEBUG` - Enable debug mode (true/false)
- `NEXUS_LOG_LEVEL` - Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `NEXUS_MAX_PARALLEL` - Set maximum parallel processes
- `NEXUS_FEATURE_*` - Enable/disable features (e.g., `NEXUS_FEATURE_AUTO_RELOAD=true`)

## Adding New Configuration

1. Add new fields to the main configuration schema
2. Update environment-specific configs as needed
3. Add environment variable mappings in the config system
4. Update templates if the setting should be templatable
5. Document the new configuration option

## Validation

Configuration is automatically validated when loaded. Validation errors will be reported during startup.

To manually validate configuration:
```python
from nexus.core.config import validate_config
errors = validate_config()
for error in errors:
    print(f"Config error: {error}")
```

## Configuration Templates

Templates use environment variable substitution for easy customization:

```yaml
# Example template usage
project:
  name: "${PROJECT_NAME}"  # Will be replaced with $PROJECT_NAME env var
  version: "${PROJECT_VERSION}"
```

## Runtime Configuration

Runtime configuration is stored in `.nexus/config.json` and allows for:
- Temporary overrides during development
- User-specific preferences
- Session-specific settings

Example runtime config:
```json
{
  "runtime_overrides": {
    "max_parallel": 8,
    "debug_mode": true
  },
  "session": {
    "session_id": "sess_abc123",
    "user_preferences": {
      "ui_theme": "dark"
    }
  }
}
```
