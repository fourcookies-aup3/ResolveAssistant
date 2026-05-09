# ResolveAssistant v4.0 (AUTONOMOUS)

An AI-powered video editing assistant for DaVinci Resolve with **Fully Autonomous "Fire-and-Forget" Mode**, **High-Precision Vision**, and **Cognitive Learning**.

## Features
- **Fully Autonomous Mode**: Monitor a folder and automatically edit/render every new video that appears.
- **Precision OCR Vision**: Reads UI labels and menus for 100% reliable state detection.
- **Verification-Based Macros**: Verifies UI state before every action (clicks, typing).
- **Brain Engine v4.0**: Footage-aware decision making for professional "Tricks" (Dynamic Zoom, Grade, Audio).
- **Smart Task Tracking**: Database-backed persistence ensures no file is processed twice.
- **Universal Support**: Native support for the Free version of DaVinci Resolve.

## Setup

### Prerequisites
- DaVinci Resolve (Studio or Free).
- Python 3.6 or higher.
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed.
- `pip install -r requirements.txt`

## Usage Modes

### 1. Fully Autonomous ("The Video Factory")
Automatically processes new files in `C:\Users\finnr\Videos\Source`.
```bash
python src/main.py --fully-auto
```
The AI will:
1. Scan for new videos.
2. Launch DaVinci Resolve.
3. Create a project and ingest the video.
4. Perform a professional edit (Sound, Grade, Effects).
5. Render and Save.

### 2. Live Interactive Mode
Execute specific commands live on your screen.
```bash
python src/main.py
```

## Advanced Training & Observation
- `train`: AI researches professional tutorials in the background.
- `stop training`: Saves all learned knowledge to the database.
- `watch [seconds]`: AI watches you edit manually to learn your style.

## Development & Testing
Run all 8 test suites:
```bash
python3 tests/test_autonomous.py
python3 tests/test_precision.py
# ... etc
```
