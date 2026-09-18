#!/usr/bin/env python3
"""Validate a normalized scene snapshot without requiring an engine runtime."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SEVERITY_ORDER = {"info": 0, "warning": 1, "error": 2}


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
    configured = snapshot.get("settings", {}).get("thresholds", {})
    defaults = {
        "instancing_min_instances": 10,
        "srp_min_renderers": 20,
        "particle_count": 500,
        "particle_screen_coverage": 0.15,
    }
    return {**defaults, **configured}


def _asset_exists(assets: dict[str, Any], kind: str, value: Any) -> bool:
    if value in (None, ""):
        return False
    return value in set(_as_list(assets.get(kind, [])))


def validate_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic validation report for a normalized scene snapshot."""

    findings: list[dict[str, str]] = []
    objects = snapshot.get("objects", [])
    assets = snapshot.get("assets", {})
    settings = snapshot.get("settings", {})
    thresholds = _thresholds(snapshot)

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
        "shader": "shaders",
        "texture": "textures",
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
                            f"Assign a valid {asset_kind[:-1]} or remove the optional field.",
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
    parser.add_argument(
        "--fail-on",
        choices=("error", "warning", "info"),
        default="error",
        help="Exit non-zero when findings reach this severity",
    )
    args = parser.parse_args(argv)
    report = validate_snapshot(load_snapshot(args.snapshot))
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render_text(report))
    limit = SEVERITY_ORDER[args.fail_on]
    return int(any(SEVERITY_ORDER[f["severity"]] >= limit for f in report["findings"]))


if __name__ == "__main__":
    raise SystemExit(main())
