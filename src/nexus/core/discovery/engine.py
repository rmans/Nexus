"""
Discovery Engine - Main orchestrator for code discovery processes.
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from rich.console import Console
from .analyzer import CodeAnalyzer
from .synthesizer import DiscoverySynthesizer
from .validator import DiscoveryValidator
from .cache import DiscoveryCache
from .outputs import DiscoveryOutputs

console = Console()


class DiscoveryEngine:
    """Main engine for orchestrating code discovery processes."""
    
    def __init__(self, config_manager=None):
        """Initialize the discovery engine.
        
        Args:
            config_manager: Nexus config manager (optional for testing)
        """
        self.config = config_manager
        
        # Initialize cache system
        if config_manager:
            cache_dir = Path(config_manager.get_cache_directory()) / "discovery"
        else:
            cache_dir = Path(".nexus/cache/discovery")
        
        self.cache = DiscoveryCache(cache_dir)
        
        # Initialize components
        self.analyzer = CodeAnalyzer(config_manager)
        self.synthesizer = DiscoverySynthesizer(config_manager)
        self.validator = DiscoveryValidator(config_manager)
        self.outputs = DiscoveryOutputs(config_manager)
        
    def discover(self, target_path: Path, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run the complete discovery process for a target file or directory.
        
        Args:
            target_path: Path to analyze
            options: Discovery options (deep, languages, cache, etc.)
            
        Returns:
            Complete discovery results
        """
        target_path = Path(target_path).resolve()
        options = options or {}
        
        # Check cache if enabled
        if options.get('cache', False):
            cached_result = self.cache.get(target_path, options)
            if cached_result:
                console.print("✅ Using cached discovery results", style="green")
                return cached_result
        
        console.print(f"🔍 Starting discovery for: {target_path}", style="blue")
        
        # 1. Analyze the code
        console.print("📊 Analyzing project structure...", style="blue")
        analysis_data = self.analyzer.analyze(target_path, options)
        
        # 2. Synthesize insights
        console.print("🧠 Synthesizing insights...", style="blue")
        synthesis_data = self.synthesizer.synthesize(analysis_data, options)
        
        # 3. Validate results
        console.print("✅ Validating results...", style="blue")
        validation_data = self.validator.validate(analysis_data, synthesis_data)
        
        # 4. Generate metadata
        metadata = self._generate_metadata(target_path, options)
        
        # 5. Package results
        discovery_results = {
            'metadata': metadata,
            'analysis': analysis_data,
            'synthesis': synthesis_data,
            'validation': validation_data
        }
        
        # Cache results if requested
        if options.get('cache', False):
            self.cache.set(target_path, options, discovery_results)
        
        console.print("🎉 Discovery complete!", style="green")
        return discovery_results
    
    def _generate_metadata(self, target_path: Path, options: Dict[str, Any]) -> Dict[str, Any]:
        """Generate metadata for discovery results."""
        return {
            'target_path': str(target_path),
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'options': options,
            'engine': 'nexus-discovery',
            'config_used': self.config.to_dict() if self.config else {}
        }
