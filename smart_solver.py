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

# Fallback models in priority order (active and tested on API)
MODELS_TO_TRY = [
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.7-flash"
]

# Global state
state = {
    "language": "Java",
    "mode": "ultra",
    "sound": True,
    "delay": 1.5,
    "auto_clear": True,
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
        "auto_clear_editor": True,
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
    state["auto_clear"] = bool(config.get("auto_clear_editor", True))

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
    
    # 1. Match all ``` code blocks and pick the largest one (the actual solution code)
    blocks = re.findall(r"```(?:[a-zA-Z0-9_\+\#-]*\s*\r?\n)?(.*?)\r?\n```", text, re.DOTALL)
    if blocks:
        best = max(blocks, key=lambda b: len(b.strip()))
        if len(best.strip()) > 10:
            text = best.strip()
    elif "```" in text:
        parts = text.split("```")
        if len(parts) >= 2:
            code_candidate = parts[1]
            lines = code_candidate.splitlines()
            if lines and not lines[0].strip().endswith(";"):
                lines = lines[1:]
            text = "\n".join(lines).strip()
    else:
        # Fallback: Find code start keyword if commentary is present
        lines = text.splitlines()
        start_idx = -1
        for i, line in enumerate(lines):
            l = line.strip()
            if l.startswith(("import ", "package ", "public class ", "class ", "#include", "def ", "using ")):
                start_idx = i
                break
        if start_idx != -1:
            text = "\n".join(lines[start_idx:]).strip()

    # 2. Remove multi-line block comments /* ... */
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)

    # 3. Filter out single-line comments (// and #) that the AI dumps its thought process into
    is_python = (language or state.get("language", "")).lower() == "python"
    clean_lines = []
    for line in text.splitlines():
        trimmed = line.strip()
        # Skip comment-only lines
        if trimmed.startswith("//") or trimmed.startswith("/*"):
            continue
        if is_python and trimmed.startswith("#"):
            continue
        clean_lines.append(line)

    # 4. For class-based languages (Java, C++, C#): Sanitize trailing garbage after the code closes
    is_class_lang = (language or state.get("language", "")).lower() in ("java", "c++", "c#", "cpp")
    if is_class_lang:
        brace_count = 0
        class_started = False
        final_lines = []
        for i, line in enumerate(clean_lines):
            stripped = line.strip()
            if not class_started and any(stripped.startswith(k) or f" {k}" in stripped for k in ("class ", "interface ", "struct ", "enum ")):
                class_started = True

            final_lines.append(line)

            if class_started:
                in_quote = False
                for ch in line:
                    if ch == '"':
                        in_quote = not in_quote
                    elif not in_quote:
                        if ch == '{':
                            brace_count += 1
                        elif ch == '}':
                            brace_count -= 1

                if brace_count == 0:
                    # Check if any remaining line contains a new class, struct, interface, or function
                    has_subsequent_code = False
                    for next_line in clean_lines[i + 1:]:
                        nl = next_line.strip()
                        if any(nl.startswith(kw) or f" {kw}" in nl for kw in ("class ", "interface ", "struct ", "enum ", "public ", "static ", "void ", "int ", "long ", "def ")):
                            has_subsequent_code = True
                            break
                    if not has_subsequent_code:
                        # Top-level code has finished! Cut off trailing markdown noise, stray brackets, or commentary
                        break
        clean_lines = final_lines

    return "\n".join(clean_lines).strip()


def get_language_specific_rules(language: str) -> str:
    lang = language.lower()
    if lang == "java":
        return """JAVA COMPILATION & PLATFORM RULES:
- Standard I/O (Talentely, TCS, Codeforces, MySlate): Use `public class Main` with `public static void main(String[] args)`. Use `Scanner` (`sc.hasNext()`, `sc.nextLong()`, `sc.nextInt()`).
- CoCubes: Use `class UserMainCode` with the exact method signature requested. Return result directly.
- LeetCode: Use `class Solution` with the exact method signature requested. Return result directly.
- HackerRank / GFG: Match the exact class/function name expected (e.g. `class Result` or solution function).
- 64-Bit Safety: Use `long` for sums, differences, products, and map keys (`TreeSet<Long>`, `HashMap<Long, Integer>`).
- Tree & Heap Roots: Return `Node` or `TreeNode` object pointer, NEVER primitive int."""
    elif lang in ("c++", "cpp"):
        return """C++ COMPILATION & PLATFORM RULES:
- Standard I/O: Include `#include <bits/stdc++.h>` and `using namespace std;`. Inside `int main()`, start with `ios_base::sync_with_stdio(false); cin.tie(NULL);` and end with `return 0;`.
- LeetCode: Use `class Solution { public: ... };`.
- Types: ALWAYS use `long long` for values, sums, products, and map keys to prevent 32-bit overflow.
- Modulo: Intermediate negative values must be `((a % MOD) + MOD) % MOD`.
- Floats: Output with `cout << fixed << setprecision(X)` matching sample output."""
    elif lang == "python":
        return """PYTHON EXECUTION & PLATFORM RULES:
- Standard I/O: `import sys; sys.setrecursionlimit(2000000)`. Read inputs with `tokens = sys.stdin.read().split()`.
- LeetCode: Use `class Solution: def methodName(self, ...):`.
- Division: Use `//` for integer division and `/` for floating point.
- Recursion: Always include `sys.setrecursionlimit(2000000)` for deep tree or graph traversals."""
    elif lang in ("javascript", "typescript"):
        return """JAVASCRIPT / TYPESCRIPT RULES:
- Standard I/O: `const fs = require('fs'); const tokens = fs.readFileSync(0, 'utf-8').trim().split(/\\s+/);`.
- LeetCode: Use the exact function signature or `class Solution`.
- Precision: Use `BigInt` for large integer calculations exceeding 2^53 - 1."""
    elif lang == "c#":
        return """C# COMPILATION RULES:
- Standard I/O: `using System; using System.Collections.Generic; class Program { static void Main(string[] args) { ... } }`.
- LeetCode: `public class Solution { public ... }`.
- Types: Use `long` (Int64) for large values."""
    elif lang == "go":
        return """GO COMPILATION RULES:
- Standard I/O: `package main\nimport ("bufio"\n"fmt"\n"os")\nfunc main() { scanner := bufio.NewScanner(os.Stdin); scanner.Split(bufio.ScanWords); ... }`.
- Types: Use `int64`."""
    return ""


def build_text_prompt(problem_text: str, language: str) -> str:
    lang_rules = get_language_specific_rules(language)
    return f"""You are an expert competitive programmer.
Solve the following coding challenge in {language}.

{lang_rules}

UNIVERSAL ZERO-ERROR EXECUTION DIRECTIVES:

1. DIRECTIONAL, RANK & EXTREMUM ACCURACY:
   - Carefully distinguish LARGEST / MAXIMUM / HIGHEST vs SMALLEST / MINIMUM / LOWEST:
     * SECOND LARGEST / 2nd MAXIMUM: In TreeSet/SortedSet, largest is `last()`, second largest is `lower(last())` or remove `pollLast()` and take `last()`. NEVER call `pollFirst()` (which removes the minimum)!
     * SECOND SMALLEST / 2nd MINIMUM: In TreeSet/SortedSet, smallest is `first()`, second smallest is `higher(first())` or remove `pollFirst()` and take `first()`.
   - DUPLICATES & DISTINCT ELEMENTS: For "second largest" or "second smallest", duplicates of the maximum/minimum do NOT count as the second element (e.g. `[2, 2, 2, 2]` has NO second largest -> print `-1`). If distinct elements < 2, return / print `-1`.
   - NEGATIVE VALUES DEFENSE: NEVER initialize extremum trackers to 0. If all inputs are negative (e.g. `[-5, -12, -3]`), initializing to 0 corrupts the answer! Always initialize extremum trackers to negative infinity (`Long.MIN_VALUE`, `LLONG_MIN`, `-float('inf')`).
   - PRIORITY QUEUES: Default is MIN-HEAP. For Max-Heap, you MUST use a reverse comparator!
   - SORTING: Ascending sort places minimum at index 0 and maximum at index `n - 1`.

2. DATA STRUCTURE & RETURN TYPE ACCURACY:
   - TREE & HEAP: If returning a tree root (e.g. `CreateHeap`, `buildTree`, `invertTree`), return the root `Node` / `TreeNode` object, NEVER a raw integer or array! Build complete binary tree (`left = 2*i + 1`, `right = 2*i + 2`).
   - LINKED LIST: If returning a list head (e.g. `reverseList`, `mergeTwoLists`), return the head `ListNode` / `Node` object, NEVER a raw integer or array!
   - ARRAYS & COLLECTIONS: Return the exact type expected (`int[]`, `List<Integer>`, `String[]`).

3. NUMERICAL OVERFLOW & PRECISION SAFETY:
   - ALWAYS use 64-bit integers (`long` in Java/C#, `long long` in C++) for sums, products, differences, and Map keys whenever constraints reach 10^5 or negative numbers exist, to completely prevent 32-bit integer overflow/underflow!
   - MODULO ARITHMETIC: When problem asks for modulo (e.g. `10^9 + 7` or `1000000007`), apply `% 1000000007L` at every intermediate addition and multiplication step. For subtraction: `(a % MOD - b % MOD + MOD) % MOD`.
   - LCM OVERFLOW: Calculate `(a / gcd(a, b)) * b`, NEVER `(a * b) / gcd(a, b)`.
   - BINARY SEARCH: Calculate midpoint as `mid = low + (high - low) / 2` to prevent overflow.

4. CATEGORY-SPECIFIC SAFEGUARDS:
   - DYNAMIC PROGRAMMING: Size DP arrays `n + 1` or `(n + 1) x (m + 1)` to prevent out-of-bounds on 1-indexed constraints. Explicitly initialize base cases.
   - GRAPHS: Check if vertices are 1-based or 0-based. If 1-based, size adjacency list to `n + 1`.
   - STRINGS: Respect boundary slicing (e.g. Java `substring` end is exclusive). Count character frequencies with arrays or maps.

5. ROBUST MULTI-LINE INPUT & OUTPUT MATCHING:
   - For Java Standard I/O, use `java.util.Scanner` (`sc.nextInt()`, `sc.nextLong()`, `sc.next()`, `sc.hasNext()`) which seamlessly processes numbers split across multiple lines, blank lines, and trailing spaces without crashing.
   - Always guard input loops with `sc.hasNext()` to prevent `NoSuchElementException` on empty or malformed inputs.
   - Output format: Match sample output spacing (e.g. space-separated `ans1 + " " + ans2` vs newline-separated) exactly.

6. OPTIMAL COMPLEXITY (TLE PREVENTION) & EDGE CASES:
   - Choose optimal O(N) or O(N log N) algorithms to prevent Time Limit Exceeded (TLE).
   - Guard against edge cases: empty array (n=0), single element (n=1), negative numbers, all elements equal, target not found.

7. MENTAL DRY-RUN VERIFICATION:
   - Mentally trace your solution step-by-step against Sample 1, Sample 2, and edge cases before outputting.
   - Ensure the logic outputs the EXACT sample outputs without off-by-one errors or inverted logic.

STRICT CONSTRAINTS:
- Do NOT write ANY comments (no `//` or `/* */`).
- Do NOT write any explanations, markdown notes, or walkthroughs.
- Output ONLY the pure source code inside ```{language.lower()} ```.

Problem:
{problem_text}
"""


def build_vision_prompt(language: str) -> str:
    lang_rules = get_language_specific_rules(language)
    return f"""You are an expert competitive programmer.
Look at the attached screen image carefully. Identify and solve the coding challenge shown on the screen in {language}.

{lang_rules}

UNIVERSAL ZERO-ERROR EXECUTION DIRECTIVES:

1. CLEAN-ROOM VISION ISOLATION & DRY-RUN:
   - IGNORE any pre-existing code, failed attempts, or starter snippets visible in the web editor/IDE area of the image.
   - Formulate the solution strictly from the Problem Statement, Input/Output specifications, Constraints, and Sample Cases.
   - Mentally verify against visible Sample 1 and Sample 2 to guarantee 100% correct outputs before generating.

2. DIRECTIONAL, RANK & EXTREMUM ACCURACY:
   - Carefully distinguish LARGEST / MAXIMUM / HIGHEST vs SMALLEST / MINIMUM / LOWEST:
     * SECOND LARGEST / 2nd MAXIMUM: In TreeSet/SortedSet, largest is `last()`, second largest is `lower(last())` or remove `pollLast()` and take `last()`. NEVER call `pollFirst()` (which removes the minimum)!
     * SECOND SMALLEST / 2nd MINIMUM: In TreeSet/SortedSet, smallest is `first()`, second smallest is `higher(first())` or remove `pollFirst()` and take `first()`.
   - DUPLICATES & DISTINCT ELEMENTS: For "second largest" or "second smallest", duplicates of the maximum/minimum do NOT count as the second element (e.g. `[2, 2, 2, 2]` has NO second largest -> print `-1`). If distinct elements < 2, return / print `-1`.
   - NEGATIVE VALUES DEFENSE: NEVER initialize extremum trackers to 0. If all inputs are negative (e.g. `[-5, -12, -3]`), initializing to 0 corrupts the answer! Always initialize extremum trackers to negative infinity (`Long.MIN_VALUE`, `LLONG_MIN`, `-float('inf')`).
   - PRIORITY QUEUES: Default is MIN-HEAP. For Max-Heap, you MUST use a reverse comparator!
   - SORTING: Ascending sort places minimum at index 0 and maximum at index `n - 1`.

3. DATA STRUCTURE & RETURN TYPE ACCURACY:
   - TREE & HEAP: If returning a tree root (e.g. `CreateHeap`, `buildTree`, `invertTree`), return the root `Node` / `TreeNode` object, NEVER a raw integer or array! Build complete binary tree (`left = 2*i + 1`, `right = 2*i + 2`).
   - LINKED LIST: If returning a list head (e.g. `reverseList`, `mergeTwoLists`), return the head `ListNode` / `Node` object, NEVER a raw integer or array!
   - ARRAYS & COLLECTIONS: Return the exact type expected (`int[]`, `List<Integer>`, `String[]`).

4. NUMERICAL OVERFLOW & PRECISION SAFETY:
   - ALWAYS use 64-bit integers (`long` in Java/C#, `long long` in C++) for sums, products, differences, and Map keys whenever constraints reach 10^5 or negative numbers exist, to completely prevent 32-bit integer overflow/underflow!
   - MODULO ARITHMETIC: When problem asks for modulo (e.g. `10^9 + 7` or `1000000007`), apply `% 1000000007L` at every intermediate addition and multiplication step. For subtraction: `(a % MOD - b % MOD + MOD) % MOD`.
   - LCM OVERFLOW: Calculate `(a / gcd(a, b)) * b`, NEVER `(a * b) / gcd(a, b)`.
   - BINARY SEARCH: Calculate midpoint as `mid = low + (high - low) / 2` to prevent overflow.

5. CATEGORY-SPECIFIC SAFEGUARDS:
   - DYNAMIC PROGRAMMING: Size DP arrays `n + 1` or `(n + 1) x (m + 1)` to prevent out-of-bounds on 1-indexed constraints. Explicitly initialize base cases.
   - GRAPHS: Check if vertices are 1-based or 0-based. If 1-based, size adjacency list to `n + 1`.
   - STRINGS: Respect boundary slicing (e.g. Java `substring` end is exclusive). Count character frequencies with arrays or maps.

6. ROBUST MULTI-LINE INPUT & OUTPUT MATCHING:
   - For Java Standard I/O, use `java.util.Scanner` (`sc.nextInt()`, `sc.nextLong()`, `sc.next()`, `sc.hasNext()`) which seamlessly processes numbers split across multiple lines, blank lines, and trailing spaces without crashing.
   - Always guard input loops with `sc.hasNext()` to prevent `NoSuchElementException` on empty or malformed inputs.
   - Output format: Match sample output spacing (e.g. space-separated `ans1 + " " + ans2` vs newline-separated) exactly.

7. OPTIMAL COMPLEXITY (TLE PREVENTION) & EDGE CASES:
   - Choose optimal O(N) or O(N log N) algorithms to prevent Time Limit Exceeded (TLE).
   - Guard against edge cases: empty array (n=0), single element (n=1), negative numbers, all elements equal, target not found.

STRICT CONSTRAINTS:
- Do NOT write ANY comments (no `//` or `/* */`).
- Do NOT write any explanations, markdown notes, or walkthroughs.
- Output ONLY the pure source code inside ```{language.lower()} ```.
"""


def image_to_genai_part(img: Image.Image) -> types.Part:
    max_dimension = 1280
    w, h = img.size
    if max(w, h) > max_dimension:
        scale = max_dimension / max(w, h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=75, optimize=True)
    return types.Part.from_bytes(data=buf.getvalue(), mime_type="image/jpeg")


def insert_code(code: str, mode: str):
    # Ensure clipboard also has the code as backup
    try:
        pyperclip.copy(code)
    except Exception:
        pass
    time.sleep(0.04)

    # 1. Clear existing template code in the editor completely
    if state.get("auto_clear", True):
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.08)
        pyautogui.press("backspace")
        time.sleep(0.04)
        pyautogui.press("delete")
        time.sleep(0.06)

    # 2. Insert code based on selected mode
    if mode == "instant":
        # Fast atomic paste (for sites that allow Ctrl+V)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.04)

    elif mode == "ultra":
        # Ultra Keystroke Engine: Trailing space neutralizer prevents Ace auto-bracket on Enter
        lines = [l.strip() for l in code.splitlines() if l.strip()]
        lang = state.get("language", "Java").lower()
        is_brace_lang = lang in ("java", "c++", "c", "c#", "javascript", "typescript")

        for i, line in enumerate(lines):
            # In Ace editor, appending a trailing space after '{' ensures prevChar != '{' on Enter,
            # which completely bypasses Ace's auto-bracket insertion with 0 race conditions!
            content = (line + " ") if (is_brace_lang and line.endswith("{")) else line

            keyboard.write(content, delay=0.008, exact=True)
            time.sleep(0.04)

            if i < len(lines) - 1:
                keyboard.send("enter")
                time.sleep(0.08)

    elif mode == "human":
        # Realistic Human Keystroke Engine: Trailing space neutralizer prevents Ace auto-bracket
        lines = [l.strip() for l in code.splitlines() if l.strip()]
        lang = state.get("language", "Java").lower()
        is_brace_lang = lang in ("java", "c++", "c", "c#", "javascript", "typescript")

        for i, line in enumerate(lines):
            content = (line + " ") if (is_brace_lang and line.endswith("{")) else line

            for char in content:
                keyboard.write(char, exact=True)
                if char in (";", "{", "}", "(", ")", "[", "]", ":"):
                    time.sleep(random.uniform(0.12, 0.25))
                elif char == " ":
                    time.sleep(random.uniform(0.06, 0.14))
                elif char in (",", ".", "=", "+", "-", "*", "/", ">", "<"):
                    time.sleep(random.uniform(0.08, 0.18))
                else:
                    time.sleep(random.uniform(0.035, 0.085))

                if random.random() < 0.03:
                    time.sleep(random.uniform(0.20, 0.45))

            time.sleep(0.05)
            if i < len(lines) - 1:
                keyboard.send("enter")
                time.sleep(random.uniform(0.20, 0.45))


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
        "ultra": "🚀 ULTRA (High-Speed Direct Keystroke Emulation)",
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

    gen_config = types.GenerateContentConfig(
        temperature=0.0,
        max_output_tokens=4096,
        system_instruction=f"You are an expert competitive programmer. Solve the problem in {lang}. You must ONLY output the {lang} source code inside a single ```{lang.lower()} ``` code block. Do NOT write any explanations, thinking steps, mathematical scratchpad notes, sample walkthroughs, or commentary. NEVER write any comments (no `//` or `/* */`) in the code. Output pure executable statements only."
    )

    for i, model_name in enumerate(MODELS_TO_TRY):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=gen_config
            )
            if response and response.text:
                if i > 0:
                    MODELS_TO_TRY.insert(0, MODELS_TO_TRY.pop(i))
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
    print(">> ⚡ CODEFLASH - MULTIMODAL AI PAIR PROGRAMMER & KEYSTROKE AUTOMATION ENGINE")
    print("=" * 70)
    print(f"  • Current Language:      [ {state['language']} ]  (Press {config.get('hotkey_switch_lang', 'F9')} to switch)")
    print(f"  • Typing Profile:        [ {state['mode'].upper()} ]  (Press {config.get('hotkey_switch_mode', 'F10')} to switch)")
    print(f"  • Vision Solve (Screen): [ {config.get('hotkey_vision', 'F7')} ] ──▶ (Zero Copying Needed!)")
    print(f"  • Solve from Clipboard:  [ {config.get('hotkey_solve', 'F8')} ] ──▶ (Text or Win+Shift+S Snip)")
    print(f"  • Auto-Replace Editor:   [ {'ON' if state['auto_clear'] else 'OFF'} ]")
    print(f"  • Sound Feedback:        [ {'ON' if state['sound'] else 'OFF'} ]")
    print("-" * 70)
    print("How to use:")
    print("  ⭐ Option A (Screen Reading):  Have problem on screen and press [ F7 ].")
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

    keyboard.add_hotkey(hk_vision, lambda: trigger_solve_vision(client), suppress=True)
    keyboard.add_hotkey(hk_solve, lambda: trigger_solve_text(client), suppress=True)
    keyboard.add_hotkey(hk_lang, cycle_language, suppress=True)
    keyboard.add_hotkey(hk_mode, cycle_mode, suppress=True)

    try:
        keyboard.wait()
    except (KeyboardInterrupt, SystemExit):
        print("\n[!] CodeFlash stopped.")


if __name__ == "__main__":
    main()
