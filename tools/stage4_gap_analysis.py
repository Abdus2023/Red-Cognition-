#!/usr/bin/env python3
"""Stage 4 — Implementation gap analysis.

Cross-references the Stage-1 requirements inventory against the Stage-4
implementation plan to surface: which RFCs have requirements but no tasks.

Never infers coverage. Only reports explicit and missing linkages.

Output: docs/implementation/gap-analysis.json

Usage:
  python3 tools/stage4_gap_analysis.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def analyze_gaps(root: Path) -> dict:
    """Identify RFCs with requirements but no implementation tasks."""
    inv_path = root / "docs" / "implementation" / "requirements-inventory.json"
    plan_path = root / "docs" / "implementation" / "implementation-plan.json"
    if not inv_path.is_file() or not plan_path.is_file():
        return {"error": "missing inventory or plan — run earlier stages first"}

    inventory = json.loads(inv_path.read_text())
    plan = json.loads(plan_path.read_text())

    # RFCs that have extracted requirements
    rfcs_with_reqs = set(inventory.get("by_rfc", {}).keys())

    # RFCs referenced by tasks (from source_authority + specification_refs)
    rfcs_referenced_by_tasks = set()
    for task in plan.get("tasks", []):
        for ref in task.get("source_authority", []) + task.get("specification_refs", []):
            doc = ref.get("doc", "")
            m = re.search(r"RFC-(\d{4})", doc)
            if m:
                rfcs_referenced_by_tasks.add(f"RFC-{m.group(1)}")

    # Also check spec_conflicts / spec_gaps
    for task in plan.get("tasks", []):
        for conflict in task.get("spec_conflicts", []):
            m = re.search(r"(\d{4})", conflict)
            if m:
                rfcs_referenced_by_tasks.add(f"RFC-{m.group(1)}")

    rfcs_with_tasks = rfcs_with_reqs & rfcs_referenced_by_tasks
    rfcs_without_tasks = rfcs_with_reqs - rfcs_referenced_by_tasks

    # Requirement counts for gap RFCs
    req_counts = inventory.get("by_rfc", {})
    gap_details = []
    for rfc in sorted(rfcs_without_tasks):
        gap_details.append({
            "rfc_id": rfc,
            "requirement_count": req_counts.get(rfc, 0),
        })

    gap_reqs_total = sum(d["requirement_count"] for d in gap_details)

    return {
        "rfcs_with_requirements": len(rfcs_with_reqs),
        "rfcs_with_task_coverage": len(rfcs_with_tasks),
        "rfcs_without_task_coverage": len(rfcs_without_tasks),
        "coverage_pct": round(len(rfcs_with_tasks) / max(len(rfcs_with_reqs), 1) * 100, 2),
        "requirements_in_gap_rfcs": gap_reqs_total,
        "gap_rfcs": gap_details,
        "covered_rfcs": sorted(rfcs_with_tasks),
        "task_rfc_references": sorted(rfcs_referenced_by_tasks),
    }


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    gaps = analyze_gaps(root)
    out = root / "docs" / "implementation" / "gap-analysis.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(gaps, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "rfcs_with_requirements": gaps.get("rfcs_with_requirements", 0),
        "rfcs_with_task_coverage": gaps.get("rfcs_with_task_coverage", 0),
        "rfcs_without_task_coverage": gaps.get("rfcs_without_task_coverage", 0),
        "coverage_pct": gaps.get("coverage_pct", 0),
        "requirements_in_gap_rfcs": gaps.get("requirements_in_gap_rfcs", 0),
        "output": str(out.relative_to(root)),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
