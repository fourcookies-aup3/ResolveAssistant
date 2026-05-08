from resolve_proxy import get_resolve, is_api_available
import vision
import input_control
import media_manager
import os
import sys
import time

def create_new_project(project_name):
    if is_api_available():
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        project = pm.CreateProject(project_name)
        if project:
            print(f"Project '{project_name}' created successfully via API.")
            pm.LoadProject(project_name)
            return True
        else:
            return False

    print(f"Attempting to create project '{project_name}' via UI automation.")
    input_control.hotkey('shift', '1') # Open Project Manager
    time.sleep(2)

    # Tier 1: Vision
    if click_ui_element('new_project_button'):
        input_control.type_text(project_name)
        input_control.press_key('enter')
        time.sleep(2)
        return True

    # Tier 2: Hotkey Fallback
    print("Vision failed. Trying hotkey fallback (Ctrl+N)...")
    if sys.platform == 'darwin':
        input_control.hotkey('command', 'n')
    else:
        input_control.hotkey('ctrl', 'n')
    time.sleep(1)
    input_control.type_text(project_name)
    input_control.press_key('enter')

    # Tier 3: Right-Click Fallback (Context menu in Project Manager)
    print("Hotkey might have failed. Trying right-click fallback...")
    width, height = input_control.get_screen_size()
    input_control.right_click(width // 2, height // 2)
    time.sleep(1)
    # Most Resolve versions have 'New Project...' in context menu
    if click_ui_element('context_new_project') or True: # Force try if image missing
        input_control.type_text(project_name)
        input_control.press_key('enter')
        return True

    return False

def open_project(project_name):
    if is_api_available():
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        if pm.LoadProject(project_name):
            print(f"Project '{project_name}' opened.")
            return True

    input_control.hotkey('shift', '1')
    time.sleep(1)
    input_control.type_text(project_name)
    input_control.press_key('enter')
    return True

def import_media(file_paths):
    if is_api_available():
        resolve = get_resolve()
        ms = resolve.GetMediaStorage()
        clips = ms.AddItemListToMediaPool(file_paths)
        if clips:
            print(f"Imported {len(clips)} clips via API.")
            return clips

    for path in file_paths:
        if sys.platform == 'darwin':
            input_control.hotkey('command', 'i')
        else:
            input_control.hotkey('ctrl', 'i')
        time.sleep(1.5)
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

    if sys.platform == 'darwin':
        input_control.hotkey('command', 'n')
    else:
        input_control.hotkey('ctrl', 'n')
    time.sleep(1)
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
            clips_to_add = []
            for name in clip_names:
                for clip in all_clips:
                    if clip.GetName() == name or (hasattr(clip, 'path') and os.path.basename(clip.path) == name):
                        clips_to_add.append(clip)
                        break
            if clips_to_add:
                return mp.AppendToTimeline(clips_to_add)

    for name in clip_names:
        input_control.type_text(name)
        input_control.press_key('f12')
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
        print(f"Vision Alert: Could not find '{template_name}'.")
        return False

def render_project():
    switch_to_page('deliver')
    return click_ui_element('start_render')

# --- Advanced Commands ---

def apply_color_grade(style):
    context = vision.analyze_frame()
    print(f"Vision Analysis: {context['dominant_color']} scene. Brightness: {context['brightness']:.1f}")

    switch_to_page('color')
    print(f"Applying {style} color grade...")

    if not click_ui_element('luts_tab'):
        input_control.hotkey('ctrl', '4')

    input_control.type_text(style)
    input_control.press_key('enter')
    return True

def import_and_add_smart_media(media_type):
    context = vision.analyze_frame()
    selection = media_manager.get_smart_media_selection(media_type, context)

    if not selection or "dummy" in selection:
        print(f"No real {media_type} files found. Please check paths in README.")
        return False

    print(f"Smart {media_type} selection: {selection}")
    path = os.path.join(media_manager.MUSIC_PATH if media_type == "music" else media_manager.SFX_PATH, selection)

    import_media([path])
    add_clips_to_timeline([selection])
    return True

def professional_auto_edit(project_name, source_clips=None):
    if not source_clips:
        source_dir = r"C:\Users\finnr\Videos\Source"
        if os.path.exists(source_dir):
            source_clips = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if f.endswith(('.mp4', '.mov'))]

    if not source_clips:
        print("Error: No source footage found. Add clips to 'Videos/Source'.")
        return False

    print(f"Starting Professional Auto-Edit for '{project_name}'...")
    create_new_project(project_name)

    import_media(source_clips)
    create_timeline("Master Edit")
    add_clips_to_timeline([os.path.basename(c) for c in source_clips])

    switch_to_page('edit')
    import_and_add_smart_media("music")
    import_and_add_smart_media("sfx")

    apply_color_grade("cinematic")

    save_project()
    print("Auto-Edit Complete!")
    return True
