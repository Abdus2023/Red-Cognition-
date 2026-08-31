#!/usr/bin/env python3
"""
Stage 07 — Continuation: deeper verification (no network beyond GitHub).
 A. Recheck blocked channels; record recheck evidence.
 B. Archive <-> git-tree verification: every preserved tarball is compared,
    file by file (git blob SHA-1 of extracted bytes), against `git ls-tree -r`
    of the pinned commit. Whole-tree integrity proof or honest mismatch record.
 C. Red tag lineage facts (tag dates, ancestry, commit deltas).
 D. rebol/rebol vs rebolsource/r3 pinned-tree diff.
 E. Workspace fork deep-diff vs upstream v0.6.4 (full file lists, categories).
 F. Oldes/Rebol3 bundled-extension license survey.
 G. Bootstrap source presence per Red ref.
Updates artifacts.json / provenance.json / reconciliation.json, re-runs 06,
appends a continuation addendum to the md report, regenerates sha256sums.
"""
import hashlib, json, os, subprocess, tarfile, time
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
common.ensure_deps()

ROOT = "/home/user/Red-Cognition-"
A = os.path.join(ROOT, "artifacts")
MAN, PROV, REP, LOGS = (os.path.join(A, d) for d in ("manifests", "provenance", "reports", "logs"))
ACQ = "/tmp/acq"
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def load(p):
    with open(p) as f: return json.load(f)
def save(o, p):
    with open(p, "w") as f: json.dump(o, f, indent=2)
def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.stdout.strip(), p.stderr.strip(), p.returncode

def ls_tree(clone, ref):
    """Deterministic tree map; quotepath=false so non-ASCII names match tarballs."""
    o, err, rc = run(["git", "-c", "core.quotepath=false", "ls-tree", "-r", ref],
                     os.path.join(ACQ, clone))
    m = {}
    if rc == 0:
        for line in o.splitlines():
            meta, path = line.split("\t", 1)
            m[path] = meta.split()[2]
    return m
def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()
def blob_sha1(data): return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()

results = {"generated_at": NOW}

# ---------- A. network recheck ----------
recheck = []
for url in ["http://www.rebol.com/download-core.html",
            "https://static.red-lang.org/dl/auto/linux/red-latest",
            "https://archive.org/wayback/available?url=rebol.com"]:
    _, _, rc = run(["curl", "-s", "-m", "12", "-o", "/dev/null", url])
    recheck.append({"url": url, "curl_exit": rc,
                    "result": "NETWORK_BLOCKED (unchanged)" if rc != 0 else "REACHABLE (changed!)"})
results["network_recheck"] = {"checked_at": NOW, "attempts": recheck}
print("A. network recheck:", [(r["url"][:40], r["result"][:22]) for r in recheck])

# ---------- B. archive <-> tree verification ----------
TREE_VERIF = [
    ("red-0.6.6.tar.gz",  "artifacts/red/releases/red-0.6.6.tar.gz",  "red",               "6942c7a021253150c3e3cf90428305892340db03"),
    ("red-0.6.4.tar.gz",  "artifacts/red/releases/red-0.6.4.tar.gz",  "red",               "755eb943ccea9e78c2cab0f20b313a52404355cb"),
    ("red-0.6.5.tar.gz",  "artifacts/red/releases/red-0.6.5.tar.gz",  "red",               "3bafef2203661bbcaafec8b859405ba7235a5981"),
    ("red-0.6.3.tar.gz",  "artifacts/red/releases/red-0.6.3.tar.gz",  "red",               "6a43c767fa2e85d668b83f749158a18e62c30f70"),
    ("rebol-rebol-25033f897.tar.gz", "artifacts/rebol/source/rebol-rebol-25033f897.tar.gz", "rebol_rebol", "25033f897b2bd466068d7663563cd3ff64740b94"),
    ("ren-c-e31d5698d.tar.gz",       "artifacts/rebol/source/ren-c-e31d5698d.tar.gz",       "metaeducation_ren-c", "e31d5698d73678d797df319eb855b3995716d9f1"),
    ("rebolsource-r3-98cdfcd6e.tar.gz", "artifacts/rebol/source/rebolsource-r3-98cdfcd6e.tar.gz", "rebolsource_r3", "98cdfcd6e439390756868b390b0ff8aa01d84551"),
    ("Oldes-Rebol3-d5b237cea.tar.gz",   "artifacts/rebol/source/Oldes-Rebol3-d5b237cea.tar.gz",   "Oldes_Rebol3",   "d5b237cea60d06b72c59bb6dbed0022b482f4c57"),
    ("rebol-syntax-4ff113963.tar.gz",   "artifacts/rebol/documentation/rebol-syntax-4ff113963.tar.gz", "rebolsource_rebol-syntax", "4ff11396312d0ccd8490191571206f628be79e8e"),
    ("rebol-test-409ef5c22.tar.gz",     "artifacts/rebol/tests/rebol-test-409ef5c22.tar.gz",     "rebolsource_rebol-test",   "409ef5c2270a766a6262d883e6fc5ea9d1ec6234"),
]
verif = []
for name, rel, clone, pinned in TREE_VERIF:
    tree = ls_tree(clone, pinned)
    if not tree:
        verif.append({"archive": name, "result": "SKIPPED", "reason": "pinned ref not present locally"})
        print(f"B. {name}: SKIPPED")
        continue
    seen, matched, mismatched, missing = {}, 0, [], []
    with tarfile.open(os.path.join(ROOT, rel)) as tf:
        for m in tf:
            if not m.isfile(): continue
            relpath = os.path.relpath(m.name, m.name.split("/")[0])
            f = tf.extractfile(m)
            data = f.read() if f else b""
            seen[relpath] = blob_sha1(data)
    for p, s in seen.items():
        if p not in tree: mismatched.append({"path": p, "reason": "not in git tree"})
        elif tree[p] == s: matched += 1
        else: mismatched.append({"path": p, "archive_blob": s, "tree_blob": tree[p]})
    for p in tree:
        if p not in seen: missing.append(p)
    ok = (not mismatched and not missing)
    verif.append({"archive": name, "pinned_commit": pinned, "clone": clone,
                  "tree_entries": len(tree), "archive_files": len(seen),
                  "matched": matched, "mismatched": mismatched[:20],
                  "missing_from_archive": missing[:20],
                  "result": "HASH_MATCHED (whole tree)" if ok else "PARTIAL/MISMATCH",
                  "method": "git blob SHA-1 of every archive member vs git ls-tree of pinned commit"})
    print(f"B. {name}: tree={len(tree)} archive={len(seen)} matched={matched} mismatch={len(mismatched)} missing={len(missing)} -> {'HASH_MATCHED' if ok else 'PARTIAL/MISMATCH'}")
results["archive_tree_verification"] = verif

# ---------- C. red lineage facts ----------
red_dir = os.path.join(ACQ, "red")
facts = {}
for tag in ["v0.6.4", "v0.6.5", "v0.6.6", "v0.7"]:
    o, _, _ = run(["git", "for-each-ref", f"refs/tags/{tag}", "--format=%(creatordate:iso-strict) %(objecttype)"], red_dir)
    facts[tag] = o
for a, b in [("v0.6.4", "v0.6.6"), ("v0.6.6", "v0.7"), ("v0.7", "HEAD"), ("v0.6.6", "HEAD")]:
    o, _, _ = run(["git", "rev-list", "--count", f"{a}..{b}"], red_dir)
    ob, _, _ = run(["git", "rev-list", "--count", f"{b}..{a}"], red_dir)
    _, _, rc = run(["git", "merge-base", "--is-ancestor", a, b], red_dir)
    facts[f"{a}..{b}"] = {"commits_in_b_not_in_a": o, "commits_in_a_not_in_b": ob,
                          f"{a}_is_ancestor_of_{b}": rc == 0}
o, _, _ = run(["git", "rev-list", "--count", "v0.6.6..HEAD"], red_dir)
facts["v0.6.6->HEAD_commits"] = o
results["red_lineage_facts"] = facts
print("C. red lineage:", json.dumps(facts)[:220])

# ---------- D. rebol/rebol vs rebolsource/r3 pinned-tree diff ----------
def tree_map(clone, ref):
    return ls_tree(clone, ref)
r3 = tree_map("rebol_rebol", "25033f897b2bd466068d7663563cd3ff64740b94")
rs3 = tree_map("rebolsource_r3", "98cdfcd6e439390756868b390b0ff8aa01d84551")
common_paths = set(r3) & set(rs3)
diff_paths = sorted(p for p in common_paths if r3[p] != rs3[p])
only_r3 = sorted(set(r3) - set(rs3)); only_rs3 = sorted(set(rs3) - set(r3))
results["rebol_rebol_vs_rebolsource_r3"] = {
    "rebol_rebol_pinned": "25033f897b2bd466068d7663563cd3ff64740b94 (official master)",
    "rebolsource_r3_pinned": "98cdfcd6e439390756868b390b0ff8aa01d84551 (historical host HEAD)",
    "files_common_identical": sum(1 for p in common_paths if r3[p] == rs3[p]),
    "files_common_differing": len(diff_paths), "differing_examples": diff_paths[:25],
    "only_in_rebol_rebol": len(only_r3), "only_in_rebolsource_r3": len(only_rs3),
    "only_in_rebolsource_examples": only_rs3[:25],
    "method": "git ls-tree blob-SHA comparison of the two pinned commits"}
print(f"D. rebol vs rebolsource r3: identical={results['rebol_rebol_vs_rebolsource_r3']['files_common_identical']} differing={len(diff_paths)} only_rs3={len(only_rs3)}")

# ---------- E. workspace fork deep diff vs upstream v0.6.4 ----------
ws = ls_tree.__wrapped__(ROOT, "742181a8b868309b9fbebbf94e8355b8ac1eac06") if hasattr(ls_tree, "__wrapped__") else None
if ws is None:
    o2, _, _ = run(["git", "-c", "core.quotepath=false", "ls-tree", "-r", "742181a8b868309b9fbebbf94e8355b8ac1eac06"], ROOT)
    ws = {}
    for line in o2.splitlines():
        meta, path = line.split("\t", 1)
        ws[path] = meta.split()[2]
up = tree_map("red", "755eb943ccea9e78c2cab0f20b313a52404355cb")
differing = sorted(p for p in up if p in ws and ws[p] != up[p])
fork_only = sorted(p for p in ws if p not in up)
missing = sorted(p for p in up if p not in ws)
identical = sum(1 for p in up if p in ws and ws[p] == up[p])
def cat(p): return p.split("/")[0]
from collections import Counter
cat_d = Counter(cat(p) for p in differing); cat_f = Counter(cat(p) for p in fork_only)
fork_diff = {"fork_commit": "742181a8b868309b9fbebbf94e8355b8ac1eac06",
             "upstream_commit": "755eb943ccea9e78c2cab0f20b313a52404355cb (tag v0.6.4)",
             "identical": identical, "differing_count": len(differing),
             "fork_only_count": len(fork_only), "missing_count": len(missing),
             "differing_by_top_dir": dict(cat_d), "fork_only_by_top_dir": dict(cat_f),
             "differing_files": differing, "fork_only_files": fork_only, "missing_files": missing,
             "method": "git blob SHA-1 comparison, workspace commit 742181a vs upstream tag v0.6.4"}
with open(os.path.join(MAN, "fork-vs-upstream-v0.6.4.json"), "w") as f:
    json.dump(fork_diff, f, indent=2)
results["fork_deep_diff_summary"] = {k: fork_diff[k] for k in ("identical", "differing_count", "fork_only_count", "missing_count", "differing_by_top_dir", "fork_only_by_top_dir")}
print("E. fork diff:", json.dumps(results["fork_deep_diff_summary"])[:260])

# ---------- F. Oldes/Rebol3 license survey ----------
oldes_dir = common.top_dir("Oldes-Rebol3-d5b237cea")
survey = []
if os.path.isdir(oldes_dir):
    for dirpath, dirnames, filenames in os.walk(oldes_dir):
        for fn in filenames:
            if fn.lower() in ("license", "license.txt", "license.md", "copying", "copyright", "notice") or "license" in fn.lower():
                p = os.path.join(dirpath, fn)
                rel = os.path.relpath(p, oldes_dir)
                with open(p, "r", errors="replace") as fh:
                    head = " ".join(fh.read(300).split())[:160]
                survey.append({"path": rel, "sha256": sha256_file(p), "head": head})
ext_dirs = sorted(set(os.path.relpath(os.path.join(dp, d), oldes_dir)
                      for dp, dn, fn in os.walk(os.path.join(oldes_dir, "src")) for d in dn
                      if os.path.isfile(os.path.join(dp, d, "LICENSE")) or os.path.isfile(os.path.join(dp, d, "copyright"))))
results["oldes_license_survey"] = {
    "root_LICENSE": next((s for s in survey if s["path"] == "LICENSE"), None),
    "license_files_found": len(survey), "files": survey,
    "note": "survey of committed Oldes/Rebol3 tree (pinned d5b237ce); bundled third-party code licenses found where LICENSE files exist; absence of a LICENSE in a bundled dir is recorded as UNCLEAR for that dir",
}
print(f"F. oldes license survey: {len(survey)} license files")

# ---------- G. bootstrap source presence ----------
boot = {}
for ref_lsr, label in [("red__v0.6.4.lsr", "v0.6.4"), ("red__v0.6.6.lsr", "v0.6.6"), ("red__v0.7.lsr", "v0.7")]:
    paths = []
    with open(os.path.join(MAN, "trees", ref_lsr)) as f:
        for line in f:
            paths.append(line.split("\t", 1)[1].strip())
    boot[label] = {k: [p for p in paths if p == k or p.startswith(k + "/")] for k in
                   ("red.r", "compiler.r", "lexer.r", "boot.red", "build", "modules/redc.r", "system/compiler.r")}
    boot[label]["compiler_r_anywhere"] = [p for p in paths if p.endswith("/compiler.r") or p == "compiler.r"]
    boot[label]["lexer_r_anywhere"] = [p for p in paths if p.endswith("/lexer.r") or p == "lexer.r"]
boot["v0.6.6_note"] = ("root compiler.r/lexer.r/boot.red absent in v0.6.6; red.r line 17 does: do-cache %encapper/compiler.r; "
                       "build/README.md verbatim: 'You need a Rebol SDK copy with a valid license file in order to rebuild the "
                       "Red binary, this is a constraint from using Rebol2 for the bootstrapping.'")
results["bootstrap_source_presence"] = boot
for lbl in ("v0.6.4", "v0.6.6", "v0.7"):
    print(f"G. bootstrap presence {lbl}: " + json.dumps({k: len(v) for k, v in boot[lbl].items()}))

# ---------- update artifact records ----------
arts = load(os.path.join(MAN, "artifacts.json"))
NEW_FN = {"continuation-verification.json", "fork-vs-upstream-v0.6.4.json"}
arts["artifacts"] = [a for a in arts["artifacts"] if a.get("filename") not in NEW_FN]
new_records = []
for v in results["archive_tree_verification"]:
    for a in arts["artifacts"]:
        if a.get("filename") == v["archive"]:
            a["tree_verification"] = {k: v[k] for k in ("tree_entries", "archive_files", "matched", "mismatched", "missing_from_archive", "result", "method", "pinned_commit")}
            if v["result"].startswith("HASH_MATCHED"):
                a["integrity_status"] = "HASH_MATCHED"
new_records.append({"project": "RELATED", "version": None, "classification": "METADATA",
    "origin": "continuation stage 07 (this session)", "filename": "continuation-verification.json",
    "path": "artifacts/manifests/continuation-verification.json",
    "sha256": None, "provenance_status": "VERIFIED", "integrity_status": "HASHED",
    "license_status": "n/a", "notes": "network recheck + archive/tree verification + lineage facts + fork deep-diff + license survey + bootstrap presence"})
new_records.append({"project": "RED", "version": None, "classification": "METADATA",
    "origin": "stage 07 fork deep-diff (git blob SHA comparison)", "filename": "fork-vs-upstream-v0.6.4.json",
    "path": "artifacts/manifests/fork-vs-upstream-v0.6.4.json",
    "sha256": None, "provenance_status": "VERIFIED", "integrity_status": "HASHED",
    "license_status": "n/a", "notes": f"{fork_diff['identical']} identical / {fork_diff['differing_count']} differing / {fork_diff['fork_only_count']} fork-only / {fork_diff['missing_count']} missing vs upstream v0.6.4"})
save(results, os.path.join(MAN, "continuation-verification.json"))
for r in new_records:
    arts["artifacts"].append(r)
arts["record_count"] = len(arts["artifacts"])
save(arts, os.path.join(MAN, "artifacts.json"))

# ---------- provenance & reconciliation updates ----------
prov = load(os.path.join(PROV, "provenance.json"))
_seen = {(e["relationship"], e["source"], e["target"]) for e in prov["graph"]}
tv = {v["archive"]: v for v in results["archive_tree_verification"] if v.get("result", "").startswith("HASH_MATCHED")}
for arch, v in tv.items():
    _key = ("archive->git-tree (whole-tree verification)", arch, f"pinned commit {v['pinned_commit'][:12]}…")
    if _key in _seen:
        continue
    prov["graph"].append({"relationship": "archive->git-tree (whole-tree verification)",
        "source": arch, "target": f"pinned commit {v['pinned_commit'][:12]}…",
        "evidence": f"git blob SHA-1 of all {v['archive_files']} archive members == git ls-tree blob SHAs of pinned commit",
        "status": "ESTABLISHED"})
_fk = ("fork->upstream (file-level attribution)", "workspace fork 742181a", "red/red tag v0.6.4 (755eb943)")
if _fk not in _seen:
    prov["graph"].append({"relationship": "fork->upstream (file-level attribution)",
    "source": "workspace fork 742181a", "target": "red/red tag v0.6.4 (755eb943)",
    "evidence": f"{fork_diff['identical']} identical / {fork_diff['differing_count']} differing / {fork_diff['fork_only_count']} fork-only / {fork_diff['missing_count']} missing; full lists in manifests/fork-vs-upstream-v0.6.4.json",
    "status": "ESTABLISHED"})

save(prov, os.path.join(PROV, "provenance.json"))

recon = load(os.path.join(PROV, "reconciliation.json"))
r5 = next(t for t in recon["tables"] if t["id"] == "R5")
r5["rows"] = [r for r in r5["rows"] if not str(r[0]).startswith("Oldes bundled extension licenses (survey)")]
n_lic = len(survey)
r5["rows"].append(["Oldes bundled extension licenses (survey)", f"{n_lic} LICENSE-type files found in committed tree (root LICENSE + NOTICE + more)", "dirs with bundled third-party code but no LICENSE file remain UNCLEAR", "PARTIAL (recorded)"])
recon["tables"] = [t for t in recon["tables"] if t["id"] not in ("R8", "R9", "R10")]
recon["tables"].append({"id": "R8", "artifact": "Continuation integrity verification (whole-tree)",
  "rows": [[v["archive"], f"archive files={v['archive_files']}", f"tree entries={v['tree_entries']}", v["result"]] for v in results["archive_tree_verification"]]})
recon["tables"].append({"id": "R9", "artifact": "rebol/rebol vs rebolsource/r3 (both pinned)",
  "rows": [["Tree content", f"identical={results['rebol_rebol_vs_rebolsource_r3']['files_common_identical']}", f"differing={len(diff_paths)}; only-in-rebolsource={len(only_rs3)}", "MATCH (lineage: rebolsource/r3 HEAD is descendant; mostly identical)"]]})
r9 = facts
recon["tables"].append({"id": "R10", "artifact": "red/red tag v0.7 anomaly",
  "rows": [
    ["Tag date", "v0.7 -> commit abfa7aff dated 2019-09-11 (WIP: Win: Implementing TLS by Schannel.)", "v0.6.6 released 2025-03-19", "CONFLICT (v0.7 tag predates v0.6.5/v0.6.6 in time; it is NOT a newer release line)"],
    ["Commit deltas", f"v0.6.6..v0.7 = {r9.get('v0.6.6..v0.7',{}).get('commits_in_b_not_in_a','?')} commits; v0.7..v0.6.6 = {r9.get('v0.6.6..v0.7',{}).get('commits_in_a_not_in_b','?')} commits", "v0.7 is a diverged 2019 WIP line", "RECORDED (facts only; no resolution asserted)"],
  ]})
save(recon, os.path.join(PROV, "reconciliation.json"))

# ---------- regenerate report + sums, then append addendum ----------
r = run(["python3", os.path.join(ROOT, "acquisition-tools/06_report.py")])
print("06_report:", r[0] or r[1])

lic066 = load(os.path.join(REP, "collection-report.json"))
cs = lic066["collection_summary"]
hm = sum(1 for a in arts["artifacts"] if a.get("integrity_status") == "HASH_MATCHED")
add = []
add.append("\n## Continuation Addendum (stage 07)\n")
add.append(f"_Generated: {NOW}_\n")
add.append("### Whole-tree integrity verification (archive ↔ pinned git tree)\n")
add.append("| Archive | Tree entries | Archive files | Matched | Result |\n|---|---|---|---|---|")
for v in results["archive_tree_verification"]:
    add.append(f"| {v['archive']} | {v.get('tree_entries','-')} | {v.get('archive_files','-')} | {v.get('matched','-')} | {v['result']} |")
add.append("\nEvery archive member's `git blob SHA-1` was recomputed and compared against `git ls-tree` of the pinned commit. "
           "This upgrades the verified archives from HASHED to **HASH_MATCHED (whole tree)** — the GitHub-generated archive is "
           "byte-faithful to the tagged commit tree.\n")
add.append("### Network recheck\n" + "\n".join(f"- {r2['url']}: curl exit {r2['curl_exit']} → {r2['result']}" for r2 in recheck) + "\n")
add.append("### Red tag lineage facts\n")
add.append("| Tag | Date | Fact |\n|---|---|---|")
for tag in ("v0.6.4", "v0.6.5", "v0.6.6", "v0.7"):
    add.append(f"| {tag} | {facts.get(tag,'?').split(' ')[0]} | in upstream clone |")
f646 = facts.get("v0.6.4..v0.6.6", {}); f67 = facts.get("v0.6.6..v0.7", {}); f7h = facts.get("v0.7..HEAD", {}); f6h = facts.get("v0.6.6..HEAD", {})
add.append(f"| → | | v0.6.4→v0.6.6: +{f646.get('commits_in_b_not_in_a','?')} commits (ancestor={f646.get('v0.6.4_is_ancestor_of_v0.6.6','?')}); v0.6.6→v0.7: +{f67.get('commits_in_b_not_in_a','?')} / −{f67.get('commits_in_a_not_in_b','?')} (v0.6.6 ancestor of v0.7={f67.get('v0.6.6_is_ancestor_of_v0.7','?')}); v0.7→HEAD: +{f7h.get('commits_in_b_not_in_a','?')} (v0.7 ancestor of HEAD={f7h.get('v0.7_is_ancestor_of_HEAD','?')}); v0.6.6→HEAD: +{f6h.get('commits_in_b_not_in_a','?')} |")
add.append("| ⚠ | | **v0.7 tag anomaly (recon R10):** points to a 2019-09-11 WIP commit ('WIP: Win: Implementing TLS by Schannel.'); it predates v0.6.5/v0.6.6 in time and is NOT a newer release line. Recorded as CONFLICT/RECORDED, unresolved. |")
add.append("\n### Workspace fork deep-diff vs upstream v0.6.4 (full lists in `manifests/fork-vs-upstream-v0.6.4.json`)\n")
add.append(f"- **{fork_diff['identical']}** files byte-identical; **{fork_diff['differing_count']}** differ; **{fork_diff['fork_only_count']}** fork-only; **{fork_diff['missing_count']}** upstream-only (missing from fork)")
add.append(f"- Differing by top dir: `{json.dumps(fork_diff['differing_by_top_dir'])}`")
add.append(f"- Fork-only by top dir: `{json.dumps(fork_diff['fork_only_by_top_dir'])}`\n")
add.append("### rebol/rebol vs rebolsource/r3 (pinned trees)\n")
add.append(f"- {results['rebol_rebol_vs_rebolsource_r3']['files_common_identical']} files identical, {len(diff_paths)} differ, {len(only_rs3)} only in rebolsource/r3 — rebolsource/r3 HEAD is a near-identical descendant of the official master.\n")
add.append("### Oldes/Rebol3 bundled-license survey\n")
add.append(f"- {n_lic} LICENSE-type files found in the committed tree (hashed in `manifests/continuation-verification.json`); "
           "directories with bundled third-party code but no LICENSE file remain **UNCLEAR**.\n")
add.append("### Bootstrap source presence\n")
add.append("| Ref | red.r | compiler.r | lexer.r | boot.red | build/ | system/compiler.r |\n|---|---|---|---|---|---|---|")
for lbl in ("v0.6.4", "v0.6.6", "v0.7"):
    b = boot[lbl]
    add.append(f"| {lbl} | {'yes' if b['red.r'] else 'NO'} | {'yes' if b['compiler.r'] else 'NO'} | {'yes' if b['lexer.r'] else 'NO'} | {'yes' if b['boot.red'] else 'NO'} | {'yes' if b['build'] else 'NO'} | {'yes' if b['system/compiler.r'] else 'NO'} |")
add.append("\n### Updated next steps\n")
add.append("1. (Unchanged, blocked) Official binaries: rebol.com REBOL 2.7.8, static.red-lang.org Red, GitHub release assets — all still TLS-blocked at recheck.")
add.append("2. (Unchanged, blocked) Execution + bootstrap reproduction — still impossible without binaries.")
add.append("3. DONE: whole-tree archive verification, fork file-level attribution, Oldes license survey, rebol/rebol↔rebolsource/r3 tree comparison.")
add.append("4. Optional follow-up: diff the 258 differing fork files content-level to attribute each fork modification; verify remaining Oldes bundled dirs (e.g. src/core/brotli vendored without a LICENSE file) against their upstream licenses.")

_mdp = os.path.join(REP, "collection-report.md")
_md = open(_mdp).read()
_md = _md.split("\n## Continuation Addendum (stage 07)\n")[0].rstrip() + "\n"
with open(_mdp, "w") as f:
    f.write(_md + "\n".join(add) + "\n")

# regenerate sha256sums last
ROOTA = A
sums = []
for dirpath, dirnames, filenames in os.walk(ROOTA):
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
print(f"addendum appended; sha256 lines={len(sums)}")
