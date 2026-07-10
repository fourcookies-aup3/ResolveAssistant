## 2026-07-10 - [Grayscale Template Caching]
**Learning:** Grayscale template matching combined with memory caching significantly reduces latency in UI automation. Converting both the screen and template to grayscale reduces channel processing by ~66%, and caching prevents redundant disk I/O.
**Action:** Always prefer grayscale matching and template caching for UI element detection unless color is a critical discriminator.
