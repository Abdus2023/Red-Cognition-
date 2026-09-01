#!/usr/bin/env python3
"""
Stage 05 — Finalize.
Builds:
  artifacts/manifests/artifacts.json        (unified machine-readable manifest)
  artifacts/manifests/sha256sums.txt
  artifacts/provenance/provenance.json      (provenance graph with evidence)
  artifacts/provenance/reconciliation.json  (cross-source reconciliation tables)
  artifacts/reports/collection-report.json
  artifacts/reports/collection-report.md
  artifacts/logs/blocked-attempts.json
  artifacts/logs/execution/execution-evidence.json
"""
import hashlib, json, os, subprocess, time

ROOT = "/home/user/Red-Cognition-"
A = os.path.join(ROOT, "artifacts")
MAN, PROV, REP, LOGS = (os.path.join(A, d) for d in ("manifests", "provenance", "reports", "logs"))
EXE = os.path.join(LOGS, "execution")
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def load(p):
    with open(p) as f:
        return json.load(f)

disc = load(os.path.join(MAN, "github-discovery.json"))
gitc = load(os.path.join(MAN, "git-collection.json"))
dls = load(os.path.join(MAN, "downloads.json"))
insp = load(os.path.join(MAN, "source-inspection.json"))

artifacts = []
def add(**kw):
    kw.setdefault("retrieved_at", NOW)
    kw.setdefault("integrity_status", "HASHED")
    artifacts.append(kw)

# ---------------------------------------------------------------- downloads
for d in dls["downloads"]:
    name = os.path.basename(d["dest"])
    cls, proj = d["classification"], d["project"]
    if "libRed" in name or "libstruct" in name or "structlib" in name:
        cls = "BINARY"
        role = "test fixture shipped inside upstream red/red tree (not a standalone release binary)"
    proj_out = proj
    lic_map = {"rebol-syntax": "UNCLEAR"}  # no LICENSE file; README-only
    lic = "UNCLEAR" if "rebol-syntax" in name else "CONFIRMED"
    add(project=proj_out, version=d["version_claim"], classification=cls,
        origin=d["origin"], url=d["url"], repository=d["repository"],
        commit=d["pinned_ref"].split("->")[-1].strip() if "->" in d["pinned_ref"] else d["pinned_ref"],
        tag=d["pinned_ref"].split("->")[0].strip() if "->" in d["pinned_ref"] else None,
        filename=name, path=d["dest"], sha256=d["sha256"], size=d["size"],
        retrieved_at=d["retrieved_at"], provenance_status="VERIFIED",
        license_status=lic,
        license_evidence={
            "RED": "BSD-3-License.txt + BSL-License.txt inside archive (hashed in source-inspection.json)",
            "REBOL": "LICENSE file inside archive (hashed in source-inspection.json)",
        }.get(proj), integrity_status="HASH_MATCHED" if d.get("git_hash_object_check", {}).get("match") else "HASHED",
        notes=d.get("role") or ("GitHub auto-generated archive of pinned ref; bytes not authored by GitHub (tree contents of the commit)"))

# ---- repo evidence ----
REPO_META = {
    "red": dict(owner="red", official=True, tier=1,
                license="BSL-1.0 (repo metadata) + BSD-3-License.txt/BSL-License.txt in tree",
                desc=disc["repositories"]["red/red"].get("description"),
                url="https://github.com/red/red", default_branch="master"),
    "rebol_rebol": dict(owner="rebol", official=True, tier=1, license="Apache-2.0",
                        desc=disc["repositories"]["rebol/rebol"].get("description"),
                        url="https://github.com/rebol/rebol", default_branch="master"),
    "rebolsource_r3": dict(owner="rebolsource", official=False, tier=2,
                           license="Apache-2.0 (identical LICENSE hash to rebol/rebol)",
                           desc=disc["repositories"].get("rebolsource_r3", {}).get("description") or "Source code for the Rebol [R3] interpreter (rebolsource org)",
                           url="https://github.com/rebolsource/r3", default_branch="master"),
    "metaeducation_ren-c": dict(owner="metaeducation", official=False, tier=2, license="LGPL-3.0",
                                desc=disc["repositories"]["metaeducation/ren-c"].get("description"),
                                url="https://github.com/metaeducation/ren-c", default_branch="master"),
    "Oldes_Rebol3": dict(owner="Oldes", official=False, tier=3, license="Apache-2.0 (LICENSE text identical to rebol/rebol; bundled extensions NOT individually verified)",
                         desc=disc["repositories"]["Oldes/Rebol3"].get("description"),
                         url="https://github.com/Oldes/Rebol3", default_branch="master"),
    "rebolsource_rebol-syntax": dict(owner="rebolsource", official=False, tier=2, license="UNCLEAR (no LICENSE file; README only)",
                                     desc="Formal specification of Rebol syntax",
                                     url="https://github.com/rebolsource/rebol-syntax", default_branch="master"),
    "rebolsource_rebol-test": dict(owner="rebolsource", official=False, tier=2, license="Apache-2.0",
                                   desc="Suite of regression tests for Rebol (R2 and R3)",
                                   url="https://github.com/rebolsource/rebol-test", default_branch="master"),
}
for key, rec in gitc["repos"].items():
    if key == "workspace-fork":
        continue
    meta = REPO_META[key]
    # distinct deterministic digest: sha256 over this repo's tree-manifest .lsr files
    h = hashlib.sha256()
    for ref, tm in sorted(rec["tree_manifests"].items()):
        if isinstance(tm, dict):
            with open(os.path.join(ROOT, tm["path"]), "rb") as f:
                h.update(f.read())
    ev_digest = h.hexdigest()
    ev_paths = [os.path.relpath(os.path.join(MAN, "trees"), ROOT)]
    add(project="RED" if key == "red" else "REBOL", version=None, classification="METADATA",
        origin="GitHub API repository metadata + git clone evidence (blobless clone in session storage)",
        url=meta["url"], repository=meta["url"], commit=rec["head_commit"],
        tag=None, filename=f"{key}.git-evidence", path="artifacts/manifests/git-collection.json#" + key,
        sha256=ev_digest, size=None,
        provenance_status="VERIFIED" if meta["official"] else "PARTIALLY_VERIFIED",
        provenance_status_reason="official upstream organization" if meta["official"] else
                                 "third-party/historical repository; lineage partially established via git merge-base evidence (see provenance.json)",
        license_status="CONFIRMED" if meta["license"].startswith(("Apache", "BSL", "LGPL")) else "UNCLEAR",
        license_evidence=meta["license"], tier=meta["tier"], official=meta["official"],
        head_commit=rec["head_commit"], commit_count=rec["commit_count"],
        describe=rec["describe"], tag_count=rec["tag_count"],
        tree_manifests=rec["tree_manifests"],
        integrity_status="HASHED",
        hash_note="sha256 over the repo's deterministic tree-manifest files (git ls-tree output)")

# Red/System derived records (material inside red/red v0.6.6 tree)
v066_tree = os.path.join(MAN, "trees", "red__v0.6.6.lsr")
sys_tests = sys_src = 0
with open(v066_tree) as f:
    for line in f:
        p = line.split("\t", 1)[1].strip() if "\t" in line else ""
        if p.startswith("system/tests/"): sys_tests += 1
        elif p.startswith("system/"): sys_src += 1
add(project="RED_SYSTEM", version="0.6.6 (same tree as red/red v0.6.6)", classification="SOURCE",
    origin="red/red tag v0.6.6 tree (system/ directory: Red/System compiler, runtime, docs)",
    url="https://github.com/red/red/tree/v0.6.6/system", repository="https://github.com/red/red",
    commit="6942c7a021253150c3e3cf90428305892340db03", tag="v0.6.6",
    filename="red-system-source@v0.6.6", path="inside artifacts/red/releases/red-0.6.6.tar.gz + red__v0.6.6.lsr",
    sha256=sha256_file(os.path.join(ROOT, "artifacts/red/releases/red-0.6.6.tar.gz")),
    size=None, provenance_status="VERIFIED", license_status="CONFIRMED",
    license_evidence="BSD-3-License.txt + BSL-License.txt in same tree", tree_file_count=sys_src,
    notes="Red/System is part of the red/red repository; source counted from deterministic tree manifest")
add(project="RED_SYSTEM", version="0.6.6", classification="TEST_SUITE",
    origin="red/red tag v0.6.6 tree (system/tests/ directory: Red/System test suite)",
    url="https://github.com/red/red/tree/v0.6.6/system/tests", repository="https://github.com/red/red",
    commit="6942c7a021253150c3e3cf90428305892340db03", tag="v0.6.6",
    filename="red-system-tests@v0.6.6", path="inside artifacts/red/releases/red-0.6.6.tar.gz + red__v0.6.6.lsr",
    sha256=sha256_file(os.path.join(ROOT, "artifacts/red/releases/red-0.6.6.tar.gz")),
    size=None, provenance_status="VERIFIED", license_status="CONFIRMED",
    license_evidence="BSD-3-License.txt + BSL-License.txt in same tree", tree_file_count=sys_tests,
    notes="97 Red/System test files counted in v0.6.6 tree manifest; NOT executed this session")

# workspace fork tree
wf = gitc["repos"]["workspace-fork"]
add(project="RED", version="0.6.4 (version.r claim)", classification="SOURCE",
    origin="pre-existing working tree of https://github.com/Abdus2023/Red-Cognition- (THIRD_PARTY fork; single fork-original commit)",
    url="https://github.com/Abdus2023/Red-Cognition-", repository="https://github.com/Abdus2023/Red-Cognition-",
    commit=wf["head_commit"], tag=None, filename="workspace-fork-tree", path="(repository working tree)",
    sha256=None, size=None, integrity_status="NO_REFERENCE_HASH",
    provenance_status="PARTIALLY_VERIFIED",
    provenance_status_reason="248/530 upstream v0.6.4 source files byte-identical (git blob SHA match); 253 files differ; 334 fork-only files; commit 742181a NOT present in upstream red/red history (upstream rejects ref)",
    license_status="CONFIRMED", license_evidence="BSD-3-License.txt + BSL-License.txt in tree root",
    tree_manifest=wf["tree_manifest"],
    notes="fork head commit authored 2026-08-31 by Abdus2023; not an upstream red/red commit")

# prior-session lead binary
lead = insp["previous_session_lead"]
add(project="REBOL", version="2.7.8 (filename claim only - UNVERIFIED)", classification="BINARY",
    origin="UNKNOWN - found inside repo zip artifacts/archives/red-cognition-test-artifacts.zip (prior session); no acquisition URL recorded",
    url=None, repository=None, commit=None, tag=None, filename="rebol-2.7.8 (prior-session lead)",
    path="artifacts/derived/from-previous-session/red-cognition-test-artifacts/downloaded/rebol-2.7.8",
    sha256=lead["sha256"], size=lead["size"], provenance_status="UNVERIFIED",
    license_status="MISSING", elf=lead["elf"],
    integrity_status="HASHED", execution="NOT_EXECUTED (ELF32; no i386 runtime on host)",
    notes="held as a lead only; original container zip preserved unchanged in artifacts/archives/")

# tree manifest files as METADATA artifacts
for fn in sorted(os.listdir(os.path.join(MAN, "trees"))):
    p = os.path.join(MAN, "trees", fn)
    add(project="RELATED", version=None, classification="METADATA",
        origin="deterministic file-level manifests generated from git trees (git ls-tree -r)",
        url=None, repository=None, commit=None, tag=None, filename=fn,
        path=os.path.relpath(p, ROOT), sha256=sha256_file(p), size=os.path.getsize(p),
        provenance_status="VERIFIED", integrity_status="HASHED")

# ------------------------------------------------------------------ manifest
manifest = {"generated_at": NOW, "generator": "acquisition-tools/05_finalize.py",
            "record_count": len(artifacts), "artifacts": artifacts}
with open(os.path.join(MAN, "artifacts.json"), "w") as f:
    json.dump(manifest, f, indent=2)

# sha256sums.txt regenerated at the end of 06_report.py (after reports exist,
# and excluding the ephemeral artifacts/derived/ extraction area)

# --------------------------------------------------------------- provenance
prov = {"generated_at": NOW, "graph": []}
def edge(rel_type, src, dst, evidence, status="ESTABLISHED"):
    prov["graph"].append({"relationship": rel_type, "source": src, "target": dst,
                          "evidence": evidence, "status": status})

edge("release->tag", "GitHub release red/red v0.6.6 (published 2025-03-19)",
     "tag v0.6.6", "github-discovery.json releases[].tag_name=v0.6.6; target_commitish=master")
edge("tag->commit", "tag v0.6.6", "commit 6942c7a021253150c3e3cf90428305892340db03",
     "git rev-parse v0.6.6^{commit} in blobless clone (git-collection.json)")
edge("commit->source-tree", "commit 6942c7a021253150c3e3cf90428305892340db03",
     "source tree (673 entries, red__v0.6.6.lsr)",
     "git ls-tree -r v0.6.6 deterministic manifest")
edge("source-tree->archive", "tree of commit 6942c7a0...",
     "artifacts/red/releases/red-0.6.6.tar.gz",
     "codeload.github.com/red/red/tar.gz/refs/tags/v0.6.6 (download pinned to tag->commit); version evidence encapper/version.r=0.6.6 inside")
edge("archive->binary", "red-0.6.6.tar.gz tree (commit 6942c7a0...)",
     "artifacts/red/tests/libRed-v0.6.6/libRed.dll",
     "git blob SHA-1 26e21ac96ad441a6888052538f8c468b50a67105 == git hash-object of downloaded bytes (verified)")
edge("upstream-tag->fork-tree", "red/red tag v0.6.4 (commit 755eb943...)",
     "workspace fork tree 742181a8...",
     "blob-SHA comparison: 248/530 upstream source files byte-identical; 253 differ; 334 fork-only; upstream rejects ref 742181a (not present)")
edge("upstream-repo->historical-repo", "rebol/rebol master (25033f89..., 2014-03-03)",
     "rebolsource/r3 HEAD (98cdfcd6...)",
     "git merge-base(rebolsource_r3 HEAD, rebol/rebol master) == 25033f89... -> rebol/rebol master is ancestor of rebolsource/r3 HEAD")
edge("historical-repo->continuation", "rebolsource/r3 (98cdfcd6...)",
     "metaeducation/ren-c HEAD (e31d5698d...)",
     "git merge-base(ren-c HEAD, rebolsource/r3 master) == d5d6908f... (2015-04-14); 10176 ren-c commits after fork point; GitHub metadata parent=rebolsource/r3")
edge("upstream-repo->fork", "rebol/rebol master (25033f89...)",
     "Oldes/Rebol3 HEAD (d5b237ce...)",
     "git merge-base(Oldes_Rebol3 HEAD, rebol/rebol master) == 25033f89... -> fork of official R3 master")
edge("license-text-identity", "rebol/rebol LICENSE (sha256 c95bae1d...)",
     "rebolsource/r3, rebol-test, Oldes/Rebol3 LICENSE files",
     "identical SHA-256 of LICENSE file content in all four archives (source-inspection.json)")
edge("license-text-divergence", "rebolsource/r3 (Apache-2.0)",
     "metaeducation/ren-c (LGPL-3.0)",
     "ren-c LICENSE sha256 1a45b1d0... = GNU LGPL v3 text; differs from lineage Apache-2.0")
edge("bootstrap-claim", "red/red README (v0.6.4 line 12; v0.6.6 line 24)",
     "Rebol2 interpreter required during bootstrap phase",
     "verbatim: 'except for a Rebol2 interpreter, required during the bootstrap phase' (v0.6.4) / 'required during the alpha stage' (v0.6.6); red.r + build/ present in trees")
edge("bootstrap-status", "Red bootstrap chain", "BOOTSTRAP_CLAIMED + BOOTSTRAP_SOURCE_PRESENT",
     "claim documented by upstream; build scripts present; NOTHING executed -> BOOTSTRAP_EXECUTED/REPRODUCED NOT established", status="PARTIAL")
edge("no-release-assets", "GitHub releases of red/red (v0.6.6, v0.6.4, v0.6.3)", "assets=0",
     "github-discovery.json: all three releases have empty assets arrays; binaries are distributed via official site (blocked from this environment)")
with open(os.path.join(PROV, "provenance.json"), "w") as f:
    json.dump(prov, f, indent=2)

# ------------------------------------------------------------ reconciliation
lic066 = next(x for x in insp["archives"] if x["archive"].endswith("red-0.6.6.tar.gz"))
lic064 = next(x for x in insp["archives"] if x["archive"].endswith("red-0.6.4.tar.gz"))
recon = {"generated_at": NOW, "tables": [
 {"id": "R1", "artifact": "Red v0.6.6 (latest release)",
  "rows": [
   ["Version (release name)", "0.6.6: Memory Management Improvements", "tag v0.6.6", "MATCH"],
   ["Version (embedded)", "encapper/version.r = 0.6.6 (in tarball)", "release name 0.6.6", "MATCH"],
   ["Commit", "release target_commitish=master", "tag v0.6.6 -> 6942c7a0...", "MATCH (tag is on master line)"],
   ["Source", "github.com/red/red (official)", "codeload archive of tag", "MATCH"],
   ["License", "repo metadata BSL-1.0", "BSD-3-License.txt + BSL-License.txt in tree", "PARTIAL (both files present; SPDX metadata captures BSL only)"],
  ]},
 {"id": "R2", "artifact": "Red v0.6.4 vs workspace fork",
  "rows": [
   ["Version claim", "upstream version.r = 0.6.4", "fork version.r = 0.6.4", "MATCH"],
   ["Tree content", "upstream 530 source files", "248 byte-identical / 253 differing / 334 fork-only", "CONFLICT (fork is NOT byte-identical to v0.6.4; it is a modified subset)"],
   ["Commit", "755eb943... (upstream v0.6.4)", "742181a8... (fork-only; rejected by upstream)", "CONFLICT (fork commit not in upstream history)"],
   ["License", "BSD-3 (c) 2011 Nenad Rakocevic", "same files carried in fork", "MATCH"],
  ]},
 {"id": "R3", "artifact": "Red license text across versions",
  "rows": [
   ["BSD-3 text v0.6.4", "sha256 09b59353... (c) 2011 Nenad Rakocevic", "-", "NOTED"],
   ["BSD-3 text v0.6.6", "sha256 e64d2571... (c) 2011-2019 Red Foundation", "-", "NOTED (text changed between versions; per-artifact license is CONFIRMED by its own tree)"],
  ]},
 {"id": "R4", "artifact": "R3 lineage versions",
  "rows": [
   ["rebol/rebol (official R3)", "src/boot/version.r = 2.101.0.3.1", "no tags, no releases on GitHub", "NOTED"],
   ["rebolsource/r3", "src/boot/version.r = 2.101.0.3.1", "same as rebol/rebol", "MATCH"],
   ["metaeducation/ren-c", "src/specs/version.r = 2.102.0.0.0", "no releases; atronix tags only", "NOTED"],
   ["Oldes/Rebol3", "internal .version = 3.22.53.5.4.3.1", "GitHub release/tag 3.22.1", "CONFLICT (different version schemes: internal 3.22.53.x vs tag 3.22.1 - recorded, not resolved)"],
  ]},
 {"id": "R5", "artifact": "R3 lineage licenses",
  "rows": [
   ["LICENSE text hash", "rebol/rebol / rebolsource/r3 / rebol-test / Oldes-Rebol3 all sha256 c95bae1d... (Apache-2.0)", "ren-c sha256 1a45b1d0... (LGPL-3.0)", "CONFLICT (ren-c relicensed vs lineage; recorded with evidence)"],
   ["rebolsource/rebol-syntax", "no LICENSE file in repo", "-", "UNCLEAR"],
  ]},
 {"id": "R6", "artifact": "REBOL 2.7.8 official distribution",
  "rows": [
   ["Version claims", "rebol.com download pages (via search-index snapshot): Core 2.7.8.3.1 / .4.2 / .4.3 / .4.10, View 2.7.8.x", "direct fetch from rebol.com: BLOCKED (TLS)", "UNVERIFIED (second-hand page content only; acquisition BLOCKED)"],
   ["Binary availability", "rebol.com/pub/platforms/... (URLs from page snippet)", "all attempts TLS-blocked from sandbox", "BLOCKED"],
  ]},
 {"id": "R7", "artifact": "Red binary distribution",
  "rows": [
   ["GitHub release assets", "v0.6.6/v0.6.4/v0.6.3 assets=0", "official binaries hosted on static.red-lang.org", "CONFLICT (expectation: release binaries on GitHub; reality: off-GitHub hosting)"],
   ["static.red-lang.org", "official download host", "TLS-blocked from sandbox", "BLOCKED"],
  ]},
]}
with open(os.path.join(PROV, "reconciliation.json"), "w") as f:
    json.dump(recon, f, indent=2)

# ----------------------------------------------------------- blocked attempts
blocked = {"generated_at": NOW, "environment": "sandbox egress allowlist: github.com, api.github.com, codeload.github.com only",
 "attempts": [
  {"url": "http://www.rebol.com/", "purpose": "official REBOL site reachability", "result": "NETWORK_BLOCKED", "detail": "curl exit 52 empty reply (http)"},
  {"url": "http://www.rebol.com/download-core.html", "purpose": "official REBOL/Core 2.7.8 download page", "result": "NETWORK_BLOCKED", "detail": "http_code 000 (direct + with UA retry)"},
  {"url": "https://www.rebol.com/download-core.html", "purpose": "official REBOL/Core 2.7.8 download page", "result": "NETWORK_BLOCKED", "detail": "curl exit 35 SSL_ERROR_SYSCALL"},
  {"url": "https://www.rebol.com/pub/platforms/rebol-core-278-4-10.tar.gz", "purpose": "official REBOL 2.7.8 Linux x86-64 binary", "result": "NETWORK_BLOCKED", "detail": "curl exit 35 SSL_ERROR_SYSCALL (evidence log: logs/execution/blocked-rebol-com.log)"},
  {"url": "https://archive.org/wayback/available?url=rebol.com/pub/platforms/rebol-core-278-4-3.tar.gz", "purpose": "archival copy of official REBOL 2.7.8 binary", "result": "NETWORK_BLOCKED", "detail": "curl exit 35"},
  {"url": "https://web.archive.org/web/2020id_/http://www.rebol.com/pub/platforms/rebol-core-278-4-3.tar.gz", "purpose": "archival copy of official REBOL 2.7.8 binary", "result": "NETWORK_BLOCKED", "detail": "curl exit 35"},
  {"url": "https://static.red-lang.org/dl/auto/linux/red-latest", "purpose": "official Red binary (automated build)", "result": "NETWORK_BLOCKED", "detail": "curl exit 35 SSL_ERROR_SYSCALL (evidence log: logs/execution/blocked-static-red-lang-org.log)"},
  {"url": "https://www.red-lang.org/p/download.html", "purpose": "official Red download page", "result": "NETWORK_BLOCKED", "detail": "curl exit 35"},
  {"url": "https://github.com/Oldes/Rebol3/releases/download/3.22.1/rebol3-core-linux-x64.gz", "purpose": "third-party prebuilt Rebol 3 binary (GitHub release asset)", "result": "NETWORK_BLOCKED", "detail": "github.com -> 302 -> release-assets.githubusercontent.com TLS blocked (curl exit 35; evidence log: logs/execution/blocked-github-release-assets-rebol3.log)"},
  {"url": "https://raw.githubusercontent.com/red/red/master/version.r", "purpose": "raw file access test", "result": "NETWORK_BLOCKED", "detail": "curl exit 35"},
  {"url": "https://media.githubusercontent.com/", "purpose": "LFS/asset host reachability", "result": "NETWORK_BLOCKED", "detail": "curl exit 35"},
  {"url": "https://objects.githubusercontent.com/", "purpose": "release asset host reachability", "result": "NETWORK_BLOCKED", "detail": "curl exit 35"},
  {"url": "https://release-assets.githubusercontent.com/", "purpose": "release asset host reachability", "result": "NETWORK_BLOCKED", "detail": "curl exit 35"},
  {"url": "https://rebolsource.net", "purpose": "historical Ren-C/R3 build host", "result": "NETWORK_BLOCKED", "detail": "curl exit 35"},
  {"url": "https://www.rebol.tech", "purpose": "Oldes' Rebol site", "result": "NETWORK_BLOCKED", "detail": "curl exit 35"},
  {"url": "https://deb.debian.org", "purpose": "distro package mirror (rebol package)", "result": "NETWORK_BLOCKED", "detail": "curl exit 35"},
  {"url": "https://snapshot.debian.org", "purpose": "distro archive (rebol package)", "result": "NETWORK_BLOCKED", "detail": "curl exit 35"},
  {"url": "https://gitlab.com", "purpose": "alternative host check", "result": "NETWORK_BLOCKED", "detail": "curl exit 35"},
  {"url": "https://sourceforge.net", "purpose": "alternative host check", "result": "NETWORK_BLOCKED", "detail": "curl exit 35"},
  {"url": "https://github.com/red/red/releases (assets)", "purpose": "Red release binaries", "result": "NOT_FOUND", "detail": "releases exist but all have 0 assets (not a network failure)"},
  {"url": "https://github.com/Oldes/Rebol-legacy", "purpose": "Rebol 2 maintained fork (lead)", "result": "NOT_FOUND", "detail": "HTTP 404; Oldes' current fork is Oldes/Rebol3"},
 ]}
with open(os.path.join(LOGS, "blocked-attempts.json"), "w") as f:
    json.dump(blocked, f, indent=2)

# --------------------------------------------------------- execution evidence
exe = {"generated_at": NOW,
 "summary": "NO artifact was executed in this session. Execution claims made: NONE.",
 "evidence": [
  {"artifact": "rebol-2.7.8 (prior-session lead, sha256 1c902e0f...)", "action": "NOT_EXECUTED",
   "reason": "ELF32 little-endian binary; host is x86_64 without i386 loader; provenance UNKNOWN so not trusted for execution",
   "elf_header_evidence": "7f 45 4c 46 class=1(ELF32) endian=1(LE), recorded in source-inspection.json"},
  {"artifact": "rebol3-core-linux-x64.gz (Oldes/Rebol3 v3.22.1 release asset)", "action": "NOT_ACQUIRED",
   "reason": "download blocked at release-assets.githubusercontent.com (TLS)", "log": "logs/execution/blocked-github-release-assets-rebol3.log"},
  {"artifact": "Red linux binary (static.red-lang.org)", "action": "NOT_ACQUIRED",
   "reason": "host TLS-blocked", "log": "logs/execution/blocked-static-red-lang-org.log"},
  {"artifact": "red/red test fixtures (libRed.dll, libstructlib.so, structlib.dll)", "action": "NOT_EXECUTED",
   "reason": "test-support libraries, not interpreters; execution out of scope for acquisition"},
  {"artifact": "bootstrap reproduction (Red from source via Rebol 2.7.8)", "action": "NOT_ATTEMPTED",
   "reason": "no Rebol interpreter obtainable in this environment -> reproducibility NOT_REPRODUCED (no attempt made)"}]}
with open(os.path.join(EXE, "execution-evidence.json"), "w") as f:
    json.dump(exe, f, indent=2)

# append web-search queries used by the agent (search engine, not GitHub API)
webq = [
 ["web-search", "REBOL 2.7.8 download Linux binary rebol.com archive.org"],
 ["web-search", "metaeducation ren-c Rebol 3 github releases binaries"],
 ["github-search", "search/repositories q='rebol2' (per_page=6)"],
 ["github-search", "search/repositories q='rebol 2 source' (per_page=6)"],
 ["github-api", "GET /users/Oldes/repos?per_page=100 (locate Rebol-legacy successor)"],
 ["github-api", "GET /orgs/rebolsource/repos?per_page=100"],
 ["github-api", "GET /repos/Oldes/Rebol3/releases?per_page=5"],
 ["github-api", "GET /repos/red/red/contents/version.r?ref=v0.6.4"],
 ["connectivity-probe", "TLS reachability probes: rebol.com, archive.org, web.archive.org, static.red-lang.org, www.red-lang.org, rebolsource.net, www.rebol.tech, deb.debian.org, snapshot.debian.org, gitlab.com, sourceforge.net, raw|media|objects|release-assets.githubusercontent.com"],
]
with open(os.path.join(LOGS, "search-queries.log"), "a") as f:
    for kind, q in webq:
        f.write(json.dumps({"ts": NOW, "tool": "05_finalize.py (recorded retrospectively)",
                            "kind": kind, "query": q, "status": "ATTEMPTED"}) + "\n")

print(f"artifacts={len(artifacts)} provenance_edges={len(prov['graph'])} recon_tables={len(recon['tables'])} blocked={len(blocked['attempts'])}")
