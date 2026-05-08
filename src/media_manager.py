import os
import random

MUSIC_PATH = r"C:\Users\finnr\Videos\Music"
SFX_PATH = r"C:\Users\finnr\Videos\SFX"

def get_smart_media_selection(media_type, context=None):
    """
    Scans media directories and selects a 'fitting' file.
    In a real AI, this would use the context (e.g., scene type from vision)
    to choose a matching mood.
    """
    path = MUSIC_PATH if media_type == "music" else SFX_PATH

    # Handle mock environment/missing paths
    if not os.path.exists(path):
        # For testing purposes, we'll return a dummy name if path doesn't exist
        return f"dummy_{media_type}_01.mp3"

    files = [f for f in os.listdir(path) if f.lower().endswith(('.mp3', '.wav', '.m4a'))]
    if not files:
        return None

    # AI Decision Logic
    if context and "dominant_color" in context:
        # Example: Choose upbeat music for bright scenes, moody for dark
        if context["brightness"] > 128:
            # Filter for files that might be 'upbeat' (based on filename for this mock)
            upbeat = [f for f in files if "upbeat" in f.lower() or "happy" in f.lower()]
            if upbeat: return random.choice(upbeat)
        else:
            dark = [f for f in files if "dark" in f.lower() or "moody" in f.lower()]
            if dark: return random.choice(dark)

    return random.choice(files)
