# Example Scene Audit Report

Input: `evals/fixtures/scene_problematic.json`

Status: **FAIL**

Summary:

- 15 objects
- 12 mesh renderers
- 1 particle system
- 2 errors
- 5 warnings

Findings:

- **Error — missing dependency:** `Props/Broken_Prop` references `SM_Missing` and has a null material.
- **Warning — GPU Instancing:** six identical crate renderers support instancing but have it disabled.
- **Warning — SRP Batcher:** the scene has many renderers, but all are marked incompatible with the enabled SRP Batcher.
- **Warning — particle overdraw:** the smoke system has 1,200 transparent particles, 35% screen coverage, and four overlap layers.
- **Warning — scene payload:** imported camera and light are present although the scene is asset-focused.

Recommended next steps:

1. Repair or remove the broken prop references.
2. Evaluate GPU Instancing for the crate group and verify the actual render path.
3. Inspect SRP Batcher compatibility blockers in the shader/material setup.
4. Capture overdraw and GPU timing for the smoke effect from representative cameras.
5. Remove imported camera/light payloads or move them into an explicit cinematic scene.
