"""Nexus CLI main module implementing the API reference design."""

import click
from rich.console import Console

console = Console()

@click.group()
@click.version_option(version="0.1.0")
@click.option('--debug', is_flag=True, help='Enable debug logging')
@click.option('--config', default='config.yaml', help='Path to configuration file')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
@click.pass_context
def main(ctx, debug, config, verbose):
    """Nexus - AI context orchestration system for Cursor and other coding assistants.
    
    A modular project framework designed for scalable development and comprehensive documentation.
    """
    # Store global options in context
    ctx.ensure_object(dict)
    ctx.obj['debug'] = debug
    ctx.obj['config'] = config
    ctx.obj['verbose'] = verbose
    
    if debug:
        console.print("🐛 Debug mode enabled", style="yellow")
    if verbose:
        console.print("📢 Verbose output enabled", style="blue")


@main.command("init-project")
@click.option('--docs-dir', default='nexus_docs', help='Documentation directory name')
@click.option('--force', is_flag=True, help='Overwrite existing configuration')
@click.option('--template', help='Use specific template for initialization')
@click.pass_context
def init_project(ctx, docs_dir, force, template):
    """Initialize Nexus in current project.
    
    This command sets up the Nexus system in your current directory, creating
    the necessary configuration files and directory structure.
    """
    from nexus.core.project_init import ProjectInitializer
    
    console.print("🚀 Initializing Nexus project...", style="blue")
    
    initializer = ProjectInitializer(docs_dir=docs_dir, template=template)
    initializer.initialize(force=force)


@main.command("status")
@click.option('--detailed', is_flag=True, help='Show detailed status information')
@click.option('--json', is_flag=True, help='Output in JSON format')
@click.pass_context
def status(ctx, detailed, json):
    """Show current project status and configuration.
    
    Displays information about the current Nexus project including
    configuration, documentation status, and system health.
    """
    from nexus.core.status import show_status
    
    show_status(detailed=detailed, output_json=json)


@main.command("list-commands")
@click.option('--category', help='Filter by command category')
@click.option('--json', is_flag=True, help='Output in JSON format')
@click.pass_context
def list_commands(ctx, category, json):
    """List all available commands.
    
    Shows all available Nexus commands, optionally filtered by category.
    """
    from nexus.core.commands import list_available_commands
    
    list_available_commands(category=category, output_json=json)


@main.command("create-instruction")
@click.argument('name')
@click.option('--template', help='Instruction template to use')
@click.option('--output', help='Output file path')
@click.option('--interactive', is_flag=True, help='Use interactive mode')
@click.pass_context
def create_instruction(ctx, name, template, output, interactive):
    """Create a new instruction template.
    
    Creates a new instruction file that can be used to guide AI assistants
    in specific tasks or workflows.
    """
    from nexus.core.instructions import create_instruction_template
    
    console.print(f"📝 Creating instruction: {name}", style="green")
    create_instruction_template(name, template=template, output=output, interactive=interactive)


@main.command("execute-instruction")
@click.argument('instruction')
@click.option('--dry-run', is_flag=True, help='Preview execution without running')
@click.option('--parallel', is_flag=True, help='Enable parallel execution')
@click.option('--timeout', type=int, help='Execution timeout in seconds')
@click.pass_context
def execute_instruction(ctx, instruction, dry_run, parallel, timeout):
    """Execute an instruction or workflow.
    
    Runs a specific instruction file, executing the defined workflow
    or task sequence.
    """
    from nexus.core.instructions import execute_instruction_file
    
    console.print(f"🚀 Executing: {instruction}", style="green")
    execute_instruction_file(instruction, dry_run=dry_run, parallel=parallel, timeout=timeout)


@main.command("generate-docs")
@click.option('--output', help='Output directory')
@click.option('--format', type=click.Choice(['html', 'pdf', 'markdown']), default='markdown', help='Documentation format')
@click.option('--include', help='Include specific documentation sections')
@click.option('--auto-reload', is_flag=True, help='Auto-reload on changes')
@click.pass_context
def generate_docs(ctx, output, format, include, auto_reload):
    """Generate project documentation.
    
    Creates comprehensive documentation from your project structure,
    code, and configuration files.
    """
    from nexus.core.generator import DocumentGenerator
    
    console.print("📚 Generating documentation...", style="blue")
    
    generator = DocumentGenerator()
    generator.generate(output_dir=output, format=format, include=include, auto_reload=auto_reload)


@main.command("serve-docs")
@click.option('--port', default=8000, help='Server port')
@click.option('--host', default='localhost', help='Server host')
@click.option('--auto-reload', is_flag=True, help='Auto-reload on changes')
@click.pass_context
def serve_docs(ctx, port, host, auto_reload):
    """Start a local documentation server.
    
    Launches a local web server to view and interact with your
    project documentation.
    """
    from nexus.core.server import start_docs_server
    
    console.print(f"🌐 Starting documentation server on {host}:{port}", style="blue")
    start_docs_server(host=host, port=port, auto_reload=auto_reload)


@main.command("validate")
@click.option('--fix', is_flag=True, help='Automatically fix issues where possible')
@click.option('--strict', is_flag=True, help='Use strict validation rules')
@click.pass_context
def validate(ctx, fix, strict):
    """Validate project configuration and structure.
    
    Checks your Nexus project for common issues and ensures
    everything is properly configured.
    """
    from nexus.core.validator import validate_project
    
    console.print("🔍 Validating project...", style="blue")
    validate_project(fix=fix, strict=strict)


if __name__ == "__main__":
    main()
