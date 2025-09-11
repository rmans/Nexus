# Example: Using the hybrid configuration system in documentation generation

from nexus.core.hybrid_config import get_config, get_docs_dir, get_templates_dir, get_doc_formats

class DocumentationGenerator:
    """Documentation generator using hybrid configuration."""
    
    def __init__(self):
        self.config = get_config()
    
    def generate(self):
        """Generate documentation using configuration settings."""
        # All paths from configuration
        docs_dir = get_docs_dir()
        templates_dir = get_templates_dir()
        formats = get_doc_formats()
        auto_generate = self.config.get('documentation.auto_generate', True)
        
        print(f"Generating docs in {docs_dir}")
        print(f"Formats: {', '.join(formats)}")
        print(f"Templates: {templates_dir}")
        
        if auto_generate:
            self._auto_generate_all()
        else:
            self._generate_on_demand()
    
    def _auto_generate_all(self):
        """Auto-generate all documentation."""
        print("Auto-generating all documentation...")
        # Implementation would go here
    
    def _generate_on_demand(self):
        """Generate documentation on demand."""
        print("Generating documentation on demand...")
        # Implementation would go here

if __name__ == "__main__":
    generator = DocumentationGenerator()
    generator.generate()
