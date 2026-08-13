#!/usr/bin/env python3
"""Stage 4 — Auto-planner: generate implementation backlog from requirements.

Reads the Stage-1 requirements inventory + gap analysis and produces a
machine-readable implementation backlog: one task stub per uncovered RFC,
each carrying requirement IDs, authority, dependencies, blocker classification,
confidence, and candidate source paths.

IMPORTANT: generated tasks are SPECIFIED WORK, not fabricated completion.
They are BLOCKED pending toolchain/implementation — never READY or PASS.

Output: docs/implementation/implementation-backlog.json

Usage:
  python3 tools/stage4_auto_planner.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# RFC number range → domain → candidate source module
RFC_DOMAINS = {
    (1, 10): ("Core cognitive types", "cognition/"),
    (11, 18): ("Execution / CVM / CISA / runtime", "runtime/"),
    (19, 26): ("CogOS / distributed / security", "cognition/"),
    (27, 33): ("Compiler / CIR / verification", "system/"),
    (34, 42): ("Ecosystem (package/sandbox/marketplace)", "cognition/"),
    (43, 50): ("Language / toolchain / conformance", "cognition/"),
    (51, 59): ("Distributed cognition / transactions", "cognition/"),
    (60, 64): ("Verified execution / formal semantics", "cognition/"),
    (65, 72): ("Supply chain / proof-carrying", "cognition/"),
    (73, 74): ("Security / monitoring / autonomous defense", "cognition/"),
    (75, 75): ("Federation knowledge exchange", "cognition/"),
}


def _domain_for(rfc_num: int):
    for (lo, hi), (domain, path) in RFC_DOMAINS.items():
        if lo <= rfc_num <= hi:
            return domain, path
    return "UNCLASSIFIED", "cognition/"


def _blocker_for(rfc_num: int, rfc_status: str, conflicts: set) -> str:
    if f"RFC-{rfc_num:04d}" in conflicts or rfc_num == 75:
        return "SPECIFICATION_CONFLICT"
    return "TOOLCHAIN"


def _confidence_for(rfc_status: str) -> str:
    s = rfc_status.lower()
    if "ratif" in s:  # matches "ratified", "ratification"
        return "HIGH"
    if "candidate" in s:
        return "MEDIUM"
    if "draft" in s:
        return "LOW"
    return "UNKNOWN"


def generate_backlog(root: Path) -> dict:
    """Generate implementation task stubs from the requirements inventory."""
    inv_path = root / "docs" / "implementation" / "requirements-inventory.json"
    gap_path = root / "docs" / "implementation" / "gap-analysis.json"
    rfc_dir = root / "rfcs"

    if not inv_path.is_file():
        return {"error": "requirements-inventory.json not found — run stage1 first"}

    inventory = json.loads(inv_path.read_text())
    gaps = json.loads(gap_path.read_text()) if gap_path.is_file() else {}

    # Group requirements by RFC
    reqs_by_rfc = {}
    for r in inventory.get("requirements", []):
        reqs_by_rfc.setdefault(r["rfc_id"], []).append(r)

    # Known covered RFCs (already have tasks)
    covered = set(gaps.get("covered_rfcs", []))

    # RFC metadata (status, parent) from file headers
    rfc_meta = {}
    for f in sorted(rfc_dir.glob("RFC-*.md")):
        text = f.read_text(errors="replace")
        rid = re.search(r"RFC-(\d{4})", f.name)
        if not rid:
            continue
        rfc_id = f"RFC-{rid.group(1)}"
        status_m = re.search(r"\*\*Status:\*\*\s*(.+?)\s*$", text, re.M)
        parent_m = re.search(r"\*\*Parent:\*\*\s*(.+?)\s*$", text, re.M)
        title_m = re.search(r"\*\*RFC-\d{4}\s+—\s+(.+?)\*\*", text)
        rfc_meta[rfc_id] = {
            "status": (status_m.group(1).strip() if status_m else "UNKNOWN"),
            "parent": "",
            "title": (title_m.group(1).strip() if title_m else ""),
            "file": f.name,
        }
        if parent_m:
            pm = re.search(r"RFC-(\d{4})", parent_m.group(1))
            if pm:
                rfc_meta[rfc_id]["parent"] = f"RFC-{pm.group(1)}"

    conflicts = {"RFC-0075"}  # known spec conflict

    # Generate one task per uncovered RFC with requirements
    tasks = []
    for rfc_id in sorted(reqs_by_rfc.keys()):
        if rfc_id in covered:
            continue
        rfc_num = int(rfc_id.split("-")[1])
        reqs = reqs_by_rfc[rfc_id]
        meta = rfc_meta.get(rfc_id, {})
        domain, source_path = _domain_for(rfc_num)
        status = meta.get("status", "UNKNOWN")
        blocker = _blocker_for(rfc_num, status, conflicts)
        confidence = _confidence_for(status)
        parent = meta.get("parent", "")

        # Dependency: parent RFC task (if also uncovered)
        dep_refs = []
        if parent and parent != rfc_id and parent in reqs_by_rfc and parent not in covered:
            dep_refs.append({"ref": f"IMPL-{parent}", "required_state": "PASS"})

        # All tasks also transitively depend on the toolchain
        if blocker == "TOOLCHAIN":
            dep_refs.append({"ref": "RED-LEX-001", "required_state": "PASS"})

        task = {
            "task_id": f"IMPL-{rfc_id}",
            "title": f"{rfc_id}: {meta.get('title', 'Unknown')}",
            "description": f"Implementation of {len(reqs)} requirements from {rfc_id} ({domain}). Auto-generated; not a fabricated completion.",
            "priority": rfc_num,
            "plan_order": rfc_num,
            "scope": f"TBD — implementer must define based on {domain} requirements",
            "source_authority": [{"doc": f"rfcs/{meta.get('file', '')}",
                                  "anchor": f"{rfc_id} ({status})"}],
            "requirement_refs": [r["id"] for r in reqs[:20]],  # first 20 for readability
            "requirement_count": len(reqs),
            "specification_refs": [{"doc": f"rfcs/{meta.get('file', '')}"}],
            "implementation_targets": [],  # TBD by implementer
            "dependency_refs": dep_refs,
            "required_tools": [],  # TBD
            "validation_commands": [],  # TBD
            "acceptance_criteria": [{"id": "AC-001",
                                     "criterion": "TBD — implementer must define acceptance criteria"}],
            "allowed_tools": [],
            "prohibited_scope": ["rfcs/", "docs/specifications/"],
            "expected_outputs": [],
            "provenance": f"auto-generated from requirements inventory ({rfc_id})",
            # Auto-planner metadata (NOT controller-executable fields):
            "rfc_id": rfc_id,
            "rfc_status": status,
            "rfc_domain": domain,
            "candidate_source_path": source_path,
            "blocker_classification": blocker,
            "blocker_reason": ("Specification conflict" if blocker == "SPECIFICATION_CONFLICT"
                               else "Red toolchain (Rebol 2.7.8) unavailable"),
            "confidence": confidence,
            "parent_rfc": parent,
            "auto_generated": True,
            "implementation_status": "ABSENT",
        }
        tasks.append(task)

    # Summary
    by_blocker = {}
    by_confidence = {}
    by_domain = {}
    for t in tasks:
        by_blocker[t["blocker_classification"]] = by_blocker.get(t["blocker_classification"], 0) + 1
        by_confidence[t["confidence"]] = by_confidence.get(t["confidence"], 0) + 1
        by_domain[t["rfc_domain"]] = by_domain.get(t["rfc_domain"], 0) + 1

    total_reqs = sum(t["requirement_count"] for t in tasks)

    return {
        "backlog_version": "1.0",
        "description": "Auto-generated implementation backlog from the requirements inventory. "
                       "Tasks are SPECIFIED WORK, not fabricated completion. All are BLOCKED.",
        "total_tasks": len(tasks),
        "total_requirements_covered": total_reqs,
        "by_blocker": dict(sorted(by_blocker.items())),
        "by_confidence": dict(sorted(by_confidence.items())),
        "by_domain": dict(sorted(by_domain.items(), key=lambda x: -x[1])),
        "tasks": tasks,
    }


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    backlog = generate_backlog(root)
    out = root / "docs" / "implementation" / "implementation-backlog.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(backlog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "total_tasks": backlog["total_tasks"],
        "total_requirements": backlog["total_requirements_covered"],
        "by_blocker": backlog["by_blocker"],
        "by_confidence": backlog["by_confidence"],
        "output": str(out.relative_to(root)),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
