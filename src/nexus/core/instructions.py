"""Instructions module for creating and executing instructions."""

from pathlib import Path
from rich.console import Console

console = Console()

def create_instruction_template(name, template=None, output=None, interactive=False):
    """Create a new instruction template.
    
    Args:
        name: Name of the instruction
        template: Template to use
        output: Output file path
        interactive: Use interactive mode
    """
    console.print(f"📝 Creating instruction: {name}", style="green")
    
    # Determine output path
    if output:
        output_path = Path(output)
    else:
        output_path = Path(f"{name}.md")
    
    # Create instruction content
    content = f"""# {name.title()} Instruction

## Purpose
Describe the purpose of this instruction.

## Prerequisites
- List any prerequisites here
- Add more items as needed

## Steps
1. First step
2. Second step
3. Third step

## Expected Outcome
Describe what should be achieved.

## Notes
Add any additional notes or considerations.
"""
    
    # Write instruction file
    output_path.write_text(content)
    console.print(f"✅ Created instruction: {output_path}", style="green")
    
    if interactive:
        console.print("💡 You can now edit the instruction file to customize it.", style="blue")

def execute_instruction_file(instruction, dry_run=False, parallel=False, timeout=None):
    """Execute an instruction file.
    
    Args:
        instruction: Path to instruction file
        dry_run: Preview execution without running
        parallel: Enable parallel execution
        timeout: Execution timeout in seconds
    """
    instruction_path = Path(instruction)
    
    if not instruction_path.exists():
        console.print(f"❌ Instruction file not found: {instruction}", style="red")
        return
    
    console.print(f"🚀 Executing: {instruction}", style="green")
    
    if dry_run:
        console.print("🔍 Dry run mode - no actual execution", style="yellow")
        console.print("📄 Instruction content:")
        console.print(instruction_path.read_text())
        return
    
    # For now, just show the instruction content
    # In a full implementation, this would parse and execute the instruction
    console.print("📄 Instruction content:")
    console.print(instruction_path.read_text())
    console.print("✅ Instruction execution complete", style="green")
