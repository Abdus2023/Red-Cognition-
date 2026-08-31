#!/usr/bin/env python3
"""Generate conservative Rebol/Red monorepo inventory and audit reports.

This tool is intentionally dependency-free. It inspects the repository checkout,
classifies tracked artifacts by path, extension, and source headers, computes
SHA-256 hashes from local file bytes, and writes machine-readable and
human-readable verification artifacts.

Generated artifacts identify this script and the current Git commit as their
origin. The script does not move, delete, rewrite, or normalize upstream source.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-08-31"
SCRIPT_PATH = Path(__file__).relative_to(ROOT).as_posix()
OUTPUTS = {
    "inventory_json": "verification/inventory/REBOL_RED_INVENTORY.json",
    "inventory_md": "verification/inventory/REBOL_RED_INVENTORY.md",
    "sha256sums": "verification/hashes/SHA256SUMS",
    "audit_md": "verification/reports/MONOREPO_AUDIT.md",
    "architecture_md": "docs/architecture/REBOL_RED_MONOREPO.md",
    "provenance_md": "docs/provenance/PROVENANCE.md",
    "bootstrap_md": "docs/bootstrap/BOOTSTRAP.md",
}
BINARY_EXTS = {
    ".zip", ".xlsx", ".xlsm", ".png", ".ico", ".icns", ".dll", ".so",
    ".dylib", ".lib", ".dex", ".jar", ".class", ".exe", ".bin", ".a",
}
ARCHIVE_EXTS = {".zip", ".tar", ".gz", ".tgz", ".bz2", ".xz", ".7z", ".rar"}
DOC_EXTS = {".md", ".txt", ".html", ".css", ".csv"}
CONFIG_EXTS = {".yml", ".yaml", ".json", ".xml", ".plist", ".sample"}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def tracked_files() -> list[str]:
    """Return audited source/control files, excluding generated reports.

    Generated report outputs are excluded even after they become tracked, so the
    inventory and SHA256SUMS manifests remain stable and non-self-referential.
    Source-audit tools themselves are included.
    """
    generated = set(OUTPUTS.values()) | {
        "verification/inventory/MIGRATION_MANIFEST.json",
        "verification/inventory/DUPLICATE_ANALYSIS.json",
        "verification/inventory/TEST_INVENTORY.json",
        "verification/inventory/BINARY_INVENTORY.json",
        "verification/inventory/OWNER_DECISIONS.json",
        "verification/inventory/CONFLICT_REGISTER.json",
        "verification/inventory/MONOREPO_PATH_MAP.json",
        "verification/reports/MANIFEST_VALIDATION.json",
        "verification/provenance/PROVENANCE_MANIFEST.json",
        "verification/provenance/LICENSE_SUMMARY.json",
        "verification/provenance/RED_UPSTREAM_V0_6_4_COMPARISON.json",
        "verification/reproducibility/OFFLINE_DEPENDENCIES.json",
        "verification/reports/DUPLICATE_ANALYSIS.md",
        "verification/reports/TEST_STATUS.md",
        "verification/reports/LOCAL_EXECUTION_EVIDENCE.md",
        "verification/reports/CI_EVIDENCE.md",
        "verification/reports/RED_UPSTREAM_V0_6_4_COMPARISON.md",
        "verification/reports/BINARY_INVENTORY.md",
        "verification/reports/LICENSE_SUMMARY.md",
        "verification/reports/OFFLINE_STATUS.md",
        "verification/reports/OWNER_DECISIONS.md",
        "verification/reports/CONFLICT_REGISTER.md",
        "verification/reports/MONOREPO_PATH_MAP.md",
        "verification/reports/MANIFEST_VALIDATION.md",
    }
    generated_prefixes = set()

    def include(rel: str) -> bool:
        return rel not in generated and not any(rel.startswith(prefix) for prefix in generated_prefixes)

    files = {rel for rel in git("ls-files").splitlines() if include(rel)}
    try:
        untracked = set(git("ls-files", "--others", "--exclude-standard").splitlines())
    except subprocess.CalledProcessError:
        untracked = set()
    for rel in untracked:
        if include(rel):
            files.add(rel)
    return sorted(files)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def is_binary_bytes(data: bytes, suffix: str) -> bool:
    if suffix.lower() in BINARY_EXTS:
        return True
    if b"\0" in data[:8192]:
        return True
    return False


def text_sample(path: Path, max_bytes: int = 32768) -> str:
    try:
        return path.read_bytes()[:max_bytes].decode("utf-8", "replace")
    except Exception:
        return ""


def header_kind(sample: str) -> str | None:
    stripped = sample.lstrip("\ufeff\n\r\t ")[:512]
    for kind in ("Red/System", "REBOL", "Red"):
        if stripped.startswith(kind + " ["):
            return kind
    return None


def detect_license(sample: str, path: str) -> str:
    lower = sample.lower()
    name = Path(path).name.lower()
    if name == "bsd-3-license.txt" or "bsd-3" in lower or "bsd 3" in lower:
        return "BSD-3-Clause (as stated or indicated locally)"
    if name == "bsl-license.txt" or "boost software license" in lower:
        return "Boost Software License 1.0 (as stated or indicated locally)"
    # Treat Rebol/Red header License: fields as license metadata. Do not
    # interpret arbitrary Markdown/YAML prose containing the word "license" as
    # artifact licensing.
    if "license:" in lower and header_kind(sample) in {"REBOL", "Red", "Red/System"}:
        m = re.search(r"License:\s*(?:\{)?\s*([^\n\r}]+)", sample, re.I)
        if m:
            return m.group(1).strip().strip('"')
    return "UNKNOWN"


def origin_for(path: str, sample: str) -> dict[str, str]:
    # Conservative provenance: local repository is known; exact upstream commit is not.
    p = Path(path)
    lower = sample.lower()
    if "github.com/red/red" in lower or p.parts[:1] in [("runtime",), ("system",), ("environment",), ("modules",), ("libRed",), ("quick-test",)] or path in {"red.r", "compiler.r", "boot.red", "lexer.r", "run-all.r"}:
        return {
            "origin": "retained in local repository; apparent upstream Red project lineage",
            "upstream_project": "Red Programming Language",
            "upstream_url": "https://github.com/red/red (referenced by source headers where present)",
            "repository": "https://github.com/Abdus2023/Red-Cognition-",
            "branch": git("branch", "--show-current") or "UNKNOWN",
            "tag": "UNKNOWN",
            "commit": "UNKNOWN upstream commit; local commit " + git("rev-parse", "HEAD"),
            "version": "UNKNOWN",
            "modification_status": "UNKNOWN",
            "provenance_confidence": "MEDIUM for Red lineage; LOW for exact upstream revision",
        }
    if path.startswith(("rfcs/", "specs/", "cognition/", "dialects/", "docs/wiki/", "docs/implementation/", "docs/specifications/", "docs/governance/", "knowledge-base/")):
        return {
            "origin": "retained in local Red-Cognition repository checkout",
            "upstream_project": "Red-Cognition",
            "upstream_url": "UNKNOWN",
            "repository": "https://github.com/Abdus2023/Red-Cognition-",
            "branch": git("branch", "--show-current") or "UNKNOWN",
            "tag": "UNKNOWN",
            "commit": git("rev-parse", "HEAD"),
            "version": "UNKNOWN",
            "modification_status": "UNKNOWN",
            "provenance_confidence": "MEDIUM for local repository retention; LOW for external origin",
        }
    return {
        "origin": "retained in local repository checkout",
        "upstream_project": "UNKNOWN",
        "upstream_url": "UNKNOWN",
        "repository": "https://github.com/Abdus2023/Red-Cognition-",
        "branch": git("branch", "--show-current") or "UNKNOWN",
        "tag": "UNKNOWN",
        "commit": git("rev-parse", "HEAD"),
        "version": "UNKNOWN",
        "modification_status": "UNKNOWN",
        "provenance_confidence": "LOW",
    }


def classify(path: str, sample: str, binary: bool) -> tuple[str, str]:
    p = Path(path)
    suffix = p.suffix.lower()
    parts = p.parts
    name = p.name.lower()
    hk = header_kind(sample)

    if suffix in ARCHIVE_EXTS:
        return "ARCHIVE", "archive extension"
    if binary:
        return "BINARY", "binary extension or NUL bytes"
    if path.startswith(".github/") or path in {".travis.yml", ".appveyor.yml"}:
        return "BUILD-INFRASTRUCTURE", "CI workflow/configuration path"
    if path.startswith("docker/"):
        if "rebol" in path.lower():
            return "REBOL-BOOTSTRAP", "Docker bootstrap path references Rebol"
        return "BUILD-INFRASTRUCTURE", "Docker path"
    if path.startswith("build/"):
        return "RED-TOOLING", "Red build tooling path"
    if path in {"BSD-3-License.txt", "BSL-License.txt", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md"} or path.startswith("docs/governance/"):
        return "GOVERNANCE", "governance/license path"
    if path.startswith("rfcs/") or p.name.startswith("RFC-"):
        return "RFC", "RFC filename/path"
    if path.startswith(("specs/", "docs/specifications/")):
        return "SPECIFICATION", "specification path"
    if path.startswith("docs/traceability/"):
        return "SPECIFICATION", "traceability specification path"
    if path.startswith("docs/wiki/") or path.startswith("knowledge-base/"):
        return "DOCUMENTATION", "knowledge-base/wiki documentation path"
    if path.startswith("docs/implementation/") or path.startswith("tools/impl_controller") or path.startswith("tools/source-audit/") or path.startswith("tools/impl-") or path.startswith("tools/stage") or path in {"tools/generate_report.py", "tools/generate_repository_index.py", "tools/run-full-pipeline.py", "tools/run-implementation-pipeline.py", "tools/validate_repository_index.py", "tools/validate_rfc_0075_traceability.py"}:
        return "RED-COGNITION", "Red-Cognition implementation/control-plane or audit tooling path"
    if path == "tools/run-container-tests.sh":
        return "RED-TOOLING", "Red/Rebol container test tooling path"
    if path.startswith("docs/"):
        if "red-system" in path.lower():
            return "SPECIFICATION", "Red/System documentation path"
        return "DOCUMENTATION", "documentation path"
    if path.startswith("cognition/") or path.startswith("dialects/"):
        return "RED-COGNITION", "Red-Cognition top-level path"
    if path.startswith("tests/") or path.startswith("quick-test/") or "/tests/" in path:
        if suffix in {".red", ".reds", ".r", ".tests"}:
            return "RED-TEST", "test path with Red/Rebol-family source extension"
        return "RED-FIXTURE", "test path fixture/support artifact"
    if path.startswith("fixtures/"):
        return "RED-FIXTURE", "fixture path"
    if path.startswith("runtime/"):
        return "RED-RUNTIME", "runtime path"
    if path.startswith("environment/"):
        return "RED-RUNTIME", "base environment path"
    if path.startswith("system/runtime/"):
        return "RED-RUNTIME", "system runtime path"
    if path.startswith("system/tests/"):
        return "RED-TEST", "system test path"
    if path.startswith("system/"):
        if suffix == ".r":
            return "RED-COMPILER", "system compiler/linker/emitter/toolchain path"
        if suffix == ".reds":
            return "RED-SYSTEM-SOURCE", "Red/System source under system path"
        return "RED-TOOLING", "system support path"
    if path.startswith("modules/"):
        if suffix == ".reds":
            return "RED-SYSTEM-SOURCE", "module Red/System source"
        if suffix == ".red":
            return "RED-SOURCE", "module Red source"
        return "RED-FIXTURE", "module support artifact"
    if path.startswith(("bridges/", "libRed/")):
        if suffix == ".reds":
            return "RED-SYSTEM-SOURCE", "bridge/libRed Red/System source"
        if suffix in {".red", ".r"}:
            return "RED-SOURCE", "bridge/libRed Red/Rebol-family source"
        return "RED-TOOLING", "bridge/libRed support artifact"
    if path in {"compiler.r", "lexer.r"}:
        return "RED-COMPILER", "top-level compiler source"
    if path == "red.r":
        return "RED-TOOLING", "top-level Red command-line front-end"
    if path == "boot.red":
        return "RED-RUNTIME", "top-level Red base environment source"
    if suffix == ".reds" or hk == "Red/System":
        return "RED-SYSTEM-SOURCE", "Red/System header or extension"
    if suffix == ".red" or hk == "Red":
        return "RED-SOURCE", "Red header or extension"
    if suffix == ".r" or hk == "REBOL":
        # Many .r files are Rebol-implemented Red toolchain components.
        if "red/system" in sample.lower() or "red compiler" in sample.lower() or "red/system compiler" in sample.lower():
            return "RED-COMPILER", "REBOL script participating in Red compiler/toolchain"
        return "REBOL-SOURCE", "REBOL header or .r extension"
    if suffix in DOC_EXTS:
        return "DOCUMENTATION", "text documentation extension"
    if suffix in CONFIG_EXTS or name.startswith("."):
        return "BUILD-INFRASTRUCTURE", "configuration/manifest extension"
    return "UNKNOWN", "no reliable path, extension, or header rule matched"


def normalized_text_hash(path: Path, binary: bool) -> str | None:
    if binary:
        return None
    data = path.read_text("utf-8", "replace")
    data = data.replace("\r\n", "\n").replace("\r", "\n")
    data = "\n".join(line.rstrip() for line in data.split("\n"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def collect() -> dict[str, Any]:
    branch = git("branch", "--show-current") or "UNKNOWN"
    commit = git("rev-parse", "HEAD")
    status = git("status", "--short")
    files = []
    sha_groups: dict[str, list[str]] = defaultdict(list)
    filename_groups: dict[str, list[str]] = defaultdict(list)
    normalized_groups: dict[str, list[str]] = defaultdict(list)
    for rel in tracked_files():
        path = ROOT / rel
        data = path.read_bytes()
        suffix = path.suffix.lower()
        binary = is_binary_bytes(data, suffix)
        sample = data[:32768].decode("utf-8", "replace") if not binary else ""
        digest = hashlib.sha256(data).hexdigest()
        norm = normalized_text_hash(path, binary)
        classification, reason = classify(rel, sample, binary)
        origin = origin_for(rel, sample)
        entry = {
            "path": rel,
            "size": len(data),
            "sha256": digest,
            "normalized_sha256": norm,
            "classification": classification,
            "classification_reason": reason,
            "header_kind": header_kind(sample),
            "binary": binary,
            "license": detect_license(sample, rel),
            "copyright": "FOUND" if "copyright" in sample.lower() else "UNKNOWN",
            "retrieval_date": TODAY,
            "local_path": rel,
            **origin,
        }
        files.append(entry)
        sha_groups[digest].append(rel)
        filename_groups[path.name.lower()].append(rel)
        if norm:
            normalized_groups[norm].append(rel)

    exact = [{"relationship": "IDENTICAL", "sha256": k, "paths": v} for k, v in sorted(sha_groups.items()) if len(v) > 1]
    same_name = [{"relationship": "RELATED-VARIANT", "filename": k, "paths": v} for k, v in sorted(filename_groups.items()) if len(v) > 1]
    normalized = [{"relationship": "LIKELY-DUPLICATE", "normalized_sha256": k, "paths": v} for k, v in sorted(normalized_groups.items()) if len(v) > 1 and len({sha256(ROOT / p) for p in v}) > 1]

    return {
        "schema_version": 1,
        "generated": {
            "date": TODAY,
            "timestamp_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
            "tool": SCRIPT_PATH,
            "method": "git ls-files enumeration; local byte-size and SHA-256 hashing; conservative rule-based classification from path, extension, and source headers",
            "scope": "tracked files at generation time; generated outputs are listed separately and may not be self-included in SHA256SUMS",
        },
        "repository": {
            "url": "https://github.com/Abdus2023/Red-Cognition-",
            "branch": branch,
            "commit": commit,
            "primary_development_branch_from_user_request": "audio",
            "working_tree_status_at_generation": status or "clean",
            "initial_reconnaissance_status": "clean (observed before repository modifications in this Arena turn)",
        },
        "files": files,
        "summary": {
            "total_files": len(files),
            "by_classification": dict(sorted(Counter(f["classification"] for f in files).items())),
            "by_extension": dict(sorted(Counter(Path(f["path"]).suffix.lower() or "[no extension]" for f in files).items())),
            "binary_files": sum(1 for f in files if f["binary"]),
            "red_header_files": sum(1 for f in files if f["header_kind"] == "Red"),
            "red_system_header_files": sum(1 for f in files if f["header_kind"] == "Red/System"),
            "rebol_header_files": sum(1 for f in files if f["header_kind"] == "REBOL"),
            "unknown_files": sum(1 for f in files if f["classification"] == "UNKNOWN"),
        },
        "duplicates": {
            "exact_sha256_groups": exact,
            "same_filename_groups": same_name,
            "normalized_content_groups": normalized,
            "policy": "No duplicates were deleted. Historical variants require owner review before consolidation.",
        },
        "migration_manifest": {
            "status": "NO_MOVES_PERFORMED",
            "entries": [],
            "reason": "Reconnaissance established inventory/provenance baseline first; no destructive migration was justified in this phase.",
        },
        "tests": {
            "discovery_status": "DISCOVERED",
            "execution_status": "NOT-RUN by this inventory generator",
            "known_test_roots": ["tests/", "quick-test/", "system/tests/", "modules/audio/tests/", "tools/impl_controller/tests/"],
            "red_family_test_files": [f["path"] for f in files if f["classification"] == "RED-TEST"],
        },
        "bootstrap": {
            "status": "PROVISIONAL",
            "stage0": "External Rebol 2 interpreter required; not vendored as source artifact.",
            "known_ci_bootstrap_binary": {
                "url": "https://static.red-lang.org/tmp/rebol",
                "sha256": "1c902e0f75e994d739975e12963323832ce00f52208b3287cbfe5e7029d856d6",
                "source": ".github/workflows/red-container-tests.yml",
                "execution_status": "NOT-RUN locally by this generator",
            },
        },
    }


def rel_link(path: str) -> str:
    return "../" * 2 + path


def write_json(data: dict[str, Any]) -> None:
    out = ROOT / OUTPUTS["inventory_json"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def write_sha256sums(data: dict[str, Any]) -> None:
    out = ROOT / OUTPUTS["sha256sums"]
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Generated by tools/source-audit/generate_rebol_red_inventory.py",
        f"# Date: {TODAY}",
        f"# Repository commit: {data['repository']['commit']}",
        "# Scope: tracked files enumerated by git ls-files before writing this checksum file.",
    ]
    for f in sorted(data["files"], key=lambda x: x["path"]):
        lines.append(f"{f['sha256']}  {f['path']}")
    out.write_text("\n".join(lines) + "\n")


def table_counts(counter: dict[str, int]) -> str:
    return "\n".join(f"| {k} | {v} |" for k, v in counter.items())


def write_inventory_md(data: dict[str, Any]) -> None:
    out = ROOT / OUTPUTS["inventory_md"]
    out.parent.mkdir(parents=True, exist_ok=True)
    s = data["summary"]
    lines = [
        "# Rebol + Red Inventory",
        "",
        f"Generated: {data['generated']['timestamp_utc']}",
        f"Tool: `{data['generated']['tool']}`",
        f"Repository: `{data['repository']['url']}`",
        f"Branch: `{data['repository']['branch']}`",
        f"Commit: `{data['repository']['commit']}`",
        "",
        "## Scope and Method",
        data["generated"]["method"] + ".",
        "No upstream source was moved or rewritten by this inventory phase.",
        "",
        "## Summary",
        f"- Total tracked files inventoried: {s['total_files']}",
        f"- Binary files: {s['binary_files']}",
        f"- Files with `REBOL [` headers: {s['rebol_header_files']}",
        f"- Files with `Red [` headers: {s['red_header_files']}",
        f"- Files with `Red/System [` headers: {s['red_system_header_files']}",
        f"- UNKNOWN classifications: {s['unknown_files']}",
        "",
        "## Classification Counts",
        "| Classification | Count |",
        "|---|---:|",
        table_counts(s["by_classification"]),
        "",
        "## Key Inventories",
    ]
    for cls in ["REBOL-SOURCE", "REBOL-TOOLING", "REBOL-BOOTSTRAP", "RED-COMPILER", "RED-RUNTIME", "RED-SYSTEM-SOURCE", "RED-SOURCE", "RED-TEST", "RED-FIXTURE", "RED-COGNITION", "SPECIFICATION", "RFC", "BINARY", "ARCHIVE", "UNKNOWN"]:
        paths = [f["path"] for f in data["files"] if f["classification"] == cls]
        if not paths:
            continue
        lines += ["", f"### {cls} ({len(paths)})"]
        for p in paths[:80]:
            lines.append(f"- `{p}`")
        if len(paths) > 80:
            lines.append(f"- ... {len(paths) - 80} additional entries in `{OUTPUTS['inventory_json']}`")
    lines += [
        "",
        "## Duplicate Analysis Summary",
        f"- Exact SHA-256 duplicate groups: {len(data['duplicates']['exact_sha256_groups'])}",
        f"- Same filename groups: {len(data['duplicates']['same_filename_groups'])}",
        f"- Normalized-content likely duplicate groups: {len(data['duplicates']['normalized_content_groups'])}",
        "- Policy: no duplicate deletion was performed.",
        "",
    ]
    out.write_text("\n".join(lines))


def write_architecture(data: dict[str, Any]) -> None:
    out = ROOT / OUTPUTS["architecture_md"]
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Rebol + Red Monorepository Architecture",
        "",
        f"Generated by `{SCRIPT_PATH}` on {TODAY} from commit `{data['repository']['commit']}`.",
        "",
        "## Lineage Model",
        "",
        "```text",
        "REBOL bootstrap/interpreter lineage",
        "  ↓",
        "Red/System compiler and low-level runtime sources",
        "  ↓",
        "Red compiler, runtime, environment, modules, and tests",
        "  ↓",
        "Red-Cognition RFCs, specifications, governance, traceability, and implementation-control artifacts",
        "```",
        "",
        "## Current Non-Destructive Layout Map",
        "",
        "The checkout currently retains the historical Red source-tree layout. This phase did not move source files because exact upstream revision/provenance and owner-approved target paths have not yet been established.",
        "",
        "| Conceptual monorepo area | Current repository paths | Status |",
        "|---|---|---|",
        "| `rebol/bootstrap` | `.github/workflows/red-container-tests.yml`, `docker/rebol-bootstrap/`, Rebol `.r` build/test scripts | External bootstrap dependency documented; source/interpreter not vendored |",
        "| `red/compiler` | `compiler.r`, `red.r`, `lexer.r`, `system/compiler.r`, `system/emitter.r`, `system/linker.r`, `system/formats/` | Retained in place |",
        "| `red/red-system` | `system/`, `runtime/*.reds`, `modules/**/*.reds`, `environment/console/**/*.reds` | Retained in place; classifications recorded |",
        "| `red/runtime` | `runtime/`, `environment/`, `boot.red` | Retained in place |",
        "| `red/tools` | `build/`, `quick-test/`, `tools/run-container-tests.sh`, bridge tooling | Retained in place |",
        "| `red/tests` | `tests/`, `system/tests/`, `quick-test/tests/`, `modules/audio/tests/` | Discovered; not all executed locally |",
        "| `red-cognition/rfc` | `rfcs/`, RFC-related docs | Retained in place |",
        "| `red-cognition/specs` | `specs/`, `docs/specifications/`, `docs/traceability/` | Retained in place |",
        "| `red-cognition/governance` | `docs/governance/`, top-level governance docs | Retained in place |",
        "| `red-cognition/implementation` | `docs/implementation/`, `tools/impl_controller/`, `cognition/`, `dialects/` | Retained in place |",
        "| `verification/*` | `verification/inventory/`, `verification/hashes/`, `verification/reports/` | Added by this phase |",
        "",
        "## Migration Policy",
        "",
        "Future physical moves should use the migration-safety process in `verification/reports/MONOREPO_AUDIT.md`: hash before, move, hash after, record old/new path and transformation. Until then, this architecture document is an overlay map, not a destructive refactor.",
        "",
    ]
    out.write_text("\n".join(lines))


def write_provenance(data: dict[str, Any]) -> None:
    out = ROOT / OUTPUTS["provenance_md"]
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Provenance",
        "",
        f"Generated by `{SCRIPT_PATH}` on {TODAY} from commit `{data['repository']['commit']}`.",
        "",
        "## Evidence Boundaries",
        "",
        "- SHA-256 values were calculated locally from repository file bytes.",
        "- Upstream exact commits, tags, versions, and modification status remain `UNKNOWN` unless explicitly present in local source headers, repository configuration, or separately generated comparison evidence.",
        "- A supplemental comparison against upstream Red `v0.6.4` is recorded in `verification/provenance/RED_UPSTREAM_V0_6_4_COMPARISON.json`; it verifies byte identity for matching files only and does not prove pristine state for diverged files.",
        "- Red-Cognition artifacts are retained from this repository checkout; external origins are not inferred.",
        "",
        "## Known Origins",
        "",
        "| Area | Origin evidence | Confidence | Unknowns |",
        "|---|---|---|---|",
        "| Red compiler/runtime/tooling | Headers reference Red Foundation and `https://github.com/red/red`; README describes Red toolchain; supplemental SHA-256 comparison against Red `v0.6.4` peeled commit `755eb943ccea9e78c2cab0f20b313a52404355cb` | High for byte-identical files matched to `v0.6.4`; medium lineage confidence otherwise | Intentionality of diverged files, history after/before `v0.6.4` |",                
        "| Rebol bootstrap | README and CI require Rebol2 interpreter; container workflow downloads `https://static.red-lang.org/tmp/rebol` with SHA-256 | Medium for bootstrap dependency | Source provenance for the binary, local execution status |",
        "| Red-Cognition RFC/spec/governance docs | Present in this checkout under `rfcs/`, `docs/`, `knowledge-base/`, `specs/` | Medium for local retention | External origin/history |",
        "| Binary/library artifacts | Present as tracked bytes and hashed in inventory | Medium for local bytes | Build provenance and reproducibility |",
        "",
        "## Machine-Readable Provenance",
        "",
        f"Per-file provenance fields are recorded in `{OUTPUTS['inventory_json']}`. Unknown fields are explicitly represented as `UNKNOWN` rather than inferred.",
        "Supplemental upstream comparison evidence is recorded in `verification/provenance/RED_UPSTREAM_V0_6_4_COMPARISON.json` and summarized in `verification/reports/RED_UPSTREAM_V0_6_4_COMPARISON.md`.",
        "",
    ]
    out.write_text("\n".join(lines))


def write_bootstrap(data: dict[str, Any]) -> None:
    out = ROOT / OUTPUTS["bootstrap_md"]
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Bootstrap Model",
        "",
        f"Generated by `{SCRIPT_PATH}` on {TODAY} from commit `{data['repository']['commit']}`.",
        "",
        "## Stage Model",
        "",
        "| Stage | Required tool | Input artifacts | Output artifacts | Execution status | Reproducibility status |",
        "|---|---|---|---|---|---|",
        "| Stage 0 | Host OS plus external Rebol 2 interpreter | External `rebol`/`rebview` binary; CI references `https://static.red-lang.org/tmp/rebol` SHA-256 `1c902e0f75e994d739975e12963323832ce00f52208b3287cbfe5e7029d856d6` | Runnable bootstrap interpreter | NOT-RUN locally; CI metadata in `verification/reports/CI_EVIDENCE.md` records successful bootstrap download/verification steps in observed container workflows | PROVISIONAL/BLOCKED for offline use because binary source is not vendored |"
        "| Rebol bootstrap | Rebol 2.x interpreter | `.r` scripts, `compiler.r`, `system/*.r`, tests runners | Red/System and Red compilation steps | NOT-RUN locally in this phase | PROVISIONAL |",
        "| Red compiler bootstrap | Rebol-implemented Red compiler | `red.r`, `compiler.r`, `system/compiler.r`, `lexer.r`, `utils/`, `runtime/` | Red executables/libraries when build is run | NOT-RUN locally in this phase | PROVISIONAL |",
        "| Red/System | Red/System compiler and `.reds` sources | `runtime/*.reds`, `system/runtime/*.reds`, modules/bridges `.reds` | Low-level runtime/library artifacts | NOT-RUN locally in this phase | PROVISIONAL |",
        "| Red runtime/compiler | Red compiler/runtime sources | `boot.red`, `environment/`, `runtime/`, `libRed/` | Red runtime/libRed products | NOT-RUN locally in this phase | PROVISIONAL |",
        "| Red-Cognition tooling | Python control-plane tools and RFC/spec docs | `tools/impl_controller/`, `tools/source-audit/`, `docs/implementation/`, `rfcs/`, `specs/` | Generated reports/status documents | Source-audit generators and existing repository/RFC validators executed; see `verification/reports/LOCAL_EXECUTION_EVIDENCE.md` | PARTIALLY_VERIFIED for source-audit outputs; RFC-0075 validator currently FAILS with known critical gaps |"
        "",
        "## Offline Status",
        "",
        "- SOURCE-AVAILABLE: Red and Red-Cognition source/documentation in this checkout are available offline.",
        "- BUILD-AVAILABLE: BLOCKED until required Rebol bootstrap interpreter/container availability is demonstrated offline.",
        "- BOOTSTRAP-AVAILABLE: BLOCKED for Stage 0 because the Rebol binary is an external network dependency in CI.",
        "- EXECUTION-AVAILABLE: PARTIALLY_VERIFIED only for Python source-audit/report validation commands listed in `verification/reports/LOCAL_EXECUTION_EVIDENCE.md`; Red/Rebol tests were not executed locally by this phase.",
        "",
    ]
    out.write_text("\n".join(lines))


def write_audit(data: dict[str, Any]) -> None:
    out = ROOT / OUTPUTS["audit_md"]
    out.parent.mkdir(parents=True, exist_ok=True)
    s = data["summary"]
    tests = data["tests"]
    lines = [
        "# Monorepo Audit",
        "",
        f"Generated by `{SCRIPT_PATH}` on {TODAY} from commit `{data['repository']['commit']}`.",
        "",
        "## Repository Identity",
        f"- Repository: `{data['repository']['url']}`",
        f"- Current branch: `{data['repository']['branch']}`",
        f"- Primary development branch stated by user: `audio`",
        f"- Current commit at reconnaissance: `{data['repository']['commit']}`",
        f"- Initial reconnaissance working tree status: `{data['repository']['initial_reconnaissance_status']}`",
        "- Working tree status at report generation: recorded in `verification/inventory/REBOL_RED_INVENTORY.json`; generated-file updates may appear dirty during generation.",
        "",
        "## Result",
        "PROVISIONAL: repository inventory, hashing, conservative classification, and documentation baseline were established. Red/Rebol bootstrap and test execution remain blocked/not-run locally in this phase.",
        "",
        "## Inventory Summary",
        f"- Total tracked files: {s['total_files']}",
        f"- Binary files: {s['binary_files']}",
        f"- REBOL header files: {s['rebol_header_files']}",
        f"- Red header files: {s['red_header_files']}",
        f"- Red/System header files: {s['red_system_header_files']}",
        "",
        "### Classification Counts",
        "| Classification | Count |",
        "|---|---:|",
        table_counts(s["by_classification"]),
        "",
        "## Duplicate Analysis",
        f"- IDENTICAL exact SHA-256 groups: {len(data['duplicates']['exact_sha256_groups'])}",
        f"- RELATED-VARIANT same-filename groups: {len(data['duplicates']['same_filename_groups'])}",
        f"- LIKELY-DUPLICATE normalized-content groups: {len(data['duplicates']['normalized_content_groups'])}",
        "- No duplicate artifacts were deleted or merged.",
        "",
        "## Migration Manifest",
        f"- Status: {data['migration_manifest']['status']}",
        f"- Entries: {len(data['migration_manifest']['entries'])}",
        f"- Reason: {data['migration_manifest']['reason']}",
        "",
        "## License Analysis",
        "License indications are recorded per file where present. Repository-level license files `BSD-3-License.txt` and `BSL-License.txt` are retained. No reconciliation or relicensing was performed.",
        "",
        "## Binary and Archive Inventory",
        "- Dedicated binary/archive inventory is generated in `verification/inventory/BINARY_INVENTORY.json` and summarized in `verification/reports/BINARY_INVENTORY.md`.",
        "- Binary/archive artifacts are retained and hashed; none are promoted to source/bootstrap status without build provenance.",
        "",
        "## Offline Dependency Analysis",
        "- Offline dependency scan is generated in `verification/reproducibility/OFFLINE_DEPENDENCIES.json` and summarized in `verification/reports/OFFLINE_STATUS.md`.",
        "- BUILD-AVAILABLE and BOOTSTRAP-AVAILABLE remain blocked for fully offline operation until external toolchain/bootstrap requirements are locally provisioned and executed.",
        "",
        "## Owner Decision Register",
        "- Owner decisions are generated in `verification/inventory/OWNER_DECISIONS.json` and summarized in `verification/reports/OWNER_DECISIONS.md`.",
        "- Blocking decisions include physical migration authority, upstream Red baseline authority, bootstrap strategy, and diverged-file classification.",
        "",
        "## Conflict Register",
        "- Conflict records are generated in `verification/inventory/CONFLICT_REGISTER.json` and summarized in `verification/reports/CONFLICT_REGISTER.md`.",
        "- The register flags same-filename variants, upstream-divergence records, binary provenance gaps, and RFC-0075 validation failure without selecting a winner or deleting artifacts.",
        "",
        "## Logical Path Map",
        "- Proposed conceptual destination paths are generated in `verification/inventory/MONOREPO_PATH_MAP.json` and summarized in `verification/reports/MONOREPO_PATH_MAP.md`.",
        "- The path map is an overlay only; every entry is `PROPOSED_NOT_EXECUTED` and no move is claimed.",
        "",
        "## Manifest Validation",
        "- Generated manifests and SHA-256 records are validated by `tools/source-audit/validate_monorepo_audit.py`.",
        "- Validation evidence is written to `verification/reports/MANIFEST_VALIDATION.json` and `verification/reports/MANIFEST_VALIDATION.md`.",
        "",
        "## Upstream Provenance Comparison",
        "- Upstream Red tag `v0.6.4` was explicitly fetched from `https://github.com/red/red.git` and compared by SHA-256 in this phase.",
        "- Peeled upstream commit: `755eb943ccea9e78c2cab0f20b313a52404355cb`.",
        "- Result summary: 251 local files matched upstream at the same path, 13 matched upstream content at relocated/renamed paths, 258 diverged at the same path, and 596 were local-only/non-Red-upstream relative to `v0.6.4` after excluding generated audit artifacts from comparison.",
        "- Diverged files are not automatically classified as intentional local modifications; maintainer review is required.",
        "- Evidence: `verification/provenance/RED_UPSTREAM_V0_6_4_COMPARISON.json` and `verification/reports/RED_UPSTREAM_V0_6_4_COMPARISON.md`.",
        "",
        "## Test Status",
        f"- Discovery: {tests['discovery_status']}",
        f"- Red-family test files discovered: {len(tests['red_family_test_files'])}",
        "- Executed locally in this consolidation phase: inventory generator, supplemental manifest generator, checksum verification, inventory/supplemental JSON validation, source-audit Python bytecode compilation, repository index validator, and RFC-0075 traceability validator.",
        "- Passed locally: inventory generation, supplemental manifest generation, checksum verification, JSON validation, source-audit Python bytecode compilation, and repository index validator.",
        "- Failed locally: RFC-0075 traceability validator reported unresolved critical gaps; this is preserved as evidence, not fixed or reclassified.",
        "- Blocked locally: `python3 -m pytest tools/impl_controller/tests` did not execute tests because `pytest` is not installed.",
        "- Red/Rebol suites: NOT-RUN locally; `rebol`/`red` executables are not on PATH in this sandbox reconnaissance.",
        "- Container suite: NOT-RUN locally; Docker execution was not established by this phase.",
        "- Detailed local command evidence: `verification/reports/LOCAL_EXECUTION_EVIDENCE.md`.",
        "- Test inventory: `verification/inventory/TEST_INVENTORY.json` and `verification/reports/TEST_STATUS.md`.",
        "",
        "## CI Status",
        "- `.github/workflows/main.yml` discovered Windows jobs that download `rebview.exe` and run Red suites.",
        "- `.github/workflows/red-container-tests.yml` discovered Ubuntu container tests using a pinned Rebol SHA-256.",
        "- GitHub Actions runs were observed after pushes to `arena/01a058c5-red-cognition`.",
        "- Windows workflow run `33428373251` for commit `de7913f4e9156a1a093e84fc33c73dfee284cc4f` completed with conclusion `failure`; observed jobs failed during `Set up job`.",
        "- Red container tests workflow run `33428373183` for commit `de7913f4e9156a1a093e84fc33c73dfee284cc4f` completed with conclusion `cancelled`; bootstrap download/verification and image build steps succeeded, while `Run Red and Red/System container tests` was cancelled.",
        "- Earlier Red container tests run `33418665227` for commit `b4c5005efcfc7810a1ff24ed508c62ad4bfeeec2` completed with conclusion `cancelled` during the Red/Red-System test step.",
        "- No successful CI conclusion is claimed for Red, Red/System, or Red-Cognition tests.",
        "- Detailed CI metadata evidence: `verification/reports/CI_EVIDENCE.md`.",
        "",
        "## Offline Status",
        "SOURCE-AVAILABLE is partially established by local source presence and hashes. BUILD-AVAILABLE, BOOTSTRAP-AVAILABLE, and EXECUTION-AVAILABLE for Red/Rebol are not established locally; Stage 0 depends on external bootstrap binaries unless separately provisioned.",
        "",
        "## Blocked Items",
        "- Exact upstream Red `v0.6.4` tag comparison was performed, but exact provenance for files not matching that tag remains UNKNOWN/BLOCKED pending additional upstream research.",
        "- Intentional local modification status for files diverged from upstream Red `v0.6.4` remains UNKNOWN/BLOCKED pending maintainer review.",
        "- Offline Stage 0 Rebol bootstrap: BLOCKED; CI downloads external binary.",
        "- Red/Rebol tests: BLOCKED locally without runnable Rebol/Red toolchain or verified container execution.",
        "",
        "## Unknown Items",
        "- Per-file external origin for many Red-Cognition documents.",
        "- Build provenance for tracked binary/library artifacts.",
        "- Whether same-filename groups represent intentional platform variants, historical variants, or conflicts.",
        "",
        "## Open Decisions",
        "- OWNER DECISION REQUIRED before physically moving historical Red source into new `red/` or `rebol/` subtrees.",
        "- OWNER DECISION REQUIRED on whether to vendor source-buildable bootstrap material or keep external bootstrap binary workflow.",
        "",
        "## Evidence Files",
        f"- `{OUTPUTS['inventory_json']}`",
        f"- `{OUTPUTS['inventory_md']}`",
        f"- `{OUTPUTS['sha256sums']}`",
        f"- `{OUTPUTS['architecture_md']}`",
        f"- `{OUTPUTS['provenance_md']}`",
        f"- `{OUTPUTS['bootstrap_md']}`",
        "- `verification/inventory/MIGRATION_MANIFEST.json`",
        "- `verification/inventory/DUPLICATE_ANALYSIS.json`",
        "- `verification/inventory/TEST_INVENTORY.json`",
        "- `verification/inventory/BINARY_INVENTORY.json`",
        "- `verification/inventory/OWNER_DECISIONS.json`",
        "- `verification/inventory/CONFLICT_REGISTER.json`",
        "- `verification/inventory/MONOREPO_PATH_MAP.json`",
        "- `verification/reports/MANIFEST_VALIDATION.json`",
        "- `verification/provenance/PROVENANCE_MANIFEST.json`",
        "- `verification/provenance/LICENSE_SUMMARY.json`",
        "- `verification/reproducibility/OFFLINE_DEPENDENCIES.json`",
        "- `verification/provenance/RED_UPSTREAM_V0_6_4_COMPARISON.json`",
        "- `verification/reports/RED_UPSTREAM_V0_6_4_COMPARISON.md`",
        "- `verification/reports/BINARY_INVENTORY.md`",
        "- `verification/reports/LICENSE_SUMMARY.md`",
        "- `verification/reports/OFFLINE_STATUS.md`",
        "- `verification/reports/OWNER_DECISIONS.md`",
        "- `verification/reports/CONFLICT_REGISTER.md`",
        "- `verification/reports/MONOREPO_PATH_MAP.md`",
        "- `verification/reports/MANIFEST_VALIDATION.md`",
        "- `verification/reports/DUPLICATE_ANALYSIS.md`",
        "- `verification/reports/TEST_STATUS.md`",
        "- `verification/reports/LOCAL_EXECUTION_EVIDENCE.md`",
        "- `verification/reports/CI_EVIDENCE.md`", 
        "",
    ]
    out.write_text("\n".join(lines))


def main() -> None:
    os.chdir(ROOT)
    data = collect()
    write_json(data)
    write_sha256sums(data)
    write_inventory_md(data)
    write_architecture(data)
    write_provenance(data)
    write_bootstrap(data)
    write_audit(data)
    print(json.dumps({"result": "ok", "outputs": OUTPUTS, "summary": data["summary"]}, indent=2))


if __name__ == "__main__":
    main()
