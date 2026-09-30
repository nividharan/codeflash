# ⚡ CodeFlash & NPTEL AI HUD Overlay

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/AI-Gemini%20Flash%20Vision-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini AI" />
  <img src="https://img.shields.io/badge/UI-HUD%20Glassmorphic%20Overlay-00C7FF?style=for-the-badge" alt="HUD Overlay" />
  <img src="https://img.shields.io/badge/Speed-Instant%20AI%20Solver-FFD700?style=for-the-badge" alt="Speed" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

A powerful dual-mode AI automation suite:
1. **⚡ NPTEL AI HUD Overlay (`nptel_hud.py`)**: A floating, semi-transparent Heads-Up Display that overlays your browser screen, instantly analyzing and solving NPTEL assignment questions (MCQ, MSQ, NAT, True/False) with high-contrast answers, formula breakdowns, and step-by-step reasoning.
2. **💻 CodeFlash Typer (`smart_solver.py`)**: Universal AI companion that captures coding problems and types optimal solutions directly into any IDE/editor.

---

## 🎯 1. NPTEL AI HUD Overlay Screen (`nptel_hud.py`)

A cyberpunk/dark-glassmorphic HUD designed specifically for online assignments and assessments.

```text
[ NPTEL Question on Screen ] ──▶ [ Press F6 to Drag Snip ] ──▶ [ ⚡ Instant Answers & Derivations in HUD! ]
```

### ✨ NPTEL HUD Key Features
- **🛡️ Anti-Screen-Recording Guard (100% Invisible to Capture)**: Uses native Windows `SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)`. The HUD and Snip overlay are **completely excluded** from OBS Studio, Zoom, MS Teams, Google Meet, Loom, browser WebRTC screen recorders, and exam proctoring tools! Only YOU see the HUD on your physical monitor—recorded videos or screen shares show only your browser!
- **👻 Ghost Stealth Mode (`F3`)**: Turns the entire HUD background 100% transparent (`-transparentcolor`). Hides borders and controls, leaving ONLY floating answer text on screen.
- **🖱️ Click-Through Mode (`Ctrl+F3`)**: Mouse clicks pass straight through the HUD to underlying checkboxes/buttons on the webpage so you can interact with the exam without moving the HUD.
- **🎯 Multi-Select (MSQ) & MCQ Accuracy**: Recognizes checkboxes `[ ]` vs radio buttons `( )`, evaluating each option independently to show exact options (e.g. `[A, C] (Multi-Select)`).
- **📐 Formula & Step-by-Step Rationale**: Shows key formulas, derivations, and breakdown for each option.
- **✂️ Interactive Drag Snip (`F6`)**: Drag a selection box over any question on your browser (both the box and HUD are invisible on screen recordings!).
- **📸 Fullscreen Vision AI (`F7`)**: One-tap full screen solve.
- **📋 Clipboard Solver (`F8`)**: Reads copied text (`Ctrl+C`) or snipped image (`Win+Shift+S`).
- **👁️ Stealth Panic Hotkey (`F4` or `Esc`)**: Instantly hides/reveals the HUD overlay.
- **◀ ▶ History Stack**: Browse through all solved questions in your session.

### 🎮 Running NPTEL HUD
```bash
python nptel_hud.py
```

### ⌨️ NPTEL HUD Shortcuts
| Hotkey | Action | Description |
| :--- | :--- | :--- |
| **`F6`** | **Interactive Drag Snip** | Drag a bounding box over any question on your screen *(Recommended)* |
| **`F7`** | **Fullscreen Vision Solve** | Captures screen & uses Gemini Vision AI |
| **`F8`** | **Clipboard Solve** | Reads copied text (`Ctrl+C`) or snipped image (`Win+Shift+S`) |
| **`F3`** | **Toggle Ghost Stealth Mode** | Hides HUD background; shows **ONLY floating answer text** on screen |
| **`Ctrl + F3`** | **Toggle Click-Through** | Allows mouse clicks to pass straight through HUD to the webpage |
| **`F2`** | **Toggle Anti-Capture Guard** | Toggles hardware protection against screen recorders / OBS / Zoom |
| **`F4`** / **`Esc`** | **Toggle HUD Hide / Show** | Instant stealth toggle to show or hide the overlay |
| *Click Titlebar* | **Drag HUD** | Move HUD anywhere on screen |

---

## 💻 2. CodeFlash Coding Assistant (`smart_solver.py`)

For coding challenges (LeetCode, HackerRank, College IDEs). Solves algorithmic problems and types the code into your editor.

```bash
python smart_solver.py
```

### Keyboard Shortcuts:
| Action | Key | Description |
| :--- | :--- | :--- |
| **Vision Solve (Screen)** | `F7` | Captures screen & types solution into active code editor |
| **Clipboard Solve** | `F8` | Reads copied text or Snipping Tool image |
| **Cycle Target Language** | `F9` | Java ➔ Python ➔ C++ ➔ JavaScript ➔ TypeScript ➔ C# ➔ Go |
| **Cycle Typing Profile** | `F10` | Instant (0.1s Paste) ➔ Ultra (Anti-Paste Bypass) ➔ Human Cadence |

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
Add your API key to `config.json`:
```json
{
  "api_key": "YOUR_GEMINI_API_KEY_HERE",
  "sound_feedback": true,
  "hotkey_snip": "F6",
  "hotkey_vision": "F7",
  "hotkey_solve": "F8",
  "hotkey_toggle_hud": "F4",
  "hud_opacity": 0.94,
  "hud_always_on_top": true,
  "hud_compact_mode": false
}
```

---

## 📂 Workspace Structure

```text
codeflash/
├── carrom_aim_overlay/     # 📱 Carrom Live Aim Overlay & Vision Bot (Scrcpy, OpenCV Detection, Transparent HUD)
│   ├── start_scrcpy_with_overlay.bat # 🚀 One-click launcher: scrcpy mirror + transparent overlay
│   ├── carrom_overlay.py   # Transparent Win32 HUD with live trajectory prediction
│   ├── detect.py           # OpenCV board & coin detection
│   ├── solver.js           # Bridge into physics.js auto-aim solver
│   ├── scrcpy-win64-v2.7/  # Android screen mirroring
│   └── README.md           # Live aim overlay guide & hotkeys
│
├── carrom_theme_studio/    # 🎯 Carrom Theme Studio (HTML5/Canvas Web App, Miniclip Digital Physics, 1:1 Canvas, Auto-Aim)
│   ├── css/                # Responsive 1:1 board styling & 4 themes (Tribal, Cyber, Minimalist, Vintage)
│   ├── js/                 # physics.js, board_renderer.js, app.js, physics_bridge.js
│   ├── test/               # Verification test suites & empirical benchmarks
│   └── README.md           # Developer & manual customization guide
│
├── carrom_python_labs/     # 🎱 Carrom Python Physics Laboratories & Tools
│   ├── carrom_game.py      # Pygame 2D Carrom Game
│   ├── carrom_physics_lab.py # Gravitational physics laboratory
│   ├── carrom_themes.py    # Visual themes engine
│   ├── chain_collision_lab.py # Multi-piece chain collision visualizer
│   ├── elastic_carrom_lab.py  # 2D elastic collision experimenter
│   ├── vector_space_lab.py # Vector reflection forecasting
│   ├── screen_ruler.py     # Transparent precision screen ruler & protractor
│   └── README.md           # Python labs guide
│
├── mobile/                 # 💳 Nova Mobile Application (React Native / Expo)
├── showcase-dashboard/     # 📊 PulseMetrics Dashboard
│
├── nptel_hud.py            # ⚡ NPTEL AI HUD Overlay
├── smart_solver.py         # 💻 CodeFlash Coding Typer
├── typer.py                # Standalone code typer
├── config.json             # Local configuration
└── requirements.txt        # Python dependencies
```

---

## 📄 License
Distributed under the MIT License.
