# ResolveAssistant

An AI-powered video editing assistant for DaVinci Resolve with Screen Vision and Live Control.

## Features
- **Scripting API Integration**: Direct control via Resolve's Python API.
- **Computer Vision**: Sees your screen to find UI elements using OpenCV.
- **Live Control**: Automates mouse and keyboard for real-time editing.
- **Natural Language**: Process commands like "click the render button" or "save project".
- **Mock Mode**: Full development and testing support without requiring a Resolve installation.

## Prerequisites
- DaVinci Resolve Studio (Scripting API is required).
- Python 3.6 or higher.
- `pip install pyautogui opencv-python pillow`
- **Important**: Ensure "External scripting using" is set to "Local" or "Network" in Resolve Preferences -> System -> General.

## Setup

### Environment Variables
Configure these to point to your Resolve installation:

**Windows:**
```cmd
set RESOLVE_SCRIPT_API=%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\
set RESOLVE_SCRIPT_LIB=C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll
set PYTHONPATH=%PYTHONPATH%;%RESOLVE_SCRIPT_API%\Modules\
```

**macOS:**
```bash
export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/"
export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
```

## Usage

Run the assistant:
```bash
python3 src/main.py
```

### Example Commands
- `create project My Movie`
- `switch to edit page`
- `click export_button` (requires template image in `assets/templates/export_button.png`)
- `save project`
- `render`

## Live Control & Vision
The assistant uses `PyAutoGUI` for mouse/keyboard control and `OpenCV` for template matching.
- Template images should be placed in `assets/templates/`.
- Screen capturing is handled by `Pillow`.

## Development
Run in mock mode:
```bash
export USE_MOCK_RESOLVE=true
python3 src/main.py
```

### Running Tests
```bash
python3 tests/test_assistant.py
python3 tests/test_advanced.py
```
