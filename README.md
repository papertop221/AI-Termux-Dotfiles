# 🤖 AI-First Termux Dotfiles

Transform your Termux into a pure Natural Language Terminal. Powered by Gemini CLI.

## ✨ Features
- **Natural Language to Bash:** Execute commands using human language.
- **Silent Execution:** `cd` and other state-changing commands work seamlessly without subshell issues.
- **Headless Chat:** Conversational AI directly in your shell (remember context!).
- **Tokyo Night Theme:** Beautiful aesthetic for high-productivity.

## 🚀 Installation

```bash
pkg install git -y
git clone https://github.com/YOUR_USERNAME/AI-Termux-Dotfiles.git
cd AI-Termux-Dotfiles
chmod +x install.sh
./install.sh
```

## 🛠 How it works
- `install.sh`: The master setup script.
- `.ai_terminal.py`: The brain of the AI interaction (handles history and logic).
- `bashrc_template`: AI-enhanced shell configuration.
- `.termux/`: UI and Keyboard settings.

## 📝 Usage
Just type like a human:
- `pindah ke folder storage`
- `apa saja file yang ada di sini?`
- `siapa pembuat linux?`
- `hapus semua file sementara`
