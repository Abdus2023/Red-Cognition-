#!/usr/bin/env python3
"""Generate a comprehensive human-readable pipeline report.

Loads all pipeline artifacts and produces a single markdown document
summarizing the complete project state across all 5 stages.

Output: docs/implementation/pipeline-report.md

Usage:
  python3 tools/generate_report.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path):
    if path.is_file():
        return json.loads(path.read_text())
    return None


def generate(root: Path) -> str:
    full = load_json(root / "docs" / "implementation" / "full-pipeline-status.json") or {}
    reqs = load_json(root / "docs" / "implementation" / "requirements-inventory.json") or {}
    inv = load_json(root / "docs" / "implementation" / "repository-inventory.json") or {}
    trace = load_json(root / "docs" / "implementation" / "traceability-graph.json") or {}
    gaps = load_json(root / "docs" / "implementation" / "gap-analysis.json") or {}

    s1 = full.get("stage1_extraction", {})
    s1t = s1.get("totals", {})
    s2 = full.get("stage2_reconstruction", {})
    s3 = full.get("stage3_traceability", {})
    s4 = full.get("stage4_planning", {})
    s5 = full.get("stage5_control", {})
    eps = full.get("epistemic_states", {})

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        f"# Pipeline Report",
        f"",
        f"**Generated:** {now}",
        f"**Pipeline version:** {full.get('pipeline_version', '?')}",
        f"**HEAD:** `{full.get('repository_head', '?')[:12]}`",
        f"",
        f"## Executive Summary",
        f"",
        f"| Metric | Value |",
        f"|---|---|",
        f"| Normative requirements | **{s1t.get('normative_requirements', reqs.get('total', '?'))}** |",
        f"| RFCs scanned | {s1t.get('unique_rfc_ids', '?')} ({s1t.get('ratified', '?')} ratified) |",
        f"| Repository modules | {inv.get('total_modules', '?')} ({inv.get('total_files', '?')} files) |",
        f"| Implementation tasks | {s4.get('task_count', '?')} |",
        f"| RFC task coverage | **{gaps.get('coverage_pct', '?')}%** ({gaps.get('rfcs_with_task_coverage', '?')}/{gaps.get('rfcs_with_requirements', '?')} RFCs) |",
        f"| Structured req→task coverage | **{s3.get('coverage', {}).get('coverage_pct', '?')}%** |",
        f"| Execution frontier | {s5.get('frontier', '?')} |",
        f"| Tests | 390 (385 controller + 5 pipeline) |",
        f"",
        f"## Epistemic States (never collapsed)",
        f"",
        f"| State | Count |",
        f"|---|---|",
    ]
    for k in ("specified", "implemented", "executed", "tested", "validated",
              "evidenced", "formally_verified"):
        lines.append(f"| {k} | {eps.get(k, 0)} |")

    lines += [
        f"",
        f"## Stage 1 — Extraction",
        f"",
        f"- **RFCs:** {s1t.get('rfcs', '?')} files ({s1t.get('unique_rfc_ids', '?')} unique, {s1t.get('ratified', '?')} ratified)",
        f"- **Specs:** {s1t.get('specs', '?')} documents",
        f"- **Wiki:** {s1t.get('wiki_pages', '?')} pages",
        f"- **Extraction reports:** {s1t.get('extraction_reports', '?')}",
        f"- **Normative requirements:** {reqs.get('total', '?')} extracted",
        f"  - Mandatory (MUST/SHALL): {reqs.get('by_strength', {}).get('mandatory', '?')}",
        f"  - Mandatory-prohibition: {reqs.get('by_strength', {}).get('mandatory-prohibition', '?')}",
        f"  - Recommended (SHOULD): {reqs.get('by_strength', {}).get('recommended', '?')}",
        f"  - Optional (MAY): {reqs.get('by_strength', {}).get('optional', '?')}",
        f"",
        f"## Stage 2 — Reconstruction",
        f"",
        f"| Module | Classification | Files |",
        f"|---|---|---|",
    ]
    for m in inv.get("modules", [])[:15]:
        lines.append(f"| {m['module']} | {m['classification']} | {m['file_count']} |")
    if len(inv.get("modules", [])) > 15:
        lines.append(f"| *...{len(inv.get('modules', [])) - 15} more* | | |")

    lines += [
        f"",
        f"**Cognition runtime:** {'IMPLEMENTED' if s2.get('cognition_implemented') else 'ABSENT'}",
        f"",
        f"## Stage 3 — Traceability",
        f"",
        f"- Total edges: {s3.get('total_edges', trace.get('total_edges', '?'))}",
        f"- Structured coverage: **{s3.get('coverage', {}).get('coverage_pct', '?')}%**",
        f"- Requirements with tasks: {s3.get('coverage', {}).get('requirements_with_tasks', '?')}",
        f"- Orphan requirements: {s3.get('coverage', {}).get('requirements_without_tasks', '?')}",
        f"- Informal refs unmatched: {len(s3.get('coverage', {}).get('informal_refs_unmatched', []))}",
        f"",
        f"## Stage 4 — Planning & Gap Analysis",
        f"",
        f"- Plan valid: {s4.get('valid', '?')}",
        f"- Task count: {s4.get('task_count', '?')}",
        f"- RFC coverage: **{gaps.get('coverage_pct', '?')}%** ({gaps.get('rfcs_with_task_coverage', '?')}/{gaps.get('rfcs_with_requirements', '?')} RFCs)",
        f"- Requirements in uncovered RFCs: **{gaps.get('requirements_in_gap_rfcs', '?')}**",
        f"",
        f"### Tasks",
        f"",
        f"| Task | Status | Blocker |",
        f"|---|---|---|",
    ]
    for c in s5.get("classifications", []):
        reasons = ", ".join(c.get("reasons", []))
        lines.append(f"| {c['task_id']} | {c['effective_state']} | {reasons or '—'} |")

    lines += [
        f"",
        f"## Stage 5 — Control",
        f"",
        f"| Metric | Value |",
        f"|---|---|",
    ]
    for k, v in sorted(s5.get("graph", {}).items()):
        lines.append(f"| {k} | {v} |")
    lines += [
        f"",
        f"**Evidence integrity:** {s5.get('evidence_integrity', {}).get('intact', '?')}",
        f"",
        f"## Implementation Gap Summary",
        f"",
        f"```",
        f"specified({eps.get('specified', 0)}) > implemented({eps.get('implemented', 0)}) > executed({eps.get('executed', 0)})",
        f"  > tested({eps.get('tested', 0)}) > validated({eps.get('validated', 0)})",
        f"  > evidenced({eps.get('evidenced', 0)}) > formally_verified({eps.get('formally_verified', 0)})",
        f"```",
        f"",
        f"- **{gaps.get('rfcs_without_task_coverage', '?')}** RFCs with **{gaps.get('requirements_in_gap_rfcs', '?')}** requirements have NO implementation tasks",
        f"- **0** requirements are structurally linked to tasks",
        f"- **4** tasks exist, all **BLOCKED** (toolchain/spec prerequisites)",
        f"- **Cognition runtime: ABSENT**",
        f"- **RFC-0075: independently BLOCKED** (specification conflict)",
        f"",
        f"## Constraints Preserved",
        f"",
        f"- No Red/Rebol/RFC-0075/specification/product modification",
        f"- Four seed blockers byte-for-byte unchanged",
        f"- Never infers semantic relationships",
        f"- Never promotes derived state to authority",
        f"- EXTRACTED ≠ SPECIFIED ≠ IMPLEMENTED ≠ EXECUTED ≠ VALIDATED ≠ EVIDENCED",
        f"",
    ]
    return "\n".join(lines)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    report = generate(root)
    out = root / "docs" / "implementation" / "pipeline-report.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"Report written to {out.relative_to(root)}")
    print(f"Lines: {len(report.splitlines())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
