"""Commands module for listing available commands."""

from rich.console import Console
from rich.table import Table

console = Console()

def list_available_commands(category=None, output_json=False):
    """List all available commands based on API reference.
    
    Args:
        category: Filter by command category
        output_json: Output in JSON format
    """
    commands = {
        "project": [
            {"name": "init-project", "description": "Initialize Nexus in current project"},
            {"name": "status", "description": "Show current project status and configuration"},
            {"name": "validate", "description": "Validate project configuration and structure"},
        ],
        "documentation": [
            {"name": "generate-docs", "description": "Generate project documentation"},
            {"name": "serve-docs", "description": "Start a local documentation server"},
        ],
        "instructions": [
            {"name": "create-instruction", "description": "Create a new instruction template"},
            {"name": "execute-instruction", "description": "Execute an instruction or workflow"},
        ],
        "content": [
            {"name": "analyze-content", "description": "Analyze existing documentation content for patterns"},
            {"name": "migrate-content", "description": "Migrate existing generated-docs content to new structure"},
            {"name": "enhance-content", "description": "Enhance documentation content quality"},
        ],
        "testing": [
            {"name": "test-integration", "description": "Run comprehensive integration tests"},
            {"name": "test-performance", "description": "Run performance tests"},
            {"name": "test-all", "description": "Run all tests (integration and performance)"},
        ],
        "system": [
            {"name": "list-commands", "description": "List all available commands"},
        ]
    }
    
    # Filter by category if specified
    if category:
        if category in commands:
            commands = {category: commands[category]}
        else:
            console.print(f"❌ Unknown category: {category}", style="red")
            return commands
    
    if output_json:
        import json
        print(json.dumps(commands, indent=2))
        return commands
    
    # Display commands table
    table = Table(title="Available Nexus Commands")
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Category", style="blue")
    table.add_column("Description", style="white")
    
    for cat, cmd_list in commands.items():
        for cmd in cmd_list:
            table.add_row(cmd["name"], cat, cmd["description"])
    
    console.print(table)
    
    if not category:
        console.print("\n💡 Use 'nexus list-commands --category <category>' to filter by category", style="dim")
    
    return commands
