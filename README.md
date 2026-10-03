# ⚡ CodeFlash — AI-Powered Developer Productivity & Accessibility Engine

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/AI-Google%20Gemini%20Multimodal-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini AI" />
  <img src="https://img.shields.io/badge/OS%20Automation-Win32%20Keystroke%20Engine-FF6F00?style=for-the-badge" alt="OS Automation" />
  <img src="https://img.shields.io/badge/Languages-7%20Supported-00C7FF?style=for-the-badge" alt="Languages" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

**CodeFlash** is an open-source developer productivity and assistive automation engine engineered to bridge visual problem comprehension with instant, mathematically verified code synthesis. Built with **Google Gemini Multimodal Vision AI** and a **low-level OS keystroke streaming pipeline**, CodeFlash enables software engineers and researchers to prototype algorithms, automate repetitive programming tasks, and stream code directly into any desktop environment or remote terminal session.

---

## 🏗️ System Architecture

```text
┌───────────────────────┐       ┌────────────────────────┐
│ Visual Screen Capture │  ──▶  │   Google Gemini AI     │
│   (Hotkey: F7)        │       │  Multimodal Reasoning  │
└───────────────────────┘       └───────────┬────────────┘
                                            │
┌───────────────────────┐                   ▼
│   Clipboard Input     │  ──▶  ┌────────────────────────┐
│   (Hotkey: F8)        │       │    Syntax Sanitizer    │
└───────────────────────┘       │ & Class Tail Validator │
                                └───────────┬────────────┘
                                            │
                                            ▼
                                ┌────────────────────────┐
                                │   Keystroke Engine     │
                                │  • Instant Paste       │
                                │  • Direct OS Stream    │
                                │  • Human Cadence       │
                                └───────────┬────────────┘
                                            │
                                            ▼
                                ┌────────────────────────┐
                                │ Target Editor/Terminal │
                                │ (IDE, VM, Remote SSH)  │
                                └────────────────────────┘
```

---

## 🌟 Core Technical Highlights

### 1. 👁️ Multimodal Visual Comprehension
- Uses Google Gemini Multimodal Vision API to parse complex technical specifications, constraints, diagrams, and mathematical problem statements directly from active displays without requiring manual copying or OCR preprocessing.
- Operates in a **Clean-Room Isolation** mode: extracts core specifications while ignoring extraneous editor clutter, previous failed attempts, or UI noise.

### 2. 🌐 Multi-Language Architecture
CodeFlash supports dynamic, idiomatic code generation across 7 industry-standard languages: **Java, Python, C++, TypeScript, JavaScript, C#, and Go**, with automated numerical precision handling and platform-specific standard I/O streaming.

### 3. ⌨️ Low-Level OS Keystroke Automation
Designed for accessibility and developer productivity across diverse computing environments:
- **Instant Mode (`0.1s`)**: High-speed clipboard injection for standard editors.
- **Ultra Keystroke Streaming (~0.008s/char)**: Direct hardware-level keystroke emulation with **Trailing Space Auto-Bracket Neutralization (`{ `)** to bypass web editor auto-closing brace duplications. Ideal for remote desktop sessions, Citrix, SSH terminals, and virtual machines where host clipboard sharing is restricted.
- **Human Cadence Mode**: Generates natural typing cadences with randomized character delays and punctuation jitter for live demonstrations and testing.

### 4. 🛡️ Robust Code Sanitization Pipeline
- **Class Boundary Validator**: Preserves multi-class structures (e.g. auxiliary `Node`, `Pair`, or `Edge` classes alongside the main class) while stripping trailing markdown artifacts and syntax noise.
- **Auto-Bracket Neutralizer**: Automatically prevents race conditions and auto-closing bracket corruptions in web-based code editors (Ace, Monaco, CodeMirror).

---

## ⌨️ Hotkey Controls

| Hotkey | Action | Description |
| :--- | :--- | :--- |
| **`F6`** | **Visual Debug & Auto-Patch** | Captures code + error on screen, prints diagnosis & expected output, and in-place patches editor |
| **`F7`** | **Visual Screen Solve** | Captures active display, analyzes problem, and streams fresh code to active editor |
| **`F8`** | **Clipboard Solve** | Processes problem text (`Ctrl+C`) or snipped image (`Win+Shift+S`) from clipboard |
| **`F9`** | **Cycle Target Language** | Cycles through Java ➔ Python ➔ C++ ➔ JavaScript ➔ TypeScript ➔ C# ➔ Go |
| **`F10`** | **Cycle Typing Profile** | Cycles through Instant (Paste) ➔ Ultra (Direct Stream) ➔ Human Cadence |

---

## 🛠️ Quick Start

### 1. Prerequisites
- Python 3.8 or higher
- Google Gemini API Key ([Get one free from Google AI Studio](https://aistudio.google.com/))

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/nividharan/codeflash.git
cd codeflash

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Copy the configuration template and add your API key:
```bash
cp config.example.json config.json
```

Edit `config.json`:
```json
{
  "api_key": "YOUR_GEMINI_API_KEY_HERE",
  "target_language": "Java",
  "typing_mode": "ultra",
  "sound_feedback": true,
  "paste_delay_seconds": 1.5,
  "auto_clear_editor": true,
  "hotkey_debug": "F6",
  "hotkey_vision": "F7",
  "hotkey_solve": "F8",
  "hotkey_switch_lang": "F9",
  "hotkey_switch_mode": "F10"
}
```

> [!NOTE]
> `config.json` is protected in `.gitignore` to prevent confidential API keys from ever being committed to source control.

---

## 🚀 Running CodeFlash

### Launch the Background Assistant:
```bash
python smart_solver.py
```
1. Position your coding challenge or problem description on screen.
2. Click inside your destination code editor or terminal.
3. Press **`F7`** to solve from screen, or copy the problem text and press **`F8`**.
4. The verified solution will be automatically typed into your editor.

### Standalone Typer Utility:
To stream pre-existing code from `code.txt` without calling the AI:
```bash
python typer.py --mode instant   # High-speed clipboard injection
python typer.py --mode ultra     # Direct OS keystroke streaming
python typer.py --mode human     # Natural typing cadence simulation
```

---

## 📂 Repository Structure

```text
codeflash/
├── smart_solver.py      # Core multimodal AI engine, vision pipeline & keystroke streamer
├── typer.py             # Standalone cross-platform keystroke automation utility
├── config.example.json  # Configuration template
├── config.json          # Local credentials & runtime settings (gitignored)
├── requirements.txt     # Python package dependencies
└── README.md            # Technical documentation & architecture reference
```

---

## 📄 License
This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
