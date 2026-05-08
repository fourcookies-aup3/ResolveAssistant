import os
import sys

class MockResolve:
    def __init__(self, is_api_available=True):
        self.is_api_available = is_api_available
        if is_api_available:
            self.project_manager = MockProjectManager()
            self.media_storage = MockMediaStorage()
        else:
            self.project_manager = None
            self.media_storage = None

    def GetProjectManager(self):
        return self.project_manager

    def GetMediaStorage(self):
        return self.media_storage

    def Fusion(self):
        return "MockFusion" if self.is_api_available else None

    def OpenPage(self, page_name):
        if self.is_api_available:
            print(f"Mock API: Opening page {page_name}")
        else:
            print(f"API Unavailable: Cannot open page {page_name} via API.")

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
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        if pm:
            project = pm.GetCurrentProject()
            if project:
                project.timelines.append(timeline)
        return timeline

    def AppendToTimeline(self, *args):
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
        resolve = get_resolve()
        pm = resolve.GetProjectManager()
        if pm:
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

    # Default to False for production-readiness, but check env
    use_mock = os.getenv("USE_MOCK_RESOLVE", "false").lower() == "true"
    api_unavailable = os.getenv("RESOLVE_API_UNAVAILABLE", "false").lower() == "true"

    if api_unavailable:
        _resolve_instance = MockResolve(is_api_available=False)
        return _resolve_instance

    if use_mock:
        _resolve_instance = MockResolve(is_api_available=True)
        return _resolve_instance

    try:
        import DaVinciResolveScript as dvr_script
        _resolve_instance = dvr_script.scriptapp("Resolve")
        if not _resolve_instance:
             print("Warning: Resolve API connection failed. Falling back to UI automation.")
             return None
        return _resolve_instance
    except ImportError:
        # If not Studio and not explicitly mocking, we fall back to UI automation
        return None

def is_api_available():
    res = get_resolve()
    if res is None:
        return False
    if isinstance(res, MockResolve):
        return res.is_api_available
    return True
