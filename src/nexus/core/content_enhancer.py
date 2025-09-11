"""Content enhancement module for improving documentation quality."""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from rich.console import Console
from .content_analyzer import ContentAnalyzer, SectionInfo

console = Console()

@dataclass
class EnhancementRule:
    """Represents a content enhancement rule."""
    name: str
    pattern: str
    replacement: str
    description: str
    category: str

@dataclass
class EnhancementSuggestion:
    """Represents a suggestion for content enhancement."""
    rule_name: str
    file_path: Path
    line_number: int
    original_text: str
    suggested_text: str
    confidence: float
    category: str

class ContentEnhancer:
    """Enhance documentation content using patterns and best practices."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize content enhancer.
        
        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root or Path.cwd()
        self.analyzer = ContentAnalyzer(self.project_root)
        self.enhancement_rules = self._load_enhancement_rules()
        self.suggestions: List[EnhancementSuggestion] = []
    
    def _load_enhancement_rules(self) -> List[EnhancementRule]:
        """Load enhancement rules for content improvement.
        
        Returns:
            List of enhancement rules
        """
        rules = [
            # Structure improvements
            EnhancementRule(
                name="add_toc",
                pattern=r"^# (.+)$",
                replacement=r"# \1\n\n## Table of Contents\n- [Overview](#overview)\n- [Requirements](#requirements)\n- [Implementation](#implementation)\n- [Testing](#testing)\n",
                description="Add table of contents to documents",
                category="structure"
            ),
            
            # Code block improvements
            EnhancementRule(
                name="improve_code_blocks",
                pattern=r"```(\w+)?\n(.*?)\n```",
                replacement=r"```\1\n\2\n```\n\n*Code explanation: Add description of what this code does*",
                description="Add explanations to code blocks",
                category="code"
            ),
            
            # Link improvements
            EnhancementRule(
                name="improve_links",
                pattern=r"\[([^\]]+)\]\(([^)]+)\)",
                replacement=r"[\1](\2) - *Add link description*",
                description="Add descriptions to links",
                category="links"
            ),
            
            # List improvements
            EnhancementRule(
                name="improve_lists",
                pattern=r"^(\s*)[-*+]\s+(.+)$",
                replacement=r"\1- **\2** - *Add description*",
                description="Improve list item formatting",
                category="formatting"
            ),
            
            # Header improvements
            EnhancementRule(
                name="improve_headers",
                pattern=r"^## (.+)$",
                replacement=r"## \1\n\n*Brief description of this section*",
                description="Add descriptions to section headers",
                category="structure"
            ),
            
            # TODO improvements
            EnhancementRule(
                name="improve_todos",
                pattern=r"- \[ \]\s+(.+)",
                replacement=r"- [ ] **\1** - *Add priority and deadline*",
                description="Improve TODO item formatting",
                category="tasks"
            ),
            
            # Table improvements
            EnhancementRule(
                name="improve_tables",
                pattern=r"\|(.+)\|\n\|[-:]+\|\n(\|.+\|)",
                replacement=r"| \1 |\n|:---|\n\2\n\n*Table description: Add explanation of table contents*",
                description="Add descriptions to tables",
                category="tables"
            ),
            
            # Image improvements
            EnhancementRule(
                name="improve_images",
                pattern=r"!\[([^\]]*)\]\(([^)]+)\)",
                replacement=r"![\\1](\\2)\n\n*Image description: Add alt text and explanation*",
                description="Add descriptions to images",
                category="media"
            ),
            
            # Emphasis improvements
            EnhancementRule(
                name="improve_emphasis",
                pattern=r"\*\*([^*]+)\*\*",
                replacement=r"**\\1** - *Add explanation*",
                description="Add explanations to emphasized text",
                category="formatting"
            ),
            
            # Code improvements
            EnhancementRule(
                name="improve_inline_code",
                pattern=r"`([^`]+)`",
                replacement=r"`\\1` - *Add description*",
                description="Add descriptions to inline code",
                category="code"
            )
        ]
        
        return rules
    
    def analyze_and_enhance(self, target_dir: Optional[Path] = None) -> Dict[str, Any]:
        """Analyze content and generate enhancement suggestions.
        
        Args:
            target_dir: Directory to analyze (defaults to nexus_docs)
            
        Returns:
            Analysis results with enhancement suggestions
        """
        if target_dir is None:
            target_dir = self.project_root / "nexus_docs"
        
        console.print(f"🔍 Analyzing content in {target_dir}...", style="blue")
        
        if not target_dir.exists():
            console.print(f"⚠️  Directory not found: {target_dir}", style="yellow")
            return {"suggestions": [], "files_analyzed": 0}
        
        # Analyze content
        self.analyzer.generated_docs_dir = target_dir
        analysis = self.analyzer.analyze_existing_content()
        
        # Generate enhancement suggestions
        self.suggestions = []
        files_analyzed = 0
        
        for section_name, sections in analysis["sections"].items():
            for section in sections:
                file_path = target_dir / section_name / f"{section.title.lower().replace(' ', '_')}.md"
                if file_path.exists():
                    self._analyze_file_for_enhancements(file_path)
                    files_analyzed += 1
        
        console.print(f"✅ Generated {len(self.suggestions)} enhancement suggestions", style="green")
        
        return {
            "suggestions": self.suggestions,
            "files_analyzed": files_analyzed,
            "rules_applied": len(self.enhancement_rules)
        }
    
    def _analyze_file_for_enhancements(self, file_path: Path) -> None:
        """Analyze a file for enhancement opportunities.
        
        Args:
            file_path: File to analyze
        """
        try:
            content = file_path.read_text()
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for rule in self.enhancement_rules:
                    matches = re.finditer(rule.pattern, line, re.MULTILINE | re.DOTALL)
                    for match in matches:
                        # Calculate confidence based on pattern complexity
                        confidence = self._calculate_confidence(rule, match, line)
                        
                        if confidence > 0.3:  # Only suggest if confidence is reasonable
                            suggestion = EnhancementSuggestion(
                                rule_name=rule.name,
                                file_path=file_path,
                                line_number=line_num,
                                original_text=match.group(0),
                                suggested_text=match.expand(rule.replacement),
                                confidence=confidence,
                                category=rule.category
                            )
                            self.suggestions.append(suggestion)
        
        except Exception as e:
            console.print(f"⚠️  Error analyzing {file_path}: {e}", style="yellow")
    
    def _calculate_confidence(self, rule: EnhancementRule, match: re.Match, line: str) -> float:
        """Calculate confidence score for an enhancement suggestion.
        
        Args:
            rule: Enhancement rule
            match: Regex match object
            line: Original line text
            
        Returns:
            Confidence score between 0 and 1
        """
        confidence = 0.5  # Base confidence
        
        # Adjust based on rule category
        if rule.category == "structure":
            confidence += 0.2
        elif rule.category == "code":
            confidence += 0.1
        elif rule.category == "formatting":
            confidence += 0.05
        
        # Adjust based on line length (longer lines might need more enhancement)
        if len(line) > 100:
            confidence += 0.1
        elif len(line) < 20:
            confidence -= 0.1
        
        # Adjust based on existing enhancements (avoid over-enhancement)
        if "description" in line.lower() or "explanation" in line.lower():
            confidence -= 0.2
        
        return max(0.0, min(1.0, confidence))
    
    def apply_enhancements(self, suggestions: Optional[List[EnhancementSuggestion]] = None, 
                          dry_run: bool = True) -> Dict[str, Any]:
        """Apply enhancement suggestions to files.
        
        Args:
            suggestions: Specific suggestions to apply (uses all if None)
            dry_run: If True, only show what would be changed
            
        Returns:
            Application results
        """
        if suggestions is None:
            suggestions = self.suggestions
        
        if not suggestions:
            console.print("ℹ️  No enhancement suggestions to apply", style="blue")
            return {"applied": 0, "skipped": 0, "errors": 0}
        
        console.print(f"🔧 {'Previewing' if dry_run else 'Applying'} {len(suggestions)} enhancements...", style="blue")
        
        results = {"applied": 0, "skipped": 0, "errors": 0}
        
        # Group suggestions by file
        file_suggestions = {}
        for suggestion in suggestions:
            file_path = suggestion.file_path
            if file_path not in file_suggestions:
                file_suggestions[file_path] = []
            file_suggestions[file_path].append(suggestion)
        
        for file_path, file_suggestions_list in file_suggestions.items():
            try:
                if dry_run:
                    self._preview_enhancements(file_path, file_suggestions_list)
                else:
                    self._apply_file_enhancements(file_path, file_suggestions_list)
                    results["applied"] += len(file_suggestions_list)
            except Exception as e:
                console.print(f"❌ Error processing {file_path}: {e}", style="red")
                results["errors"] += 1
        
        if dry_run:
            console.print("💡 Run with dry_run=False to apply changes", style="yellow")
        else:
            console.print(f"✅ Applied {results['applied']} enhancements", style="green")
        
        return results
    
    def _preview_enhancements(self, file_path: Path, suggestions: List[EnhancementSuggestion]) -> None:
        """Preview enhancements for a file.
        
        Args:
            file_path: File to preview
            suggestions: Suggestions to preview
        """
        console.print(f"\n📄 {file_path.relative_to(self.project_root)}", style="bold blue")
        
        for suggestion in suggestions:
            console.print(f"  Line {suggestion.line_number}: {suggestion.rule_name}", style="cyan")
            console.print(f"    Original: {suggestion.original_text[:60]}...", style="dim")
            console.print(f"    Enhanced: {suggestion.suggested_text[:60]}...", style="green")
            console.print(f"    Confidence: {suggestion.confidence:.2f}", style="yellow")
    
    def _apply_file_enhancements(self, file_path: Path, suggestions: List[EnhancementSuggestion]) -> None:
        """Apply enhancements to a file.
        
        Args:
            file_path: File to enhance
            suggestions: Suggestions to apply
        """
        content = file_path.read_text()
        lines = content.split('\n')
        
        # Sort suggestions by line number (descending) to avoid index issues
        suggestions.sort(key=lambda s: s.line_number, reverse=True)
        
        for suggestion in suggestions:
            line_idx = suggestion.line_number - 1
            if 0 <= line_idx < len(lines):
                # Apply the enhancement
                lines[line_idx] = suggestion.suggested_text
        
        # Write back to file
        enhanced_content = '\n'.join(lines)
        file_path.write_text(enhanced_content)
    
    def create_enhancement_report(self, output_file: Path) -> None:
        """Create a report of enhancement suggestions.
        
        Args:
            output_file: Path to save enhancement report
        """
        console.print("📊 Creating enhancement report...", style="blue")
        
        # Group suggestions by category
        category_suggestions = {}
        for suggestion in self.suggestions:
            category = suggestion.category
            if category not in category_suggestions:
                category_suggestions[category] = []
            category_suggestions[category].append(suggestion)
        
        # Create report content
        report_content = f"""# Content Enhancement Report

## Overview
This report contains suggestions for improving documentation content quality.

## Summary
- **Total Suggestions**: {len(self.suggestions)}
- **Files Analyzed**: {len(set(s.file_path for s in self.suggestions))}
- **Categories**: {', '.join(category_suggestions.keys())}

## Suggestions by Category

"""
        
        for category, suggestions in category_suggestions.items():
            report_content += f"### {category.title()}\n"
            report_content += f"**Count**: {len(suggestions)}\n\n"
            
            for suggestion in suggestions[:5]:  # Show first 5 examples
                report_content += f"- **{suggestion.rule_name}** (confidence: {suggestion.confidence:.2f})\n"
                report_content += f"  - File: {suggestion.file_path.relative_to(self.project_root)}\n"
                report_content += f"  - Line: {suggestion.line_number}\n"
                report_content += f"  - Original: `{suggestion.original_text[:50]}...`\n"
                report_content += f"  - Suggested: `{suggestion.suggested_text[:50]}...`\n\n"
            
            if len(suggestions) > 5:
                report_content += f"*... and {len(suggestions) - 5} more suggestions*\n\n"
        
        report_content += """## How to Apply Enhancements

1. Review the suggestions above
2. Use `nexus enhance-content --preview` to see changes
3. Use `nexus enhance-content --apply` to apply changes
4. Review and customize applied changes as needed

## Best Practices

- Always review suggestions before applying
- Customize generic suggestions to fit your content
- Test changes in a development environment first
- Consider the context and audience for each change
"""
        
        output_file.write_text(report_content)
        console.print(f"📊 Enhancement report saved to {output_file}", style="green")
    
    def get_enhancement_stats(self) -> Dict[str, Any]:
        """Get statistics about enhancement suggestions.
        
        Returns:
            Dictionary of enhancement statistics
        """
        if not self.suggestions:
            return {"total": 0, "by_category": {}, "by_confidence": {}}
        
        # Count by category
        category_counts = {}
        for suggestion in self.suggestions:
            category = suggestion.category
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Count by confidence level
        confidence_levels = {"high": 0, "medium": 0, "low": 0}
        for suggestion in self.suggestions:
            if suggestion.confidence >= 0.7:
                confidence_levels["high"] += 1
            elif suggestion.confidence >= 0.4:
                confidence_levels["medium"] += 1
            else:
                confidence_levels["low"] += 1
        
        return {
            "total": len(self.suggestions),
            "by_category": category_counts,
            "by_confidence": confidence_levels,
            "files_affected": len(set(s.file_path for s in self.suggestions))
        }
