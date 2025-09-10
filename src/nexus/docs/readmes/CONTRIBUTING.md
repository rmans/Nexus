# Contributing to Nexus

Thank you for your interest in contributing to Nexus! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment (venv, conda, or similar)
- Code editor with Python support

### Development Setup

1. **Review Requirements**
   - Read the [Requirements](REQUIREMENTS.md) to understand project specifications
   - Familiarize yourself with functional and non-functional requirements

2. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/Nexus.git
   cd Nexus
   ```

3. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install development dependencies
   pip install -r requirements-dev.txt
   pip install -e .
   ```

4. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

## Development Workflow

### Branch Strategy

- `main`: Stable, production-ready code
- `develop`: Integration branch for features
- `feature/*`: Feature development branches
- `bugfix/*`: Bug fix branches
- `hotfix/*`: Critical bug fixes

### Making Changes

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clean, well-documented code
   - Follow the coding standards (see below)
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   # Run all tests
   python -m pytest
   
   # Run specific test file
   python -m pytest test/test_specific.py
   
   # Run with coverage
   python -m pytest --cov=nexus
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line Length**: 88 characters (Black formatter default)
- **Imports**: Use absolute imports, group by standard library, third-party, local
- **Docstrings**: Use Google style docstrings
- **Type Hints**: Use type hints for all function parameters and return values

### Code Formatting

We use Black for code formatting and isort for import sorting:

```bash
# Format code
black nexus/ test/

# Sort imports
isort nexus/ test/
```

### Linting

We use flake8 for linting:

```bash
# Run linter
flake8 nexus/ test/
```

### Example Code Style

```python
"""Example module demonstrating code style."""

from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class ExampleClass:
    """Example class demonstrating proper documentation and type hints."""
    
    def __init__(self, name: str, config: Optional[Dict] = None) -> None:
        """Initialize the example class.
        
        Args:
            name: The name of the instance
            config: Optional configuration dictionary
        """
        self.name = name
        self.config = config or {}
    
    def process_data(self, data: List[str]) -> Dict[str, int]:
        """Process a list of strings and return counts.
        
        Args:
            data: List of strings to process
            
        Returns:
            Dictionary mapping strings to their counts
            
        Raises:
            ValueError: If data is empty
        """
        if not data:
            raise ValueError("Data cannot be empty")
        
        return {item: data.count(item) for item in set(data)}
```

## Testing Guidelines

### Test Structure

- Place tests in the `test/` directory
- Mirror the source code structure
- Use descriptive test names
- Group related tests in classes

### Test Naming

```python
def test_function_name_should_do_something_when_condition():
    """Test that function_name does something when condition is met."""
    # Test implementation
    pass
```

### Test Categories

- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows

### Example Test

```python
"""Tests for the ExampleClass."""

import pytest
from nexus.core import ExampleClass


class TestExampleClass:
    """Test cases for ExampleClass."""
    
    def test_init_with_name_only(self):
        """Test initialization with name only."""
        instance = ExampleClass("test")
        assert instance.name == "test"
        assert instance.config == {}
    
    def test_init_with_config(self):
        """Test initialization with name and config."""
        config = {"key": "value"}
        instance = ExampleClass("test", config)
        assert instance.name == "test"
        assert instance.config == config
    
    def test_process_data_with_valid_input(self):
        """Test process_data with valid input."""
        instance = ExampleClass("test")
        data = ["a", "b", "a", "c"]
        result = instance.process_data(data)
        expected = {"a": 2, "b": 1, "c": 1}
        assert result == expected
    
    def test_process_data_with_empty_input(self):
        """Test process_data raises ValueError with empty input."""
        instance = ExampleClass("test")
        with pytest.raises(ValueError, match="Data cannot be empty"):
            instance.process_data([])
```

## Documentation

### Code Documentation

- Use docstrings for all public functions, classes, and methods
- Include type hints for better IDE support
- Add inline comments for complex logic

### README Updates

- Update relevant README sections when adding features
- Keep examples current and working
- Add new sections to the modular documentation structure

### API Documentation

- Update API reference when changing interfaces
- Include examples for new functions
- Document breaking changes clearly

## Pull Request Process

### Before Submitting

1. **Ensure Tests Pass**
   ```bash
   python -m pytest
   ```

2. **Check Code Style**
   ```bash
   black --check nexus/ test/
   isort --check-only nexus/ test/
   flake8 nexus/ test/
   ```

3. **Update Documentation**
   - Update relevant README sections
   - Add/update docstrings
   - Update API reference if needed

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] All existing tests still pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and linting
2. **Code Review**: At least one maintainer reviews the code
3. **Testing**: Manual testing may be required for complex changes
4. **Approval**: Maintainer approves and merges the PR

## Issue Reporting

### Bug Reports

When reporting bugs, include:

- **Description**: Clear description of the issue
- **Steps to Reproduce**: Detailed steps to reproduce the bug
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: OS, Python version, package versions
- **Logs**: Relevant error messages or logs

### Feature Requests

When requesting features, include:

- **Description**: Clear description of the feature
- **Use Case**: Why this feature is needed
- **Proposed Solution**: How you think it should work
- **Alternatives**: Other solutions you've considered

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the golden rule

### Getting Help

- **Requirements**: Review the [Requirements](REQUIREMENTS.md) for project specifications
- **Documentation**: Check existing documentation first
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions
- **Discord/Slack**: Join our community channels

## Release Process

### Version Numbering

We use Semantic Versioning (SemVer):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number updated
- [ ] CHANGELOG.md updated
- [ ] Release notes prepared
- [ ] Tag created
- [ ] Package published

## License

By contributing to Nexus, you agree that your contributions will be licensed under the same license as the project.

---

*Thank you for contributing to Nexus! Your contributions help make this project better for everyone.*
