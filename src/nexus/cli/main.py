"""Nexus CLI main module implementing the API reference design."""

import click
from pathlib import Path
from rich.console import Console
from ..core.version import get_version_string

console = Console()

@click.group()
@click.version_option(version=get_version_string())
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


@main.command("update-project")
@click.option('--force', is_flag=True, help='Force update without confirmation')
@click.option('--check-only', is_flag=True, help='Only check if update is needed')
@click.pass_context
def update_project(ctx, force, check_only):
    """Update project files to latest Nexus version.
    
    Updates Cursor rules, instruction files, and documentation scaffolds
    to the latest version without affecting your generated content.
    """
    from nexus.core.updater import ProjectUpdater
    
    updater = ProjectUpdater()
    
    if check_only:
        needs_update = updater.check_needs_update()
        if needs_update:
            console.print("🔄 Project files need updating", style="yellow")
            console.print("Run 'nexus update-project' to update", style="blue")
        else:
            console.print("✅ Project files are up to date", style="green")
        return
    
    updater.update_project_files(force=force)


@main.command("discover")
@click.argument('path', default='.')
@click.option('--output', type=click.Choice(['json', 'summary']), default='summary')
@click.option('--cache', is_flag=True, help='Use cached results if available')
@click.option('--deep', is_flag=True, help='Enable deeper analysis')
@click.option('--languages', help='Comma-separated list of languages')
@click.option('--clear-cache', is_flag=True, help='Clear discovery cache')
@click.option('--save', help='Save discovery report with given title')
@click.pass_context
def discover(ctx, path, output, cache, deep, languages, clear_cache, save):
    """Discover and analyze code structure, dependencies, and patterns.
    
    Automatically analyzes codebases to understand structure, dependencies, 
    patterns, and quality. Provides structured data for other Nexus systems.
    """
    from nexus.core.discovery.engine import DiscoveryEngine
    from nexus.core.discovery.cache import DiscoveryCache
    from nexus.core.discovery.reports import DiscoveryReportManager
    
    if clear_cache:
        config_manager = ctx.obj.get('config_manager')
        cache = DiscoveryCache(Path(config_manager.get_cache_directory()) / "discovery")
        target_path = Path(path).resolve() if path != '.' else None
        cache.clear(target_path)
        console.print("🗑️ Discovery cache cleared", style="green")
        return
    
    config_manager = ctx.obj.get('config_manager')
    engine = DiscoveryEngine(config_manager)
    
    options = {'cache': cache, 'deep': deep}
    if languages:
        options['languages'] = [lang.strip() for lang in languages.split(',')]
    
    target_path = Path(path).resolve()
    results = engine.discover(target_path, options)
    
    # Save report if requested
    if save:
        report_manager = DiscoveryReportManager(config_manager)
        report_path = report_manager.save_report(results, save, target_path)
        console.print(f"📄 Discovery report saved: {report_path}", style="green")
    
    if output == 'json':
        console.print(engine.outputs.format_json(results, pretty=True))
    else:
        console.print(engine.outputs.format_summary(results))


@main.command("discovery")
@click.argument('action', type=click.Choice(['list', 'view']))
@click.argument('report_id', required=False)
@click.pass_context
def discovery(ctx, action, report_id):
    """Manage discovery reports.
    
    List or view saved discovery reports.
    """
    from nexus.core.discovery.reports import DiscoveryReportManager
    
    config_manager = ctx.obj.get('config_manager')
    report_manager = DiscoveryReportManager(config_manager)
    
    if action == 'list':
        reports = report_manager.list_reports()
        
        if not reports:
            console.print("📄 No discovery reports found", style="yellow")
            return
        
        console.print("📄 Discovery Reports", style="bold blue")
        console.print("=" * 50)
        
        for report in reports:
            title = report.get('title', report['filename'])
            date = report.get('date', 'Unknown')
            console.print(f"• {title} ({date})")
            console.print(f"  File: {report['filename']}")
            console.print()
    
    elif action == 'view':
        if not report_id:
            console.print("❌ Report ID required for view action", style="red")
            console.print("Usage: nexus discovery view <report-id>")
            return
        
        report = report_manager.get_report(report_id)
        if not report:
            console.print(f"❌ Report not found: {report_id}", style="red")
            return
        
        console.print(f"📄 Viewing: {report['metadata'].get('title', report_id)}")
        console.print("=" * 50)
        console.print(report['content'])


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
@click.option('--include', help='Include specific documentation sections (comma-separated)')
@click.option('--auto-reload', is_flag=True, help='Auto-reload on changes')
@click.pass_context
def generate_docs(ctx, output, format, include, auto_reload):
    """Generate project documentation.
    
    Creates comprehensive documentation from your project structure,
    code, and configuration files.
    """
    from nexus.core.generator import DocumentGenerator
    
    console.print("📚 Generating documentation...", style="blue")
    
    # Parse include parameter
    include_list = None
    if include:
        include_list = [s.strip() for s in include.split(',')]
    
    generator = DocumentGenerator()
    generator.generate(
        output_dir=Path(output) if output else None, 
        format=format, 
        include=include_list, 
        auto_reload=auto_reload
    )


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


@main.command("analyze-content")
@click.option('--output', help='Output file for analysis results')
@click.option('--export-templates', is_flag=True, help='Export templates from analysis')
@click.pass_context
def analyze_content(ctx, output, export_templates):
    """Analyze existing documentation content for patterns and insights.
    
    Examines your documentation to find common patterns, suggest templates,
    and provide insights for improvement.
    """
    from nexus.core.content_analyzer import ContentAnalyzer
    
    console.print("🔍 Analyzing documentation content...", style="blue")
    
    analyzer = ContentAnalyzer()
    results = analyzer.analyze_existing_content()
    
    # Display summary
    console.print(f"📊 Found {len(results['patterns'])} patterns across {len(results['sections'])} sections", style="green")
    
    if results['insights']['template_suggestions']:
        console.print("\n💡 Template Suggestions:", style="blue")
        for suggestion in results['insights']['template_suggestions']:
            console.print(f"  • {suggestion['description']} ({suggestion['count']} instances)", style="cyan")
    
    # Export results if requested
    if output:
        output_path = Path(output)
        analyzer.export_analysis(output_path)
    
    # Export templates if requested
    if export_templates:
        templates_dir = Path("nexus_docs/templates")
        analyzer.create_templates_from_patterns(templates_dir)


@main.command("migrate-content")
@click.option('--preserve-original', is_flag=True, help='Keep original files after migration')
@click.option('--report', help='Generate migration report file')
@click.pass_context
def migrate_content(ctx, preserve_original, report):
    """Migrate existing generated-docs content to new structure.
    
    Moves and enhances content from generated-docs/ to nexus_docs/
    with improved structure and metadata.
    """
    from nexus.core.content_migrator import ContentMigrator
    
    console.print("🔄 Migrating content to new structure...", style="blue")
    
    migrator = ContentMigrator()
    results = migrator.migrate_content(preserve_original=preserve_original)
    
    console.print(f"✅ Migrated {results['migrated']} files", style="green")
    if results['errors'] > 0:
        console.print(f"⚠️  {results['errors']} errors occurred", style="yellow")
    
    # Generate report if requested
    if report:
        report_path = Path(report)
        migrator.create_migration_report(report_path)


@main.command("enhance-content")
@click.option('--preview', is_flag=True, help='Preview enhancements without applying')
@click.option('--apply', is_flag=True, help='Apply enhancement suggestions')
@click.option('--report', help='Generate enhancement report file')
@click.option('--target-dir', help='Directory to enhance (defaults to nexus_docs)')
@click.pass_context
def enhance_content(ctx, preview, apply, report, target_dir):
    """Enhance documentation content quality.
    
    Analyzes content and suggests improvements for better readability,
    structure, and completeness.
    """
    from nexus.core.content_enhancer import ContentEnhancer
    
    if not preview and not apply:
        console.print("❌ Please specify --preview or --apply", style="red")
        return
    
    target_path = Path(target_dir) if target_dir else None
    
    console.print("🔧 Analyzing content for enhancements...", style="blue")
    
    enhancer = ContentEnhancer()
    results = enhancer.analyze_and_enhance(target_path)
    
    if not results['suggestions']:
        console.print("ℹ️  No enhancement suggestions found", style="blue")
        return
    
    # Show summary
    stats = enhancer.get_enhancement_stats()
    console.print(f"📊 Found {stats['total']} suggestions across {stats['files_affected']} files", style="green")
    
    # Preview or apply enhancements
    if preview:
        enhancer.apply_enhancements(dry_run=True)
    elif apply:
        enhancer.apply_enhancements(dry_run=False)
    
    # Generate report if requested
    if report:
        report_path = Path(report)
        enhancer.create_enhancement_report(report_path)


@main.command("test-integration")
@click.option('--output', help='Output file for test results')
@click.option('--verbose', is_flag=True, help='Show detailed test output')
@click.pass_context
def test_integration(ctx, output, verbose):
    """Run comprehensive integration tests.
    
    Tests all system components and their interactions to ensure
    everything works correctly together.
    """
    from nexus.core.integration_tester import IntegrationTester
    
    console.print("🧪 Running integration tests...", style="blue")
    
    tester = IntegrationTester()
    results = tester.run_all_tests()
    
    # Export results if requested
    if output:
        import json
        output_path = Path(output)
        output_path.write_text(json.dumps(results, indent=2))
        console.print(f"📊 Test results exported to {output_path}", style="green")
    
    # Exit with error code if tests failed
    if results["failed"] > 0:
        console.print(f"❌ {results['failed']} tests failed", style="red")
        exit(1)
    else:
        console.print(f"✅ All {results['passed']} tests passed", style="green")


@main.command("test-performance")
@click.option('--output', help='Output file for performance results')
@click.option('--large-files', is_flag=True, help='Test with large files')
@click.pass_context
def test_performance(ctx, output, large_files):
    """Run performance tests.
    
    Tests system performance under various conditions to ensure
    it can handle real-world workloads efficiently.
    """
    from nexus.core.performance_tester import PerformanceTester
    
    console.print("⚡ Running performance tests...", style="blue")
    
    tester = PerformanceTester()
    results = tester.run_performance_tests()
    
    # Export results if requested
    if output:
        import json
        output_path = Path(output)
        output_path.write_text(json.dumps(results, indent=2))
        console.print(f"📊 Performance results exported to {output_path}", style="green")
    
    # Check performance thresholds
    if results.get("max_duration", 0) > 30:  # 30 seconds threshold
        console.print("⚠️  Some operations took longer than expected", style="yellow")
    
    if results.get("max_memory", 0) > 500:  # 500MB threshold
        console.print("⚠️  High memory usage detected", style="yellow")


@main.command("test-all")
@click.option('--integration', is_flag=True, help='Run integration tests')
@click.option('--performance', is_flag=True, help='Run performance tests')
@click.option('--output', help='Output directory for test results')
@click.pass_context
def test_all(ctx, integration, performance, output):
    """Run all tests (integration and performance).
    
    Comprehensive testing suite that validates both functionality
    and performance of the entire system.
    """
    if not integration and not performance:
        integration = True
        performance = True
    
    output_dir = Path(output) if output else Path("test_results")
    output_dir.mkdir(exist_ok=True)
    
    console.print("🧪 Running comprehensive test suite...", style="bold blue")
    
    all_passed = True
    
    if integration:
        console.print("\n" + "="*50, style="blue")
        console.print("INTEGRATION TESTS", style="bold blue")
        console.print("="*50, style="blue")
        
        from nexus.core.integration_tester import IntegrationTester
        tester = IntegrationTester()
        results = tester.run_all_tests()
        
        # Save integration results
        integration_file = output_dir / "integration_results.json"
        import json
        integration_file.write_text(json.dumps(results, indent=2))
        
        if results["failed"] > 0:
            all_passed = False
    
    if performance:
        console.print("\n" + "="*50, style="blue")
        console.print("PERFORMANCE TESTS", style="bold blue")
        console.print("="*50, style="blue")
        
        from nexus.core.performance_tester import PerformanceTester
        tester = PerformanceTester()
        results = tester.run_performance_tests()
        
        # Save performance results
        performance_file = output_dir / "performance_results.json"
        import json
        performance_file.write_text(json.dumps(results, indent=2))
    
    # Final summary
    console.print("\n" + "="*50, style="bold blue")
    console.print("TEST SUITE SUMMARY", style="bold blue")
    console.print("="*50, style="bold blue")
    
    if all_passed:
        console.print("✅ All tests completed successfully", style="green")
        console.print(f"📊 Results saved to {output_dir}", style="blue")
    else:
        console.print("❌ Some tests failed", style="red")
        exit(1)


if __name__ == "__main__":
    main()
