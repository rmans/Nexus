#!/usr/bin/env python3
"""Nexus installation script with hybrid configuration support."""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from nexus.core.installer import install_nexus, uninstall_nexus, check_installation
from rich.console import Console

console = Console()

def main():
    """Main installation entry point."""
    console.print("🚀 Nexus Installer", style="bold blue")
    console.print("=" * 50)
    
    # Check if already installed
    status = check_installation()
    
    if status["installed"]:
        console.print(f"✅ Nexus is already installed at: {status['install_dir']}", style="green")
        console.print(f"Version: {status.get('version', 'Unknown')}")
        
        choice = input("\nWhat would you like to do? (r)eininstall, (u)ninstall, (q)uit: ").lower()
        
        if choice == 'r':
            console.print("Reinstalling Nexus...", style="yellow")
            success = install_nexus(force=True)
        elif choice == 'u':
            console.print("Uninstalling Nexus...", style="yellow")
            success = uninstall_nexus()
        else:
            console.print("Installation cancelled.", style="yellow")
            return
    else:
        console.print("Installing Nexus...", style="blue")
        success = install_nexus()
    
    if success:
        console.print("\n🎉 Operation completed successfully!", style="green")
    else:
        console.print("\n❌ Operation failed!", style="red")
        sys.exit(1)

if __name__ == "__main__":
    main()
