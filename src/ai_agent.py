import editor_actions
import json
import re
from resolve_proxy import is_api_available
import trainer
import observer
import database

class AIAgent:
    def __init__(self):
        database.init_db()

    def process_command(self, command):
        """
        Translates natural language into editor actions.
        Now includes training and observation modes.
        """
        patterns = [
            (r'(?i)create project (.*)', self._handle_create_project),
            (r'(?i)import (.*)', self._handle_import),
            (r'(?i)create timeline (.*)', self._handle_create_timeline),
            (r'(?i)add (.*) to timeline', self._handle_add_to_timeline),
            (r'(?i)switch to (.*) page', self._handle_switch_page),
            (r'(?i)save project', self._handle_save_project),
            (r'(?i)click (.*)', self._handle_click_ui),
            (r'(?i)render', self._handle_render),
            (r'(?i)color grade (.*)', self._handle_color_grade),
            (r'(?i)add music', lambda: self._handle_smart_media("music")),
            (r'(?i)add sfx', lambda: self._handle_smart_media("sfx")),
            (r'(?i)auto edit (.*)', self._handle_auto_edit),
            (r'(?i)train', self._handle_train),
            (r'(?i)watch (.*)', self._handle_watch),
        ]

        for pattern, handler in patterns:
            match = re.search(pattern, command)
            if match:
                if match.groups():
                    arg = match.group(1).strip()
                    return handler(arg)
                else:
                    return handler()

        return ("I'm sorry, I don't understand that command yet. Try:\n"
                "- create project [name]\n"
                "- color grade [style]\n"
                "- auto edit [project name]\n"
                "- train\n"
                "- watch [duration in seconds]")

    def _handle_create_project(self, name):
        editor_actions.create_new_project(name)
        mode = "API" if is_api_available() else "UI Automation"
        return f"Created and opened project: {name} (via {mode})"

    def _handle_import(self, path):
        editor_actions.import_media([path])
        mode = "API" if is_api_available() else "UI Automation"
        return f"Imported media from: {path} (via {mode})"

    def _handle_create_timeline(self, name):
        editor_actions.create_timeline(name)
        mode = "API" if is_api_available() else "UI Automation"
        return f"Created timeline: {name} (via {mode})"

    def _handle_add_to_timeline(self, clip_name):
        clip_names = [c.strip() for c in re.split(r',| and |(?i) and ', clip_name)]
        success = editor_actions.add_clips_to_timeline(clip_names)
        mode = "API" if is_api_available() else "UI Automation"
        if success:
            return f"Added {clip_name} to timeline (via {mode})."
        else:
            return f"Failed to add {clip_name} to timeline."

    def _handle_switch_page(self, page):
        editor_actions.switch_to_page(page)
        return f"Switched to {page} page."

    def _handle_save_project(self):
        editor_actions.save_project()
        return "Saving project..."

    def _handle_click_ui(self, element):
        success = editor_actions.click_ui_element(element)
        if success:
            return f"Clicked {element}."
        else:
            return f"Failed to find or click {element}."

    def _handle_render(self):
        editor_actions.render_project()
        return "Starting render process..."

    def _handle_color_grade(self, style):
        params = trainer.get_best_grade_params(style)
        if params:
            print(f"Applying learned parameters for {style}: {params}")
        editor_actions.apply_color_grade(style)
        return f"Applying {style} color grade using learned knowledge."

    def _handle_smart_media(self, media_type):
        editor_actions.import_and_add_smart_media(media_type)
        return f"AI selected and added fitting {media_type}."

    def _handle_auto_edit(self, project_name):
        default_clips = [r"C:\Users\finnr\Videos\Source\clip1.mp4"]
        editor_actions.professional_auto_edit(project_name, default_clips)
        return f"Professional Auto-Edit for '{project_name}' in progress."

    def _handle_train(self):
        trainer.train_from_internet()
        return "Training complete. I am now more advanced!"

    def _handle_watch(self, duration):
        try:
            d = int(duration)
        except:
            d = 60
        observer.run_observer_session(d)
        return f"Observation complete. I have learned from your editing for {d} seconds."

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
                results.append({"action": func_name, "status": "success", "result": str(result)})
            else:
                results.append({"action": func_name, "status": "failed", "error": "Function not found"})
        return results
