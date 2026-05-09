# ResolveAssistant v3.0 (PRECISION)

An AI-powered video editing assistant for DaVinci Resolve with **High-Precision Vision (OCR)**, **Verification-Based Automation**, and **Comprehensive Task Orchestration**.

## Features
- **High-Precision Vision**: Integrated OCR (Tesseract) allows the AI to read labels, timecodes, and menu items directly from your screen.
- **Verification-Based Macros**: Every click and keystroke is verified against the UI state. The AI won't type until it "sees" the correct dialog is open.
- **Professional Orchestrator**: The Brain Engine (v3.0) now handles complex multi-step task graphs, mapping visual footage analysis to specific professional parameters.
- **High-Fidelity Learning**: Training Mode captures not just visual frames, but full UI layouts and text labels to build a comprehensive editing knowledge base.
- **Universal & Resilient**: Deep integration for the Free version with tiered fallbacks (API -> OCR Vision -> Template Matching -> Hotkeys).

## Setup

### Prerequisites
- DaVinci Resolve (Studio or Free).
- Python 3.6 or higher.
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on your system.
- `pip install -r requirements.txt`

## Advanced Command System

### 1. Precision Auto-Edit (`auto edit [project name]`)
The AI performs a comprehensive professional edit by:
- Creating a verified project structure.
- Reading UI labels to ensure correct media ingestion.
- Orchestrating a sequence of "Tricks" (e.g., dynamic range compression, exposure correction) based on deep visual analysis.

### 2. High-Fidelity Training (`train`)
The AI researches professional workflows by "watching" tutorials and simultaneously "reading" the UI labels in those videos to understand the relationship between actions and screen states.

### 3. State-Aware Control
The AI now understands *context*. For example, if you say `switch to color page`, it verifies it has actually reached that page before attempting any grading commands.

## Troubleshooting & Calibration
- **Calibration**: Use `python src/setup_assistant.py [name]` to capture high-res templates.
- **OCR Issues**: Ensure DaVinci Resolve is not obscured by other windows for best reading accuracy.

## Development & Testing
Run the comprehensive test suite (7 suites):
```bash
python3 tests/test_precision.py
python3 tests/test_assistant.py
# ... and others
```
