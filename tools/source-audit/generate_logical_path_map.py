#!/usr/bin/env python3
"""Generate a proposed logical monorepo path map without moving files.

This is an overlay/migration-planning artifact. It maps each inventoried source
or retained artifact to a proposed conceptual monorepo destination while keeping
all files in their current paths. It is intentionally conservative: every entry
is PROPOSED_NOT_EXECUTED and requires owner approval before any physical move.
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
INV_PATH = ROOT / "verification/inventory/REBOL_RED_INVENTORY.json"
OUT_JSON = ROOT / "verification/inventory/MONOREPO_PATH_MAP.json"
OUT_MD = ROOT / "verification/reports/MONOREPO_PATH_MAP.md"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def load_inventory() -> dict[str, Any]:
    return json.loads(INV_PATH.read_text())


def generated(method: str) -> dict[str, str]:
    return {
        "date": TODAY,
        "timestamp_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "tool": TOOL,
        "method": method,
        "source_inventory": INV_PATH.relative_to(ROOT).as_posix(),
        "repository_commit": git("rev-parse", "HEAD"),
        "branch": git("branch", "--show-current"),
    }


def logical_destination(entry: dict[str, Any]) -> tuple[str, str, str]:
    path = entry["path"]
    cls = entry["classification"]

    if cls == "REBOL-BOOTSTRAP":
        return f"bootstrap/rebol/{path}", "HIGH", "Rebol bootstrap material belongs under bootstrap/rebol overlay."
    if cls in {"REBOL-SOURCE", "REBOL-TOOLING"}:
        return f"rebol/tools/{path}", "MEDIUM", "Rebol-family source/tooling separated from Red compiler/runtime."
    if cls == "RED-COMPILER":
        if path.startswith("system/formats/"):
            return f"red/linker/{path}", "MEDIUM", "Format/linker-related compiler component."
        return f"red/compiler/{path}", "HIGH", "Red compiler/toolchain source."
    if cls == "RED-RUNTIME":
        return f"red/runtime/{path}", "HIGH", "Red runtime/environment source."
    if cls == "RED-SYSTEM-SOURCE":
        return f"red/red-system/{path}", "HIGH", "Red/System source separated from Red high-level source."
    if cls == "RED-SOURCE":
        if path.startswith("bridges/") or path.startswith("libRed/"):
            return f"red/tools/{path}", "MEDIUM", "Bridge/libRed source is Red tooling/support, not core compiler."
        return f"red/source/{path}", "MEDIUM", "General Red source."
    if cls == "RED-TOOLING":
        return f"red/tools/{path}", "MEDIUM", "Red build/tooling/support artifact."
    if cls == "RED-TEST":
        return f"red/tests/{path}", "HIGH", "Red/Rebol-family test artifact."
    if cls == "RED-FIXTURE":
        return f"fixtures/red/{path}", "MEDIUM", "Red test fixture/support artifact."
    if cls == "RED-COGNITION":
        if path.startswith("dialects/"):
            return f"red-cognition/dialects/{path}", "HIGH", "Red-Cognition dialect artifact."
        return f"red-cognition/implementation/{path}", "MEDIUM", "Red-Cognition implementation/control-plane artifact."
    if cls == "RFC":
        return f"red-cognition/rfc/{path}", "HIGH", "RFC artifact."
    if cls == "SPECIFICATION":
        return f"red-cognition/specs/{path}", "HIGH", "Specification/traceability artifact."
    if cls == "GOVERNANCE":
        return f"red-cognition/governance/{path}", "MEDIUM", "Governance/license artifact retained with provenance."
    if cls == "DOCUMENTATION":
        return f"docs/historical/{path}", "LOW", "Documentation requires owner review to distinguish Red historical docs from Red-Cognition docs."
    if cls == "BUILD-INFRASTRUCTURE":
        return f"bootstrap/manifests/{path}", "LOW", "Build/CI infrastructure may span bootstrap and test execution."
    if cls in {"BINARY", "ARCHIVE", "BOOTSTRAP-ARTIFACT"}:
        return f"fixtures/cross-language/binaries/{path}", "LOW", "Binary/archive retained as fixture/provenance object until build origin is known."
    return f"verification/provenance/unknown/{path}", "LOW", "Uncertain classification; do not physically move without review."


def main() -> None:
    inv = load_inventory()
    entries = []
    collisions: dict[str, list[str]] = {}
    for entry in inv["files"]:
        dest, confidence, reason = logical_destination(entry)
        entries.append({
            "current_path": entry["path"],
            "proposed_logical_path": dest,
            "classification": entry["classification"],
            "sha256_before": entry["sha256"],
            "sha256_after": "NOT_APPLICABLE_NO_MOVE_PERFORMED",
            "transformation": "NONE_PROPOSED_OVERLAY_ONLY",
            "status": "PROPOSED_NOT_EXECUTED",
            "mapping_confidence": confidence,
            "reason": reason,
            "origin": entry.get("origin", "UNKNOWN"),
            "license": entry.get("license", "UNKNOWN"),
            "modification_status": entry.get("modification_status", "UNKNOWN"),
            "owner_decision_required": True,
        })
        collisions.setdefault(dest, []).append(entry["path"])
    collisions = {k: v for k, v in collisions.items() if len(v) > 1}
    by_conf: dict[str, int] = {}
    by_class: dict[str, int] = {}
    for e in entries:
        by_conf[e["mapping_confidence"]] = by_conf.get(e["mapping_confidence"], 0) + 1
        by_class[e["classification"]] = by_class.get(e["classification"], 0) + 1

    data = {
        "schema_version": 1,
        "generated": generated("derive proposed logical monorepo path map from classified inventory; no filesystem moves performed"),
        "status": "PROPOSED_NOT_EXECUTED",
        "policy": [
            "This map is an overlay for review and planning only.",
            "Do not treat proposed_logical_path as current filesystem truth.",
            "Before physical migration, create a new migration entry with sha256_before, move, sha256_after, comparison result, and owner approval.",
        ],
        "summary": {
            "mapped_entries": len(entries),
            "by_mapping_confidence": dict(sorted(by_conf.items())),
            "by_classification": dict(sorted(by_class.items())),
            "proposed_path_collisions": len(collisions),
            "moves_performed": 0,
        },
        "collisions": collisions,
        "entries": entries,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")

    lines = [
        "# Proposed Logical Monorepo Path Map",
        "",
        f"Generated by `{TOOL}` on {TODAY}.",
        "",
        "Status: **PROPOSED_NOT_EXECUTED**",
        "",
        "No files were moved. This report is a planning overlay only.",
        "",
        "## Summary",
        f"- Mapped entries: {len(entries)}",
        f"- Proposed path collisions: {len(collisions)}",
        "- Moves performed: 0",
        "",
        "### Mapping confidence",
        "| Confidence | Count |",
        "|---|---:|",
    ]
    for key, value in sorted(by_conf.items()):
        lines.append(f"| {key} | {value} |")
    lines += ["", "## Conceptual Mapping Rules", ""]
    rules = [
        ("REBOL", "`rebol/tools/` and `bootstrap/rebol/`"),
        ("Red/System", "`red/red-system/`"),
        ("Red compiler/linker", "`red/compiler/` and `red/linker/`"),
        ("Red runtime", "`red/runtime/`"),
        ("Red tests/fixtures", "`red/tests/` and `fixtures/red/`"),
        ("Red-Cognition", "`red-cognition/rfc/`, `red-cognition/specs/`, `red-cognition/governance/`, `red-cognition/implementation/`"),
        ("Binaries/archives", "`fixtures/cross-language/binaries/` pending provenance review"),
    ]
    for name, dest in rules:
        lines.append(f"- {name}: {dest}")
    lines += ["", "## Sample Proposed Entries", ""]
    for e in entries[:200]:
        lines.append(f"- `{e['current_path']}` → `{e['proposed_logical_path']}` ({e['classification']}, confidence {e['mapping_confidence']})")
    if len(entries) > 200:
        lines.append(f"- ... {len(entries) - 200} additional entries in `{OUT_JSON.relative_to(ROOT).as_posix()}`")
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(json.dumps({"result": "ok", "summary": data["summary"], "outputs": [OUT_JSON.relative_to(ROOT).as_posix(), OUT_MD.relative_to(ROOT).as_posix()]}, indent=2))


if __name__ == "__main__":
    main()
