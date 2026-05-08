# ResolveAssistant

An AI-powered video editing assistant for DaVinci Resolve (Studio and Free versions).

## Features
- **Hybrid Control**: Automatically detects if the DaVinci Resolve Scripting API is available.
- **Studio Support**: Uses the official Python API for high-precision control.
- **Free Version Support**: Falls back to Computer Vision and UI Automation when the API is unavailable.
- **Computer Vision**: Sees your screen to find UI elements using OpenCV.
- **Live Control**: Automates mouse and keyboard for real-time editing.
- **Natural Language**: Process commands like "create project My Movie" or "switch to edit page".

## Prerequisites
- DaVinci Resolve (Studio or Free).
- Python 3.6 or higher.
- `pip install pyautogui opencv-python pillow`

## Setup

### For Studio Version (API Support)
Ensure "External scripting using" is set to "Local" or "Network" in Resolve Preferences -> System -> General.
Configure environment variables:

**macOS:**
```bash
export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/"
export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
```

### For Free Version (UI Automation Support)
No special API configuration is needed, but the assistant will rely heavily on:
1. **Hotkeys**: Standard DaVinci Resolve hotkeys (e.g., Shift+4 for Edit page).
2. **Vision**: Template images in `assets/templates/` to find buttons on your screen.

## Usage

Run the assistant:
```bash
python3 src/main.py
```

### Example Commands
- `create project My Movie`
- `import /path/to/video/clip1.mp4`
- `switch to edit page`
- `add clip1.mp4 to timeline`
- `save project`
- `render`

## How it Works

The assistant uses a tiered execution model:
1. **API Tier**: If the `DaVinciResolveScript` module is found and a connection is established, it uses direct API calls.
2. **UI Tier**: If the API is missing (common in the Free version), it uses `PyAutoGUI` to simulate hotkeys and `OpenCV` to find and click buttons.

## Development
To test Free Version behavior (API Unavailable):
```bash
export RESOLVE_API_UNAVAILABLE=true
python3 src/main.py
```

### Running Tests
```bash
python3 tests/test_assistant.py
python3 tests/test_advanced.py
python3 tests/test_free_version.py
```
