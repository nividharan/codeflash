import time
import os
import json
import re
import io
import random
import threading
import pyautogui
import pyperclip
import keyboard
from PIL import Image, ImageGrab
from google import genai
from google.genai import types

try:
    import winsound
except ImportError:
    winsound = None

pyautogui.PAUSE = 0.0
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

SUPPORTED_LANGUAGES = ["Java", "Python", "C++", "JavaScript", "TypeScript", "C#", "Go"]
TYPING_MODES = ["instant", "ultra", "human"]

# Fallback models in priority order
MODELS_TO_TRY = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-flash-lite-latest",
    "gemini-3.7-flash"
]

# Global state
state = {
    "language": "Java",
    "mode": "instant",
    "sound": True,
    "delay": 1.5,
    "is_busy": False
}


def play_sound(sound_type: str):
    if not winsound or not state.get("sound"):
        return
    try:
        if sound_type == "start":
            winsound.Beep(900, 100)
        elif sound_type == "success":
            winsound.Beep(1200, 80)
            time.sleep(0.04)
            winsound.Beep(1500, 120)
        elif sound_type == "switch":
            winsound.Beep(1100, 60)
        elif sound_type == "error":
            winsound.Beep(450, 200)
    except Exception:
        pass


def load_config():
    config = {
        "api_key": "",
        "target_language": "Java",
        "typing_mode": "instant",
        "sound_feedback": True,
        "paste_delay_seconds": 1.5,
        "hotkey_vision": "F7",
        "hotkey_solve": "F8",
        "hotkey_switch_lang": "F9",
        "hotkey_switch_mode": "F10"
    }

    if "GEMINI_API_KEY" in os.environ and os.environ["GEMINI_API_KEY"].strip():
        config["api_key"] = os.environ["GEMINI_API_KEY"].strip()

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                config.update(data)
        except Exception as e:
            print(f"[!] Warning reading config: {e}")

    # Synchronize loaded configuration with active runtime state
    if config.get("target_language") in SUPPORTED_LANGUAGES:
        state["language"] = config["target_language"]
    elif config.get("target_language", "").title() in SUPPORTED_LANGUAGES:
        state["language"] = config["target_language"].title()

    if config.get("typing_mode", "").lower() in TYPING_MODES:
        state["mode"] = config["typing_mode"].lower()

    state["sound"] = bool(config.get("sound_feedback", True))
    state["delay"] = float(config.get("paste_delay_seconds", 1.5))

    return config


def save_config(config: dict):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"[!] Could not save config: {e}")


def get_api_key(config: dict) -> str:
    if config.get("api_key"):
        return config["api_key"]

    key = input("Enter Gemini API Key: ").strip()
    if key:
        config["api_key"] = key
        save_config(config)
        return key
    return ""


def clean_code(raw_text: str, language: str = "") -> str:
    text = raw_text.strip()
    # Match markdown code fences like ```python\n...\n``` or ```java\n...\n```
    match = re.search(r"```[a-zA-Z0-9_\+\#-]*\s*\r?\n(.*?)\r?\n```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    match = re.search(r"```[a-zA-Z0-9_\+\#-]*\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    if text.startswith("```"):
        lines = text.splitlines()
        start = 1 if lines[0].startswith("```") else 0
        end = len(lines) - 1 if lines and lines[-1].strip().startswith("```") else len(lines)
        return "\n".join(lines[start:end]).strip()
    return text


def build_text_prompt(problem_text: str, language: str) -> str:
    return f"""You are an expert competitive programmer.
Solve the following coding problem in {language}.

Requirements:
1. Provide an optimal time and space complexity solution.
2. Provide ONLY valid {language} solution code suitable for LeetCode / competitive programming platforms (e.g. standard class/function signatures).
3. Do NOT include markdown explanations, intro/outro, or commentary. Output only raw {language} code.

Problem:
{problem_text}
"""


def build_vision_prompt(language: str) -> str:
    return f"""You are an expert competitive programmer.
Look at the attached screen image carefully. Identify and solve the coding challenge / algorithmic problem shown on the screen in {language}.

Requirements:
1. Provide an optimal time and space complexity solution.
2. Provide ONLY valid {language} solution code suitable for LeetCode / competitive programming platforms (e.g. standard class or function signatures).
3. Do NOT include any markdown explanations, commentary, intro/outro, or test harness. Output ONLY raw {language} code.
"""


def image_to_genai_part(img: Image.Image) -> types.Part:
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=85)
    return types.Part.from_bytes(data=buf.getvalue(), mime_type="image/jpeg")


def insert_code(code: str, mode: str):
    if mode == "instant":
        pyperclip.copy(code)
        time.sleep(0.05)
        pyautogui.hotkey("ctrl", "v")
    elif mode == "ultra":
        # Direct Unicode character typing (bypasses anti-paste clipboard hooks)
        keyboard.write(code, delay=0.003)
    elif mode == "human":
        # Cadence-based typing with natural jitter and pause after statements
        for char in code:
            keyboard.write(char)
            if char in ("\n", ";", "{", "}"):
                time.sleep(random.uniform(0.10, 0.25))
            elif char == " ":
                time.sleep(random.uniform(0.02, 0.06))
            else:
                time.sleep(random.uniform(0.015, 0.04))


def cycle_language():
    current_idx = SUPPORTED_LANGUAGES.index(state["language"])
    next_idx = (current_idx + 1) % len(SUPPORTED_LANGUAGES)
    state["language"] = SUPPORTED_LANGUAGES[next_idx]
    play_sound("switch")

    print("\n" + "=" * 50)
    print(f"🌐 [F9] TARGET LANGUAGE SWITCHED ➔ 【 {state['language']} 】")
    print("=" * 50 + "\n")


def cycle_mode():
    current_idx = TYPING_MODES.index(state["mode"])
    next_idx = (current_idx + 1) % len(TYPING_MODES)
    state["mode"] = TYPING_MODES[next_idx]
    play_sound("switch")

    mode_display = {
        "instant": "⚡ INSTANT (0.1s Clipboard Paste)",
        "ultra": "🚀 ULTRA (Keystroke Burst - Anti-Paste Bypass)",
        "human": "👤 HUMAN (Natural Typing Cadence with Jitter)"
    }

    print("\n" + "=" * 50)
    print(f"⚙️  [F10] TYPING PROFILE SWITCHED ➔ 【 {mode_display.get(state['mode'], state['mode'])} 】")
    print("=" * 50 + "\n")


def solve_with_gemini(client, contents, prompt_desc: str):
    lang = state["language"]
    mode = state["mode"]
    print(f"[⚡] Solving problem ({prompt_desc}) in {lang} using Gemini AI...")

    response = None
    last_error = None

    for model_name in MODELS_TO_TRY:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents,
            )
            if response and response.text:
                print(f"[✓] Solved using model: {model_name}")
                break
        except Exception as e:
            last_error = e
            continue

    if not response or not response.text:
        print(f"[!] Error generating solution across models: {last_error}")
        play_sound("error")
        return

    code = clean_code(response.text, lang)

    delay = state["delay"]
    print(f"[⚡] Solution ready! Inserting via [{mode.upper()}] mode into editor in {delay}s...")
    time.sleep(delay)

    insert_code(code, mode)
    play_sound("success")
    print(f"[✓] SUCCESS: {lang} solution inserted into editor via {mode.upper()} mode!\n")


def solve_text_worker(client):
    if state["is_busy"]:
        print("[!] Solver is already running. Please wait for current operation to finish.")
        return

    state["is_busy"] = True
    try:
        print("\n[⚡] F8 detected! Reading from clipboard...")
        play_sound("start")

        # 1. Check for text in clipboard
        question = pyperclip.paste().strip()
        if question and len(question) >= 5:
            prompt = build_text_prompt(question, state["language"])
            solve_with_gemini(client, prompt, prompt_desc="Text Mode")
            return

        # 2. If no text, check if clipboard contains an image (e.g. Win + Shift + S snip)
        try:
            cb_image = ImageGrab.grabclipboard()
            if isinstance(cb_image, Image.Image):
                print("[📸] Detected image in clipboard (Snipping Tool). Using Vision AI...")
                img_part = image_to_genai_part(cb_image)
                prompt = build_vision_prompt(state["language"])
                solve_with_gemini(client, [img_part, prompt], prompt_desc="Clipboard Snip Vision")
                return
        except Exception:
            pass

        print("[!] Clipboard is empty. Either:")
        print("    • Copy problem text (Ctrl + C), OR")
        print("    • Take a snip of problem (Win + Shift + S), OR")
        print("    • Press [ F7 ] to automatically capture full screen with Vision AI!")
        play_sound("error")

    except Exception as err:
        print(f"[!] Unexpected error during solve: {err}")
        play_sound("error")
    finally:
        state["is_busy"] = False


def solve_vision_worker(client):
    if state["is_busy"]:
        print("[!] Solver is already running. Please wait for current operation to finish.")
        return

    state["is_busy"] = True
    try:
        print("\n[📸] F7 detected! Capturing screen for Vision AI (No Copy Required)...")
        play_sound("start")

        screenshot = None
        try:
            screenshot = ImageGrab.grab()
        except Exception:
            # Fallback to clipboard image if direct grab failed
            try:
                cb_image = ImageGrab.grabclipboard()
                if isinstance(cb_image, Image.Image):
                    screenshot = cb_image
            except Exception:
                pass

        if not screenshot or not isinstance(screenshot, Image.Image):
            print("[!] Could not capture screen image. You can snip the problem with Win+Shift+S and press F8!")
            play_sound("error")
            return

        img_part = image_to_genai_part(screenshot)
        prompt = build_vision_prompt(state["language"])
        solve_with_gemini(client, [img_part, prompt], prompt_desc="Full Screen Vision")

    except Exception as err:
        print(f"[!] Unexpected error during vision solve: {err}")
        play_sound("error")
    finally:
        state["is_busy"] = False


def trigger_solve_text(client):
    threading.Thread(target=solve_text_worker, args=(client,), daemon=True).start()


def trigger_solve_vision(client):
    threading.Thread(target=solve_vision_worker, args=(client,), daemon=True).start()


def print_banner(config: dict):
    print("=" * 70)
    print(">> ⚡ CODEFLASH - UNIVERSAL AI COMPANION (TEXT & VISION) & TYPER")
    print("=" * 70)
    print(f"  • Current Language:      [ {state['language']} ]  (Press {config.get('hotkey_switch_lang', 'F9')} to switch)")
    print(f"  • Typing Profile:        [ {state['mode'].upper()} ]  (Press {config.get('hotkey_switch_mode', 'F10')} to switch)")
    print(f"  • Vision Solve (Screen): [ {config.get('hotkey_vision', 'F7')} ] ──▶ (Zero Copying Needed!)")
    print(f"  • Solve from Clipboard:  [ {config.get('hotkey_solve', 'F8')} ] ──▶ (Text or Win+Shift+S Snip)")
    print(f"  • Sound Feedback:        [ {'ON' if state['sound'] else 'OFF'} ]")
    print("-" * 70)
    print("How to use:")
    print("  ⭐ Option A (Copy Disabled?): Have problem on screen and press [ F7 ].")
    print("  ⭐ Option B (Snipped Image):   Snip with Win + Shift + S, then press [ F8 ].")
    print("  ⭐ Option C (Standard Text):   Copy text with Ctrl + C, then press [ F8 ].")
    print("=" * 70)
    print("Listening for hotkeys... (Press Ctrl+C in terminal to stop)\n")


def main():
    config = load_config()
    api_key = get_api_key(config)
    if not api_key:
        print("[!] No API key provided. Exiting.")
        return

    client = genai.Client(api_key=api_key)

    print_banner(config)

    hk_vision = config.get("hotkey_vision", "F7")
    hk_solve = config.get("hotkey_solve", "F8")
    hk_lang = config.get("hotkey_switch_lang", "F9")
    hk_mode = config.get("hotkey_switch_mode", "F10")

    keyboard.add_hotkey(hk_vision, lambda: trigger_solve_vision(client))
    keyboard.add_hotkey(hk_solve, lambda: trigger_solve_text(client))
    keyboard.add_hotkey(hk_lang, cycle_language)
    keyboard.add_hotkey(hk_mode, cycle_mode)

    try:
        keyboard.wait()
    except (KeyboardInterrupt, SystemExit):
        print("\n[!] CodeFlash stopped.")


if __name__ == "__main__":
    main()
