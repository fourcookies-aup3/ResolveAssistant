# ResolveAssistant

An AI-powered video editing assistant for DaVinci Resolve with **Cognitive Learning** and **Observer Mode**.

## Features
- **Learning Database**: Stores editing patterns, color grading styles, and UI locations.
- **Training Mode**: The AI researches the internet for tutorials and advanced techniques.
- **Observer Mode**: The AI watches you edit and learns from your manual actions.
- **Live Visual Execution**: Watch the AI edit your videos in real-time.
- **Smart Media Selection**: Automatically picks fitting Music and SFX.
- **Universal Support**: Works on both DaVinci Resolve Studio and Free.

## Setup

### Prerequisites
- DaVinci Resolve (Studio or Free).
- Python 3.6 or higher.
- `pip install pyautogui opencv-python pillow sqlalchemy pynput`

## Advanced Modes

### 1. Training Mode (`train`)
The AI will simulate searching the internet for "DaVinci Resolve Color Grading" and "Tutorials". It extracts knowledge about styles like Cinematic, Nature, etc., and stores them in `resolve_assistant.db`.
```bash
ResolveAI (LIVE)> train
```

### 2. Observer Mode (`watch [seconds]`)
The AI will listen to your mouse and keyboard inputs while you edit manually in DaVinci Resolve. It records your actions along with the visual context (brightness, color) to understand how you edit.
```bash
ResolveAI (LIVE)> watch 120
```

## Usage
Start the assistant:
```bash
python src/main.py
```

### Learned Commands
- `color grade cinematic`: Now uses parameters learned from the database.
- `auto edit [project name]`: Continues to evolve as the database grows.

## Troubleshooting & Calibration
- **Vision Fails**: Calibrate using `python src/setup_assistant.py new_project_button`.
- **Database**: To reset the AI's knowledge, simply delete `resolve_assistant.db`.

## Development & Testing
```bash
python tests/test_assistant.py
python tests/test_learning.py
```
