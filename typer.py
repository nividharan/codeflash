import time
import os
import sys
import random
import argparse
import pyautogui
import pyperclip
import keyboard

# Disable PyAutoGUI default delay
pyautogui.PAUSE = 0.0

CODE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "code.txt")


def load_code():
    if os.path.exists(CODE_FILE):
        with open(CODE_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return content
    return "class Solution {\n    public int solve() {\n        return 0;\n    }\n}"


def type_code(text: str, mode: str = "instant"):
    mode = mode.lower()
    print("=" * 60)
    print(f">> Mode: {mode.upper()} SPEED ACTIVATED")
    print(">> Switch to your code editor window now!")
    print(">> Click inside the editor so the cursor is blinking.")
    print("=" * 60)

    for i in range(3, 0, -1):
        print(f"Starting in {i} seconds...", end="\r")
        time.sleep(1)
    print("\n[+] Typing/Pasting code into editor...\n")

    start_time = time.time()

    if mode == "instant":
        pyperclip.copy(text)
        time.sleep(0.05)
        pyautogui.hotkey("ctrl", "v")
    elif mode == "ultra":
        clean_code_str = "\n".join([l.strip() for l in text.splitlines() if l.strip()])
        keyboard.write(clean_code_str, delay=0.003, exact=True)

    elif mode == "human":
        clean_code_str = "\n".join([l.strip() for l in text.splitlines() if l.strip()])
        for char in clean_code_str:
            keyboard.write(char, exact=True)
            if char == "\n":
                time.sleep(random.uniform(0.06, 0.14))
            elif char in (";", "{", "}", "(", ")"):
                time.sleep(random.uniform(0.03, 0.07))
            elif char == " ":
                time.sleep(random.uniform(0.012, 0.03))
            else:
                time.sleep(random.uniform(0.005, 0.018))
    else:
        print(f"[!] Unknown mode '{mode}', defaulting to instant paste.")
        pyperclip.copy(text)
        time.sleep(0.05)
        pyautogui.hotkey("ctrl", "v")

    elapsed = time.time() - start_time
    print(f"\n[✓] Done! Completed in {elapsed:.2f} seconds.")


def main():
    parser = argparse.ArgumentParser(description="CodeFlash Standalone Code Typer")
    parser.add_argument(
        "--mode",
        "-m",
        choices=["instant", "ultra", "human"],
        default="instant",
        help="Typing speed profile (instant, ultra, human)",
    )
    args = parser.parse_args()

    code = load_code()
    type_code(code, mode=args.mode)


if __name__ == "__main__":
    main()
