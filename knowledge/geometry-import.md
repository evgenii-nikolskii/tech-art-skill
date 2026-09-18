# Geometry Import

## Principle

Model import is a translation from a DCC scene into runtime asset data. A DCC file often contains much more than the geometry that the engine needs: cameras, lights, render settings, helper objects, constraints, embedded materials, textures, animation takes, and scene organization. Treat those as optional payloads, not as harmless defaults.

The default production import should be an asset-focused import:

- import the required mesh data and its transform hierarchy;
- preserve only the UV sets, vertex colors, skinning, morphs, LODs, and collision data that the asset actually uses;
- keep material slots and stable material names when they are needed for assignment;
- do not create cameras, lights, scene-level render objects, or embedded materials unless the workflow explicitly requires them.

Use a separate scene/layout import when the purpose is to reconstruct a shot, level blockout, or lighting setup. Do not use a scene import for ordinary reusable props or characters merely because the source file happens to contain a camera and lights.

## Export and Import Contract

Before changing importer settings, establish the contract between the DCC, interchange format, and target engine:

1. **Units and scale:** define the unit and the expected engine scale. A scale error affects physics, lighting falloff, animation speed, camera clipping, and procedural effects—not just visual size.
2. **Axes and handedness:** define up, forward, and handedness. Validate a known orientation marker and a deliberately asymmetric test mesh; a symmetric model can hide an axis conversion error.
3. **Transform policy:** decide whether transforms are applied before export or converted by the importer. Avoid compensating for a bad export with arbitrary per-asset scale overrides.
4. **Static versus skeletal:** select the asset class intentionally. A static mesh does not need a skeleton; a skinned mesh needs a stable hierarchy, bind pose, bone names/paths, weights, and the expected animation or morph data.
5. **Topology and triangulation:** decide where triangulation occurs and keep it deterministic. A change in triangulation can change normals, tangents, skin deformation, morph deltas, and baked texture correspondence.
6. **Normals and tangents:** choose whether to import authored normals/tangents or regenerate them. Preserve smoothing groups/hard edges required by the bake. Do not regenerate only one side of a baked normal-map workflow without rechecking the result.
7. **UV sets:** document the semantic purpose and index of every UV set, such as material UVs, lightmap UVs, or decal/detail UVs. Check for overlaps only where the target system permits them.
8. **Optional geometry data:** import vertex colors, blend shapes/morph targets, cloth data, custom attributes, and collision meshes only when a runtime system consumes them. Unused data increases memory and can create confusing downstream dependencies.

## What to Import by Default

| Payload | Default | Import when |
| --- | --- | --- |
| Meshes and required hierarchy | On | Always, for the requested asset |
| Normals and tangents | Contract-dependent | Authored data is required for the intended shading or bake; otherwise regenerate deterministically |
| UV0/material UVs | On | The material samples textures |
| Secondary/lightmap UVs | Conditional | The target lighting or baking workflow needs them |
| Vertex colors | Conditional | A shader, vertex animation, masking, or tooling uses them |
| Skinning/bones | Conditional | The asset deforms or is animated |
| Blend shapes/morph targets | Conditional | Facial animation, deformation, or a runtime morph system uses them |
| LODs | Conditional | The runtime uses authored LODs; verify naming/order and screen-size transitions |
| Collision geometry | Conditional | Physics or navigation needs authored collision; keep it separate from render geometry |
| Animation takes | Conditional | The file is an animation source or the asset contract includes animation |
| Cameras | Off by default | Shot/layout reconstruction or a camera-specific cinematic import |
| Lights | Off by default | Shot/layout reconstruction or a deliberately imported lighting rig |
| Constraints/helpers/locators | Off by default | A known downstream tool or runtime system consumes them |
| Embedded materials | Off by default | Look-development handoff or a controlled one-off scene import |
| Embedded textures | Off by default | A controlled interchange package explicitly owns those texture assets |

“Off by default” does not mean “never import.” It means the payload must have an identified consumer, owner, and validation step. In common engine importers, cameras and lights have explicit toggles, while material import can create new assets or assign embedded materials; leaving these options enabled can silently turn one model file into a scene and a collection of project assets.

## Cameras, Lights, and Scene Objects

Cameras and lights are usually authoring or presentation context, not part of a reusable model. Importing them can:

- create duplicate cameras or lights in the level;
- change exposure, shadows, reflections, or post-processing expectations;
- introduce objects with unexpected names, transforms, animation, or ownership;
- make a prefab/asset dependent on a source scene that the runtime does not need;
- produce misleading validation, because the asset looks correct only under imported lighting.

If they are required, import them into an explicitly named scene or cinematic asset, keep them in a dedicated hierarchy, and validate their units, orientation, clipping, intensity, color, shadow settings, and animation separately from mesh validation.

## Materials and Textures

Embedded DCC materials are not a portable representation of a production shader. They often contain renderer-specific nodes, unsupported procedural inputs, naming ambiguity, and incomplete texture semantics. Automatic conversion may produce a material that looks approximately correct while silently losing roughness, metallic, opacity mode, normal-map interpretation, or packed-channel assignments.

For reusable assets:

- import geometry and material slots, but assign project-owned materials through a material library or explicit mapping;
- keep material and texture creation disabled unless the importer is part of a controlled asset-ingestion pipeline;
- prevent duplicate materials on reimport by using stable names, search rules, or an explicit mapping table;
- inspect every material slot after import and record missing or unresolved references;
- validate the imported material with the texture-map rules from `knowledge/texture-maps.md` rather than trusting a DCC viewport match.

For a look-development or scene handoff, embedded materials may be useful as temporary previews. Label them as generated/interchange assets and do not let them replace the production material without a deliberate review.

## Static Mesh Validation

Check the imported asset at the target scale and under a neutral diagnostic material:

- orientation, pivot, origin, and world-space dimensions;
- transform values and absence of unintended global scale compensation;
- vertex/triangle counts and index format;
- normals, hard edges, tangents, and normal-map response under a moving directional light;
- UV set count, layout, density, and lightmap requirements;
- material-slot count, order, names, and unresolved references;
- authored LODs and transition behavior;
- collision representation and collision complexity;
- vertex colors, morphs, and custom attributes when present;
- absence of unwanted cameras, lights, helpers, textures, and generated materials.

## Skeletal Mesh Validation

In addition to static-mesh checks, validate:

- root bone and hierarchy stability;
- bind pose and rest-pose alignment;
- bone names/paths and maximum influences per vertex;
- weight normalization and deformation at extreme poses;
- animation range, frame rate, root motion, and imported takes;
- morph target deltas and normal behavior;
- whether animation-only files accidentally create duplicate meshes, materials, cameras, or lights.

## Reimport and Ownership

Importer settings are part of the asset pipeline and must be reproducible. Store or document presets for asset classes such as static prop, skeletal character, animation-only file, collision mesh, and scene/cinematic import.

On reimport, verify that the importer does not overwrite project-owned materials, manually assigned references, or generated collision/LOD assets unexpectedly. A clean reimport test should produce the same asset graph and the same validation results from the same source and preset.

When an import produces unexpected objects, first inspect the source scene and importer payload toggles. Do not delete generated assets until their ownership and references are known; remove or disable the unwanted payload at the import boundary, then reimport and validate the resulting asset graph.
