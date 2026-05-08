# ResolveAssistant

An AI-powered video editing assistant for DaVinci Resolve with **Professional Auto-Edit** and **Computer Vision**.

## Features
- **Live Visual Execution**: Watch the AI edit your videos in real-time.
- **Smart Media Selection**: Automatically picks fitting Music and SFX based on visual analysis of your footage.
- **Style-Based Color Grading**: Apply "Cinematic", "Nature", "HD", or "Colourful" grades.
- **Professional Auto-Edit**: Automate the entire workflow from project creation to final grading with a single command.
- **Universal Support**: Works on both DaVinci Resolve Studio (API) and Free (UI Automation).

## Prerequisites
- DaVinci Resolve (Studio or Free).
- Python 3.6 or higher.
- `pip install pyautogui opencv-python pillow`

## Setup

### Media Directories
The assistant looks for media in these default paths:
- **Music**: `C:\Users\finnr\Videos\Music`
- **Sound Effects**: `C:\Users\finnr\Videos\SFX`
- **Source Footage**: `C:\Users\finnr\Videos\Source` (used for Auto-Edit)

### Paths (Optional)
```bash
export RESOLVE_PATH="/path/to/resolve"
```

## Usage

Start the assistant:
```bash
python3 src/main.py
```

### Advanced Commands
- `auto edit [project name]`: Runs a full professional edit sequence.
- `color grade [cinematic|nature|hd|colourful]`: Analyzes the screen and applies a style.
- `add music`: AI selects a fitting music track and adds it to your timeline.
- `add sfx`: AI selects a fitting sound effect and adds it to your timeline.

### Basic Commands
- `create project [name]` (now automatically opens the project)
- `import [path]`
- `switch to [edit|color|deliver] page`
- `save project`

## How it Works
The assistant uses **Computer Vision (OpenCV)** to analyze the current frame in DaVinci Resolve. It calculates brightness and dominant colors to decide which music or color grade "fits" the mood of your video.

## Development & Testing
```bash
python3 tests/test_assistant.py
python3 tests/test_advanced.py
python3 tests/test_free_version.py
python3 tests/test_live.py
python3 tests/test_professional.py
```
