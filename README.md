# Nexus

A modular project framework designed for scalable development and comprehensive documentation.

## Overview

Nexus is a Python-based project framework that provides a structured approach to development with built-in documentation generation, modular architecture, and comprehensive testing infrastructure.

## Quick Start

🚀 **New to Nexus?** Start with our [Getting Started Guide](src/nexus/docs/readmes/GETTING_STARTED.md) to get up and running quickly.

## Documentation

Our documentation is organized into focused, modular sections:

### 📚 Core Documentation

- **[Getting Started](src/nexus/docs/readmes/GETTING_STARTED.md)** - Installation, setup, and quick start guide
- **[Requirements](src/nexus/docs/readmes/REQUIREMENTS.md)** - Functional and non-functional requirements
- **[Project Structure](src/nexus/docs/readmes/PROJECT_STRUCTURE.md)** - Detailed directory structure and organization
- **[API Reference](src/nexus/docs/readmes/API_REFERENCE.md)** - Complete API documentation and command reference
- **[Installer Checklist](src/nexus/docs/readmes/INSTALLER_CHECKLIST.md)** - Installer development and testing guide
- **[Contributing](src/nexus/docs/readmes/CONTRIBUTING.md)** - Guidelines for contributing to the project
- **[Changelog](src/nexus/docs/readmes/CHANGELOG.md)** - Project history and version changes

### 🔧 Generated Documentation

Auto-generated technical documentation is available in the `generated-docs/` directory:

- **Architecture** (`generated-docs/arch/`) - System design and technical specifications
- **Implementation** (`generated-docs/impl/`) - Code documentation and technical details
- **Integration** (`generated-docs/int/`) - API documentation and external interfaces
- **Execution** (`generated-docs/exec/`) - Runtime behavior and operational procedures
- **Testing** (`generated-docs/tests/`) - Test documentation and strategies

## Features

- 🏗️ **Modular Architecture** - Clean separation of concerns with organized package structure
- 📖 **Comprehensive Documentation** - Auto-generated docs with modular README sections
- 🧪 **Testing Infrastructure** - Built-in testing framework with organized test structure
- ⚙️ **Hybrid Configuration System** - Multi-layer configuration with full API compatibility and performance optimization
- 🔄 **Smart Update System** - Automatic detection and seamless updates of project files
- 🔍 **Discovery System** - Automatic code analysis, pattern recognition, and intelligent insights with report management
- 🎯 **Cursor Integration** - Built-in support for Cursor AI assistant with rule management
- 📊 **Documentation Generation** - Automated documentation generation from code
- 🌍 **Environment Management** - Development, testing, staging, and production configurations
- 🚀 **Professional Installer** - Cross-platform installation with hybrid configuration support
- 🔧 **Configuration Templates** - Pre-built templates and schemas for easy setup
- 📄 **Report Management** - Save, list, and view discovery reports with DISC-YYYY-MM-DD-Title naming
- 🎨 **Rich CLI Interface** - Beautiful console output with progress indicators and colored output

## Installation

### Quick Install (Recommended)
```bash
# Install from PyPI
pip install nexus-context

# Or install from source
git clone https://github.com/rmans/Nexus.git
cd Nexus
pip install -e .
```

### Professional Installer
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

### Development Installation
```bash
# Clone the repository
git clone https://github.com/rmans/Nexus.git
cd Nexus

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Basic Usage

```bash
# Install Nexus
pip install nexus-context

# Initialize a new project
nexus init-project

# Check project status and updates
nexus status

# Update project files to latest version
nexus update-project

# Generate documentation
nexus generate-docs

# Serve documentation locally
nexus serve-docs

# Run comprehensive tests
nexus test-all

# Discover and analyze codebase
nexus discover
nexus discover --deep
nexus discover --output json

# Save discovery reports
nexus discover --save "Project Analysis"
nexus discover --deep --save "Deep Analysis Report"

# Manage discovery reports
nexus discovery list
nexus discovery view DISC-2025-09-11-Project-Analysis
```

## Discovery System

Nexus includes a powerful **Discovery System** that automatically analyzes your codebase to understand structure, dependencies, patterns, and quality:

### Key Features
- 🔍 **Advanced Code Analysis** - Sophisticated analysis of project structure, dependencies, and patterns
- 📊 **Comprehensive Framework Detection** - Identifies Click, Rich, Jinja2, PyYAML, pytest, and 20+ frameworks
- 🏗️ **Intelligent Architecture Classification** - Detects CLI applications, development frameworks, and architectural patterns
- 💡 **Professional Insights** - Provides specific, actionable recommendations and quality assessments
- ⚡ **Performance Caching** - Caches results for faster subsequent analyses
- 📄 **Report Management** - Save, list, and view discovery reports with DISC-YYYY-MM-DD-Title naming
- 🎯 **CLI Integration** - Easy-to-use command-line interface with rich output

### Discovery Commands
```bash
# Basic discovery
nexus discover [path]

# Deep analysis with detailed insights
nexus discover --deep

# JSON output for integration
nexus discover --output json

# Language-specific analysis
nexus discover --languages python,javascript

# Use cached results
nexus discover --cache

# Clear discovery cache
nexus discover --clear-cache

# Save discovery reports
nexus discover --save "Project Analysis"
nexus discover --deep --save "Deep Analysis Report"

# Manage discovery reports
nexus discovery list
nexus discovery view DISC-2025-09-11-Project-Analysis
```

### Discovery Output
The Discovery System provides:
- **Project Overview** - File count, size, languages, frameworks
- **Quality Assessment** - Advanced scoring (0-100) with CLI framework bonuses
- **Architecture Analysis** - Intelligent classification (CLI apps, development frameworks, etc.)
- **Professional Insights** - Specific recommendations for CLI frameworks, plugin architecture, etc.
- **Tech Stack Summary** - Accurate stack type detection and framework identification
- **Entry Point Detection** - Discovers CLI commands and application entry points
- **Pattern Recognition** - Detects plugin architecture, template systems, hybrid configuration
- **Comprehensive Reports** - Detailed markdown reports with frontmatter metadata
- **Report Management** - Save, list, and view discovery reports with consistent naming

## Configuration

Nexus uses a **hybrid configuration system** with full API compatibility and performance optimization:

### Configuration Priority (Highest to Lowest)
1. **Environment Variables** (`NEXUS_*`) - Runtime overrides
2. **Runtime Config** (`.nexus/config.json`) - Session-specific settings
3. **Environment-Specific** (`src/nexus/docs/configs/environments/{env}.yaml`) - Environment overrides
4. **Main Config** (`config.yaml`) - Project root configuration

### Main Configuration (`config.yaml`)
```yaml
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

### Environment-Specific Configs
- `src/nexus/docs/configs/environments/development.yaml` - Development settings
- `src/nexus/docs/configs/environments/testing.yaml` - Testing configuration
- `src/nexus/docs/configs/environments/staging.yaml` - Staging environment
- `src/nexus/docs/configs/environments/production.yaml` - Production settings

### Configuration Templates & Schemas
- `src/nexus/docs/configs/templates/` - Configuration templates
- `src/nexus/docs/configs/schemas/` - JSON schemas for validation

### Environment Variables
```bash
# Override any configuration with NEXUS_* environment variables
export NEXUS_ENV=production
export NEXUS_DEBUG=true
export NEXUS_LOG_LEVEL=DEBUG
export NEXUS_OUTPUT_DIR=./prod-docs
export NEXUS_MAX_PARALLEL=8
export NEXUS_FEATURE_AUTO_RELOAD=true
export NEXUS_FEATURE_DEBUG_MODE=false
```

### API Compatibility
The configuration system maintains full backwards compatibility:
```python
from nexus.core.config import ConfigManager

# Existing API works unchanged
config_manager = ConfigManager()
docs_dir = config_manager.get_docs_directory()
is_init = config_manager.is_initialized()

# New enhanced API
from nexus.core.hybrid_config import get_config, is_debug, is_development
config = get_config()
debug_mode = is_debug()
dev_mode = is_development()
```

## Project Structure

```
Nexus/
├── config.yaml                # Main configuration (discoverable in root)
├── .env.example               # Environment variables template
├── src/nexus/                 # Main package
│   ├── cli/                   # CLI commands and interface
│   │   └── discover.py        # Discovery CLI commands
│   ├── core/                  # Core functionality
│   │   ├── config.py          # Configuration management
│   │   ├── hybrid_config.py   # Hybrid configuration system
│   │   ├── updater.py         # Smart update system
│   │   ├── status.py          # Project status management
│   │   ├── version.py         # Centralized version management
│   │   └── discovery/         # Discovery System
│   │       ├── engine.py      # Main discovery orchestrator
│   │       ├── analyzer.py    # Code analysis engine
│   │       ├── synthesizer.py # Data synthesis and insights
│   │       ├── validator.py   # Result validation
│   │       ├── cache.py       # Caching system
│   │       ├── outputs.py     # Output formatting
│   │       └── reports.py     # Report management
│   ├── docs/                  # Documentation system
│   │   ├── readmes/           # Modular documentation
│   │   └── configs/           # Configuration structure
│   │       ├── environments/  # Environment-specific configs
│   │       ├── templates/     # Configuration templates
│   │       ├── schemas/       # Validation schemas
│   │       └── examples/      # Usage examples
│   └── instructions/          # Instruction definitions
├── .nexus/                    # Runtime configuration
│   ├── config.json           # Runtime overrides
│   ├── cache/                # Cache directory
│   └── logs/                 # Log files
├── .cursor/                   # Cursor AI integration
│   └── rules/                # Cursor rules and commands
├── nexus_docs/               # Project documentation
│   └── discovery/            # Discovery reports
│       ├── index.md          # Discovery reports index
│       └── DISC-*.md         # Discovery reports
├── test/                     # Test files
│   └── discovery/            # Discovery system tests
└── venv/                     # Virtual environment
```

## Development

### Prerequisites

- Python 3.8+
- Git
- Virtual environment support

### Setup

1. Fork and clone the repository
2. Set up development environment (see [Contributing Guide](src/nexus/docs/readmes/CONTRIBUTING.md))
3. Install development dependencies
4. Run tests to verify setup

### Contributing

We welcome contributions! Please see our [Contributing Guidelines](src/nexus/docs/readmes/CONTRIBUTING.md) for:

- Development setup
- Coding standards
- Testing requirements
- Pull request process
- Code of conduct

## License

This project is licensed under the [LICENSE](LICENSE) file.

## Support

- 📖 **Documentation**: Check the modular documentation in `src/nexus/docs/readmes/`
- 🐛 **Issues**: Report bugs and request features via GitHub Issues
- 💬 **Discussions**: Join community discussions for questions and ideas
- 📧 **Contact**: Reach out to maintainers for direct support

## Status

[![Project Status](https://img.shields.io/badge/status-early%20development-yellow)](https://github.com/your-username/Nexus)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

**Ready to get started?** Check out our [Getting Started Guide](src/nexus/docs/readmes/GETTING_STARTED.md) or explore the [Project Structure](src/nexus/docs/readmes/PROJECT_STRUCTURE.md) to understand how Nexus is organized.