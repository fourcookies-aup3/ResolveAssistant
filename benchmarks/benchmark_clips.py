import time
import os
import sys
from unittest.mock import MagicMock

# Mock dependencies to avoid import errors and environment issues
class MockResolve:
    def __init__(self):
        self.pm = MockProjectManager()
    def GetProjectManager(self):
        return self.pm

class MockProjectManager:
    def __init__(self):
        self.project = MockProject()
    def GetCurrentProject(self):
        return self.project

class MockProject:
    def __init__(self):
        self.mp = MockMediaPool()
    def GetCurrentTimeline(self):
        return MagicMock()
    def GetMediaPool(self):
        return self.mp

class MockMediaPool:
    def __init__(self):
        self.root = MockFolder()
    def GetRootFolder(self):
        return self.root
    def AppendToTimeline(self, clips):
        # Verification that we actually got the right number of clips
        self.last_appended_count = len(clips)
        return True

class MockFolder:
    def __init__(self):
        self.clips = []
    def GetClipList(self):
        return self.clips

class MockClip:
    def __init__(self, name):
        self.name = name
        self.path = f"/path/to/{name}"
    def GetName(self):
        return self.name

# Mock the proxy
sys.modules['resolve_proxy'] = MagicMock()
import resolve_proxy
resolve_proxy.is_api_available.return_value = True
mock_resolve = MockResolve()
resolve_proxy.get_resolve.return_value = mock_resolve

# Mock vision and input_control
sys.modules['vision'] = MagicMock()
sys.modules['input_control'] = MagicMock()

# Now we can import the function to test
# We need to make sure 'src' is in path
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
from editor_actions import add_clips_to_timeline

def benchmark():
    # Setup 10,000 clips
    pool_clips = [MockClip(f"clip_{i}.mp4") for i in range(10000)]
    mock_resolve.pm.project.mp.root.clips = pool_clips

    # 5,000 targets
    targets = [f"clip_{i}.mp4" for i in range(0, 10000, 2)]

    start = time.time()
    add_clips_to_timeline(targets)
    end = time.time()

    duration = end - start
    print(f"Optimized Execution time: {duration:.4f}s")

    # Simple verification
    if mock_resolve.pm.project.mp.last_appended_count == 5000:
        print("Verification: Successfully matched 5000 clips.")
    else:
        print(f"Verification: FAILED. Expected 5000, got {mock_resolve.pm.project.mp.last_appended_count}")

if __name__ == "__main__":
    benchmark()
