#!/usr/bin/env python3
import sys, json, subprocess, os

HISTORY_FILE = os.path.expanduser("~/.ai_history.json")

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f: return json.load(f)
        except: pass
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f: json.dump(history[-3:], f, indent=2)

def main():
    if len(sys.argv) < 2: return
    user_input, last_cmd = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ""
    last_status = sys.argv[3] if len(sys.argv) > 3 else "0"
    
    history = load_history()
    h_ctx = "\n".join([f"U:{h['u']}\nA:{h['a']}" for h in history])
    
    if user_input == "[AUTO_ERROR_CHECK]":
        prompt = (
            f"You are an OMNISCIENT TERMINAL GUARDIAN.\n"
            f"Failed Command: '{last_cmd}' (Exit Code: {last_status})\n"
            f"Task: Analyze the failure. If it's a simple typo or missing common directory, output 'AUTO_FIX: <corrected command>'.\n"
            f"If it's complex or destructive (rm, system changes), output 'FIX: <corrected command>'.\n"
            f"Output ONLY the prefix and command. No explanation."
        )
    else:
        prompt = (
            f"You are a SUPER INTELLIGENT AUTONOMOUS TERMINAL AGENT.\n"
            f"Dir: {os.getcwd()}\nLastCmd: '{last_cmd}' ({last_status})\n"
            f"Context: {h_ctx}\nInput: {user_input}\n\n"
            f"Instructions:\n"
            f"1. Be proactive. If task is multi-step, use && to chain commands.\n"
            f"2. If you are 100% sure about a simple fix for a failure, use 'AUTO_FIX: <bash>'.\n"
            f"3. For normal tasks, use 'EXEC: <bash>'.\n"
            f"4. For chat, use 'CHAT: <text>'.\n"
            f"Output ONLY one prefix per response."
        )

    try:
        proc = subprocess.run(
            ["gemini", "--approval-mode", "yolo", "--output-format", "text", "-p", prompt],
            capture_output=True, text=True
        )
        response = proc.stdout.strip()
        final_line = ""
        for line in reversed(response.split('\n')):
            if any(p in line for p in ["EXEC:", "CHAT:", "FIX:", "AUTO_FIX:"]):
                final_line = line.strip().replace("`", "")
                break
        
        if final_line:
            print(final_line)
            if "AUTO_ERROR" not in user_input:
                history.append({"u": user_input, "a": final_line})
                save_history(history)
        else:
            clean = " ".join([l for l in response.split('\n') if not l.startswith('[') and l.strip()])
            if clean: print(f"CHAT: {clean}")
    except Exception as e:
        print(f"CHAT: Error: {str(e)}")

if __name__ == "__main__":
    main()
