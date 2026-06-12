## 2025-05-14 - Robust Hash Map Optimization for Clip Lookups
**Learning:** When replacing nested loops with hash maps for object lookups based on optional attributes (like `clip.path`), always verify the attribute exists and is not None before processing. In this codebase, some Mock objects or API items might have a `path` attribute that is `None`, which causes `os.path.basename()` to raise a `TypeError`.
**Action:** Use `if hasattr(obj, 'attr') and obj.attr:` patterns when building lookup tables from object attributes to ensure resilience against incomplete data.
