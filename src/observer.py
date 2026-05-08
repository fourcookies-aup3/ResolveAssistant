from pynput import mouse, keyboard
import time
import database
from database import ObservedAction
import vision
import threading

class Observer:
    def __init__(self):
        self.is_observing = False
        self.mouse_listener = None
        self.key_listener = None

    def on_click(self, x, y, button, pressed):
        if pressed and self.is_observing:
            context = vision.analyze_frame()
            self._record_action('click', f'Button {button} at ({x}, {y})', context)

    def on_press(self, key):
        if self.is_observing:
            try:
                k = key.char
            except AttributeError:
                k = str(key)
            context = vision.analyze_frame()
            self._record_action('hotkey', f'Pressed {k}', context)

    def _record_action(self, type, details, context):
        session = database.get_session()
        action = ObservedAction(
            page='unknown', # Could be inferred from context later
            action_type=type,
            details=details,
            visual_context=context,
            timestamp=time.time()
        )
        session.add(action)
        session.commit()
        session.close()
        print(f"Observer: Recorded {type} - {details}")

    def start(self):
        print("--- Observer Mode: Active. Watching your edits... ---")
        print("Press 'ESC' in the terminal or move mouse to corner to stop if failsafe active.")
        self.is_observing = True
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.key_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener.start()
        self.key_listener.start()

    def stop(self):
        self.is_observing = False
        if self.mouse_listener: self.mouse_listener.stop()
        if self.key_listener: self.key_listener.stop()
        print("--- Observer Mode: Stopped. ---")

def run_observer_session(duration=60):
    obs = Observer()
    obs.start()
    time.sleep(duration)
    obs.stop()
