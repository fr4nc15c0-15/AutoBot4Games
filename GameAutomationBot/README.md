# GameAutomationBot

A production-grade, modular Python automation framework for PC games that combines computer vision, OCR, and simulated input.

## Features
- Modular architecture (`core`, `vision`, `ocr`, `actions`, `system`, `games`).
- Universal UI detection with template matching + OCR fallback.
- Human-like mouse and keyboard automation.
- Anti-popup service that auto-closes common dialogs.
- Watchdog with auto-restart and recovery.
- Multi-game orchestration (Arknights Endfield, Solo Leveling Arise, 7DS Grand Cross).
- Extensible game plugin layout.

## Installation
1. Install Python 3.11+.
2. Install Tesseract OCR engine:
   - Windows: install from official UB Mannheim build.
   - Linux: `sudo apt-get install tesseract-ocr`.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure `config/settings.py` and `config/paths.py`.

## Project Architecture
- **config/**: shared runtime settings, regions, display profiles, asset/game paths.
- **core/**: engine, scheduler, watchdog, fault recovery orchestration.
- **vision/**: screenshots, OpenCV template search, region UI detector, popup detector.
- **ocr/**: OCR extraction for text and numeric values.
- **actions/**: human-like mouse and keyboard control wrappers.
- **system/**: process launching/monitoring and monitor power controls.
- **utils/**: logging, retry decorators, timers, randomization helpers.
- **games/**: independent game modules built on shared services.

## Capturing UI Assets
1. Run the game in a fixed resolution profile (see `config/resolution.py`).
2. Capture UI snippets with clean edges (buttons/icons/popups).
3. Save assets under:
   - `assets/buttons/`
   - `assets/items/`
   - `assets/popups/`
   - `assets/resources/`
4. Keep one template per state when possible (normal/hover/disabled).
5. Tune confidence per template in `config/settings.py`.

## Configuration System
- `config/settings.py`: retry counts, confidence thresholds, delays, monitor behavior.
- `config/paths.py`: game executable locations and asset directories.
- `config/regions.py`: named search regions for OCR and UI detection.
- `config/resolution.py`: supported monitor profiles and scale factors.

## Running the Bot
```bash
python main.py
```
From `GameAutomationBot/` directory, the orchestrator will:
1. Run Endfield bot
2. Run Solo Leveling bot
3. Run 7DS bot
4. Close game, free memory, and wait between runs

## Adding a New Game
1. Create a folder under `games/new_game/`.
2. Add at minimum:
   - `bot.py`
   - `exploration.py`
   - `dailies.py`
   - `combat.py`
3. Import shared services from `vision`, `ocr`, `actions`, `core`, `system`.
4. Register and execute the bot in `main.py`.

## Safety Notes
- PyAutoGUI failsafe is enabled. Move cursor to top-left corner to stop automation.
- Use windowed mode during development.
- Test modules with low click speed and high logging verbosity first.
