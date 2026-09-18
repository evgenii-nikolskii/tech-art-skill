---
name: tech-art-skill
description: Apply the Tech Art Skill universal workflow to technical-art tasks when the repository contains a configured domain workflow.
metadata:
  short-description: Universal technical-art workflow
---

# Tech Art Skill

This is the Codex adapter for the universal Tech Art Skill core.

## Scope

Use this skill for technical-art workflows defined in the repository's universal core. Preserve the user's requested scope and do not invent a concrete workflow when the relevant domain guidance has not yet been added.

Prioritize explanation over repair. Technical-art tasks often contain an artistic intention that cannot be inferred from technical evidence alone. Do not decide what is beautiful or visually desirable on the user's behalf. Explain what is happening, what influences it, what to inspect, and which controls can change it before proposing or making changes. Distinguish technical facts from aesthetic judgments and state when the intended look is unknown.

## Workflow

1. Read `core/instructions.md` from the repository when the task requires the shared contract.
2. Identify the concrete technical-art workflow and its required evidence.
3. Identify and read the relevant module from the repository's `knowledge/` directory. For texture-map tasks, read `knowledge/texture-maps.md`; for model and geometry import tasks, read `knowledge/geometry-import.md`; for animation import tasks, read `knowledge/animation-import.md`; for reflection-source tasks, read `knowledge/reflection-sources.md`.
4. If the relevant module is empty or does not cover the task, report the coverage gap and rely on the general contract without fabricating repository-specific knowledge.
5. Explain the situation before proposing a fix: identify the evidence, influencing factors, visual checks, available controls, and trade-offs.
6. Use the narrowest applicable tools and resources.
7. State assumptions when the workflow is not fully specified.
8. Validate the result against the workflow's quality criteria before responding.

## Knowledge modules

Knowledge modules are stored in the repository's `knowledge/` directory and are selected by technical-art problem category. The repository currently includes populated `texture-maps.md`, `geometry-import.md`, and `animation-import.md` modules covering texture data/import/compression, model import contracts, and animation/skeleton import contracts. The `reflection-sources.md` module is reserved for reflection-source guidance and is currently empty.
