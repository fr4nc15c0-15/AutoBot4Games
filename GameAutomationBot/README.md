# GameAutomationBot

GameAutomationBot is a production-grade Python automation framework designed for PC games.
It combines **computer vision**, **OCR**, and **human-like simulated input** to automate routine
in-game workflows while remaining modular and easy to extend.

---

## Core Features

- Highly modular architecture by domain (`vision`, `ocr`, `actions`, `system`, `core`, `games`).
- Universal UI detection pipeline: **template matching → OCR → fallback region strategy**.
- Fast OpenCV matching helpers with retries, confidence control, timeout, and regions.
- OCR subsystem with image preprocessing for text and number extraction.
- Human-like mouse behavior (offset jitter, randomized movement speed, delays).
- Anti-popup thread to automatically close common disruptive dialogs.
- Watchdog thread to recover from crashes/freezes.
- Scheduler thread for background periodic tasks.
- Auto-recovery strategy when UI detection repeatedly fails.
- Sequential multi-game orchestration with cleanup between games.

---

## Supported Games (Initial)

- Arknights Endfield
- Solo Leveling Arise
- 7DS Grand Cross

The framework is extensible: adding new games only requires a new folder in `games/` and wiring
its bot in `main.py`.

---

## Installation

1. Install **Python 3.11+**.
2. Install **Tesseract OCR** engine:
   - Windows: Install Tesseract and add it to PATH.
   - Linux: `sudo apt-get install tesseract-ocr`
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure paths and runtime settings:
   - `config/paths.py`
   - `config/settings.py`
   - `config/regions.py`

---

## Architecture

```text
GameAutomationBot/
  main.py
  config/
  core/
  vision/
  ocr/
  actions/
  system/
  utils/
  games/
    endfield/
    solo_leveling/
    seven_ds/
  assets/
    buttons/
    items/
    popups/
    resources/
  logs/
```

### Module Responsibilities

- **vision/**: screenshot capture, template matching, UI and popup detection.
- **ocr/**: text and number extraction with preprocessing.
- **actions/**: mouse and keyboard control wrappers.
- **system/**: launcher/process/memory/monitor controls.
- **core/**: bot engine, scheduler, watchdog.
- **games/**: game-specific routines and orchestration.
- **utils/**: logging, retry helpers, timers, randomization.

---

## Capturing UI Assets

1. Launch game in a stable resolution profile (see `config/resolution.py`).
2. Capture clean templates (without compression artifacts).
3. Store assets in:
   - `assets/buttons/`
   - `assets/items/`
   - `assets/popups/`
   - `assets/resources/`
4. Name templates with lowercase snake_case to align with detector conventions.
5. Tune confidence values per asset in your game logic and settings.

---

## Running the Bot

From inside `GameAutomationBot/`:

```bash
python main.py
```

The orchestrator executes:
1. Endfield bot
2. Solo Leveling bot
3. 7DS bot

Between each run, it will:
- close the game process
- free memory
- wait 10 seconds

---

## Configuration System

- `config/settings.py`: retries, delays, confidence thresholds, service intervals.
- `config/paths.py`: executable paths, asset paths, log path.
- `config/regions.py`: named regions for OCR and targeted search.
- `config/resolution.py`: supported resolution profiles.

---

## Extending with a New Game

1. Create `games/new_game/`.
2. Add modules (minimum):
   - `bot.py`
   - `exploration.py`
   - `dailies.py`
   - `combat.py`
3. Reuse shared modules from `vision`, `ocr`, `actions`, `core`, and `system`.
4. Register new bot sequence in `main.py`.

---

## Safety

- PyAutoGUI FAILSAFE is enabled. Move cursor to top-left corner to abort automation.
- Start in windowed mode and test with conservative action timings.
- Review logs in `logs/automation.log`.
