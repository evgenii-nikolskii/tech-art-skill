#!/usr/bin/env python3
"""Validate a normalized scene snapshot without requiring an engine runtime."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:  # surfaced as a finding when validating v2 snapshots
    Draft202012Validator = None


SEVERITY_ORDER = {"info": 0, "warning": 1, "error": 2}
GENERIC_NAMES = {
    "new", "newasset", "new asset", "untitled", "unnamed", "unknown", "default",
    "placeholder", "dummy", "sample", "example", "test", "testing", "temp", "tmp",
    "work", "wip", "todo", "asset", "file", "data", "object", "objects", "item",
    "model", "mesh", "geometry", "material", "materials", "texture", "textures", "image",
    "map", "shader", "surface", "node", "group", "collection", "scene", "level", "prefab",
    "cube", "plane", "sphere", "cylinder", "cone", "camera", "light", "empty", "null",
    "root", "origin", "polySurface1", "lambert1", "blinn1", "phong1", "box001", "sphere001",
}
GENERIC_DUPLICATE = re.compile(r"^(?:asset|object|mesh|model|material|texture|copy|duplicate|backup|final|new|test|cube|plane|sphere|camera|light)[._ -]?\d+$", re.I)


def _finding(
    code: str,
    severity: str,
    location: str,
    message: str,
    evidence: str,
    recommendation: str,
) -> dict[str, str]:
    return {
        "code": code,
        "severity": severity,
        "location": location,
        "message": message,
        "evidence": evidence,
        "recommendation": recommendation,
    }


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _thresholds(snapshot: dict[str, Any]) -> dict[str, float]:
    settings = snapshot.get("settings", {})
    configured = settings.get("thresholds", {}) if isinstance(settings, dict) else {}
    if not isinstance(configured, dict):
        configured = {}
    defaults = {
        "instancing_min_instances": 10,
        "srp_min_renderers": 20,
        "particle_count": 500,
        "particle_screen_coverage": 0.15,
    }
    result = {**defaults, **configured}
    for key, value in result.items():
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
            raise ValueError(f"settings.thresholds.{key} must be a non-negative number")
    return result


def _schema_errors(snapshot: dict[str, Any]) -> list[dict[str, str]]:
    if Draft202012Validator is None:
        return [_finding("SCHEMA_VALIDATOR_UNAVAILABLE", "error", "schema_version",
                         "JSON Schema validation requires the validation dependency.",
                         "python package jsonschema is not installed",
                         "Install dependencies with: python3 -m pip install -r requirements-validation.txt")]
    schema_path = Path(__file__).with_name("scene-snapshot.schema.json")
    with schema_path.open(encoding="utf-8") as handle:
        schema = json.load(handle)
    validator = Draft202012Validator(schema)
    findings = []
    for error in sorted(validator.iter_errors(snapshot), key=lambda item: list(map(str, item.absolute_path))):
        location = ".".join(str(part) for part in error.absolute_path) or "$"
        findings.append(_finding("INVALID_SCHEMA", "error", location, error.message,
                                 f"validator_path={location}",
                                 "Correct the snapshot to match tools/scene-snapshot.schema.json."))
    return findings


def _validate_structure(snapshot: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    version = snapshot.get("schema_version", 1)
    if version not in (1, 2):
        findings.append(_finding("UNSUPPORTED_SCHEMA_VERSION", "error", "schema_version",
                                 "Snapshot schema version is not supported.", str(version),
                                 "Export schema_version 1 or 2."))
    elif version == 2:
        findings.extend(_schema_errors(snapshot))
    for field in ("metadata", "settings", "assets", "objects"):
        if field not in snapshot:
            findings.append(_finding("INVALID_SNAPSHOT", "error", field,
                                     f"Required top-level field {field!r} is missing.", "field absent",
                                     "Export all required snapshot fields."))
    for field in ("metadata", "settings", "assets"):
        if field in snapshot and not isinstance(snapshot[field], dict):
            findings.append(_finding("INVALID_SNAPSHOT", "error", field,
                                     f"Snapshot field {field!r} must be an object.",
                                     f"received {type(snapshot[field]).__name__}",
                                     "Export this field as a JSON object."))
    if "objects" in snapshot and not isinstance(snapshot["objects"], list):
        findings.append(_finding("INVALID_SNAPSHOT", "error", "objects",
                                 "Snapshot field 'objects' must be an array.",
                                 f"received {type(snapshot['objects']).__name__}",
                                 "Export scene objects as an array."))
    if isinstance(snapshot.get("settings"), dict):
        for group in ("thresholds", "budgets"):
            values = snapshot["settings"].get(group, {})
            if not isinstance(values, dict):
                findings.append(_finding("INVALID_SNAPSHOT", "error", f"settings.{group}",
                                         f"{group} must be an object.", f"received {type(values).__name__}",
                                         "Export this settings group as an object."))
            else:
                for key, value in values.items():
                    if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
                        findings.append(_finding("INVALID_SNAPSHOT", "error", f"settings.{group}.{key}",
                                                 "Thresholds and budgets must be non-negative numbers.", repr(value),
                                                 "Correct the setting or remove it to use the default."))
        mode = snapshot["settings"].get("naming_mode", "off")
        if mode not in {"off", "prototype", "production"}:
            findings.append(_finding("INVALID_NAMING_MODE", "error", "settings.naming_mode",
                                     "Naming mode must be off, prototype, or production.", str(mode),
                                     "Set a supported naming mode."))
    if "assets" in snapshot and isinstance(snapshot["assets"], dict):
        for kind, values in snapshot["assets"].items():
            if not isinstance(values, list):
                findings.append(_finding("INVALID_SNAPSHOT", "error", f"assets.{kind}",
                                         "Asset registry entries must be arrays.",
                                         f"received {type(values).__name__}",
                                         "Export each asset registry as an array."))
    return findings


def _asset_exists(assets: dict[str, Any], kind: str, value: Any) -> bool:
    if value in (None, ""):
        return False
    known = set()
    for asset in _as_list(assets.get(kind, [])):
        if isinstance(asset, dict):
            known.update(str(asset[key]) for key in ("id", "path", "name") if asset.get(key))
        elif isinstance(asset, (str, int, float)):
            known.add(str(asset))
    return str(value) in known


def _matches_naming_convention(name: str, settings: dict[str, Any]) -> bool | None:
    custom = settings.get("naming_regex")
    convention = settings.get("naming_convention")
    patterns = {
        "lowercase-kebab-case": r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
        "lowercase_snake_case": r"^[a-z0-9]+(?:_[a-z0-9]+)*$",
        "PascalCase": r"^[A-Z][A-Za-z0-9]*$",
    }
    pattern = custom or patterns.get(convention)
    if not pattern:
        return None
    try:
        return re.fullmatch(pattern, name) is not None
    except re.error:
        return False


def validate_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic validation report for a normalized scene snapshot."""

    findings: list[dict[str, str]] = _validate_structure(snapshot)
    objects = snapshot.get("objects", [])
    assets = snapshot.get("assets", {})
    settings = snapshot.get("settings", {})
    try:
        thresholds = _thresholds(snapshot)
    except ValueError:
        thresholds = _thresholds({})
    if not isinstance(assets, dict):
        assets = {}
    if not isinstance(settings, dict):
        settings = {}
    naming_mode = settings.get("naming_mode", "off")
    if naming_mode == "production" and not settings.get("naming_convention") and not settings.get("naming_regex"):
        findings.append(_finding("NAMING_SYSTEM_UNKNOWN", "warning", "settings.naming_mode",
                                 "Production naming audit has no declared local convention.",
                                 "naming_convention and naming_regex are absent",
                                 "Declare a project convention or set naming_mode to prototype when appropriate."))

    if not isinstance(objects, list):
        findings.append(
            _finding(
                "INVALID_SNAPSHOT",
                "error",
                "objects",
                "Scene snapshot objects must be an array.",
                f"received {type(objects).__name__}",
                "Export objects as a JSON array.",
            )
        )
        objects = []

    # Dependency integrity is checked before interpreting performance data.
    reference_fields = {
        "mesh": "meshes",
        "material": "materials",
        "materials": "materials",
        "shader": "shaders",
        "shaders": "shaders",
        "texture": "textures",
        "textures": "textures",
        "animation": "animations",
        "controller": "controllers",
    }
    renderers: list[dict[str, Any]] = []
    particles: list[dict[str, Any]] = []
    for index, obj in enumerate(objects):
        if not isinstance(obj, dict):
            findings.append(
                _finding(
                    "INVALID_OBJECT",
                    "error",
                    f"objects[{index}]",
                    "Scene object must be an object.",
                    f"received {type(obj).__name__}",
                    "Export each scene object as a JSON object.",
                )
            )
            continue
        location = str(obj.get("path") or obj.get("name") or f"objects[{index}]")
        name = str(obj.get("name") or location.rsplit("/", 1)[-1])
        if naming_mode not in {"off", "prototype", "production"}:
            naming_mode = "off"
        if naming_mode != "off" and (name.strip().lower() in {n.lower() for n in GENERIC_NAMES}
                                     or GENERIC_DUPLICATE.match(name.strip())):
            severity = "warning" if naming_mode == "prototype" else "error"
            findings.append(_finding("GENERIC_NAME", severity, location,
                                     "Name appears to be a generic default or unresolved duplicate.",
                                     f"name={name!r}, mode={naming_mode}",
                                     "Rename using the selected zone's established naming convention."))
        if naming_mode != "off":
            matches = _matches_naming_convention(name, settings)
            if matches is False:
                findings.append(_finding("NAMING_CONVENTION_MISMATCH", "error" if naming_mode == "production" else "warning",
                                         location, "Name does not match the declared naming convention.",
                                         f"name={name!r}, convention={settings.get('naming_convention') or settings.get('naming_regex')!r}",
                                         "Rename only after confirming the convention for this asset class."))
        for field, asset_kind in reference_fields.items():
            if field not in obj:
                continue
            value = obj[field]
            references = [value] if value in (None, "") else _as_list(value)
            for reference in references:
                if reference in (None, ""):
                    findings.append(
                        _finding(
                            "MISSING_REFERENCE",
                            "error",
                            location,
                            f"{field} reference is null or empty.",
                            f"{field}={reference!r}",
                                    f"Assign a valid {asset_kind.rstrip('s')} or remove the optional field.",
                        )
                    )
                elif not _asset_exists(assets, asset_kind, reference):
                    findings.append(
                        _finding(
                            "MISSING_REFERENCE",
                            "error",
                            location,
                            f"{field} references an asset that is not in the snapshot registry.",
                            f"{field}={reference!r}",
                            f"Restore the dependency or update the snapshot adapter.",
                        )
                    )

        if obj.get("active", True) and obj.get("type") in {"MeshRenderer", "SkinnedMeshRenderer"}:
            renderers.append(obj)
        if obj.get("active", True) and obj.get("type") == "ParticleSystem":
            particles.append(obj)

        if obj.get("type") in {"Camera", "Light"} and obj.get("imported_from_source"):
            if not settings.get("allow_scene_payloads", False):
                findings.append(
                    _finding(
                        "UNEXPECTED_SCENE_PAYLOAD",
                        "warning",
                        location,
                        f"Imported {obj['type'].lower()} is present in an asset-focused scene.",
                        "allow_scene_payloads=false",
                        "Disable this payload at import or move it to an explicit scene/cinematic asset.",
                    )
                )

    # Material texture slots are dependencies too, even though they are stored on assets.
    for index, material in enumerate(assets.get("materials", [])):
        if not isinstance(material, dict):
            continue
        location = str(material.get("path") or material.get("name") or f"assets.materials[{index}]")
        for texture_id in _as_list(material.get("textures")):
            if texture_id in (None, "") or not _asset_exists(assets, "textures", texture_id):
                findings.append(_finding("MISSING_REFERENCE", "error", location,
                                         "Material references a texture that is null or absent from the snapshot.",
                                         f"texture={texture_id!r}",
                                         "Restore the texture dependency or update the snapshot producer."))

    # Same mesh/material/shader groups are the candidates for GPU Instancing.
    groups: dict[tuple[Any, Any, Any], list[dict[str, Any]]] = defaultdict(list)
    for obj in renderers:
        groups[(obj.get("mesh"), obj.get("material"), obj.get("shader"))].append(obj)
    for key, group in sorted(groups.items(), key=lambda item: str(item[0])):
        if len(group) < thresholds["instancing_min_instances"]:
            continue
        location = str(group[0].get("path") or group[0].get("name") or "renderers")
        supported = all(obj.get("gpu_instancing_supported", False) for obj in group)
        enabled = all(obj.get("gpu_instancing_enabled", False) for obj in group)
        if supported and not enabled:
            findings.append(
                _finding(
                    "GPU_INSTANCING_RECOMMENDED",
                    "warning",
                    location,
                    "Many identical mesh/material renderers are not using GPU Instancing.",
                    f"instances={len(group)}, mesh={key[0]!r}, material={key[1]!r}",
                    "Evaluate GPU Instancing, then verify grouping, culling, LOD, shadows, and frame cost.",
                )
            )
        elif not supported:
            findings.append(
                _finding(
                    "GPU_INSTANCING_BLOCKED",
                    "warning",
                    location,
                    "Many identical renderers cannot currently use GPU Instancing.",
                    f"instances={len(group)}, compatible={sum(obj.get('gpu_instancing_supported', False) for obj in group)}/{len(group)}",
                    "Inspect shader, material, renderer type, and per-instance property compatibility.",
                )
            )

    # Many ordinary renderers should be checked for SRP Batcher compatibility.
    render_pipeline = str(settings.get("render_pipeline", "")).lower()
    srp_pipeline = "srp" in render_pipeline or render_pipeline in {"urp", "hdrp"}
    if settings.get("srp_batcher_enabled") and srp_pipeline:
        if len(renderers) >= thresholds["srp_min_renderers"]:
            incompatible = [obj for obj in renderers if not obj.get("srp_batcher_compatible", False)]
            if incompatible:
                findings.append(
                    _finding(
                        "SRP_BATCHER_INCOMPATIBLE",
                        "warning",
                        "scene.renderers",
                        "Many renderers are not compatible with the enabled SRP Batcher.",
                        f"renderers={len(renderers)}, incompatible={len(incompatible)}",
                        "Inspect shader/material layout, per-renderer state, MaterialPropertyBlock use, and special render paths.",
                    )
                )
            else:
                findings.append(
                    _finding(
                        "SRP_BATCHER_READY",
                        "info",
                        "scene.renderers",
                        "Renderer population is compatible with the enabled SRP Batcher.",
                        f"renderers={len(renderers)}",
                        "Confirm CPU benefit with Frame Debugger and Profiler on the target device.",
                    )
                )

    # Transparent particle/VFX systems are a static overdraw risk indicator.
    risky_particles = [
        obj
        for obj in particles
        if obj.get("transparent", False)
        and (
            obj.get("particle_count", 0) >= thresholds["particle_count"]
            or obj.get("screen_coverage", 0) >= thresholds["particle_screen_coverage"]
            or obj.get("overlap_layers", 0) >= 3
        )
    ]
    if risky_particles:
        total_particles = sum(int(obj.get("particle_count", 0)) for obj in risky_particles)
        max_coverage = max(float(obj.get("screen_coverage", 0)) for obj in risky_particles)
        findings.append(
            _finding(
                "PARTICLE_OVERDRAW_RISK",
                "warning",
                "scene.particles",
                "Active transparent particle systems have a high static overdraw risk.",
                f"systems={len(risky_particles)}, particles={total_particles}, max_screen_coverage={max_coverage:.2f}",
                "Confirm with overdraw visualization and GPU timing; then tune coverage, overlap, lifetime, spawn rate, or shader cost.",
            )
        )

    # Imported asset settings are optional, but when present they are validated as evidence.
    for kind, registry in assets.items():
        for index, asset in enumerate(registry if isinstance(registry, list) else []):
            if not isinstance(asset, dict):
                continue
            asset_name = str(asset.get("path") or asset.get("name") or f"assets.{kind}[{index}]")
            if kind == "textures":
                if asset.get("texture_type") == "normal" and asset.get("srgb") is True:
                    findings.append(_finding("TEXTURE_COLORSPACE_MISMATCH", "error", asset_name,
                                             "Normal maps should be imported as linear data.",
                                             "texture_type=normal, srgb=true",
                                             "Disable sRGB sampling for this normal map and verify its channel convention."))
                dimensions = max(asset.get("width", 0), asset.get("height", 0))
                if asset.get("max_size", 0) and dimensions > asset.get("max_size", 0):
                    findings.append(_finding("TEXTURE_MAX_SIZE_EXCEEDED", "warning", asset_name,
                                             "Texture dimensions exceed the declared max size.",
                                             f"dimensions={dimensions}, max_size={asset.get('max_size')}",
                                             "Review platform import settings and visual quality at target resolution."))
            if kind == "meshes":
                if asset.get("lightmap_uv_required") and not asset.get("has_lightmap_uv", False):
                    findings.append(_finding("LIGHTMAP_UV_MISSING", "warning", asset_name,
                                             "Mesh requires a lightmap UV set but none is reported.",
                                             "lightmap_uv_required=true, has_lightmap_uv=false",
                                             "Generate or author a non-overlapping lightmap UV set, then inspect the bake."))
                if asset.get("triangle_budget") is not None and asset.get("triangles", 0) > asset["triangle_budget"]:
                    findings.append(_finding("MESH_TRIANGLE_BUDGET_EXCEEDED", "warning", asset_name,
                                             "Mesh exceeds its declared triangle budget.",
                                             f"triangles={asset.get('triangles')}, budget={asset.get('triangle_budget')}",
                                             "Check target platform, silhouette contribution, LODs, and measured frame cost."))

    # Measured runtime data is distinct from static risk heuristics.
    metrics = snapshot.get("performance", {})
    budgets = settings.get("budgets", {})
    if isinstance(metrics, dict) and isinstance(budgets, dict):
        if metrics and not snapshot.get("performance_evidence"):
            findings.append(_finding("PERFORMANCE_EVIDENCE_MISSING", "warning", "performance_evidence",
                                     "Performance values have no capture provenance.",
                                     f"metrics={','.join(sorted(metrics))}",
                                     "Record device, build configuration, capture source, and representative scene/camera."))
        for metric, budget in budgets.items():
            measured = metrics.get(metric)
            if measured is None:
                continue
            if not isinstance(measured, (int, float)) or isinstance(measured, bool):
                findings.append(_finding("INVALID_PERFORMANCE_METRIC", "error", f"performance.{metric}",
                                         "Measured performance value must be numeric.", repr(measured),
                                         "Export a numeric measurement in the documented unit."))
            elif isinstance(budget, (int, float)) and measured > budget:
                findings.append(_finding("PERFORMANCE_BUDGET_EXCEEDED", "warning", f"performance.{metric}",
                                         "Measured performance exceeds its configured budget.",
                                         f"measured={measured}, budget={budget}",
                                         "Profile a representative build on the target device and investigate the dominant cost."))

    counts = Counter(finding["severity"] for finding in findings)
    status = "fail" if counts["error"] else "warn" if counts["warning"] else "pass"
    return {
        "schema_version": 1,
        "scene": snapshot.get("metadata", {}),
        "status": status,
        "summary": {
            "objects": len(objects),
            "renderers": len(renderers),
            "particles": len(particles),
            "errors": counts["error"],
            "warnings": counts["warning"],
            "info": counts["info"],
        },
        "findings": findings,
    }


def load_snapshot(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("Scene snapshot root must be a JSON object")
    return payload


def render_text(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        f"Scene validation: {report['status'].upper()}",
        f"Objects: {summary['objects']} | Renderers: {summary['renderers']} | Particles: {summary['particles']}",
        f"Errors: {summary['errors']} | Warnings: {summary['warnings']} | Info: {summary['info']}",
    ]
    for finding in report["findings"]:
        lines.extend(
            [
                "",
                f"[{finding['severity'].upper()}] {finding['code']} @ {finding['location']}",
                f"  {finding['message']}",
                f"  Evidence: {finding['evidence']}",
                f"  Recommendation: {finding['recommendation']}",
            ]
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", help="Path to a normalized scene snapshot JSON")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--schema-only", action="store_true",
                        help="Validate a schema v2 snapshot against the JSON Schema and exit")
    parser.add_argument(
        "--fail-on",
        choices=("error", "warning", "info"),
        default="error",
        help="Exit non-zero when findings reach this severity",
    )
    args = parser.parse_args(argv)
    snapshot = load_snapshot(args.snapshot)
    if args.schema_only:
        if snapshot.get("schema_version") != 2:
            parser.error("--schema-only requires schema_version 2")
        errors = _schema_errors(snapshot)
        for error in errors:
            print(f"{error['code']} @ {error['location']}: {error['message']}")
        if not errors:
            print("JSON Schema validation: PASS (schema_version 2)")
        return int(bool(errors))
    report = validate_snapshot(snapshot)
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render_text(report))
    limit = SEVERITY_ORDER[args.fail_on]
    return int(any(SEVERITY_ORDER[f["severity"]] >= limit for f in report["findings"]))


if __name__ == "__main__":
    raise SystemExit(main())
