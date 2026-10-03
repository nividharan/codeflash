# ⚡ CodeFlash: Multimodal AI Algorithmic Pair Programmer

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/AI-Google%20Gemini%20Multimodal-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini AI" />
  <img src="https://img.shields.io/badge/Speed-Rapid%20Keystroke%20Automation-FFD700?style=for-the-badge" alt="Speed" />
  <img src="https://img.shields.io/badge/Languages-7%20Supported-00C7FF?style=for-the-badge" alt="Languages" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

CodeFlash is an open-source multimodal developer productivity tool designed for competitive programming practice, algorithmic interview preparation, and rapid software prototyping. It bridges visual problem comprehension with high-speed automated code generation across multiple languages.

---

## ✨ Key Features

- **📸 Multimodal Visual Understanding (`F7`)**: Captures algorithmic challenges directly from your screen using Google Gemini Vision AI—no manual copy-pasting required.
- **📋 Clipboard Solver (`F8`)**: Instantly solves problems from copied text (`Ctrl + C`) or Snipping Tool screenshots (`Win + Shift + S`).
- **🌐 7 Programming Languages (`F9`)**: Switch on the fly between **Java, Python, C++, JavaScript, TypeScript, C#, and Go**.
- **🛡️ Built-in Zero-Error Algorithmic Directives**:
  - 64-bit numerical overflow protection (`long` in Java/C#, `long long` in C++).
  - Directional rank accuracy (distinguishes *second largest* vs *second smallest*, reverse comparator for Max-Heaps).
  - Proper data structure return fidelity (`Node`/`TreeNode`/`ListNode` object references).
  - Modulo arithmetic negative handling `((a % MOD) + MOD) % MOD`.
- **⌨️ Universal Keystroke Injection Engine (`F10`)**:
  - `Instant Mode`: Fast clipboard injection (`0.1s`).
  - `Ultra Mode`: Direct OS keystroke streaming (~0.008s/char) compatible with remote desktops, SSH sessions, virtual machines, and secure IDEs where clipboard sharing is restricted.
  - `Human Mode`: Realistic typing cadence with natural micro-delays for live demonstrations.
- **🔊 Subtle Audio Cues**: Distinct system chimes alert you when problem solving begins and when typing finishes.

---

## ⌨️ Shortcuts Reference

| Shortcut | Action | Description |
| :--- | :--- | :--- |
| **`F7`** | **Visual Screen Solve** | Reads problem from active display and streams code to editor |
| **`F8`** | **Clipboard Solve** | Reads copied text or Snipping Tool screenshot |
| **`F9`** | **Cycle Target Language** | Java ➔ Python ➔ C++ ➔ JavaScript ➔ TypeScript ➔ C# ➔ Go |
| **`F10`** | **Cycle Typing Profile** | Instant (0.1s Paste) ➔ Ultra (Direct Keystroke Streamer) ➔ Human Cadence |

---

## 🛠️ Installation & Setup

### 1. Clone & Navigate
```bash
git clone https://github.com/nividharan/codeflash.git
cd codeflash
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Gemini API Key
Add your Google AI Studio API key to `config.json`:
```json
{
  "api_key": "YOUR_GEMINI_API_KEY_HERE",
  "target_language": "Java",
  "typing_mode": "ultra",
  "sound_feedback": true,
  "paste_delay_seconds": 1.5,
  "auto_clear_editor": true,
  "hotkey_vision": "F7",
  "hotkey_solve": "F8",
  "hotkey_switch_lang": "F9",
  "hotkey_switch_mode": "F10"
}
```

---

## 🚀 Usage

### Run CodeFlash Assistant:
```bash
python smart_solver.py
```

### Standalone Code Typer (Without AI):
Type pre-saved code from `code.txt` directly into any editor:
```bash
python typer.py --mode instant   # High-speed clipboard paste
python typer.py --mode ultra     # Direct OS keystroke streaming
python typer.py --mode human     # Natural typing cadence
```

---

## 📂 Project Architecture

```text
codeflash/
├── smart_solver.py      # Main AI Pair Programmer (Vision + Text AI + Hotkey Listener)
├── typer.py             # Standalone OS Keystroke Automation Engine
├── config.example.json  # Example configuration template
├── config.json          # Local configuration & API key (gitignored)
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
```

---

## 📄 License
Distributed under the MIT License.
