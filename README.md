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
- ⚙️ **Hybrid Configuration System** - Multi-layer configuration with environment-specific overrides
- 🔄 **Smart Update System** - Automatic detection and seamless updates of project files
- 🎯 **Cursor Integration** - Built-in support for Cursor AI assistant with rule management
- 📊 **Documentation Generation** - Automated documentation generation from code
- 🌍 **Environment Management** - Development, testing, staging, and production configurations

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd Nexus

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
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
```

## Configuration

Nexus uses a hybrid configuration system with multiple layers:

### Main Configuration (`config.yaml`)
```yaml
project:
  name: "My Project"
  version: "1.0.0"
  description: "AI-assisted development project"

environment: "development"

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

features:
  auto_reload: true
  debug_mode: false
  experimental_features: false
```

### Environment-Specific Configs
- `src/nexus/docs/configs/environments/development.yaml`
- `src/nexus/docs/configs/environments/testing.yaml`
- `src/nexus/docs/configs/environments/staging.yaml`
- `src/nexus/docs/configs/environments/production.yaml`

### Environment Variables
```bash
# Override any configuration with NEXUS_* environment variables
export NEXUS_ENV=production
export NEXUS_DEBUG=true
export NEXUS_LOG_LEVEL=DEBUG
export NEXUS_FEATURE_AUTO_RELOAD=true
```

## Project Structure

```
Nexus/
├── config.yaml                # Main configuration (discoverable in root)
├── .env.example               # Environment variables template
├── src/nexus/                 # Main package
│   ├── cli/                   # CLI commands and interface
│   ├── core/                  # Core functionality
│   │   ├── config.py          # Configuration management
│   │   ├── hybrid_config.py   # Hybrid configuration system
│   │   ├── updater.py         # Smart update system
│   │   └── status.py          # Project status management
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
├── test/                     # Test files
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