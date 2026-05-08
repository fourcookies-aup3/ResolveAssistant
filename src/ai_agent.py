import editor_actions
import json
import re
from resolve_proxy import is_api_available
import trainer
import observer
import database
import brain

class AIAgent:
    def __init__(self):
        database.init_db()

    def process_command(self, command):
        """
        Translates natural language into editor actions.
        Boosted version with advanced decision making and feedback.
        """
        patterns = [
            (r'(?i)create project (.*)', self._handle_create_project),
            (r'(?i)auto edit (.*)', self._handle_auto_edit),
            (r'(?i)train', self._handle_start_training),
            (r'(?i)stop training', self._handle_stop_training),
            (r'(?i)status', self._handle_status),
            (r'(?i)import (.*)', self._handle_import),
            (r'(?i)switch to (.*) page', self._handle_switch_page),
            (r'(?i)save project', self._handle_save_project),
            (r'(?i)color grade (.*)', self._handle_color_grade),
            (r'(?i)watch (.*)', self._handle_watch),
            (r'(?i)click (.*)', self._handle_click_ui),
        ]

        for pattern, handler in patterns:
            match = re.search(pattern, command)
            if match:
                if match.groups():
                    arg = match.group(1).strip()
                    return handler(arg)
                else:
                    return handler()

        return ("ResolveAI v2.0 (BOOSTED)\n- auto edit [name]\n- train (research all editing tricks)\n- stop training\n- watch [seconds]\n- status")

    def _handle_status(self):
        summary = brain.get_brain_summary()
        return f"AI Status: ONLINE. Speed: BOOSTED. Engine: {summary}"

    def _handle_auto_edit(self, project_name):
        editor_actions.professional_auto_edit(project_name)
        return f"Boosted Auto-Edit complete for '{project_name}'. AI applied dynamic tricks based on footage."

    def _handle_start_training(self):
        trainer.start_video_training()
        return "Broad Editing Training STARTED. Researching all professional tricks (cutting, effects, speed ramping)..."

    def _handle_stop_training(self):
        trainer.stop_video_training()
        return "Training Mode STOPPED. Knowledge base expanded with new professional tricks."

    def _handle_watch(self, duration):
        try:
            d = int(duration)
        except:
            d = 60
        observer.run_observer_session(d)
        return f"Observation complete. I have learned from your editing for {d} seconds."

    def _handle_create_project(self, name):
        editor_actions.create_new_project(name)
        mode = "API" if is_api_available() else "UI Automation"
        return f"Created project: {name} (via {mode})"

    def _handle_import(self, path):
        editor_actions.import_media([path])
        mode = "API" if is_api_available() else "UI Automation"
        return f"Imported: {path} (via {mode})"

    def _handle_switch_page(self, page):
        editor_actions.switch_to_page(page)
        return f"Page: {page}"

    def _handle_save_project(self):
        editor_actions.save_project()
        return "Saved."

    def _handle_color_grade(self, style):
        editor_actions.apply_color_grade(style)
        return f"Graded: {style}"

    def _handle_click_ui(self, element):
        success = editor_actions.click_ui_element(element)
        if success:
            return f"Clicked {element}."
        else:
            return f"Failed to find or click {element}."

    def execute_plan(self, plan_json):
        actions = json.loads(plan_json)
        results = []
        for action in actions:
            func_name = action.get("function")
            args = action.get("args", [])
            kwargs = action.get("kwargs", {})
            if hasattr(editor_actions, func_name):
                func = getattr(editor_actions, func_name)
                result = func(*args, **kwargs)
                results.append({"action": func_name, "status": "success"})
            else:
                results.append({"action": func_name, "status": "failed"})
        return results
