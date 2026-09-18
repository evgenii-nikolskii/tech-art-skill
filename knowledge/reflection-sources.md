## Unity

### Built-in Render Pipeline note

In the Built-in Render Pipeline, global environment reflections are controlled from the Lighting settings. A custom cubemap or the scene skybox can be selected as the reflection source. If a skybox is unavailable while a reflection probe is capturing with skybox clear flags, the probe uses its own `backgroundColor`.

The camera background color is a camera-clear fallback, not a guaranteed universal reflection source.

### URP fallback without a local probe

In URP, when no local Reflection Probe affects an object, the renderer uses the global or default environment reflection. In the usual setup this is the reflection cubemap associated with the Skybox source in the Lighting settings.

When no Skybox Material is assigned, Unity can still provide a hidden default Reflection Probe containing the built-in Default Skybox cubemap. Therefore, the absence of a Reflection Probe GameObject in the scene does not necessarily mean that the object has no reflection source.

For URP, the practical fallback is:

1. A local Reflection Probe, when one affects the object.
2. The global or default reflection cubemap.
3. The built-in Default Skybox cubemap when Unity's hidden default reflection probe is active.

The camera background color is not the standard universal fallback for reflection data in URP. It controls camera background clearing and may visually resemble the reflection fallback in some configurations, but it should not be treated as the same source. When diagnosing a reflection, inspect the local probe volumes, the renderer's Reflection Probes setting, the URP asset reflection-probe settings, the Lighting settings, the Skybox Material, and the active default reflection data separately.
