from resolve_proxy import get_resolve, is_api_available
import vision
import input_control
import os
import sys

def create_new_project(project_name):
    if is_api_available():
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        project = pm.CreateProject(project_name)
        if project:
            print(f"Project '{project_name}' created successfully via API.")
            return True

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
    if is_api_available():
        resolve = get_resolve()
        ms = resolve.GetMediaStorage()
        clips = ms.AddItemListToMediaPool(file_paths)
        if clips:
            print(f"Imported {len(clips)} clips via API.")
            return clips

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
        project = pm.GetCurrentProject()
        if project:
            mp = project.GetMediaPool()
            timeline = mp.CreateEmptyTimeline(timeline_name)
            if timeline:
                print(f"Timeline '{timeline_name}' created via API.")
                return timeline

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
        project = pm.GetCurrentProject()
        if project:
            timeline = project.GetCurrentTimeline()
            if not timeline:
                timeline = create_timeline("Timeline 1")

            mp = project.GetMediaPool()
            all_clips = list_clips_in_media_pool()

            # Build a lookup map for faster access O(N+M)
            # Use a dictionary to index clips by name and basename for O(1) lookup
            clip_lookup = {}
            for clip in all_clips:
                name = clip.GetName()
                # First-wins matching to preserve original behavior
                if name not in clip_lookup:
                    clip_lookup[name] = clip

                # Check path-based name if available
                path = getattr(clip, 'path', None)
                if path:
                    basename = os.path.basename(path)
                    if basename not in clip_lookup:
                        clip_lookup[basename] = clip

            clips_to_add = [clip_lookup[name] for name in clip_names if name in clip_lookup]

            if clips_to_add:
                return mp.AppendToTimeline(clips_to_add)

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

    if is_api_available():
        resolve = get_resolve()
        resolve.OpenPage(page_name)

    if page_name in pages:
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
