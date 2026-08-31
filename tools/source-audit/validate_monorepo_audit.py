#!/usr/bin/env python3
"""Validate generated Rebol/Red monorepo audit artifacts.

This validator checks internal consistency of generated manifests and recalculates
SHA-256 values from local files. It does not execute Red/Rebol builds or tests
and does not modify historical source artifacts.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-08-31"
TOOL = Path(__file__).relative_to(ROOT).as_posix()
OUT_JSON = ROOT / "verification/reports/MANIFEST_VALIDATION.json"
OUT_MD = ROOT / "verification/reports/MANIFEST_VALIDATION.md"

JSON_MANIFESTS = [
    "verification/inventory/REBOL_RED_INVENTORY.json",
    "verification/inventory/MIGRATION_MANIFEST.json",
    "verification/inventory/DUPLICATE_ANALYSIS.json",
    "verification/inventory/TEST_INVENTORY.json",
    "verification/inventory/BINARY_INVENTORY.json",
    "verification/inventory/OWNER_DECISIONS.json",
    "verification/inventory/CONFLICT_REGISTER.json",
    "verification/inventory/MONOREPO_PATH_MAP.json",
    "verification/provenance/PROVENANCE_MANIFEST.json",
    "verification/provenance/LICENSE_SUMMARY.json",
    "verification/provenance/RED_UPSTREAM_V0_6_4_COMPARISON.json",
    "verification/reproducibility/OFFLINE_DEPENDENCIES.json",
]


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def load(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    errors: list[str] = []
    warnings: list[str] = []
    checks: list[dict[str, Any]] = []

    manifests: dict[str, dict[str, Any]] = {}
    for rel in JSON_MANIFESTS:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing JSON manifest: {rel}")
            continue
        try:
            data = json.loads(path.read_text())
            manifests[rel] = data
        except Exception as exc:  # pragma: no cover - reported in result
            errors.append(f"invalid JSON manifest {rel}: {exc}")
            continue
        if data.get("schema_version") != 1:
            errors.append(f"schema_version != 1: {rel}")
        checks.append({"check": "json_manifest_schema", "path": rel, "status": "PASS" if data.get("schema_version") == 1 else "FAIL"})

    inv = manifests.get("verification/inventory/REBOL_RED_INVENTORY.json", {})
    files = inv.get("files", [])
    if inv:
        if inv.get("summary", {}).get("total_files") != len(files):
            errors.append("inventory summary.total_files does not match files length")
        if inv.get("summary", {}).get("unknown_files") != 0:
            errors.append("inventory reports UNKNOWN classifications")
        for entry in files:
            rel = entry.get("path")
            digest = entry.get("sha256")
            if not rel or not digest:
                errors.append(f"inventory entry missing path or sha256: {entry}")
                continue
            path = ROOT / rel
            if not path.is_file():
                errors.append(f"inventory path missing locally: {rel}")
                continue
            actual = sha256(path)
            if actual != digest:
                errors.append(f"inventory hash mismatch: {rel}")
        checks.append({"check": "inventory_cardinality_and_hashes", "status": "PASS" if not [e for e in errors if "inventory" in e] else "FAIL", "files_checked": len(files)})

    sums = ROOT / "verification/hashes/SHA256SUMS"
    sum_entries = 0
    if not sums.is_file():
        errors.append("missing verification/hashes/SHA256SUMS")
    else:
        for line in sums.read_text().splitlines():
            if not line or line.startswith("#"):
                continue
            m = re.match(r"^([0-9a-f]{64})  (.+)$", line)
            if not m:
                errors.append(f"malformed SHA256SUMS line: {line}")
                continue
            expected, rel = m.groups()
            sum_entries += 1
            path = ROOT / rel
            if not path.is_file():
                errors.append(f"SHA256SUMS path missing: {rel}")
            elif sha256(path) != expected:
                errors.append(f"SHA256SUMS hash mismatch: {rel}")
        if inv and sum_entries != len(files):
            errors.append(f"SHA256SUMS entries {sum_entries} != inventory files {len(files)}")
        checks.append({"check": "sha256sums", "status": "PASS" if not [e for e in errors if "SHA256SUMS" in e] else "FAIL", "entries": sum_entries})

    mig = manifests.get("verification/inventory/MIGRATION_MANIFEST.json", {})
    if mig:
        if mig.get("status") != "NO_MOVES_PERFORMED" or mig.get("entries") != []:
            errors.append("migration manifest is not the expected no-move baseline")
        checks.append({"check": "migration_no_move_baseline", "status": "PASS" if mig.get("status") == "NO_MOVES_PERFORMED" and mig.get("entries") == [] else "FAIL"})

    conflict = manifests.get("verification/inventory/CONFLICT_REGISTER.json", {})
    if conflict:
        count = len(conflict.get("conflicts", []))
        if conflict.get("summary", {}).get("open_conflicts") != count:
            errors.append("conflict register summary does not match conflict list length")
        if conflict.get("summary", {}).get("destructive_actions_performed") != 0:
            errors.append("conflict register reports destructive actions")
        checks.append({"check": "conflict_register", "status": "PASS" if conflict.get("summary", {}).get("open_conflicts") == count and conflict.get("summary", {}).get("destructive_actions_performed") == 0 else "FAIL", "conflicts": count})

    path_map = manifests.get("verification/inventory/MONOREPO_PATH_MAP.json", {})
    if path_map:
        mapped = path_map.get("entries", [])
        if path_map.get("summary", {}).get("mapped_entries") != len(mapped):
            errors.append("monorepo path map summary does not match entry length")
        if path_map.get("summary", {}).get("moves_performed") != 0:
            errors.append("monorepo path map reports performed moves")
        if any(e.get("status") != "PROPOSED_NOT_EXECUTED" for e in mapped):
            errors.append("monorepo path map contains non-proposed entry status")
        checks.append({"check": "monorepo_path_map", "status": "PASS" if not [e for e in errors if "path map" in e] else "FAIL", "mapped_entries": len(mapped)})

    dup = manifests.get("verification/inventory/DUPLICATE_ANALYSIS.json", {})
    if dup:
        if dup.get("summary", {}).get("exact_sha256_groups") != len(dup.get("exact_sha256_groups", [])):
            errors.append("duplicate exact group count mismatch")
        if dup.get("summary", {}).get("same_filename_groups") != len(dup.get("same_filename_groups", [])):
            errors.append("duplicate same-filename group count mismatch")
        checks.append({"check": "duplicate_analysis_counts", "status": "PASS" if not [e for e in errors if "duplicate" in e] else "FAIL"})

    upstream = manifests.get("verification/provenance/RED_UPSTREAM_V0_6_4_COMPARISON.json", {})
    if upstream:
        if upstream.get("repository", {}).get("upstream_commit") != "755eb943ccea9e78c2cab0f20b313a52404355cb":
            errors.append("unexpected upstream Red v0.6.4 peeled commit")
        local_entries = upstream.get("local_entries", [])
        status_sum = sum(upstream.get("summary", {}).get("local_status_counts", {}).values())
        if status_sum != len(local_entries):
            errors.append("upstream comparison local status counts do not sum to local entry length")
        checks.append({"check": "upstream_comparison_counts", "status": "PASS" if not [e for e in errors if "upstream" in e] else "FAIL", "local_entries": len(local_entries)})

    audit_text = (ROOT / "verification/reports/MONOREPO_AUDIT.md").read_text() if (ROOT / "verification/reports/MONOREPO_AUDIT.md").is_file() else ""
    ci_text = (ROOT / "verification/reports/CI_EVIDENCE.md").read_text() if (ROOT / "verification/reports/CI_EVIDENCE.md").is_file() else ""
    forbidden = ["CI PASS", "Red/Rebol tests passed", "bootstrap verified"]
    for phrase in forbidden:
        if phrase in audit_text or phrase in ci_text:
            errors.append(f"forbidden overclaim phrase found: {phrase}")
    checks.append({"check": "epistemic_overclaim_scan", "status": "PASS" if not [e for e in errors if "overclaim" in e] else "FAIL"})

    result = {
        "schema_version": 1,
        "generated": {
            "date": TODAY,
            "timestamp_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
            "tool": TOOL,
            "method": "validate generated monorepo audit manifests and checksum records; no Red/Rebol build or test execution",
            "repository_commit": git("rev-parse", "HEAD"),
            "branch": git("branch", "--show-current"),
        },
        "result": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "checks": checks,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    lines = [
        "# Manifest Validation Report",
        "",
        f"Generated by `{TOOL}` on {TODAY}.",
        "",
        f"Result: **{result['result']}**",
        "",
        "This validates generated audit manifests and local SHA-256 records only. It does not execute Red/Rebol builds or tests.",
        "",
        "## Checks",
        "| Check | Status | Detail |",
        "|---|---|---|",
    ]
    for check in checks:
        detail = ", ".join(f"{k}={v}" for k, v in check.items() if k not in {"check", "status"})
        lines.append(f"| {check['check']} | {check['status']} | {detail} |")
    lines += ["", "## Errors"]
    if errors:
        lines.extend(f"- {e}" for e in errors)
    else:
        lines.append("- None")
    lines += ["", "## Warnings"]
    if warnings:
        lines.extend(f"- {w}" for w in warnings)
    else:
        lines.append("- None")
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(json.dumps({"result": result["result"], "errors": len(errors), "checks": len(checks), "outputs": [OUT_JSON.relative_to(ROOT).as_posix(), OUT_MD.relative_to(ROOT).as_posix()]}, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
