"""Auto-discovery of template files and document types."""

from pathlib import Path
from typing import List, Dict

def get_available_commands() -> List[str]:
    """Auto-discover available Cursor command files."""
    try:
        import nexus
        if hasattr(nexus, '__file__') and nexus.__file__:
            package_root = Path(nexus.__file__).parent
        else:
            import os
            package_root = Path(os.path.dirname(os.path.abspath(__file__))).parent
    except ImportError:
        import os
        package_root = Path(os.path.dirname(os.path.abspath(__file__))).parent
    
    commands_dir = package_root / "commands"
    
    if not commands_dir.exists():
        return []
    
    return [f.stem for f in commands_dir.glob("*.md")]

def get_available_instructions() -> List[str]:
    """Auto-discover available instruction files."""
    try:
        import nexus
        if hasattr(nexus, '__file__') and nexus.__file__:
            package_root = Path(nexus.__file__).parent
        else:
            import os
            package_root = Path(os.path.dirname(os.path.abspath(__file__))).parent
    except ImportError:
        import os
        package_root = Path(os.path.dirname(os.path.abspath(__file__))).parent
    
    instructions_dir = package_root / "instructions"
    
    if not instructions_dir.exists():
        return []
    
    return [f.stem for f in instructions_dir.glob("*.md")]

def get_document_types() -> List[str]:
    """Get supported document types."""
    # This could be made configurable in the future
    return ["arch", "exec", "impl", "int", "prd", "rules", "task", "tests"]

def get_template_info() -> Dict:
    """Get comprehensive template information."""
    return {
        "commands": get_available_commands(),
        "instructions": get_available_instructions(), 
        "document_types": get_document_types(),
        "version": get_template_version()
    }

def get_template_version() -> str:
    """Get current template version."""
    from nexus.core.updater import ProjectUpdater
    return ProjectUpdater.CURRENT_TEMPLATE_VERSION
