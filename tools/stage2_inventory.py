#!/usr/bin/env python3
"""Stage 2 — Detailed repository component inventory.

Walks the repository tree and classifies every module/package by implementation
status, producing a granular component map that answers: what exists, what's
scaffolded, what's absent.

Output: docs/implementation/repository-inventory.json

Usage:
  python3 tools/stage2_inventory.py
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

# Module → RFC domain mapping (from repository structure)
MODULE_DOMAINS = {
    "runtime": "Red runtime (RFC-0012..0018 CVM/CISA/execution)",
    "system": "Red/System compiler (Red language infrastructure)",
    "compiler": "Red compiler (lexer/parser/codegen)",
    "libRed": "libRed C FFI (RFC-0048 CFFI)",
    "cognition": "Cognition runtime (RFC-0050 architecture — ABSENT)",
    "tests": "Red test suite (Quick-Test harness)",
    "rfcs": "Authoritative RFC specifications (92 files, 75 RFCs)",
    "specs": "Deep technical specifications (52 documents)",
    "knowledge-base": "Extracted corpus knowledge (35 reports, 19 wiki)",
    "docs/implementation": "Stage-5 pipeline + controller infrastructure",
    "tools": "Pipeline tools + validators",
    "environment": "Red environment (console, codecs, schemes)",
    "modules": "Red extension modules (audio, view)",
    "bridges": "Platform bridges (Android, Java)",
    "quick-test": "Quick-Test framework",
    "build": "Build scripts (Rebol SDK)",
}

CLASSIFICATION = {
    "runtime": "SCAFFOLDED",
    "system": "SCAFFOLDED",
    "libRed": "SCAFFOLDED",
    "cognition": "ABSENT",
    "tests": "SCAFFOLDED",
    "rfcs": "AUTHORITATIVE",
    "docs/specifications": "AUTHORITATIVE",
    "knowledge-base": "AUTHORITATIVE",
    "docs/implementation": "IMPLEMENTED",
    "tools": "IMPLEMENTED",
    "environment": "SCAFFOLDED",
    "modules": "SCAFFOLDED",
    "bridges": "SCAFFOLDED",
    "quick-test": "SCAFFOLDED",
    "build": "SCAFFOLDED",
}

SKIP_DIRS = {".git", ".impl_controller", "__pycache__", "node_modules"}


def inventory_repository(root: Path) -> dict:
    """Build a detailed component inventory from the repository tree."""
    modules = defaultdict(lambda: {"files": 0, "by_ext": defaultdict(int),
                                    "paths": [], "sample_files": []})

    for path in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        rel = path.relative_to(root)
        parts = rel.parts
        if not parts:
            continue

        # Map to top-level module
        top = parts[0]
        if top == "docs" and len(parts) > 1:
            if parts[1] == "specifications":
                top = "docs/specifications"
            elif parts[1] == "implementation":
                top = "docs/implementation"
            elif parts[1] == "traceability":
                top = "docs/traceability"

        if path.is_file():
            ext = path.suffix or "(none)"
            modules[top]["files"] += 1
            modules[top]["by_ext"][ext] += 1
            if len(modules[top]["sample_files"]) < 3:
                modules[top]["sample_files"].append(str(rel))

    result = []
    for mod_name in sorted(modules.keys()):
        info = modules[mod_name]
        result.append({
            "module": mod_name,
            "domain": MODULE_DOMAINS.get(mod_name, "UNCLASSIFIED"),
            "classification": CLASSIFICATION.get(mod_name, "UNKNOWN"),
            "file_count": info["files"],
            "extensions": dict(sorted(info["by_ext"].items(), key=lambda x: -x[1])),
            "sample_files": info["sample_files"],
        })

    total_files = sum(m["file_count"] for m in result)
    by_class = defaultdict(int)
    for m in result:
        by_class[m["classification"]] += m["file_count"]

    return {
        "total_modules": len(result),
        "total_files": total_files,
        "by_classification": dict(sorted(by_class.items())),
        "modules": result,
    }


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    inv = inventory_repository(root)
    out = root / "docs" / "implementation" / "repository-inventory.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(inv, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "total_modules": inv["total_modules"],
        "total_files": inv["total_files"],
        "by_classification": inv["by_classification"],
        "output": str(out.relative_to(root)),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
