"""Content analysis module for processing existing documentation."""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from rich.console import Console

console = Console()

@dataclass
class DocumentPattern:
    """Represents a pattern found in documentation."""
    pattern_type: str
    content: str
    metadata: Dict[str, Any]
    file_path: Path
    line_number: int

@dataclass
class SectionInfo:
    """Information about a documentation section."""
    title: str
    level: int
    content: str
    subsections: List['SectionInfo']
    metadata: Dict[str, Any]

class ContentAnalyzer:
    """Analyze existing documentation content to extract patterns and templates."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize content analyzer.
        
        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root or Path.cwd()
        self.generated_docs_dir = self.project_root / "generated-docs"
        self.patterns: List[DocumentPattern] = []
        self.sections: Dict[str, List[SectionInfo]] = {}
    
    def analyze_existing_content(self) -> Dict[str, Any]:
        """Analyze existing generated-docs content.
        
        Returns:
            Analysis results with patterns and insights
        """
        console.print("🔍 Analyzing existing documentation content...", style="blue")
        
        if not self.generated_docs_dir.exists():
            console.print("⚠️  No generated-docs directory found", style="yellow")
            return {"patterns": [], "sections": {}, "insights": {}}
        
        # Analyze each section
        for section_dir in self.generated_docs_dir.iterdir():
            if section_dir.is_dir():
                self._analyze_section(section_dir)
        
        # Extract patterns
        self._extract_patterns()
        
        # Generate insights
        insights = self._generate_insights()
        
        console.print(f"✅ Analyzed {len(self.patterns)} patterns across {len(self.sections)} sections", style="green")
        
        return {
            "patterns": self.patterns,
            "sections": self.sections,
            "insights": insights
        }
    
    def _analyze_section(self, section_dir: Path) -> None:
        """Analyze a specific documentation section.
        
        Args:
            section_dir: Directory containing section documents
        """
        section_name = section_dir.name
        self.sections[section_name] = []
        
        for md_file in section_dir.glob("*.md"):
            if md_file.name == "index.md":
                continue
            
            sections = self._parse_markdown_sections(md_file)
            self.sections[section_name].extend(sections)
    
    def _parse_markdown_sections(self, file_path: Path) -> List[SectionInfo]:
        """Parse markdown file into sections.
        
        Args:
            file_path: Path to markdown file
            
        Returns:
            List of section information
        """
        content = file_path.read_text()
        sections = []
        current_section = None
        current_content = []
        
        for line_num, line in enumerate(content.split('\n'), 1):
            # Check for headers
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if header_match:
                # Save previous section
                if current_section:
                    current_section.content = '\n'.join(current_content)
                    sections.append(current_section)
                
                # Start new section
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                current_section = SectionInfo(
                    title=title,
                    level=level,
                    content="",
                    subsections=[],
                    metadata={"file": file_path.name, "line": line_num}
                )
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_section:
            current_section.content = '\n'.join(current_content)
            sections.append(current_section)
        
        return sections
    
    def _extract_patterns(self) -> None:
        """Extract patterns from analyzed content."""
        # Common patterns to look for
        patterns_to_find = [
            ("code_block", r'```[\s\S]*?```'),
            ("todo_item", r'- \[[ x]\]\s+(.+)'),
            ("link", r'\[([^\]]+)\]\(([^)]+)\)'),
            ("image", r'!\[([^\]]*)\]\(([^)]+)\)'),
            ("table", r'\|.*\|'),
            ("list_item", r'^\s*[-*+]\s+(.+)'),
            ("numbered_item", r'^\s*\d+\.\s+(.+)'),
            ("bold_text", r'\*\*([^*]+)\*\*'),
            ("italic_text", r'\*([^*]+)\*'),
            ("inline_code", r'`([^`]+)`'),
        ]
        
        for section_name, sections in self.sections.items():
            for section in sections:
                for pattern_type, pattern_regex in patterns_to_find:
                    matches = re.finditer(pattern_regex, section.content, re.MULTILINE)
                    for match in matches:
                        pattern = DocumentPattern(
                            pattern_type=pattern_type,
                            content=match.group(0),
                            metadata={
                                "section": section_name,
                                "title": section.title,
                                "match_group": match.groups()
                            },
                            file_path=Path(section.metadata["file"]),
                            line_number=section.metadata["line"]
                        )
                        self.patterns.append(pattern)
    
    def _generate_insights(self) -> Dict[str, Any]:
        """Generate insights from analyzed content.
        
        Returns:
            Dictionary of insights and statistics
        """
        insights = {
            "total_patterns": len(self.patterns),
            "pattern_counts": {},
            "section_stats": {},
            "common_structures": [],
            "template_suggestions": []
        }
        
        # Count patterns by type
        for pattern in self.patterns:
            pattern_type = pattern.pattern_type
            insights["pattern_counts"][pattern_type] = insights["pattern_counts"].get(pattern_type, 0) + 1
        
        # Section statistics
        for section_name, sections in self.sections.items():
            insights["section_stats"][section_name] = {
                "document_count": len(sections),
                "total_sections": sum(len(s.subsections) + 1 for s in sections),
                "avg_section_length": sum(len(s.content) for s in sections) // max(len(sections), 1)
            }
        
        # Find common structures
        insights["common_structures"] = self._find_common_structures()
        
        # Generate template suggestions
        insights["template_suggestions"] = self._generate_template_suggestions()
        
        return insights
    
    def _find_common_structures(self) -> List[Dict[str, Any]]:
        """Find common structural patterns in documentation.
        
        Returns:
            List of common structures found
        """
        structures = []
        
        # Look for common section patterns
        section_titles = []
        for sections in self.sections.values():
            for section in sections:
                section_titles.append(section.title.lower())
        
        # Find frequently occurring section titles
        from collections import Counter
        title_counts = Counter(section_titles)
        common_titles = title_counts.most_common(10)
        
        for title, count in common_titles:
            if count > 1:  # Only include if it appears multiple times
                structures.append({
                    "type": "common_section",
                    "title": title,
                    "frequency": count,
                    "suggestion": f"Consider creating a template for '{title}' sections"
                })
        
        return structures
    
    def _generate_template_suggestions(self) -> List[Dict[str, Any]]:
        """Generate suggestions for new templates based on analysis.
        
        Returns:
            List of template suggestions
        """
        suggestions = []
        
        # Analyze patterns to suggest templates
        code_blocks = [p for p in self.patterns if p.pattern_type == "code_block"]
        if code_blocks:
            suggestions.append({
                "type": "code_template",
                "description": "Create templates for common code patterns",
                "count": len(code_blocks),
                "example": code_blocks[0].content[:100] + "..." if len(code_blocks[0].content) > 100 else code_blocks[0].content
            })
        
        # Look for TODO patterns
        todos = [p for p in self.patterns if p.pattern_type == "todo_item"]
        if todos:
            suggestions.append({
                "type": "checklist_template",
                "description": "Create checklist templates based on common TODO patterns",
                "count": len(todos),
                "example": todos[0].content
            })
        
        # Look for table patterns
        tables = [p for p in self.patterns if p.pattern_type == "table"]
        if tables:
            suggestions.append({
                "type": "table_template",
                "description": "Create table templates for structured data",
                "count": len(tables),
                "example": tables[0].content
            })
        
        return suggestions
    
    def create_templates_from_patterns(self, output_dir: Path) -> None:
        """Create templates based on analyzed patterns.
        
        Args:
            output_dir: Directory to save generated templates
        """
        console.print("📝 Creating templates from analyzed patterns...", style="blue")
        
        # Create templates directory
        templates_dir = output_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Group patterns by section
        section_patterns = {}
        for pattern in self.patterns:
            section = pattern.metadata["section"]
            if section not in section_patterns:
                section_patterns[section] = []
            section_patterns[section].append(pattern)
        
        # Create templates for each section
        for section, patterns in section_patterns.items():
            self._create_section_templates(section, patterns, templates_dir)
        
        console.print(f"✅ Created templates in {templates_dir}", style="green")
    
    def _create_section_templates(self, section: str, patterns: List[DocumentPattern], templates_dir: Path) -> None:
        """Create templates for a specific section.
        
        Args:
            section: Section name
            patterns: Patterns found in this section
            templates_dir: Templates output directory
        """
        section_dir = templates_dir / section
        section_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a basic template based on common patterns
        template_content = """# {{ title }}

## Overview
{{ description }}

{% for section in sections %}
## {{ section.title }}
{{ section.content }}

{% endfor %}

## Additional Information
{% for pattern in patterns %}
{{ pattern.content }}
{% endfor %}
"""
        
        template_file = section_dir / "analyzed.j2"
        template_file.write_text(template_content)
        
        # Create a pattern-specific template
        pattern_template = self._create_pattern_template(section, patterns)
        pattern_file = section_dir / "patterns.j2"
        pattern_file.write_text(pattern_template)
    
    def _create_pattern_template(self, section: str, patterns: List[DocumentPattern]) -> str:
        """Create a template based on specific patterns.
        
        Args:
            section: Section name
            patterns: Patterns to include
            
        Returns:
            Template content
        """
        # Group patterns by type
        pattern_groups = {}
        for pattern in patterns:
            pattern_type = pattern.pattern_type
            if pattern_type not in pattern_groups:
                pattern_groups[pattern_type] = []
            pattern_groups[pattern_type].append(pattern)
        
        template_parts = [f"# {{ title }} - {section.title()}"]
        
        # Add sections for each pattern type
        for pattern_type, pattern_list in pattern_groups.items():
            if pattern_type == "code_block":
                template_parts.append("## Code Examples")
                template_parts.append("```")
                template_parts.append("{{ code_example }}")
                template_parts.append("```")
            elif pattern_type == "todo_item":
                template_parts.append("## Checklist")
                template_parts.append("{% for item in checklist %}")
                template_parts.append("- [ ] {{ item }}")
                template_parts.append("{% endfor %}")
            elif pattern_type == "table":
                template_parts.append("## Data Table")
                template_parts.append("| Column 1 | Column 2 | Column 3 |")
                template_parts.append("|----------|----------|----------|")
                template_parts.append("| {{ value1 }} | {{ value2 }} | {{ value3 }} |")
        
        return "\n".join(template_parts)
    
    def export_analysis(self, output_file: Path) -> None:
        """Export analysis results to a file.
        
        Args:
            output_file: Path to save analysis results
        """
        import json
        
        # Convert patterns to serializable format
        serializable_patterns = []
        for pattern in self.patterns:
            serializable_patterns.append({
                "pattern_type": pattern.pattern_type,
                "content": pattern.content,
                "metadata": pattern.metadata,
                "file_path": str(pattern.file_path),
                "line_number": pattern.line_number
            })
        
        # Convert sections to serializable format
        serializable_sections = {}
        for section_name, sections in self.sections.items():
            serializable_sections[section_name] = []
            for section in sections:
                serializable_sections[section_name].append({
                    "title": section.title,
                    "level": section.level,
                    "content": section.content,
                    "metadata": section.metadata
                })
        
        analysis_data = {
            "patterns": serializable_patterns,
            "sections": serializable_sections,
            "insights": self._generate_insights()
        }
        
        output_file.write_text(json.dumps(analysis_data, indent=2))
        console.print(f"📊 Analysis exported to {output_file}", style="green")
