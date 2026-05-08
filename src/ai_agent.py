import editor_actions
import json
import re

class AIAgent:
    def __init__(self):
        # In a real implementation, this would connect to an LLM
        pass

    def process_command(self, command):
        """
        Translates natural language into editor actions.
        Improved to handle basic multi-step commands and better argument extraction.
        """
        # Patterns use case-insensitive matching but we want to capture the original case for arguments
        patterns = [
            (r'(?i)create project (.*)', self._handle_create_project),
            (r'(?i)import (.*)', self._handle_import),
            (r'(?i)create timeline (.*)', self._handle_create_timeline),
            (r'(?i)add (.*) to timeline', self._handle_add_to_timeline),
        ]

        for pattern, handler in patterns:
            match = re.search(pattern, command)
            if match:
                arg = match.group(1).strip()
                return handler(arg)

        return "I'm sorry, I don't understand that command yet. Try:\n- create project [name]\n- import [path]\n- create timeline [name]\n- add [clip name] to timeline"

    def _handle_create_project(self, name):
        editor_actions.create_new_project(name)
        return f"Created project: {name}"

    def _handle_import(self, path):
        editor_actions.import_media([path])
        return f"Imported media from: {path}"

    def _handle_create_timeline(self, name):
        editor_actions.create_timeline(name)
        return f"Created timeline: {name}"

    def _handle_add_to_timeline(self, clip_name):
        # Could be multiple clips separated by comma or 'and'
        clip_names = [c.strip() for c in re.split(r',| and |(?i) and ', clip_name)]
        success = editor_actions.add_clips_to_timeline(clip_names)
        if success:
            return f"Added {clip_name} to timeline."
        else:
            return f"Failed to add {clip_name} to timeline. Make sure clips are imported."

    def execute_plan(self, plan_json):
        """
        Executes a sequence of actions provided in JSON format (e.g., from an LLM).
        """
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
