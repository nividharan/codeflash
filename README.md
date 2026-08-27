# Universal LeetCode & Competitive Programming Auto-Solver ⚡

An automated Python assistant that listens for a global hotkey (`F8`), reads coding problem statements from your clipboard, uses Gemini AI to generate optimal Java solutions, and automatically types/pastes them into your code editor.

## Features
- **Universal:** Works on LeetCode, HackerRank, CodeChef, Codeforces, GeeksforGeeks, etc.
- **Continuous Mode:** Runs in the background and solves multiple questions sequentially without restarting.
- **Instant Insertion:** Inserts solutions into the active editor in milliseconds.
- **Target Language:** Optimized for clean, judge-ready Java code.

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/leetcode-auto-solver.git
   cd leetcode-auto-solver
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key:**
   Get a free API key from [Google AI Studio](https://aistudio.google.com) and create `config.json`:
   ```json
   {
     "api_key": "YOUR_GEMINI_API_KEY"
   }
   ```

## Usage

1. Start the solver:
   ```bash
   python smart_solver.py
   ```
2. Copy (`Ctrl + C`) any problem description on any website.
3. Click inside your Java code editor.
4. Press **`F8`** on your keyboard.
5. Press `Ctrl + C` in the terminal when you are done.
