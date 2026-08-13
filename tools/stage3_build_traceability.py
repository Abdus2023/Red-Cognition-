#!/usr/bin/env python3
"""Stage 3 — Bidirectional traceability graph builder.

Links the Stage-1 requirements inventory to the Stage-4 implementation plan,
surfacing coverage gaps: which requirements have tasks, which don't, and which
task references don't match the structured inventory.

Never infers relationships — only reports explicit and missing edges.

Output: docs/implementation/traceability-graph.json

Usage:
  python3 tools/stage3_build_traceability.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def build_traceability(root: Path) -> dict:
    """Build bidirectional traceability graph from requirements + plan."""
    # Load requirements inventory
    inv_path = root / "docs" / "implementation" / "requirements-inventory.json"
    plan_path = root / "docs" / "implementation" / "implementation-plan.json"
    if not inv_path.is_file():
        return {"error": "requirements-inventory.json not found — run stage1 first"}
    if not plan_path.is_file():
        return {"error": "implementation-plan.json not found"}

    inventory = json.loads(inv_path.read_text())
    plan = json.loads(plan_path.read_text())

    req_ids = {r["id"] for r in inventory.get("requirements", [])}
    req_by_rfc = {}
    for r in inventory.get("requirements", []):
        req_by_rfc.setdefault(r["rfc_id"], []).append(r["id"])

    tasks = plan.get("tasks", [])

    # --- Forward edges: task → requirement/spec/authority ---
    forward = []
    for task in tasks:
        tid = task["task_id"]
        for ref in task.get("requirement_refs", []):
            forward.append({"from": tid, "to": ref, "kind": "task→requirement",
                            "structured": ref in req_ids})
        for spec in task.get("specification_refs", []):
            forward.append({"from": tid, "to": spec.get("doc", ""),
                            "kind": "task→specification"})
        for auth in task.get("source_authority", []):
            forward.append({"from": tid, "to": auth.get("doc", ""),
                            "kind": "task→authority"})

    # --- Reverse edges: requirement → task (explicit only) ---
    reverse = []
    task_req_refs = set()
    for task in tasks:
        for ref in task.get("requirement_refs", []):
            task_req_refs.add(ref)
            reverse.append({"from": ref, "to": task["task_id"],
                            "kind": "requirement→task", "explicit": True})

    # --- Coverage analysis ---
    structured_refs = task_req_refs & req_ids
    informal_refs = task_req_refs - req_ids
    covered_reqs = structured_refs  # requirements with explicit task linkage
    orphan_reqs = req_ids - structured_refs  # requirements with NO task

    # Group orphans by RFC for summary
    orphan_by_rfc = {}
    for rid in orphan_reqs:
        rfc = rid.split("-")[1] if "-" in rid else "UNKNOWN"
        orphan_by_rfc.setdefault(rfc, 0)
        orphan_by_rfc[rfc] += 1

    return {
        "forward_edges": forward,
        "reverse_edges": reverse,
        "total_edges": len(forward) + len(reverse),
        "coverage": {
            "total_structured_requirements": len(req_ids),
            "requirements_with_tasks": len(covered_reqs),
            "requirements_without_tasks": len(orphan_reqs),
            "coverage_pct": round(len(covered_reqs) / max(len(req_ids), 1) * 100, 2),
            "task_requirement_refs": list(sorted(task_req_refs)),
            "structured_refs_matched": len(structured_refs),
            "informal_refs_unmatched": list(sorted(informal_refs)),
        },
        "orphan_requirements_by_rfc": dict(sorted(orphan_by_rfc.items())),
        "tasks": [{"id": t["task_id"], "requirement_refs": t.get("requirement_refs", [])}
                  for t in tasks],
    }


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    graph = build_traceability(root)
    out = root / "docs" / "implementation" / "traceability-graph.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    cov = graph.get("coverage", {})
    print(json.dumps({
        "total_edges": graph.get("total_edges", 0),
        "coverage": cov.get("coverage_pct", 0),
        "requirements_with_tasks": cov.get("requirements_with_tasks", 0),
        "requirements_without_tasks": cov.get("requirements_without_tasks", 0),
        "informal_refs": cov.get("informal_refs_unmatched", []),
        "output": str(out.relative_to(root)),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
