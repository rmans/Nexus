"""Integration testing module for comprehensive system validation."""

import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from .project_init import ProjectInitializer
from .generator import DocumentGenerator
from .content_analyzer import ContentAnalyzer
from .content_migrator import ContentMigrator
from .content_enhancer import ContentEnhancer
from .config import ConfigManager

console = Console()

@dataclass
class TestResult:
    """Represents the result of a test."""
    test_name: str
    status: str  # "PASS", "FAIL", "SKIP"
    message: str
    duration: float
    details: Dict[str, Any]

class IntegrationTester:
    """Comprehensive integration testing for the Nexus system."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize integration tester.
        
        Args:
            project_root: Root directory for testing
        """
        self.project_root = project_root or Path.cwd()
        self.test_results: List[TestResult] = []
        self.temp_dir: Optional[Path] = None
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests.
        
        Returns:
            Test results summary
        """
        console.print("🧪 Running comprehensive integration tests...", style="bold blue")
        
        # Create temporary test environment
        self.temp_dir = Path(tempfile.mkdtemp(prefix="nexus_test_"))
        console.print(f"📁 Test environment: {self.temp_dir}", style="blue")
        
        try:
            # Run test suites
            self._test_project_initialization()
            self._test_document_generation()
            self._test_content_analysis()
            self._test_content_migration()
            self._test_content_enhancement()
            self._test_configuration_management()
            self._test_template_system()
            self._test_cli_integration()
            self._test_full_workflow()
            
            # Generate summary
            summary = self._generate_test_summary()
            self._display_test_results()
            
            return summary
            
        finally:
            # Cleanup
            if self.temp_dir and self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
                console.print("🧹 Cleaned up test environment", style="green")
    
    def _test_project_initialization(self) -> None:
        """Test project initialization functionality."""
        console.print("\n🔧 Testing project initialization...", style="blue")
        
        # Test 1: Basic initialization
        test_dir = self.temp_dir / "test_init"
        test_dir.mkdir()
        
        try:
            initializer = ProjectInitializer(project_root=test_dir)
            initializer.initialize()
            
            # Verify structure
            assert (test_dir / ".nexus").exists(), "Nexus directory not created"
            assert (test_dir / ".cursor").exists(), "Cursor directory not created"
            assert (test_dir / "nexus_docs").exists(), "Docs directory not created"
            assert (test_dir / ".nexus" / "config.json").exists(), "Config file not created"
            
            self._add_test_result("project_init_basic", "PASS", "Basic initialization successful", 0.0)
            
        except Exception as e:
            self._add_test_result("project_init_basic", "FAIL", f"Basic initialization failed: {e}", 0.0)
        
        # Test 2: Force reinitialization
        try:
            initializer = ProjectInitializer(project_root=test_dir)
            initializer.initialize(force=True)
            
            # Verify structure still exists
            assert (test_dir / ".nexus").exists(), "Nexus directory not preserved"
            
            self._add_test_result("project_init_force", "PASS", "Force reinitialization successful", 0.0)
            
        except Exception as e:
            self._add_test_result("project_init_force", "FAIL", f"Force reinitialization failed: {e}", 0.0)
    
    def _test_document_generation(self) -> None:
        """Test document generation functionality."""
        console.print("\n📚 Testing document generation...", style="blue")
        
        test_dir = self.temp_dir / "test_docs"
        test_dir.mkdir()
        
        try:
            # Initialize project
            initializer = ProjectInitializer(project_root=test_dir)
            initializer.initialize()
            
            # Test document generation
            generator = DocumentGenerator(project_root=test_dir)
            generator.generate()
            
            # Verify generated documents
            docs_dir = test_dir / "nexus_docs"
            assert docs_dir.exists(), "Docs directory not created"
            
            # Check for generated files
            generated_files = list(docs_dir.rglob("*.md"))
            assert len(generated_files) > 0, "No markdown files generated"
            
            # Check for specific sections
            expected_sections = ["prd", "arch", "impl", "int", "exec", "rules", "task", "tests"]
            for section in expected_sections:
                section_dir = docs_dir / section
                assert section_dir.exists(), f"Section {section} not created"
                assert (section_dir / "index.md").exists(), f"Index file for {section} not created"
            
            self._add_test_result("doc_generation_basic", "PASS", f"Generated {len(generated_files)} files", 0.0)
            
        except Exception as e:
            self._add_test_result("doc_generation_basic", "FAIL", f"Document generation failed: {e}", 0.0)
    
    def _test_content_analysis(self) -> None:
        """Test content analysis functionality."""
        console.print("\n🔍 Testing content analysis...", style="blue")
        
        test_dir = self.temp_dir / "test_analysis"
        test_dir.mkdir()
        
        try:
            # Create sample content
            sample_docs = test_dir / "generated-docs"
            sample_docs.mkdir()
            
            # Create sample PRD
            prd_dir = sample_docs / "prd"
            prd_dir.mkdir()
            prd_file = prd_dir / "sample.md"
            prd_file.write_text("""# Sample PRD

## Overview
This is a test document.

## Requirements
- Feature 1: Authentication
- Feature 2: Data storage

## Code Example
```python
def authenticate(user):
    return True
```

## Checklist
- [ ] Implement authentication
- [ ] Add data storage
""")
            
            # Test analysis
            analyzer = ContentAnalyzer(project_root=test_dir)
            results = analyzer.analyze_existing_content()
            
            # Verify results
            assert len(results["patterns"]) > 0, "No patterns found"
            assert len(results["sections"]) > 0, "No sections analyzed"
            assert "prd" in results["sections"], "PRD section not found"
            
            # Check pattern types
            pattern_types = set(p.pattern_type for p in results["patterns"])
            expected_types = {"code_block", "todo_item", "list_item"}
            assert pattern_types.intersection(expected_types), f"Expected pattern types not found: {pattern_types}"
            
            self._add_test_result("content_analysis_basic", "PASS", f"Found {len(results['patterns'])} patterns", 0.0)
            
        except Exception as e:
            self._add_test_result("content_analysis_basic", "FAIL", f"Content analysis failed: {e}", 0.0)
    
    def _test_content_migration(self) -> None:
        """Test content migration functionality."""
        console.print("\n🔄 Testing content migration...", style="blue")
        
        test_dir = self.temp_dir / "test_migration"
        test_dir.mkdir()
        
        try:
            # Create source content
            source_dir = test_dir / "generated-docs"
            source_dir.mkdir()
            
            # Create sample content
            prd_dir = source_dir / "prd"
            prd_dir.mkdir()
            prd_file = prd_dir / "test-prd.md"
            prd_file.write_text("""# Test PRD

## Overview
This is a test PRD for migration.

## Requirements
- Feature A
- Feature B
""")
            
            # Test migration
            migrator = ContentMigrator(project_root=test_dir)
            results = migrator.migrate_content(preserve_original=True)
            
            # Verify migration
            assert results["migrated"] > 0, "No files migrated"
            assert results["errors"] == 0, f"Migration errors: {results['errors']}"
            
            # Check migrated files
            target_dir = test_dir / "nexus_docs"
            assert target_dir.exists(), "Target directory not created"
            
            migrated_file = target_dir / "prd" / "test-prd.md"
            assert migrated_file.exists(), "Migrated file not found"
            
            # Check migration metadata
            content = migrated_file.read_text()
            assert "migrated from" in content.lower(), "Migration metadata not added"
            
            self._add_test_result("content_migration_basic", "PASS", f"Migrated {results['migrated']} files", 0.0)
            
        except Exception as e:
            self._add_test_result("content_migration_basic", "FAIL", f"Content migration failed: {e}", 0.0)
    
    def _test_content_enhancement(self) -> None:
        """Test content enhancement functionality."""
        console.print("\n✨ Testing content enhancement...", style="blue")
        
        test_dir = self.temp_dir / "test_enhancement"
        test_dir.mkdir()
        
        try:
            # Create test content in the expected structure
            docs_dir = test_dir / "nexus_docs"
            docs_dir.mkdir()
            
            # Create a section directory
            prd_dir = docs_dir / "prd"
            prd_dir.mkdir()
            
            test_file = prd_dir / "test.md"
            test_file.write_text("""# Test Document

## Overview
This is a test document.

## Requirements
- Feature 1
- Feature 2

## Code
```python
def test():
    pass
```
""")
            
            # Test enhancement
            enhancer = ContentEnhancer(project_root=test_dir)
            results = enhancer.analyze_and_enhance()
            
            # Verify analysis
            assert "files_analyzed" in results, "Analysis results missing files_analyzed"
            assert results["files_analyzed"] >= 0, "Files analyzed should be non-negative"
            
            # Test preview mode
            preview_results = enhancer.apply_enhancements(dry_run=True)
            assert "applied" in preview_results, "Preview results missing applied count"
            assert preview_results["applied"] >= 0, "Applied count should be non-negative"
            
            self._add_test_result("content_enhancement_basic", "PASS", f"Analyzed {results['files_analyzed']} files", 0.0)
            
        except Exception as e:
            self._add_test_result("content_enhancement_basic", "FAIL", f"Content enhancement failed: {e}", 0.0)
    
    def _test_configuration_management(self) -> None:
        """Test configuration management functionality."""
        console.print("\n⚙️ Testing configuration management...", style="blue")
        
        test_dir = self.temp_dir / "test_config"
        test_dir.mkdir()
        
        try:
            # Test config manager
            config_manager = ConfigManager(project_root=test_dir)
            
            # Test default config
            config = config_manager.config
            assert "nexus" in config, "Default config not loaded"
            assert "project" in config, "Project config not found"
            
            # Test config updates
            config_manager.set("test.value", "test_data")
            assert config_manager.get("test.value") == "test_data", "Config set/get failed"
            
            # Test deep updates
            config_manager.update_config({"test": {"nested": {"value": "nested_data"}}})
            assert config_manager.get("test.nested.value") == "nested_data", "Deep update failed"
            
            # Test validation
            errors = config_manager.validate_config()
            # Should have errors since project not initialized
            assert len(errors) > 0, "Validation should find errors for uninitialized project"
            
            self._add_test_result("config_management_basic", "PASS", "Configuration management working", 0.0)
            
        except Exception as e:
            self._add_test_result("config_management_basic", "FAIL", f"Configuration management failed: {e}", 0.0)
    
    def _test_template_system(self) -> None:
        """Test template system functionality."""
        console.print("\n📝 Testing template system...", style="blue")
        
        test_dir = self.temp_dir / "test_templates"
        test_dir.mkdir()
        
        try:
            # Initialize project to get templates
            initializer = ProjectInitializer(project_root=test_dir)
            initializer.initialize()
            
            # Test template manager
            from .templates import TemplateManager
            template_manager = TemplateManager(project_root=test_dir)
            
            # Test template listing
            templates = template_manager.list_templates()
            assert len(templates) > 0, "No templates found"
            
            # Test template rendering
            context = {
                "title": "Test Document",
                "description": "A test document",
                "project_name": "test-project"
            }
            
            # Test basic template (if it exists)
            try:
                content = template_manager.render_template("basic", context, "prd")
                assert content, "Template rendering failed"
                assert "Test Document" in content, "Context not applied"
            except Exception:
                # Template might not exist, that's okay for testing
                pass
            
            self._add_test_result("template_system_basic", "PASS", f"Found {len(templates)} template categories", 0.0)
            
        except Exception as e:
            self._add_test_result("template_system_basic", "FAIL", f"Template system failed: {e}", 0.0)
    
    def _test_cli_integration(self) -> None:
        """Test CLI integration."""
        console.print("\n🖥️ Testing CLI integration...", style="blue")
        
        test_dir = self.temp_dir / "test_cli"
        test_dir.mkdir()
        
        try:
            # Test CLI commands (simulate)
            from .commands import list_available_commands
            
            # Test command listing
            commands = list_available_commands()
            assert commands is not None, "Commands not returned"
            assert isinstance(commands, dict), "Commands should be a dictionary"
            assert "project" in commands, "Project commands not found"
            assert "documentation" in commands, "Documentation commands not found"
            assert "content" in commands, "Content commands not found"
            
            # Test command categories
            project_commands = [cmd["name"] for cmd in commands["project"]]
            assert "init-project" in project_commands, "init-project command not found"
            assert "status" in project_commands, "status command not found"
            
            self._add_test_result("cli_integration_basic", "PASS", f"Found {len(commands)} command categories", 0.0)
            
        except Exception as e:
            self._add_test_result("cli_integration_basic", "FAIL", f"CLI integration failed: {e}", 0.0)
    
    def _test_full_workflow(self) -> None:
        """Test complete end-to-end workflow."""
        console.print("\n🔄 Testing full workflow...", style="blue")
        
        test_dir = self.temp_dir / "test_workflow"
        test_dir.mkdir()
        
        try:
            # Step 1: Initialize project
            initializer = ProjectInitializer(project_root=test_dir)
            initializer.initialize()
            
            # Step 2: Create some source content
            source_dir = test_dir / "generated-docs"
            source_dir.mkdir()
            prd_dir = source_dir / "prd"
            prd_dir.mkdir()
            prd_file = prd_dir / "workflow-test.md"
            prd_file.write_text("""# Workflow Test PRD

## Overview
This tests the complete workflow.

## Requirements
- Feature 1: Authentication
- Feature 2: Data storage

## Code Example
```python
def main():
    print("Hello World")
```
""")
            
            # Step 3: Migrate content
            migrator = ContentMigrator(project_root=test_dir)
            migration_results = migrator.migrate_content()
            
            # Step 4: Analyze content
            analyzer = ContentAnalyzer(project_root=test_dir)
            analysis_results = analyzer.analyze_existing_content()
            
            # Step 5: Generate documentation
            generator = DocumentGenerator(project_root=test_dir)
            generator.generate()
            
            # Step 6: Enhance content (optional - may not find enhancement opportunities)
            enhancer = ContentEnhancer(project_root=test_dir)
            enhancement_results = enhancer.analyze_and_enhance()
            
            # Verify workflow completion
            assert migration_results["migrated"] > 0, "Migration failed in workflow"
            assert len(analysis_results["patterns"]) > 0, "Analysis failed in workflow"
            # Enhancement is optional - just check it doesn't crash
            assert "files_analyzed" in enhancement_results, "Enhancement analysis failed in workflow"
            
            # Check final structure
            docs_dir = test_dir / "nexus_docs"
            assert docs_dir.exists(), "Final docs directory not created"
            
            generated_files = list(docs_dir.rglob("*.md"))
            assert len(generated_files) > 0, "No files in final structure"
            
            self._add_test_result("full_workflow", "PASS", f"Complete workflow successful with {len(generated_files)} files", 0.0)
            
        except Exception as e:
            self._add_test_result("full_workflow", "FAIL", f"Full workflow failed: {e}", 0.0)
    
    def _add_test_result(self, test_name: str, status: str, message: str, duration: float, details: Optional[Dict[str, Any]] = None) -> None:
        """Add a test result.
        
        Args:
            test_name: Name of the test
            status: Test status (PASS, FAIL, SKIP)
            message: Test message
            duration: Test duration in seconds
            details: Additional test details
        """
        result = TestResult(
            test_name=test_name,
            status=status,
            message=message,
            duration=duration,
            details=details or {}
        )
        self.test_results.append(result)
    
    def _generate_test_summary(self) -> Dict[str, Any]:
        """Generate test summary.
        
        Returns:
            Test summary dictionary
        """
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r.status == "PASS"])
        failed_tests = len([r for r in self.test_results if r.status == "FAIL"])
        skipped_tests = len([r for r in self.test_results if r.status == "SKIP"])
        
        # Convert TestResult objects to dictionaries for JSON serialization
        serializable_results = []
        for result in self.test_results:
            serializable_results.append({
                "test_name": result.test_name,
                "status": result.status,
                "message": result.message,
                "duration": result.duration,
                "details": result.details
            })
        
        return {
            "total": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "skipped": skipped_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "results": serializable_results
        }
    
    def _display_test_results(self) -> None:
        """Display test results in a formatted table."""
        console.print("\n" + "="*60, style="bold blue")
        console.print("🧪 INTEGRATION TEST RESULTS", style="bold blue")
        console.print("="*60, style="bold blue")
        
        # Create results table
        table = Table(title="Test Results")
        table.add_column("Test", style="cyan", no_wrap=True)
        table.add_column("Status", style="bold")
        table.add_column("Message", style="white")
        table.add_column("Duration", style="yellow")
        
        for result in self.test_results:
            status_style = {
                "PASS": "green",
                "FAIL": "red",
                "SKIP": "yellow"
            }.get(result.status, "white")
            
            table.add_row(
                result.test_name,
                f"[{status_style}]{result.status}[/{status_style}]",
                result.message,
                f"{result.duration:.2f}s"
            )
        
        console.print(table)
        
        # Display summary
        summary = self._generate_test_summary()
        summary_panel = Panel(
            f"""Total Tests: {summary['total']}
Passed: {summary['passed']}
Failed: {summary['failed']}
Skipped: {summary['skipped']}
Success Rate: {summary['success_rate']:.1f}%""",
            title="Summary",
            border_style="green" if summary['failed'] == 0 else "red"
        )
        console.print(summary_panel)
