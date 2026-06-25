from resolve_proxy import get_resolve, is_api_available
import vision
import input_control
import os
import sys

def create_new_project(project_name):
    if is_api_available():
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        if not pm:
            print(f"Error: Could not access Project Manager.")
            return False
        project = pm.CreateProject(project_name)
        if project:
            print(f"Project '{project_name}' created successfully via API.")
            return True
        else:
            print(f"Failed to create project '{project_name}' via API (may already exist).")
            return False

    # Fallback to UI Automation
    print(f"API unavailable. Attempting to create project '{project_name}' via UI automation.")
    # Step 1: Open Project Manager (Shift+1)
    input_control.hotkey('shift', '1')
    # Step 2: Click 'New Project' button (needs template)
    if click_ui_element('new_project_button'):
        input_control.type_text(project_name)
        input_control.press_key('enter')
        return True
    return False

def import_media(file_paths):
    if not file_paths:
        print("Error: No file paths provided for import.")
        return False

    if is_api_available():
        resolve = get_resolve()
        ms = resolve.GetMediaStorage()
        if not ms:
            print("Error: Could not access Media Storage.")
            return False
        clips = ms.AddItemListToMediaPool(file_paths)
        if clips:
            print(f"Imported {len(clips)} clips via API.")
            return clips
        else:
            print("Failed to import media via API.")
            return False

    # Fallback to UI Automation
    print("API unavailable. Attempting to import media via UI automation.")
    for path in file_paths:
        if sys.platform == 'darwin':
            input_control.hotkey('command', 'i')
        else:
            input_control.hotkey('ctrl', 'i')

        # This part is tricky as it opens a OS dialog.
        # Usually we would type the path and press enter.
        input_control.type_text(path)
        input_control.press_key('enter')
    return True

def create_timeline(timeline_name):
    if is_api_available():
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        if not pm:
            print("Error: Could not access Project Manager.")
            return False
        project = pm.GetCurrentProject()
        if not project:
            print("Error: No project is currently open. Create or load a project first.")
            return False
        mp = project.GetMediaPool()
        timeline = mp.CreateEmptyTimeline(timeline_name)
        if timeline:
            print(f"Timeline '{timeline_name}' created via API.")
            return timeline
        else:
            print(f"Failed to create timeline '{timeline_name}' via API.")
            return False

    # Fallback
    print(f"API unavailable. Creating timeline '{timeline_name}' via UI automation.")
    if sys.platform == 'darwin':
        input_control.hotkey('command', 'n')
    else:
        input_control.hotkey('ctrl', 'n')
    input_control.type_text(timeline_name)
    input_control.press_key('enter')
    return True

def list_clips_in_media_pool():
    if is_api_available():
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        if not pm:
            return []
        project = pm.GetCurrentProject()
        if project:
            mp = project.GetMediaPool()
            root_folder = mp.GetRootFolder()
            return root_folder.GetClipList()
    return []

def add_clips_to_timeline(clip_names):
    if is_api_available():
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        if not pm:
            print("Error: Could not access Project Manager.")
            return False
        project = pm.GetCurrentProject()
        if not project:
            print("Error: No project is currently open.")
            return False

        timeline = project.GetCurrentTimeline()
        if not timeline:
            timeline = create_timeline("Timeline 1")
            if not timeline:
                print("Error: Could not create a default timeline.")
                return False

        mp = project.GetMediaPool()
        all_clips = list_clips_in_media_pool()
        clips_to_add = []
        for name in clip_names:
            for clip in all_clips:
                if clip.GetName() == name or (hasattr(clip, 'path') and os.path.basename(clip.path) == name):
                    clips_to_add.append(clip)
                    break
        if clips_to_add:
            return mp.AppendToTimeline(clips_to_add)
        else:
            print(f"No matching clips found in media pool for: {', '.join(clip_names)}")
            return False

    # Fallback: Very basic UI automation (Drag and drop or F12)
    print("API unavailable. Adding clips via UI automation (F12).")
    for name in clip_names:
        # Assuming clip is selected or can be found by typing
        input_control.type_text(name)
        input_control.press_key('f12') # 'Append to end of timeline' hotkey
    return True

# --- UI Automation Actions ---

def switch_to_page(page_name):
    pages = {
        'media': 'shift+2',
        'cut': 'shift+3',
        'edit': 'shift+4',
        'fusion': 'shift+5',
        'color': 'shift+6',
        'fairlight': 'shift+7',
        'deliver': 'shift+8'
    }

    if page_name not in pages:
        print(f"Error: Unknown page '{page_name}'. Valid pages: {', '.join(pages.keys())}")
        return False

    if is_api_available():
        resolve = get_resolve()
        resolve.OpenPage(page_name)

    keys = pages[page_name].split('+')
    input_control.hotkey(*keys)

    print(f"Switched to page: {page_name}")
    return True

def save_project():
    if sys.platform == 'darwin':
        input_control.hotkey('command', 's')
    else:
        input_control.hotkey('ctrl', 's')
    print("Project saved.")
    return True

def click_ui_element(template_name):
    template_path = os.path.join('assets', 'templates', f'{template_name}.png')
    coords = vision.find_image_on_screen(template_path)
    if coords:
        input_control.click(coords[0], coords[1])
        print(f"Clicked UI element: {template_name}")
        return True
    else:
        print(f"Could not find UI element: {template_name}")
        return False

def render_project():
    switch_to_page('deliver')
    return click_ui_element('start_render')
