#!/usr/bin/env python3
"""
Stage 15 — Official distribution channels + prior-session build products.
 A. Egress probes recorded.
 B. Official-org packaging repos collected: red/Homebrew-red, red/scoop-bucket,
    red/chocolatey-packages (Tier-1) -> archives + tree manifests + reference
    evidence files with quotes (official Red binary URLs; hash policy: :no_check).
 C. Prior-session local build products (zip binaries/: libRedRT.so etc.) recorded
    as UNVERIFIED local-build leads with hashes (NOT upstream artifacts).
 D. Red-org coverage statement (33 repos: collected vs not-collected + reasons).
 E. Recon R7 refresh + R16 (distribution-channel version conflict); ledger;
    provenance; addendum; sums; self-check.
"""
import hashlib, json, os, subprocess, time, urllib.request, zipfile
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common

common.ensure_deps()
ROOT = common.ROOT
A = os.path.join(ROOT, "artifacts")
MAN, PROV, REP, LOGS = (os.path.join(A, d) for d in ("manifests", "provenance", "reports", "logs"))
REFDIR = os.path.join(MAN, "reference-evidence")
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

results = {"generated_at": NOW, "stage": "15"}

# ---- A. probes ----
probes = []
for u in ("http://www.rebol.com/downloads/v278/rebol-core-278-4-2.tar.gz",
          "https://static.red-lang.org/dl/auto/linux/red-latest"):
    _, _, rc = run(["curl", "-s", "-m", "10", "-o", "/dev/null", u])
    probes.append({"url": u, "curl_exit": rc, "result": "NETWORK_BLOCKED" if rc != 0 else "REACHABLE (changed!)"})
results["probes"] = probes
print("A.", [(p["url"][7:40], p["curl_exit"]) for p in probes])

# ---- B. packaging repos ----
PACK = [
    ("red_Homebrew-red", "https://github.com/red/Homebrew-red",
     [("Casks/red-latest.rb", "homebrew-red-latest.rb")], "Homebrew cask for the official mac auto binary"),
    ("red_scoop-bucket", "https://github.com/red/scoop-bucket",
     [("red-latest.json", "scoop-red-latest.json")], "Scoop manifest for the official windows auto binary"),
    ("red_chocolatey-packages", "https://github.com/red/chocolatey-packages",
     [("manual/red/red.nuspec", "chocolatey-manual-red.nuspec"),
      ("automatic/red/red.nuspec", "chocolatey-automatic-red.nuspec"),
      ("automatic/red/build-package.ps1", "chocolatey-build-package.ps1")],
     "Chocolatey packaging (manual pins 0.6.4; automatic is an AU generator embedding binary checksums at publish time)"),
]
dls = load(os.path.join(MAN, "downloads.json"))
pack_state = {"generated_at": NOW, "repos": {}, "official_red_binary_urls": [
    {"platform": "mac", "url": "http://static.red-lang.org/dl/auto/mac/red-latest",
     "declared_by": "red/Homebrew-red Casks/red-latest.rb (official org)", "hash_policy": "sha256 :no_check"},
    {"platform": "win", "url": "http://static.red-lang.org/dl/auto/win/red-latest.exe",
     "declared_by": "red/scoop-bucket red-latest.json (official org)", "hash_policy": "none (manifest has no hash)"},
    {"platform": "linux", "url": "https://static.red-lang.org/dl/auto/linux/red-latest",
     "declared_by": "pattern completion; blocked-probed since stage 1", "hash_policy": "n/a"},
]}
for name, url, extracts, desc in PACK:
    d = os.path.join(common.ACQ, name)
    if not os.path.isdir(os.path.join(d, ".git")):
        subprocess.run(["git", "clone", "--quiet", "--filter=blob:none", "--no-checkout", url + ".git", d], check=True)
    head, _, _ = run(["git", "rev-parse", "HEAD"], d)
    o, _, _ = run(["git", "-c", "core.quotepath=false", "ls-tree", "-r", "HEAD"], d)
    open(os.path.join(MAN, "trees", f"{name}__HEAD.lsr"), "w").write(o + "\n")
    dest_rel = f"artifacts/red/documentation/{name.lower()}-{head[:9]}.tar.gz"
    dest = os.path.join(ROOT, dest_rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if not os.path.exists(dest):
        req = urllib.request.Request(f"https://codeload.github.com/{url.split('github.com/')[1]}/tar.gz/{head}",
                                     headers={"User-Agent": "rebol-red-acquisition-agent/1.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        open(dest, "wb").write(data)
    if not any(x["dest"] == dest_rel for x in dls["downloads"]):
        dls["downloads"].append({"url": f"https://codeload.github.com/{url.split('github.com/')[1]}/tar.gz/{head}",
            "dest": dest_rel, "http_status": 200, "size": os.path.getsize(dest),
            "sha256": sha256_file(dest), "retrieved_at": NOW, "origin": url + " (pinned HEAD archive)",
            "project": "RED", "classification": "ARCHIVE", "version_claim": "master",
            "pinned_ref": f"commit {head}", "repository": url,
            "note": "official Red org packaging/distribution repo"})
    # extract reference files with quotes
    exdir = os.path.join(ROOT, "artifacts", "derived", "extracted", name)
    if not os.path.isdir(exdir) or not os.listdir(exdir):
        import tarfile
        os.makedirs(exdir, exist_ok=True)
        with tarfile.open(dest) as tf:
            tf.extractall(exdir)
    top = common.top_dir(name)
    q_files = []
    for repo_path, out_name in extracts:
        src = os.path.join(top, repo_path)
        if not os.path.exists(src):
            continue
        out = os.path.join(REFDIR, out_name)
        data = open(src, "rb").read()
        open(out, "wb").write(data)
        txt = data.decode(errors="replace")
        quotes = [{"line": i + 1, "text": l.strip()[:220]} for i, l in enumerate(txt.splitlines())
                  if "static.red-lang.org" in l or "<version>" in l or "sha256" in l.lower()
                  or "checksum" in l.lower() or "0.6." in l]
        q_files.append({"file": out_name, "source_path": repo_path, "sha256": hashlib.sha256(data).hexdigest(),
                        "quotes": quotes[:8]})
    pack_state["repos"][name] = {"repo": url, "head_commit": head, "tree_entries": len(o.splitlines()),
                                 "archive": dest_rel, "sha256": sha256_file(dest),
                                 "size": os.path.getsize(dest), "description": desc,
                                 "reference_files": q_files}
    print(f"B. {name}: head={head[:12]} refs={len(q_files)}")
save(dls, os.path.join(MAN, "downloads.json"))
save(pack_state, os.path.join(MAN, "red-distribution-channels.json"))

# ---- C. prior-session build products ----
zpath = os.path.join(ROOT, "artifacts", "archives", "red-cognition-test-artifacts.zip")
pdest = os.path.join(ROOT, "artifacts", "derived", "from-previous-session")
os.makedirs(pdest, exist_ok=True)
products = []
with zipfile.ZipFile(zpath) as z:
    for n in z.namelist():
        if n.startswith("red-cognition-test-artifacts/binaries/") and not n.endswith("/"):
            data = z.read(n)
            rel = n.split("binaries/", 1)[1]
            out = os.path.join(pdest, "binaries", rel)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, "wb").write(data)
            products.append({"file": rel, "sha256": hashlib.sha256(data).hexdigest(),
                             "size": len(data)})
prod_rec = {"generated_at": NOW,
            "role": ("prior-session LOCAL BUILD products (embedded logs show a bootstrap/test run at commit "
                     "f860bbe on 2026-08-30, image red-cognition/rebol-bootstrap:2.7.8) — NOT upstream artifacts; "
                     "provenance UNVERIFIED (prior session, no reproducible link to this tree's commits)"),
            "container_zip_sha256": sha256_file(zpath), "products": products,
            "note": "preserved unchanged in derived/; libRedRT.so is a Red compilation byproduct (evidence of a prior bootstrap EXECUTION by the prior session, not by this agent)"}
save(prod_rec, os.path.join(MAN, "previous-session-build-products.json"))
print(f"C. prior-session build products: {len(products)} files hashed")

# ---- D. org coverage statement ----
disc = load(os.path.join(MAN, "github-discovery.json"))
org_repos = disc.get("red_org_repos") or []
COLLECTED = {
    "red/red": "official language/toolchain source + releases",
    "red/REP": "official enhancement proposals",
    "red/docs": "official user documentation",
    "red/RS-fossil-mirror": "pre-GitHub Fossil history mirrors (Tier-2)",
    "red/Homebrew-red": "official mac distribution channel",
    "red/scoop-bucket": "official windows distribution channel",
    "red/chocolatey-packages": "official windows package channel",
    "red/web-red": "official website source (reference evidence only)",
}
SKIP_REASON = "ecosystem/application material (wallets, editors, demos, promotion, web framework) — outside the toolchain/bootstrap acquisition scope"
coverage = {"generated_at": NOW, "org": "red (GitHub org)", "total_repos": len(org_repos),
            "collected": [{"repo": k, "reason": v} for k, v in COLLECTED.items() if k in org_repos or k == "red/red"],
            "not_collected": [{"repo": r, "reason": SKIP_REASON} for r in org_repos
                              if r not in COLLECTED and r != "red/red"],
            "note": "scope statement: language/toolchain/bootstrap/distribution material collected; end-user ecosystem apps not collected (leads preserved in github-discovery.json)"}
save(coverage, os.path.join(MAN, "red-org-coverage.json"))
print(f"D. org coverage: {len(coverage['collected'])} collected / {len(coverage['not_collected'])} out-of-scope")

# ---- ledger ----
arts = load(os.path.join(MAN, "artifacts.json"))
MANAGED = {"red-distribution-channels.json", "previous-session-build-products.json",
           "red-org-coverage.json"}
arts["artifacts"] = [a for a in arts["artifacts"]
                     if a.get("filename") not in MANAGED
                     and not str(a.get("path", "")).startswith(("artifacts/red/documentation/red_homebrew",
                                                                "artifacts/red/documentation/red_scoop",
                                                                "artifacts/red/documentation/red_chocolatey",
                                                                "artifacts/manifests/reference-evidence/homebrew",
                                                                "artifacts/manifests/reference-evidence/scoop",
                                                                "artifacts/manifests/reference-evidence/chocolatey"))]
def mrec(fn, project, origin, notes, classification="METADATA", path=None):
    p2 = os.path.join(ROOT, path or f"artifacts/manifests/{fn}")
    return {"project": project, "version": None, "classification": classification, "origin": origin,
            "filename": fn, "path": path or f"artifacts/manifests/{fn}", "sha256": sha256_file(p2),
            "size": os.path.getsize(p2), "retrieved_at": NOW, "provenance_status": "VERIFIED",
            "integrity_status": "HASHED", "license_status": "n/a", "notes": notes}
for name, st in pack_state["repos"].items():
    arts["artifacts"].append({"project": "RED", "version": "master", "classification": "ARCHIVE",
        "origin": st["repo"] + " (official Red org packaging repo, pinned HEAD archive)",
        "url": st["repo"], "repository": st["repo"], "commit": st["head_commit"], "tag": None,
        "filename": os.path.basename(st["archive"]), "path": st["archive"],
        "sha256": st["sha256"], "size": st["size"], "retrieved_at": NOW,
        "provenance_status": "VERIFIED", "integrity_status": "HASHED",
        "license_status": "n/a",
        "notes": st["description"]})
    for rf in st["reference_files"]:
        arts["artifacts"].append(mrec(rf["file"], "RED",
            f"{st['repo']} :: {rf['source_path']} (official org packaging definition)",
            "quotes: " + "; ".join(q["text"][:60] for q in rf["quotes"][:2]),
            classification="DOCUMENTATION",
            path=f"artifacts/manifests/reference-evidence/{rf['file']}"))
arts["artifacts"].append(mrec("red-distribution-channels.json", "RED",
    "stage 15 registry", "official Red binary URLs (mac/win/linux) + hash policies from org packaging repos"))
arts["artifacts"].append(mrec("previous-session-build-products.json", "RED",
    "stage 15 archival of prior-session zip content",
    f"{len(products)} local-build products (libRedRT.so etc.) — UNVERIFIED provenance, preserved in derived/"))
arts["artifacts"].append(mrec("red-org-coverage.json", "RELATED",
    "stage 15 scope statement", f"{coverage['total_repos']} org repos: {len(coverage['collected'])} collected, {len(coverage['not_collected'])} documented out-of-scope"))
arts["record_count"] = len(arts["artifacts"])
save(arts, os.path.join(MAN, "artifacts.json"))

# ---- provenance ----
prov = load(os.path.join(PROV, "provenance.json"))
_seen = {(e["relationship"], e["source"], e["target"]) for e in prov["graph"]}
def edge(rel, s2, t, evd, status="ESTABLISHED"):
    if (rel, s2, t) in _seen: return
    prov["graph"].append({"relationship": rel, "source": s2, "target": t, "evidence": evd, "status": status})
edge("distribution-channel", "official Red org packaging repos (Homebrew/scoop/chocolatey)",
     "official binary URLs static.red-lang.org/dl/auto/{mac,win,linux}",
     "official-org-authored cask/manifest/nuspec pin the auto-binary URLs; hash policy :no_check / none (manifests/red-distribution-channels.json)")
edge("prior-session-builds", "prior session (zip binaries/, commit f860bbe era)", "libRedRT.so + support files",
     "LOCAL BUILD products, UNVERIFIED; preserved with hashes; NOT upstream artifacts", status="PARTIAL")
save(prov, os.path.join(PROV, "provenance.json"))

# ---- reconciliation ----
recon = load(os.path.join(PROV, "reconciliation.json"))
recon["tables"] = [t for t in recon["tables"] if t["id"] not in ("R16",)]
r7 = next(t for t in recon["tables"] if t["id"] == "R7")
r7["rows"].append(["Official binary URLs", "static.red-lang.org/dl/auto/{mac,win,linux} pinned by official org packaging repos", "hash policy: :no_check (homebrew) / none (scoop) / checksum added at chocolatey publish time", "RECORDED (no public reference hash found for Red binaries in any collected source)"])
recon["tables"].append({"id": "R16", "artifact": "Red distribution-channel versions",
  "rows": [
   ["GitHub release", "0.6.6 (2025-03-19)", "-", "REFERENCE"],
   ["chocolatey (manual package)", "0.6.4 (nuspec <version>)", "lags latest release by one version", "CONFLICT (distribution lag; recorded)"],
   ["homebrew / scoop", "version :latest / \"nightly\" (auto binaries)", "track the auto builds, not releases", "NOTED"],
   ["nixpkgs", "0.6.4 (package.nix version + pinned commit)", "matches our v0.6.4 commit exactly", "MATCH (to v0.6.4)"],
   ["bootstrap claim", "chocolatey nuspec repeats the Rebol2-bootstrap wording verbatim", "same claim as red/red READMEs", "MATCH (independent channel, identical claim)"],
  ]})
save(recon, os.path.join(PROV, "reconciliation.json"))

# ---- report + addendum + sums ----
run(["python3", os.path.join(ROOT, "acquisition-tools/06_report.py")])
add = []
add.append("\n## Continuation Addendum (stage 15)\n")
add.append(f"_Generated: {NOW}_\n")
add.append("### Official distribution channels collected (recon R7 refresh + R16)\n")
add.append("- **red/Homebrew-red, red/scoop-bucket, red/chocolatey-packages** archived (Tier-1 org repos) with their definitions extracted as reference evidence.")
add.append("- Official Red binary URLs pinned by the org itself: `static.red-lang.org/dl/auto/mac/red-latest`, `…/win/red-latest.exe`, `…/linux/red-latest`. **Hash policy finding:** homebrew uses `sha256 :no_check`, scoop has no hash, chocolatey embeds the checksum only at publish time (chocolatey.org itself is blocked) — **no public reference hash exists for Red binaries in any collected source**; first-download hashing will be the original verification.")
add.append("- **Distribution-lag conflict (R16):** chocolatey manual package pins **0.6.4** while the latest release is 0.6.6; homebrew/scoop track nightlies; nixpkgs pins 0.6.4 (commit MATCH). The nuspec also repeats the Rebol2-bootstrap claim verbatim — independent-channel confirmation.\n")
add.append("### Prior-session build products archived (leads, not evidence)\n")
add.append(f"- {len(products)} files from the repo zip's `binaries/` (libRedRT.so, checkum-repro, …) hashed and preserved in `derived/`: **LOCAL BUILD products** of the prior session (its logs show commit f860bbe, image red-cognition/rebol-bootstrap:2.7.8) — NOT upstream artifacts; provenance UNVERIFIED.\n")
add.append("### Red-org coverage statement\n")
add.append(f"- {coverage['total_repos']} org repos: **{len(coverage['collected'])} collected** (language, docs, proposals, history, distribution), **{len(coverage['not_collected'])} documented out-of-scope** (end-user ecosystem apps; leads preserved in `manifests/github-discovery.json`).\n")
add.append("### Egress recheck\n")
add.append("; ".join(f"`{p['url']}` → curl exit {p['curl_exit']} ({'blocked' if p['curl_exit'] != 0 else 'REACHABLE'})" for p in probes) + "\n")
add.append("### Status impact\n")
add.append("- Final gate remains **PARTIALLY_VERIFIED**. The distribution-channel layer of the Red ecosystem is now fully documented with pinned evidence.\n")
_mdp = os.path.join(REP, "collection-report.md")
_md = open(_mdp).read()
_md = _md.split("\n## Continuation Addendum (stage 15)\n")[0].rstrip() + "\n"
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
print(f"stage 15 complete; records={arts['record_count']} sha_lines={len(sums)}")
