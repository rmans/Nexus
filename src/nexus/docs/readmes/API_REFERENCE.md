# API Reference

This document provides detailed information about the Nexus API, commands, and interfaces.

## Command Line Interface

### Basic Usage

```bash
python -m nexus [OPTIONS] COMMAND [ARGS]...
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

##### `init`
Initialize a new Nexus project or workspace.

```bash
python -m nexus init [OPTIONS]
```

**Options:**
- `--force`: Overwrite existing configuration
- `--template`: Use specific template
- `--directory`: Target directory for initialization

**Example:**
```bash
python -m nexus init --template basic --directory ./my-project
```

##### `status`
Show current project status and configuration.

```bash
python -m nexus status [OPTIONS]
```

**Options:**
- `--detailed`: Show detailed status information
- `--json`: Output in JSON format

**Example:**
```bash
python -m nexus status --detailed
```

##### `list-commands`
List all available commands.

```bash
python -m nexus list-commands [OPTIONS]
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

### Configuration File

The main configuration is stored in `config.yaml`:

```yaml
# Nexus Configuration
project:
  name: "Nexus"
  version: "1.0.0"
  description: "A modular project framework"

# Logging configuration
logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "nexus.log"

# Documentation settings
documentation:
  output_dir: "generated-docs"
  formats: ["html", "markdown"]
  auto_generate: true

# Execution settings
execution:
  max_parallel: 4
  timeout: 300
  retry_attempts: 3
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXUS_CONFIG` | Path to configuration file | `config.yaml` |
| `NEXUS_LOG_LEVEL` | Logging level | `INFO` |
| `NEXUS_DEBUG` | Enable debug mode | `false` |
| `NEXUS_OUTPUT_DIR` | Default output directory | `./output` |

## Python API

### Core Classes

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

#### `load_config(config_path)`

Load configuration from file.

```python
from nexus.core import load_config

config = load_config("config.yaml")
```

#### `setup_logging(level, format)`

Configure logging for the application.

```python
from nexus.core import setup_logging

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
