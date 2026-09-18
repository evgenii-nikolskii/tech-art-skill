# Scene Audit

## Purpose

A scene audit is a structured, read-only examination of a scene and its directly required dependencies. It describes what is present, what is missing or suspicious, which systems influence the result, and what should be investigated next. It does not silently repair assets or redesign the scene.

The audit must distinguish:

- **Observed facts:** objects, references, settings, counts, warnings, and measurable resource usage;
- **Likely risks:** evidence-based consequences such as duplicate lights, missing materials, invalid references, or excessive draw calls;
- **Artistic judgments:** whether the composition, lighting, color, or visual quality is desirable. These require an explicit target or comparison reference.

## Scope and Point of Entry

Start from the scene or location named by the user. Inspect the scene hierarchy and the dependencies required to understand it. Do not scan the whole project unless the user asks for a project-wide audit.

Record the audit scope:

- scene/level path and revision, if available;
- target platform, render pipeline, quality tier, and intended use;
- whether the scene is a prototype, production level, cinematic, test map, or reusable template;
- included and excluded subtrees or systems;
- evidence sources and limitations.

If the intended target platform, visual reference, or performance budget is unknown, report that uncertainty instead of treating a generic threshold as a failure.

## Audit Order

Use this order so that missing dependencies and scene structure are understood before visual or performance conclusions:

1. Identify the point of entry and applicable naming system.
2. Inventory the hierarchy and scene-level settings.
3. Check dependency integrity, including null and missing references.
4. Audit transforms, ownership, and object roles.
5. Audit cameras, lights, environment, and render settings.
6. Audit renderers, materials, textures, and shader variants.
7. Audit geometry, LODs, culling, batching, and instancing.
8. Selectively audit GPU Instancing and SRP Batcher compatibility for repeated or numerous renderers.
9. Audit physics, collision, navigation, probes, and gameplay-supporting objects when in scope.
10. Check performance evidence and identify likely bottlenecks.
11. Produce prioritized findings, evidence, risks, and suggested next checks.

## Scene Inventory

Create a compact inventory before interpreting the scene:

- root objects and hierarchy depth;
- active/enabled versus inactive/disabled objects;
- static, dynamic, animated, pooled, and editor-only objects;
- mesh renderers, skinned renderers, particle/VFX systems, decals, terrain, water, and UI/canvas systems;
- cameras, lights, reflection/refraction systems, volumes, probes, fog, sky/environment objects;
- colliders, rigidbodies, joints, triggers, navigation surfaces, agents, and blockers;
- scripts/components with scene-level responsibilities;
- materials, textures, meshes, animation controllers, audio, and other referenced assets;
- particle/VFX system count, active emission, screen coverage, transparency, and layering;
- duplicate or generated objects and likely source ownership.

Counts alone are not findings. Interpret them relative to the scene's role, camera coverage, target hardware, and runtime behavior.

## Hierarchy, Naming, and Ownership

Use the naming-audit workflow for names in the selected scene zone. Check for:

- meaningful names for roots, groups, instances, cameras, lights, volumes, and gameplay markers;
- duplicated names that make logs, search, or automation ambiguous;
- imported DCC names or temporary suffixes that should not survive production;
- inconsistent prefixes, namespaces, or asset-role labels;
- objects owned by the wrong scene/prefab/level layer;
- hidden or disabled objects with unclear purpose;
- scene-local overrides that diverge from the source prefab or asset.

Do not rename production content merely because a preferred convention exists. First establish whether the scene is a prototype or production asset and report the scope of any naming work separately.

## Dependency Integrity

Check every dependency required by the scene and record:

- null references;
- missing assets or broken links;
- missing scripts/components;
- unresolved material slots;
- missing textures, animation clips, controllers, audio, probes, or volume profiles;
- incompatible or duplicate skeleton/material/asset references;
- references crossing scene, package, or ownership boundaries unexpectedly.

Continue the audit after recording a missing dependency. Explain which conclusions are weakened by the missing data and which checks remain reliable.

## Transforms and Spatial Integrity

Inspect representative objects and outliers for:

- unexpected non-uniform or negative scale;
- unapplied rotations or scale on imported roots;
- wrong units or scene-wide scale;
- misplaced pivots and origins;
- objects far outside the intended playable bounds;
- hidden overlaps, z-fighting risk, interpenetration, and floating props;
- inconsistent parent spaces or inherited transforms;
- precision-sensitive coordinates and excessive distance from world origin;
- inconsistent bounds that affect culling, lighting, navigation, or physics.

For large scenes, sample by spatial region and by object class; do not infer the whole scene from one visually representative location.

## Cameras and Composition

Audit cameras as technical scene dependencies before making aesthetic claims:

- active camera and fallback behavior;
- projection type, field of view/orthographic size, aspect handling, and clipping planes;
- camera transforms, parent hierarchy, animation, and constraints;
- culling masks/layers and visibility exclusions;
- post-processing/volume influence and exposure ownership;
- camera-relative effects, streaming bounds, and cut/shot markers when relevant.

If the scene's purpose is not a shot or cinematic, report unused imported cameras as scene clutter or ownership risk rather than assuming they should influence the runtime view.

## Lighting and Environment

Inventory light sources and environment controls:

- light count, type, range, intensity, color, shadow settings, and baked/realtime mode;
- duplicate or overlapping lights and lights outside the playable area;
- shadow distance, resolution, cascades, contact shadows, and filtering;
- sky, ambient, fog, exposure, tone mapping, reflection probes, light probes, and volumes;
- baked lighting data, lightmap settings, UV requirements, and stale bake indicators;
- ownership of lighting between scene, prefab, volume, and runtime systems.

Do not call lighting “wrong” without a target look or reference. Do report technical contradictions such as multiple exposure owners, missing probes where materials depend on them, or imported DCC lights that are not part of the intended runtime setup.

## Renderers, Materials, and Textures

For representative and high-cost objects, inspect:

- renderer enabled state, sorting/layer behavior, shadows, probes, lightmap flags, and motion-vector settings;
- material count per renderer and avoidable material-instance duplication;
- shader family, keywords/variants, render queue, blend mode, culling, and transparency;
- missing or unresolved material slots;
- texture import settings, resolution, mipmaps, sRGB/linear interpretation, normal-map type, and platform format;
- packed-channel contracts and material parameters that differ from the asset source;
- transparent surfaces, overdraw, decals, particles, and effects that require special validation.

Use `knowledge/texture-maps.md` for texture semantics and compression. Do not judge a material from a thumbnail alone; verify its imported data contract and the shader that consumes it.

## Geometry, LOD, and Visibility

Check:

- vertex/triangle counts and high-cost meshes;
- duplicated geometry that could be instanced or merged appropriately;
- LOD presence, ordering, screen thresholds, transitions, and shadow/collision LOD behavior;
- frustum, distance, occlusion, portal, and streaming culling;
- bounds that are too large, too small, or invalid;
- static/dynamic flags and batching/instancing eligibility;
- skinned mesh bone counts, update rates, and off-screen behavior;
- terrain, foliage, crowds, and procedural systems separately from ordinary props.

An object is not automatically a problem because it has high geometry complexity. Relate cost to visibility, update frequency, target platform, and measured frame impact.

## GPU Instancing

Recommend GPU Instancing when the scene contains many repeated copies of the same render mesh and the copies can share the same material/shader setup. Typical candidates are repeated props, foliage, rocks, modular parts, and crowds of identical rigid meshes.

Audit the conditions before recommending it:

- the instances use the same mesh and compatible material/shader;
- the shader supports GPU Instancing and the material option is enabled where required;
- per-instance variation is limited to supported instanced properties rather than unique material assets;
- the objects are renderable as instances and are not skinned meshes that require independent deformation;
- bounds, culling, shadows, light probes, LODs, and per-instance data remain correct;
- the target platform and render path benefit from the reduced draw submission cost.

The recommendation is stronger when there are many copies of one mesh/material pair. It is weaker when objects only look generally similar but use different meshes, materials, shaders, lightmap state, or per-object properties. Instancing reduces repeated draw submission; it does not remove vertex, pixel, shadow, overdraw, memory, or culling costs.

In Unity SRP projects, check the interaction with SRP Batcher before changing a shader. A GameObject that is SRP Batcher-compatible is rendered through the SRP Batcher instead of ordinary GPU Instancing. If GPU Instancing is still the measured winner for a repeated mesh/material group, use an intentional instancing path and verify the result with the Frame Debugger and Profiler; do not disable SRP Batcher compatibility speculatively.

## SRP Batcher

When the scene contains many renderers—not necessarily identical meshes—check whether their shaders and materials are compatible with the SRP Batcher. This is the preferred direction for reducing CPU render-state setup when there are many ordinary objects sharing a compatible SRP shader family.

Audit:

- whether the project uses a Scriptable Render Pipeline and the SRP Batcher is enabled for the target pipeline;
- which shaders are compatible and which renderers fall back to the standard SRP path;
- whether materials use the expected constant-buffer/property layout for the pipeline;
- whether `MaterialPropertyBlock` or other per-renderer state prevents compatibility;
- whether particles, special render paths, transparent effects, skinned meshes, or custom passes have different support or costs;
- whether the Frame Debugger shows SRP Batcher draws and the Profiler shows a meaningful CPU benefit on the target device.

Recommend SRP Batcher when the scene has many different objects and there is no strong same-mesh/same-material grouping for instancing. Do not describe “many objects” alone as proof of compatibility: compatibility is a shader/material/render-path property and must be verified per group.

### Choosing Between GPU Instancing and SRP Batcher

Use this decision rule for a Unity SRP scene:

| Scene pattern | First recommendation | Validation |
| --- | --- | --- |
| Many copies of the same mesh with the same material | GPU Instancing | Confirm shader support, instance grouping, culling/LOD behavior, and measured frame cost |
| Many different meshes/objects using compatible SRP shaders/materials | SRP Batcher | Inspect compatibility and compare CPU render time in the Profiler |
| Same mesh but many unique materials or incompatible shaders | Fix material/shader grouping first | Determine whether materials can be shared or whether a deliberate instancing path is justified |
| SRP Batcher-compatible objects where Instancing is also enabled | SRP Batcher usually takes precedence | Verify the actual path; do not infer Instancing from the material checkbox |

These are optimization recommendations, not automatic fixes. A scene audit should report the repeated mesh/material groups, the compatibility blockers, the active render path, and the measured result before proposing a shader or renderer change.

## Physics, Navigation, and Supporting Systems

When in scope, inspect:

- render geometry versus collision geometry;
- unexpected mesh colliders, excessive convex hull complexity, or missing triggers;
- rigidbody/kinematic state, layers, collision matrix, and joints;
- navigation surfaces, modifiers, links, agent settings, holes, and blockers;
- reflection/light probes and probe volumes;
- audio emitters, occlusion, reverb zones, and distance settings;
- spawn points, gameplay markers, streaming volumes, and runtime-only objects.

Check that supporting systems use the intended asset representation rather than accidentally consuming render meshes, imported cameras, or editor helpers.

## Performance Evidence

Separate measured evidence from static risk indicators.

**Measured evidence** may include:

- CPU/GPU frame time and per-pass timings;
- draw calls, batches, instanced draws, triangles, vertices, and shader variants;
- overdraw, transparency cost, shadow cost, skinning/animation time, particle time, and memory;
- streaming, loading, garbage collection, and frame spikes;
- target-device captures under representative camera positions.

**Static risk indicators** include:

- duplicated materials preventing batching;
- missing LODs or culling on large repeated assets;
- excessive realtime lights/shadows;
- many active particle/VFX systems, especially transparent effects with large screen coverage or multiple overlapping layers;
- high-resolution textures with no platform override;
- transparent effects covering large screen areas;
- oversized bounds or objects far from the scene origin;
- unnecessary cameras, lights, imported materials, or disabled-but-referenced systems.

Do not present static indicators as measured regressions. Recommend a capture or profiler check when the evidence is insufficient.

## Particle Systems and Overdraw

When a scene contains many particle or VFX systems, explicitly warn about overdraw risk. This is especially important for transparent quads, soft particles, smoke, fog, fire, additive glows, ribbons, decals, and fullscreen or near-fullscreen effects.

Audit:

- number of active systems and emitters visible from representative cameras;
- particle count, lifetime, size, spawn rate, sorting, and screen coverage;
- number of transparent layers each particle overlaps;
- blend mode, shader complexity, soft-particle/depth sampling, distortion, and additional texture samples;
- whether particles cast/receive shadows, write motion vectors, or trigger expensive lighting paths;
- off-screen simulation and rendering behavior;
- platform-specific overdraw and fill-rate evidence.

Do not infer overdraw cost from particle count alone. A small number of large overlapping transparent particles can be more expensive than many small opaque or tightly culled particles. Confirm the risk with an overdraw visualization and GPU timing on representative camera views.

If evidence is not available, report the finding as a performance risk rather than a confirmed regression. Suggested controls include reducing screen coverage, lifetime, spawn rate, overlap, particle size, shader passes, transparent layers, or unnecessary per-particle features; each change can affect the intended visual density and look.

## Finding Severity and Report Format

Use severity based on impact and evidence:

- **Critical:** scene cannot load, build, render, or run its primary function;
- **High:** likely causes severe visual breakage, missing content, memory failure, or a major target-platform/performance risk;
- **Medium:** meaningful correctness, maintainability, or localized performance issue;
- **Low:** cleanup, consistency, or small optimization with limited immediate impact;
- **Informational:** observed context, assumption, or follow-up suggestion without a defect claim.

Each finding should include:

1. location/object/asset;
2. observed evidence;
3. why it matters and which system is affected;
4. confidence and any missing evidence;
5. suggested next check or control;
6. whether the action is safe to automate or requires artistic/technical approval.

Prioritize by user impact, platform risk, scope of affected content, and confidence—not by how easy the cleanup is.

## Audit Quality Criteria

Before delivering an audit, confirm that:

- the scope and target assumptions are explicit;
- the hierarchy and dependencies were inventoried before interpretation;
- null/missing references were recorded and did not silently stop the audit;
- naming issues are separated from technical defects;
- visual judgments are not presented as objective failures without a reference;
- measured performance and static risk are clearly separated;
- cameras, lights, materials, and imported scene payloads were checked;
- repeated renderers were assessed for GPU Instancing versus SRP Batcher using the appropriate compatibility checks;
- particle/VFX systems were checked for overdraw risk and transparent screen coverage;
- findings point to concrete evidence and a next action;
- the report distinguishes confirmed issues, likely risks, and unknowns.
