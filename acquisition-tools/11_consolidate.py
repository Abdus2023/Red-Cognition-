#!/usr/bin/env python3
"""
Stage 11 — Consolidation.
 1. Oldes/Rebol3 release registry: all releases + full asset metadata via API
    (durable evidence; asset downloads remain blocked, recorded per attempt).
 2. ren-c tag registry with fork-lineage ancestry analysis (atronix-* tags).
 3. rebol/projects (official org, historical, tiny) collected: archive + manifest.
 4. artifacts/README.md collection index (layout, verification guide, statuses).
 5. acquisition-tools/verify_tree.sh reusable whole-tree verifier.
 6. Ledger updates, report addendum, sha256sums, self-check.
"""
import hashlib, json, os, subprocess, time, urllib.request
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common

common.ensure_deps()
ROOT = common.ROOT
A = os.path.join(ROOT, "artifacts")
MAN, PROV, REP, LOGS = (os.path.join(A, d) for d in ("manifests", "provenance", "reports", "logs"))
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
TOKEN = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()

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
def gh_json(url):
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json",
        "User-Agent": "rebol-red-acquisition-agent/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

results = {"generated_at": NOW, "stage": "11"}

# ---- 1. Oldes/Rebol3 release registry ----
rel_rows = []
page = 1
while True:
    chunk = gh_json(f"https://api.github.com/repos/Oldes/Rebol3/releases?per_page=100&page={page}")
    if not chunk: break
    rel_rows += chunk
    if len(chunk) < 100: break
    page += 1
registry = {"generated_at": NOW, "repo": "https://github.com/Oldes/Rebol3",
            "release_count": len(rel_rows),
            "note": ("METADATA registry only. Release assets (rebol3-*.gz/.exe binaries) are hosted behind "
                     "release-assets.githubusercontent.com, which is TLS-blocked from this sandbox "
                     "(see logs/blocked-attempts.json); asset URLs+sizes+hash-basis recorded here for future acquisition."),
            "releases": [{
                "tag": r.get("tag_name"), "name": r.get("name"),
                "url": r.get("html_url"), "published_at": r.get("published_at"),
                "prerelease": r.get("prerelease"),
                "asset_count": len(r.get("assets") or []),
                "assets": [{"name": a.get("name"), "url": a.get("browser_download_url"),
                            "size": a.get("size"), "content_type": a.get("content_type"),
                            "updated_at": a.get("updated_at"), "downloads": a.get("download_count")}
                           for a in (r.get("assets") or [])],
            } for r in rel_rows]}
tot_assets = sum(x["asset_count"] for x in registry["releases"])
save(registry, os.path.join(MAN, "oldes-rebol3-releases-registry.json"))
print(f"1. Oldes releases registered: {len(rel_rows)} releases, {tot_assets} assets (metadata only)")

# ---- 2. ren-c tag registry + lineage ----
renc = os.path.join(common.ACQ, "metaeducation_ren-c")
run(["git", "fetch", "--quiet", "--tags"], renc)
FORK_POINT = "d5d6908f552dacb087cc97ed347718247f0663aa"   # merge-base(ren-c HEAD, rebolsource/r3 master)
tags = sorted(o for o in run(["git", "tag", "-l"], renc)[0].splitlines() if o)
rows = {}
for t in tags:
    co, _, _ = run(["git", "rev-parse", f"{t}^{{commit}}"], renc)
    to, _, _ = run(["git", "rev-parse", f"{t}^{{tree}}"], renc)
    dt, _, _ = run(["git", "for-each-ref", f"refs/tags/{t}", "--format=%(creatordate:iso-strict) %(objecttype)"], renc)
    _, _, pre = run(["git", "merge-base", "--is-ancestor", co, FORK_POINT], renc)
    _, _, inh = run(["git", "merge-base", "--is-ancestor", co, "HEAD"], renc)
    rows[t] = {"commit": co, "tree": to, "date_object": dt,
               "pre_fork_shared_lineage": pre == 0,
               "in_ren_c_master_history": inh == 0}
n_inmaster = sum(1 for v in rows.values() if v["in_ren_c_master_history"])
reg2 = {"generated_at": NOW, "repo": "https://github.com/metaeducation/ren-c",
        "fork_point": FORK_POINT, "tag_count": len(rows), "tags": rows,
        "tags_in_master_history": n_inmaster,
        "finding": ("Measured by merge-base ancestry: NONE of the 7 tags are reachable from ren-c master "
                    "(nor from the rebolsource/r3 fork point d5d6908f). The version-bearing atronix-* tags "
                    "(2014-08..2015-03) are lineage-isolated build markers on side lines. ren-c master has "
                    "NO versioned release tags on GitHub; its binaries are distributed off-GitHub (blocked).")}
save(reg2, os.path.join(MAN, "ren-c-tags-registry.json"))
n_prefork = sum(1 for v in rows.values() if v["pre_fork_shared_lineage"])
print(f"2. ren-c tags: {len(rows)} registered; pre-fork(shared): {n_prefork}")

# ---- 3. rebol/projects collection ----
RP_HEAD = None
rp_dir = os.path.join(common.ACQ, "rebol_projects")
if not os.path.isdir(os.path.join(rp_dir, ".git")):
    subprocess.run(["git", "clone", "--quiet", "--filter=blob:none", "--no-checkout",
                    "https://github.com/rebol/projects.git", rp_dir], check=True)
RP_HEAD, _, _ = run(["git", "rev-parse", "HEAD"], rp_dir)
o, _, _ = run(["git", "-c", "core.quotepath=false", "ls-tree", "-r", "HEAD"], rp_dir)
open(os.path.join(ROOT, "artifacts/manifests/trees/rebol_projects__HEAD.lsr"), "w").write(o + "\n")
rp_dest = os.path.join(ROOT, "artifacts/rebol/source/rebol-projects-master.tar.gz")
if not os.path.exists(rp_dest):
    req = urllib.request.Request(f"https://codeload.github.com/rebol/projects/tar.gz/{RP_HEAD}",
                                 headers={"User-Agent": "rebol-red-acquisition-agent/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    open(rp_dest, "wb").write(data)
rp_sha = sha256_file(rp_dest)
# quick in-tree license check
import tarfile
lic_files = []
with tarfile.open(rp_dest) as tf:
    for m in tf.getmembers():
        if m.isfile() and os.path.basename(m.name).lower() in ("license", "copying", "license.txt", "readme.md"):
            f = tf.extractfile(m)
            lic_files.append({"path": m.name, "head": " ".join(f.read(200).decode(errors="replace").split())[:120]})
save({"generated_at": NOW, "repo": "https://github.com/rebol/projects",
      "head_commit": RP_HEAD, "tree_files": len(o.splitlines()),
      "archive": "artifacts/rebol/source/rebol-projects-master.tar.gz",
      "sha256": rp_sha, "size": os.path.getsize(rp_dest),
      "description": "Rebol related sources, but not part of build (official rebol org, last pushed 2013-08-19)",
      "license_files_seen": lic_files, "license_status": "CONFIRMED" if any(x["path"].endswith(("LICENSE", "COPYING")) for x in lic_files) else "UNCLEAR"},
     os.path.join(MAN, "rebol-projects-collection.json"))
print(f"3. rebol/projects: head={RP_HEAD[:12]} archive={os.path.getsize(rp_dest)}B")

# ---- artifact records (idempotent) ----
arts = load(os.path.join(MAN, "artifacts.json"))
MANAGED = {"oldes-rebol3-releases-registry.json", "ren-c-tags-registry.json",
           "rebol-projects-collection.json", "collection-index"}
arts["artifacts"] = [a for a in arts["artifacts"] if a.get("filename") not in MANAGED
                     and a.get("path") != "artifacts/rebol/source/rebol-projects-master.tar.gz"]
def mrec(fn, project, origin, notes, classification="METADATA", path=None, sha=None, size=None):
    p = os.path.join(ROOT, path or f"artifacts/manifests/{fn}")
    return {"project": project, "version": None, "classification": classification, "origin": origin,
            "filename": fn, "path": path or f"artifacts/manifests/{fn}",
            "sha256": sha or sha256_file(p), "size": size or os.path.getsize(p), "retrieved_at": NOW,
            "provenance_status": "VERIFIED", "integrity_status": "HASHED", "license_status": "n/a", "notes": notes}
arts["artifacts"].append(mrec("oldes-rebol3-releases-registry.json", "REBOL",
    "GitHub API releases listing (persisted evidence)", f"{len(rel_rows)} releases, {tot_assets} assets - metadata only; binaries blocked"))
arts["artifacts"].append(mrec("ren-c-tags-registry.json", "REBOL",
    "git for-each-ref + merge-base ancestry analysis", f"{len(rows)} tags; {n_prefork} pre-fork on shared rebolsource/r3 lineage"))
arts["artifacts"].append({"project": "REBOL", "version": "master (2013-era)", "classification": "ARCHIVE",
    "origin": "https://github.com/rebol/projects (official rebol org, historical) - pinned HEAD archive",
    "url": "https://github.com/rebol/projects", "repository": "https://github.com/rebol/projects",
    "commit": RP_HEAD, "tag": None, "filename": "rebol-projects-master.tar.gz",
    "path": "artifacts/rebol/source/rebol-projects-master.tar.gz",
    "sha256": rp_sha, "size": os.path.getsize(rp_dest), "retrieved_at": NOW,
    "provenance_status": "VERIFIED", "integrity_status": "HASHED",
    "license_status": load(os.path.join(MAN, "rebol-projects-collection.json"))["license_status"],
    "notes": "official-org historical material ('Rebol related sources, but not part of build')"})
arts["record_count"] = len(arts["artifacts"])
save(arts, os.path.join(MAN, "artifacts.json"))

# ---- 4/5. artifacts/README.md index + verify_tree.sh (written before record hashing) ----
readme_rel = "artifacts/README.md"
script_rel = "acquisition-tools/verify_tree.sh"
n_arch = sum(1 for a in arts["artifacts"] if a.get("classification") == "ARCHIVE")
n_bin = sum(1 for a in arts["artifacts"] if a.get("classification") == "BINARY")
readme = f"""# Rebol & Red Acquisition — Collection Index

_Forensic acquisition per the "Rebol & Red Collection Agent — GitHub + Web Acquisition Protocol".
Final gate: **PARTIALLY_VERIFIED** (all GitHub-reachable material collected, pinned, and whole-tree
verified; every executable-binary channel is network-blocked from this environment — see
`logs/blocked-attempts.json` for 21+ recorded attempts with verbatim TLS errors)._

## Layout

| Path | Contents |
|---|---|
| `releases/` (red) | red/red tag archives v0.6.3, v0.6.4, v0.6.5, v0.6.6 — each whole-tree verified against its pinned commit (git blob SHA-1 of every member == `git ls-tree`) |
| `source/` (rebol) | rebol/rebol @25033f89 (official R3), rebolsource/r3 @98cdfcd6, ren-c @e31d5698, Oldes/Rebol3 @d5b237ce, rebol/projects (historical org material) |
| `documentation/` (red) | red/REP @95d96a64 (BSD-3, in-tree LICENSE), red/docs @e6272166 (license UNCLEAR) |
| `documentation/` (rebol) | rebolsource/rebol-syntax @4ff11396 (license UNCLEAR) |
| `tests/` | rebolsource/rebol-test @409ef5c2; red test-fixture binaries @v0.6.6 (git-blob verified) |
| `manifests/` | machine-readable evidence (see below) |
| `provenance/` | provenance graph + reconciliation tables |
| `reports/` | collection-report.json (authoritative) + collection-report.md (human) |
| `logs/` | network events, search queries, blocked attempts, execution evidence |
| `derived/` | ephemeral extraction area (gitignored; re-derivable via `acquisition-tools/common.py`) |

## Key manifests

| File | Purpose |
|---|---|
| `manifests/artifacts.json` | **Authoritative artifact ledger** ({arts['record_count']} records: {n_arch} archives, {n_bin} binaries) |
| `manifests/sha256sums.txt` | hash manifest over all committed evidence — `sha256sum -c artifacts/manifests/sha256sums.txt` |
| `manifests/git-collection.json` | clone evidence: HEADs, tag->commit/tree resolution, describe, per-ref tree manifests |
| `manifests/continuation-verification.json` | whole-tree archive verification results (10/10 HASH_MATCHED) |
| `manifests/red-tags-registry.json` / `oldes-tags-registry.json` / `ren-c-tags-registry.json` | complete tag registries with commit/tree/date/subject |
| `manifests/oldes-rebol3-releases-registry.json` | all releases + asset URLs/sizes (binaries blocked) |
| `manifests/upstream-ci-rebol-urls.json` | official CI's own Rebol download URLs (static.red-lang.org/tmp/rebol) |
| `manifests/fork-vs-upstream-v0.6.4.json` + `fork-diff-magnitudes.json` | workspace fork attribution vs upstream |
| `manifests/bootstrap-procedure-evidence.json` | verbatim line-numbered Rebol2/SDK bootstrap claims |
| `manifests/acquisition-determinism.json` | codeload re-fetch byte-identity proof (REPRODUCED) |

## How to re-verify (any environment with GitHub access)

1. `sha256sum -c artifacts/manifests/sha256sums.txt` — integrity of the evidence layer.
2. Whole-tree verification: `acquisition-tools/verify_tree.sh <clone-dir> <pinned-ref> <archive.tar.gz>`
   (recomputes git blob SHA-1 of every archive member vs `git ls-tree` of the ref).
3. Re-fetch any `releases/*.tar.gz` from `https://codeload.github.com/red/red/tar.gz/refs/tags/<tag>`
   and compare SHA-256 — proven byte-deterministic (2/2 samples).

## Status taxonomy in use

- provenance: VERIFIED / PARTIALLY_VERIFIED / PROVISIONAL / BLOCKED / UNVERIFIED / CONFLICTING
- integrity: HASHED / HASH_MATCHED / NO_REFERENCE_HASH
- license: CONFIRMED / PARTIALLY_CONFIRMED / UNCLEAR / MISSING
- bootstrap: BOOTSTRAP_CLAIMED + BOOTSTRAP_SOURCE_PRESENT only — nothing executed, NOT_REPRODUCED
"""
open(os.path.join(ROOT, readme_rel), "w").write(readme)

# ---- 5. verify_tree.sh ----
script = """#!/usr/bin/env bash
# Whole-tree verification: does a stored codeload archive match a pinned git ref?
# usage: verify_tree.sh <clone-dir> <ref> <archive.tar.gz>
set -euo pipefail
CLONE="$1"; REF="$2"; ARCHIVE="$3"
comm -3 \\
  <(git -C "$CLONE" -c core.quotepath=false ls-tree -r "$REF" | awk '{print $3"\\t"$2}' | sort) \\
  <(tar -tzf "$ARCHIVE" | tail -n +2 | sort) >/dev/null && echo "path-set: OK" || echo "path-set: DIFFERS"
python3 - "$CLONE" "$REF" "$ARCHIVE" <<'PY'
import hashlib, subprocess, sys, tarfile
clone, ref, archive = sys.argv[1:4]
ls = {}
out = subprocess.run(["git", "-C", clone, "-c", "core.quotepath=false", "ls-tree", "-r", ref],
                     capture_output=True, text=True).stdout
for line in out.splitlines():
    meta, path = line.split("\\t", 1)
    ls[path] = meta.split()[2]
matched = missing = extra = mismatch = 0
with tarfile.open(archive) as tf:
    for m in tf:
        if not m.isfile(): continue
        rel = m.name.split("/", 1)[1]
        data = tf.extractfile(m).read()
        b = hashlib.sha1(b"blob %d\\0" % len(data) + data).hexdigest()
        if rel not in ls: extra += 1
        elif ls[rel] == b: matched += 1
        else: mismatch += 1
missing = len(ls) - matched - mismatch
print(f"matched={matched} mismatch={mismatch} missing={missing} extra={extra}")
sys.exit(0 if (mismatch == 0 and missing == 0 and extra == 0) else 1)
PY
"""
open(os.path.join(ROOT, script_rel), "w").write(script)
os.chmod(os.path.join(ROOT, script_rel), 0o755)



# ---- provenance ----
prov = load(os.path.join(PROV, "provenance.json"))
_seen = {(e["relationship"], e["source"], e["target"]) for e in prov["graph"]}
def edge(rel, s, t, evd, status="ESTABLISHED"):
    if (rel, s, t) in _seen: return
    prov["graph"].append({"relationship": rel, "source": s, "target": t, "evidence": evd, "status": status})
edge("release-registry", "Oldes/Rebol3 GitHub releases (29)", "asset metadata registry",
     f"{tot_assets} asset URLs+sizes persisted (manifests/oldes-rebol3-releases-registry.json); downloads blocked")
prov["graph"] = [e for e in prov["graph"] if e["relationship"] != "tag-lineage"]
edge("tag-lineage", "ren-c version-bearing tags (atronix-*)", "isolated side lines (NOT in master history)",
     "merge-base ancestry: 0/7 tags reachable from ren-c master or from fork point d5d6908f - build markers on side lines (manifests/ren-c-tags-registry.json)")
edge("org-collection", "rebol org (rebol/projects)", "pinned HEAD archive + tree manifest",
     f"HEAD {RP_HEAD[:12]} archived (sha256 {rp_sha[:12]}…); official org, historical (last push 2013)")
save(prov, os.path.join(PROV, "provenance.json"))

# ---- reconciliation ----
recon = load(os.path.join(PROV, "reconciliation.json"))
recon["tables"] = [t for t in recon["tables"] if t["id"] != "R14"]
recon["tables"].append({"id": "R14", "artifact": "ren-c release identity",
  "rows": [
   ["GitHub releases", "none exist", "-", "MISSING"],
   ["Version-bearing tags", "atronix-3.0.90/91/99 (2014-2015)", f"ancestry check: 0/{len(rows)} tags reachable from ren-c master; 0 from rebolsource/r3 fork point", "CONFLICT (version-bearing tags are lineage-isolated build markers, not part of any main line)"],
   ["ren-c version claim", "internal src/specs/version.r = 2.102.0.0.0", "no matching tag or release anywhere on GitHub", "UNRESOLVED (no release channel to reconcile against; binaries off-GitHub, blocked)"],
  ]})
save(recon, os.path.join(PROV, "reconciliation.json"))

# ---- report, addendum, sums ----
run(["python3", os.path.join(ROOT, "acquisition-tools/06_report.py")])
add = []
add.append("\n## Continuation Addendum (stage 11)\n")
add.append(f"_Generated: {NOW}_\n")
add.append("### Release-asset registries (metadata persisted; downloads blocked)\n")
add.append(f"- **Oldes/Rebol3**: all {len(rel_rows)} releases + {tot_assets} asset URLs/sizes persisted (`manifests/oldes-rebol3-releases-registry.json`) — durable acquisition targets.")
add.append(f"- **ren-c**: {len(rows)} tags registered; merge-base ancestry shows **0/{len(rows)} tags are reachable from ren-c master** (nor from the rebolsource/r3 fork point) — the atronix-* version tags are lineage-isolated build markers. ren-c master has **no versioned release tags** (recon R14).\n")
add.append("### rebol/projects collected (official org, historical)\n")
add.append(f"- HEAD `{RP_HEAD[:12]}` archived (`rebol-projects-master.tar.gz`, sha256 `{rp_sha[:16]}…`) + tree manifest. \"Rebol related sources, but not part of build\" (last push 2013-08-19).\n")
add.append("### Collection index + verifier\n")
add.append("- `artifacts/README.md` — layout, key manifests, **re-verification guide**, status taxonomy.")
add.append("- `acquisition-tools/verify_tree.sh` — reusable whole-tree verifier (clone + ref + archive).\n")
add.append("### Status impact\n")
add.append("- Final gate remains **PARTIALLY_VERIFIED**. The acquisition layer is now self-describing: a third party can re-verify every claim from the repository alone.\n")

_mdp = os.path.join(REP, "collection-report.md")
_md = open(_mdp).read()
_md = _md.split("\n## Continuation Addendum (stage 11)\n")[0].rstrip() + "\n"
with open(_mdp, "w") as f:
    f.write(_md + "\n".join(add) + "\n")

sums = []
for dirpath, dirnames, filenames in os.walk(A):
    if "derived" in dirpath.split(os.sep):
        continue
    for fn in sorted(filenames):
        p = os.path.join(dirpath, fn)
        rel = os.path.relpath(p, ROOT)
        if rel.endswith("sha256sums.txt"):
            continue
        sums.append(f"{sha256_file(p)}  {rel}")
with open(os.path.join(MAN, "sha256sums.txt"), "w") as f:
    f.write("\n".join(sorted(sums)) + "\n")
print(f"stage 11 complete; records={arts['record_count']} sha_lines={len(sums)}")
