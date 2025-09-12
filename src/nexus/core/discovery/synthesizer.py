"""
Discovery Synthesizer - Turns raw analysis into insights and recommendations.
"""

from typing import Dict, List, Optional, Any


class DiscoverySynthesizer:
    """Synthesizes analysis data into insights and recommendations."""
    
    def __init__(self, config_manager=None):
        """Initialize the synthesizer."""
        self.config = config_manager
    
    def synthesize(self, analysis_data: Dict[str, Any], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Synthesize analysis data into insights and recommendations.
        
        Args:
            analysis_data: Raw analysis results
            options: Synthesis options
            
        Returns:
            Synthesis results
        """
        return {
            'insights': self._generate_insights(analysis_data),
            'recommendations': self._generate_recommendations(analysis_data),
            'architecture_summary': self._summarize_architecture(analysis_data),
            'quality_assessment': self._assess_quality(analysis_data),
            'technology_stack': self._summarize_tech_stack(analysis_data)
        }
    
    def _generate_insights(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Generate insights from analysis data."""
        insights = []
        
        # Project size insights
        total_files = analysis_data['structure']['total_files']
        if total_files > 1000:
            insights.append(f"Large codebase with {total_files} files - consider modularization")
        elif total_files < 10:
            insights.append("Small project - good for rapid development")
        
        # Language diversity
        languages = analysis_data['languages']
        if len(languages) > 3:
            insights.append(f"Multi-language project using {', '.join(languages)}")
        elif 'python' in languages and 'javascript' in languages:
            insights.append("Full-stack project with Python backend and JavaScript frontend")
        
        # Framework insights
        frameworks = analysis_data['frameworks']
        patterns = analysis_data['patterns']
        
        # CLI Framework insights
        if 'cli_application' in patterns:
            if 'click' in frameworks and 'rich' in frameworks:
                insights.append("Professional CLI development framework with Click and Rich console interface")
            elif 'click' in frameworks:
                insights.append("Click-based CLI application with structured command interface")
            else:
                insights.append("Command-line application with entry points defined")
        
        # Plugin architecture insights
        if 'plugin_architecture' in patterns:
            insights.append("Modular plugin architecture - excellent for extensibility and maintainability")
        
        # Template system insights
        if 'template_system' in patterns:
            insights.append("Template-driven content generation system - professional development approach")
        
        # Configuration insights
        if 'hybrid_configuration' in patterns:
            insights.append("Hybrid configuration system with multi-layer environment support")
        
        # Cross-platform insights
        if 'cross_platform' in patterns:
            insights.append("Cross-platform installer system - Windows, macOS, and Linux support")
        
        # Documentation system insights
        if 'documentation_system' in patterns:
            insights.append("Comprehensive documentation system with multiple specialized guides")
        
        # Traditional framework insights
        if 'django' in frameworks:
            insights.append("Django web application - follows MVT pattern")
        elif 'fastapi' in frameworks:
            insights.append("FastAPI application - modern async API framework")
        elif 'nextjs' in frameworks:
            insights.append("Next.js application - full-stack React framework")
        
        # Testing insights
        patterns = analysis_data['patterns']
        if 'has_tests' in patterns:
            test_count = analysis_data['quality_metrics']['test_file_count']
            insights.append(f"Well-tested project with {test_count} test files")
        else:
            insights.append("No testing structure detected - consider adding tests")
        
        # Architecture insights
        if 'api_service' in patterns:
            insights.append("Service-oriented architecture with API layer")
        if 'microservices' in patterns:
            insights.append("Microservices architecture - distributed system design")
        if 'monorepo' in patterns:
            insights.append("Monorepo structure - multiple packages in single repository")
        
        return insights
    
    def _generate_recommendations(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Testing recommendations
        patterns = analysis_data['patterns']
        if 'has_tests' not in patterns:
            frameworks = analysis_data['frameworks']
            if 'python' in analysis_data['languages']:
                if 'pytest' not in frameworks:
                    recommendations.append("Add pytest for Python testing")
            if 'javascript' in analysis_data['languages'] or 'typescript' in analysis_data['languages']:
                if 'jest' not in frameworks and 'vitest' not in frameworks:
                    recommendations.append("Add Jest or Vitest for JavaScript testing")
        
        # Documentation recommendations
        if 'documented' not in patterns:
            recommendations.append("Add documentation directory and README files")
        
        # Containerization recommendations
        if 'containerized' not in patterns:
            if any(fw in analysis_data['frameworks'] for fw in ['django', 'fastapi', 'express', 'nextjs']):
                recommendations.append("Consider adding Docker for containerization")
        
        # Quality recommendations
        quality = analysis_data['quality_metrics']
        if quality['total_lines_of_code'] > 10000 and quality['test_file_count'] == 0:
            recommendations.append("Large codebase without tests - prioritize test coverage")
        
        # Dependencies recommendations
        python_deps = analysis_data['dependencies']['python']
        if python_deps['requirements_txt'] and not python_deps['pyproject_toml']:
            recommendations.append("Consider migrating to pyproject.toml for modern Python packaging")
        
        return recommendations
    
    def _summarize_architecture(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize the project architecture."""
        patterns = analysis_data['patterns']
        frameworks = analysis_data['frameworks']
        
        architecture_type = "unknown"
        if 'monorepo' in patterns:
            architecture_type = "monorepo"
        elif 'microservices' in patterns:
            architecture_type = "microservices"
        elif 'api_service' in patterns:
            architecture_type = "api_service"
        elif 'mvc' in patterns or 'mvc_like' in patterns:
            architecture_type = "mvc"
        else:
            architecture_type = "standard"
        
        # Determine application type
        app_type = "unknown"
        if 'cli_application' in patterns:
            app_type = "cli_framework"
        elif any(fw in frameworks for fw in ['django', 'fastapi', 'flask']):
            app_type = "web_api"
        elif any(fw in frameworks for fw in ['nextjs', 'react', 'vue', 'angular']):
            app_type = "web_frontend" 
        elif 'express' in frameworks:
            app_type = "web_backend"
        elif analysis_data['entry_points']:
            app_type = "application"
        else:
            app_type = "library"
        
        # Enhanced architecture type detection
        if 'cli_application' in patterns and 'plugin_architecture' in patterns:
            architecture_type = "cli_development_framework"
        elif 'cli_application' in patterns:
            architecture_type = "cli_application"
        elif 'plugin_architecture' in patterns:
            architecture_type = "plugin_based"
        elif 'microservices' in patterns:
            architecture_type = "microservices"
        elif 'monorepo' in patterns:
            architecture_type = "monorepo"
        elif 'api_service' in patterns:
            architecture_type = "api_service"
        elif 'mvc' in patterns or 'mvc_like' in patterns:
            architecture_type = "mvc"
        else:
            architecture_type = "standard"
        
        return {
            'type': architecture_type,
            'application_type': app_type,
            'patterns': patterns,
            'complexity': 'high' if len(patterns) > 3 else 'medium' if len(patterns) > 1 else 'low'
        }
    
    def _assess_quality(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall code quality."""
        quality_metrics = analysis_data['quality_metrics']
        patterns = analysis_data['patterns']
        
        # Calculate quality score (0-100)
        score = 50  # Base score
        
        # Test coverage indicator
        if 'has_tests' in patterns:
            score += 20
            test_ratio = quality_metrics['test_file_count'] / max(1, analysis_data['structure']['total_files'])
            if test_ratio > 0.1:  # More than 10% test files
                score += 10
        
        # Documentation - enhanced scoring
        if 'documented' in patterns:
            score += 15
        if 'documentation_system' in patterns:
            score += 10  # Bonus for comprehensive documentation system
        
        # CLI Framework bonus
        if 'cli_application' in patterns:
            score += 15  # CLI applications are well-structured
        if 'plugin_architecture' in patterns:
            score += 10  # Plugin architecture shows good design
        if 'template_system' in patterns:
            score += 5   # Template system shows sophistication
        if 'hybrid_configuration' in patterns:
            score += 5   # Advanced configuration system
        if 'cross_platform' in patterns:
            score += 5   # Cross-platform support
        if 'rich_output' in patterns:
            score += 5   # Professional user interface
        
        # Containerization
        if 'containerized' in patterns:
            score += 10
        
        # Code organization
        if any(pattern in patterns for pattern in ['mvc', 'api_service', 'microservices']):
            score += 10
        
        # Complexity penalty
        total_files = analysis_data['structure']['total_files']
        if total_files > 1000:
            score -= 5  # Large projects are harder to maintain
        
        score = max(0, min(100, score))  # Clamp to 0-100
        
        return {
            'overall_score': score,
            'has_tests': 'has_tests' in patterns,
            'has_documentation': 'documented' in patterns,
            'is_containerized': 'containerized' in patterns,
            'test_file_count': quality_metrics['test_file_count'],
            'lines_of_code': quality_metrics['total_lines_of_code'],
            'assessment': 'excellent' if score >= 80 else 'good' if score >= 60 else 'needs_improvement'
        }
    
    def _summarize_tech_stack(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize the technology stack."""
        return {
            'languages': analysis_data['languages'],
            'frameworks': analysis_data['frameworks'],
            'main_language': self._determine_main_language(analysis_data),
            'stack_type': self._determine_stack_type(analysis_data),
            'entry_points': analysis_data['entry_points']
        }
    
    def _determine_main_language(self, analysis_data: Dict[str, Any]) -> str:
        """Determine the main programming language."""
        languages = analysis_data['languages']
        frameworks = analysis_data['frameworks']
        
        # Check frameworks first for hints
        if any(fw in frameworks for fw in ['django', 'fastapi', 'flask', 'pytest']):
            return 'python'
        elif any(fw in frameworks for fw in ['nextjs', 'react', 'vue', 'angular', 'express', 'jest']):
            return 'javascript' if 'javascript' in languages else 'typescript'
        
        # Fall back to first language detected
        return languages[0] if languages else 'unknown'
    
    def _determine_stack_type(self, analysis_data: Dict[str, Any]) -> str:
        """Determine the type of technology stack."""
        frameworks = analysis_data['frameworks']
        languages = analysis_data['languages']
        patterns = analysis_data['patterns']
        
        # CLI Framework detection
        if 'cli_application' in patterns and 'plugin_architecture' in patterns:
            return 'cli_development_framework'
        elif 'cli_application' in patterns:
            return 'cli_application'
        
        # Full-stack detection
        has_backend = any(fw in frameworks for fw in ['django', 'fastapi', 'flask', 'express'])
        has_frontend = any(fw in frameworks for fw in ['nextjs', 'react', 'vue', 'angular'])
        
        if has_backend and has_frontend:
            return 'full_stack'
        elif has_backend:
            return 'backend'
        elif has_frontend:
            return 'frontend'
        elif 'python' in languages:
            return 'python_application'
        elif 'javascript' in languages or 'typescript' in languages:
            return 'javascript_application'
        else:
            return 'unknown'
