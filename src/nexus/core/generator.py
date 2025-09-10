"""Document generation module."""

from pathlib import Path
from rich.console import Console

console = Console()

class DocumentGenerator:
    """Generate project documentation."""
    
    def __init__(self):
        """Initialize the document generator."""
        self.project_root = Path.cwd()
    
    def generate(self, output_dir=None, format="markdown", include=None, auto_reload=False):
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
            output_path = self.project_root / "nexus_docs"
        
        output_path.mkdir(parents=True, exist_ok=True)
        
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
    
    def _generate_markdown_docs(self, output_path, include):
        """Generate markdown documentation."""
        console.print("📝 Generating markdown documentation...", style="blue")
        
        # Create basic documentation structure
        readme_content = """# Project Documentation

This directory contains generated documentation for the project.

## Structure
- `prd/` - Product Requirements Documents
- `arch/` - Architecture Documentation
- `impl/` - Implementation Details
- `int/` - Integration Documentation
- `exec/` - Execution Documentation
- `rules/` - Business Rules
- `task/` - Task Documentation
- `tests/` - Test Documentation

## Usage
This documentation is automatically generated and should be kept up to date.
"""
        
        (output_path / "README.md").write_text(readme_content)
        console.print("✅ Markdown documentation generated", style="green")
    
    def _generate_html_docs(self, output_path, include):
        """Generate HTML documentation."""
        console.print("🌐 Generating HTML documentation...", style="blue")
        console.print("💡 HTML generation not yet implemented", style="yellow")
    
    def _generate_pdf_docs(self, output_path, include):
        """Generate PDF documentation."""
        console.print("📄 Generating PDF documentation...", style="blue")
        console.print("💡 PDF generation not yet implemented", style="yellow")
