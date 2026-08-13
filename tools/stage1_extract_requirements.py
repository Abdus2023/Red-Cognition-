#!/usr/bin/env python3
"""Stage 1 — Normative requirement extraction from authoritative sources.

Scans RFC files for normative statements (MUST, SHALL, SHOULD, MAY) and
extracts them with stable IDs, preserving normative strength and source location.

Output: docs/implementation/requirements-inventory.json

Usage:
  python3 tools/stage1_extract_requirements.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

NORMATIVE_RE = re.compile(
    r'\b(MUST NOT|SHALL NOT|SHOULD NOT|MUST|SHALL|SHOULD|MAY)\b', re.IGNORECASE)

STRENGTH_MAP = {
    "MUST": "mandatory", "MUST NOT": "mandatory-prohibition",
    "SHALL": "mandatory", "SHALL NOT": "mandatory-prohibition",
    "SHOULD": "recommended", "SHOULD NOT": "recommended-prohibition",
    "MAY": "optional",
}


def extract_requirements(rfc_dir: Path) -> list:
    """Extract normative requirements from RFC files with stable IDs."""
    requirements = []
    for f in sorted(rfc_dir.glob("RFC-*.md")):
        text = f.read_text(errors="replace")
        rid_match = re.search(r"RFC-(\d{4})", f.name)
        if not rid_match:
            continue
        rfc_id = f"RFC-{rid_match.group(1)}"
        seq = 0
        for line_no, line in enumerate(text.splitlines(), 1):
            for m in NORMATIVE_RE.finditer(line):
                keyword = m.group(1).upper()
                seq += 1
                req_id = f"REQ-{rfc_id}-{seq:03d}"
                # extract surrounding sentence context (trimmed)
                sentence = line.strip()
                if len(sentence) > 300:
                    start = max(0, m.start() - 100)
                    end = min(len(sentence), m.end() + 200)
                    sentence = ("..." if start > 0 else "") + \
                               sentence[start:end] + ("..." if end < len(sentence) else "")
                requirements.append({
                    "id": req_id,
                    "rfc_id": rfc_id,
                    "source_file": f.name,
                    "line": line_no,
                    "keyword": keyword,
                    "strength": STRENGTH_MAP.get(keyword, "unknown"),
                    "text": sentence,
                })
    return requirements


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    rfc_dir = root / "rfcs"
    if not rfc_dir.is_dir():
        print(f"RFC directory not found: {rfc_dir}", file=sys.stderr)
        return 1

    reqs = extract_requirements(rfc_dir)

    # group by strength for summary
    by_strength = {}
    for r in reqs:
        by_strength.setdefault(r["strength"], []).append(r["id"])

    inventory = {
        "total": len(reqs),
        "by_strength": {k: len(v) for k, v in sorted(by_strength.items())},
        "by_rfc": {},
        "requirements": reqs,
    }
    for r in reqs:
        inventory["by_rfc"].setdefault(r["rfc_id"], 0)
        inventory["by_rfc"][r["rfc_id"]] += 1

    out = root / "docs" / "implementation" / "requirements-inventory.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(json.dumps({
        "total_requirements": inventory["total"],
        "by_strength": inventory["by_strength"],
        "rfcs_with_requirements": len(inventory["by_rfc"]),
        "output": str(out.relative_to(root)),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
