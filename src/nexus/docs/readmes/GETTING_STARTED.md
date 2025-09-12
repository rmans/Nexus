# Getting Started with Nexus

This guide will help you get up and running with the Nexus project quickly.

## Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment support (venv, conda, or similar)

## Installation

### Option 1: Professional Installer (Recommended)

Nexus includes cross-platform installation scripts with hybrid configuration support:

```bash
# Python installer (cross-platform)
python install.py

# Unix/Linux
./install.sh

# Windows
install.bat

# macOS (with Homebrew support)
./install-macos.sh

# Check installation status
python install.py --check
```

### Option 2: Install from PyPI

```bash
# Install Nexus globally
pip install nexus-context

# Verify installation
nexus --version
```

### Option 3: Development Installation

```bash
# Clone the repository
git clone https://github.com/rmans/Nexus.git
cd Nexus

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install in development mode
pip install -e .
```

## Quick Start

### 1. Initialize a New Project

```bash
# Create a new Nexus project
nexus init-project

# Check project status
nexus status

# Update project files to latest version
nexus update-project
```

### 2. Explore Available Commands

```bash
# Get help
nexus --help

# List available commands
nexus list-commands

# Check project status with details
nexus status --detailed
```

### 3. Generate and Serve Documentation

```bash
# Generate project documentation
nexus generate-docs

# Serve documentation locally
nexus serve-docs

# Run comprehensive tests
nexus test-all
```

## Discovery System

Nexus includes a powerful **Discovery System** that automatically analyzes your codebase to understand structure, dependencies, patterns, and quality.

### Quick Discovery

```bash
# Basic discovery of current directory
nexus discover

# Deep analysis with detailed insights
nexus discover --deep

# Analyze specific directory
nexus discover /path/to/project

# JSON output for integration
nexus discover --output json
```

### Discovery Features

- **🔍 Automatic Code Analysis** - Analyzes project structure, dependencies, and patterns
- **📊 Language Detection** - Identifies programming languages and frameworks used
- **🏗️ Architectural Pattern Recognition** - Detects design patterns and architectural styles
- **💡 Intelligent Insights** - Provides recommendations and quality assessments
- **⚡ Performance Caching** - Caches results for faster subsequent analyses

### Discovery Output

The Discovery System provides:
- **Project Overview** - File count, size, languages, frameworks
- **Quality Assessment** - Code quality score, test coverage, documentation status
- **Architecture Analysis** - Project type, complexity, patterns
- **Insights & Recommendations** - Actionable suggestions for improvement
- **Tech Stack Summary** - Main languages, frameworks, and tools

### Advanced Discovery

```bash
# Language-specific analysis
nexus discover --languages python,javascript

# Use cached results for faster analysis
nexus discover --cache

# Clear discovery cache
nexus discover --clear-cache

# Deep analysis with caching
nexus discover --deep --cache
```

## Configuration

### Fixed Hybrid Configuration System

Nexus uses a **fixed hybrid configuration system** with full API compatibility and performance optimization:

#### Configuration Priority (Highest to Lowest)
1. **Environment Variables** (`NEXUS_*`) - Runtime overrides
2. **Runtime Config** (`.nexus/config.json`) - Session-specific settings
3. **Environment-Specific** (`src/nexus/docs/configs/environments/{env}.yaml`) - Environment overrides
4. **Main Config** (`config.yaml`) - Project root configuration

#### Environment Setup

1. **Main Configuration**: Edit `config.yaml` in your project root
2. **Environment Variables**: Copy `.env.example` to `.env` and customize
3. **Environment-Specific**: Modify files in `src/nexus/docs/configs/environments/`
4. **Templates & Schemas**: Use files in `src/nexus/docs/configs/templates/` and `schemas/`

#### Configuration Examples

```yaml
# config.yaml
project:
  name: "My Project"
  version: "1.0.0"
  description: "AI-assisted development project"

environment: "development"

directories:
  docs: "generated-docs"
  cache: ".nexus/cache"
  logs: ".nexus/logs"

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "nexus.log"
  max_size: 10485760  # 10MB
  backup_count: 5

execution:
  max_parallel: 4
  timeout: 300
  retry_attempts: 3

documentation:
  formats: ["html", "markdown"]
  auto_generate: true

features:
  auto_reload: true
  debug_mode: false
  experimental_features: false
```

```bash
# .env
NEXUS_ENV=development
NEXUS_DEBUG=true
NEXUS_LOG_LEVEL=DEBUG
NEXUS_OUTPUT_DIR=./dev-docs
NEXUS_MAX_PARALLEL=2
NEXUS_FEATURE_AUTO_RELOAD=true
NEXUS_FEATURE_DEBUG_MODE=true
```

#### API Compatibility

The configuration system maintains full backwards compatibility:

```python
# Existing API works unchanged
from nexus.core.config import ConfigManager
config_manager = ConfigManager()
docs_dir = config_manager.get_docs_directory()
is_init = config_manager.is_initialized()

# New enhanced API
from nexus.core.hybrid_config import get_config, is_debug, is_development
config = get_config()
debug_mode = is_debug()
dev_mode = is_development()
```

## Development Setup

### Code Style

The project follows PEP 8 guidelines. Install pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

### Running in Development Mode

```bash
# Install in development mode
pip install -e .

# Run with debug logging
python -m nexus --debug <command>
```

## Troubleshooting

### Common Issues

1. **Virtual Environment Issues**
   - Ensure you're using the correct Python version
   - Try recreating the virtual environment

2. **Import Errors**
   - Verify the project is installed: `pip list | grep nexus`
   - Check PYTHONPATH if running from different directory

3. **Permission Errors**
   - Ensure proper file permissions
   - Check if running in the correct directory

### Getting Help

- Check the [Requirements](REQUIREMENTS.md) for project specifications and constraints
- Review the [API Reference](API_REFERENCE.md) for detailed command documentation
- See the [Project Structure](PROJECT_STRUCTURE.md) for understanding the codebase
- Read the [Contributing Guidelines](CONTRIBUTING.md) for development practices

## Next Steps

- Review the [Requirements](REQUIREMENTS.md) to understand project specifications
- Explore the [API Reference](API_REFERENCE.md) to understand available commands
- Check out the [Project Structure](PROJECT_STRUCTURE.md) to understand the codebase
- Read the [Contributing Guidelines](CONTRIBUTING.md) if you want to contribute

---

*For more detailed information, see the other documentation files in this directory.*
