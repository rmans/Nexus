#!/bin/bash
# Nexus installation script for macOS

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

# Check if Homebrew is installed
check_homebrew() {
    if command -v brew &> /dev/null; then
        print_success "Homebrew found"
        return 0
    else
        print_warning "Homebrew not found"
        return 1
    fi
}

# Install Homebrew if not present
install_homebrew() {
    print_status "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for Apple Silicon Macs
    if [[ $(uname -m) == "arm64" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    
    print_success "Homebrew installed"
}

# Check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed."
        
        if check_homebrew; then
            print_status "Installing Python via Homebrew..."
            brew install python
        else
            print_status "Please install Python 3.8 or higher from https://python.org"
            exit 1
        fi
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
        print_status "Installing pip..."
        python3 -m ensurepip --upgrade
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

# Set up PATH for different shells
setup_path() {
    print_status "Setting up PATH..."
    
    # Get user's home directory
    USER_HOME="$HOME"
    
    # Determine shell
    SHELL_NAME=$(basename "$SHELL")
    
    case "$SHELL_NAME" in
        "zsh")
            SHELL_RC="$USER_HOME/.zshrc"
            ;;
        "bash")
            SHELL_RC="$USER_HOME/.bash_profile"
            ;;
        *)
            SHELL_RC="$USER_HOME/.profile"
            ;;
    esac
    
    # Add ~/.local/bin to PATH if not already there
    if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$SHELL_RC" 2>/dev/null; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
        print_success "Added ~/.local/bin to PATH in $SHELL_RC"
        print_warning "Please run 'source $SHELL_RC' or restart your terminal"
    else
        print_success "~/.local/bin already in PATH"
    fi
}

# Create application bundle (optional)
create_app_bundle() {
    print_status "Creating application bundle..."
    
    APP_DIR="$HOME/Applications/Nexus.app"
    APP_CONTENTS="$APP_DIR/Contents"
    APP_MACOS="$APP_CONTENTS/MacOS"
    APP_RESOURCES="$APP_CONTENTS/Resources"
    
    # Create app bundle structure
    mkdir -p "$APP_MACOS"
    mkdir -p "$APP_RESOURCES"
    
    # Create Info.plist
    cat > "$APP_CONTENTS/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>nexus</string>
    <key>CFBundleIdentifier</key>
    <string>com.nexus.nexus</string>
    <key>CFBundleName</key>
    <string>Nexus</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
</dict>
</plist>
EOF
    
    # Create launcher script
    cat > "$APP_MACOS/nexus" << EOF
#!/bin/bash
exec "$HOME/.local/bin/nexus" "\$@"
EOF
    
    chmod +x "$APP_MACOS/nexus"
    
    print_success "Application bundle created at $APP_DIR"
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
        print_status "You may need to restart your terminal or run 'source ~/.zshrc' (or ~/.bash_profile)"
    fi
}

# Main installation process
main() {
    echo "🚀 Nexus Installer for macOS"
    echo "============================"
    
    # Check/install Homebrew
    if ! check_homebrew; then
        install_homebrew
    fi
    
    # Check prerequisites
    check_python
    check_pip
    
    # Install Nexus
    install_nexus
    
    # Set up PATH
    setup_path
    
    # Create application bundle (optional)
    if [[ "$1" == "--create-app" ]]; then
        create_app_bundle
    fi
    
    # Verify installation
    verify_installation
    
    echo ""
    print_success "Installation complete!"
    echo ""
    echo "Next steps:"
    echo "1. Run 'source ~/.zshrc' (or ~/.bash_profile) or restart your terminal"
    echo "2. Run 'nexus init-project' to create a new project"
    echo "3. Run 'nexus status' to check the installation"
    echo "4. Run 'nexus --help' for more information"
    echo ""
    print_status "For documentation, visit: https://github.com/rmans/Nexus"
}

# Run main function
main "$@"
