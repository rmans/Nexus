"""Document generation module."""

import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
from rich.console import Console
from rich.progress import Progress, TaskID
from .templates import TemplateManager
from .config import ConfigManager

console = Console()

class DocumentGenerator:
    """Generate project documentation using templates and existing content."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize the document generator.
        
        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root or Path.cwd()
        self.config_manager = ConfigManager(self.project_root)
        self.template_manager = TemplateManager(self.project_root)
        self.source_docs_dir = self.project_root / "generated-docs"
    
    def generate(self, output_dir: Optional[Path] = None, format: str = "markdown", 
                 include: Optional[List[str]] = None, auto_reload: bool = False) -> None:
        """Generate project documentation.
        
        Args:
            output_dir: Output directory for generated docs
            format: Documentation format (html, pdf, markdown)
            include: Include specific documentation sections
            auto_reload: Auto-reload on changes
        """
        console.print("📚 Generating documentation...", style="blue")
        
        # Determine output directory
        if output_dir:
            output_path = Path(output_dir)
        else:
            output_path = self.config_manager.get_docs_directory()
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Determine which sections to include
        if include is None:
            include = self.config_manager.get("documentation.include_types", [])
        
        # Generate documentation based on format
        if format == "markdown":
            self._generate_markdown_docs(output_path, include)
        elif format == "html":
            self._generate_html_docs(output_path, include)
        elif format == "pdf":
            self._generate_pdf_docs(output_path, include)
        else:
            console.print(f"❌ Unsupported format: {format}", style="red")
            return
        
        console.print(f"✅ Documentation generated in {output_path}", style="green")
    
    def _generate_markdown_docs(self, output_path: Path, include: List[str]) -> None:
        """Generate markdown documentation.
        
        Args:
            output_path: Output directory
            include: List of sections to include
        """
        console.print("📝 Generating markdown documentation...", style="blue")
        
        # Copy existing generated-docs if available
        if self.source_docs_dir.exists():
            self._copy_existing_docs(output_path, include)
        else:
            self._create_basic_docs(output_path, include)
        
        # Generate new documents from templates
        self._generate_from_templates(output_path, include)
        
        # Create main README
        self._create_main_readme(output_path)
        
        console.print("✅ Markdown documentation generated", style="green")
    
    def _copy_existing_docs(self, output_path: Path, include: List[str]) -> None:
        """Copy existing documentation from generated-docs.
        
        Args:
            output_path: Output directory
            include: List of sections to include
        """
        with Progress() as progress:
            task = progress.add_task("Copying existing docs...", total=len(include))
            
            for section in include:
                source_dir = self.source_docs_dir / section
                target_dir = output_path / section
                
                if source_dir.exists():
                    target_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Copy all markdown files
                    for md_file in source_dir.glob("*.md"):
                        shutil.copy2(md_file, target_dir / md_file.name)
                    
                    console.print(f"📋 Copied {section} documentation", style="green")
                else:
                    console.print(f"⚠️  Source directory not found: {source_dir}", style="yellow")
                
                progress.update(task, advance=1)
    
    def _create_basic_docs(self, output_path: Path, include: List[str]) -> None:
        """Create basic documentation structure.
        
        Args:
            output_path: Output directory
            include: List of sections to include
        """
        for section in include:
            section_dir = output_path / section
            section_dir.mkdir(parents=True, exist_ok=True)
            
            # Create index file
            index_file = section_dir / "index.md"
            index_content = f"""# {section.upper()} Documents

*Generated {section} documents will appear here*

## Overview
This directory contains {section} documentation for the project.

## Files
*No {section} documents yet*

## Usage
Use the `nexus generate-docs` command to create documentation in this directory.
"""
            index_file.write_text(index_content)
    
    def _generate_from_templates(self, output_path: Path, include: List[str]) -> None:
        """Generate documents from templates.
        
        Args:
            output_path: Output directory
            include: List of sections to include
        """
        # Install default templates if not present
        if not self.template_manager.templates_dir.exists():
            self.template_manager.install_default_templates()
        
        # Generate documents for each section
        for section in include:
            self._generate_section_docs(output_path / section, section)
    
    def _generate_section_docs(self, section_dir: Path, section: str) -> None:
        """Generate documents for a specific section.
        
        Args:
            section_dir: Directory for the section
            section: Section name
        """
        # Get available templates for this section
        templates = self.template_manager.list_templates(section)
        
        if not templates:
            return
        
        # Generate documents from templates
        for category, template_list in templates.items():
            for template_name in template_list:
                self._generate_document_from_template(
                    section_dir, section, category, template_name
                )
    
    def _generate_document_from_template(self, section_dir: Path, section: str, 
                                       category: str, template_name: str) -> None:
        """Generate a document from a template.
        
        Args:
            section_dir: Directory for the section
            section: Section name
            category: Template category
            template_name: Template name
        """
        # Create context for template
        context = self._create_template_context(section, template_name)
        
        # Render template
        content = self.template_manager.render_template(
            template_name, context, category
        )
        
        if content:
            # Create document file
            doc_file = section_dir / f"{template_name}.md"
            doc_file.write_text(content)
            console.print(f"📄 Generated {section}/{template_name}.md", style="green")
    
    def _create_template_context(self, section: str, template_name: str) -> Dict[str, Any]:
        """Create context for template rendering.
        
        Args:
            section: Section name
            template_name: Template name
            
        Returns:
            Context dictionary
        """
        # Base context
        context = {
            "title": f"{template_name.title()} {section.upper()}",
            "description": f"Generated {section} document for {self.project_root.name}",
            "project_name": self.project_root.name,
            "section": section,
            "template_name": template_name
        }
        
        # Add section-specific context
        if section == "prd":
            context.update({
                "goals": [
                    "Define clear product requirements",
                    "Establish success criteria",
                    "Guide development efforts"
                ],
                "requirements": [
                    {
                        "title": "Core Functionality",
                        "description": "Essential features and capabilities",
                        "criteria": [
                            "Feature works as specified",
                            "Performance meets requirements",
                            "User experience is intuitive"
                        ]
                    }
                ],
                "success_metrics": [
                    "User adoption rate",
                    "Feature completion rate",
                    "User satisfaction score"
                ],
                "start_date": "TBD",
                "end_date": "TBD",
                "stakeholders": [
                    {"role": "Product Manager", "name": "TBD"},
                    {"role": "Engineering Lead", "name": "TBD"},
                    {"role": "Design Lead", "name": "TBD"}
                ]
            })
        elif section == "arch":
            context.update({
                "components": [
                    {
                        "name": "Core System",
                        "description": "Main application components",
                        "responsibilities": [
                            "Business logic processing",
                            "Data management",
                            "API handling"
                        ],
                        "interfaces": [
                            "REST API",
                            "Database interface",
                            "External service integration"
                        ]
                    }
                ],
                "data_flow_description": "Data flows through the system components as follows...",
                "technology_stack": [
                    {"category": "Backend", "choices": ["Python", "FastAPI", "PostgreSQL"]},
                    {"category": "Frontend", "choices": ["React", "TypeScript", "Tailwind CSS"]},
                    {"category": "Infrastructure", "choices": ["Docker", "Kubernetes", "AWS"]}
                ],
                "deployment_description": "The system is deployed using containerization...",
                "security_considerations": [
                    "Authentication and authorization",
                    "Data encryption",
                    "Input validation",
                    "Secure communication"
                ]
            })
        elif section == "task":
            context.update({
                "description": f"Task description for {template_name}",
                "prerequisites": [
                    "Required setup completed",
                    "Dependencies installed",
                    "Environment configured"
                ],
                "steps": [
                    {
                        "number": 1,
                        "title": "Initial Setup",
                        "description": "Set up the initial environment",
                        "commands": ["echo 'Setting up...'", "mkdir -p workspace"],
                        "expected_output": "Environment ready"
                    }
                ],
                "verification": [
                    "Check that all steps completed successfully",
                    "Verify expected outputs",
                    "Test functionality"
                ],
                "troubleshooting": [
                    {
                        "problem": "Common issue",
                        "solution": "Solution description"
                    }
                ]
            })
        
        return context
    
    def _create_main_readme(self, output_path: Path) -> None:
        """Create main README for documentation.
        
        Args:
            output_path: Output directory
        """
        readme_content = f"""# {self.project_root.name} Documentation

This directory contains generated documentation for the project.

## Structure
"""
        
        # Add structure based on available sections
        for section_dir in output_path.iterdir():
            if section_dir.is_dir():
                section_name = section_dir.name
                readme_content += f"- `{section_name}/` - {self._get_section_description(section_name)}\n"
        
        readme_content += """
## Usage
This documentation is automatically generated and should be kept up to date.

## Commands
- `nexus generate-docs` - Regenerate all documentation
- `nexus serve-docs` - Start local documentation server
- `nexus status` - Check documentation status
"""
        
        (output_path / "README.md").write_text(readme_content)
    
    def _get_section_description(self, section: str) -> str:
        """Get description for a documentation section.
        
        Args:
            section: Section name
            
        Returns:
            Section description
        """
        descriptions = {
            "prd": "Product Requirements Documents",
            "arch": "Architecture Documentation",
            "impl": "Implementation Details",
            "int": "Integration Documentation",
            "exec": "Execution Documentation",
            "rules": "Business Rules",
            "task": "Task Documentation",
            "tests": "Test Documentation"
        }
        return descriptions.get(section, f"{section.upper()} Documentation")
    
    def _generate_html_docs(self, output_path: Path, include: List[str]) -> None:
        """Generate HTML documentation.
        
        Args:
            output_path: Output directory
            include: List of sections to include
        """
        console.print("🌐 Generating HTML documentation...", style="blue")
        console.print("💡 HTML generation not yet implemented", style="yellow")
    
    def _generate_pdf_docs(self, output_path: Path, include: List[str]) -> None:
        """Generate PDF documentation.
        
        Args:
            output_path: Output directory
            include: List of sections to include
        """
        console.print("📄 Generating PDF documentation...", style="blue")
        console.print("💡 PDF generation not yet implemented", style="yellow")
