# Tech Art Skill

A skill for AI assistants that helps Technical Artists and anyone who needs support with technical art in game development.

This repository will capture and structure years of hands-on experience as a Technical Artist: practical workflows, production knowledge, problem-solving patterns, and guidance for bridging art and engineering.

The goal is to make that experience useful through an AI-assisted workflow that can help with real technical-art questions, investigations, implementation tasks, and decisions across game development projects.

## Repository structure

- `core/` — platform-independent behavior and decision rules.
- `knowledge/` — category-specific technical-art knowledge modules.
- `adapters/` — guidance for integrating the core with a specific AI platform.
- `skills/tech-art-skill/` — Codex-installable package.

## Current status

The repository is an early working MVP. The reusable core contract, Codex adapter, naming-audit workflow, naming references, and the first populated technical-art knowledge module are in place.

Current coverage includes:

- explanation-first technical-art assistance that separates technical facts from subjective artistic judgments;
- scoped naming audits with Rapid Prototype and Production branches;
- dependency-integrity checks for null and missing references;
- texture-map fundamentals, including texture maps as data carriers, swizzling, PBR map semantics, color space, roughness, metallic, ambient occlusion, and tangent-space normal maps.

The knowledge base and workflows are intentionally incomplete. Additional focused modules are still needed for areas such as materials, shaders, UVs, mesh processing, baking, VFX, and engine-specific pipelines. There is not yet an automated test or evaluation suite.

## Codex installation

Ask Codex to install the skill from `evgenii-nikolskii/tech-art-skill` using the path `skills/tech-art-skill`.

## Other AI systems

Use `core/instructions.md` as the platform-independent source and combine it with the relevant adapter from `adapters/`.
