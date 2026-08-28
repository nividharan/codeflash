# ⚡ CodeFlash - Universal AI Code Companion & Instant Typer (Text + Vision)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/AI-Gemini%20Flash%20Vision-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini AI" />
  <img src="https://img.shields.io/badge/Speed-Instant%20%26%20Ultra-FFD700?style=for-the-badge" alt="Speed" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

**CodeFlash** is a lightweight, background developer automation tool that instantly solves coding challenges and inserts optimal, judge-ready solutions into any code editor with global hotkeys (**`F7`** for Vision Screen Capture, **`F8`** for Clipboard Solve).

---

## 🚀 How It Works

### Option A: When Copying is Disabled (Vision Screen AI)
```text
[ Problem on Screen ] ──▶ [ Focus Code Editor ] ──▶ [ Press F7 ] ──▶ [ 📸✨ Instant Vision Solution! ]
```
1. Have the coding problem visible on your screen.
2. Click inside your code editor window.
3. Press **`F7`**: CodeFlash captures your screen, analyzes the question using Gemini Vision, and types the optimal solution directly into your editor—**no copying required!**

---

### Option B: Standard Clipboard Solve
```text
[ Copy Problem (Ctrl+C / Win+Shift+S) ] ──▶ [ Focus Code Editor ] ──▶ [ Press F8 ] ──▶ [ ⚡ Solution Pasted! ]
```
1. **Highlight & Copy (`Ctrl + C`)** text, OR **Snip a box (`Win + Shift + S`)**.
2. **Click inside your code editor**.
3. **Press `F8`**: CodeFlash solves the problem and inserts the code.

---

## ✨ Key Features

- **📸 Vision AI (No Copy Required):** Uses Gemini Multimodal Vision to solve problems even on locked-down assessment pages where text selection and `Ctrl+C` are blocked.
- **🌐 100% Universal:** Works seamlessly with any web editor, IDE, and online assessment platform.
- **⚡ 3 Typing Speed Profiles:**
  - `Instant Mode`: Pastes formatted code in **0.1s flat** via clipboard shortcuts.
  - `Ultra Mode`: High-speed Unicode keystrokes (~0.003s/char) to **bypass anti-paste restrictions**.
  - `Human Mode`: Realistic typing cadence with natural micro-delays and punctuation pauses.
  - *Toggle anytime with **`F10`**!*
- **☕ Multi-Language Ready:** Switch between **Java, Python, C++, JavaScript, TypeScript, C#, and Go** on the fly with **`F9`**.
- **🔊 Subtle Audio Cues:** Sound feedback alerts you when a solution is being generated and when it finishes inserting.
- **🔒 Privacy First:** API keys are stored locally in `.gitignore` and never committed or uploaded.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/nividharan/codeflash.git
cd codeflash
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Your API Key & Preferences
Add your key to `config.json`:
```json
{
  "api_key": "YOUR_GEMINI_API_KEY_HERE",
  "target_language": "Java",
  "typing_mode": "instant",
  "sound_feedback": true,
  "paste_delay_seconds": 1.5,
  "hotkey_vision": "F7",
  "hotkey_solve": "F8",
  "hotkey_switch_lang": "F9",
  "hotkey_switch_mode": "F10"
}
```

---

## 🎮 Usage

Start the background solver:
```bash
python smart_solver.py
```

### Keyboard Shortcuts:
| Action | Key / Command | Description |
| :--- | :--- | :--- |
| **Vision Solve (Screen)** | `F7` | **Zero-copy**: Captures screen & uses Vision AI to solve directly |
| **Solve from Clipboard** | `F8` | Reads copied text (`Ctrl+C`) or snipped image (`Win+Shift+S`) |
| **Cycle Target Language** | `F9` | Cycles through Java ➔ Python ➔ C++ ➔ JS ➔ TS ➔ C# ➔ Go |
| **Cycle Typing Profile** | `F10` | Cycles through Instant ➔ Ultra (Anti-Paste) ➔ Human |
| **Stop Background Assistant** | `Ctrl + C` | In the terminal window |

---

## 🧪 Standalone Typer

Type out code already saved in `code.txt` without calling the AI:
```bash
python typer.py --mode instant   # Fast paste
python typer.py --mode ultra     # Anti-paste bypass
python typer.py --mode human     # Natural typing simulation
```

---

## 📂 Project Structure

```text
codeflash/
├── smart_solver.py      # Main AI solver (Vision Screen AI + Text + F7/F8/F9/F10 hotkeys)
├── typer.py             # Standalone high-speed code typer with multi-profile support
├── requirements.txt     # Python package dependencies
├── config.example.json  # Template configuration file
├── config.json          # Your local config & API key (gitignored)
├── .gitignore           # Keeps API keys & cache private
└── README.md            # Project documentation
```

---

## 📄 License
Distributed under the MIT License.
