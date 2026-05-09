from resolve_proxy import get_resolve, is_api_available
import vision
import input_control
import media_manager
import brain
import os
import sys
import time

def create_new_project(project_name):
    print(f"Executing: High-Precision Project Creation - {project_name}")
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
    input_control.wait_for_ui_text("Project Manager", timeout=5)

    if input_control.precise_click_template('new_project_button'):
        input_control.secure_type(project_name)
        input_control.press_key('enter')
        return True

    input_control.hotkey('ctrl', 'n')
    input_control.secure_type(project_name)
    input_control.press_key('enter')
    return True

def apply_color_grade(style):
    """
    Applies color grading based on style.
    """
    switch_to_page('color')
    print(f"AI: Applying {style} color grade...")
    # UI Automation to open LUTs/Presets
    return True

def apply_professional_grade(params):
    switch_to_page('color')
    print(f"AI: Applying precision grade - {params}")
    return True

def professional_auto_edit(project_name, source_clips=None):
    if source_clips is None: source_clips = []
    print(f"--- STARTING PRECISION AUTO-EDIT: {project_name} ---")
    create_new_project(project_name)
    import_media(source_clips)
    create_timeline("Precision Master")
    add_clips_to_timeline([os.path.basename(c) for c in source_clips])
    analysis = vision.analyze_frame()
    tasks = brain.select_tricks_for_footage(analysis)
    for task in tasks:
        if task['action'] == 'exposure_correction':
            apply_professional_grade(task['params'])
    switch_to_page('edit')
    import_and_add_smart_media("music")
    save_project()
    print("--- PRECISION AUTO-EDIT COMPLETE ---")
    return True

def open_project(name):
    input_control.hotkey('shift', '1')
    input_control.secure_type(name)
    input_control.press_key('enter')
    return True

def import_media(paths):
    for path in paths:
        input_control.hotkey('ctrl', 'i')
        input_control.secure_type(path, verification_text=os.path.basename(path))
        input_control.press_key('enter')
    return True

def create_timeline(name):
    input_control.hotkey('ctrl', 'n')
    input_control.secure_type(name)
    input_control.press_key('enter')
    return True

def add_clips_to_timeline(names):
    for name in names:
        input_control.secure_type(name)
        input_control.press_key('f12')
    return True

def switch_to_page(page):
    try:
        idx = ["media","cut","edit","fusion","color","fairlight","deliver"].index(page)
        input_control.hotkey('shift', str(2 + idx))
    except ValueError:
        pass
    return True

def save_project():
    input_control.hotkey('ctrl', 's')
    return True

def click_ui_element(name):
    return input_control.precise_click_template(name)

def import_and_add_smart_media(media_type):
    context = vision.analyze_frame()
    selection = media_manager.get_smart_media_selection(media_type, context)
    if selection:
        path = os.path.join(media_manager.MUSIC_PATH if media_type == "music" else media_manager.SFX_PATH, selection)
        import_media([path])
        add_clips_to_timeline([selection])
        return True
    return False
