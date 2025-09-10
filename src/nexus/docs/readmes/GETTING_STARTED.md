# Getting Started with Nexus

This guide will help you get up and running with the Nexus project quickly.

## Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment support (venv, conda, or similar)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Nexus
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install project dependencies
pip install -r requirements.txt

# Or if using development dependencies
pip install -r requirements-dev.txt
```

## Quick Start

### 1. Verify Installation

```bash
# Check if Nexus is properly installed
python -m nexus --version
```

### 2. Run Basic Commands

```bash
# Get help
python -m nexus --help

# List available commands
python -m nexus list-commands
```

### 3. Run Tests

```bash
# Run all tests
python -m pytest test/

# Run specific test category
python -m pytest test/scripts/
```

## Configuration

### Environment Setup

1. Copy the example configuration file:
   ```bash
   cp config.example.yaml config.yaml
   ```

2. Edit `config.yaml` with your specific settings

### First Run

1. Initialize the project:
   ```bash
   python -m nexus init
   ```

2. Verify setup:
   ```bash
   python -m nexus status
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
