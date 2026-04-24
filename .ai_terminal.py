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
        # Simpan hanya 3 history terakhir untuk kecepatan maksimal
        json.dump(history[-3:], f, indent=2)

def main():
    user_input = " ".join(sys.argv[1:])
    if not user_input:
        return

    history = load_history()
    h_ctx = "\n".join([f"U:{h['u']}\nA:{h['a']}" for h in history])
    
    # Prompt minimalis untuk mengurangi latency pemrosesan
    prompt = f"Dir:{os.getcwd()}\n{h_ctx}\nIn:{user_input}\nOut: EXEC: <cmd> OR CHAT: <msg>"

    try:
        # Gunakan --output-format text agar tidak streaming (lebih cepat untuk headless)
        proc = subprocess.run(
            ["gemini", "--approval-mode", "yolo", "--output-format", "text", "-p", prompt],
            capture_output=True, text=True
        )
        response = proc.stdout.strip()
        
        final_line = ""
        # Ambil baris jawaban terakhir
        for line in reversed(response.split('\n')):
            if "EXEC:" in line or "CHAT:" in line:
                # Bersihkan sisa-sisa markdown atau simbol jika ada
                final_line = line.strip().replace("`", "")
                break
        
        if final_line:
            # Pastikan prefix benar
            if final_line.startswith("EXEC:") or final_line.startswith("CHAT:"):
                print(final_line)
                history.append({"u": user_input, "a": final_line})
                save_history(history)
            else:
                # Jika prefix hilang tapi ada konten, paksa CHAT
                print(f"CHAT: {final_line}")
        else:
            # Fallback
            clean = " ".join([l for l in response.split('\n') if not l.startswith('[') and l.strip()])
            if clean:
                print(f"CHAT: {clean}")
            
    except Exception as e:
        print(f"CHAT: Error: {str(e)}")

if __name__ == "__main__":
    main()
