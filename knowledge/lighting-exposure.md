# Lighting and Exposure

## Principle

Lighting is the combined result of sources, environment, material response, exposure, color transforms, shadows, reflections, and post-processing. A visual difference is not automatically a bug; diagnose ownership and signal flow before changing intensity or color.

## Ownership

Identify which system owns:

- key/fill/rim or directional lights;
- sky/environment and ambient contribution;
- exposure and adaptation;
- tone mapping and color grading;
- shadows, contact shadows, probes, and baked lighting;
- fog, volumetrics, bloom, and other light-dependent effects.

Warn when multiple systems control the same result or when a scene relies on an imported DCC light/camera that is not part of the runtime contract.

## Technical Audit

Check light type, range, intensity, color space, shadow mode, culling/layers, update frequency, and platform tier. Check environment reflections and probes alongside lighting because material response may appear incorrect when the reflection source is wrong.

Inspect exposure histogram or luminance ranges, auto-exposure limits/speed, view transforms, tone mapping, and post-process volumes. Avoid compensating for an incorrect exposure owner by changing every material or light.

## Baked and Dynamic Lighting

Confirm which objects and lights participate in baked, mixed, or realtime lighting. Check stale data, lightmap UVs, probe coverage, dynamic-object response, shadow distance, and transitions between lighting systems. A correct static bake can still leave moving objects without valid lighting data.

## Validation

Use a neutral diagnostic scene, controlled reference exposure, and representative camera views. Compare direct light, indirect light, shadow, reflection, and post-processing contributions separately. Record target platform, quality level, visual reference, and whether the finding is technical or aesthetic.
