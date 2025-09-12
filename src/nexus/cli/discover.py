"""
Nexus Discovery CLI - Command line interface for the discovery system.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

from rich.console import Console
from rich.panel import Panel

console = Console()

# Minimal config adapter for standalone operation
class _Config:
    def __init__(self, data: Dict[str, Any] = None) -> None:
        self._data = data or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return dict(self._data)
    
    def get_cache_directory(self) -> str:
        return self._data.get('cache_dir', '.nexus/cache')


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for discovery commands."""
    parser = argparse.ArgumentParser(
        prog='nexus discover',
        description='Discover and analyze code structure, dependencies, and patterns'
    )
    
    # Basic arguments
    parser.add_argument(
        'path', 
        nargs='?', 
        default='.', 
        help='Target path to analyze (default: current directory)'
    )
    
    # Output options
    parser.add_argument(
        '--output', 
        choices=['json', 'summary'], 
        default='summary',
        help='Output format (default: summary)'
    )
    
    parser.add_argument(
        '--pretty', 
        action='store_true', 
        help='Pretty-print JSON output'
    )
    
    # Analysis options
    parser.add_argument(
        '--cache', 
        action='store_true', 
        help='Use cached results if available'
    )
    
    parser.add_argument(
        '--deep', 
        action='store_true', 
        help='Enable deeper analysis (slower but more detailed)'
    )
    
    parser.add_argument(
        '--languages', 
        type=str, 
        help='Comma-separated list of languages to focus on (e.g., py,js,ts)'
    )
    
    # Cache management
    parser.add_argument(
        '--clear-cache', 
        action='store_true', 
        help='Clear discovery cache'
    )
    
    return parser


def main() -> None:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Import discovery engine (after argparse to avoid import errors on --help)
    try:
        from nexus.core.discovery.engine import DiscoveryEngine
        from nexus.core.discovery.cache import DiscoveryCache
    except ImportError as e:
        console.print(f"❌ Error importing discovery system: {e}", style="red")
        sys.exit(1)
    
    # Handle cache clearing
    if args.clear_cache:
        config = _Config({'cache_dir': '.nexus/cache'})
        cache = DiscoveryCache(Path(config.get_cache_directory()) / "discovery")
        target_path = Path(args.path).resolve() if args.path != '.' else None
        cache.clear(target_path)
        console.print("🗑️ Discovery cache cleared", style="green")
        return
    
    # Setup configuration
    config = _Config({
        'cache': args.cache,
        'cache_dir': '.nexus/cache'
    })
    
    # Initialize discovery engine
    try:
        engine = DiscoveryEngine(config)
    except Exception as e:
        console.print(f"❌ Error initializing discovery engine: {e}", style="red")
        sys.exit(1)
    
    # Parse options
    options = {
        'cache': args.cache,
        'deep': args.deep
    }
    
    if args.languages:
        options['languages'] = [lang.strip() for lang in args.languages.split(',')]
    
    # Run discovery
    try:
        target_path = Path(args.path).resolve()
        
        if not target_path.exists():
            console.print(f"❌ Target path does not exist: {target_path}", style="red")
            sys.exit(1)
        
        console.print(Panel.fit(f"🔍 Discovering: {target_path}", style="blue"))
        
        results = engine.discover(target_path, options)
        
        # Output results
        if args.output == 'json':
            output = engine.outputs.format_json(results, pretty=args.pretty)
            print(output)
        else:
            output = engine.outputs.format_summary(results)
            console.print(output)
        
    except KeyboardInterrupt:
        console.print("\n⚠️ Discovery interrupted by user", style="yellow")
        sys.exit(130)
    except Exception as e:
        console.print(f"❌ Discovery failed: {e}", style="red")
        if args.deep:  # Show full traceback in deep mode
            import traceback
            console.print(traceback.format_exc(), style="red dim")
        sys.exit(1)


if __name__ == "__main__":
    main()
