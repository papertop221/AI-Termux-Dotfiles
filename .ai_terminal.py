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
        except: pass
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[-3:], f, indent=2)

def main():
    if len(sys.argv) < 2: return
    
    user_input = sys.argv[1]
    last_cmd = sys.argv[2] if len(sys.argv) > 2 else ""
    last_status = sys.argv[3] if len(sys.argv) > 3 else "0"
    
    history = load_history()
    h_ctx = "\n".join([f"U:{h['u']}\nA:{h['a']}" for h in history])
    
    prompt = (
        f"You are a Proactive Terminal Guardian.\n"
        f"Dir: {os.getcwd()}\n"
        f"LastCmd: '{last_cmd}' (Exit:{last_status})\n"
        f"Context:\n{h_ctx}\n\n"
        f"User: {user_input}\n\n"
        f"Task:\n"
        f"1. If LastCmd failed and user asks 'why' or 'fix', output 'FIX: <bash command>'.\n"
        f"2. If user wants a task, output 'EXEC: <bash command>'.\n"
        f"3. Else, output 'CHAT: <response>'.\n"
        f"4. Be terse. NO markdown."
    )

    try:
        proc = subprocess.run(
            ["gemini", "--approval-mode", "yolo", "--output-format", "text", "-p", prompt],
            capture_output=True, text=True
        )
        response = proc.stdout.strip()
        
        final_line = ""
        for line in reversed(response.split('\n')):
            if any(p in line for p in ["EXEC:", "CHAT:", "FIX:"]):
                final_line = line.strip().replace("`", "")
                break
        
        if final_line:
            print(final_line)
            history.append({"u": user_input, "a": final_line})
            save_history(history)
        else:
            clean = " ".join([l for l in response.split('\n') if not l.startswith('[') and l.strip()])
            if clean: print(f"CHAT: {clean}")
            
    except Exception as e:
        print(f"CHAT: Error: {str(e)}")

if __name__ == "__main__":
    main()
