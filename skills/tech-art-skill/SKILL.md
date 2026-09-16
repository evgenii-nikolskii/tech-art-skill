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

## Workflow

1. Read `core/instructions.md` from the repository when the task requires the shared contract.
2. Identify the concrete technical-art workflow and its required evidence.
3. Identify and read the relevant module from the repository's `knowledge/` directory. For texture-map tasks, read `knowledge/texture-maps.md`.
4. If the relevant module is empty, report the coverage gap and rely on the general contract without fabricating repository-specific knowledge.
5. Use the narrowest applicable tools and resources.
6. State assumptions when the workflow is not fully specified.
7. Validate the result against the workflow's quality criteria before responding.

## Knowledge modules

Knowledge modules are stored in the repository's `knowledge/` directory and are selected by technical-art problem category. The texture-map module exists as a placeholder and is intentionally empty until its content is written.
