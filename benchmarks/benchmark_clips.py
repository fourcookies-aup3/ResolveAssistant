import time
import os
import sys
from unittest.mock import MagicMock

# Mock GUI modules before importing src modules
sys.modules['pyautogui'] = MagicMock()
sys.modules['pynput'] = MagicMock()

# Mock Resolve API objects
class MockClip:
    def __init__(self, name):
        self._name = name
    def GetName(self):
        return self._name

class MockMediaPool:
    def AppendToTimeline(self, clips):
        return True

class MockProject:
    def GetCurrentTimeline(self):
        return True
    def GetMediaPool(self):
        return MockMediaPool()

class MockProjectManager:
    def GetCurrentProject(self):
        return MockProject()

class MockResolve:
    def GetProjectManager(self):
        return MockProjectManager()

# Add src to path
sys.path.append(os.path.abspath('src'))

# Mock resolve_proxy
import resolve_proxy
resolve_proxy.is_api_available = lambda: True
resolve_proxy.get_resolve = lambda: MockResolve()

import editor_actions

def benchmark_add_clips_to_timeline(num_pool_clips, num_targets):
    # Setup
    all_clips = [MockClip(f"clip_{i}") for i in range(num_pool_clips)]
    target_names = [f"clip_{i}" for i in range(num_targets)]

    # Patch list_clips_in_media_pool to return our large list
    editor_actions.list_clips_in_media_pool = lambda: all_clips

    start_time = time.time()
    editor_actions.add_clips_to_timeline(target_names)
    end_time = time.time()

    return end_time - start_time

if __name__ == "__main__":
    num_pool = 10000
    num_targets = 5000
    print(f"Benchmarking add_clips_to_timeline with {num_pool} clips in pool and {num_targets} targets...")
    duration = benchmark_add_clips_to_timeline(num_pool, num_targets)
    print(f"Duration: {duration:.4f} seconds")
