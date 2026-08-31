#!/usr/bin/env python3
"""
Stage 02 — Git collection evidence.
For every cloned repository: remotes, HEAD, describe, commit count, tag->SHA
resolution, and deterministic per-ref file-level tree manifests (git ls-tree).
Also records the workspace fork tree and compares it against upstream v0.6.4.
Output: artifacts/manifests/git-collection.json, artifacts/manifests/trees/*.lsr
"""
import json, os, subprocess, time

ROOT = "/home/user/Red-Cognition-"
ACQ = "/tmp/acq"
MAN = os.path.join(ROOT, "artifacts", "manifests")
TREES = os.path.join(MAN, "trees")
os.makedirs(TREES, exist_ok=True)

def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if p.returncode != 0:
        return None, p.stderr.strip()
    return p.stdout.strip(), None

def log_net(s):
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "tool": "02_git", "event": s}
    with open(os.path.join(ROOT, "artifacts", "logs", "network-events.log"), "a") as f:
        f.write(json.dumps(rec) + "\n")

out = {"collected_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "clone_protocol": "git clone --filter=blob:none --no-checkout (blobless; full commit history, no blob content)",
       "repos": {}}

TARGET_REFS = {
    "red":               ["HEAD", "v0.6.6", "v0.6.4", "v0.7", "v0.6.3"],
    "rebol_rebol":       ["HEAD"],
    "rebolsource_r3":    ["HEAD"],
    "metaeducation_ren-c": ["HEAD"],
    "Oldes_Rebol3":      ["HEAD"],
    "rebolsource_rebol-syntax": ["HEAD"],
    "rebolsource_rebol-test":   ["HEAD"],
}

for name in TARGET_REFS:
    d = os.path.join(ACQ, name)
    print(f"=== {name} ===")
    rec = {"local_clone_path": d, "upstream_url": None}
    o, e = run(["git", "remote", "-v"], d); rec["remotes"] = (o or e)
    rec["upstream_url"] = "https://github.com/%s.git" % name.replace("_", "/", 1) if name != "red" else "https://github.com/red/red.git"
    o, e = run(["git", "rev-parse", "HEAD"], d); rec["head_commit"] = o or f"ERROR: {e}"
    o, e = run(["git", "status", "--short"], d); rec["status_short"] = o if o else "clean"
    o, e = run(["git", "describe", "--tags", "--always"], d); rec["describe"] = o or f"no tags ({e})"
    o, e = run(["git", "rev-list", "--count", "HEAD"], d); rec["commit_count"] = o
    o, e = run(["git", "log", "-1", "--format=%H%n%an <%ae>%n%aI%n%s"], d)
    if o:
        lines = o.split("\n")
        rec["head_commit_detail"] = {"sha": lines[0], "author": lines[1], "date": lines[2], "subject": lines[3]}
    o, e = run(["git", "tag", "-l"], d)
    tags = sorted(o.split("\n")) if o else []
    rec["tag_count"] = len(tags)
    rec["tags"] = tags
    # resolve key tags to immutable SHAs
    rec["tag_resolutions"] = {}
    for t in tags[:80]:  # cap recorded at 80 tags; full list in rec["tags"]
        co, _ = run(["git", "rev-parse", f"{t}^{{commit}}"], d)
        to, _ = run(["git", "rev-parse", f"{t}^{{tree}}"], d)
        rec["tag_resolutions"][t] = {"commit": co, "tree": to}
    if len(tags) > 80:
        rec["tag_resolutions_note"] = f"resolved first 80 of {len(tags)} tags (alphabetical)"
    # per-ref tree manifests
    rec["tree_manifests"] = {}
    for ref in TARGET_REFS[name]:
        o, e = run(["git", "ls-tree", "-r", ref], d)
        if o is None:
            rec["tree_manifests"][ref] = f"ERROR: {e}"
            continue
        n = len(o.splitlines())
        fn = os.path.join(TREES, f"{name}__{ref.replace('/', '_')}.lsr")
        with open(fn, "w") as f:
            f.write(o + "\n")
        rec["tree_manifests"][ref] = {"path": os.path.relpath(fn, ROOT), "entries": n,
                                      "format": "git ls-tree -r <ref> (mode SP type SP blob-sha TAB path)"}
        co, _ = run(["git", "rev-parse", f"{ref}^{{commit}}"], d)
        rec.setdefault("ref_resolutions", {})[ref] = {"commit": co}
    log_net(f"git-evidence recorded for {name}")
    out["repos"][name] = rec
    print(json.dumps({k: rec[k] for k in ("head_commit", "describe", "commit_count", "tag_count")}, indent=1))

# ---- workspace fork tree (the repo this agent runs inside) ----
print("=== workspace fork tree ===")
ws = {"role": "pre-existing working tree of this repository (THIRD_PARTY fork of red/red)"},
rec = {"upstream_url": "https://github.com/Abdus2023/Red-Cognition-.git",
       "head_commit": None}
o, _ = run(["git", "rev-parse", "HEAD"], ROOT); rec["head_commit"] = o
o, _ = run(["git", "status", "--short"], ROOT); rec["status_short"] = o if o else "clean"
o, _ = run(["git", "describe", "--tags", "--always"], ROOT); rec["describe"] = o
o, _ = run(["git", "log", "-1", "--format=%H%n%an <%ae>%n%aI%n%s"], ROOT)
lines = o.split("\n")
rec["head_commit_detail"] = {"sha": lines[0], "author": lines[1], "date": lines[2], "subject": lines[3]}
o, _ = run(["git", "ls-tree", "-r", "HEAD"], ROOT)
fn = os.path.join(TREES, "workspace-fork__HEAD.lsr")
with open(fn, "w") as f:
    f.write(o + "\n")
rec["tree_manifest"] = {"path": os.path.relpath(fn, ROOT), "entries": len(o.splitlines())}
out["repos"]["workspace-fork"] = rec

# ---- fork vs upstream v0.6.4 comparison (blob-sha + path based) ----
def load_lsr(path):
    m = {}
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line: continue
            meta, p = line.split("\t", 1)
            sha = meta.split()[2]
            m[p] = sha
    return m

up = load_lsr(os.path.join(TREES, "red__v0.6.4.lsr"))
ws_map = load_lsr(fn)
red_src_prefixes = ("boot.red", "compiler.r", "lexer.r", "red.r", "run-all.r", "usage.txt", "version.r",
                    "BSD-3-License.txt", "BSL-License.txt", "build/", "bridges/", "compiler/", "dialects/",
                    "docs/", "environment/", "examples/", "libRed/", "modules/", "quick-test/", "runtime/",
                    "specs/", "system/", "tests/", "tools/", "utils/")
up_src = {p: s for p, s in up.items() if p.startswith(red_src_prefixes)}
matched, differing, extra_ws = 0, [], []
for p, s in up_src.items():
    if p in ws_map:
        if ws_map[p] == s: matched += 1
        else: differing.append(p)
    else:
        extra_ws.append(p)
ws_src_only = [p for p in ws_map if p.startswith(red_src_prefixes) and p not in up_src]
cmp_rec = {
    "upstream_ref": "red/red tag v0.6.4", "upstream_commit": out["repos"]["red"]["ref_resolutions"]["v0.6.4"]["commit"],
    "upstream_source_files": len(up_src),
    "workspace_source_files_present_in_upstream": matched,
    "differing_content_files": len(differing), "differing_examples": differing[:20],
    "in_workspace_only": len(ws_src_only), "in_workspace_only_examples": ws_src_only[:20],
    "missing_from_workspace": len(extra_ws), "missing_examples": extra_ws[:20],
    "method": "compared git blob SHA-1 per identical path between workspace HEAD tree and upstream v0.6.4 tree",
}
rec["comparison_to_upstream_v0.6.4"] = cmp_rec
out["workspace_vs_upstream_v0.6.4"] = cmp_rec
print(json.dumps(cmp_rec, indent=1))

with open(os.path.join(MAN, "git-collection.json"), "w") as f:
    json.dump(out, f, indent=2)
print("done")
