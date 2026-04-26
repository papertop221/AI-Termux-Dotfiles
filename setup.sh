#!/bin/bash

# Termux AI Setup - Modern & Minimalist
# Author: Gemini CLI Agent

set -e

echo "🚀 Memulai instalasi Termux AI..."

# 1. Update & Install Dependensi
echo "📦 Mengupdate paket dan menginstal dependensi..."
pkg update -y && pkg upgrade -y
pkg install -y nodejs-lts starship eza wget fontconfig git

# 2. Persiapan Folder Konfigurasi
echo "📁 Menyiapkan folder konfigurasi..."
mkdir -p ~/.termux
mkdir -p ~/.config

# 3. Menerapkan Konfigurasi Tampilan
echo "🎨 Menerapkan tema dan properti..."
cp configs/colors.properties ~/.termux/colors.properties
cp configs/termux.properties ~/.termux/termux.properties
cp configs/starship.toml ~/.config/starship.toml

# 4. Instalasi Font (Nerd Font)
echo "🔡 Mengunduh JetBrainsMono Nerd Font..."
FONT_DIR="$HOME/.termux"
FONT_URL="https://github.com/ryanoasis/nerd-fonts/raw/master/patched-fonts/JetBrainsMono/Ligatures/Regular/JetBrainsMonoNerdFont-Regular.ttf"
wget -q --show-progress "$FONT_URL" -O "$FONT_DIR/font.ttf"

# 5. Konfigurasi Shell (.bashrc)
echo "🐚 Mengonfigurasi shell bash..."
if ! grep -q "starship init bash" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# Termux AI Elite Setup" >> ~/.bashrc
    echo 'eval "$(starship init bash)"' >> ~/.bashrc
    echo "alias ls='eza --icons --group-directories-first'" >> ~/.bashrc
    echo "alias ll='eza -l --icons --group-directories-first'" >> ~/.bashrc
    echo "alias ai='bash ~/termux-ai-setup/scripts/ai-wrapper.sh'" >> ~/.bashrc
fi

# 6. Memberikan izin pada script
chmod +x scripts/ai-wrapper.sh

# 6. Instalasi Gemini CLI
echo "🧠 Menginstal Gemini CLI secara global..."
npm install -g @google/gemini-cli

# 7. Finalisasi
echo "✨ Menyegarkan pengaturan Termux..."
termux-reload-settings

echo ""
echo "✅ SETUP BERHASIL SELESAI!"
echo "------------------------------------------------"
echo "Silakan ketik 'source ~/.bashrc' atau buka kembali"
echo "Termux Anda untuk melihat perubahannya."
echo "Gunakan perintah 'ai' untuk berinteraksi dengan AI."
echo "------------------------------------------------"
