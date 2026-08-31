#!/usr/bin/env python3
"""Compare local checkout against an upstream Red tag without modifying source.

Default upstream reference: `v0.6.4^{}` from https://github.com/red/red.git.
The tag must be present in the local Git object database before this script runs;
fetching is intentionally an explicit operator action, not a hidden side effect.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-08-31"
TOOL = Path(__file__).relative_to(ROOT).as_posix()
UPSTREAM_REF = "v0.6.4^{}"
UPSTREAM_REPOSITORY = "https://github.com/red/red.git"
OUT_JSON = ROOT / "verification/provenance/RED_UPSTREAM_V0_6_4_COMPARISON.json"
OUT_MD = ROOT / "verification/reports/RED_UPSTREAM_V0_6_4_COMPARISON.md"


def git(*args: str, check: bool = True) -> str:
    p = subprocess.run(["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr.strip()}")
    return p.stdout.strip()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tree_files(ref: str) -> list[str]:
    out = git("ls-tree", "-r", "--name-only", ref)
    return out.splitlines() if out else []


def blob_bytes(ref: str, path: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "-p", f"{ref}:{path}"], cwd=ROOT)


def tracked_head_files() -> list[str]:
    out = git("ls-tree", "-r", "--name-only", "HEAD")
    return out.splitlines() if out else []


def head_bytes(path: str) -> bytes:
    return (ROOT / path).read_bytes()


def main() -> None:
    try:
        upstream_commit = git("rev-parse", UPSTREAM_REF)
    except RuntimeError as exc:
        OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "schema_version": 1,
            "generated": {
                "date": TODAY,
                "timestamp_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
                "tool": TOOL,
                "method": "attempted upstream Red comparison using local Git tag",
            },
            "status": "BLOCKED",
            "blocked_reason": str(exc),
            "required_operator_action": f"Fetch upstream tag explicitly, e.g. git fetch --depth=1 {UPSTREAM_REPOSITORY} tag v0.6.4",
        }
        OUT_JSON.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        raise SystemExit(2)

    upstream_paths = tree_files(UPSTREAM_REF)
    local_paths = tracked_head_files()

    upstream: dict[str, dict[str, Any]] = {}
    upstream_by_hash: dict[str, list[str]] = defaultdict(list)
    for path in upstream_paths:
        b = blob_bytes(UPSTREAM_REF, path)
        h = sha256(b)
        upstream[path] = {"path": path, "sha256": h, "size": len(b)}
        upstream_by_hash[h].append(path)

    local: dict[str, dict[str, Any]] = {}
    local_by_hash: dict[str, list[str]] = defaultdict(list)
    for path in local_paths:
        b = head_bytes(path)
        h = sha256(b)
        local[path] = {"path": path, "sha256": h, "size": len(b)}
        local_by_hash[h].append(path)

    local_entries = []
    for path, lf in sorted(local.items()):
        uf = upstream.get(path)
        if uf:
            if lf["sha256"] == uf["sha256"]:
                status = "UNMODIFIED_AT_SAME_PATH"
                evidence = "path and SHA-256 match upstream Red v0.6.4"
                related = [path]
            else:
                same_hash_upstream_paths = upstream_by_hash.get(lf["sha256"], [])
                if same_hash_upstream_paths:
                    status = "RENAMED_OR_RELOCATED_UPSTREAM_CONTENT_WITH_LOCAL_PATH_CONFLICT"
                    evidence = "local path differs from path(s) with matching upstream content, while same upstream path has different content"
                    related = same_hash_upstream_paths
                else:
                    status = "LOCALLY_MODIFIED_OR_DIVERGED_AT_SAME_PATH"
                    evidence = "same path exists upstream, but SHA-256 differs"
                    related = [path]
        else:
            same_hash_upstream_paths = upstream_by_hash.get(lf["sha256"], [])
            if same_hash_upstream_paths:
                status = "UPSTREAM_CONTENT_RELOCATED_OR_RENAMED"
                evidence = "SHA-256 matches upstream Red v0.6.4 content at different path(s)"
                related = same_hash_upstream_paths
            else:
                status = "LOCAL_ONLY_OR_NON_RED_UPSTREAM"
                evidence = "path and SHA-256 not found in upstream Red v0.6.4"
                related = []
        local_entries.append({
            "local_path": path,
            "local_sha256": lf["sha256"],
            "local_size": lf["size"],
            "comparison_status": status,
            "evidence": evidence,
            "upstream_related_paths": related,
        })

    upstream_missing = []
    for path, uf in sorted(upstream.items()):
        lf = local.get(path)
        if lf and lf["sha256"] == uf["sha256"]:
            continue
        matching_local_paths = local_by_hash.get(uf["sha256"], [])
        if matching_local_paths:
            status = "PRESENT_AT_DIFFERENT_LOCAL_PATH"
            evidence = "upstream SHA-256 exists locally at different path(s)"
        elif lf:
            status = "LOCAL_PATH_DIVERGED"
            evidence = "same path exists locally, but content differs"
        else:
            status = "MISSING_FROM_LOCAL_CHECKOUT"
            evidence = "upstream path/content not present in local HEAD"
        upstream_missing.append({
            "upstream_path": path,
            "upstream_sha256": uf["sha256"],
            "upstream_size": uf["size"],
            "comparison_status": status,
            "evidence": evidence,
            "local_related_paths": matching_local_paths,
        })

    summary = {
        "local_files": len(local_entries),
        "upstream_files": len(upstream_paths),
        "local_status_counts": dict(sorted(Counter(e["comparison_status"] for e in local_entries).items())),
        "upstream_gap_counts": dict(sorted(Counter(e["comparison_status"] for e in upstream_missing).items())),
    }
    data = {
        "schema_version": 1,
        "generated": {
            "date": TODAY,
            "timestamp_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
            "tool": TOOL,
            "method": "compare SHA-256 of local HEAD tracked files against locally fetched upstream Red v0.6.4 tag; no source files modified",
        },
        "repository": {
            "local_repository": "https://github.com/Abdus2023/Red-Cognition-",
            "branch": git("branch", "--show-current"),
            "local_commit": git("rev-parse", "HEAD"),
            "upstream_repository": UPSTREAM_REPOSITORY,
            "upstream_ref": "v0.6.4",
            "upstream_commit": upstream_commit,
            "upstream_tag_object": git("rev-parse", "v0.6.4"),
        },
        "status": "PARTIALLY_VERIFIED",
        "summary": summary,
        "local_entries": local_entries,
        "upstream_missing_or_diverged_entries": upstream_missing,
        "epistemic_limits": [
            "A SHA-256 match against v0.6.4 verifies byte identity to that tag for that file only.",
            "A mismatch does not by itself prove intentional local modification; it may reflect a different upstream version, generated artifact, path relocation, case-only rename, or Red-Cognition addition.",
            "This comparison does not compare full Git history because the local checkout is shallow/grafted.",
        ],
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")

    lines = [
        "# Red Upstream v0.6.4 Comparison",
        "",
        f"Generated by `{TOOL}` on {TODAY}.",
        "",
        "## Method",
        "Compared SHA-256 values of local `HEAD` tracked files against the locally fetched upstream Red tag `v0.6.4`. No source files were modified.",
        "",
        "## Repository Evidence",
        f"- Local commit: `{data['repository']['local_commit']}`",
        f"- Upstream repository: `{UPSTREAM_REPOSITORY}`",
        f"- Upstream tag: `v0.6.4`",
        f"- Upstream peeled commit: `{upstream_commit}`",
        "",
        "## Summary",
        f"- Local tracked files compared: {summary['local_files']}",
        f"- Upstream Red v0.6.4 files compared: {summary['upstream_files']}",
        "",
        "### Local status counts",
        "| Status | Count |",
        "|---|---:|",
    ]
    for k, v in summary["local_status_counts"].items():
        lines.append(f"| {k} | {v} |")
    lines += ["", "### Upstream missing/diverged status counts", "| Status | Count |", "|---|---:|"]
    for k, v in summary["upstream_gap_counts"].items():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## Important Limits",
        "- Matching files are byte-identical to upstream Red v0.6.4 at the compared path or related path.",
        "- Diverged/local-only files require owner or maintainer review before being classified as intentional local modifications.",
        "- No historical source was deleted, moved, or normalized by this comparison.",
        "",
        "## Diverged Same-Path Samples",
    ]
    diverged = [e for e in local_entries if e["comparison_status"] == "LOCALLY_MODIFIED_OR_DIVERGED_AT_SAME_PATH"]
    for e in diverged[:80]:
        lines.append(f"- `{e['local_path']}`")
    if len(diverged) > 80:
        lines.append(f"- ... {len(diverged) - 80} additional entries in `{OUT_JSON.relative_to(ROOT).as_posix()}`")
    lines += ["", "## Relocated/Renamed Upstream-Content Samples"]
    relocated = [e for e in local_entries if e["comparison_status"] == "UPSTREAM_CONTENT_RELOCATED_OR_RENAMED"]
    for e in relocated[:80]:
        lines.append(f"- `{e['local_path']}` ← {', '.join('`'+p+'`' for p in e['upstream_related_paths'])}")
    if len(relocated) > 80:
        lines.append(f"- ... {len(relocated) - 80} additional entries in `{OUT_JSON.relative_to(ROOT).as_posix()}`")
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(json.dumps({"result": "ok", "summary": summary, "outputs": [OUT_JSON.relative_to(ROOT).as_posix(), OUT_MD.relative_to(ROOT).as_posix()]}, indent=2))


if __name__ == "__main__":
    main()
