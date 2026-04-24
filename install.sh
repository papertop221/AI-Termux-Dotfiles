#!/data/data/com.termux/files/usr/bin/bash

# AI Terminal Dotfiles Installer
REPO_DIR=$(pwd)

echo "[*] Initializing AI Terminal Installation from Repo..."

# 1. Update & Install Basic Deps
pkg update -y && pkg upgrade -y
pkg install -y python nodejs-lts starship git ncurses-utils

# 2. Install Gemini CLI
if ! command -v gemini &> /dev/null; then
    echo "[*] Installing Gemini CLI..."
    npm install -g @google/gemini-cli
fi

# 3. Copy AI Logic
echo "[*] Setting up AI brain..."
cp "$REPO_DIR/.ai_terminal.py" ~/.ai_terminal.py
chmod +x ~/.ai_terminal.py

# 4. Setup Bash Config
echo "[*] Configuring shell..."
cp "$REPO_DIR/bashrc_template" ~/.bashrc

# 5. Restore Styling
echo "[*] Applying Tokyo Night theme..."
mkdir -p ~/.termux
cp "$REPO_DIR/.termux/colors.properties" ~/.termux/
cp "$REPO_DIR/.termux/termux.properties" ~/.termux/

# Refresh styling
termux-reload-settings

echo -e "\n[+] AI Terminal Installed Successfully!"
echo "[!] Please run 'source ~/.bashrc' or restart Termux."
