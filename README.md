# ⚡ CodeFlash & StudyLens: Multimodal AI Developer & Learning Suite

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/AI-Google%20Gemini%20Multimodal-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini AI" />
  <img src="https://img.shields.io/badge/UI-Win32%20Glassmorphic%20HUD-00C7FF?style=for-the-badge" alt="HUD Overlay" />
  <img src="https://img.shields.io/badge/Speed-Rapid%20Keystroke%20Automation-FFD700?style=for-the-badge" alt="Speed" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

An open-source multimodal developer productivity and technical research suite designed to bridge visual problem understanding with automated code generation, accessibility keystroke automation, and distraction-free learning overlays.

---

## 🌟 Core Modules

### 💻 1. CodeFlash Algorithmic Assistant (`smart_solver.py`)
A multimodal pair programming companion for competitive programming practice, interview preparation, and rapid algorithm prototyping.
- **Multimodal Visual Input (`F7`)**: Captures algorithmic problem specifications directly from the screen using Gemini Vision AI—no manual copying required.
- **Multi-Language Architecture (`F9`)**: Dynamically generates production-grade, mathematically verified solutions across **Java, Python, C++, JavaScript, TypeScript, C#, and Go**.
- **Zero-Error Algorithmic Directives**: Built-in compiler and runtime safeguards (64-bit numerical overflow defense, 0/1-index normalization, tree/heap pointer return fidelity, and negative sentinel protection).
- **Universal Keystroke Injection Engine (`F10`)**:
  - `Instant Mode`: High-speed clipboard injection (`0.1s`).
  - `Ultra Mode`: Direct OS keystroke streaming (~0.008s/char) designed for remote desktops, SSH sessions, virtual machines, and secure IDEs where clipboard sharing is restricted.
  - `Human Mode`: Realistic typing cadence with natural micro-delays for live demonstrations.

### 🔬 2. StudyLens STEM Research HUD (`nptel_hud.py`)
A floating, semi-transparent Heads-Up Display (HUD) engineered for accelerated technical study, mathematical research, and assignment review.
- **Interactive Region Snip (`F6`)**: Drag a selection box over complex formulas, circuit diagrams, or technical questions for instant analysis.
- **Step-by-Step Derivations**: Formulates detailed breakdowns, underlying physical principles, and mathematical equations.
- **🛡️ Presentation & Streamer Privacy Shield (`F2`)**: Uses native Windows `SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)` to keep your HUD notes and formulas hidden from Zoom, MS Teams, Google Meet, and OBS screen captures during presentations or live streams.
- **✨ Distraction-Free Transparent HUD (`F3`)**: Minimalist borderless mode displaying only clean typography directly over your workspace.
- **🖱️ Interactive Click-Through (`Ctrl + F3`)**: Allows full mouse interaction with underlying web pages or code editors while keeping reference documentation in view.
- **👁️ Quick Toggle (`F4` or `Esc`)**: Instantly shows or minimizes the HUD overlay.

---

## ⌨️ Global Shortcuts Quick Reference

### CodeFlash Assistant (`smart_solver.py`)
| Hotkey | Action | Description |
| :--- | :--- | :--- |
| **`F7`** | **Visual Screen Solve** | Reads problem from screen and streams code to active editor |
| **`F8`** | **Clipboard Solve** | Solves problem from copied text (`Ctrl+C`) or screenshot (`Win+Shift+S`) |
| **`F9`** | **Cycle Target Language** | Java ➔ Python ➔ C++ ➔ JavaScript ➔ TypeScript ➔ C# ➔ Go |
| **`F10`** | **Cycle Typing Profile** | Instant (0.1s Paste) ➔ Ultra (Direct Keystroke Streamer) ➔ Human Cadence |

### StudyLens HUD (`nptel_hud.py`)
| Hotkey | Action | Description |
| :--- | :--- | :--- |
| **`F6`** | **Interactive Drag Snip** | Drag a bounding box over any equation or problem on screen |
| **`F7`** | **Fullscreen Vision Solve** | Captures active display and generates step-by-step breakdown |
| **`F8`** | **Clipboard Solve** | Analyzes copied question text or snipped diagram |
| **`F3`** | **Toggle Transparent HUD** | Minimalist borderless mode displaying floating text |
| **`Ctrl + F3`** | **Toggle Click-Through** | Passes mouse clicks directly through the HUD to underlying windows |
| **`F2`** | **Toggle Privacy Shield** | Toggles exclusion from OBS, Zoom, and Teams screen sharing |
| **`F4`** / **`Esc`** | **Toggle HUD Visibility** | Minimizes or restores the HUD overlay |

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
  "hotkey_snip": "F6",
  "hotkey_vision": "F7",
  "hotkey_solve": "F8",
  "hotkey_toggle_hud": "F4",
  "hud_opacity": 0.94,
  "hud_always_on_top": true,
  "hud_compact_mode": false,
  "anti_capture_protection": true
}
```

---

## 🚀 Usage

### Launch CodeFlash Assistant:
```bash
python smart_solver.py
```

### Launch StudyLens HUD:
```bash
python nptel_hud.py
```

### Standalone Typer (Without AI):
```bash
python typer.py --mode instant   # High-speed clipboard paste
python typer.py --mode ultra     # Direct OS keystroke streaming
python typer.py --mode human     # Natural typing cadence
```

---

## 📂 Project Architecture

```text
codeflash/
├── carrom_aim_overlay/     # 📱 Carrom Live Aim Overlay & Vision Bot (Scrcpy, OpenCV Detection, Transparent HUD)
│   ├── start_scrcpy_with_overlay.bat # 🚀 One-click launcher: scrcpy mirror + transparent overlay
│   ├── carrom_overlay.py   # Transparent Win32 HUD with live trajectory prediction
│   ├── detect.py           # OpenCV board & coin detection
│   ├── solver.js           # Bridge into physics.js auto-aim solver
│   └── scrcpy-win64-v2.7/  # Android screen mirroring
│
├── carrom_theme_studio/    # 🎯 Carrom Theme Studio (HTML5/Canvas Web App, Digital Physics, 1:1 Canvas)
│   ├── css/                # Responsive 1:1 board styling & themes
│   ├── js/                 # physics.js, board_renderer.js, app.js, physics_bridge.js
│   └── test/               # Verification test suites & benchmarks
│
├── carrom_python_labs/     # 🎱 Carrom Python Physics Laboratories & Tools
│   ├── carrom_game.py      # Pygame 2D Carrom Game
│   ├── carrom_physics_lab.py # Gravitational physics laboratory
│   ├── chain_collision_lab.py # Multi-piece chain collision visualizer
│   └── screen_ruler.py     # Transparent precision screen ruler & protractor
│
├── mobile/                 # 💳 Nova Mobile Application (React Native / Expo)
├── showcase-dashboard/     # 📊 PulseMetrics Dashboard
│
├── nptel_hud.py            # 🔬 StudyLens STEM Research HUD Overlay
├── smart_solver.py         # 💻 CodeFlash Multimodal Pair Programmer
├── typer.py                # ⚡ Standalone OS Keystroke Automation Engine
├── config.json             # Local configuration
└── requirements.txt        # Python dependencies
```

---

## 📄 License
Distributed under the MIT License.
