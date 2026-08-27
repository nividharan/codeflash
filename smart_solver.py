import time
import os
import json
import re
import pyautogui
import pyperclip
import keyboard
from google import genai

pyautogui.PAUSE = 0.0
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
TARGET_LANGUAGE = "Java"

# Fallback models in priority order
MODELS_TO_TRY = ["gemini-3.6-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-flash"]

def get_api_key():
    if "GEMINI_API_KEY" in os.environ and os.environ["GEMINI_API_KEY"].strip():
        return os.environ["GEMINI_API_KEY"].strip()

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("api_key"):
                    return data["api_key"]
        except Exception:
            pass

    key = input("Enter Gemini API Key: ").strip()
    if key:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"api_key": key}, f)
        return key
    return None

def clean_code(raw_text: str) -> str:
    text = raw_text.strip()
    match = re.search(r"```(?:java)?\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    if text.startswith("```"):
        lines = text.split("\n")
        return "\n".join(lines[1:-1]).strip()
    return text

def solve_and_type(client):
    print("\n[⚡] F8 detected! Reading question from clipboard...")
    
    question = pyperclip.paste().strip()
    if not question or len(question) < 5:
        print("[!] Clipboard is empty or too short. Please copy (Ctrl+C) the problem description first!")
        return

    print("[⚡] Solving problem in Java using Gemini AI...")
    
    prompt = f"""
You are an expert competitive programmer. 
Solve the following coding problem in Java.
Requirements:
1. Write optimal time and space complexity solution.
2. Provide ONLY valid Java class and methods suitable for LeetCode / competitive programming platforms.
3. Do NOT include any explanations, markdown text, or intro/outro. Only raw Java code.

Problem:
{question}
"""

    response = None
    last_error = None
    for model_name in MODELS_TO_TRY:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            if response and response.text:
                print(f"[✓] Solved using model: {model_name}")
                break
        except Exception as e:
            last_error = e
            continue

    if not response or not response.text:
        print(f"[!] Error generating solution across models: {last_error}")
        return

    code = clean_code(response.text)

    print("[⚡] Solution ready! Pasting into active editor in 1.5 seconds...")
    time.sleep(1.5)

    pyperclip.copy(code)
    time.sleep(0.05)
    pyautogui.hotkey('ctrl', 'v')

    print("[✓] SUCCESS: Java solution inserted into editor!\n")

def main():
    api_key = get_api_key()
    if not api_key:
        print("[!] No API key provided. Exiting.")
        return

    client = genai.Client(api_key=api_key)

    print("=" * 60)
    print(">> UNIVERSAL JAVA ONE-HOTKEY SOLVER READY")
    print(">> Target Language: JAVA")
    print(">> Global Hotkey:   [ F8 ]")
    print("=" * 60)
    print("How to use on LeetCode / HackerRank / any site:")
    print("  1. Highlight problem description and press Ctrl + C.")
    print("  2. Click inside the code editor so cursor is blinking.")
    print("  3. Press F8 on your keyboard.")
    print("=" * 60)
    print("Listening for F8 keypress... (Press Ctrl+C in terminal to stop)\n")

    keyboard.add_hotkey('F8', lambda: solve_and_type(client))
    keyboard.wait()

if __name__ == "__main__":
    main()
