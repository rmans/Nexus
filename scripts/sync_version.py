#!/usr/bin/env python3
"""Sync version from centralized config to pyproject.toml and other files."""

import re
import sys
from pathlib import Path

# Add src to path to import version module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nexus.core.version import get_version_string, get_template_version

def update_pyproject_toml():
    """Update version in pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    
    if not pyproject_path.exists():
        print("❌ pyproject.toml not found")
        return False
    
    content = pyproject_path.read_text()
    version = get_version_string()
    
    # Update version line
    pattern = r'^version = "[^"]*"'
    replacement = f'version = "{version}"'
    
    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    if new_content != content:
        pyproject_path.write_text(new_content)
        print(f"✅ Updated pyproject.toml version to {version}")
        return True
    else:
        print(f"ℹ️ pyproject.toml already has version {version}")
        return True

def update_setup_py():
    """Update version in setup.py if it exists."""
    setup_path = Path(__file__).parent.parent / "setup.py"
    
    if not setup_path.exists():
        print("ℹ️ setup.py not found, skipping")
        return True
    
    content = setup_path.read_text()
    version = get_version_string()
    
    # Look for version in setup() call
    pattern = r'version\s*=\s*["\'][^"\']*["\']'
    replacement = f'version="{version}"'
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        setup_path.write_text(new_content)
        print(f"✅ Updated setup.py version to {version}")
        return True
    else:
        print(f"ℹ️ setup.py already has version {version}")
        return True

def main():
    """Main sync function."""
    print("🔄 Syncing versions from centralized config...")
    print(f"Version: {get_version_string()}")
    print(f"Template Version: {get_template_version()}")
    
    success = True
    success &= update_pyproject_toml()
    success &= update_setup_py()
    
    if success:
        print("✅ Version sync completed successfully")
    else:
        print("❌ Version sync failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
