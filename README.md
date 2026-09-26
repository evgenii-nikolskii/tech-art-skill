# Tech Art Skill

A skill for AI assistants that helps Technical Artists and anyone who needs support with technical art in game development.

This repository will capture and structure years of hands-on experience as a Technical Artist: practical workflows, production knowledge, problem-solving patterns, and guidance for bridging art and engineering.

The goal is to make that experience useful through an AI-assisted workflow that can help with real technical-art questions, investigations, implementation tasks, and decisions across game development projects.

## Repository structure

- `core/` — platform-independent behavior and decision rules.
- `knowledge/` — category-specific technical-art knowledge modules.
- `adapters/` — guidance for integrating the core with a specific AI platform.
- `skills/tech-art-skill/` — Codex-installable package.
- `tools/` — platform-neutral executable validation tools.
- `evals/` — fixtures and expected validation scenarios.
- `tests/` — automated tests for the tools and contracts.
- `examples/` — sample audit reports and user-facing artifacts.

## Current status

The repository is an early working MVP for an AI technical-art assistant. It contains a reusable core contract, Codex adapter, naming-audit workflow, knowledge modules, and an optional engine-neutral snapshot validator for repeatable checks. Snapshot schema v2, asset checks, measured-budget checks, and CI validation support repository QA; they are not required to use the skill.

Current coverage includes:

- explanation-first technical-art assistance that separates technical facts from subjective artistic judgments;
- scoped naming audits with Rapid Prototype and Production branches;
- dependency-integrity checks for null and missing references;
- texture-map fundamentals, including texture maps as data carriers, swizzling, PBR map semantics, color space, roughness, metallic, ambient occlusion, tangent-space normal maps, texture import contracts, and platform-aware GPU compression.
- geometry import fundamentals, including units and axes, static versus skeletal data, normals/tangents, UVs, LODs, collision, and explicit handling of cameras, lights, embedded materials, and other optional scene payloads.
- animation import fundamentals, including skeleton compatibility, reference poses, root motion, clips and takes, timing, retargeting, morph curves, compression, and animation-only asset ownership.
- scene-audit fundamentals, including scoped inventory, dependency integrity, hierarchy and ownership, cameras and lighting, render assets, geometry and visibility, GPU Instancing, SRP Batcher, physics/navigation, particle/VFX overdraw, performance evidence, and prioritized findings;
- materials/shaders, UVs, baking/lightmaps, VFX/particles, LOD/culling/streaming, reflection sources, mesh processing, lighting/exposure, and repeatable asset validation.

The knowledge base and workflows are intentionally incomplete. Additional depth and examples are still needed. Some knowledge sections include engine-specific guidance; these are scoped examples and must only be applied when the project uses that engine and pipeline.

## Skill assessment

The repository is currently a strong knowledge-first MVP:

- **Coverage:** 13 populated technical-art modules now span texture maps, geometry and animation import, scene auditing, materials/shaders, UVs, baking/lightmaps, VFX, LOD/culling/streaming, reflection sources, mesh processing, lighting/exposure, and asset validation.
- **Workflow quality:** the core contract consistently requires scoped analysis, dependency checks, explanation before repair, explicit assumptions, visual validation, and separation of technical facts from artistic judgment.
- **Practical value:** the modules contain production-oriented decision rules, risk warnings, platform considerations, and validation checklists rather than only terminology.
- **Current limitation:** there is no engine integration that automatically gathers project data. The AI uses the project files and evidence available in the user's environment; the optional snapshot validator consumes data supplied by the user or another tool.

The skill is intended for structured technical-art analysis, investigation plans, import reviews, and audit reports across engines. The snapshot schema and validator are optional repository QA utilities, separate from the AI reasoning workflow.

## Executable validation baseline

Run the automated tests:

```bash
python3 -m unittest discover -s tests -v
```

Run a sample clean validation with a zero exit code:

```bash
python3 tools/scene_validator.py evals/fixtures/scene_clean.json --fail-on warning
```

Run the intentionally problematic fixture to inspect actionable findings:

```bash
python3 tools/scene_validator.py evals/fixtures/scene_problematic.json
```

## Codex installation

Ask Codex to install the skill from `evgenii-nikolskii/tech-art-skill` using the path `skills/tech-art-skill`.

## Other AI systems

Use `core/instructions.md` as the platform-independent source and combine it with the relevant adapter from `adapters/`.
