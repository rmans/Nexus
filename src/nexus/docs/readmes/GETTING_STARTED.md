# Getting Started with Nexus

This guide will help you get up and running with the Nexus project quickly.

## Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment support (venv, conda, or similar)

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
# Install Nexus globally
pip install nexus-context

# Verify installation
nexus --version
```

### Option 2: Development Installation

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

## Configuration

### Hybrid Configuration System

Nexus uses a hybrid configuration system with multiple layers:

1. **Main Config** (`config.yaml`) - Core project settings in project root
2. **Environment Config** - Environment-specific overrides
3. **Runtime Config** (`.nexus/config.json`) - Runtime changes
4. **Environment Variables** (`NEXUS_*`) - System environment overrides

### Environment Setup

1. **Main Configuration**: Edit `config.yaml` in your project root
2. **Environment Variables**: Copy `.env.example` to `.env` and customize
3. **Environment-Specific**: Modify files in `src/nexus/docs/configs/environments/`

### Configuration Examples

```yaml
# config.yaml
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

```bash
# .env
NEXUS_ENV=development
NEXUS_DEBUG=true
NEXUS_LOG_LEVEL=DEBUG
NEXUS_FEATURE_AUTO_RELOAD=true
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
