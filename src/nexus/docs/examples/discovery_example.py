#!/usr/bin/env python3
"""Discovery System Example

This example demonstrates how to use the Nexus Discovery System
to analyze codebases and extract insights.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from nexus.core.discovery.engine import DiscoveryEngine
from nexus.core.discovery.cache import DiscoveryCache
from nexus.core.hybrid_config import get_config_manager
from rich.console import Console

console = Console()

def main():
    """Run discovery example."""
    console.print("🔍 Nexus Discovery System Example", style="bold blue")
    console.print("=" * 50)
    
    # Initialize configuration and discovery engine
    config_manager = get_config_manager()
    engine = DiscoveryEngine(config_manager)
    
    # Set up cache
    cache_dir = config_manager.get_cache_dir() / "discovery"
    cache = DiscoveryCache(cache_dir)
    
    # Example 1: Basic discovery
    console.print("\n📊 Example 1: Basic Discovery", style="bold")
    console.print("Analyzing current directory...")
    
    target_path = Path.cwd()
    results = engine.discover(target_path, {'cache': True})
    
    # Display summary
    console.print(engine.outputs.format_summary(results))
    
    # Example 2: Deep analysis
    console.print("\n🔬 Example 2: Deep Analysis", style="bold")
    console.print("Running deep analysis...")
    
    deep_results = engine.discover(target_path, {
        'cache': True,
        'deep': True
    })
    
    # Display insights
    if deep_results.get('synthesis', {}).get('insights'):
        console.print("\n💡 Key Insights:", style="bold green")
        for insight in deep_results['synthesis']['insights'][:3]:
            console.print(f"  • {insight}")
    
    # Example 3: Language-specific analysis
    console.print("\n🐍 Example 3: Python-focused Analysis", style="bold")
    console.print("Analyzing Python code only...")
    
    python_results = engine.discover(target_path, {
        'cache': True,
        'languages': ['python']
    })
    
    # Display tech stack
    if python_results.get('synthesis', {}).get('tech_stack'):
        tech_stack = python_results['synthesis']['tech_stack']
        console.print(f"\n🛠️ Tech Stack: {tech_stack.get('main_language', 'Unknown')}")
        if tech_stack.get('frameworks'):
            console.print(f"  Frameworks: {', '.join(tech_stack['frameworks'])}")
    
    # Example 4: JSON output
    console.print("\n📄 Example 4: JSON Output", style="bold")
    console.print("Generating JSON output...")
    
    json_output = engine.outputs.format_json(results, pretty=True)
    console.print("JSON output generated (first 200 chars):")
    console.print(json_output[:200] + "..." if len(json_output) > 200 else json_output)
    
    # Example 5: Cache management
    console.print("\n🗑️ Example 5: Cache Management", style="bold")
    console.print("Cache statistics:")
    
    cache_stats = cache.get_stats()
    console.print(f"  Cache entries: {cache_stats.get('entries', 0)}")
    console.print(f"  Cache size: {cache_stats.get('size', 0)} bytes")
    console.print(f"  Hit rate: {cache_stats.get('hit_rate', 0):.1%}")
    
    console.print("\n✅ Discovery examples completed!", style="green")
    console.print("\nNext steps:")
    console.print("  • Run 'nexus discover' for CLI usage")
    console.print("  • Use 'nexus discover --help' for options")
    console.print("  • Check the documentation for advanced usage")

if __name__ == "__main__":
    main()
