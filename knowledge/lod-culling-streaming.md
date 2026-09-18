# LOD, Culling, and Streaming

## Principle

Visibility systems trade visual continuity and memory for frame time. LOD, culling, and streaming decisions must be made from camera coverage, object importance, target platform, and measured transitions—not from object count alone.

## LOD

Audit:

- authored LOD ordering and geometric validity;
- screen-relative or distance thresholds;
- transition popping, silhouette changes, material changes, and shadow/collision behavior;
- skinned mesh LOD bone reduction and animation cost;
- foliage, crowds, particles, and impostors as separate asset classes;
- whether the highest LOD is used too far away or lower LODs are missing.

Do not optimize a hero asset with the same thresholds as a background prop. Validate LODs from the intended camera paths and at the target resolution.

## Culling

Check frustum, distance, occlusion, portal, layer, instance, and streaming culling. Investigate bounds that are too large and prevent culling, or too small and cause popping. Include shadows, probes, VFX, and skinned meshes because their effective visibility may differ from the visible renderer.

## Streaming

Record asset and scene ownership, load/unload boundaries, dependencies, preload behavior, memory peaks, and fallback content. Validate traversal, teleportation, camera cuts, additive scene changes, and low-bandwidth or slow-storage conditions. A streamed scene must not depend on an object that unloads earlier than its consumers.

## Validation

Use representative camera paths and profiler captures. Check visual continuity, load latency, memory peak, draw-call changes, and whether culling/streaming actually reduces work. Treat missing LODs, oversized bounds, and duplicated dependencies as evidence-based findings with a concrete next check.
