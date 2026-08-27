import time
import os
import pyautogui
import pyperclip

# Disable PyAutoGUI's internal default delays for MAXIMUM speed
pyautogui.PAUSE = 0.0

CODE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "code.txt")

def load_code():
    if os.path.exists(CODE_FILE):
        with open(CODE_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return content
    return "class Solution {}"

def instant_type(text: str):
    print("=" * 60)
    print(">> Mode: LIGHTNING / MAXIMUM SPEED ACTIVATED")
    print(">> Switch to your LeetCode editor window now!")
    print(">> Click inside the editor so the cursor is blinking.")
    print("=" * 60)

    for i in range(3, 0, -1):
        print(f"Starting in {i} seconds...", end="\r")
        time.sleep(1)
    print("\n[+] Instant pasting into editor...\n")

    # Copy full code to clipboard and paste instantly in 1 keystroke
    pyperclip.copy(text)
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'v')

    print("\n[✓] Done! 100% completed in 0.1 seconds.")

if __name__ == "__main__":
    code = load_code()
    instant_type(code)
