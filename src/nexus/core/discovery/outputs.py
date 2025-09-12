"""
Discovery Outputs - Structured output generation for discovery results.
"""

import json
from typing import Dict, Any, Optional


class DiscoveryOutputs:
    """Handles structured output generation for discovery results."""
    
    def __init__(self, config_manager=None):
        """Initialize the outputs handler."""
        self.config = config_manager
    
    def format_json(self, results: Dict[str, Any], pretty: bool = True) -> str:
        """Format results as JSON.
        
        Args:
            results: Discovery results
            pretty: Whether to pretty-print the JSON
            
        Returns:
            JSON string
        """
        if pretty:
            return json.dumps(results, indent=2, default=str)
        else:
            return json.dumps(results, default=str)
    
    def format_summary(self, results: Dict[str, Any]) -> str:
        """Format results as a human-readable summary.
        
        Args:
            results: Discovery results
            
        Returns:
            Formatted summary string
        """
        lines = []
        
        # Header
        target_path = results['metadata']['target_path']
        lines.append(f"🔍 Discovery Results for: {target_path}")
        lines.append("=" * 50)
        lines.append("")
        
        # Basic info
        analysis = results['analysis']
        structure = analysis['structure']
        lines.append(f"📊 Project Overview:")
        lines.append(f"   Total Files: {structure['total_files']}")
        lines.append(f"   Total Size: {self._format_bytes(structure['total_size_bytes'])}")
        lines.append(f"   Languages: {', '.join(analysis['languages'])}")
        lines.append(f"   Frameworks: {', '.join(analysis['frameworks'])}")
        lines.append("")
        
        # Quality assessment
        quality = results['synthesis']['quality_assessment']
        lines.append(f"✅ Quality Assessment:")
        lines.append(f"   Overall Score: {quality['overall_score']}/100 ({quality['assessment']})")
        lines.append(f"   Has Tests: {'Yes' if quality['has_tests'] else 'No'}")
        lines.append(f"   Has Documentation: {'Yes' if quality['has_documentation'] else 'No'}")
        lines.append(f"   Lines of Code: {quality['lines_of_code']:,}")
        lines.append("")
        
        # Architecture
        arch = results['synthesis']['architecture_summary']
        lines.append(f"🏗️ Architecture:")
        lines.append(f"   Type: {arch['type']}")
        lines.append(f"   Application Type: {arch['application_type']}")
        lines.append(f"   Complexity: {arch['complexity']}")
        lines.append("")
        
        # Insights
        insights = results['synthesis']['insights']
        if insights:
            lines.append(f"💡 Key Insights:")
            for insight in insights:
                lines.append(f"   • {insight}")
            lines.append("")
        
        # Recommendations
        recommendations = results['synthesis']['recommendations']
        if recommendations:
            lines.append(f"🎯 Recommendations:")
            for rec in recommendations:
                lines.append(f"   • {rec}")
            lines.append("")
        
        # Validation
        validation = results['validation']
        lines.append(f"✅ Validation:")
        lines.append(f"   Status: {'Valid' if validation['is_valid'] else 'Invalid'}")
        lines.append(f"   Completeness: {validation['completeness_score']}/100")
        
        if validation['warnings']:
            lines.append(f"   Warnings: {len(validation['warnings'])}")
        if validation['errors']:
            lines.append(f"   Errors: {len(validation['errors'])}")
        
        return "\n".join(lines)
    
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
