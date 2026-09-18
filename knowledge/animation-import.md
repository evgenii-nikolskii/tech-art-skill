# Animation Import

## Principle

Animation import is the translation of motion data onto a runtime skeleton. The animation is not correct merely because the clip plays: it must use the intended skeleton, reference pose, coordinate system, time range, and motion ownership.

The default production import should be animation-focused:

- import only the animation tracks and morph curves required by the target asset;
- bind the clip to an existing, validated skeleton whenever the animation is intended for an existing character;
- do not import a second skeletal mesh, materials, textures, cameras, lights, helpers, or scene settings unless the workflow explicitly requires them;
- choose root-motion, retargeting, and compression policies before importing a library of clips.

Use a full skeletal-scene import only for a controlled character handoff or cinematic reconstruction. A normal animation file should not create a new character asset graph by accident.

## Export and Import Contract

Before importing, document:

1. **Target skeleton:** the exact skeleton asset, bone hierarchy, bone names/paths, reference pose, and expected rest-pose orientation. An animation with a similar-looking character is not necessarily compatible.
2. **Root policy:** decide whether movement belongs in the animation's root track, in-place motion, or a separate gameplay controller. Do not mix root motion and code-driven movement without an explicit ownership rule.
3. **Coordinate system and units:** use the same axes, handedness, scale, and time units as the mesh import. A scale or axis conversion error can look like incorrect root motion, foot sliding, or a rotated character.
4. **Time range and rate:** define source frame rate, target sample rate, start/end frame, preroll/postroll, and whether the export contains one clip or multiple takes. Avoid relying on an incidental DCC timeline range.
5. **Deformation data:** decide whether the clip includes bone animation, morph/blend-shape curves, or both. Morph names and curve semantics must match the target mesh.
6. **Rig evaluation:** bake constraints, IK, space switches, and procedural controls into exportable joints or morph curves when the runtime will not evaluate the original rig. Do not assume DCC constraints survive interchange.
7. **Retargeting mode:** choose a generic/exact skeleton workflow or a humanoid/retargetable workflow. Retargeting is a transformation with trade-offs, not a substitute for skeleton compatibility.

## What to Import by Default

| Payload | Default | Import when |
| --- | --- | --- |
| Bone transform tracks | On | The clip drives the target skeleton |
| Root transform track | Contract-dependent | Root motion is consumed by the animation system |
| Morph/blend-shape curves | Conditional | Facial, corrective, or other vertex deformation is required |
| Animation events/markers | Conditional | The runtime has an agreed event naming and timing contract |
| Mesh geometry | Off for animation-only files | The file is also the source of a new skeletal mesh |
| Skeleton asset | Reuse existing | Create only for the first validated character import |
| Materials/textures | Off | A controlled character scene/look-development handoff requires them |
| Cameras/lights | Off | A cinematic or scene reconstruction explicitly needs them |
| DCC constraints/controls/helpers | Off | A downstream tool explicitly consumes those objects; otherwise bake their result |

An animation-only import should leave the project with an animation asset referencing the intended skeleton, not a duplicate mesh, skeleton, material set, or scene hierarchy.

## Skeleton Compatibility and Reference Pose

The safest workflow is to import the character mesh and skeleton once, validate them, and target that existing skeleton for subsequent animation imports. Check:

- root bone identity and hierarchy;
- bone names and paths, including namespaces and suffixes;
- parent-child relationships and bone order where the importer requires it;
- reference/rest pose and bone local axes;
- bone lengths and proportions when using exact-skeleton playback;
- required tracks and whether missing bones are intentionally static or indicate an export error;
- extra bones, virtual bones, IK bones, and twist bones that may affect retargeting.

Do not update the production reference pose from every incoming animation. A different first frame or a changed bind pose can shift the whole character and invalidate existing clips. If a source uses a different reference pose, fix it in a dedicated retargeting or correction step and validate the result before publishing.

## Root Motion

Root motion answers who owns the character's world-space movement:

- **Root-motion clip:** the animation carries horizontal and/or vertical displacement; the runtime extracts and applies it to the actor.
- **In-place clip:** the animation cycles locally while gameplay, navigation, or a controller moves the actor.
- **Hybrid:** only selected components, such as yaw or forward displacement, are extracted; every retained component must be documented.

Validate root motion on a floor with a visible world-space trajectory. Check forward distance, turning, vertical motion, facing direction, loop continuity, and contact timing. A clip can look correct in a DCC viewport while moving twice, not at all, or along the wrong axis in the engine.

Do not solve root-motion errors by scaling the character or shifting the mesh under the skeleton. Identify whether the error comes from axis conversion, root/hips selection, baked transforms, extraction settings, or double application by gameplay code.

## Clips, Takes, and Timing

Prefer one clearly named clip per file or an explicitly defined take table. For each clip, record:

- source and target frame rate;
- exact start/end frames and whether end time is inclusive;
- loop behavior and a loop-safe first/last pose;
- additive/reference pose if the clip is additive;
- root-motion policy;
- event/marker locations;
- intended skeleton and retargeting profile.

Avoid importing editor preview ranges, camera cuts, or unrelated scene animation as character clips. Remove preroll and postroll unless they are needed for blending or simulation warm-up.

Resampling and key reduction are lossy operations. They can reduce memory and evaluation cost but may introduce foot sliding, jitter, hand drift, facial popping, or inaccurate root motion. Set error tolerances per class of animation and inspect fast motion, contacts, facial curves, and extreme poses after compression.

## Humanoid and Generic Workflows

- **Exact/generic skeleton:** preserves the authored hierarchy and is appropriate when the target skeleton must be driven precisely. It requires compatible bone names/paths, reference pose, and local axes.
- **Humanoid/retargetable skeleton:** maps motion through a semantic body model and can share clips across proportions. It may alter limb lengths, twist behavior, foot contacts, spine motion, or non-human appendages.

Choose the workflow based on the intended use. Do not classify every biped as humanoid if mechanical parts, tails, extra limbs, facial bones, or precise authored proportions matter. Validate retargeted motion on short, tall, and extreme-pose examples before importing a large library.

## Morph Targets and Curves

Import morph/blend-shape tracks only when the target mesh contains matching shapes. Verify:

- exact curve names and namespace rules;
- value range and whether values are normalized or percentage-based;
- frame rate and key reduction on facial curves;
- interaction with bone deformation and corrective shapes;
- missing, duplicated, or unsupported curves.

Do not silently discard curves that drive gameplay, facial sync, cloth, or corrective deformation. Report them as missing dependencies and decide whether to rename, remap, bake, or intentionally remove them.

## Animation Import Validation

Validate every new animation against a neutral test actor and diagnostic scene:

- the intended skeleton is referenced and no duplicate skeleton was created;
- reference pose matches the target mesh;
- root, hips, feet, hands, and head follow expected trajectories;
- no axis flip, scale drift, shearing, or unexpected offsets occur;
- clip length, frame rate, start/end frames, and loop boundary are correct;
- root-motion distance and facing match the source contract;
- foot contacts, hand contacts, and fast arcs survive resampling/compression;
- morph curves reach the intended values without popping;
- animation events/markers occur on the intended frames;
- no unwanted mesh, materials, textures, cameras, lights, controls, or helpers were imported;
- missing tracks and warnings are either resolved or explicitly accepted.

For an animation library, validate representative clips: idle, walk/run, sharp turns, jump/fall, stop/start, additive pose, facial animation, and the clip with the greatest root displacement. A single successful idle import is not evidence that the whole library is compatible.

## Reimport and Ownership

Store or document importer presets for animation-only, skeletal-mesh-with-animation, morph-only, cinematic, and retargeted imports. On reimport, verify that the importer preserves the selected skeleton, clip names, event data, root-motion policy, and project-owned references.

If an animation import creates unexpected assets, inspect the source selection and importer payload toggles before deleting anything. Disable mesh/material/texture/scene payloads at the import boundary, reimport into the correct folder, and compare the resulting asset graph with the expected animation-only contract.
