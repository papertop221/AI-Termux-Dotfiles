#!/bin/bash

# Termux AI Setup - Modern & Minimalist
# Author: Gemini CLI Agent

set -e

echo "🚀 Memulai instalasi Termux AI..."

# 1. Update & Install Dependensi
echo "📦 Mengupdate paket dan menginstal dependensi..."
pkg update -y && pkg upgrade -y
pkg install -y nodejs-lts starship eza wget fontconfig git neovim python-pip

# 2. Persiapan Folder Konfigurasi
echo "📁 Menyiapkan folder konfigurasi..."
mkdir -p ~/.termux
mkdir -p ~/.config

# 3. Menerapkan Konfigurasi Tampilan
echo "🎨 Menerapkan tema dan properti..."
cp configs/colors.properties ~/.termux/colors.properties
cp configs/termux.properties ~/.termux/termux.properties
cp configs/starship.toml ~/.config/starship.toml
cp .ai_terminal.py ~/.ai_terminal.py
chmod +x ~/.ai_terminal.py

# 4. Instalasi Font (Nerd Font)
echo "🔡 Mengunduh JetBrainsMono Nerd Font..."
FONT_DIR="$HOME/.termux"
FONT_URL="https://github.com/ryanoasis/nerd-fonts/raw/master/patched-fonts/JetBrainsMono/Ligatures/Regular/JetBrainsMonoNerdFont-Regular.ttf"
wget -q --show-progress "$FONT_URL" -O "$FONT_DIR/font.ttf"

# 5. Konfigurasi Shell (.bashrc)
echo "🐚 Mengonfigurasi shell bash..."
REPO_DIR=$(pwd)
# Update path in bashrc_template before copying/appending
sed -i "s|~/AI-Termux-Dotfiles|$REPO_DIR|g" bashrc_template

if [ ! -f ~/.bashrc_backup ]; then
    cp ~/.bashrc ~/.bashrc_backup
    echo "✅ Backup .bashrc dibuat di ~/.bashrc_backup"
fi

cat bashrc_template > ~/.bashrc
echo "✅ .bashrc diperbarui dengan bashrc_template"

# 6. Memberikan izin pada script
chmod +x scripts/ai-wrapper.sh

# 7. Instalasi Gemini CLI & Extensions
echo "🧠 Menginstal Gemini CLI dan ekstensi..."
npm install -g @google/gemini-cli
gemini extensions install https://github.com/gemini-cli-extensions/jules --consent --skip-settings || true
gemini extensions install https://github.com/gemini-cli-extensions/conductor --consent --skip-settings || true
gemini extensions install https://github.com/JuliusBrussee/caveman --consent --skip-settings || true

# 8. Setup Neovim + LazyVim
echo "💤 Menyiapkan Neovim + LazyVim..."
if [ ! -d "$HOME/.config/nvim" ]; then
    git clone https://github.com/LazyVim/starter ~/.config/nvim
    rm -rf ~/.config/nvim/.git
    echo "✅ LazyVim starter terinstal."
else
    echo "ℹ️ ~/.config/nvim sudah ada, melewati instalasi LazyVim."
fi

# 9. Finalisasi
echo "✨ Menyegarkan pengaturan Termux..."
termux-reload-settings

echo ""
echo "✅ SETUP BERHASIL SELESAI!"
echo "------------------------------------------------"
echo "Silakan ketik 'source ~/.bashrc' atau buka kembali"
echo "Termux Anda untuk melihat perubahannya."
echo "Gunakan perintah 'ai' untuk berinteraksi dengan AI."
echo "------------------------------------------------"
