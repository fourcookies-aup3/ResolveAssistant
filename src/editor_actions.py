from resolve_proxy import get_resolve, is_api_available
import vision
import input_control
import media_manager
import brain
import os
import sys
import time

def create_new_project(project_name):
    if is_api_available():
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        project = pm.CreateProject(project_name)
        if project:
            pm.LoadProject(project_name)
            return True
        else:
            return False

    input_control.hotkey('shift', '1')
    time.sleep(0.5)
    if click_ui_element('new_project_button'):
        input_control.type_text(project_name)
        input_control.press_key('enter')
        return True

    if sys.platform == 'darwin':
        input_control.hotkey('command', 'n')
    else:
        input_control.hotkey('ctrl', 'n')
    input_control.type_text(project_name)
    input_control.press_key('enter')
    return True

# --- Advanced Tricks ---

def apply_dynamic_zoom():
    print("AI: Applying Dynamic Zoom trick...")
    input_control.hotkey('alt', 'z')
    return True

def apply_exposure_boost():
    print("AI: Applying Exposure Boost (for dark footage)...")
    switch_to_page('color')
    input_control.hotkey('alt', 'g')
    return True

def apply_teal_orange_cinematic():
    print("AI: Applying Teal & Orange Cinematic Look...")
    switch_to_page('color')
    return True

# --- Improved Orchestration ---

def professional_auto_edit(project_name, source_clips=None):
    if source_clips is None:
        source_clips = []

    print(f"--- STARTING BOOSTED AUTO-EDIT: {project_name} ---")
    create_new_project(project_name)

    if source_clips:
        import_media(source_clips)
        create_timeline("Advanced Edit")
        add_clips_to_timeline([os.path.basename(c) for c in source_clips])
    else:
        print("No source clips provided. Creating empty project structure.")
        create_timeline("Master Timeline")

    # 1. BRAIN ANALYSIS: AI watches the footage and decides tricks
    analysis = vision.analyze_frame()
    tricks = brain.select_tricks_for_footage(analysis)
    print(f"Brain selected tricks: {tricks}")

    # 2. Apply tricks dynamically
    for trick in tricks:
        if trick == "apply_exposure_boost":
            apply_exposure_boost()
        elif trick == "apply_teal_orange_cinematic":
            apply_teal_orange_cinematic()

    # 3. Add Smart Audio
    switch_to_page('edit')
    import_and_add_smart_media("music")

    save_project()
    print("--- BOOSTED AUTO-EDIT COMPLETE ---")
    return True

def open_project(project_name):
    if is_api_available():
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        if pm.LoadProject(project_name):
            return True
    input_control.hotkey('shift', '1')
    input_control.type_text(project_name)
    input_control.press_key('enter')
    return True

def import_media(file_paths):
    if not file_paths:
        return True

    if is_api_available():
        resolve = get_resolve()
        ms = resolve.GetMediaStorage()
        ms.AddItemListToMediaPool(file_paths)
        return True
    for path in file_paths:
        if sys.platform == 'darwin':
            input_control.hotkey('command', 'i')
        else:
            input_control.hotkey('ctrl', 'i')
        time.sleep(0.5)
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
            mp.CreateEmptyTimeline(timeline_name)
            return True
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
            mp = project.GetMediaPool()
            all_clips = list_clips_in_media_pool()
            clips_to_add = [c for c in all_clips if c.GetName() in clip_names]
            if clips_to_add:
                mp.AppendToTimeline(clips_to_add)
                return True
    for name in clip_names:
        input_control.type_text(name)
        input_control.press_key('f12')
    return True

def switch_to_page(page_name):
    pages = {'media':'shift+2','cut':'shift+3','edit':'shift+4','fusion':'shift+5','color':'shift+6','fairlight':'shift+7','deliver':'shift+8'}
    if is_api_available():
        resolve = get_resolve()
        resolve.OpenPage(page_name)
    if page_name in pages:
        keys = pages[page_name].split('+')
        input_control.hotkey(*keys)
    return True

def save_project():
    if sys.platform == 'darwin':
        input_control.hotkey('command', 's')
    else:
        input_control.hotkey('ctrl', 's')
    return True

def click_ui_element(template_name):
    template_path = os.path.join('assets', 'templates', f'{template_name}.png')
    coords = vision.find_image_on_screen(template_path)
    if coords:
        input_control.click(coords[0], coords[1])
        return True
    return False

def apply_color_grade(style):
    switch_to_page('color')
    input_control.hotkey('ctrl', '4')
    input_control.type_text(style)
    input_control.press_key('enter')
    return True

def import_and_add_smart_media(media_type):
    context = vision.analyze_frame()
    selection = media_manager.get_smart_media_selection(media_type, context)
    if not selection or "dummy" in selection:
        return False
    path = os.path.join(media_manager.MUSIC_PATH if media_type == "music" else media_manager.SFX_PATH, selection)
    import_media([path])
    add_clips_to_timeline([selection])
    return True
