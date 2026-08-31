#!/usr/bin/env python3
"""Generate binary, license, offline, and owner-decision reports.

Inputs are generated inventory/provenance comparison files. Outputs are
conservative reports for monorepo governance. The script does not modify
historical source and does not execute build/test/bootstrap commands.
"""
from __future__ import annotations

import datetime as _dt
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-08-31"
TOOL = Path(__file__).relative_to(ROOT).as_posix()
INV_PATH = ROOT / "verification/inventory/REBOL_RED_INVENTORY.json"
DUP_PATH = ROOT / "verification/inventory/DUPLICATE_ANALYSIS.json"
UPSTREAM_PATH = ROOT / "verification/provenance/RED_UPSTREAM_V0_6_4_COMPARISON.json"

URL_RE = re.compile(r"https?://[^\s\])}>\"']+")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text()) if path.exists() else {}


def header(method: str) -> dict[str, str]:
    return {
        "date": TODAY,
        "timestamp_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "tool": TOOL,
        "method": method,
        "repository_commit": git("rev-parse", "HEAD"),
        "branch": git("branch", "--show-current"),
    }


def write_json(path: str, data: dict[str, Any]) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def write_text(path: str, text: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def magic(path: Path) -> str:
    b = path.read_bytes()[:16]
    if b.startswith(b"PK\x03\x04"):
        return "ZIP/container"
    if b.startswith(b"\x89PNG\r\n\x1a\n"):
        return "PNG image"
    if b.startswith(b"\x00\x00\x01\x00"):
        return "ICO icon"
    if b.startswith(b"\x00\x00\x02\x00"):
        return "ICNS/icon-like"
    if b.startswith(b"\x7fELF"):
        return "ELF binary/library"
    if b.startswith(b"MZ"):
        return "PE/MZ binary"
    if b.startswith(bytes.fromhex("d0cf11e0a1b11ae1")):
        return "OLE compound document"
    if b.startswith(b"dex\n"):
        return "Android DEX"
    return "UNKNOWN binary/container format"


def binary_inventory(inv: dict[str, Any]) -> dict[str, Any]:
    artifacts = []
    for f in inv["files"]:
        if f.get("binary") or f["classification"] in {"BINARY", "ARCHIVE", "BOOTSTRAP-ARTIFACT"}:
            artifacts.append({
                "path": f["path"],
                "size": f["size"],
                "sha256": f["sha256"],
                "classification": f["classification"],
                "license": f.get("license", "UNKNOWN"),
                "origin": f.get("origin", "UNKNOWN"),
                "upstream_project": f.get("upstream_project", "UNKNOWN"),
                "modification_status": f.get("modification_status", "UNKNOWN"),
                "format_hint": magic(ROOT / f["path"]),
                "provenance_risk": "HIGH" if f.get("license") == "UNKNOWN" or f.get("modification_status") == "UNKNOWN" else "MEDIUM",
                "policy": "Retain and hash; do not call this a source/bootstrap artifact unless build provenance is established.",
            })
    return {
        "schema_version": 1,
        "generated": header("derive binary/archive artifact inventory from source inventory and local byte magic"),
        "summary": {
            "binary_or_archive_artifacts": len(artifacts),
            "by_classification": dict(sorted(Counter(a["classification"] for a in artifacts).items())),
            "by_format_hint": dict(sorted(Counter(a["format_hint"] for a in artifacts).items())),
            "unknown_license": sum(1 for a in artifacts if a["license"] == "UNKNOWN"),
        },
        "artifacts": sorted(artifacts, key=lambda x: x["path"]),
    }


def license_summary(inv: dict[str, Any]) -> dict[str, Any]:
    by_license = defaultdict(list)
    for f in inv["files"]:
        by_license[f.get("license") or "UNKNOWN"].append(f["path"])
    groups = {lic: {"count": len(paths), "sample_paths": paths[:50]} for lic, paths in sorted(by_license.items())}
    return {
        "schema_version": 1,
        "generated": header("summarize license fields captured in repository inventory; no legal interpretation performed"),
        "summary": {
            "files": len(inv["files"]),
            "license_groups": {lic: data["count"] for lic, data in groups.items()},
            "unknown_license_files": len(by_license.get("UNKNOWN", [])),
            "policy": "Preserve existing license headers/files; unknown is not inferred.",
        },
        "groups": groups,
    }


def offline_dependencies(inv: dict[str, Any]) -> dict[str, Any]:
    refs = []
    domain_counts = Counter()
    for f in inv["files"]:
        if f.get("binary"):
            continue
        path = ROOT / f["path"]
        try:
            text = path.read_text(errors="replace")
        except Exception:
            continue
        urls = sorted(set(URL_RE.findall(text)))
        for url in urls:
            domain = re.sub(r"^https?://", "", url).split("/", 1)[0].lower()
            domain_counts[domain] += 1
            lower = (f["path"] + " " + url).lower()
            if "static.red-lang.org" in lower or "rebview" in lower or "rebol" in lower:
                kind = "BOOTSTRAP_OR_TOOLCHAIN_NETWORK_DEPENDENCY"
            elif f["path"].startswith(".github/") or f["path"].startswith("docker/"):
                kind = "CI_OR_BUILD_NETWORK_DEPENDENCY"
            elif "github.com" in lower:
                kind = "EXTERNAL_REPOSITORY_REFERENCE"
            else:
                kind = "DOCUMENTATION_OR_EXTERNAL_REFERENCE"
            refs.append({"path": f["path"], "url": url, "domain": domain, "kind": kind})
    return {
        "schema_version": 1,
        "generated": header("scan audited non-binary files for HTTP(S) references and classify offline risk conservatively"),
        "summary": {
            "network_references": len(refs),
            "domains": dict(domain_counts.most_common()),
            "bootstrap_or_toolchain_network_dependencies": sum(1 for r in refs if r["kind"] == "BOOTSTRAP_OR_TOOLCHAIN_NETWORK_DEPENDENCY"),
            "ci_or_build_network_dependencies": sum(1 for r in refs if r["kind"] == "CI_OR_BUILD_NETWORK_DEPENDENCY"),
            "external_repository_references": sum(1 for r in refs if r["kind"] == "EXTERNAL_REPOSITORY_REFERENCE"),
            "offline_status": {
                "SOURCE_AVAILABLE": "PARTIALLY_VERIFIED by local inventory and hashes",
                "BUILD_AVAILABLE": "BLOCKED until bootstrap/toolchain dependencies are locally provisioned and executed",
                "BOOTSTRAP_AVAILABLE": "BLOCKED for fully offline Stage 0 because observed workflows download external Rebol binaries",
                "EXECUTION_AVAILABLE": "PARTIALLY_VERIFIED only for Python audit/report commands",
            },
        },
        "references": refs,
    }


def owner_decisions(inv: dict[str, Any], dup: dict[str, Any], upstream: dict[str, Any]) -> dict[str, Any]:
    decisions = [
        {
            "id": "OWNER-DECISION-001",
            "topic": "Physical source migration",
            "question": "Should historical Red/Rebol source remain in the upstream-like layout with overlay docs, or be physically moved into red/, rebol/, and red-cognition/ subtrees?",
            "blocking": True,
            "reason": "Physical moves require owner-approved path authority and hash-before/hash-after migration records.",
        },
        {
            "id": "OWNER-DECISION-002",
            "topic": "Upstream Red baseline",
            "question": "Is upstream Red v0.6.4 the intended baseline for provenance comparison, or should another Red commit/tag be used?",
            "blocking": True,
            "reason": "version.r contains 0.6.4 and v0.6.4 was compared, but diverged/local-only files require baseline confirmation.",
        },
        {
            "id": "OWNER-DECISION-003",
            "topic": "Bootstrap strategy",
            "question": "Should the repo vendor source-buildable bootstrap materials or continue to reference external Rebol bootstrap binaries?",
            "blocking": True,
            "reason": "Offline Stage 0 bootstrap remains blocked under current evidence.",
        },
        {
            "id": "OWNER-DECISION-004",
            "topic": "Duplicate groups",
            "question": "Which same-filename groups are intentional platform variants, historical variants, or conflicts requiring resolution?",
            "blocking": False,
            "reason": f"Duplicate analysis reports {dup.get('summary', {}).get('owner_review_required_groups', 'UNKNOWN')} same-filename groups requiring review.",
        },
        {
            "id": "OWNER-DECISION-005",
            "topic": "RFC-0075 critical gaps",
            "question": "Should unresolved RFC-0075 critical traceability gaps block further migration phases?",
            "blocking": False,
            "reason": "Existing validator reports unresolved critical gaps and exits non-zero.",
        },
    ]
    if upstream:
        counts = upstream.get("summary", {}).get("local_status_counts", {})
        decisions.append({
            "id": "OWNER-DECISION-006",
            "topic": "Diverged upstream files",
            "question": "How should files diverged from upstream Red v0.6.4 be classified after maintainer review?",
            "blocking": True,
            "reason": f"Comparison currently reports {counts.get('LOCALLY_MODIFIED_OR_DIVERGED_AT_SAME_PATH', 'UNKNOWN')} same-path diverged files and {counts.get('LOCAL_ONLY_OR_NON_RED_UPSTREAM', 'UNKNOWN')} local-only/non-upstream files.",
        })
    return {
        "schema_version": 1,
        "generated": header("derive owner decision register from audit, duplicate, bootstrap, CI, and upstream comparison evidence"),
        "summary": {"decisions": len(decisions), "blocking_decisions": sum(1 for d in decisions if d["blocking"])},
        "decisions": decisions,
    }


def write_binary_md(data: dict[str, Any]) -> None:
    lines = ["# Binary and Archive Inventory", "", f"Generated by `{TOOL}` on {TODAY}.", "", "## Summary"]
    for k, v in data["summary"].items():
        lines.append(f"- {k}: `{v}`")
    lines += ["", "## Artifacts"]
    for a in data["artifacts"]:
        lines.append(f"- `{a['path']}` — {a['format_hint']} — {a['classification']} — SHA-256 `{a['sha256']}` — provenance risk {a['provenance_risk']}")
    write_text("verification/reports/BINARY_INVENTORY.md", "\n".join(lines) + "\n")


def write_license_md(data: dict[str, Any]) -> None:
    lines = ["# License Summary", "", f"Generated by `{TOOL}` on {TODAY}.", "", "No legal interpretation or relicensing was performed.", "", "## License Groups", "| License field | Count |", "|---|---:|"]
    for lic, count in data["summary"]["license_groups"].items():
        lines.append(f"| {lic} | {count} |")
    write_text("verification/reports/LICENSE_SUMMARY.md", "\n".join(lines) + "\n")


def write_offline_md(data: dict[str, Any]) -> None:
    s = data["summary"]
    lines = [
        "# Offline Dependency and Status Report", "", f"Generated by `{TOOL}` on {TODAY}.", "",
        "## Status Separation",
    ]
    for k, v in s["offline_status"].items():
        lines.append(f"- {k}: {v}")
    lines += [
        "", "## Network Reference Summary",
        f"- Network references detected: {s['network_references']}",
        f"- Bootstrap/toolchain network dependency references: {s['bootstrap_or_toolchain_network_dependencies']}",
        f"- CI/build network dependency references: {s['ci_or_build_network_dependencies']}",
        f"- External repository references: {s['external_repository_references']}",
        "", "## High-Relevance References",
    ]
    for r in data["references"]:
        if r["kind"] != "DOCUMENTATION_OR_EXTERNAL_REFERENCE":
            lines.append(f"- `{r['path']}` — {r['kind']} — {r['url']}")
    write_text("verification/reports/OFFLINE_STATUS.md", "\n".join(lines) + "\n")


def write_owner_md(data: dict[str, Any]) -> None:
    lines = ["# Owner Decisions Required", "", f"Generated by `{TOOL}` on {TODAY}.", ""]
    for d in data["decisions"]:
        lines += [f"## {d['id']}: {d['topic']}", "", f"- Blocking: `{d['blocking']}`", f"- Question: {d['question']}", f"- Reason: {d['reason']}", ""]
    write_text("verification/reports/OWNER_DECISIONS.md", "\n".join(lines))


def main() -> None:
    inv = load_json(INV_PATH)
    dup = load_json(DUP_PATH)
    upstream = load_json(UPSTREAM_PATH)
    binary = binary_inventory(inv)
    licenses = license_summary(inv)
    offline = offline_dependencies(inv)
    decisions = owner_decisions(inv, dup, upstream)
    write_json("verification/inventory/BINARY_INVENTORY.json", binary)
    write_json("verification/provenance/LICENSE_SUMMARY.json", licenses)
    write_json("verification/reproducibility/OFFLINE_DEPENDENCIES.json", offline)
    write_json("verification/inventory/OWNER_DECISIONS.json", decisions)
    write_binary_md(binary)
    write_license_md(licenses)
    write_offline_md(offline)
    write_owner_md(decisions)
    print(json.dumps({
        "result": "ok",
        "binary_summary": binary["summary"],
        "license_summary": licenses["summary"],
        "offline_summary": offline["summary"],
        "owner_decisions": decisions["summary"],
    }, indent=2))


if __name__ == "__main__":
    main()
