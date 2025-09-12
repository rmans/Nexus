---
title: Enhanced Analysis Test
type: discovery
date: 2025-09-11
target_path: /home/rmans/projects/Nexus
analysis_timestamp: 2025-09-11T21:11:52.364222
engine_version: 1.0.0
deep_analysis: True
languages: json, markdown, python, shell, yaml
frameworks: pytest, click, rich, jinja2, pyyaml
---

# Enhanced Analysis Test

**Analysis Date:** 2025-09-11 21:11:52
**Target Path:** `/home/rmans/projects/Nexus`

## Executive Summary

This discovery analysis examined **99 files** totaling **485.8 KB** across **5 programming languages** (json, markdown, python, shell, yaml).

**Quality Score:** 100/100 (excellent)
**Architecture Type:** cli_application
**Application Type:** cli_framework

## Project Overview

- **Total Files:** 99
- **Total Size:** 485.8 KB
- **Languages:** json, markdown, python, shell, yaml
- **Frameworks:** pytest, click, rich, jinja2, pyyaml
- **Lines of Code:** 7,333

## Quality Assessment

**Overall Score:** 100/100 (excellent)

| Metric | Value |
|--------|-------|
| Has Tests | ✅ Yes |
| Has Documentation | ✅ Yes |
| Is Containerized | ❌ No |
| Test Files | 5 |
| Lines of Code | 7,333 |

## Architecture Analysis

**Type:** cli_application
**Application Type:** cli_framework
**Complexity:** high

**Detected Patterns:**
- Has Tests
- Documented
- Cli Application
- Rich Output
- Template System
- Hybrid Configuration
- Documentation System

## Key Insights

- Multi-language project using json, markdown, python, shell, yaml
- Professional CLI development framework with Click and Rich console interface
- Template-driven content generation system - professional development approach
- Hybrid configuration system with multi-layer environment support
- Comprehensive documentation system with multiple specialized guides
- Well-tested project with 5 test files

## Technology Stack

**Main Language:** python
**Stack Type:** cli_application

## Dependencies

### Python Dependencies
```
click>=8.0.0
pyyaml>=6.0
jinja2>=3.0.0
rich>=12.0.0
psutil>=5.8.0
pytest>=7.0.0
pytest-cov>=4.0.0
black>=22.0.0
flake8>=5.0.0
isort>=5.0.0
pre-commit>=2.0.0
mkdocs>=1.4.0
mkdocs-material>=8.0.0
mkdocs-mermaid2-plugin>=0.6.0
```

## File Structure

**File Types:**
- .bat: 1 files
- .example: 1 files
- .j2: 6 files
- .json: 6 files
- .md: 30 files
- .py: 40 files
- .sh: 2 files
- .toml: 1 files
- .txt: 1 files
- .yaml: 8 files

**Largest Files:**
- `src/nexus/core/hybrid_config.py` (34.2 KB)
- `nexus_docs/discovery/DISC-2025-09-11-discoverysystemadded.md` (30.6 KB)
- `src/nexus/core/installer.py` (25.4 KB)
- `src/nexus/core/integration_tester.py` (21.6 KB)
- `src/nexus/core/discovery/analyzer.py` (20.5 KB)
- `src/nexus/cli/main.py` (20.0 KB)
- `src/nexus/core/performance_tester.py` (19.4 KB)
- `src/nexus/core/content_enhancer.py` (16.5 KB)
- `src/nexus/docs/readmes/API_REFERENCE.md` (15.6 KB)
- `src/nexus/docs/readmes/PROJECT_STRUCTURE.md` (15.6 KB)

## Validation Results

**Status:** ✅ Valid
**Completeness:** 85/100

**Warnings:**
- No recommendations generated

## Raw Data

For integration with other tools, the complete analysis data is available in JSON format:

```json
{
  "metadata": {
    "target_path": "/home/rmans/projects/Nexus",
    "timestamp": "2025-09-11T21:11:52.364222",
    "version": "1.0.0",
    "options": {
      "cache": false,
      "deep": true
    },
    "engine": "nexus-discovery",
    "config_used": {}
  },
  "analysis": {
    "structure": {
      "total_files": 99,
      "total_size_bytes": 497418,
      "directories": [
        "test",
        "scripts",
        ".cursor",
        "test_results",
        "nexus_docs",
        ".nexus",
        "generated-docs",
        "src",
        "installers",
        "test/scripts",
        "test/results",
        "test/discovery",
        ".cursor/rules",
        ".git/branches",
        ".git/info",
        ".git/refs",
        ".git/hooks",
        ".git/objects",
        ".git/logs",
        "nexus_docs/task",
        "nexus_docs/prd",
        "nexus_docs/impl",
        "nexus_docs/arch",
        "nexus_docs/discovery",
        "nexus_docs/rules",
        "nexus_docs/int",
        "nexus_docs/exec",
        "nexus_docs/tests",
        ".nexus/config",
        ".nexus/templates",
        ".nexus/cache",
        ".nexus/instructions",
        "generated-docs/task",
        "generated-docs/prd",
        "generated-docs/impl",
        "generated-docs/arch",
        "generated-docs/discovery",
        "generated-docs/rules",
        "generated-docs/int",
        "generated-docs/exec",
        "generated-docs/tests",
        "src/nexus",
        "venv/lib",
        "venv/bin",
        "venv/include",
        "venv/lib64",
        ".git/refs/remotes",
        ".git/refs/heads",
        ".git/refs/tags",
        ".git/objects/e2",
        ".git/objects/c0",
        ".git/objects/1a",
        ".git/objects/a0",
        ".git/objects/9b",
        ".git/objects/58",
        ".git/objects/54",
        ".git/objects/8b",
        ".git/objects/22",
        ".git/objects/46",
        ".git/objects/dc",
        ".git/objects/72",
        ".git/objects/09",
        ".git/objects/bb",
        ".git/objects/f1",
        ".git/objects/aa",
        ".git/objects/b3",
        ".git/objects/f2",
        ".git/objects/1d",
        ".git/objects/2e",
        ".git/objects/83",
        ".git/objects/d7",
        ".git/objects/0f",
        ".git/objects/b2",
        ".git/objects/18",
        ".git/objects/9e",
        ".git/objects/82",
        ".git/objects/5d",
        ".git/objects/ef",
        ".git/objects/6e",
        ".git/objects/1f",
        ".git/objects/d6",
        ".git/objects/0c",
        ".git/objects/05",
        ".git/objects/b4",
        ".git/objects/dd",
        ".git/objects/5f",
        ".git/objects/1e",
        ".git/objects/6d",
        ".git/objects/c8",
        ".git/objects/01",
        ".git/objects/63",
        ".git/objects/30",
        ".git/objects/44",
        ".git/objects/c5",
        ".git/objects/a6",
        ".git/objects/84",
        ".git/objects/88",
        ".git/objects/6b",
        ".git/objects/e4",
        ".git/objects/b0",
        ".git/objects/34",
        ".git/objects/87",
        ".git/objects/70",
        ".git/objects/de",
        ".git/objects/ea",
        ".git/objects/75",
        ".git/objects/7b",
        ".git/objects/ec",
        ".git/objects/4a",
        ".git/objects/9a",
        ".git/objects/6a",
        ".git/objects/3c",
        ".git/objects/15",
        ".git/objects/b7",
        ".git/objects/13",
        ".git/objects/7a",
        ".git/objects/ca",
        ".git/objects/info",
        ".git/objects/d0",
        ".git/objects/ae",
        ".git/objects/55",
        ".git/objects/8e",
        ".git/objects/a9",
        ".git/objects/3d",
        ".git/objects/21",
        ".git/objects/43",
        ".git/objects/b9",
        ".git/objects/da",
        ".git/objects/db",
        ".git/objects/a7",
        ".git/objects/pack",
        ".git/objects/b1",
        ".git/objects/cb",
        ".git/objects/d2",
        ".git/objects/0d",
        ".git/objects/d4",
        ".git/objects/eb",
        ".git/objects/a3",
        ".git/objects/3b",
        ".git/objects/f9",
        ".git/objects/19",
        ".git/objects/91",
        ".git/objects/fd",
        ".git/objects/c3",
        ".git/objects/be",
        ".git/objects/2d",
        ".git/objects/5e",
        ".git/objects/b8",
        ".git/objects/2b",
        ".git/objects/86",
        ".git/objects/45",
        ".git/objects/c4",
        ".git/objects/60",
        ".git/objects/47",
        ".git/objects/61",
        ".git/objects/4b",
        ".git/objects/00",
        ".git/objects/10",
        ".git/objects/5a",
        ".git/objects/12",
        ".git/objects/68",
        ".git/objects/31",
        ".git/objects/73",
        ".git/objects/8a",
        ".git/objects/4c",
        ".git/objects/53",
        ".git/objects/37",
        ".git/objects/69",
        ".git/objects/27",
        ".git/objects/ce",
        ".git/objects/bc",
        ".git/objects/2a",
        ".git/objects/08",
        ".git/objects/e6",
        ".git/objects/32",
        ".git/objects/85",
        ".git/objects/23",
        ".git/objects/ac",
        ".git/objects/62",
        ".git/objects/7c",
        ".git/objects/c7",
        ".git/objects/f0",
        ".git/objects/5c",
        ".git/objects/81",
        ".git/objects/e5",
        ".git/objects/a8",
        ".git/objects/f6",
        ".git/objects/c9",
        ".git/objects/cd",
        ".git/objects/17",
        ".git/objects/0b",
        ".git/objects/50",
        ".git/objects/25",
        ".git/objects/52",
        ".git/objects/03",
        ".git/objects/6c",
        ".git/objects/fe",
        ".git/objects/df",
        ".git/objects/20",
        ".git/objects/cf",
        ".git/objects/8d",
        ".git/objects/d5",
        ".git/objects/89",
        ".git/objects/80",
        ".git/objects/8c",
        ".git/objects/fb",
        ".git/objects/33",
        ".git/objects/02",
        ".git/objects/49",
        ".git/objects/d1",
        ".git/objects/2c",
        ".git/objects/76",
        ".git/objects/c6",
        ".git/objects/07",
        ".git/objects/67",
        ".git/objects/bf",
        ".git/objects/ba",
        ".git/objects/e3",
        ".git/objects/9c",
        ".git/objects/98",
        ".git/objects/e1",
        ".git/objects/0e",
        ".git/objects/06",
        ".git/objects/a1",
        ".git/objects/16",
        ".git/objects/65",
        ".git/objects/4f",
        ".git/objects/59",
        ".git/objects/cc",
        ".git/objects/2f",
        ".git/objects/5b",
        ".git/objects/ff",
        ".git/objects/95",
        ".git/objects/4d",
        ".git/logs/refs",
        ".git/refs/remotes/origin",
        ".git/logs/refs/remotes",
        ".git/logs/refs/heads",
        ".git/logs/refs/remotes/origin",
        ".nexus/templates/task",
        ".nexus/templates/prd",
        ".nexus/templates/arch",
        ".nexus/cache/discovery",
        "src/nexus/commands",
        "src/nexus/core",
        "src/nexus/instructions",
        "src/nexus/docs",
        "src/nexus/cli",
        "src/nexus/core/discovery",
        "src/nexus/docs/context",
        "src/nexus/docs/templates",
        "src/nexus/docs/readmes",
        "src/nexus/docs/cache",
        "src/nexus/docs/rules",
        "src/nexus/docs/configs",
        "src/nexus/docs/examples",
        "src/nexus/docs/tests",
        "src/nexus/docs/configs/environments",
        "src/nexus/docs/configs/templates",
        "src/nexus/docs/configs/schemas",
        "src/nexus/docs/configs/examples",
        "venv/lib/python3.12",
        "venv/include/python3.12",
        "venv/lib/python3.12/site-packages",
        "venv/lib/python3.12/site-packages/yaml",
        "venv/lib/python3.12/site-packages/jinja2-3.1.6.dist-info",
        "venv/lib/python3.12/site-packages/nexus_context-0.1.0.dist-info",
        "venv/lib/python3.12/site-packages/psutil-7.0.0.dist-info",
        "venv/lib/python3.12/site-packages/pygments-2.19.2.dist-info",
        "venv/lib/python3.12/site-packages/rich-14.1.0.dist-info",
        "venv/lib/python3.12/site-packages/pygments",
        "venv/lib/python3.12/site-packages/_yaml",
        "venv/lib/python3.12/site-packages/rich",
        "venv/lib/python3.12/site-packages/click-8.2.1.dist-info",
        "venv/lib/python3.12/site-packages/markupsafe",
        "venv/lib/python3.12/site-packages/mdurl",
        "venv/lib/python3.12/site-packages/MarkupSafe-3.0.2.dist-info",
        "venv/lib/python3.12/site-packages/click",
        "venv/lib/python3.12/site-packages/markdown_it_py-4.0.0.dist-info",
        "venv/lib/python3.12/site-packages/psutil",
        "venv/lib/python3.12/site-packages/pip",
        "venv/lib/python3.12/site-packages/PyYAML-6.0.2.dist-info",
        "venv/lib/python3.12/site-packages/jinja2",
        "venv/lib/python3.12/site-packages/markdown_it",
        "venv/lib/python3.12/site-packages/mdurl-0.1.2.dist-info",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info",
        "venv/lib/python3.12/site-packages/jinja2-3.1.6.dist-info/licenses",
        "venv/lib/python3.12/site-packages/nexus_context-0.1.0.dist-info/licenses",
        "venv/lib/python3.12/site-packages/pygments-2.19.2.dist-info/licenses",
        "venv/lib/python3.12/site-packages/pygments/styles",
        "venv/lib/python3.12/site-packages/pygments/lexers",
        "venv/lib/python3.12/site-packages/pygments/filters",
        "venv/lib/python3.12/site-packages/pygments/formatters",
        "venv/lib/python3.12/site-packages/click-8.2.1.dist-info/licenses",
        "venv/lib/python3.12/site-packages/markdown_it_py-4.0.0.dist-info/licenses",
        "venv/lib/python3.12/site-packages/psutil/tests",
        "venv/lib/python3.12/site-packages/pip/_vendor",
        "venv/lib/python3.12/site-packages/pip/_internal",
        "venv/lib/python3.12/site-packages/markdown_it/presets",
        "venv/lib/python3.12/site-packages/markdown_it/common",
        "venv/lib/python3.12/site-packages/markdown_it/rules_block",
        "venv/lib/python3.12/site-packages/markdown_it/rules_core",
        "venv/lib/python3.12/site-packages/markdown_it/helpers",
        "venv/lib/python3.12/site-packages/markdown_it/cli",
        "venv/lib/python3.12/site-packages/markdown_it/rules_inline",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses",
        "venv/lib/python3.12/site-packages/pip/_vendor/tomli",
        "venv/lib/python3.12/site-packages/pip/_vendor/idna",
        "venv/lib/python3.12/site-packages/pip/_vendor/truststore",
        "venv/lib/python3.12/site-packages/pip/_vendor/pygments",
        "venv/lib/python3.12/site-packages/pip/_vendor/rich",
        "venv/lib/python3.12/site-packages/pip/_vendor/distro",
        "venv/lib/python3.12/site-packages/pip/_vendor/certifi",
        "venv/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks",
        "venv/lib/python3.12/site-packages/pip/_vendor/resolvelib",
        "venv/lib/python3.12/site-packages/pip/_vendor/platformdirs",
        "venv/lib/python3.12/site-packages/pip/_vendor/msgpack",
        "venv/lib/python3.12/site-packages/pip/_vendor/pkg_resources",
        "venv/lib/python3.12/site-packages/pip/_vendor/requests",
        "venv/lib/python3.12/site-packages/pip/_vendor/cachecontrol",
        "venv/lib/python3.12/site-packages/pip/_vendor/urllib3",
        "venv/lib/python3.12/site-packages/pip/_vendor/distlib",
        "venv/lib/python3.12/site-packages/pip/_vendor/packaging",
        "venv/lib/python3.12/site-packages/pip/_vendor/dependency_groups",
        "venv/lib/python3.12/site-packages/pip/_vendor/tomli_w",
        "venv/lib/python3.12/site-packages/pip/_internal/resolution",
        "venv/lib/python3.12/site-packages/pip/_internal/operations",
        "venv/lib/python3.12/site-packages/pip/_internal/locations",
        "venv/lib/python3.12/site-packages/pip/_internal/index",
        "venv/lib/python3.12/site-packages/pip/_internal/network",
        "venv/lib/python3.12/site-packages/pip/_internal/commands",
        "venv/lib/python3.12/site-packages/pip/_internal/models",
        "venv/lib/python3.12/site-packages/pip/_internal/utils",
        "venv/lib/python3.12/site-packages/pip/_internal/req",
        "venv/lib/python3.12/site-packages/pip/_internal/cli",
        "venv/lib/python3.12/site-packages/pip/_internal/metadata",
        "venv/lib/python3.12/site-packages/pip/_internal/vcs",
        "venv/lib/python3.12/site-packages/pip/_internal/distributions",
        "venv/lib/python3.12/site-packages/pip/_vendor/pygments/styles",
        "venv/lib/python3.12/site-packages/pip/_vendor/pygments/lexers",
        "venv/lib/python3.12/site-packages/pip/_vendor/pygments/filters",
        "venv/lib/python3.12/site-packages/pip/_vendor/pygments/formatters",
        "venv/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/_in_process",
        "venv/lib/python3.12/site-packages/pip/_vendor/resolvelib/resolvers",
        "venv/lib/python3.12/site-packages/pip/_vendor/cachecontrol/caches",
        "venv/lib/python3.12/site-packages/pip/_vendor/urllib3/packages",
        "venv/lib/python3.12/site-packages/pip/_vendor/urllib3/contrib",
        "venv/lib/python3.12/site-packages/pip/_vendor/urllib3/util",
        "venv/lib/python3.12/site-packages/pip/_vendor/packaging/licenses",
        "venv/lib/python3.12/site-packages/pip/_vendor/urllib3/packages/backports",
        "venv/lib/python3.12/site-packages/pip/_vendor/urllib3/contrib/_securetransport",
        "venv/lib/python3.12/site-packages/pip/_internal/resolution/legacy",
        "venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib",
        "venv/lib/python3.12/site-packages/pip/_internal/operations/install",
        "venv/lib/python3.12/site-packages/pip/_internal/metadata/importlib",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/tomli",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/idna",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/truststore",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/pygments",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/rich",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/distro",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/certifi",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/pyproject_hooks",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/resolvelib",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/platformdirs",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/msgpack",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/pkg_resources",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/requests",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/cachecontrol",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/urllib3",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/distlib",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/packaging",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/dependency_groups",
        "venv/lib/python3.12/site-packages/pip-25.2.dist-info/licenses/src/pip/_vendor/tomli_w"
      ],
      "file_types": {
        ".md": 30,
        ".yaml": 8,
        ".example": 1,
        ".txt": 1,
        ".py": 40,
        ".toml": 1,
        ".json": 6,
        ".sh": 2,
        ".bat": 1,
        ".j2": 6
      },
      "largest_files": [
        {
          "path": "src/nexus/core/hybrid_config.py",
          "size": 35009,
          "extension": ".py"
        },
        {
          "path": "nexus_docs/discovery/DISC-2025-09-11-discoverysystemadded.md",
          "size": 31381,
          "extension": ".md"
        },
        {
          "path": "src/nexus/core/installer.py",
          "size": 26052,
          "extension": ".py"
        },
        {
          "path": "src/nexus/core/integration_tester.py",
          "size": 22082,
          "extension": ".py"
        },
        {
          "path": "src/nexus/core/discovery/analyzer.py",
          "size": 21015,
          "extension": ".py"
        },
        {
          "path": "src/nexus/cli/main.py",
          "size": 20528,
          "extension": ".py"
        },
        {
          "path": "src/nexus/core/performance_tester.py",
          "size": 19896,
          "extension": ".py"
        },
        {
          "path": "src/nexus/core/content_enhancer.py",
          "size": 16902,
          "extension": ".py"
        },
        {
          "path": "src/nexus/docs/readmes/API_REFERENCE.md",
          "size": 15958,
          "extension": ".md"
        },
        {
          "path": "src/nexus/docs/readmes/PROJECT_STRUCTURE.md",
          "size": 15954,
          "extension": ".md"
        }
      ]
    },
    "dependencies": {
      "python": {
        "requirements_txt": [
          "click>=8.0.0",
          "pyyaml>=6.0",
          "jinja2>=3.0.0",
          "rich>=12.0.0",
          "psutil>=5.8.0",
          "pytest>=7.0.0",
          "pytest-cov>=4.0.0",
          "black>=22.0.0",
          "flake8>=5.0.0",
          "isort>=5.0.0",
          "pre-commit>=2.0.0",
          "mkdocs>=1.4.0",
          "mkdocs-material>=8.0.0",
          "mkdocs-mermaid2-plugin>=0.6.0"
        ],
        "pyproject_toml": {
          "build-system": {
            "requires": [
              "setuptools>=61.0",
              "wheel"
            ],
            "build-backend": "setuptools.build_meta"
          },
          "project": {
            "name": "nexus-context",
            "version": "1.0.0",
            "description": "A modular project framework with fixed hybrid configuration system and professional installer",
            "readme": "README.md",
            "requires-python": ">=3.8",
            "license": {
              "text": "MIT"
            },
            "authors": [
              {
                "name": "Nexus Team",
                "email": "contact@nexus-project.dev"
              }
            ],
            "keywords": [
              "ai",
              "context",
              "documentation",
              "cursor",
              "coding-assistant",
              "nexus",
              "configuration",
              "installer",
              "hybrid-config",
              "project-framework",
              "modular",
              "development",
              "automation",
              "templates",
              "schemas"
            ],
            "classifiers": [
              "Development Status :: 4 - Beta",
              "Intended Audience :: Developers",
              "License :: OSI Approved :: MIT License",
              "Operating System :: OS Independent",
              "Programming Language :: Python :: 3",
              "Programming Language :: Python :: 3.8",
              "Programming Language :: Python :: 3.9",
              "Programming Language :: Python :: 3.10",
              "Programming Language :: Python :: 3.11",
              "Programming Language :: Python :: 3.12",
              "Topic :: Software Development :: Libraries :: Python Modules",
              "Topic :: Software Development :: Documentation",
              "Topic :: Software Development :: Build Tools",
              "Topic :: Software Development :: Testing",
              "Topic :: Text Processing :: Markup",
              "Topic :: System :: Installation/Setup",
              "Topic :: System :: Systems Administration",
              "Environment :: Console",
              "Environment :: Web Environment"
            ],
            "dependencies": [
              "click>=8.0.0",
              "pyyaml>=6.0",
              "jinja2>=3.0.0",
              "rich>=12.0.0",
              "pathlib2>=2.3.0; python_version < '3.4'",
              "typing-extensions>=4.0.0; python_version < '3.8'"
            ],
            "optional-dependencies": {
              "dev": [
                "pytest>=7.0.0",
                "pytest-cov>=4.0.0",
                "black>=22.0.0",
                "flake8>=5.0.0",
                "isort>=5.0.0",
                "pre-commit>=2.0.0",
                "mypy>=1.0.0",
                "pytest-mock>=3.0.0"
              ],
              "docs": [
                "mkdocs>=1.4.0",
                "mkdocs-material>=8.0.0",
                "mkdocs-mermaid2-plugin>=0.6.0",
                "sphinx>=5.0.0",
                "sphinx-rtd-theme>=1.0.0"
              ],
              "installer": [
                "pyinstaller>=5.0.0",
                "cx-freeze>=6.0.0",
                "py2exe>=0.10.0; sys_platform == 'win32'",
                "py2app>=0.28.0; sys_platform == 'darwin'"
              ],
              "config": [
                "jsonschema>=4.0.0",
                "pydantic>=1.10.0",
                "python-dotenv>=0.19.0",
                "configparser>=5.0.0"
              ]
            },
            "scripts": {
              "nexus": "nexus.__main__:main"
            },
            "urls": {
              "Homepage": "https://github.com/rmans/Nexus",
              "Repository": "https://github.com/rmans/Nexus",
              "Documentation": "https://github.com/rmans/Nexus#readme",
              "Bug Reports": "https://github.com/rmans/Nexus/issues"
            }
          },
          "tool": {
            "setuptools": {
              "packages": {
                "find": {
                  "where": [
                    "src"
                  ]
                }
              },
              "package-data": {
                "nexus": [
                  "commands/*.md",
                  "instructions/*.md",
                  "templates/**/*",
                  "docs/readmes/*.md",
                  "docs/configs/**/*",
                  "cli/**/*",
                  "core/**/*",
                  "*.py",
                  "*.yaml",
                  "*.yml",
                  "*.json",
                  "*.md",
                  "*.txt",
                  "*.sh",
                  "*.bat"
                ]
              }
            },
            "black": {
              "line-length": 88,
              "target-version": [
                "py38",
                "py39",
                "py310",
                "py311",
                "py312"
              ],
              "include": "\\.pyi?$",
              "extend-exclude": "/(\n  # directories\n  \\.eggs\n  | \\.git\n  | \\.hg\n  | \\.mypy_cache\n  | \\.tox\n  | \\.venv\n  | venv\n  | _build\n  | buck-out\n  | build\n  | dist\n)/\n"
            },
            "isort": {
              "profile": "black",
              "multi_line_output": 3,
              "line_length": 88,
              "known_first_party": [
                "nexus"
              ]
            },
            "mypy": {
              "python_version": "3.8",
              "warn_return_any": true,
              "warn_unused_configs": true,
              "disallow_untyped_defs": true,
              "disallow_incomplete_defs": true,
              "check_untyped_defs": true,
              "disallow_untyped_decorators": true,
              "no_implicit_optional": true,
              "warn_redundant_casts": true,
              "warn_unused_ignores": true,
              "warn_no_return": true,
              "warn_unreachable": true,
              "strict_equality": true
            },
            "pytest": {
              "ini_options": {
                "testpaths": [
                  "test"
                ],
                "python_files": [
                  "test_*.py",
                  "*_test.py"
                ],
                "python_classes": [
                  "Test*"
                ],
                "python_functions": [
                  "test_*"
                ],
                "addopts": [
                  "--strict-markers",
                  "--strict-config",
                  "--cov=nexus",
                  "--cov-report=term-missing",
                  "--cov-report=html",
                  "--cov-report=xml"
                ],
                "markers": [
                  "slow: marks tests as slow (deselect with '-m \"not slow\"')",
                  "integration: marks tests as integration tests",
                  "unit: marks tests as unit tests"
                ]
              }
            }
          }
        },
        "setup_py": [],
        "pipfile": {}
      },
      "javascript": {
        "package_json": {},
        "yarn_lock": false,
        "package_lock": false
      },
      "other": {}
    },
    "languages": [
      "json",
      "markdown",
      "python",
      "shell",
      "yaml"
    ],
    "frameworks": [
      "pytest",
      "click",
      "rich",
      "jinja2",
      "pyyaml"
    ],
    "patterns": [
      "has_tests",
      "documented",
      "cli_application",
      "rich_output",
      "template_system",
      "hybrid_configuration",
      "documentation_system"
    ],
    "quality_metrics": {
      "total_lines_of_code": 7333,
      "test_file_count": 5,
      "python_complexity": {
        "setup.py": 8,
        "scripts/sync_version.py": 7,
        "installers/install.py": 6,
        "test/discovery/__init__.py": 1,
        "test/discovery/test_engine.py": 1,
        "src/nexus/__main__.py": 2,
        "src/nexus/core/performance_tester.py": 24,
        "src/nexus/core/validator.py": 13,
        "src/nexus/core/content_migrator.py": 31,
        "src/nexus/core/content_enhancer.py": 42,
        "src/nexus/core/instructions.py": 5,
        "src/nexus/core/generator.py": 23,
        "src/nexus/core/config.py": 27,
        "src/nexus/core/updater.py": 17,
        "src/nexus/core/__init__.py": 1,
        "src/nexus/core/version.py": 6,
        "src/nexus/core/server.py": 3,
        "src/nexus/core/hybrid_config.py": 95,
        "src/nexus/core/integration_tester.py": 24,
        "src/nexus/core/templates.py": 18,
        "src/nexus/core/installer.py": 45,
        "src/nexus/core/project_init.py": 17,
        "src/nexus/core/commands.py": 7,
        "src/nexus/core/status.py": 20,
        "src/nexus/core/content_analyzer.py": 41,
        "src/nexus/core/template_discovery.py": 11,
        "src/nexus/cli/discover.py": 13,
        "src/nexus/cli/__init__.py": 1,
        "src/nexus/cli/main.py": 42,
        "src/nexus/core/discovery/reports.py": 41,
        "src/nexus/core/discovery/synthesizer.py": 88,
        "src/nexus/core/discovery/engine.py": 6,
        "src/nexus/core/discovery/validator.py": 20,
        "src/nexus/core/discovery/cache.py": 19,
        "src/nexus/core/discovery/__init__.py": 1,
        "src/nexus/core/discovery/analyzer.py": 133,
        "src/nexus/core/discovery/outputs.py": 11,
        "src/nexus/docs/examples/discovery_example.py": 6,
        "src/nexus/docs/configs/examples/serve_example.py": 4,
        "src/nexus/docs/configs/examples/docs_example.py": 3
      },
      "code_coverage_indicators": []
    },
    "entry_points": []
  },
  "synthesis": {
    "insights": [
      "Multi-language project using json, markdown, python, shell, yaml",
      "Professional CLI development framework with Click and Rich console interface",
      "Template-driven content generation system - professional development approach",
      "Hybrid configuration system with multi-layer environment support",
      "Comprehensive documentation system with multiple specialized guides",
      "Well-tested project with 5 test files"
    ],
    "recommendations": [],
    "architecture_summary": {
      "type": "cli_application",
      "application_type": "cli_framework",
      "patterns": [
        "has_tests",
        "documented",
        "cli_application",
        "rich_output",
        "template_system",
        "hybrid_configuration",
        "documentation_system"
      ],
      "complexity": "high"
    },
    "quality_assessment": {
      "overall_score": 100,
      "has_tests": true,
      "has_documentation": true,
      "is_containerized": false,
      "test_file_count": 5,
      "lines_of_code": 7333,
      "assessment": "excellent"
    },
    "technology_stack": {
      "languages": [
        "json",
        "markdown",
        "python",
        "shell",
        "yaml"
      ],
      "frameworks": [
        "pytest",
        "click",
        "rich",
        "jinja2",
        "pyyaml"
      ],
      "main_language": "python",
      "stack_type": "cli_application",
      "entry_points": []
    }
  },
  "validation": {
    "is_valid": true,
    "completeness_score": 85,
    "warnings": [
      "No recommendations generated"
    ],
    "errors": [],
    "missing_data": [],
    "analysis_validation": {
      "warnings": [],
      "errors": []
    },
    "synthesis_validation": {
      "warnings": [
        "No recommendations generated"
      ],
      "errors": []
    }
  }
}
```