#!/bin/bash

# AI Elite Wrapper v4.4 - Auto-Wrap Box Edition
# Author: Gemini CLI Agent

# Colors
LAVENDER='\033[38;5;189m'
CYAN='\033[38;5;117m'
NC='\033[0m'

MEMORY_FILE="$HOME/.gemini_context.log"
TMP_FILE="/tmp/.ai_raw_$(date +%s)"
USER_INPUT="$*"
[ -z "$USER_INPUT" ] && exit 0

spinner() {
    local pid=$1
    local delay=0.08
    local spinstr='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    while kill -0 $pid 2>/dev/null; do
        for (( i=0; i<${#spinstr}; i++ )); do
            printf "${CYAN} ${spinstr:$i:1} ${NC}Thinking..."
            sleep $delay
            printf "\r\033[K"
        done
    done
}

CONTEXT=""
[ -f "$MEMORY_FILE" ] && CONTEXT="[Mem: $(tail -n 3 "$MEMORY_FILE" | tr '\n' ' ')] "
SYSTEM="[Style: Human Minimalist. Brief. Wrap response to fit narrow terminal.]"

(gemini "${SYSTEM} ${CONTEXT}Input: ${USER_INPUT}" 2>/dev/null > "$TMP_FILE") &
GEMINI_PID=$!

spinner $GEMINI_PID

if [ -f "$TMP_FILE" ]; then
    RESPONSE=$(grep -Ev "execution plan|hook command|Hook execution|Expanding hook|Created execution" "$TMP_FILE")
    rm "$TMP_FILE"
else
    RESPONSE="Error: Gagal mendapatkan respon dari Gemini."
fi

if [ ! -z "$RESPONSE" ]; then
    echo -e "${LAVENDER}󰚩  AI Assistant${NC}"
    echo -e "${LAVENDER}┌─────────────────────────────────────────────────┐${NC}"
    
    # Bungkus teks agar maksimal 45 karakter per baris
    echo -e "$RESPONSE" | fold -s -w 45 | while IFS= read -r line; do
        # Render setiap baris di dalam bingkai
        printf "${LAVENDER}│ ${NC}%-47s ${LAVENDER}│${NC}\n" "$line"
    done
    
    echo -e "${LAVENDER}└─────────────────────────────────────────────────┘${NC}"
    
    echo "U:$USER_INPUT" >> "$MEMORY_FILE"
    echo "A:$(echo "$RESPONSE" | head -n 1)" >> "$MEMORY_FILE"
fi

if echo "$RESPONSE" | grep -q '```'; then
    echo -ne "${CYAN} 󰑮 Run? (y/N): ${NC}"
    read -n 1 -r
    echo
    if [[ "$REPLY" =~ ^[yY]$ ]]; then
        CMD=$(echo "$RESPONSE" | sed -n '/```/,/```/p' | grep -v '```' | head -n 1)
        eval "$CMD"
    fi
fi
