# ResolveAssistant

An AI-powered video editing assistant for DaVinci Resolve with **Infinite Cognitive Training** and **Enhanced UI Resilience**.

## Features
- **Infinite Video Training**: The AI can watch YouTube tutorials and learn continuously until you tell it to stop.
- **Improved UI Automation**: Advanced tiered fallbacks (Vision -> Hotkeys -> Context Menus) ensure smooth operation even without the official API.
- **Live Visual Execution**: Watch the AI work in real-time with deliberate, human-like movements.
- **Smart Media Selection**: Visual-mood-based selection of Music and SFX.
- **Universal Support**: Native support for the Free version of DaVinci Resolve.

## Advanced Training Mode

To start a session where the AI watches and learns from video tutorials:
```bash
ResolveAI (LIVE)> train
```
The AI will open a browser to YouTube tutorials and start analyzing patterns in the background.

To stop the learning session:
```bash
ResolveAI (LIVE)> stop training
```
All gathered knowledge is permanently saved to `resolve_assistant.db`.

## UI Calibration & Resiliency
The assistant is designed to be highly resilient. If it cannot find a button visually:
1. It tries standard **Keyboard Hotkeys** (e.g., Ctrl+N).
2. It tries a **Right-Click Context Menu** fallback in the Project Manager.
3. You can always manually calibrate a specific button:
   ```bash
   python src/setup_assistant.py new_project_button
   ```

## Development & Testing
```bash
python tests/test_assistant.py
python tests/test_advanced.py
python tests/test_free_version.py
python tests/test_live.py
python tests/test_professional.py
python tests/test_learning.py
```
