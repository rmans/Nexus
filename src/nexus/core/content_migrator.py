"""Content migration module for moving existing documentation to new structure."""

import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from rich.console import Console
from rich.progress import Progress, TaskID
from .content_analyzer import ContentAnalyzer
from .templates import TemplateManager

console = Console()

class ContentMigrator:
    """Migrate existing documentation content to new Nexus structure."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize content migrator.
        
        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root or Path.cwd()
        self.generated_docs_dir = self.project_root / "generated-docs"
        self.nexus_docs_dir = self.project_root / "nexus_docs"
        self.analyzer = ContentAnalyzer(self.project_root)
        self.template_manager = TemplateManager(self.project_root)
    
    def migrate_content(self, preserve_original: bool = True) -> Dict[str, Any]:
        """Migrate existing content to new structure.
        
        Args:
            preserve_original: Whether to keep original files
            
        Returns:
            Migration results and statistics
        """
        console.print("🔄 Migrating existing content to new structure...", style="blue")
        
        if not self.generated_docs_dir.exists():
            console.print("⚠️  No generated-docs directory found to migrate", style="yellow")
            return {"migrated": 0, "errors": 0, "warnings": 0}
        
        # Ensure target directory exists
        self.nexus_docs_dir.mkdir(parents=True, exist_ok=True)
        
        migration_stats = {
            "migrated": 0,
            "errors": 0,
            "warnings": 0,
            "files_processed": [],
            "templates_created": 0
        }
        
        with Progress() as progress:
            # Get all markdown files to migrate
            md_files = list(self.generated_docs_dir.rglob("*.md"))
            task = progress.add_task("Migrating files...", total=len(md_files))
            
            for md_file in md_files:
                try:
                    result = self._migrate_file(md_file, preserve_original)
                    migration_stats["migrated"] += result["migrated"]
                    migration_stats["errors"] += result["errors"]
                    migration_stats["warnings"] += result["warnings"]
                    migration_stats["files_processed"].append(str(md_file))
                    
                    if result["template_created"]:
                        migration_stats["templates_created"] += 1
                        
                except Exception as e:
                    console.print(f"❌ Error migrating {md_file}: {e}", style="red")
                    migration_stats["errors"] += 1
                
                progress.update(task, advance=1)
        
        # Create templates from migrated content
        self._create_templates_from_migrated_content()
        
        console.print(f"✅ Migration complete: {migration_stats['migrated']} files migrated", style="green")
        if migration_stats["errors"] > 0:
            console.print(f"⚠️  {migration_stats['errors']} errors occurred", style="yellow")
        
        return migration_stats
    
    def _migrate_file(self, source_file: Path, preserve_original: bool) -> Dict[str, int]:
        """Migrate a single file.
        
        Args:
            source_file: Source file to migrate
            preserve_original: Whether to keep original file
            
        Returns:
            Migration result statistics
        """
        result = {"migrated": 0, "errors": 0, "warnings": 0, "template_created": False}
        
        # Calculate relative path from generated-docs
        try:
            relative_path = source_file.relative_to(self.generated_docs_dir)
        except ValueError:
            # File is not under generated-docs
            result["errors"] += 1
            return result
        
        # Determine target path
        target_file = self.nexus_docs_dir / relative_path
        
        # Create target directory if needed
        target_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Process and migrate content
        try:
            content = source_file.read_text()
            processed_content = self._process_content(content, source_file)
            
            # Write to target location
            target_file.write_text(processed_content)
            result["migrated"] += 1
            
            # Create template if this looks like a template
            if self._is_template_candidate(source_file, content):
                self._create_template_from_file(source_file, content)
                result["template_created"] = True
            
        except Exception as e:
            console.print(f"⚠️  Warning processing {source_file}: {e}", style="yellow")
            result["warnings"] += 1
            
            # Copy file as-is if processing fails
            shutil.copy2(source_file, target_file)
            result["migrated"] += 1
        
        return result
    
    def _process_content(self, content: str, source_file: Path) -> str:
        """Process content during migration.
        
        Args:
            content: Original content
            source_file: Source file path
            
        Returns:
            Processed content
        """
        # Add migration header
        migration_header = f"""<!-- 
This file was migrated from {source_file.relative_to(self.project_root)}
Migrated on: {Path().cwd()}
-->
"""
        
        # Process content
        processed_content = content
        
        # Update relative links to work in new structure
        processed_content = self._update_relative_links(processed_content, source_file)
        
        # Add metadata section if not present
        if "<!-- metadata -->" not in processed_content:
            processed_content = self._add_metadata_section(processed_content, source_file)
        
        return migration_header + processed_content
    
    def _update_relative_links(self, content: str, source_file: Path) -> str:
        """Update relative links in content.
        
        Args:
            content: Content to process
            source_file: Source file path
            
        Returns:
            Content with updated links
        """
        import re
        
        # Find relative links
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        def update_link(match):
            link_text = match.group(1)
            link_url = match.group(2)
            
            # Skip absolute URLs and anchors
            if link_url.startswith(('http://', 'https://', '#')):
                return match.group(0)
            
            # Update relative paths
            if link_url.startswith('./') or not link_url.startswith('/'):
                # Calculate new relative path
                source_dir = source_file.parent
                target_dir = self.nexus_docs_dir / source_dir.relative_to(self.generated_docs_dir)
                
                # Adjust path for new structure
                new_url = link_url  # For now, keep as-is
                return f'[{link_text}]({new_url})'
            
            return match.group(0)
        
        return re.sub(link_pattern, update_link, content)
    
    def _add_metadata_section(self, content: str, source_file: Path) -> str:
        """Add metadata section to content.
        
        Args:
            content: Content to add metadata to
            source_file: Source file path
            
        Returns:
            Content with metadata section
        """
        metadata = f"""<!-- metadata -->
- **Source**: {source_file.relative_to(self.project_root)}
- **Migrated**: {Path().cwd()}
- **Type**: {self._detect_content_type(content)}

"""
        
        # Add metadata after the first header
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('#'):
                lines.insert(i + 1, metadata)
                break
        else:
            # No header found, add at the beginning
            lines.insert(0, metadata)
        
        return '\n'.join(lines)
    
    def _detect_content_type(self, content: str) -> str:
        """Detect the type of content.
        
        Args:
            content: Content to analyze
            
        Returns:
            Detected content type
        """
        content_lower = content.lower()
        
        if any(keyword in content_lower for keyword in ['requirements', 'specification', 'prd']):
            return 'PRD'
        elif any(keyword in content_lower for keyword in ['architecture', 'design', 'system']):
            return 'Architecture'
        elif any(keyword in content_lower for keyword in ['implementation', 'code', 'development']):
            return 'Implementation'
        elif any(keyword in content_lower for keyword in ['test', 'testing', 'validation']):
            return 'Testing'
        elif any(keyword in content_lower for keyword in ['task', 'procedure', 'steps']):
            return 'Task'
        else:
            return 'Documentation'
    
    def _is_template_candidate(self, source_file: Path, content: str) -> bool:
        """Check if a file is a good candidate for template creation.
        
        Args:
            source_file: Source file path
            content: File content
            
        Returns:
            True if file should be converted to template
        """
        # Check for template indicators
        template_indicators = [
            '{{',  # Jinja2 variables
            '{%',  # Jinja2 blocks
            'template',
            'example',
            'boilerplate'
        ]
        
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in template_indicators)
    
    def _create_template_from_file(self, source_file: Path, content: str) -> None:
        """Create a template from a migrated file.
        
        Args:
            source_file: Source file path
            content: File content
        """
        # Determine template category
        relative_path = source_file.relative_to(self.generated_docs_dir)
        category = relative_path.parts[0] if len(relative_path.parts) > 1 else "general"
        
        # Convert content to template format
        template_content = self._convert_to_template(content)
        
        # Create template
        template_name = source_file.stem
        self.template_manager.create_template(
            template_name, 
            template_content, 
            category
        )
    
    def _convert_to_template(self, content: str) -> str:
        """Convert content to template format.
        
        Args:
            content: Original content
            
        Returns:
            Template content
        """
        # Simple conversion - replace common patterns with template variables
        template_content = content
        
        # Replace common patterns with Jinja2 variables
        replacements = [
            (r'(\w+)\s+Project', r'{{ project_name }} Project'),
            (r'(\d{4}-\d{2}-\d{2})', r'{{ date }}'),
            (r'Version\s+(\d+\.\d+\.\d+)', r'Version {{ version }}'),
            (r'Author:\s+(\w+)', r'Author: {{ author }}'),
        ]
        
        import re
        for pattern, replacement in replacements:
            template_content = re.sub(pattern, replacement, template_content)
        
        return template_content
    
    def _create_templates_from_migrated_content(self) -> None:
        """Create templates from all migrated content."""
        console.print("📝 Creating templates from migrated content...", style="blue")
        
        # Analyze migrated content
        analysis = self.analyzer.analyze_existing_content()
        
        # Create templates based on analysis
        if analysis["patterns"]:
            self.analyzer.create_templates_from_patterns(self.nexus_docs_dir)
            console.print("✅ Templates created from migrated content", style="green")
    
    def create_migration_report(self, output_file: Path) -> None:
        """Create a migration report.
        
        Args:
            output_file: Path to save migration report
        """
        console.print("📊 Creating migration report...", style="blue")
        
        # Analyze both original and migrated content
        original_analysis = self.analyzer.analyze_existing_content()
        
        # Update analyzer to look at migrated content
        self.analyzer.generated_docs_dir = self.nexus_docs_dir
        migrated_analysis = self.analyzer.analyze_existing_content()
        
        # Create report
        report_content = f"""# Migration Report

## Overview
This report summarizes the migration of documentation from `generated-docs/` to `nexus_docs/`.

## Statistics

### Original Content
- **Total Patterns Found**: {len(original_analysis['patterns'])}
- **Sections Analyzed**: {len(original_analysis['sections'])}
- **Pattern Types**: {', '.join(original_analysis['insights']['pattern_counts'].keys())}

### Migrated Content
- **Total Patterns Found**: {len(migrated_analysis['patterns'])}
- **Sections Analyzed**: {len(migrated_analysis['sections'])}
- **Pattern Types**: {', '.join(migrated_analysis['insights']['pattern_counts'].keys())}

## Template Suggestions
{self._format_template_suggestions(original_analysis['insights']['template_suggestions'])}

## Migration Notes
- All files have been processed and migrated
- Relative links have been updated where possible
- Metadata sections have been added to migrated files
- Templates have been created based on content patterns

## Next Steps
1. Review migrated content for accuracy
2. Update any remaining broken links
3. Customize templates as needed
4. Use `nexus generate-docs` to create new documentation
"""
        
        output_file.write_text(report_content)
        console.print(f"📊 Migration report saved to {output_file}", style="green")
    
    def _format_template_suggestions(self, suggestions: List[Dict[str, Any]]) -> str:
        """Format template suggestions for the report.
        
        Args:
            suggestions: List of template suggestions
            
        Returns:
            Formatted suggestions string
        """
        if not suggestions:
            return "No specific template suggestions generated."
        
        formatted = []
        for suggestion in suggestions:
            formatted.append(f"- **{suggestion['type']}**: {suggestion['description']} (found {suggestion['count']} instances)")
        
        return '\n'.join(formatted)
