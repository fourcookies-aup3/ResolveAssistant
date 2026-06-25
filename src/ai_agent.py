import editor_actions
import json
import re
from resolve_proxy import is_api_available

# Allowlist of functions permitted in execute_plan dispatch
_ALLOWED_PLAN_FUNCTIONS = frozenset([
    "create_new_project",
    "import_media",
    "create_timeline",
    "add_clips_to_timeline",
    "switch_to_page",
    "save_project",
    "click_ui_element",
    "render_project",
    "list_clips_in_media_pool",
])


class AIAgent:
    def __init__(self):
        # In a real implementation, this would connect to an LLM
        pass

    def process_command(self, command):
        """
        Translates natural language into editor actions.
        Works in both API-enabled (Studio) and UI-Only (Free) modes.
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
                "- import [path]\n"
                "- create timeline [name]\n"
                "- add [clip name] to timeline\n"
                "- switch to [media|edit|color|deliver] page\n"
                "- save project\n"
                "- click [button name]\n"
                "- render")

    def _handle_create_project(self, name):
        editor_actions.create_new_project(name)
        mode = "API" if is_api_available() else "UI Automation"
        return f"Created project: {name} (via {mode})"

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
            return f"Failed to add {clip_name} to timeline. Make sure clips are imported."

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

    def execute_plan(self, plan_json):
        actions = json.loads(plan_json)
        results = []
        for action in actions:
            func_name = action.get("function")
            args = action.get("args", [])
            kwargs = action.get("kwargs", {})

            if func_name not in _ALLOWED_PLAN_FUNCTIONS:
                results.append({"action": func_name, "status": "failed", "error": "Function not allowed"})
                continue

            func = getattr(editor_actions, func_name, None)
            if func is not None:
                result = func(*args, **kwargs)
                results.append({"action": func_name, "status": "success", "result": str(result)})
            else:
                results.append({"action": func_name, "status": "failed", "error": "Function not found"})
        return results
