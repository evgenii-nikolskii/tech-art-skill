# Tech Art Skill

A skill for AI assistants that helps Technical Artists and anyone who needs support with technical art in game development.

This repository will capture and structure years of hands-on experience as a Technical Artist: practical workflows, production knowledge, problem-solving patterns, and guidance for bridging art and engineering.

The goal is to make that experience useful through an AI-assisted workflow that can help with real technical-art questions, investigations, implementation tasks, and decisions across game development projects.

## Repository structure

- `core/` — platform-independent behavior and decision rules.
- `adapters/` — guidance for integrating the core with a specific AI platform.
- `skills/tech-art-skill/` — Codex-installable package.

## Current status

The repository is an initial scaffold. Domain-specific workflows and accumulated technical-art knowledge will be added iteratively.

## Codex installation

Ask Codex to install the skill from `evgenii-nikolskii/tech-art-skill` using the path `skills/tech-art-skill`.

## Other AI systems

Use `core/instructions.md` as the platform-independent source and combine it with the relevant adapter from `adapters/`.
