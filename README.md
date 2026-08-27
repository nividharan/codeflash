# CodeFlash ⚡ - Universal AI Code Companion & Instant Typer

A high-speed developer automation assistant that listens for a global hotkey (`F8`), captures coding problem statements or code prompts from your clipboard, generates optimal solutions using Gemini AI, and instantly types/pastes them into any code editor or online judge.

## ✨ Features
- **Universal Compatibility:** Works seamlessly across any web platform, browser coding environment, IDE, and online judge.
- **Always-On Continuous Mode:** Runs in the background and processes consecutive tasks without manual restarts.
- **Ultra-Fast & Human Typing Modes:** Switch between instant single-click pasting or customizable human-speed keystroke simulation.
- **Multi-Language Support:** Optimized by default for clean, judge-ready code (Java, Python, C++, etc.).

## 🚀 Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nividharan/codeflash.git
   cd codeflash
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key:**
   Get a free key from [Google AI Studio](https://aistudio.google.com) and create `config.json`:
   ```json
   {
     "api_key": "YOUR_GEMINI_API_KEY"
   }
   ```

## 🎮 Usage

1. Start the tool:
   ```bash
   python smart_solver.py
   ```
2. Copy (`Ctrl + C`) any problem description or prompt from anywhere.
3. Focus your target code editor.
4. Press **`F8`** on your keyboard.
5. Press `Ctrl + C` in the terminal when you wish to stop.
