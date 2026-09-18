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

The snapshot format is intentionally small. The required top-level fields are `metadata`, `settings`, `assets`, and `objects`. Object records use fields such as `type`, `path`, `mesh`, `material`, `shader`, `gpu_instancing_supported`, `gpu_instancing_enabled`, `srp_batcher_compatible`, `particle_count`, `screen_coverage`, and `transparent`.
