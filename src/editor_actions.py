from resolve_proxy import get_resolve
import vision
import input_control
import os

def create_new_project(project_name):
    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.CreateProject(project_name)
    if project:
        print(f"Project '{project_name}' created successfully.")
        return True
    else:
        print(f"Failed to create project '{project_name}'. It might already exist.")
        return False

def import_media(file_paths):
    resolve = get_resolve()
    ms = resolve.GetMediaStorage()
    clips = ms.AddItemListToMediaPool(file_paths)
    if clips:
        print(f"Imported {len(clips)} clips.")
        return clips
    else:
        print("Failed to import clips.")
        return []

def create_timeline(timeline_name):
    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.GetCurrentProject()
    if not project:
        print("No project currently open.")
        return None

    mp = project.GetMediaPool()
    timeline = mp.CreateEmptyTimeline(timeline_name)
    if timeline:
        print(f"Timeline '{timeline_name}' created.")
        return timeline
    else:
        print(f"Failed to create timeline '{timeline_name}'.")
        return None

def list_clips_in_media_pool():
    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.GetCurrentProject()
    if not project:
        return []

    mp = project.GetMediaPool()
    root_folder = mp.GetRootFolder()
    clips = root_folder.GetClipList()
    return clips

def add_clips_to_timeline(clip_names):
    """
    Finds clips in the media pool by name and appends them to the current timeline.
    """
    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.GetCurrentProject()
    if not project:
        print("No project open.")
        return False

    timeline = project.GetCurrentTimeline()
    if not timeline:
        print("No current timeline. Creating one called 'Timeline 1'.")
        timeline = create_timeline("Timeline 1")
        if not timeline:
            return False

    mp = project.GetMediaPool()
    all_clips = list_clips_in_media_pool()

    clips_to_add = []
    for name in clip_names:
        found = False
        for clip in all_clips:
            # Check for name match or basename match of path
            if clip.GetName() == name or (hasattr(clip, 'path') and os.path.basename(clip.path) == name):
                clips_to_add.append(clip)
                found = True
                break
        if not found:
            print(f"Warning: Clip '{name}' not found in media pool.")

    if clips_to_add:
        success = mp.AppendToTimeline(clips_to_add)
        if success:
            print(f"Added {len(clips_to_add)} clips to timeline.")
            return True

    return False

# --- UI Automation Actions ---

def switch_to_page(page_name):
    """
    Uses the API to switch pages, then verifies visually or via input.
    """
    resolve = get_resolve()
    resolve.OpenPage(page_name)
    print(f"Switched to page: {page_name}")
    return True

def save_project():
    """
    Saves the project using a hotkey (Ctrl+S / Cmd+S).
    """
    import sys
    if sys.platform == 'darwin':
        input_control.hotkey('command', 's')
    else:
        input_control.hotkey('ctrl', 's')
    print("Project saved (via hotkey).")
    return True

def click_ui_element(template_name):
    """
    Finds a UI element on screen using a template image and clicks it.
    Expects templates to be in 'assets/templates/'.
    """
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
    """
    Example of a complex UI automation: Switch to deliver page and click 'Start Render'.
    """
    switch_to_page('deliver')
    # This would require a 'start_render' template image
    return click_ui_element('start_render')
