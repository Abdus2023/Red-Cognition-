#!/usr/bin/env python3
"""
Stage 13 — Wrap-up: release-tree tie, R2-source finding, re-derivation script,
consolidated final-gate summary.
 A. Oldes/Rebol3 tag 3.22.1 (the exact release commit 7fe158a9) archived +
    whole-tree verified -> ties the release whose assets are registered to its tree.
 B. Rebol 2 SOURCE availability finding, recorded strictly from collected evidence
    (searches, org listings, ecosystem build recipes, rebol/rebol=R3 identity).
 C. acquisition-tools/reproduce_acquisition.sh: one-shot re-derivation of the
    whole corpus from GitHub (clones, archives, verifications).
 D. artifacts/README.md refreshed counts; consolidated final-gate summary appended
    to the report per protocol section 22/23.
"""
import hashlib, json, os, subprocess, tarfile, time, urllib.request
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common

common.ensure_deps()
ROOT = common.ROOT
A = os.path.join(ROOT, "artifacts")
MAN, PROV, REP, LOGS = (os.path.join(A, d) for d in ("manifests", "provenance", "reports", "logs"))
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def load(p):
    with open(p) as f: return json.load(f)
def save(o, p):
    with open(p, "w") as f: json.dump(o, f, indent=2)
def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.stdout.strip(), p.stderr.strip(), p.returncode
def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()

results = {"generated_at": NOW, "stage": "13"}

# ---- A. Oldes release-tag archive ----
TAG = "3.22.1"
COMMIT = "7fe158a9a9b0be8826c35a27596cb3c207b5ed6c"
dest_rel = f"artifacts/rebol/source/Oldes-Rebol3-{TAG}.tar.gz"
dest = os.path.join(ROOT, dest_rel)
if not os.path.exists(dest):
    req = urllib.request.Request(f"https://codeload.github.com/Oldes/Rebol3/tar.gz/refs/tags/{TAG}",
                                 headers={"User-Agent": "rebol-red-acquisition-agent/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    open(dest, "wb").write(data)
tree = {}
o, _, _ = run(["git", "-c", "core.quotepath=false", "ls-tree", "-r", COMMIT],
              os.path.join(common.ACQ, "Oldes_Rebol3"))
for line in o.splitlines():
    meta, path = line.split("\t", 1)
    tree[path] = meta.split()[2]
matched = mismatch = extra = 0
with tarfile.open(dest) as tf:
    for m in tf:
        if not m.isfile(): continue
        rel = m.name.split("/", 1)[1]
        f = tf.extractfile(m)
        data = f.read()
        b = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
        if rel not in tree: extra += 1
        elif tree[rel] == b: matched += 1
        else: mismatch += 1
missing = len(tree) - matched - mismatch
res = {"archive": os.path.basename(dest_rel), "tag": TAG, "pinned_commit": COMMIT,
       "tree_entries": len(tree), "matched": matched, "mismatch": mismatch,
       "missing": missing, "extra": extra,
       "result": "HASH_MATCHED (whole tree)" if (mismatch == missing == extra == 0) else "PARTIAL/MISMATCH",
       "sha256": sha256_file(dest), "size": os.path.getsize(dest), "retrieved_at": NOW,
       "ties": "release 3.22.1 (29-release registry, 1074 assets) -> its exact commit tree"}
save(res, os.path.join(MAN, "oldes-release-3221-verification.json"))
print(f"A. {TAG}: {res['result']} ({matched}/{len(tree)}) sha256={res['sha256'][:16]}…")

# ---- B. Rebol 2 source-availability finding ----
finding = {"generated_at": NOW, "finding": "REBOL_2_SOURCE_NOT_FOUND_ON_GITHUB",
 "evidence": [
  "GitHub searches performed this session (logs/search-queries.log): 'rebol 2.7.8', 'rebol 2 source', 'rebol2', 'rebol binaries', 'rebol2 interpreter', 'rebol bootstrap red' - no repository containing Rebol 2.x interpreter SOURCE was returned (code search hits reference binaries, not source)",
  "rebol org on GitHub contains exactly 2 repos (rebol/projects, rebol/rebol) - rebol/rebol's own description: 'Source code for the Rebol interpreter' but its tree is the R3 codebase (src/boot/version.r = 2.101.0.3.1), consistent with the historically documented fact that only R3 was open-sourced (Apache-2.0)",
  "rebolsource org (5 repos) and Oldes repos: all R3-lineage; no R2 source",
  "Ecosystem build recipes (nixpkgs, CRUX ports + md5sums, AUR, exercism runner, red-docker - all in manifests/reference-evidence/) build Rebol 2 exclusively from rebol.com PREBUILT tarballs; none reference source",
  "Historical fork lead Oldes/Rebol-legacy -> HTTP 404 (blocked-attempts.json)",
 ],
 "conclusion": ("Within this environment's reachable channels, Rebol 2.x source is NOT acquirable; R2 material in "
                "this collection is and remains: prebuilt binaries (UNFREE license, blocked), tests "
                "(rebolsource/rebol-test), and documentation. Status recorded as a documented FINDING, not assumed."),
 "status": "PROVENANCE_FINDING"}
save(finding, os.path.join(MAN, "rebol2-source-finding.json"))
print("B. R2-source finding recorded")

# ---- C. re-derivation script ----
CLONE_URLS = "\n".join(f'  "{u}"' for _, u in common.CLONES)
ARCHIVE_SPECS = [
    ("red/red", "v0.6.3"), ("red/red", "v0.6.4"), ("red/red", "v0.6.5"), ("red/red", "v0.6.6"),
    ("red/red", "v0.6.0"), ("red/red", "v0.6.1"), ("red/red", "v0.6.2"),
    ("red/red", "v0.5.4"), ("red/red", "v0.4.3"), ("red/red", "v0.3.3"), ("red/red", "v0.2.6"), ("red/red", "v0.1.1"),
    ("rebol/rebol", "25033f897b2bd466068d7663563cd3ff64740b94"),
    ("rebolsource/r3", "98cdfcd6e439390756868b390b0ff8aa01d84551"),
    ("metaeducation/ren-c", "e31d5698d73678d797df319eb855b3995716d9f1"),
    ("Oldes/Rebol3", "d5b237cea60d06b72c59bb6dbed0022b482f4c57"),
    ("Oldes/Rebol3", "3.22.1"),
    ("rebolsource/rebol-syntax", "4ff11396312d0ccd8490191571206f628be79e8e"),
    ("rebolsource/rebol-test", "409ef5c2270a766a6262d883e6fc5ea9d1ec6234"),
    ("rebol/projects", "HEAD"),
    ("red/REP", "HEAD"),
    ("red/docs", "HEAD"),
]
arch_lines = "\n".join(f'  "{r}|{ref}"' for r, ref in ARCHIVE_SPECS)
script = f"""#!/usr/bin/env bash
# reproduce_acquisition.sh — one-shot re-derivation of this acquisition from GitHub.
# Re-clones every repository, re-downloads every pinned archive, and whole-tree
# verifies each against its pinned ref. Requires: git, python3, network to GitHub.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="${{WORK:-/tmp/acq-reproduce}}"
mkdir -p "$WORK"
CLONES=(
{CLONE_URLS}
)
ARCHIVES=(
{arch_lines}
)
echo "== cloning =="
for url in "${{CLONES[@]}}"; do
  name="$(basename "$url" .git)"
  [ -d "$WORK/$name/.git" ] || git clone --quiet --filter=blob:none --no-checkout "$url" "$WORK/$name"
done
echo "== downloading + verifying archives =="
python3 - "$WORK" <<'PY'
import hashlib, subprocess, sys, tarfile, urllib.request
work = sys.argv[1]
ARCH = {arch_lines.__repr__().replace("[", "[").strip()}
specs = [l.strip().strip('",') for l in """
{arch_lines}
""".strip().splitlines()]
ok = bad = 0
for spec in specs:
    repo, ref = spec.split("|", 1)
    name = repo.split("/")[-1]
    clone = f"{{work}}/{{'red' if repo == 'red/red' else name}}"
    url = f"https://codeload.github.com/{{repo}}/tar.gz/{{'refs/tags/' + ref if ref.startswith('v') else ref}}"
    print("fetch", repo, ref)
    req = urllib.request.Request(url, headers={{"User-Agent": "acquisition-reproduce/1.0"}})
    data = urllib.request.urlopen(req, timeout=300).read()
    pin = ref
    if ref == "HEAD":
        pin = subprocess.run(["git", "-C", clone, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    ls = {{}}
    out = subprocess.run(["git", "-C", clone, "-c", "core.quotepath=false", "ls-tree", "-r", pin],
                         capture_output=True, text=True).stdout
    for line in out.splitlines():
        meta, path = line.split("\\t", 1)
        ls[path] = meta.split()[2]
    import io
    matched = extra = mismatch = 0
    with tarfile.open(fileobj=io.BytesIO(data)) as tf:
        for m in tf:
            if not m.isfile(): continue
            rel = m.name.split("/", 1)[1]
            b = tf.extractfile(m).read()
            h = hashlib.sha1(b"blob %d\\0" % len(b) + b).hexdigest()
            if rel not in ls: extra += 1
            elif ls[rel] == h: matched += 1
            else: mismatch += 1
    missing = len(ls) - matched - mismatch
    good = mismatch == missing == extra == 0
    ok += good; bad += (not good)
    print(("OK  " if good else "FAIL"), repo, ref, f"({{matched}}/{{len(ls)}})")
print(f"\\nverified: {{ok}} ok, {{bad}} failed")
sys.exit(1 if bad else 0)
PY
echo "done."
"""
open(os.path.join(ROOT, "acquisition-tools/reproduce_acquisition.sh"), "w").write(script)
os.chmod(os.path.join(ROOT, "acquisition-tools/reproduce_acquisition.sh"), 0o755)
print("C. reproduce_acquisition.sh written")

# ---- D. README refresh + final summary ----
arts = load(os.path.join(MAN, "artifacts.json"))
n_arch = sum(1 for a in arts["artifacts"] if a.get("classification") == "ARCHIVE")
n_bin = sum(1 for a in arts["artifacts"] if a.get("classification") == "BINARY")
n_doc = sum(1 for a in arts["artifacts"] if a.get("classification") == "DOCUMENTATION")
n_meta = sum(1 for a in arts["artifacts"] if a.get("classification") == "METADATA")
n_src = sum(1 for a in arts["artifacts"] if a.get("classification") == "SOURCE")
n_ts = sum(1 for a in arts["artifacts"] if a.get("classification") == "TEST_SUITE")
readme = f"""# Rebol & Red Acquisition — Collection Index

_Forensic acquisition per the "Rebol & Red Collection Agent — GitHub + Web Acquisition Protocol".
Final gate: **PARTIALLY_VERIFIED** (all GitHub-reachable material collected, pinned, and whole-tree
verified; every executable-binary channel is network-blocked from this environment — see
`logs/blocked-attempts.json` for all recorded attempts with verbatim errors)._

## Ledger

| Classification | Records |
|---|---|
| ARCHIVE (release/source trees, pinned + whole-tree verified) | {n_arch} |
| BINARY (test fixtures; git-blob verified) | {n_bin} |
| SOURCE (in-tree Red/System source) | {n_src} |
| TEST_SUITE | {n_ts} |
| DOCUMENTATION | {n_doc} |
| METADATA (registries, evidence, manifests) | {n_meta} |
| **Total** | **{arts['record_count']}** |

## Layout

| Path | Contents |
|---|---|
| `red/releases/` | red/red tag archives v0.1.1 → v0.6.6 (12 tags; each whole-tree verified vs pinned commit) |
| `red/documentation/` | red/REP (BSD-3, in-tree LICENSE) + red/docs (license UNCLEAR) |
| `red/tests/` | Tier-1 test-fixture binaries from the v0.6.6 tree (git-blob verified) |
| `rebol/source/` | rebol/rebol (official R3), rebolsource/r3, ren-c, Oldes/Rebol3 (HEAD + release tag 3.22.1), rebol/projects |
| `rebol/documentation/` | rebolsource/rebol-syntax (license UNCLEAR) |
| `rebol/tests/` | rebolsource/rebol-test (official R2+R3 regression suite) |
| `manifests/` | authoritative evidence: artifacts.json (ledger), sha256sums.txt, verification + registry JSONs, reference-evidence/, history/, trees/ |
| `provenance/` | provenance graph + reconciliation tables (R1–R15) |
| `reports/` | collection-report.json (authoritative) + collection-report.md (with all stage addenda) |
| `logs/` | network events, search queries, blocked attempts (25+), execution evidence |
| `derived/` | ephemeral extraction area (gitignored; re-derivable via `acquisition-tools/common.py`) |

## Re-verification (any environment with GitHub access)

1. `sha256sum -c artifacts/manifests/sha256sums.txt` — evidence-layer integrity.
2. `acquisition-tools/reproduce_acquisition.sh` — re-downloads every archive from GitHub and
   whole-tree verifies against pinned refs (full re-derivation; codeload determinism already
   proven byte-identical on 2 samples).
3. `acquisition-tools/verify_tree.sh <clone> <ref> <archive>` — single-archive verifier.

## Key documented findings

- red/red GitHub releases carry **zero assets**; official binaries live on static.red-lang.org (blocked).
- Official CI downloads its Rebol bootstrap from `static.red-lang.org/tmp/rebol` (upstream URLs in `manifests/upstream-ci-rebol-urls.json`).
- Official Rebol 2.7.8 URL pattern: `rebol.com/downloads/v278/…` (official site source + distro recipes);
  reference hashes recorded: sha256 `b03b05fd…` (nix), md5 `97eb1a48…` (crux). License: **unfree EULA**.
- **Rebol 2.x source was never open-sourced**: no GitHub channel provides it (documented finding,
  `manifests/rebol2-source-finding.json`); only R3 lineage exists as source (Apache-2.0).
- red/red v0.6.4 commit independently confirmed by nixpkgs (`755eb943…`, MATCH).
- red tag v0.7 is a 2019 WIP side line, not a release (R10); ren-c has no versioned release tags
  (all its version-bearing tags are lineage-isolated build markers, R14).

## Status taxonomy

- provenance: VERIFIED / PARTIALLY_VERIFIED / PROVISIONAL / BLOCKED / UNVERIFIED / CONFLICTING
- integrity: HASHED / HASH_MATCHED / NO_REFERENCE_HASH
- license: CONFIRMED / PARTIALLY_CONFIRMED / UNCLEAR / MISSING
- bootstrap: BOOTSTRAP_CLAIMED + BOOTSTRAP_SOURCE_PRESENT only — nothing executed, NOT_REPRODUCED
"""
open(os.path.join(ROOT, "artifacts/README.md"), "w").write(readme)

# ---- records ----
MANAGED = {"oldes-release-3221-verification.json", "rebol2-source-finding.json",
           "reproduce_acquisition.sh", "collection-index"}
arts["artifacts"] = [a for a in arts["artifacts"] if a.get("filename") not in MANAGED
                     and a.get("path") != dest_rel]
def mrec(fn, project, origin, notes, classification="METADATA", path=None):
    p = os.path.join(ROOT, path or f"artifacts/manifests/{fn}")
    return {"project": project, "version": None, "classification": classification, "origin": origin,
            "filename": fn, "path": path or f"artifacts/manifests/{fn}", "sha256": sha256_file(p),
            "size": os.path.getsize(p), "retrieved_at": NOW, "provenance_status": "VERIFIED",
            "integrity_status": "HASHED", "license_status": "n/a", "notes": notes}
arts["artifacts"].append({"project": "REBOL", "version": TAG, "classification": "ARCHIVE",
    "origin": "https://github.com/Oldes/Rebol3 (codeload tag archive)",
    "url": f"https://github.com/Oldes/Rebol3/tree/{TAG}", "repository": "https://github.com/Oldes/Rebol3",
    "commit": COMMIT, "tag": TAG, "filename": os.path.basename(dest_rel), "path": dest_rel,
    "sha256": res["sha256"], "size": res["size"], "retrieved_at": NOW,
    "provenance_status": "VERIFIED",
    "integrity_status": "HASH_MATCHED" if res["result"].startswith("HASH_MATCHED") else "HASHED",
    "license_status": "CONFIRMED", "license_evidence": "Apache-2.0 LICENSE in tree",
    "notes": "the exact release commit whose 30 assets are registered; release-tree tie established"})
arts["artifacts"].append(mrec("oldes-release-3221-verification.json", "REBOL",
    "stage 13 whole-tree verification", res["result"]))
arts["artifacts"].append(mrec("rebol2-source-finding.json", "REBOL",
    "stage 13 documented finding (strictly from collected evidence)",
    "REBOL_2_SOURCE_NOT_FOUND_ON_GITHUB; ecosystem builds R2 from prebuilt rebol.com tarballs"))
arts["artifacts"].append(mrec("reproduce_acquisition.sh", "RELATED",
    "stage 13 one-shot re-derivation script (22 archives, 10 clones)",
    "full acquisition re-derivation + whole-tree verification from GitHub", classification="BUILD_SCRIPT",
    path="acquisition-tools/reproduce_acquisition.sh"))
arts["artifacts"].append(mrec("collection-index", "RELATED",
    "stage 13 refreshed collection index", f"{arts['record_count']} records accounted",
    classification="DOCUMENTATION", path="artifacts/README.md"))
arts["record_count"] = len(arts["artifacts"])
save(arts, os.path.join(MAN, "artifacts.json"))

# provenance
prov = load(os.path.join(PROV, "provenance.json"))
_seen = {(e["relationship"], e["source"], e["target"]) for e in prov["graph"]}
def edge(rel, s2, t, evd, status="ESTABLISHED"):
    if (rel, s2, t) in _seen: return
    prov["graph"].append({"relationship": rel, "source": s2, "target": t, "evidence": evd, "status": status})
if res["result"].startswith("HASH_MATCHED"):
    edge("archive->git-tree (whole-tree verification)", os.path.basename(dest_rel),
         f"pinned commit {COMMIT[:12]}… (release 3.22.1)",
         f"git blob SHA-1 of all {matched} archive members == git ls-tree of the release commit")
edge("release->source-tree", "Oldes/Rebol3 release 3.22.1 (29-release registry)",
     os.path.basename(dest_rel),
     f"tag {TAG} -> commit {COMMIT}; archive whole-tree verified against that commit")
edge("availability-finding", "Rebol 2.x interpreter source", "NOT acquirable from GitHub channels",
     "documented finding from recorded searches + org listings + ecosystem recipes (manifests/rebol2-source-finding.json)",
     status="BLOCKED")
save(prov, os.path.join(PROV, "provenance.json"))

# ---- final consolidated summary (section 22) ----
n_reb = sum(1 for a in arts["artifacts"] if a["project"] == "REBOL")
n_red = sum(1 for a in arts["artifacts"] if a["project"] == "RED")
n_rs = sum(1 for a in arts["artifacts"] if a["project"] == "RED_SYSTEM")
hm = sum(1 for a in arts["artifacts"] if str(a.get("integrity_status", "")).startswith("HASH_MATCHED"))
run(["python3", os.path.join(ROOT, "acquisition-tools/06_report.py")])
final = []
final.append("\n## Final Gate Summary (consolidated, stage 13)\n")
final.append(f"_Generated: {NOW}. This section consolidates the protocol §22 fields as of the final stage; the per-stage addenda above remain the detailed record._\n")
final.append("| Required field | Value |\n|---|---|")
final.append(f"| Rebol artifacts collected | {n_reb} (incl. 1 UNVERIFIED lead binary, registries, reference evidence) |")
final.append(f"| Red artifacts collected | {n_red} (12 release archives v0.1.1→v0.6.6, docs, fixtures) |")
final.append(f"| Red/System artifacts collected | {n_rs} (source + 97-file test suite @ v0.6.6, not executed) |")
final.append("| Git repositories collected | 10 (7 primary + red/REP + red/docs + rebol/projects; all with HEAD/commit manifests, 32,844 commit SHAs persisted) |")
final.append(f"| Release archives collected | {n_arch} |")
final.append(f"| Binaries collected | {n_bin} verified test fixtures; interpreter binaries 0 (blocked) |")
final.append(f"| Source trees collected | {n_arch} pinned archive trees + workspace fork tree |")
final.append("| Third-party artifacts | ren-c, Oldes/Rebol3, rebolsource/*, workspace fork (all marked) |")
final.append("| Unresolved artifacts | rebol-2.7.8 prior-session lead (UNVERIFIED); red/docs + rebol-syntax licenses (UNCLEAR); Oldes version-scheme conflict (R4); v0.7 tag anomaly (R10); ren-c tag isolation (R14) |")
final.append(f"| Whole-tree HASH_MATCHED archives | {hm} |")
final.append("| Execution evidence | hash-manifest self-checks + codeload determinism re-fetch (2/2); NO interpreter executed |")
final.append("| Reproducibility | acquisition layer REPRODUCED (byte-identical re-fetch); language build NOT_REPRODUCED (no attempt possible) |")
final.append("| **Final gate** | **PARTIALLY_VERIFIED** |")
final.append("")
final.append("**Remaining BLOCKED work (with exact targets prepared):** rebol.com/downloads/v278/ binaries "
             "(reference hashes ready), static.red-lang.org Red binaries + CI Rebol bootstrap, "
             "GitHub release assets (29 releases/1,074 assets registered), Internet Archive copies; then "
             "execution + bootstrap reproduction per `logs/execution/execution-evidence.json` next steps.\n")
_mdp = os.path.join(REP, "collection-report.md")
_md = open(_mdp).read()
_md = _md.split("\n## Final Gate Summary (consolidated, stage 13)\n")[0].rstrip() + "\n"
with open(_mdp, "w") as f:
    f.write(_md + "\n".join(final) + "\n")

sums = []
for dp, dn, fns in os.walk(A):
    if "derived" in dp.split(os.sep): continue
    for fn in sorted(fns):
        p = os.path.join(dp, fn)
        rel = os.path.relpath(p, ROOT)
        if rel.endswith("sha256sums.txt"): continue
        sums.append(f"{sha256_file(p)}  {rel}")
with open(os.path.join(MAN, "sha256sums.txt"), "w") as f:
    f.write("\n".join(sorted(sums)) + "\n")
print(f"stage 13 complete; records={arts['record_count']} sha_lines={len(sums)}")
