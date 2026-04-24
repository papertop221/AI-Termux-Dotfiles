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
        
        # Bersihkan output dari header gemini jika ada
        lines = [line for line in response.split('\n') if not line.startswith('[') and line.strip()]
        clean_response = " ".join(lines).strip()

        if clean_response.startswith("EXEC:") or clean_response.startswith("CHAT:"):
            print(clean_response)
            # Simpan history
            history.append({"u": user_input, "a": clean_response})
            save_history(history)
        else:
            # Fallback jika AI bingung
            print(f"CHAT: {clean_response}")
            
    except Exception as e:
        print(f"CHAT: Error: {str(e)}")

if __name__ == "__main__":
    main()
