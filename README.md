# ResolveAssistant

An AI-powered video editing assistant for DaVinci Resolve with **Live Live Automation**.

## Features
- **Live Visual Execution**: Watch as the assistant takes control of your mouse and keyboard to edit in DaVinci Resolve.
- **Automatic Launch**: Starts DaVinci Resolve automatically when you run the assistant.
- **Hybrid Control**: Supports both Studio (API) and Free (UI Automation) versions.
- **Computer Vision**: Locates buttons and menus on your screen.
- **Natural Language**: Commands like "create project My Movie" or "switch to color page".

## Prerequisites
- DaVinci Resolve (Studio or Free).
- Python 3.6 or higher.
- `pip install pyautogui opencv-python pillow`

## Setup

### 1. Set Resolve Executable Path (Optional)
By default, the assistant looks for Resolve in standard locations. You can override this:
```bash
export RESOLVE_PATH="/your/custom/path/to/resolve"
```

### 2. Configure API (Studio Only)
Set "External scripting using" to "Local" or "Network" in Resolve Preferences -> System -> General.

## Usage

Start the assistant in Live Mode:
```bash
python3 src/main.py
```

1. **Auto-Launch**: DaVinci Resolve will open automatically.
2. **Focus**: The assistant will bring Resolve to the front.
3. **Control**: Type commands, and watch the assistant move the cursor and perform actions on your screen.

### Example Commands
- `create project My Movie`
- `import /path/to/video/clip1.mp4`
- `switch to edit page`
- `save project`
- `render`

## Live Experience
To ensure you can follow along, the assistant:
- Moves the cursor visibly (approx. 0.8s duration).
- Pauses briefly between actions.
- Types text at a human-like speed.

## Development & Testing
Run in mock mode:
```bash
export USE_MOCK_RESOLVE=true
python3 src/main.py
```

### Running Tests
```bash
python3 tests/test_assistant.py
python3 tests/test_advanced.py
python3 tests/test_free_version.py
python3 tests/test_live.py
```
