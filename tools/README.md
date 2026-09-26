# Validation Tools

## Scene snapshot validator

`scene_validator.py` consumes a normalized JSON scene snapshot. An engine adapter can export Unity, Unreal, or custom-engine data into this format without putting engine APIs into the core validator.

Run a human-readable report:

```bash
python3 tools/scene_validator.py evals/fixtures/scene_problematic.json
```

Run machine-readable output:

```bash
python3 tools/scene_validator.py evals/fixtures/scene_problematic.json --format json
```

The validator checks missing references, unexpected imported cameras/lights, repeated mesh/material groups that should be evaluated for GPU Instancing, SRP Batcher compatibility, and transparent particle overdraw risk. It reports evidence and a recommended next action; it does not modify assets.

The snapshot contract is `scene-snapshot.schema.json` (version 2); version 1 inputs remain supported. Optional records enable conservative naming checks, texture/mesh import checks, and measured performance budgets. Naming supports the built-in `lowercase-kebab-case`, `lowercase_snake_case`, and `PascalCase` conventions or a project `naming_regex`. Measurements belong in `performance`; provenance belongs in `performance_evidence`. Missing measurements are unknown, not zero.

Install the validator dependency with `python3 -m pip install -r requirements-validation.txt`. Schema version 2 is validated against JSON Schema on every normal run. To check only the format, run `python3 tools/scene_validator.py snapshot.json --schema-only`.

This validator does not connect to or modify a game engine. A snapshot can be prepared manually or produced by an optional external adapter for any engine. The snapshot format is only a convenient structured input for repeatable checks; it is not required for using the AI skill. Keep unknown values absent and attach the relevant evidence when available.
