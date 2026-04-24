#!/usr/bin/env python3
import sys
import json
import subprocess
import os

HISTORY_FILE = os.path.expanduser("~/.ai_history.json")

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[-10:], f, indent=2)

def main():
    user_input = " ".join(sys.argv[1:])
    if not user_input:
        return

    history = load_history()
    
    # Buat prompt dengan konteks
    history_context = "\n".join([f"User: {h['u']}\nAI: {h['a']}" for h in history])
    
    system_prompt = f"""You are an AI Terminal Agent. 
Current Directory: {os.getcwd()}
History:
{history_context}

If the user wants to perform a task, output ONLY 'EXEC: <bash command>'.
If the user is asking a question or just chatting, output 'CHAT: <your response>'.
NO Markdown. NO explanations. Silence is golden.
User: {user_input}"""

    # Panggil gemini
    try:
        proc = subprocess.run(
            ["gemini", "--approval-mode", "yolo", "-p", system_prompt],
            capture_output=True, text=True
        )
        response = proc.stdout.strip()
        
        # Ambil hanya baris terakhir yang mengandung EXEC: atau CHAT:
        final_line = ""
        for line in reversed(response.split('\n')):
            if line.startswith("EXEC:") or line.startswith("CHAT:"):
                final_line = line
                break
        
        if final_line:
            print(final_line)
            # Simpan history
            history.append({"u": user_input, "a": final_line})
            save_history(history)
        else:
            # Jika tidak ada prefix, anggap itu CHAT murni
            # Tapi bersihkan dulu dari baris progress gemini
            clean_lines = [l for l in response.split('\n') if not l.startswith('[') and l.strip()]
            print(f"CHAT: {' '.join(clean_lines)}")
            
    except Exception as e:
        print(f"CHAT: Error: {str(e)}")

if __name__ == "__main__":
    main()
