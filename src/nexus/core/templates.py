"""Template management module."""

import shutil
from pathlib import Path
from typing import Dict, List, Optional
from jinja2 import Environment, FileSystemLoader, Template
from rich.console import Console

console = Console()

class TemplateManager:
    """Manage templates for various document types."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize template manager.
        
        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root or Path.cwd()
        self.nexus_dir = self.project_root / ".nexus"
        self.templates_dir = self.nexus_dir / "templates"
        self.jinja_env = None
        self._setup_jinja()
    
    def _setup_jinja(self):
        """Set up Jinja2 environment."""
        if self.templates_dir.exists():
            self.jinja_env = Environment(
                loader=FileSystemLoader(str(self.templates_dir)),
                autoescape=True
            )
        else:
            # Fallback to string templates
            self.jinja_env = Environment(loader=None)
    
    def create_template(self, template_name: str, content: str, category: str = "custom") -> None:
        """Create a new template.
        
        Args:
            template_name: Name of the template
            content: Template content
            category: Template category
        """
        category_dir = self.templates_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        template_file = category_dir / f"{template_name}.j2"
        template_file.write_text(content)
        
        console.print(f"📝 Created template: {category}/{template_name}", style="green")
    
    def get_template(self, template_name: str, category: str = "default") -> Optional[Template]:
        """Get a template by name and category.
        
        Args:
            template_name: Name of the template
            category: Template category
            
        Returns:
            Jinja2 template or None if not found
        """
        if not self.jinja_env:
            return None
        
        template_path = f"{category}/{template_name}.j2"
        try:
            return self.jinja_env.get_template(template_path)
        except:
            # Try default category
            if category != "default":
                try:
                    return self.jinja_env.get_template(f"default/{template_name}.j2")
                except:
                    pass
            return None
    
    def render_template(self, template_name: str, context: Dict, category: str = "default") -> str:
        """Render a template with context.
        
        Args:
            template_name: Name of the template
            context: Context variables for rendering
            category: Template category
            
        Returns:
            Rendered template content
        """
        template = self.get_template(template_name, category)
        if template:
            return template.render(**context)
        else:
            console.print(f"⚠️  Template not found: {category}/{template_name}", style="yellow")
            return ""
    
    def list_templates(self, category: Optional[str] = None) -> Dict[str, List[str]]:
        """List available templates.
        
        Args:
            category: Specific category to list (None for all)
            
        Returns:
            Dictionary of categories and their templates
        """
        if not self.templates_dir.exists():
            return {}
        
        templates = {}
        for cat_dir in self.templates_dir.iterdir():
            if cat_dir.is_dir():
                cat_name = cat_dir.name
                if category is None or cat_name == category:
                    templates[cat_name] = [
                        f.stem for f in cat_dir.glob("*.j2")
                    ]
        
        return templates
    
    def install_default_templates(self) -> None:
        """Install default templates."""
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Create default templates
        default_templates = {
            "prd": {
                "basic": """# {{ title }}

## Overview
{{ description }}

## Goals
{% for goal in goals %}
- {{ goal }}
{% endfor %}

## Requirements
{% for req in requirements %}
### {{ req.title }}
{{ req.description }}

**Acceptance Criteria:**
{% for criteria in req.criteria %}
- {{ criteria }}
{% endfor %}

{% endfor %}

## Success Metrics
{% for metric in success_metrics %}
- {{ metric }}
{% endfor %}

## Timeline
- **Start Date:** {{ start_date }}
- **End Date:** {{ end_date }}

## Stakeholders
{% for stakeholder in stakeholders %}
- **{{ stakeholder.role }}:** {{ stakeholder.name }}
{% endfor %}
""",
                "detailed": """# {{ title }}

## Executive Summary
{{ executive_summary }}

## Problem Statement
{{ problem_statement }}

## Solution Overview
{{ solution_overview }}

## Business Objectives
{% for objective in business_objectives %}
- {{ objective }}
{% endfor %}

## User Stories
{% for story in user_stories %}
### {{ story.title }}
**As a** {{ story.user_type }}  
**I want** {{ story.goal }}  
**So that** {{ story.benefit }}

**Acceptance Criteria:**
{% for criteria in story.criteria %}
- {{ criteria }}
{% endfor %}

{% endfor %}

## Technical Requirements
{% for req in technical_requirements %}
### {{ req.category }}
{% for item in req.items %}
- {{ item }}
{% endfor %}

{% endfor %}

## Non-Functional Requirements
{% for req in non_functional_requirements %}
- **{{ req.name }}:** {{ req.description }}
{% endfor %}

## Success Metrics
{% for metric in success_metrics %}
- **{{ metric.name }}:** {{ metric.target }} ({{ metric.measurement }})
{% endfor %}

## Risks and Mitigations
{% for risk in risks %}
- **{{ risk.description }}:** {{ risk.mitigation }}
{% endfor %}

## Timeline
{% for phase in timeline %}
- **{{ phase.name }}:** {{ phase.start_date }} - {{ phase.end_date }}
{% endfor %}

## Resources
{% for resource in resources %}
- **{{ resource.type }}:** {{ resource.description }}
{% endfor %}
"""
            },
            "arch": {
                "basic": """# {{ title }} Architecture

## Overview
{{ description }}

## System Components
{% for component in components %}
### {{ component.name }}
{{ component.description }}

**Responsibilities:**
{% for responsibility in component.responsibilities %}
- {{ responsibility }}
{% endfor %}

**Interfaces:**
{% for interface in component.interfaces %}
- {{ interface }}
{% endfor %}

{% endfor %}

## Data Flow
{{ data_flow_description }}

## Technology Stack
{% for tech in technology_stack %}
- **{{ tech.category }}:** {{ tech.choices | join(', ') }}
{% endfor %}

## Deployment Architecture
{{ deployment_description }}

## Security Considerations
{% for consideration in security_considerations %}
- {{ consideration }}
{% endfor %}
""",
                "microservices": """# {{ title }} Microservices Architecture

## Overview
{{ description }}

## Service Architecture
{% for service in services %}
### {{ service.name }}
{{ service.description }}

**Domain:** {{ service.domain }}
**Responsibilities:**
{% for responsibility in service.responsibilities %}
- {{ responsibility }}
{% endfor %}

**APIs:**
{% for api in service.apis %}
- **{{ api.method }}** {{ api.endpoint }} - {{ api.description }}
{% endfor %}

**Dependencies:**
{% for dep in service.dependencies %}
- {{ dep }}
{% endfor %}

{% endfor %}

## Data Architecture
{% for data_store in data_stores %}
### {{ data_store.name }}
- **Type:** {{ data_store.type }}
- **Purpose:** {{ data_store.purpose }}
- **Schema:** {{ data_store.schema }}

{% endfor %}

## Communication Patterns
{% for pattern in communication_patterns %}
- **{{ pattern.name }}:** {{ pattern.description }}
{% endfor %}

## Infrastructure
{% for component in infrastructure %}
### {{ component.name }}
{{ component.description }}

**Configuration:**
{% for config in component.configuration %}
- {{ config }}
{% endfor %}

{% endfor %}

## Monitoring and Observability
{% for monitoring in monitoring_setup %}
- **{{ monitoring.name }}:** {{ monitoring.description }}
{% endfor %}
"""
            },
            "task": {
                "basic": """# {{ title }}

## Description
{{ description }}

## Prerequisites
{% for prereq in prerequisites %}
- {{ prereq }}
{% endfor %}

## Steps
{% for step in steps %}
### {{ step.number }}. {{ step.title }}
{{ step.description }}

**Commands:**
```bash
{{ step.commands | join('\n') }}
```

**Expected Output:**
{{ step.expected_output }}

{% endfor %}

## Verification
{% for check in verification %}
- {{ check }}
{% endfor %}

## Troubleshooting
{% for issue in troubleshooting %}
### {{ issue.problem }}
**Solution:** {{ issue.solution }}

{% endfor %}
""",
                "development": """# {{ title }}

## Objective
{{ objective }}

## Requirements
{% for req in requirements %}
- {{ req }}
{% endfor %}

## Implementation Plan
{% for phase in implementation_phases %}
### Phase {{ phase.number }}: {{ phase.name }}
{{ phase.description }}

**Tasks:**
{% for task in phase.tasks %}
- [ ] {{ task }}
{% endfor %}

**Deliverables:**
{% for deliverable in phase.deliverables %}
- {{ deliverable }}
{% endfor %}

**Timeline:** {{ phase.timeline }}

{% endfor %}

## Testing Strategy
{% for test in testing_strategy %}
- **{{ test.type }}:** {{ test.description }}
{% endfor %}

## Code Review Checklist
{% for item in code_review_checklist %}
- [ ] {{ item }}
{% endfor %}

## Deployment
{{ deployment_instructions }}

## Rollback Plan
{{ rollback_plan }}
"""
            }
        }
        
        for category, templates in default_templates.items():
            category_dir = self.templates_dir / category
            category_dir.mkdir(parents=True, exist_ok=True)
            
            for template_name, content in templates.items():
                template_file = category_dir / f"{template_name}.j2"
                template_file.write_text(content)
        
        console.print("📦 Installed default templates", style="green")
    
    def copy_existing_templates(self, source_dir: Path) -> None:
        """Copy existing templates from source directory.
        
        Args:
            source_dir: Source directory containing templates
        """
        if not source_dir.exists():
            console.print(f"⚠️  Source directory not found: {source_dir}", style="yellow")
            return
        
        # Copy all template files
        for template_file in source_dir.rglob("*.md"):
            relative_path = template_file.relative_to(source_dir)
            target_file = self.templates_dir / relative_path.with_suffix('.j2')
            target_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(template_file, target_file)
        
        console.print(f"📋 Copied templates from {source_dir}", style="green")
