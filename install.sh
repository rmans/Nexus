#!/bin/bash
# Nexus installation script for Unix-like systems

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed."
        print_status "Please install Python 3.8 or higher and try again."
        exit 1
    fi
    
    # Check Python version
    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    required_version="3.8"
    
    if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
        print_error "Python 3.8 or higher is required. Found: $python_version"
        exit 1
    fi
    
    print_success "Python $python_version found"
}

# Check if pip is installed
check_pip() {
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is required but not installed."
        print_status "Please install pip3 and try again."
        exit 1
    fi
    
    print_success "pip3 found"
}

# Install Nexus
install_nexus() {
    print_status "Installing Nexus with hybrid configuration system..."
    
    # Install from PyPI if available, otherwise from source
    if pip3 install nexus-context --user; then
        print_success "Nexus installed from PyPI"
    else
        print_warning "PyPI installation failed, trying local installation..."
        
        # Get script directory
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        
        # Install from source
        if [ -f "$SCRIPT_DIR/setup.py" ]; then
            pip3 install "$SCRIPT_DIR" --user
            print_success "Nexus installed from source"
        else
            print_error "Could not find setup.py for local installation"
            exit 1
        fi
    fi
}

# Set up PATH
setup_path() {
    print_status "Setting up PATH..."
    
    # Get user's home directory
    USER_HOME="$HOME"
    
    # Add ~/.local/bin to PATH if not already there
    if [[ ":$PATH:" != *":$USER_HOME/.local/bin:"* ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$USER_HOME/.bashrc"
        print_success "Added ~/.local/bin to PATH in ~/.bashrc"
        print_warning "Please run 'source ~/.bashrc' or restart your terminal"
    else
        print_success "~/.local/bin already in PATH"
    fi
}

# Verify installation
verify_installation() {
    print_status "Verifying installation..."
    
    if command -v nexus &> /dev/null; then
        print_success "Nexus command found"
        
        # Test basic functionality
        if nexus --version &> /dev/null; then
            print_success "Nexus is working correctly"
        else
            print_warning "Nexus installed but may have issues"
        fi
    else
        print_warning "Nexus command not found in PATH"
        print_status "You may need to restart your terminal or run 'source ~/.bashrc'"
    fi
}

# Main installation process
main() {
    echo "🚀 Nexus Installer for Unix-like Systems"
    echo "========================================"
    
    # Check prerequisites
    check_python
    check_pip
    
    # Install Nexus
    install_nexus
    
    # Set up PATH
    setup_path
    
    # Verify installation
    verify_installation
    
    echo ""
    print_success "Installation complete!"
    echo ""
    echo "Next steps:"
    echo "1. Run 'source ~/.bashrc' or restart your terminal"
    echo "2. Run 'nexus init-project' to create a new project"
    echo "3. Run 'nexus status' to check the installation"
    echo "4. Run 'nexus --help' for more information"
    echo ""
    print_status "For documentation, visit: https://github.com/rmans/Nexus"
}

# Run main function
main "$@"
