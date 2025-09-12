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

# Validate project configuration
nexus validate
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

### 4. Content Management

```bash
# Analyze existing content
nexus analyze-content

# Migrate content to new structure
nexus migrate-content

# Enhance content quality
nexus enhance-content --preview
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

- **🔍 Advanced Code Analysis** - Sophisticated analysis of project structure, dependencies, and patterns
- **📊 Comprehensive Framework Detection** - Identifies Click, Rich, Jinja2, PyYAML, pytest, and 20+ frameworks
- **🏗️ Intelligent Architecture Classification** - Detects CLI applications, development frameworks, and architectural patterns
- **💡 Professional Insights** - Provides specific, actionable recommendations and quality assessments
- **⚡ Performance Caching** - Caches results for faster subsequent analyses
- **📄 Report Management** - Save, list, and view discovery reports with DISC-YYYY-MM-DD-Title naming
- **🎯 Entry Point Detection** - Discovers CLI commands and application entry points
- **🔧 Pattern Recognition** - Detects plugin architecture, template systems, hybrid configuration

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

# Save discovery reports
nexus discover --save "Project Analysis"
nexus discover --deep --save "Deep Analysis Report"

# Manage discovery reports
nexus discovery list
nexus discovery view DISC-2025-09-11-Project-Analysis
```

### Discovery System

The Discovery System provides comprehensive code analysis with report management:

#### Quick Discovery Examples

```bash
# Basic discovery
nexus discover

# Deep analysis with detailed insights
nexus discover --deep

# JSON output for integration
nexus discover --output json

# Language-specific analysis
nexus discover --languages python,javascript

# Save discovery reports
nexus discover --save "Project Analysis"
nexus discover --deep --save "Deep Analysis Report"

# Manage discovery reports
nexus discovery list
nexus discovery view DISC-2025-09-11-Project-Analysis
```

#### Report Management

Discovery reports are automatically saved with the naming convention `DISC-YYYY-MM-DD-Title.md` and include:

- **Frontmatter Metadata** - Analysis timestamp, options, and configuration
- **Executive Summary** - High-level project overview and key findings
- **Quality Assessment** - Code quality score, test coverage, documentation status
- **Architecture Analysis** - Project type, complexity, patterns detected
- **Insights & Recommendations** - Actionable suggestions for improvement
- **Tech Stack Summary** - Main languages, frameworks, and tools identified

Reports are stored in `nexus_docs/discovery/` and automatically indexed for easy management.

#### Enhanced Discovery Capabilities

The Discovery System now provides sophisticated analysis with advanced capabilities:

**Framework Detection:**
- Parses `pyproject.toml` for modern Python dependencies
- Detects Click, Rich, Jinja2, PyYAML, pytest, MkDocs, Black, Flake8, psutil, setuptools
- Identifies CLI frameworks and development tools

**Architecture Classification:**
- CLI Application detection
- Development Framework classification  
- Plugin Architecture recognition
- Template System detection
- Hybrid Configuration detection
- Cross-platform installer detection

**Quality Assessment:**
- Advanced scoring (0-100) with CLI framework bonuses
- CLI Application: +15 points
- Plugin Architecture: +10 points
- Template System: +5 points
- Hybrid Configuration: +5 points
- Cross-platform: +5 points
- Rich Output: +5 points
- Documentation System: +10 bonus points

**Pattern Recognition:**
- `cli_application` - Command-line applications
- `plugin_architecture` - Modular plugin systems
- `template_system` - Template-driven content generation
- `hybrid_configuration` - Multi-layer configuration systems
- `cross_platform` - Cross-platform installer support
- `documentation_system` - Comprehensive documentation systems
- `rich_output` - Professional console interfaces

## Configuration

### Hybrid Configuration System

Nexus uses a **hybrid configuration system** with full API compatibility and performance optimization:

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
