#!/usr/bin/env python3
import sys, subprocess, os

def main():
    if len(sys.argv) < 2: return
    user_goal = sys.argv[1]
    last_cmd = sys.argv[2] if len(sys.argv) > 2 else ""
    last_status = sys.argv[3] if len(sys.argv) > 3 else "0"
    
    # Prompt untuk Agent Otonom Murni
    prompt = (
        f"You are a PURE AUTONOMOUS SHELL AGENT.\n"
        f"Working Dir: {os.getcwd()}\n"
        f"Last Command: {last_cmd} (Status: {last_status})\n\n"
        f"USER GOAL: {user_goal}\n\n"
        f"YOUR RULES:\n"
        f"1. You execute commands directly to achieve the goal.\n"
        f"2. Use '&&' to chain multiple operations.\n"
        f"3. If the goal is a question, answer concisely.\n"
        f"4. Output ONLY 'EXEC: <bash_command>' or just the direct answer text.\n"
        f"5. NO MARKDOWN. NO EXPLANATIONS. JUST ACTION."
    )

    try:
        proc = subprocess.run(
            ["gemini", "--approval-mode", "yolo", "--output-format", "text", "-p", prompt],
            capture_output=True, text=True
        )
        response = proc.stdout.strip()
        
        # Filter output untuk mengambil baris eksekusi
        for line in reversed(response.split('\n')):
            if line.startswith("EXEC:"):
                print(line)
                return
        
        # Jika bukan EXEC, maka itu jawaban/chat murni
        clean_response = " ".join([l for l in response.split('\n') if not l.startswith('[') and l.strip()])
        print(clean_response)
            
    except Exception:
        pass

if __name__ == "__main__":
    main()
