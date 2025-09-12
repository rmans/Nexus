"""
Code Analyzer - Technical code analysis for the discovery system.
"""

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Set

from rich.console import Console

console = Console()


class CodeAnalyzer:
    """Analyzes code structure, dependencies, and patterns."""
    
    def __init__(self, config_manager=None):
        """Initialize the code analyzer."""
        self.config = config_manager
        
    def analyze(self, target_path: Path, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze the target path for code structure and patterns.
        
        Args:
            target_path: Path to analyze
            options: Analysis options
            
        Returns:
            Analysis results dictionary
        """
        options = options or {}
        
        return {
            'structure': self._analyze_structure(target_path),
            'dependencies': self._analyze_dependencies(target_path),
            'languages': self._detect_languages(target_path, options.get('languages')),
            'frameworks': self._detect_frameworks(target_path),
            'patterns': self._detect_patterns(target_path),
            'quality_metrics': self._analyze_quality(target_path, options.get('deep', False)),
            'entry_points': self._find_entry_points(target_path)
        }
    
    def _analyze_structure(self, target_path: Path) -> Dict[str, Any]:
        """Analyze project structure."""
        structure = {
            'total_files': 0,
            'total_size_bytes': 0,
            'directories': [],
            'file_types': {},
            'largest_files': []
        }
        
        all_files = []
        
        try:
            for item in target_path.rglob('*'):
                if item.is_file() and not self._should_ignore_file(item):
                    file_size = item.stat().st_size
                    file_ext = item.suffix.lower()
                    
                    structure['total_files'] += 1
                    structure['total_size_bytes'] += file_size
                    
                    # Track file types
                    if file_ext:
                        structure['file_types'][file_ext] = structure['file_types'].get(file_ext, 0) + 1
                    
                    # Track largest files
                    all_files.append({
                        'path': str(item.relative_to(target_path)),
                        'size': file_size,
                        'extension': file_ext
                    })
                elif item.is_dir() and not self._should_ignore_dir(item):
                    structure['directories'].append(str(item.relative_to(target_path)))
        except PermissionError:
            console.print("⚠️ Permission denied accessing some files", style="yellow")
        
        # Get top 10 largest files
        structure['largest_files'] = sorted(all_files, key=lambda x: x['size'], reverse=True)[:10]
        
        return structure
    
    def _analyze_dependencies(self, target_path: Path) -> Dict[str, Any]:
        """Analyze project dependencies."""
        dependencies = {
            'python': self._parse_python_dependencies(target_path),
            'javascript': self._parse_javascript_dependencies(target_path),
            'other': {}
        }
        
        return dependencies
    
    def _parse_python_dependencies(self, target_path: Path) -> Dict[str, Any]:
        """Parse Python dependencies from requirements.txt, pyproject.toml, etc."""
        python_deps = {
            'requirements_txt': [],
            'pyproject_toml': {},
            'setup_py': [],
            'pipfile': {}
        }
        
        # requirements.txt
        req_file = target_path / 'requirements.txt'
        if req_file.exists():
            try:
                content = req_file.read_text(encoding='utf-8')
                python_deps['requirements_txt'] = [
                    line.strip() for line in content.splitlines() 
                    if line.strip() and not line.startswith('#')
                ]
            except Exception:
                pass
        
        # pyproject.toml
        pyproject_file = target_path / 'pyproject.toml'
        if pyproject_file.exists():
            try:
                import tomllib
                content = pyproject_file.read_text(encoding='utf-8')
                python_deps['pyproject_toml'] = tomllib.loads(content)
            except Exception:
                # Fallback for systems without tomllib
                pass
        
        return python_deps
    
    def _parse_javascript_dependencies(self, target_path: Path) -> Dict[str, Any]:
        """Parse JavaScript dependencies from package.json."""
        js_deps = {
            'package_json': {},
            'yarn_lock': False,
            'package_lock': False
        }
        
        # package.json
        package_file = target_path / 'package.json'
        if package_file.exists():
            try:
                content = package_file.read_text(encoding='utf-8')
                js_deps['package_json'] = json.loads(content)
            except Exception:
                pass
        
        # Lock files
        js_deps['yarn_lock'] = (target_path / 'yarn.lock').exists()
        js_deps['package_lock'] = (target_path / 'package-lock.json').exists()
        
        return js_deps
    
    def _detect_languages(self, target_path: Path, filter_languages: Optional[List[str]] = None) -> List[str]:
        """Detect programming languages used in the project."""
        language_extensions = {
            '.py': 'python',
            '.js': 'javascript', 
            '.ts': 'typescript',
            '.jsx': 'react',
            '.tsx': 'react-typescript',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.sass': 'sass',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.php': 'php',
            '.rb': 'ruby',
            '.sh': 'shell',
            '.sql': 'sql',
            '.md': 'markdown',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.json': 'json',
            '.xml': 'xml'
        }
        
        detected_languages = set()
        
        try:
            for item in target_path.rglob('*'):
                if item.is_file() and not self._should_ignore_file(item):
                    ext = item.suffix.lower()
                    if ext in language_extensions:
                        lang = language_extensions[ext]
                        if not filter_languages or lang in filter_languages:
                            detected_languages.add(lang)
        except PermissionError:
            pass
        
        return sorted(detected_languages)
    
    def _detect_frameworks(self, target_path: Path) -> List[str]:
        """Detect frameworks and libraries used."""
        frameworks = []
        
        # Python frameworks
        if (target_path / 'manage.py').exists():
            frameworks.append('django')
        
        req_file = target_path / 'requirements.txt'
        if req_file.exists():
            try:
                content = req_file.read_text(encoding='utf-8').lower()
                if 'flask' in content:
                    frameworks.append('flask')
                if 'fastapi' in content:
                    frameworks.append('fastapi')
                if 'django' in content:
                    frameworks.append('django')
                if 'pytest' in content:
                    frameworks.append('pytest')
            except Exception:
                pass
        
        # JavaScript frameworks
        package_file = target_path / 'package.json'
        if package_file.exists():
            try:
                content = package_file.read_text(encoding='utf-8')
                package_data = json.loads(content)
                
                deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
                
                if 'next' in deps:
                    frameworks.append('nextjs')
                if 'react' in deps:
                    frameworks.append('react')
                if 'vue' in deps:
                    frameworks.append('vue')
                if 'angular' in deps or '@angular/core' in deps:
                    frameworks.append('angular')
                if 'express' in deps:
                    frameworks.append('express')
                if 'jest' in deps:
                    frameworks.append('jest')
                if 'vitest' in deps:
                    frameworks.append('vitest')
            except Exception:
                pass
        
        return frameworks
    
    def _detect_patterns(self, target_path: Path) -> List[str]:
        """Detect architectural patterns in the codebase."""
        patterns = []
        
        # Check for common directory patterns
        dirs = [d.name.lower() for d in target_path.iterdir() if d.is_dir()]
        
        # API patterns
        if any(d in dirs for d in ['api', 'apis', 'routes', 'endpoints']):
            patterns.append('api_service')
        
        # MVC pattern
        if all(d in dirs for d in ['models', 'views', 'controllers']):
            patterns.append('mvc')
        elif any(d in dirs for d in ['models', 'views']):
            patterns.append('mvc_like')
        
        # Microservices
        if 'services' in dirs or len([d for d in dirs if 'service' in d]) > 1:
            patterns.append('microservices')
        
        # Monorepo
        if 'packages' in dirs or 'apps' in dirs:
            patterns.append('monorepo')
        
        # Testing
        if any(d in dirs for d in ['test', 'tests', '__tests__', 'spec']):
            patterns.append('has_tests')
        
        # Documentation
        if any(d in dirs for d in ['docs', 'documentation']):
            patterns.append('documented')
        
        # Configuration
        if any(f.exists() for f in [target_path / 'docker-compose.yml', target_path / 'Dockerfile']):
            patterns.append('containerized')
        
        return patterns
    
    def _analyze_quality(self, target_path: Path, deep_analysis: bool = False) -> Dict[str, Any]:
        """Analyze code quality metrics."""
        quality = {
            'total_lines_of_code': 0,
            'test_file_count': 0,
            'python_complexity': {},
            'code_coverage_indicators': []
        }
        
        test_patterns = ['test_', '_test.', 'tests/', '__tests__/', '.spec.', '.test.']
        code_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx'}
        
        try:
            for file_path in target_path.rglob('*'):
                if file_path.is_file() and not self._should_ignore_file(file_path):
                    file_str = str(file_path)
                    
                    # Count lines of code
                    if file_path.suffix in code_extensions:
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                lines = len([line for line in f if line.strip()])
                                quality['total_lines_of_code'] += lines
                        except Exception:
                            pass
                    
                    # Count test files
                    if any(pattern in file_str.lower() for pattern in test_patterns):
                        quality['test_file_count'] += 1
                    
                    # Python complexity analysis (if deep analysis enabled)
                    if deep_analysis and file_path.suffix == '.py':
                        complexity = self._analyze_python_complexity(file_path)
                        if complexity > 0:
                            relative_path = str(file_path.relative_to(target_path))
                            quality['python_complexity'][relative_path] = complexity
        except Exception:
            pass
        
        # Look for coverage indicators
        coverage_files = ['.coverage', 'coverage.xml', 'htmlcov/', 'coverage/']
        for coverage_file in coverage_files:
            if (target_path / coverage_file).exists():
                quality['code_coverage_indicators'].append(coverage_file)
        
        return quality
    
    def _analyze_python_complexity(self, file_path: Path) -> int:
        """Analyze Python file complexity using AST."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            complexity = 1  # Base complexity
            
            for node in ast.walk(tree):
                # Add complexity for control flow statements
                if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                    complexity += 1
                elif isinstance(node, ast.BoolOp):
                    complexity += len(node.values) - 1
                elif isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)):
                    complexity += 1
            
            return complexity
        except Exception:
            return 0
    
    def _find_entry_points(self, target_path: Path) -> List[str]:
        """Find application entry points."""
        entry_points = []
        
        # Common Python entry points
        python_entries = ['main.py', 'app.py', 'manage.py', 'run.py', '__main__.py']
        for entry in python_entries:
            if (target_path / entry).exists():
                entry_points.append(entry)
        
        # Package.json scripts
        package_file = target_path / 'package.json'
        if package_file.exists():
            try:
                content = package_file.read_text(encoding='utf-8')
                package_data = json.loads(content)
                scripts = package_data.get('scripts', {})
                
                # Look for common entry script names
                for script_name in ['start', 'dev', 'serve', 'main']:
                    if script_name in scripts:
                        entry_points.append(f"npm run {script_name}")
            except Exception:
                pass
        
        return entry_points
    
    def _should_ignore_file(self, file_path: Path) -> bool:
        """Check if file should be ignored during analysis."""
        ignore_patterns = [
            '.git/', 'node_modules/', '__pycache__/', '.pytest_cache/',
            'venv/', 'env/', '.env/', 'build/', 'dist/', '.next/',
            '.DS_Store', '*.pyc', '*.pyo', '*.pyd', '*.so', '*.egg-info/'
        ]
        
        file_str = str(file_path).lower()
        return any(pattern.lower() in file_str for pattern in ignore_patterns)
    
    def _should_ignore_dir(self, dir_path: Path) -> bool:
        """Check if directory should be ignored during analysis."""
        ignore_dirs = {
            '.git', 'node_modules', '__pycache__', '.pytest_cache',
            'venv', 'env', '.env', 'build', 'dist', '.next',
            '.vscode', '.idea', 'htmlcov'
        }
        
        return dir_path.name.lower() in ignore_dirs
