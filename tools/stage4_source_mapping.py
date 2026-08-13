#!/usr/bin/env python3
"""Stage 4 — Requirement-to-source mapping (coverage matrix).

Maps each RFC's requirements to its candidate source module in the repository,
classifying coverage as SCAFFOLDED (source exists) or ABSENT (source missing).
Never infers relationships — uses structural RFC→domain→module mapping only.

Output: docs/implementation/source-coverage-matrix.json

Usage:
  python3 tools/stage4_source_mapping.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from stage4_auto_planner import RFC_DOMAINS, _domain_for


def build_coverage_matrix(root: Path) -> dict:
    """Map requirements to candidate source modules."""
    inv_path = root / "docs" / "implementation" / "requirements-inventory.json"
    if not inv_path.is_file():
        return {"error": "requirements-inventory.json not found — run stage1 first"}

    inventory = json.loads(inv_path.read_text())
    reqs_by_rfc = {}
    for r in inventory.get("requirements", []):
        reqs_by_rfc.setdefault(r["rfc_id"], []).append(r)

    # Count files in each candidate module
    module_files = {}
    for rfc_id in reqs_by_rfc:
        rfc_num = int(rfc_id.split("-")[1])
        _, source_path = _domain_for(rfc_num)
        if source_path not in module_files:
            p = root / source_path.rstrip("/")
            if p.is_dir():
                count = sum(1 for _ in p.rglob("*") if _.is_file()
                           and ".git" not in str(_))
            else:
                count = 0
            module_files[source_path] = count

    # Build coverage matrix
    matrix = []
    for rfc_id in sorted(reqs_by_rfc.keys()):
        rfc_num = int(rfc_id.split("-")[1])
        domain, source_path = _domain_for(rfc_num)
        req_count = len(reqs_by_rfc[rfc_id])
        file_count = module_files.get(source_path, 0)
        exists = file_count > 0

        matrix.append({
            "rfc_id": rfc_id,
            "domain": domain,
            "candidate_module": source_path,
            "module_exists": exists,
            "module_file_count": file_count,
            "module_status": "SCAFFOLDED" if exists else "ABSENT",
            "requirement_count": req_count,
            "coverage_status": "SOURCE_EXISTS_UNCOMPILED" if exists else "SOURCE_ABSENT",
        })

    # Summary
    with_source = [m for m in matrix if m["module_exists"]]
    without_source = [m for m in matrix if not m["module_exists"]]
    reqs_with = sum(m["requirement_count"] for m in with_source)
    reqs_without = sum(m["requirement_count"] for m in without_source)

    return {
        "total_rfcs": len(matrix),
        "rfcs_with_existing_source": len(with_source),
        "rfcs_without_source": len(without_source),
        "requirements_with_existing_source": reqs_with,
        "requirements_without_source": reqs_without,
        "matrix": matrix,
    }


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    matrix = build_coverage_matrix(root)
    out = root / "docs" / "implementation" / "source-coverage-matrix.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(matrix, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "total_rfcs": matrix["total_rfcs"],
        "rfcs_with_source": matrix["rfcs_with_existing_source"],
        "rfcs_without_source": matrix["rfcs_without_source"],
        "reqs_with_source": matrix["requirements_with_existing_source"],
        "reqs_without_source": matrix["requirements_without_source"],
        "output": str(out.relative_to(root)),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
