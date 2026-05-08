# ResolveAssistant v2.0 (BOOSTED)

An AI-powered video editing assistant for DaVinci Resolve with **Supercharged Speed**, **Full Creative Learning**, and **Footage-Aware Decision Making**.

## Features
- **Supercharged Speed**: Near-instant UI automation and optimized Computer Vision.
- **Full Editing Training**: The AI now researches all editing techniques, including cutting, speed ramping, transitions, and audio mixing.
- **Brain Engine**: Automatically decides which professional "tricks" to apply based on visual analysis of your footage (e.g., dynamic zoom for slow scenes, exposure boost for dark scenes).
- **Infinite Learning**: Researches YouTube and professional tutorials in the background until stopped.
- **Universal Support**: Native support for the Free version of DaVinci Resolve via Vision/Hotkey tiers.

## Setup

### Prerequisites
- DaVinci Resolve (Studio or Free).
- Python 3.6 or higher.
- `pip install pyautogui opencv-python pillow sqlalchemy pynput`

## Advanced Command & Control

### 1. Boosted Auto-Edit (`auto edit [project name]`)
The AI builds a full professional edit sequence at high speed. It analyzes each frame to apply:
- **Exposure Boosts** for dark clips.
- **Teal & Orange** cinematic grades for specific color profiles.
- **Dynamic Zoom** and **Transitions** learned from its knowledge base.

### 2. Broad Training Mode (`train`)
The AI opens multiple professional resource channels and begins researching all aspects of video editing.
```bash
ResolveAI (LIVE)> train
# AI starts researching transitions, speed ramps, and cutting tricks...
ResolveAI (LIVE)> stop training
```

### 3. Brain Status (`status`)
Check the current state of the AI's decision engine and automation speed.
```bash
ResolveAI (LIVE)> status
```

## How the Brain Works
The assistant uses the **Brain Decision Engine** (`src/brain.py`) to map vision-based analysis (brightness, dominant color, motion) to a library of learned "Tricks". This allows the AI to edit your video not just automatically, but *stylistically*.

## Development & Testing
```bash
python tests/test_assistant.py
python tests/test_advanced.py
python tests/test_free_version.py
python tests/test_live.py
python tests/test_professional.py
python tests/test_learning.py
```
