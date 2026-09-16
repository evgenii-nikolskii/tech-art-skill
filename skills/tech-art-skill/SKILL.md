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
3. Use the narrowest applicable tools and resources.
4. State assumptions when the workflow is not fully specified.
5. Validate the result against the workflow's quality criteria before responding.

## Current limitation

The repository currently contains the architecture scaffold only. Domain-specific instructions must be added before this package can reliably execute a particular technical-art workflow.
