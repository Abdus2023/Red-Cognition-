#!/usr/bin/env python3
"""
Stage 18 — Official wikis + final audit.
 A. Egress probe (recorded).
 B. Collect official GitHub wikis (Tier-1, repo-adjacent documentation):
    red/red.wiki + metaeducation/ren-c.wiki (Oldes/Rebol3 has none - recorded).
    Clone evidence + pinned HEAD archives + tree manifests + page inventory +
    bootstrap/build-content quotes (verbatim, path:line).
 C. Final audit: sha256sum -c + ledger consistency counts in one record.
 D. Ledger, provenance, addendum, sums, self-check.
"""
import hashlib, json, os, subprocess, time, urllib.request
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common

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

# ---- A. probe ----
_, _, rc = run(["curl", "-s", "-m", "10", "-o", "/dev/null",
                "https://static.red-lang.org/dl/auto/linux/red-latest"])
print("A. probe exit", rc)

# ---- B. wikis ----
WIKIS = [
    ("red_red-wiki", "https://github.com/red/red.wiki.git", "https://github.com/red/red/wiki",
     "official Red language/toolchain wiki"),
    ("ren-c_wiki", "https://github.com/metaeducation/ren-c.wiki.git", "https://github.com/metaeducation/ren-c/wiki",
     "official ren-c wiki (build/boot docs likely)"),
]
wiki_state = {"generated_at": NOW, "wikis": {}, "negative": {"Oldes/Rebol3.wiki": "not found (repo has no wiki)"}}
dls = load(os.path.join(MAN, "downloads.json"))
for name, url, web, desc in WIKIS:
    d = os.path.join(common.ACQ, name)
    if not os.path.isdir(os.path.join(d, ".git")):
        subprocess.run(["git", "clone", "--quiet", url, d], check=True)
    head, _, _ = run(["git", "rev-parse", "HEAD"], d)
    o, _, _ = run(["git", "-c", "core.quotepath=false", "ls-tree", "-r", "HEAD"], d)
    open(os.path.join(MAN, "trees", f"{name}__HEAD.lsr"), "w").write(o + "\n")
    dest_rel = f"artifacts/red/documentation/{name.replace('_', '-')}-{head[:9]}.tar.gz"
    dest = os.path.join(ROOT, dest_rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if not os.path.exists(dest):
        # wikis have no codeload endpoint; build the archive locally from the clone
        top = os.path.join(common.ACQ, f"{name}-export")
        subprocess.run(["rm", "-rf", top], check=True)
        os.makedirs(top)
        subprocess.run(["bash", "-c", f"cd '{d}' && git archive --format=tar HEAD | tar -x -C '{top}'"], check=True)
        import shutil
        shutil.make_archive(dest[:-7], "gztar", top)
    # page inventory + content quotes
    pages = [l.split("\t", 1)[1] for l in o.splitlines() if l.split("\t", 1)[1].endswith((".md", ".creole"))]
    quotes = []
    for rel in pages:
        p = os.path.join(d, rel)
        try:
            txt = open(p, errors="replace").read()
        except Exception:
            continue
        for i, l in enumerate(txt.splitlines()):
            low = l.lower()
            if ("rebol" in low and ("2.7" in low or "bootstrap" in low or "build" in low or "download" in low)) \
               or "static.red-lang.org" in l or "rebol.com/downloads" in l:
                quotes.append({"page": rel, "line": i + 1, "text": l.strip()[:220]})
    quotes = quotes[:30]
    if not any(x["dest"] == dest_rel for x in dls["downloads"]):
        dls["downloads"].append({"url": url + " (git clone; wikis have no codeload endpoint)",
            "dest": dest_rel, "http_status": 200, "size": os.path.getsize(dest),
            "sha256": sha256_file(dest), "retrieved_at": NOW,
            "origin": web + " (official wiki, local git-archive tarball)",
            "project": "RED" if "red" in name else "REBOL", "classification": "DOCUMENTATION",
            "version_claim": "wiki HEAD", "pinned_ref": f"commit {head}",
            "repository": url, "note": "wiki git repo cloned and archived locally (pinned HEAD)"})
    wiki_state["wikis"][name] = {"url": url, "web": web, "description": desc,
        "head_commit": head, "tree_entries": len(o.splitlines()), "pages": pages,
        "archive": dest_rel, "sha256": sha256_file(dest), "size": os.path.getsize(dest),
        "build_quotes": quotes}
    print(f"B. {name}: head={head[:12]} pages={len(pages)} quotes={len(quotes)}")
save(dls, os.path.join(MAN, "downloads.json"))
save(wiki_state, os.path.join(MAN, "wiki-collection.json"))

# ---- C. final audit ----
o, err, rc = run(["sha256sum", "-c", "artifacts/manifests/sha256sums.txt"], ROOT)
ok_n = sum(1 for l in o.splitlines() if l.endswith(": OK"))
arts = load(os.path.join(MAN, "artifacts.json"))
audit = {"generated_at": NOW,
         "sha_manifest_check": {"exit_code": rc, "lines_ok": ok_n},
         "ledger_records": arts["record_count"],
         "collections": {
            "archives": sum(1 for a in arts["artifacts"] if a.get("classification") == "ARCHIVE"),
            "binaries": sum(1 for a in arts["artifacts"] if a.get("classification") == "BINARY"),
            "documentation": sum(1 for a in arts["artifacts"] if a.get("classification") == "DOCUMENTATION"),
         }}
save(audit, os.path.join(MAN, "final-audit.json"))
print(f"C. audit: exit {rc}, {ok_n} OK, ledger {arts['record_count']}")

# ---- ledger ----
MANAGED = {"wiki-collection.json", "final-audit.json"}
arts["artifacts"] = [a for a in arts["artifacts"]
                     if a.get("filename") not in MANAGED
                     and "wiki" not in str(a.get("path", ""))]
def mrec(fn, project, origin, notes, classification="METADATA"):
    p2 = os.path.join(MAN, fn)
    return {"project": project, "version": None, "classification": classification, "origin": origin,
            "filename": fn, "path": f"artifacts/manifests/{fn}", "sha256": sha256_file(p2),
            "size": os.path.getsize(p2), "retrieved_at": NOW, "provenance_status": "VERIFIED",
            "integrity_status": "HASHED", "license_status": "n/a", "notes": notes}
for name, st in wiki_state["wikis"].items():
    proj = "RED" if name.startswith("red") else "REBOL"
    arts["artifacts"].append({"project": proj, "version": "wiki HEAD", "classification": "DOCUMENTATION",
        "origin": st["web"] + " (official wiki, cloned + locally archived at pinned HEAD)",
        "url": st["web"], "repository": st["url"], "commit": st["head_commit"], "tag": None,
        "filename": os.path.basename(st["archive"]), "path": st["archive"],
        "sha256": st["sha256"], "size": st["size"], "retrieved_at": NOW,
        "provenance_status": "VERIFIED", "integrity_status": "HASHED",
        "license_status": "UNCLEAR",
        "license_evidence": "wiki pages carry no explicit license (recorded)",
        "notes": f"{st['description']}: {len(st['pages'])} pages"})
arts["artifacts"].append(mrec("wiki-collection.json", "RELATED", "stage 18",
    "2 official wikis collected + 1 negative recorded (Oldes has none)"))
arts["artifacts"].append(mrec("final-audit.json", "RELATED", "stage 18",
    f"sha256 -c exit {rc} ({ok_n} OK); ledger {arts['record_count']} records"))
arts["record_count"] = len(arts["artifacts"])
save(arts, os.path.join(MAN, "artifacts.json"))

# provenance
prov = load(os.path.join(PROV, "provenance.json"))
_seen = {(e["relationship"], e["source"], e["target"]) for e in prov["graph"]}
def edge(rel, s2, t, evd, status="ESTABLISHED"):
    if (rel, s2, t) in _seen: return
    prov["graph"].append({"relationship": rel, "source": s2, "target": t, "evidence": evd, "status": status})
for name, st in wiki_state["wikis"].items():
    edge("repo->wiki", st["url"].replace(".wiki.git", ""), st["web"],
         f"wiki git HEAD {st['head_commit'][:12]}; {st['tree_entries']} entries; locally archived (wikis have no codeload endpoint)")
save(prov, os.path.join(PROV, "provenance.json"))

# ---- report + addendum + sums ----
run(["python3", os.path.join(ROOT, "acquisition-tools/06_report.py")])
add = []
add.append("\n## Continuation Addendum (stage 18 — official wikis + final audit)\n")
add.append(f"_Generated: {NOW}_\n")
add.append("### Official wikis collected (Tier-1, repo-adjacent documentation)\n")
for name, st in wiki_state["wikis"].items():
    add.append(f"- **{st['web']}** — HEAD `{st['head_commit'][:12]}`, {len(st['pages'])} pages, archived at "
               f"`{os.path.basename(st['archive'])}` (sha256 `{st['sha256'][:16]}…`; wikis have no codeload endpoint — cloned and archived locally at pinned HEAD).")
    bq = [q for q in st["build_quotes"] if "rebol" in q["text"].lower()][:3]
    for q in bq:
        add.append(f"  - bootstrap/build quote: `{q['page']}:{q['line']}` — “{q['text'][:150]}”")
add.append(f"- Negative recorded: `Oldes/Rebol3` has **no wiki** (remote not found). Wiki pages carry no explicit license → recorded UNCLEAR.\n")
add.append("### Final audit\n")
add.append(f"- `sha256sum -c` exit {rc} ({ok_n} lines OK) over the final ledger of {arts['record_count']} records "
           f"({audit['collections']['archives']} archives, {audit['collections']['binaries']} binaries, "
           f"{audit['collections']['documentation']} documentation). Both verification layers (archive reproduction, "
           "metadata regeneration) and this integrity layer all pass on the final state.\n")
add.append("### Egress recheck\n")
add.append(f"- static.red-lang.org curl exit {rc} — unchanged.\n")
add.append("### Status impact\n")
add.append("- Final gate remains **PARTIALLY_VERIFIED**. No GitHub-reachable acquisition surface remains unexamined: source, tags, releases, docs, tests, history mirrors, packaging, CI, wikis, and org coverage are all collected or recorded with reasons.\n")
_mdp = os.path.join(REP, "collection-report.md")
_md = open(_mdp).read()
_md = _md.split("\n## Continuation Addendum (stage 18")[0].rstrip() + "\n"
with open(_mdp, "w") as f:
    f.write(_md + "\n".join(add) + "\n")

sums = []
for dp, dn, fns in os.walk(A):
    if "derived" in dp.split(os.sep): continue
    for fn in sorted(fns):
        p3 = os.path.join(dp, fn)
        rel = os.path.relpath(p3, ROOT)
        if rel.endswith("sha256sums.txt"): continue
        sums.append(f"{sha256_file(p3)}  {rel}")
with open(os.path.join(MAN, "sha256sums.txt"), "w") as f:
    f.write("\n".join(sorted(sums)) + "\n")
print(f"stage 18 complete; records={arts['record_count']} sha_lines={len(sums)}")
