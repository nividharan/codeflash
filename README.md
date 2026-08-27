# ⚡ CodeFlash - Universal AI Code Companion & Instant Typer

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/AI-Gemini%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini AI" />
  <img src="https://img.shields.io/badge/Speed-Instant%20%26%20Ultra-FFD700?style=for-the-badge" alt="Speed" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

**CodeFlash** is a lightweight, background developer automation tool that instantly solves coding challenges and inserts optimal, judge-ready solutions into any code editor with a single global hotkey (**`F8`**).

---

## 🚀 How It Works

```text
[ Copy Problem (Ctrl+C) ] ──▶ [ Focus Code Editor ] ──▶ [ Press F8 ] ──▶ [ ✨ Instant Solution! ]
```

1. **Highlight & Copy (`Ctrl + C`)** any coding problem or algorithmic prompt.
2. **Click inside your code editor** (where your cursor is blinking).
3. **Press `F8`**: CodeFlash analyzes the problem, queries Gemini AI for the optimal solution, and inserts the formatted code directly into your editor in milliseconds.

---

## ✨ Key Features

- **🌐 100% Universal:** Works seamlessly with any web editor, IDE, and online judge environment.
- **🔄 Always-On Continuous Mode:** Runs quietly in the background—solve 50+ problems in a row without touching the terminal.
- **⚡ Multiple Speed Profiles:**
  - `Instant Mode`: Pastes formatted code in **0.1s flat**.
  - `Ultra Mode`: Rapid keystroke bursts (~0.005s per character).
  - `Human Mode`: Realistic typing cadence with variable pauses.
- **☕ Multi-Language Ready:** Default optimized for **Java**, with easy toggling for **Python**, **C++**, and **JavaScript**.
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

### 3. Configure Your Free API Key
Get a free API key from [Google AI Studio](https://aistudio.google.com) and add it to `config.json`:
```json
{
  "api_key": "YOUR_GEMINI_API_KEY_HERE"
}
```
*(If you do not create this file, the script will prompt you once on first startup and save it automatically).*

---

## 🎮 Usage

Start the background solver:
```bash
python smart_solver.py
```

### Keyboard Shortcuts:
| Action | Key / Command |
| :--- | :--- |
| **Solve & Insert Solution** | `F8` |
| **Copy Problem Statement** | `Ctrl + C` |
| **Stop Background Assistant** | `Ctrl + C` (in terminal) |

---

## 📂 Project Structure

```text
codeflash/
├── smart_solver.py      # Main AI solver with global F8 hotkey listener
├── typer.py             # Standalone high-speed code typer
├── requirements.txt     # Python package dependencies
├── config.example.json  # Template configuration file
├── .gitignore           # Keeps API keys & cache private
└── README.md            # Project documentation
```

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
