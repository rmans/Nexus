"""Performance testing module for system optimization."""

import time
import psutil
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from .project_init import ProjectInitializer
from .generator import DocumentGenerator
from .content_analyzer import ContentAnalyzer
from .content_migrator import ContentMigrator

console = Console()

@dataclass
class PerformanceMetric:
    """Represents a performance metric."""
    operation: str
    duration: float
    memory_usage: float
    cpu_usage: float
    file_count: int
    file_size: int

class PerformanceTester:
    """Performance testing for the Nexus system."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize performance tester.
        
        Args:
            project_root: Root directory for testing
        """
        self.project_root = project_root or Path.cwd()
        self.metrics: List[PerformanceMetric] = []
        self.process = psutil.Process(os.getpid())
    
    def run_performance_tests(self) -> Dict[str, Any]:
        """Run comprehensive performance tests.
        
        Returns:
            Performance test results
        """
        console.print("⚡ Running performance tests...", style="bold blue")
        
        # Test different scenarios
        self._test_initialization_performance()
        self._test_document_generation_performance()
        self._test_content_analysis_performance()
        self._test_content_migration_performance()
        self._test_large_file_handling()
        self._test_memory_usage()
        
        # Generate performance report
        report = self._generate_performance_report()
        self._display_performance_results()
        
        return report
    
    def _test_initialization_performance(self) -> None:
        """Test project initialization performance."""
        console.print("\n🔧 Testing initialization performance...", style="blue")
        
        test_dir = Path("/tmp/nexus_perf_init")
        test_dir.mkdir(exist_ok=True)
        
        try:
            # Measure initialization
            start_time = time.time()
            start_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            
            initializer = ProjectInitializer(project_root=test_dir)
            initializer.initialize()
            
            end_time = time.time()
            end_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            
            duration = end_time - start_time
            memory_usage = end_memory - start_memory
            
            # Count created files
            created_files = list(test_dir.rglob("*"))
            file_count = len([f for f in created_files if f.is_file()])
            file_size = sum(f.stat().st_size for f in created_files if f.is_file())
            
            metric = PerformanceMetric(
                operation="project_initialization",
                duration=duration,
                memory_usage=memory_usage,
                cpu_usage=0.0,  # Not measured for this test
                file_count=file_count,
                file_size=file_size
            )
            self.metrics.append(metric)
            
            console.print(f"✅ Initialization: {duration:.2f}s, {memory_usage:.1f}MB, {file_count} files", style="green")
            
        finally:
            # Cleanup
            import shutil
            if test_dir.exists():
                shutil.rmtree(test_dir)
    
    def _test_document_generation_performance(self) -> None:
        """Test document generation performance."""
        console.print("\n📚 Testing document generation performance...", style="blue")
        
        test_dir = Path("/tmp/nexus_perf_docs")
        test_dir.mkdir(exist_ok=True)
        
        try:
            # Initialize project
            initializer = ProjectInitializer(project_root=test_dir)
            initializer.initialize()
            
            # Measure generation
            start_time = time.time()
            start_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            
            generator = DocumentGenerator(project_root=test_dir)
            generator.generate()
            
            end_time = time.time()
            end_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            
            duration = end_time - start_time
            memory_usage = end_memory - start_memory
            
            # Count generated files
            docs_dir = test_dir / "nexus_docs"
            generated_files = list(docs_dir.rglob("*.md"))
            file_count = len(generated_files)
            file_size = sum(f.stat().st_size for f in generated_files)
            
            metric = PerformanceMetric(
                operation="document_generation",
                duration=duration,
                memory_usage=memory_usage,
                cpu_usage=0.0,
                file_count=file_count,
                file_size=file_size
            )
            self.metrics.append(metric)
            
            console.print(f"✅ Generation: {duration:.2f}s, {memory_usage:.1f}MB, {file_count} files", style="green")
            
        finally:
            # Cleanup
            import shutil
            if test_dir.exists():
                shutil.rmtree(test_dir)
    
    def _test_content_analysis_performance(self) -> None:
        """Test content analysis performance."""
        console.print("\n🔍 Testing content analysis performance...", style="blue")
        
        test_dir = Path("/tmp/nexus_perf_analysis")
        test_dir.mkdir(exist_ok=True)
        
        try:
            # Create test content
            self._create_test_content(test_dir, file_count=10)
            
            # Measure analysis
            start_time = time.time()
            start_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            
            analyzer = ContentAnalyzer(project_root=test_dir)
            results = analyzer.analyze_existing_content()
            
            end_time = time.time()
            end_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            
            duration = end_time - start_time
            memory_usage = end_memory - start_memory
            
            # Count analyzed content
            analyzed_files = list(test_dir.rglob("*.md"))
            file_count = len(analyzed_files)
            file_size = sum(f.stat().st_size for f in analyzed_files)
            
            metric = PerformanceMetric(
                operation="content_analysis",
                duration=duration,
                memory_usage=memory_usage,
                cpu_usage=0.0,
                file_count=file_count,
                file_size=file_size
            )
            self.metrics.append(metric)
            
            console.print(f"✅ Analysis: {duration:.2f}s, {memory_usage:.1f}MB, {len(results['patterns'])} patterns", style="green")
            
        finally:
            # Cleanup
            import shutil
            if test_dir.exists():
                shutil.rmtree(test_dir)
    
    def _test_content_migration_performance(self) -> None:
        """Test content migration performance."""
        console.print("\n🔄 Testing content migration performance...", style="blue")
        
        test_dir = Path("/tmp/nexus_perf_migration")
        test_dir.mkdir(exist_ok=True)
        
        try:
            # Create source content
            self._create_test_content(test_dir, file_count=5)
            
            # Measure migration
            start_time = time.time()
            start_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            
            migrator = ContentMigrator(project_root=test_dir)
            results = migrator.migrate_content()
            
            end_time = time.time()
            end_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            
            duration = end_time - start_time
            memory_usage = end_memory - start_memory
            
            # Count migrated files
            migrated_files = list((test_dir / "nexus_docs").rglob("*.md"))
            file_count = len(migrated_files)
            file_size = sum(f.stat().st_size for f in migrated_files)
            
            metric = PerformanceMetric(
                operation="content_migration",
                duration=duration,
                memory_usage=memory_usage,
                cpu_usage=0.0,
                file_count=file_count,
                file_size=file_size
            )
            self.metrics.append(metric)
            
            console.print(f"✅ Migration: {duration:.2f}s, {memory_usage:.1f}MB, {results['migrated']} files", style="green")
            
        finally:
            # Cleanup
            import shutil
            if test_dir.exists():
                shutil.rmtree(test_dir)
    
    def _test_large_file_handling(self) -> None:
        """Test handling of large files."""
        console.print("\n📁 Testing large file handling...", style="blue")
        
        test_dir = Path("/tmp/nexus_perf_large")
        test_dir.mkdir(exist_ok=True)
        
        try:
            # Create large test file
            large_file = test_dir / "large_document.md"
            large_content = self._generate_large_content(size_mb=5)  # 5MB
            large_file.write_text(large_content)
            
            # Measure analysis of large file
            start_time = time.time()
            start_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            
            analyzer = ContentAnalyzer(project_root=test_dir)
            results = analyzer.analyze_existing_content()
            
            end_time = time.time()
            end_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            
            duration = end_time - start_time
            memory_usage = end_memory - start_memory
            
            metric = PerformanceMetric(
                operation="large_file_analysis",
                duration=duration,
                memory_usage=memory_usage,
                cpu_usage=0.0,
                file_count=1,
                file_size=large_file.stat().st_size
            )
            self.metrics.append(metric)
            
            console.print(f"✅ Large file: {duration:.2f}s, {memory_usage:.1f}MB, {len(results['patterns'])} patterns", style="green")
            
        finally:
            # Cleanup
            import shutil
            if test_dir.exists():
                shutil.rmtree(test_dir)
    
    def _test_memory_usage(self) -> None:
        """Test memory usage patterns."""
        console.print("\n💾 Testing memory usage...", style="blue")
        
        test_dir = Path("/tmp/nexus_perf_memory")
        test_dir.mkdir(exist_ok=True)
        
        try:
            # Create multiple operations to test memory usage
            operations = [
                ("init", lambda: ProjectInitializer(project_root=test_dir).initialize()),
                ("generate", lambda: DocumentGenerator(project_root=test_dir).generate()),
                ("analyze", lambda: ContentAnalyzer(project_root=test_dir).analyze_existing_content()),
            ]
            
            memory_usage = []
            
            for op_name, operation in operations:
                # Measure memory before
                before_memory = self.process.memory_info().rss / 1024 / 1024  # MB
                
                # Run operation
                operation()
                
                # Measure memory after
                after_memory = self.process.memory_info().rss / 1024 / 1024  # MB
                
                memory_usage.append({
                    "operation": op_name,
                    "before": before_memory,
                    "after": after_memory,
                    "delta": after_memory - before_memory
                })
            
            # Calculate peak memory usage
            peak_memory = max(usage["after"] for usage in memory_usage)
            total_delta = sum(usage["delta"] for usage in memory_usage)
            
            metric = PerformanceMetric(
                operation="memory_usage",
                duration=0.0,
                memory_usage=peak_memory,
                cpu_usage=0.0,
                file_count=0,
                file_size=0
            )
            self.metrics.append(metric)
            
            console.print(f"✅ Memory: Peak {peak_memory:.1f}MB, Total delta {total_delta:.1f}MB", style="green")
            
        finally:
            # Cleanup
            import shutil
            if test_dir.exists():
                shutil.rmtree(test_dir)
    
    def _create_test_content(self, base_dir: Path, file_count: int = 5) -> None:
        """Create test content for performance testing.
        
        Args:
            base_dir: Base directory for content
            file_count: Number of files to create
        """
        # Create generated-docs structure
        generated_docs = base_dir / "generated-docs"
        generated_docs.mkdir()
        
        sections = ["prd", "arch", "impl", "task"]
        
        for i in range(file_count):
            section = sections[i % len(sections)]
            section_dir = generated_docs / section
            section_dir.mkdir(exist_ok=True)
            
            file_path = section_dir / f"test_{i}.md"
            content = f"""# Test Document {i}

## Overview
This is test document {i} in section {section}.

## Requirements
- Feature A{i}
- Feature B{i}
- Feature C{i}

## Code Example
```python
def test_{i}():
    return "test_{i}"
```

## Checklist
- [ ] Task 1 for doc {i}
- [ ] Task 2 for doc {i}
- [ ] Task 3 for doc {i}

## Additional Content
This is additional content to make the file larger and more realistic.
It includes multiple paragraphs and various markdown elements.

### Subsection
- List item 1
- List item 2
- List item 3

### Another Subsection
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
| Value 4  | Value 5  | Value 6  |
"""
            file_path.write_text(content)
    
    def _generate_large_content(self, size_mb: int) -> str:
        """Generate large content for testing.
        
        Args:
            size_mb: Size in megabytes
            
        Returns:
            Large content string
        """
        # Base content template
        base_content = """# Large Test Document

## Overview
This is a large test document for performance testing.

## Requirements
- Feature 1: Authentication
- Feature 2: Data storage
- Feature 3: API endpoints

## Code Examples
```python
def example_function():
    return "example"
```

## Detailed Content
"""
        
        # Calculate how much content to add
        target_size = size_mb * 1024 * 1024  # Convert to bytes
        current_size = len(base_content.encode('utf-8'))
        
        # Add content until we reach target size
        additional_content = []
        while current_size < target_size:
            chunk = f"""
### Section {len(additional_content) + 1}

This is section {len(additional_content) + 1} of the large document.
It contains detailed information about various aspects of the system.

#### Subsection A
- Item 1: Detailed description
- Item 2: Another detailed description
- Item 3: Yet another detailed description

#### Subsection B
| Column A | Column B | Column C |
|----------|----------|----------|
| Value A1 | Value B1 | Value C1 |
| Value A2 | Value B2 | Value C2 |
| Value A3 | Value B3 | Value C3 |

#### Code Example
```python
def section_{len(additional_content) + 1}_function():
    # This is a code example for section {len(additional_content) + 1}
    result = []
    for j in range(100):
        result.append(f"item_{{j}}")
    return result
```

#### Additional Information
This section contains additional information to increase the file size.
It includes multiple paragraphs with various content types.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor 
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore 
eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, 
sunt in culpa qui officia deserunt mollit anim id est laborum.
"""
            additional_content.append(chunk)
            current_size += len(chunk.encode('utf-8'))
        
        return base_content + "".join(additional_content)
    
    def _generate_performance_report(self) -> Dict[str, Any]:
        """Generate performance test report.
        
        Returns:
            Performance report dictionary
        """
        if not self.metrics:
            return {"error": "No performance metrics collected"}
        
        # Calculate statistics
        durations = [m.duration for m in self.metrics if m.duration > 0]
        memory_usage = [m.memory_usage for m in self.metrics if m.memory_usage > 0]
        file_counts = [m.file_count for m in self.metrics if m.file_count > 0]
        
        return {
            "total_operations": len(self.metrics),
            "average_duration": sum(durations) / len(durations) if durations else 0,
            "max_duration": max(durations) if durations else 0,
            "min_duration": min(durations) if durations else 0,
            "average_memory": sum(memory_usage) / len(memory_usage) if memory_usage else 0,
            "max_memory": max(memory_usage) if memory_usage else 0,
            "total_files_processed": sum(file_counts),
            "metrics": [
                {
                    "operation": m.operation,
                    "duration": m.duration,
                    "memory_usage": m.memory_usage,
                    "file_count": m.file_count,
                    "file_size": m.file_size
                }
                for m in self.metrics
            ]
        }
    
    def _display_performance_results(self) -> None:
        """Display performance results in a formatted table."""
        console.print("\n" + "="*60, style="bold blue")
        console.print("⚡ PERFORMANCE TEST RESULTS", style="bold blue")
        console.print("="*60, style="bold blue")
        
        # Create performance table
        table = Table(title="Performance Metrics")
        table.add_column("Operation", style="cyan", no_wrap=True)
        table.add_column("Duration (s)", style="green")
        table.add_column("Memory (MB)", style="yellow")
        table.add_column("Files", style="blue")
        table.add_column("Size (bytes)", style="magenta")
        
        for metric in self.metrics:
            table.add_row(
                metric.operation.replace("_", " ").title(),
                f"{metric.duration:.2f}",
                f"{metric.memory_usage:.1f}",
                str(metric.file_count),
                f"{metric.file_size:,}"
            )
        
        console.print(table)
        
        # Display summary
        report = self._generate_performance_report()
        summary_panel = Panel(
            f"""Total Operations: {report['total_operations']}
Average Duration: {report['average_duration']:.2f}s
Max Duration: {report['max_duration']:.2f}s
Average Memory: {report['average_memory']:.1f}MB
Max Memory: {report['max_memory']:.1f}MB
Total Files: {report['total_files_processed']:,}""",
            title="Performance Summary",
            border_style="green"
        )
        console.print(summary_panel)
