"""Status module for showing project status."""

import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def show_status(detailed=False, output_json=False):
    """Show project status based on API reference design.
    
    Args:
        detailed: Show detailed status information
        output_json: Output in JSON format
    """
    nexus_dir = Path(".nexus")
    
    if not nexus_dir.exists():
        console.print("❌ Nexus not initialized. Run 'nexus init-project'", style="red")
        return
    
    # Load config
    config_file = nexus_dir / "config.json"
    if not config_file.exists():
        console.print("❌ Configuration file not found", style="red")
        return
    
    config = json.loads(config_file.read_text())
    
    if output_json:
        print(json.dumps(config, indent=2))
        return
    
    # Show status table
    table = Table(title="Nexus Project Status")
    table.add_column("Component", style="cyan", no_wrap=True)
    table.add_column("Status", style="green")
    table.add_column("Details", style="yellow")
    
    # Project info
    project_name = config.get("project", {}).get("name", "Unknown")
    project_type = config.get("project", {}).get("type", "unknown")
    table.add_row("Project", "✅ Initialized", f"{project_name} ({project_type})")
    
    # Nexus info
    nexus_version = config.get("nexus", {}).get("version", "Unknown")
    docs_dir = config.get("nexus", {}).get("docs_directory", "nexus_docs")
    table.add_row("Nexus Version", "✅ Current", nexus_version)
    table.add_row("Docs Directory", "✅ Ready", docs_dir)
    
    # Cursor integration
    cursor_integration = config.get("nexus", {}).get("cursor_integration", False)
    cursor_status = "✅ Enabled" if cursor_integration else "❌ Disabled"
    table.add_row("Cursor Integration", cursor_status, "Rules in .cursor/rules/")
    
    # Update status
    from nexus.core.updater import check_project_needs_update
    if check_project_needs_update():
        table.add_row("Updates", "⚠️ Available", "Run 'nexus update-project'")
    else:
        table.add_row("Updates", "✅ Current", "Project files up to date")
    
    # Documentation status
    docs_path = Path(docs_dir)
    if docs_path.exists():
        doc_types = ["prd", "arch", "impl", "int", "exec", "rules", "task", "tests"]
        for doc_type in doc_types:
            doc_dir = docs_path / doc_type
            if doc_dir.exists():
                # Count markdown files (excluding index.md)
                md_files = list(doc_dir.glob("*.md"))
                count = len([f for f in md_files if f.name != "index.md"])
                status_icon = "📄" if count > 0 else "📁"
                table.add_row(f"{doc_type.upper()} Docs", f"{status_icon} Ready", f"{count} documents")
    else:
        table.add_row("Documentation", "❌ Missing", "Run 'nexus init-project'")
    
    console.print(table)
    
    if detailed:
        _show_detailed_status(config, docs_path)

def _show_detailed_status(config, docs_path):
    """Show detailed status information."""
    console.print("\n" + "="*50)
    console.print("Detailed Status Information", style="bold blue")
    console.print("="*50)
    
    # Configuration details
    config_panel = Panel(
        json.dumps(config, indent=2),
        title="Configuration",
        border_style="blue"
    )
    console.print(config_panel)
    
    # File system status
    if docs_path.exists():
        console.print("\n📁 Documentation Structure:", style="bold")
        _show_directory_tree(docs_path, max_depth=2)
    
    # Cursor rules status
    cursor_rules = Path(".cursor/rules")
    if cursor_rules.exists():
        rule_files = list(cursor_rules.glob("*.md"))
        console.print(f"\n🎯 Cursor Rules ({len(rule_files)} files):", style="bold")
        for rule_file in rule_files:
            console.print(f"  • {rule_file.name}")
    
    # Instructions status
    instructions = Path(".nexus/instructions")
    if instructions.exists():
        instruction_files = list(instructions.glob("*.md"))
        console.print(f"\n📝 Instructions ({len(instruction_files)} files):", style="bold")
        for instruction_file in instruction_files:
            console.print(f"  • {instruction_file.name}")

def _show_directory_tree(path, prefix="", max_depth=3, current_depth=0):
    """Show directory tree structure."""
    if current_depth >= max_depth:
        return
    
    try:
        items = sorted(path.iterdir())
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            console.print(f"{prefix}{current_prefix}{item.name}")
            
            if item.is_dir() and current_depth < max_depth - 1:
                next_prefix = prefix + ("    " if is_last else "│   ")
                _show_directory_tree(item, next_prefix, max_depth, current_depth + 1)
    except PermissionError:
        console.print(f"{prefix}└── [Permission Denied]")
