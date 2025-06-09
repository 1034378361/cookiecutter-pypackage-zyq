#!/bin/bash
# Installation script for Unix-like systems (Linux/macOS)

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up development environment...${NC}"

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="MacOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
else
    OS="Unknown"
fi

echo -e "${YELLOW}Detected OS: $OS${NC}"

# Install pyenv
install_pyenv_macos() {
    echo -e "${GREEN}Installing pyenv using Homebrew...${NC}"
    if ! command -v brew &> /dev/null; then
        echo -e "${YELLOW}Homebrew not found. Installing Homebrew...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    brew install pyenv

    # Set up shell environment
    echo -e "${YELLOW}Adding pyenv to shell configuration...${NC}"
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc

    # Also add to zsh if it exists
    if [ -f ~/.zshrc ]; then
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
        echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
        echo 'eval "$(pyenv init -)"' >> ~/.zshrc
    fi
}

install_pyenv_linux() {
    echo -e "${GREEN}Installing pyenv...${NC}"
    curl https://pyenv.run | bash

    # Set up shell environment
    echo -e "${YELLOW}Adding pyenv to shell configuration...${NC}"
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc

    # Also add to zsh if it exists
    if [ -f ~/.zshrc ]; then
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
        echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
        echo 'eval "$(pyenv init -)"' >> ~/.zshrc
    fi
}

# Install PDM
install_pdm() {
    echo -e "${GREEN}Installing PDM...${NC}"
    curl -sSL https://pdm-project.org/install-pdm.py | python3 -
}

# Main installation logic
if [[ "$OS" == "MacOS" ]]; then
    install_pyenv_macos
elif [[ "$OS" == "Linux" ]]; then
    install_pyenv_linux
else
    echo -e "${RED}Unsupported OS. Please install pyenv manually.${NC}"
    exit 1
fi

# Ask if user wants to install PDM
read -p "Do you want to install PDM? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    install_pdm
fi

echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "${YELLOW}Please restart your terminal or run 'source ~/.bashrc' (or 'source ~/.zshrc') to apply the changes.${NC}"
