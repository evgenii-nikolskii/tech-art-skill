# Tech Art Skill

Universal instruction core for AI assistants, with platform-specific adapters.

## Structure

- `core/` — platform-independent behavior and decision rules.
- `adapters/` — guidance for integrating the core with a specific AI platform.
- `skills/tech-art-skill/` — Codex-installable package.

## Current status

Initial repository scaffold. Domain-specific workflows will be added after the target technical-art use cases are defined.

## Codex installation

Ask Codex to install the skill from `evgenii-nikolskii/tech-art-skill` using the path `skills/tech-art-skill`.

## Other AI systems

Use `core/instructions.md` as the platform-independent source and combine it with the relevant adapter from `adapters/`.
