# API Reference

This document provides detailed information about the Nexus API, commands, and interfaces.

## Command Line Interface

### Basic Usage

```bash
nexus [OPTIONS] COMMAND [ARGS]...
```

### Global Options

| Option | Description | Default |
|--------|-------------|---------|
| `--version` | Show version information | - |
| `--help` | Show help message | - |
| `--debug` | Enable debug logging | False |
| `--config` | Path to configuration file | `config.yaml` |
| `--verbose` | Enable verbose output | False |

### Commands

#### Core Commands

##### `init-project`
Initialize a new Nexus project or workspace.

```bash
nexus init-project [OPTIONS]
```

**Options:**
- `--force`: Overwrite existing configuration
- `--template`: Use specific template
- `--docs-dir`: Documentation directory name (default: nexus_docs)

**Example:**
```bash
nexus init-project --template basic --docs-dir my-docs
```

##### `status`
Show current project status and configuration.

```bash
nexus status [OPTIONS]
```

**Options:**
- `--detailed`: Show detailed status information
- `--json`: Output in JSON format

**Example:**
```bash
nexus status --detailed
```

##### `update-project`
Update project files to latest Nexus version.

```bash
nexus update-project [OPTIONS]
```

**Options:**
- `--force`: Force update without confirmation
- `--check-only`: Only check if update is needed

**Example:**
```bash
nexus update-project --force
```

##### `list-commands`
List all available commands.

```bash
nexus list-commands [OPTIONS]
```

**Options:**
- `--category`: Filter by command category
- `--json`: Output in JSON format

#### Instruction Commands

##### `create-instruction`
Create a new instruction template.

```bash
python -m nexus create-instruction NAME [OPTIONS]
```

**Options:**
- `--template`: Instruction template to use
- `--output`: Output file path
- `--interactive`: Use interactive mode

**Example:**
```bash
python -m nexus create-instruction "data-processing" --template basic
```

##### `execute-instruction`
Execute an instruction or workflow.

```bash
python -m nexus execute-instruction INSTRUCTION [OPTIONS]
```

**Options:**
- `--dry-run`: Preview execution without running
- `--parallel`: Enable parallel execution
- `--timeout`: Execution timeout in seconds

**Example:**
```bash
python -m nexus execute-instruction "data-processing" --dry-run
```

#### Documentation Commands

##### `generate-docs`
Generate project documentation.

```bash
python -m nexus generate-docs [OPTIONS]
```

**Options:**
- `--output`: Output directory
- `--format`: Documentation format (html, pdf, markdown)
- `--include`: Include specific documentation sections

**Example:**
```bash
python -m nexus generate-docs --format html --output ./docs
```

##### `serve-docs`
Start a local documentation server.

```bash
python -m nexus serve-docs [OPTIONS]
```

**Options:**
- `--port`: Server port (default: 8000)
- `--host`: Server host (default: localhost)
- `--auto-reload`: Auto-reload on changes

**Example:**
```bash
python -m nexus serve-docs --port 8080
```

## Configuration

Nexus uses a **fixed hybrid configuration system** with full API compatibility and performance optimization:

### Configuration Priority (Highest to Lowest)

1. **Environment Variables** (`NEXUS_*`) - Runtime overrides
2. **Runtime Config** (`.nexus/config.json`) - Session-specific settings
3. **Environment-Specific** (`src/nexus/docs/configs/environments/{env}.yaml`) - Environment overrides
4. **Main Config** (`config.yaml`) - Project root configuration

### Main Configuration File

The main configuration is stored in `config.yaml`:

```yaml
# Nexus Configuration
project:
  name: "Nexus"
  version: "1.0.0"
  description: "A modular project framework"

environment: "development"

# Directory settings
directories:
  docs: "generated-docs"
  cache: ".nexus/cache"
  logs: ".nexus/logs"

# Logging configuration
logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "nexus.log"
  max_size: 10485760  # 10MB
  backup_count: 5

# Documentation settings
documentation:
  formats: ["html", "markdown"]
  auto_generate: true

# Execution settings
execution:
  max_parallel: 4
  timeout: 300
  retry_attempts: 3

# Server settings
server:
  host: "localhost"
  port: 8000

# Feature flags
features:
  auto_reload: true
  debug_mode: false
  experimental_features: false
```

### Environment-Specific Configurations

Environment-specific configurations are stored in `src/nexus/docs/configs/environments/`:

- `development.yaml` - Development environment settings
- `testing.yaml` - Test environment settings
- `staging.yaml` - Staging environment settings
- `production.yaml` - Production environment settings

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXUS_ENV` | Environment (development, testing, staging, production) | `development` |
| `NEXUS_DEBUG` | Enable debug mode | `false` |
| `NEXUS_LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) | `INFO` |
| `NEXUS_MAX_PARALLEL` | Maximum parallel processes | `4` |
| `NEXUS_TIMEOUT` | Execution timeout in seconds | `300` |
| `NEXUS_DOCS_DIR` | Documentation directory | `generated-docs` |
| `NEXUS_CACHE_DIR` | Cache directory | `.nexus/cache` |
| `NEXUS_LOGS_DIR` | Logs directory | `.nexus/logs` |
| `NEXUS_SERVER_HOST` | Server host | `localhost` |
| `NEXUS_SERVER_PORT` | Server port | `8000` |
| `NEXUS_FEATURE_*` | Feature flags (e.g., `NEXUS_FEATURE_AUTO_RELOAD=true`) | - |

## Python API

### Core Classes

#### `ConfigManager` (Fixed Hybrid Configuration)

Enhanced configuration manager with full API compatibility and performance optimization.

```python
from nexus.core.hybrid_config import ConfigManager, get_config, is_development

# Initialize configuration manager (backwards compatible)
config_manager = ConfigManager()

# Existing API works unchanged
docs_dir = config_manager.get_docs_directory()
is_init = config_manager.is_initialized()
version = config_manager.get("nexus.version")

# New enhanced API
config = get_config()
project_name = config.project_name
environment = config.environment.value
debug_mode = config.is_debug()

# Check environment
if is_development():
    enable_debug_features()

# Get specific values
docs_dir = config_manager.get_docs_dir()
log_level = config_manager.get_log_level()
```

#### `ProjectUpdater`

Smart update system for project files.

```python
from nexus.core.updater import ProjectUpdater

# Initialize updater
updater = ProjectUpdater()

# Check if update is needed
if updater.check_needs_update():
    print("Project files need updating")
    updater.update_project_files(force=True)
```

#### `NexusProject`

Main project class for managing Nexus projects.

```python
from nexus.core import NexusProject

# Initialize project
project = NexusProject(config_path="config.yaml")

# Get project status
status = project.get_status()

# Execute instruction
result = project.execute_instruction("instruction_name")
```

#### `InstructionManager`

Manages instruction definitions and execution.

```python
from nexus.core import InstructionManager

# Create manager
manager = InstructionManager()

# Load instruction
instruction = manager.load_instruction("instruction_name")

# Execute instruction
result = manager.execute(instruction, context={})
```

#### `DocumentationGenerator`

Generates project documentation.

```python
from nexus.core import DocumentationGenerator

# Create generator
generator = DocumentationGenerator()

# Generate documentation
generator.generate(output_dir="./docs", format="html")
```

### Utility Functions

#### Configuration Functions

```python
from nexus.core.hybrid_config import (
    get_config, 
    get_config_manager,
    is_development, 
    is_production, 
    is_debug,
    get_docs_dir,
    get_cache_dir,
    get_logs_dir,
    get_configs_dir,
    get_templates_dir,
    get_instructions_dir,
    get_doc_dir,
    validate_config,
    initialize_project
)

# Get current configuration
config = get_config()
config_manager = get_config_manager()

# Environment checks
if is_development():
    enable_debug_features()
elif is_production():
    optimize_for_performance()

# Get directory paths
docs_dir = get_docs_dir()
cache_dir = get_cache_dir()
logs_dir = get_logs_dir()
configs_dir = get_configs_dir()
templates_dir = get_templates_dir()
instructions_dir = get_instructions_dir()

# Get specific document type directory
arch_dir = get_doc_dir("arch")
impl_dir = get_doc_dir("impl")

# Validate configuration
errors = validate_config()
if errors:
    print(f"Configuration errors: {errors}")

# Initialize project with hybrid configuration
initialize_project()
```

#### Backwards Compatibility Functions

```python
from nexus.core.config import ConfigManager

# Existing API works unchanged
config_manager = ConfigManager()

# All existing methods work
docs_dir = config_manager.get_docs_directory()
is_init = config_manager.is_initialized()
version = config_manager.get("nexus.version")
config_manager.set("custom.value", "test")
config_manager.update_config({"new": "value"})
config_manager.save_config()
errors = config_manager.validate_config()
```

#### Update Functions

```python
from nexus.core.updater import check_project_needs_update, ProjectUpdater

# Check if update is needed
if check_project_needs_update():
    print("Project files need updating")

# Update project files
updater = ProjectUpdater()
updater.update_project_files(force=True)
```

#### Legacy Functions

```python
from nexus.core import load_config, setup_logging

# Load configuration (legacy)
config = load_config("config.yaml")

# Setup logging
setup_logging(level="DEBUG", format="%(levelname)s: %(message)s")
```

## Error Handling

### Exception Classes

- `NexusError`: Base exception class
- `ConfigurationError`: Configuration-related errors
- `ExecutionError`: Instruction execution errors
- `DocumentationError`: Documentation generation errors

### Error Codes

| Code | Description |
|------|-------------|
| `NEXUS_001` | Configuration file not found |
| `NEXUS_002` | Invalid configuration format |
| `NEXUS_003` | Instruction not found |
| `NEXUS_004` | Execution timeout |
| `NEXUS_005` | Documentation generation failed |

## Examples

### Basic Project Setup

```python
from nexus.core import NexusProject

# Create new project
project = NexusProject()
project.initialize("my-project", template="basic")

# Check status
status = project.get_status()
print(f"Project status: {status}")

# Generate documentation
project.generate_documentation()
```

### Custom Instruction

```python
from nexus.core import Instruction, InstructionManager

# Define custom instruction
class DataProcessingInstruction(Instruction):
    def execute(self, context):
        # Process data
        result = self.process_data(context.get('data'))
        return result

# Register and execute
manager = InstructionManager()
manager.register_instruction("data-processing", DataProcessingInstruction())
result = manager.execute_instruction("data-processing", {"data": my_data})
```

---

*For more examples and detailed usage, see the generated documentation in `generated-docs/`.*
