"""
Discovery Report Manager - Handles saving and managing discovery reports.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from rich.console import Console

console = Console()


class DiscoveryReportManager:
    """Manages discovery report saving and retrieval."""
    
    def __init__(self, config_manager=None):
        """Initialize the report manager.
        
        Args:
            config_manager: Nexus config manager
        """
        self.config = config_manager
        
        # Get docs directory
        if config_manager:
            self.docs_dir = Path(config_manager.get_docs_directory())
        else:
            self.docs_dir = Path("nexus_docs")
        
        self.discovery_dir = self.docs_dir / "discovery"
        self.discovery_dir.mkdir(parents=True, exist_ok=True)
    
    def save_report(self, results: Dict[str, Any], title: str, target_path: Path) -> Path:
        """Save a discovery report with DISC-YYYY-MM-DD-Title naming.
        
        Args:
            results: Discovery results to save
            title: Report title
            target_path: Path that was analyzed
            
        Returns:
            Path to saved report
        """
        # Generate filename with DISC-YYYY-MM-DD-Title format
        date_str = datetime.now().strftime("%Y-%m-%d")
        safe_title = self._sanitize_title(title)
        filename = f"DISC-{date_str}-{safe_title}.md"
        
        report_path = self.discovery_dir / filename
        
        # Generate report content
        content = self._generate_report_content(results, title, target_path)
        
        # Save the report
        report_path.write_text(content, encoding='utf-8')
        
        # Update index
        self._update_index()
        
        return report_path
    
    def list_reports(self) -> List[Dict[str, Any]]:
        """List all discovery reports.
        
        Returns:
            List of report metadata
        """
        reports = []
        
        for report_file in self.discovery_dir.glob("DISC-*.md"):
            if report_file.name == "index.md":
                continue
                
            try:
                metadata = self._extract_report_metadata(report_file)
                reports.append(metadata)
            except Exception:
                # Skip corrupted reports
                continue
        
        # Sort by date (newest first)
        reports.sort(key=lambda x: x.get('date', ''), reverse=True)
        return reports
    
    def get_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific report by ID.
        
        Args:
            report_id: Report ID (filename without extension)
            
        Returns:
            Report content and metadata
        """
        report_file = self.discovery_dir / f"{report_id}.md"
        
        if not report_file.exists():
            return None
        
        try:
            content = report_file.read_text(encoding='utf-8')
            metadata = self._extract_report_metadata(report_file)
            
            return {
                'content': content,
                'metadata': metadata,
                'path': report_file
            }
        except Exception:
            return None
    
    def _sanitize_title(self, title: str) -> str:
        """Sanitize title for use in filename."""
        # Replace spaces and special characters with hyphens
        sanitized = title.lower()
        sanitized = sanitized.replace(' ', '-')
        sanitized = ''.join(c if c.isalnum() or c == '-' else '' for c in sanitized)
        
        # Remove multiple consecutive hyphens
        while '--' in sanitized:
            sanitized = sanitized.replace('--', '-')
        
        # Remove leading/trailing hyphens
        sanitized = sanitized.strip('-')
        
        return sanitized or "discovery-report"
    
    def _generate_report_content(self, results: Dict[str, Any], title: str, target_path: Path) -> str:
        """Generate markdown report content."""
        lines = []
        
        # Frontmatter
        lines.append("---")
        lines.append(f"title: {title}")
        lines.append(f"type: discovery")
        lines.append(f"date: {datetime.now().strftime('%Y-%m-%d')}")
        lines.append(f"target_path: {target_path}")
        lines.append(f"analysis_timestamp: {results['metadata']['timestamp']}")
        lines.append(f"engine_version: {results['metadata']['version']}")
        lines.append(f"deep_analysis: {results['metadata']['options'].get('deep', False)}")
        lines.append(f"languages: {', '.join(results['analysis']['languages'])}")
        lines.append(f"frameworks: {', '.join(results['analysis']['frameworks'])}")
        lines.append("---")
        lines.append("")
        
        # Title
        lines.append(f"# {title}")
        lines.append("")
        lines.append(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")  
        lines.append(f"**Target Path:** `{target_path}`")
        lines.append("")
        
        # Executive Summary
        lines.append("## Executive Summary")
        lines.append("")
        analysis = results['analysis']
        synthesis = results['synthesis']
        
        lines.append(f"This discovery analysis examined **{analysis['structure']['total_files']} files** "
                    f"totaling **{self._format_bytes(analysis['structure']['total_size_bytes'])}** "
                    f"across **{len(analysis['languages'])} programming languages** "
                    f"({', '.join(analysis['languages'])}).")
        lines.append("")
        
        quality = synthesis['quality_assessment']
        lines.append(f"**Quality Score:** {quality['overall_score']}/100 ({quality['assessment']})")
        lines.append(f"**Architecture Type:** {synthesis['architecture_summary']['type']}")
        lines.append(f"**Application Type:** {synthesis['architecture_summary']['application_type']}")
        lines.append("")
        
        # Project Overview
        lines.append("## Project Overview")
        lines.append("")
        lines.append(f"- **Total Files:** {analysis['structure']['total_files']}")
        lines.append(f"- **Total Size:** {self._format_bytes(analysis['structure']['total_size_bytes'])}")
        lines.append(f"- **Languages:** {', '.join(analysis['languages'])}")
        lines.append(f"- **Frameworks:** {', '.join(analysis['frameworks']) if analysis['frameworks'] else 'None detected'}")
        lines.append(f"- **Lines of Code:** {quality['lines_of_code']:,}")
        lines.append("")
        
        # Quality Assessment
        lines.append("## Quality Assessment")
        lines.append("")
        lines.append(f"**Overall Score:** {quality['overall_score']}/100 ({quality['assessment']})")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Has Tests | {'✅ Yes' if quality['has_tests'] else '❌ No'} |")
        lines.append(f"| Has Documentation | {'✅ Yes' if quality['has_documentation'] else '❌ No'} |")
        lines.append(f"| Is Containerized | {'✅ Yes' if quality['is_containerized'] else '❌ No'} |")
        lines.append(f"| Test Files | {quality['test_file_count']} |")
        lines.append(f"| Lines of Code | {quality['lines_of_code']:,} |")
        lines.append("")
        
        # Architecture Analysis
        lines.append("## Architecture Analysis")
        lines.append("")
        arch = synthesis['architecture_summary']
        lines.append(f"**Type:** {arch['type']}")
        lines.append(f"**Application Type:** {arch['application_type']}")
        lines.append(f"**Complexity:** {arch['complexity']}")
        lines.append("")
        
        if arch['patterns']:
            lines.append("**Detected Patterns:**")
            for pattern in arch['patterns']:
                lines.append(f"- {pattern.replace('_', ' ').title()}")
            lines.append("")
        
        # Key Insights
        if synthesis['insights']:
            lines.append("## Key Insights")
            lines.append("")
            for insight in synthesis['insights']:
                lines.append(f"- {insight}")
            lines.append("")
        
        # Recommendations
        if synthesis['recommendations']:
            lines.append("## Recommendations")
            lines.append("")
            for rec in synthesis['recommendations']:
                lines.append(f"- {rec}")
            lines.append("")
        
        # Technology Stack
        lines.append("## Technology Stack")
        lines.append("")
        tech_stack = synthesis['technology_stack']
        lines.append(f"**Main Language:** {tech_stack['main_language']}")
        lines.append(f"**Stack Type:** {tech_stack['stack_type']}")
        lines.append("")
        
        if tech_stack['entry_points']:
            lines.append("**Entry Points:**")
            for entry in tech_stack['entry_points']:
                lines.append(f"- {entry}")
            lines.append("")
        
        # Dependencies
        lines.append("## Dependencies")
        lines.append("")
        deps = analysis['dependencies']
        
        if deps['python']['requirements_txt']:
            lines.append("### Python Dependencies")
            lines.append("```")
            for dep in deps['python']['requirements_txt']:
                lines.append(dep)
            lines.append("```")
            lines.append("")
        
        if deps['javascript']['package_json']:
            lines.append("### JavaScript Dependencies")
            js_deps = deps['javascript']['package_json']
            if 'dependencies' in js_deps:
                lines.append("**Runtime Dependencies:**")
                for name, version in js_deps['dependencies'].items():
                    lines.append(f"- {name}: {version}")
                lines.append("")
        
        # File Structure
        lines.append("## File Structure")
        lines.append("")
        structure = analysis['structure']
        
        lines.append(f"**File Types:**")
        for ext, count in sorted(structure['file_types'].items()):
            lines.append(f"- {ext}: {count} files")
        lines.append("")
        
        if structure['largest_files']:
            lines.append("**Largest Files:**")
            for file_info in structure['largest_files'][:10]:
                lines.append(f"- `{file_info['path']}` ({self._format_bytes(file_info['size'])})")
            lines.append("")
        
        # Validation Results
        lines.append("## Validation Results")
        lines.append("")
        validation = results['validation']
        lines.append(f"**Status:** {'✅ Valid' if validation['is_valid'] else '❌ Invalid'}")
        lines.append(f"**Completeness:** {validation['completeness_score']}/100")
        lines.append("")
        
        if validation['warnings']:
            lines.append("**Warnings:**")
            for warning in validation['warnings']:
                lines.append(f"- {warning}")
            lines.append("")
        
        if validation['errors']:
            lines.append("**Errors:**")
            for error in validation['errors']:
                lines.append(f"- {error}")
            lines.append("")
        
        # Raw Data (JSON)
        lines.append("## Raw Data")
        lines.append("")
        lines.append("For integration with other tools, the complete analysis data is available in JSON format:")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(results, indent=2, default=str))
        lines.append("```")
        
        return "\n".join(lines)
    
    def _extract_report_metadata(self, report_file: Path) -> Dict[str, Any]:
        """Extract metadata from report file."""
        try:
            content = report_file.read_text(encoding='utf-8')
            
            # Extract frontmatter
            if content.startswith('---'):
                end_marker = content.find('---', 3)
                if end_marker != -1:
                    frontmatter = content[3:end_marker]
                    metadata = {}
                    
                    for line in frontmatter.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip()
                    
                    metadata['filename'] = report_file.name
                    metadata['path'] = str(report_file)
                    return metadata
        except Exception:
            pass
        
        # Fallback metadata
        return {
            'filename': report_file.name,
            'path': str(report_file),
            'title': report_file.stem,
            'date': 'Unknown'
        }
    
    def _update_index(self) -> None:
        """Update the discovery index file."""
        reports = self.list_reports()
        
        lines = []
        lines.append("# Discovery Reports")
        lines.append("")
        lines.append("This directory contains discovery analysis reports generated by the Nexus Discovery System.")
        lines.append("")
        lines.append("## Report Naming Convention")
        lines.append("")
        lines.append("Discovery reports follow the naming convention: `DISC-YYYY-MM-DD-Title.md`")
        lines.append("")
        lines.append("- **DISC**: Document type prefix")
        lines.append("- **YYYY-MM-DD**: Date of analysis")
        lines.append("- **Title**: Descriptive title of the analysis")
        lines.append("")
        lines.append("## Available Reports")
        lines.append("")
        
        if reports:
            for report in reports:
                title = report.get('title', report['filename'])
                date = report.get('date', 'Unknown')
                lines.append(f"- **{title}** ({date}) - `{report['filename']}`")
        else:
            lines.append("*No discovery reports yet*")
        
        lines.append("")
        lines.append("## Usage")
        lines.append("")
        lines.append("Generate a new discovery report:")
        lines.append("```bash")
        lines.append('nexus discover --save "Project Analysis"')
        lines.append("```")
        lines.append("")
        lines.append("List all discovery reports:")
        lines.append("```bash")
        lines.append("nexus discovery list")
        lines.append("```")
        lines.append("")
        lines.append("View a specific report:")
        lines.append("```bash")
        lines.append("nexus discovery view DISC-2024-01-15-Project-Analysis")
        lines.append("```")
        
        index_path = self.discovery_dir / "index.md"
        index_path.write_text("\n".join(lines), encoding='utf-8')
    
    def _format_bytes(self, size_bytes: int) -> str:
        """Format byte size as human-readable string."""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        size = float(size_bytes)
        
        while size >= 1024.0 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        
        return f"{size:.1f} {size_names[i]}"
