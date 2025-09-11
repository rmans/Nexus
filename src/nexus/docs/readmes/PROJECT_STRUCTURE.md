# Nexus Project Structure

This document outlines the directory structure and organization of the Nexus project.

## Root Directory

```
Nexus/
├── .gitignore                 # Git ignore rules
├── .env.example               # Environment variables template
├── config.yaml                # Main configuration (discoverable in root)
├── LICENSE                    # Project license
├── README.md                  # Main project documentation (modular)
├── setup.py                   # Package setup and installation
├── pyproject.toml             # Modern Python packaging configuration
├── requirements.txt           # Python dependencies
├── generated-docs/            # Auto-generated documentation
├── nexus_docs/               # Project documentation
├── src/                       # Source code
│   └── nexus/                 # Main package
│       ├── cli/               # CLI commands and interface
│       ├── core/              # Core functionality and business logic
│       │   ├── config.py      # Configuration management
│       │   ├── hybrid_config.py # Hybrid configuration system
│       │   ├── updater.py     # Smart update system
│       │   ├── status.py      # Project status management
│       │   └── project_init.py # Project initialization
│       ├── docs/              # Documentation files
│       │   ├── readmes/       # Modular README sections
│       │   └── configs/       # Configuration structure
│       │       ├── environments/ # Environment-specific configs
│       │       ├── templates/    # Configuration templates
│       │       ├── schemas/      # Validation schemas
│       │       └── examples/     # Usage examples
│       └── instructions/      # Instruction definitions
├── .nexus/                    # Runtime configuration
│   ├── config.json           # Runtime overrides
│   ├── cache/                # Cache directory
│   └── logs/                 # Log files
├── .cursor/                   # Cursor AI integration
│   └── rules/                # Cursor rules and commands
├── test/                      # Test files and scripts
└── venv/                      # Python virtual environment
```

## Source Code (`src/`)

The main source code is organized under the `nexus` package:

```
src/
└── nexus/                     # Main package
    ├── cli/                   # CLI commands and interface
    │   └── main.py            # Main CLI entry point
    ├── core/                  # Core functionality and business logic
    │   ├── config.py          # Configuration management
    │   ├── hybrid_config.py   # Hybrid configuration system
    │   ├── updater.py         # Smart update system
    │   ├── status.py          # Project status management
    │   ├── project_init.py    # Project initialization
    │   └── template_discovery.py # Template auto-discovery
    ├── docs/                  # Documentation files
    │   ├── readmes/           # Modular README sections
    │   │   ├── PROJECT_STRUCTURE.md
    │   │   ├── GETTING_STARTED.md
    │   │   ├── REQUIREMENTS.md
    │   │   ├── API_REFERENCE.md
    │   │   ├── INSTALLER_CHECKLIST.md
    │   │   ├── CONTRIBUTING.md
    │   │   └── CHANGELOG.md
    │   └── configs/           # Configuration structure
    │       ├── environments/  # Environment-specific configs
    │       │   ├── development.yaml
    │       │   ├── testing.yaml
    │       │   ├── staging.yaml
    │       │   └── production.yaml
    │       ├── templates/     # Configuration templates
    │       │   ├── config.template.yaml
    │       │   ├── logging.template.yaml
    │       │   └── project.template.yaml
    │       ├── schemas/       # Validation schemas
    │       │   ├── config.schema.json
    │       │   └── environment.schema.json
    │       └── examples/      # Usage examples
    │           ├── serve_example.py
    │           └── docs_example.py
    └── instructions/          # Instruction definitions
```

### Package Structure Details

- **`cli/`**: Command-line interface implementations and command handlers
- **`core/`**: Houses the core business logic, data models, and main application functionality
  - **`config.py`**: Legacy configuration management
  - **`hybrid_config.py`**: Enhanced hybrid configuration system with priority loading
  - **`updater.py`**: Smart update system for project files
  - **`status.py`**: Project status management and reporting
  - **`project_init.py`**: Project initialization and setup
  - **`template_discovery.py`**: Auto-discovery of template files
- **`docs/`**: Project-specific documentation files
  - **`readmes/`**: Modular README sections for organized documentation
  - **`configs/`**: Comprehensive configuration structure
    - **`environments/`**: Environment-specific configuration files
    - **`templates/`**: Configuration templates with variable substitution
    - **`schemas/`**: JSON schemas for configuration validation
    - **`examples/`**: Usage examples and demonstrations
- **`instructions/`**: Instruction definitions and templates

## Testing (`test/`)

```
test/
├── results/                   # Test execution results and reports
└── scripts/                   # Test automation scripts
```

### Test Organization

- **`results/`**: Stores test output, reports, and execution logs
- **`scripts/`**: Contains automated test scripts and testing utilities

## Generated Documentation (`generated-docs/`)

This directory contains auto-generated documentation organized by category:

```
generated-docs/
├── arch/                      # Architecture documentation
├── exec/                      # Execution documentation
├── impl/                      # Implementation details
├── int/                       # Integration documentation
├── prd/                       # Product requirements documentation
├── rules/                     # Business rules and constraints
├── task/                      # Task definitions and workflows
└── tests/                     # Test documentation
```

### Documentation Categories

- **`arch/`**: System architecture diagrams, design documents, and technical specifications
- **`exec/`**: Execution flow documentation, runtime behavior, and operational procedures
- **`impl/`**: Implementation details, code documentation, and technical specifications
- **`int/`**: Integration guides, API documentation, and external system interfaces
- **`prd/`**: Product requirements, feature specifications, and user stories
- **`rules/`**: Business rules, validation logic, and constraint definitions
- **`task/`**: Task definitions, workflow documentation, and process descriptions
- **`tests/`**: Test documentation, test plans, and testing strategies

## Fixed Hybrid Configuration System

Nexus uses a **fixed hybrid configuration system** with full API compatibility and performance optimization:

### Configuration Files

- **`config.yaml`**: Main configuration file in project root (discoverable)
- **`.env.example`**: Environment variables template
- **`.nexus/config.json`**: Runtime configuration overrides
- **`src/nexus/docs/configs/environments/`**: Environment-specific configurations
- **`src/nexus/docs/configs/templates/`**: Configuration templates
- **`src/nexus/docs/configs/schemas/`**: JSON schemas for validation
- **`src/nexus/docs/configs/examples/`**: Usage examples

### Configuration Priority (Highest to Lowest)

1. **Environment Variables** (`NEXUS_*`) - Runtime overrides
2. **Runtime Config** (`.nexus/config.json`) - Session-specific settings
3. **Environment-Specific** (`environments/{env}.yaml`) - Environment overrides
4. **Main Config** (`config.yaml`) - Project root configuration

### Configuration Structure

```
config.yaml                          # Main configuration (project root)
├── project: {name, version, description}
├── environment: "development"
├── directories: {docs, cache, logs}
├── logging: {level, format, file, max_size, backup_count}
├── execution: {max_parallel, timeout, retry_attempts}
├── documentation: {formats, auto_generate}
├── server: {host, port}
└── features: {auto_reload, debug_mode, experimental_features}

src/nexus/docs/configs/
├── environments/
│   ├── development.yaml            # Development settings
│   ├── testing.yaml                # Testing configuration
│   ├── staging.yaml                # Staging environment
│   └── production.yaml             # Production settings
├── templates/
│   ├── config.template.yaml        # Main config template
│   ├── logging.template.yaml       # Logging template
│   └── project.template.yaml       # Project template
├── schemas/
│   ├── config.schema.json          # Configuration schema
│   └── environment.schema.json     # Environment schema
└── examples/
    ├── serve_example.py            # Server example
    └── docs_example.py             # Documentation example
```

### Runtime Directories

- **`.nexus/`**: Runtime configuration and data
  - **`config.json`**: Runtime overrides and session data
  - **`cache/`**: Cache directory for temporary files
  - **`logs/`**: Log files and execution logs
  - **`instructions/`**: Instruction definitions
- **`.cursor/`**: Cursor AI integration
  - **`rules/`**: Cursor rules and command definitions

## Professional Installer System

Nexus includes a comprehensive cross-platform installer system:

### Installer Files

- **`install.py`**: Python-based installer with rich UI (cross-platform)
- **`install.sh`**: Unix/Linux installation script
- **`install.bat`**: Windows installation script
- **`install-macos.sh`**: macOS installation with Homebrew support

### Installer Features

- **Cross-platform Support**: Windows, macOS, Linux
- **Hybrid Configuration Setup**: Installs all configuration layers
- **Environment Detection**: Automatic environment setup
- **PATH Configuration**: Command-line access setup
- **Dependency Management**: Automatic dependency installation
- **Verification**: Post-installation testing and validation
- **Uninstallation**: Complete removal support

### Installation Process

1. **Prerequisites Check**: Python 3.8+, pip, platform-specific requirements
2. **Configuration Installation**: Main config, environment configs, templates, schemas
3. **Documentation Setup**: Comprehensive documentation and examples
4. **Runtime Environment**: `.nexus/` directory structure and configuration
5. **Command-line Access**: PATH setup and wrapper scripts
6. **Verification**: Installation testing and status checking

## Development Environment

- **`venv/`**: Python virtual environment for dependency isolation
- **`.gitignore`**: Git ignore rules for version control

## Project Status

Based on the current structure, this appears to be a Python project in early development stages with:

- Well-organized directory structure following Python best practices
- Comprehensive documentation generation system
- Modular architecture with clear separation of concerns
- Testing infrastructure in place
- Virtual environment for dependency management

## Getting Started

1. Activate the virtual environment: `source venv/bin/activate`
2. Install dependencies (if requirements file exists)
3. Run tests from the `test/` directory
4. Check generated documentation in `generated-docs/`
5. Read the modular documentation in `src/nexus/docs/readmes/`

## Documentation Structure

The project uses a modular documentation approach:

- **Main README**: Overview and navigation to all documentation sections
- **Modular READMEs**: Located in `src/nexus/docs/readmes/` for organized, focused content
- **Generated Docs**: Auto-generated technical documentation in `generated-docs/`

## Notes

- The project appears to be in early development with empty core directories
- Documentation is auto-generated and organized by category
- The structure suggests a command-line tool or application framework
- Testing infrastructure is prepared but may need implementation

---

*This document is maintained alongside the project structure. Update it when significant organizational changes are made.*
