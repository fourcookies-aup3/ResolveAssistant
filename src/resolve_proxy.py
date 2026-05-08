import os
import sys

class MockResolve:
    def __init__(self):
        self.project_manager = MockProjectManager()
        self.media_storage = MockMediaStorage()

    def GetProjectManager(self):
        return self.project_manager

    def GetMediaStorage(self):
        return self.media_storage

    def Fusion(self):
        return "MockFusion"

    def OpenPage(self, page_name):
        print(f"Mock: Opening page {page_name}")

class MockProjectManager:
    def __init__(self):
        self.projects = {}
        self.current_project = None

    def CreateProject(self, project_name):
        if project_name in self.projects:
            print(f"Mock: Project '{project_name}' already exists.")
            return None
        project = MockProject(project_name)
        self.projects[project_name] = project
        self.current_project = project
        return project

    def GetCurrentProject(self):
        return self.current_project

    def LoadProject(self, project_name):
        if project_name in self.projects:
            self.current_project = self.projects[project_name]
            return self.current_project
        return None

class MockProject:
    def __init__(self, name):
        self.name = name
        self.media_pool = MockMediaPool()
        self.timelines = []

    def GetMediaPool(self):
        return self.media_pool

    def GetTimelineCount(self):
        return len(self.timelines)

    def GetCurrentTimeline(self):
        if self.timelines:
            return self.timelines[0]
        return None

    def SetCurrentTimeline(self, timeline):
        if timeline in self.timelines:
            # Move it to the front for simplicity in mock
            self.timelines.remove(timeline)
            self.timelines.insert(0, timeline)
            return True
        return False

class MockMediaPool:
    def __init__(self):
        self.root_folder = MockFolder("Root")
        self.current_folder = self.root_folder
        self.timelines = []

    def GetRootFolder(self):
        return self.root_folder

    def CreateEmptyTimeline(self, name):
        timeline = MockTimeline(name)
        self.timelines.append(timeline)
        # Link to current project if exists
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        project = pm.GetCurrentProject()
        if project:
            project.timelines.append(timeline)
        return timeline

    def AppendToTimeline(self, *args):
        # Can take multiple clips or a list of clips
        print(f"Mock: Appending {len(args)} items to timeline.")
        return True

class MockFolder:
    def __init__(self, name):
        self.name = name
        self.clips = []

    def GetClipList(self):
        return self.clips

class MockTimeline:
    def __init__(self, name):
        self.name = name

class MockMediaStorage:
    def AddItemListToMediaPool(self, items):
        if isinstance(items, str):
            items = [items]
        clips = [MockMediaPoolItem(item) for item in items]

        # Add to current project's media pool root
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        project = pm.GetCurrentProject()
        if project:
            project.GetMediaPool().GetRootFolder().clips.extend(clips)

        return clips

class MockMediaPoolItem:
    def __init__(self, path):
        self.path = path
    def GetName(self):
        return os.path.basename(self.path)

_resolve_instance = None

def get_resolve():
    global _resolve_instance
    if _resolve_instance:
        return _resolve_instance

    if os.getenv("USE_MOCK_RESOLVE", "true").lower() == "true":
        _resolve_instance = MockResolve()
        return _resolve_instance

    try:
        import DaVinciResolveScript as dvr_script
        _resolve_instance = dvr_script.scriptapp("Resolve")
        return _resolve_instance
    except ImportError:
        print("Warning: DaVinciResolveScript not found. Using MockResolve.")
        _resolve_instance = MockResolve()
        return _resolve_instance
