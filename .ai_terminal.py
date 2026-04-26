#!/usr/bin/env python3
import sys, subprocess, os, re

# Integrasi Kompresi VoidCore
sys.path.append(os.path.expanduser("~/.gemini/extensions/voidcore/skills/voidcore/scripts"))
try:
    import voidcore_core
    def compress(text): return voidcore_core.compress(text)
except ImportError:
    def compress(text): return text

def main():
    if len(sys.argv) < 2: return
    user_goal = sys.argv[1]
    last_cmd = sys.argv[2] if len(sys.argv) > 2 else ""
    last_status = sys.argv[3] if len(sys.argv) > 3 else "0"
    
    # Kompres goal user untuk hemat token
    compressed_goal = compress(user_goal)
    
    prompt = (
        f"Dir: {os.getcwd()}\n"
        f"LastCmd: {last_cmd} (Status: {last_status})\n"
        f"Goal: {compressed_goal}"
    )

    try:
        proc = subprocess.run(
            ["gemini", "--approval-mode", "yolo", "--output-format", "text", "-p", prompt],
            capture_output=True, text=True
        )
        response = proc.stdout.strip()
        
        for line in reversed(response.split('\n')):
            if line.startswith("EXEC:"):
                print(line)
                return
        
        clean = " ".join([l for l in response.split('\n') if not l.startswith('[') and l.strip()])
        print(clean)
            
    except Exception:
        pass

if __name__ == "__main__":
    main()
