#!/usr/bin/env python3
"""Generate a conservative conflict/decision register for monorepo consolidation.

The register is evidence-derived. It flags cases requiring human review, but it
never deletes, merges, rewrites, or chooses between artifacts.
"""
from __future__ import annotations

import datetime as _dt
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-08-31"
TOOL = Path(__file__).relative_to(ROOT).as_posix()
DUP_PATH = ROOT / "verification/inventory/DUPLICATE_ANALYSIS.json"
UPSTREAM_PATH = ROOT / "verification/provenance/RED_UPSTREAM_V0_6_4_COMPARISON.json"
BINARY_PATH = ROOT / "verification/inventory/BINARY_INVENTORY.json"
RFC75_RESULT = ROOT / "docs/traceability/rfc-0075/validation-result.json"
OUT_JSON = ROOT / "verification/inventory/CONFLICT_REGISTER.json"
OUT_MD = ROOT / "verification/reports/CONFLICT_REGISTER.md"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text()) if path.exists() else {}


def generated(method: str) -> dict[str, str]:
    return {
        "date": TODAY,
        "timestamp_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "tool": TOOL,
        "method": method,
        "repository_commit": git("rev-parse", "HEAD"),
        "branch": git("branch", "--show-current"),
    }


def main() -> None:
    dup = load(DUP_PATH)
    upstream = load(UPSTREAM_PATH)
    binary = load(BINARY_PATH)
    rfc75 = load(RFC75_RESULT)

    conflicts: list[dict[str, Any]] = []

    for index, group in enumerate(dup.get("same_filename_groups", []), start=1):
        if group.get("classification") == "IDENTICAL":
            continue
        conflicts.append({
            "id": f"CONFLICT-FILENAME-{index:04d}",
            "type": "SAME_FILENAME_RELATED_VARIANT",
            "relationship": group.get("classification", "UNKNOWN"),
            "artifact_a": group.get("paths", ["UNKNOWN"])[0],
            "artifact_b": group.get("paths", ["UNKNOWN", "UNKNOWN"])[1] if len(group.get("paths", [])) > 1 else "UNKNOWN",
            "artifacts": group.get("paths", []),
            "evidence": f"Same filename `{group.get('filename')}` appears at {len(group.get('paths', []))} paths with {group.get('distinct_sha256_count')} distinct SHA-256 values.",
            "differences": "Distinct SHA-256 values; semantic differences not interpreted by automation.",
            "likely_authority": "UNKNOWN",
            "decision_required": "OWNER DECISION REQUIRED before consolidation or deletion",
            "status": "OPEN",
        })

    # Capture a bounded but representative set of upstream divergence conflicts.
    for index, entry in enumerate((upstream.get("local_entries") or []), start=1):
        status = entry.get("comparison_status")
        if status not in {"LOCALLY_MODIFIED_OR_DIVERGED_AT_SAME_PATH", "UPSTREAM_CONTENT_RELOCATED_OR_RENAMED"}:
            continue
        ctype = "UPSTREAM_SAME_PATH_DIVERGENCE" if status == "LOCALLY_MODIFIED_OR_DIVERGED_AT_SAME_PATH" else "UPSTREAM_CONTENT_RELOCATION"
        conflicts.append({
            "id": f"CONFLICT-UPSTREAM-{index:04d}",
            "type": ctype,
            "relationship": status,
            "artifact_a": entry.get("local_path", "UNKNOWN"),
            "artifact_b": ", ".join(entry.get("upstream_related_paths") or [entry.get("local_path", "UNKNOWN")]),
            "artifacts": [entry.get("local_path", "UNKNOWN")] + (entry.get("upstream_related_paths") or []),
            "evidence": entry.get("evidence", "UNKNOWN"),
            "differences": "SHA-256 comparison against upstream Red v0.6.4; intent not inferred.",
            "likely_authority": "UNKNOWN pending owner-selected upstream baseline and maintainer review",
            "decision_required": "OWNER DECISION REQUIRED before marking as locally modified, historical variant, or conflict-resolved",
            "status": "OPEN",
        })

    for index, artifact in enumerate(binary.get("artifacts", []), start=1):
        if artifact.get("provenance_risk") != "HIGH":
            continue
        conflicts.append({
            "id": f"CONFLICT-BINARY-PROVENANCE-{index:04d}",
            "type": "BINARY_PROVENANCE_GAP",
            "relationship": "UNKNOWN_BUILD_PROVENANCE",
            "artifact_a": artifact.get("path", "UNKNOWN"),
            "artifact_b": "source/build recipe UNKNOWN",
            "artifacts": [artifact.get("path", "UNKNOWN")],
            "evidence": f"Tracked binary/archive `{artifact.get('path')}` has SHA-256 `{artifact.get('sha256')}` and format hint `{artifact.get('format_hint')}`, but license/build provenance remains unknown.",
            "differences": "Binary bytes are present; source/build derivation not established.",
            "likely_authority": "UNKNOWN",
            "decision_required": "OWNER DECISION REQUIRED: retain as fixture/binary, replace with source-built artifact, or document external provenance",
            "status": "OPEN",
        })

    if rfc75 and rfc75.get("result") == "FAIL":
        conflicts.append({
            "id": "CONFLICT-TRACEABILITY-RFC-0075",
            "type": "TRACEABILITY_VALIDATION_FAILURE",
            "relationship": "FAILED_VALIDATION_GATE",
            "artifact_a": "docs/traceability/rfc-0075/traceability.json",
            "artifact_b": "tools/validate_rfc_0075_traceability.py",
            "artifacts": ["docs/traceability/rfc-0075/traceability.json", "tools/validate_rfc_0075_traceability.py"],
            "evidence": f"RFC-0075 validator result `{rfc75.get('result')}` with {rfc75.get('critical_gaps')} critical gaps and errors: {rfc75.get('errors')}",
            "differences": "Requirements remain unmapped/orphaned according to validator output.",
            "likely_authority": "RFC-0075 traceability package and repository owners",
            "decision_required": "OWNER DECISION REQUIRED: remediate gaps or decide whether they block migration",
            "status": "OPEN",
        })

    by_type: dict[str, int] = {}
    for c in conflicts:
        by_type[c["type"]] = by_type.get(c["type"], 0) + 1

    data = {
        "schema_version": 1,
        "generated": generated("derive conflict records from duplicate analysis, upstream comparison, binary inventory, and RFC validator result"),
        "policy": "No artifact is deleted, merged, or selected as authoritative by this register. All open conflicts require owner/maintainer review.",
        "summary": {
            "open_conflicts": len(conflicts),
            "by_type": dict(sorted(by_type.items())),
            "destructive_actions_performed": 0,
        },
        "conflicts": conflicts,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")

    lines = [
        "# Conflict Register",
        "",
        f"Generated by `{TOOL}` on {TODAY}.",
        "",
        "No artifact is deleted, merged, or selected as authoritative by this register.",
        "",
        "## Summary",
        f"- Open conflicts: {len(conflicts)}",
        "- Destructive actions performed: 0",
        "",
        "| Type | Count |",
        "|---|---:|",
    ]
    for key, value in sorted(by_type.items()):
        lines.append(f"| {key} | {value} |")
    lines += ["", "## High-Level Conflict Samples", ""]
    for c in conflicts[:160]:
        lines.append(f"### {c['id']}: {c['type']}")
        lines.append("")
        lines.append(f"- Artifact A: `{c['artifact_a']}`")
        lines.append(f"- Artifact B: `{c['artifact_b']}`")
        lines.append(f"- Relationship: `{c['relationship']}`")
        lines.append(f"- Evidence: {c['evidence']}")
        lines.append(f"- Decision required: {c['decision_required']}")
        lines.append("")
    if len(conflicts) > 160:
        lines.append(f"Additional conflicts: {len(conflicts) - 160}; see `{OUT_JSON.relative_to(ROOT).as_posix()}`.")
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n")

    print(json.dumps({"result": "ok", "summary": data["summary"], "outputs": [OUT_JSON.relative_to(ROOT).as_posix(), OUT_MD.relative_to(ROOT).as_posix()]}, indent=2))


if __name__ == "__main__":
    main()
