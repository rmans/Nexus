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
        project_type = self._determine_project_type(analysis_data)
        
        # Context-aware insights based on project type
        if project_type == 'cli_application':
            if 'click' in frameworks and 'rich' in frameworks:
                insights.append("Professional CLI development framework with Click and Rich console interface")
            elif 'click' in frameworks:
                insights.append("Click-based CLI application with structured command interface")
            else:
                insights.append("Command-line application with entry points defined")
            
            if 'plugin_architecture' in patterns:
                insights.append("Modular plugin architecture - excellent for extensibility and maintainability")
            
            if 'template_system' in patterns:
                insights.append("Template-driven content generation system - professional development approach")
            
            if 'hybrid_configuration' in patterns:
                insights.append("Hybrid configuration system with multi-layer environment support")
            
            if 'cross_platform' in patterns:
                insights.append("Cross-platform installer system - Windows, macOS, and Linux support")
                
        elif project_type == 'web_application':
            if 'django' in frameworks:
                insights.append("Django web application - follows MVT pattern")
            elif 'fastapi' in frameworks:
                insights.append("FastAPI application - modern async API framework")
            elif 'nextjs' in frameworks:
                insights.append("Next.js application - full-stack React framework")
            elif 'react' in frameworks:
                insights.append("React application - component-based frontend framework")
            elif 'vue' in frameworks:
                insights.append("Vue.js application - progressive frontend framework")
            
            if 'api_service' in patterns:
                insights.append("Service-oriented architecture with API layer")
                
        elif project_type == 'data_science':
            if 'pandas' in frameworks and 'numpy' in frameworks:
                insights.append("Data analysis project with pandas and numpy")
            elif 'jupyter' in frameworks:
                insights.append("Jupyter notebook-based data science project")
            elif 'scikit-learn' in frameworks:
                insights.append("Machine learning project with scikit-learn")
                
        elif project_type == 'library':
            insights.append("Python library suitable for distribution")
            if 'documented' in patterns:
                insights.append("Well-documented library with comprehensive API reference")
            if 'has_tests' in patterns:
                insights.append("Tested library with good test coverage")
        
        # Universal insights
        if 'documentation_system' in patterns:
            insights.append("Comprehensive documentation system with multiple specialized guides")
        
        # Additional framework insights (avoid duplicates)
        if project_type != 'web_application' and 'django' in frameworks:
            insights.append("Django web application - follows MVT pattern")
        elif project_type != 'web_application' and 'fastapi' in frameworks:
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
        
        # Determine application type with better classification
        app_type = "unknown"
        project_type = self._determine_project_type(analysis_data)
        
        if project_type == 'cli_application':
            if 'plugin_architecture' in patterns:
                app_type = "cli_framework"
            else:
                app_type = "cli_application"
        elif project_type == 'web_application':
            if any(fw in frameworks for fw in ['django', 'fastapi', 'flask']):
                app_type = "web_backend"
            elif any(fw in frameworks for fw in ['nextjs', 'react', 'vue', 'angular']):
                app_type = "web_frontend"
            else:
                app_type = "web_application"
        elif project_type == 'data_science':
            app_type = "data_analysis"
        elif project_type == 'mobile_application':
            app_type = "mobile_app"
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
        """Assess overall code quality with realistic, context-aware scoring."""
        quality_metrics = analysis_data['quality_metrics']
        patterns = analysis_data['patterns']
        frameworks = analysis_data['frameworks']
        
        # More conservative base score
        score = 40  # Lower base score for realism
        
        # Test coverage - more conservative
        if 'has_tests' in patterns:
            score += 15  # Reduced from 20
            test_ratio = quality_metrics['test_file_count'] / max(1, analysis_data['structure']['total_files'])
            if test_ratio > 0.1:  # More than 10% test files
                score += 8  # Reduced from 10
        
        # Documentation - more conservative
        if 'documented' in patterns:
            score += 12  # Reduced from 15
        if 'documentation_system' in patterns:
            score += 8   # Reduced from 10
        
        # Context-aware bonuses based on project type
        project_type = self._determine_project_type(analysis_data)
        
        if project_type == 'cli_application':
            # CLI-specific bonuses
            if 'cli_application' in patterns:
                score += 10  # Reduced from 15
            if 'rich_output' in patterns:
                score += 5
            if 'plugin_architecture' in patterns:
                score += 8   # Reduced from 10
            if 'template_system' in patterns:
                score += 3   # Reduced from 5
            if 'hybrid_configuration' in patterns:
                score += 3   # Reduced from 5
            if 'cross_platform' in patterns:
                score += 3   # Reduced from 5
                
        elif project_type == 'web_application':
            # Web-specific bonuses
            if any(fw in frameworks for fw in ['django', 'flask', 'fastapi']):
                score += 8
            if any(fw in frameworks for fw in ['react', 'vue', 'angular']):
                score += 8
            if 'api_service' in patterns:
                score += 5
            if 'mvc' in patterns:
                score += 5
                
        elif project_type == 'data_science':
            # Data science bonuses
            if any(fw in frameworks for fw in ['pandas', 'numpy', 'scikit-learn']):
                score += 8
            if 'jupyter' in frameworks:
                score += 5
            if 'notebooks' in patterns:
                score += 3
                
        elif project_type == 'library':
            # Library-specific bonuses
            if 'documented' in patterns:
                score += 5  # Extra bonus for documented libraries
            if 'has_tests' in patterns:
                score += 5  # Extra bonus for tested libraries
            if 'versioned' in patterns:
                score += 3
        
        # Universal quality indicators
        if 'containerized' in patterns:
            score += 8  # Reduced from 10
        
        # Code organization
        if any(pattern in patterns for pattern in ['mvc', 'api_service', 'microservices']):
            score += 8  # Reduced from 10
        
        # Complexity penalties
        total_files = analysis_data['structure']['total_files']
        if total_files > 1000:
            score -= 5  # Large projects are harder to maintain
        elif total_files < 5:
            score -= 10  # Very small projects often lack structure
        
        # Cap excellent projects at 90-95, not 100
        score = max(0, min(95, score))  # Cap at 95 for realism
        
        return {
            'overall_score': score,
            'has_tests': 'has_tests' in patterns,
            'has_documentation': 'documented' in patterns,
            'is_containerized': 'containerized' in patterns,
            'test_file_count': quality_metrics['test_file_count'],
            'lines_of_code': quality_metrics['total_lines_of_code'],
            'assessment': 'excellent' if score >= 80 else 'good' if score >= 60 else 'needs_improvement'
        }
    
    def _determine_project_type(self, analysis_data: Dict[str, Any]) -> str:
        """Determine the project type for context-aware scoring."""
        frameworks = analysis_data['frameworks']
        patterns = analysis_data['patterns']
        entry_points = analysis_data['entry_points']
        
        # Web applications
        if any(fw in frameworks for fw in ['django', 'flask', 'fastapi', 'express', 'koa']):
            return 'web_application'
        if any(fw in frameworks for fw in ['react', 'vue', 'angular', 'nextjs', 'nuxt']):
            return 'web_application'
            
        # Data science projects
        if any(fw in frameworks for fw in ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch']):
            return 'data_science'
        if 'jupyter' in frameworks or 'notebooks' in patterns:
            return 'data_science'
            
        # CLI applications
        if any(fw in frameworks for fw in ['click', 'argparse', 'typer']) and entry_points:
            return 'cli_application'
        if 'cli_application' in patterns:
            return 'cli_application'
            
        # Mobile applications
        if any(fw in frameworks for fw in ['react-native', 'flutter', 'xamarin']):
            return 'mobile_application'
            
        # Default to library
        return 'library'
    
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
