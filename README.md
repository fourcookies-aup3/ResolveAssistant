# ResolveAssistant

An AI-powered video editing assistant for DaVinci Resolve.

## Features
- Natural language command processing to control DaVinci Resolve.
- Project creation, media import, and timeline management.
- Proxy layer to handle connection to the Resolve Scripting API.
- Mock mode for development without Resolve installed.

## Prerequisites
- DaVinci Resolve Studio (Scripting API is generally a Studio-only feature).
- Python 3.6 or higher.
- Ensure "External scripting using" is set to "Local" or "Network" in Resolve Preferences -> System -> General.

## Setup

### Environment Variables
For the assistant to find the DaVinci Resolve API, you need to set the following environment variables (adjust paths based on your installation):

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

**Linux:**
```bash
export RESOLVE_SCRIPT_API="/opt/resolve/Developer/Scripting/"
export RESOLVE_SCRIPT_LIB="/opt/resolve/libs/Fusion/fusionscript.so"
export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
```

## Usage

Run the assistant:
```bash
python3 src/main.py
```

### Example Commands
- `create project My Awesome Video`
- `import /path/to/video/clip1.mp4`
- `create timeline Main Edit`

## Development
To run in mock mode (without Resolve):
```bash
export USE_MOCK_RESOLVE=true
python3 src/main.py
```

### Running Tests
```bash
python3 tests/test_assistant.py
```
