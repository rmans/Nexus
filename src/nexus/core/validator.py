"""Project validation module."""

from pathlib import Path
from rich.console import Console

console = Console()

def validate_project(fix=False, strict=False):
    """Validate project configuration and structure.
    
    Args:
        fix: Automatically fix issues where possible
        strict: Use strict validation rules
    """
    console.print("🔍 Validating project...", style="blue")
    
    issues = []
    warnings = []
    
    # Check if Nexus is initialized
    nexus_dir = Path(".nexus")
    if not nexus_dir.exists():
        issues.append("Nexus not initialized. Run 'nexus init-project'")
    else:
        # Check configuration file
        config_file = nexus_dir / "config.json"
        if not config_file.exists():
            issues.append("Configuration file missing")
        
        # Check docs directory
        docs_dir = Path("nexus_docs")
        if not docs_dir.exists():
            warnings.append("Documentation directory not found")
        
        # Check Cursor rules
        cursor_rules = Path(".cursor/rules")
        if not cursor_rules.exists():
            warnings.append("Cursor rules directory not found")
    
    # Report issues
    if issues:
        console.print("❌ Issues found:", style="red")
        for issue in issues:
            console.print(f"  • {issue}")
    
    if warnings:
        console.print("⚠️  Warnings:", style="yellow")
        for warning in warnings:
            console.print(f"  • {warning}")
    
    if not issues and not warnings:
        console.print("✅ Project validation passed", style="green")
    elif not issues:
        console.print("✅ Project validation passed with warnings", style="green")
    else:
        console.print("❌ Project validation failed", style="red")
    
    if fix:
        console.print("🔧 Fix mode not yet implemented", style="yellow")
