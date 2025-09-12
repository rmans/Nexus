"""
Discovery Validator - Validates discovery results for completeness and accuracy.
"""

from typing import Dict, List, Any


class DiscoveryValidator:
    """Validates discovery results for completeness and accuracy."""
    
    def __init__(self, config_manager=None):
        """Initialize the validator."""
        self.config = config_manager
    
    def validate(self, analysis_data: Dict[str, Any], synthesis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate discovery results.
        
        Args:
            analysis_data: Raw analysis results
            synthesis_data: Synthesis results
            
        Returns:
            Validation results
        """
        validation = {
            'is_valid': True,
            'completeness_score': 0,
            'warnings': [],
            'errors': [],
            'missing_data': [],
            'analysis_validation': self._validate_analysis(analysis_data),
            'synthesis_validation': self._validate_synthesis(synthesis_data)
        }
        
        # Calculate completeness score
        validation['completeness_score'] = self._calculate_completeness(analysis_data, synthesis_data)
        
        # Collect all warnings and errors
        validation['warnings'].extend(validation['analysis_validation'].get('warnings', []))
        validation['warnings'].extend(validation['synthesis_validation'].get('warnings', []))
        validation['errors'].extend(validation['analysis_validation'].get('errors', []))
        validation['errors'].extend(validation['synthesis_validation'].get('errors', []))
        
        # Set overall validation status
        if validation['errors']:
            validation['is_valid'] = False
        
        return validation
    
    def _validate_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate analysis data."""
        validation = {
            'warnings': [],
            'errors': []
        }
        
        # Check required fields
        required_fields = ['structure', 'dependencies', 'languages', 'frameworks', 'patterns', 'quality_metrics', 'entry_points']
        for field in required_fields:
            if field not in analysis_data:
                validation['errors'].append(f"Missing analysis field: {field}")
        
        # Validate structure data
        structure = analysis_data.get('structure', {})
        if structure.get('total_files', 0) == 0:
            validation['warnings'].append("No files found in analysis")
        
        # Validate languages
        languages = analysis_data.get('languages', [])
        if not languages:
            validation['warnings'].append("No programming languages detected")
        
        # Validate quality metrics
        quality = analysis_data.get('quality_metrics', {})
        if quality.get('total_lines_of_code', 0) == 0:
            validation['warnings'].append("No lines of code counted")
        
        return validation
    
    def _validate_synthesis(self, synthesis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate synthesis data."""
        validation = {
            'warnings': [],
            'errors': []
        }
        
        # Check required fields
        required_fields = ['insights', 'recommendations', 'architecture_summary', 'quality_assessment', 'technology_stack']
        for field in required_fields:
            if field not in synthesis_data:
                validation['errors'].append(f"Missing synthesis field: {field}")
        
        # Validate insights
        insights = synthesis_data.get('insights', [])
        if not insights:
            validation['warnings'].append("No insights generated")
        
        # Validate recommendations
        recommendations = synthesis_data.get('recommendations', [])
        if not recommendations:
            validation['warnings'].append("No recommendations generated")
        
        # Validate quality assessment
        quality = synthesis_data.get('quality_assessment', {})
        if 'overall_score' not in quality:
            validation['errors'].append("Quality assessment missing overall score")
        
        return validation
    
    def _calculate_completeness(self, analysis_data: Dict[str, Any], synthesis_data: Dict[str, Any]) -> int:
        """Calculate completeness score (0-100)."""
        score = 0
        
        # Analysis completeness (60 points max)
        if analysis_data.get('structure', {}).get('total_files', 0) > 0:
            score += 15
        if analysis_data.get('languages'):
            score += 15
        if analysis_data.get('frameworks'):
            score += 10
        if analysis_data.get('patterns'):
            score += 10
        if analysis_data.get('quality_metrics', {}).get('total_lines_of_code', 0) > 0:
            score += 10
        
        # Synthesis completeness (40 points max)
        if synthesis_data.get('insights'):
            score += 15
        if synthesis_data.get('recommendations'):
            score += 15
        if synthesis_data.get('quality_assessment', {}).get('overall_score') is not None:
            score += 10
        
        return min(100, score)
