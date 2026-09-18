# Asset Validation

## Purpose

Asset validation turns technical-art expectations into repeatable checks before content is published or used by a scene. It should detect broken dependencies and contract violations while preserving artistic review for choices that cannot be judged mechanically.

## Validation Scope

Define:

- asset type and point of entry;
- source revision and importer preset;
- target engine, render pipeline, platform, and quality tier;
- required dependencies and allowed generated outputs;
- checks that are errors, warnings, informational, or artist-approved exceptions.

Do not run a project-wide validation when the request is scoped to one asset or folder unless explicitly asked.

## Common Checks

Validate as applicable:

- naming and ownership;
- null/missing references and unresolved dependencies;
- import type, units, axes, transforms, and scale;
- mesh topology, normals, tangents, UV sets, lightmap UVs, LODs, and collision;
- skeleton compatibility, animation clips, root motion, and morph curves;
- material shader, render state, keywords, and material slots;
- texture color space, channel packing, mipmaps, resolution, and platform compression;
- scene payloads such as cameras, lights, embedded materials, helpers, and imported textures;
- particle/VFX bounds, overdraw risk, and runtime ownership;
- memory, draw-call, shader-variant, and platform budgets where evidence exists.

## Severity and Exceptions

Each result should include location, evidence, severity, confidence, and remediation or next check. Support explicit exceptions with an owner, reason, scope, and expiry/review condition. Do not hide a failure by lowering its severity without recording why.

## Pipeline Behavior

Validation should be deterministic and safe to run repeatedly. Separate read-only checks from optional repair or normalization. Generated assets should be reproducible, and validation should not overwrite source content, project-owned materials, manual assignments, or scene layout.

## Report

Return a summary of pass/fail/warning counts, then prioritized findings. Include unknowns and skipped checks caused by missing tools or dependencies. Distinguish confirmed contract violations from likely performance risks and subjective visual review items.

## Executable Snapshot Baseline

The repository includes a platform-neutral baseline validator at `tools/scene_validator.py`. Engine integrations should export a normalized scene snapshot with:

- `metadata` for scene, engine, pipeline, platform, and revision;
- `settings` for render-pipeline flags and validation thresholds;
- `assets` registries for meshes, materials, shaders, textures, animations, and controllers;
- `objects` with stable paths, types, references, render compatibility, and particle metrics.

The baseline currently detects missing references, unexpected imported cameras/lights, repeated mesh/material groups that are candidates for GPU Instancing, SRP Batcher compatibility risks, and transparent particle overdraw risks. It returns structured findings with severity, evidence, and recommendation, and never modifies source content.

Use the JSON fixtures and unit tests under `evals/fixtures/` and `tests/` as the contract for future Unity and Unreal adapters.
