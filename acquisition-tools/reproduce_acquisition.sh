#!/usr/bin/env bash
# reproduce_acquisition.sh — one-shot re-derivation of this acquisition from GitHub.
# Re-clones every repository, re-downloads every pinned archive, and whole-tree
# verifies each against its pinned ref (git blob SHA-1 of every archive member).
# Requires: git, python3, network access to github.com + codeload.github.com.
# Usage: WORK=/tmp/acq-reproduce ./reproduce_acquisition.sh
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="${WORK:-/tmp/acq-reproduce}"
mkdir -p "$WORK"

CLONES=(
  "https://github.com/red/red.git"
  "https://github.com/rebol/rebol.git"
  "https://github.com/rebolsource/r3.git"
  "https://github.com/metaeducation/ren-c.git"
  "https://github.com/Oldes/Rebol3.git"
  "https://github.com/rebolsource/rebol-syntax.git"
  "https://github.com/rebolsource/rebol-test.git"
  "https://github.com/rebol/projects.git"
  "https://github.com/red/REP.git"
  "https://github.com/red/docs.git"
)

# repo|ref   (tag names get refs/tags/; anything else is treated as a commit SHA or HEAD)
ARCHIVES="
red/red|v0.6.6
red/red|v0.6.5
red/red|v0.6.4
red/red|v0.6.3
red/red|v0.6.2
red/red|v0.6.1
red/red|v0.6.0
red/red|v0.5.4
red/red|v0.4.3
red/red|v0.3.3
red/red|v0.2.6
red/red|v0.1.1
rebol/rebol|25033f897b2bd466068d7663563cd3ff64740b94
rebolsource/r3|98cdfcd6e439390756868b390b0ff8aa01d84551
metaeducation/ren-c|e31d5698d73678d797df319eb855b3995716d9f1
Oldes/Rebol3|d5b237cea60d06b72c59bb6dbed0022b482f4c57
Oldes/Rebol3|3.22.1
rebolsource/rebol-syntax|4ff11396312d0ccd8490191571206f628be79e8e
rebolsource/rebol-test|409ef5c2270a766a6262d883e6fc5ea9d1ec6234
rebol/projects|HEAD
red/REP|HEAD
red/docs|HEAD
"

echo "== cloning =="
for url in "${CLONES[@]}"; do
  name="$(basename "$url" .git)"
  [ -d "$WORK/$name/.git" ] || git clone --quiet --filter=blob:none --no-checkout "$url" "$WORK/$name"
done

echo "== downloading + whole-tree verifying 22 archives =="
export WORK
python3 - <<'PY'
import hashlib, io, os, subprocess, sys, tarfile, urllib.request

work = os.environ["WORK"]
SPECS = """red/red|v0.6.6
red/red|v0.6.5
red/red|v0.6.4
red/red|v0.6.3
red/red|v0.6.2
red/red|v0.6.1
red/red|v0.6.0
red/red|v0.5.4
red/red|v0.4.3
red/red|v0.3.3
red/red|v0.2.6
red/red|v0.1.1
rebol/rebol|25033f897b2bd466068d7663563cd3ff64740b94
rebolsource/r3|98cdfcd6e439390756868b390b0ff8aa01d84551
metaeducation/ren-c|e31d5698d73678d797df319eb855b3995716d9f1
Oldes/Rebol3|d5b237cea60d06b72c59bb6dbed0022b482f4c57
Oldes/Rebol3|3.22.1
rebolsource/rebol-syntax|4ff11396312d0ccd8490191571206f628be79e8e
rebolsource/rebol-test|409ef5c2270a766a6262d883e6fc5ea9d1ec6234
rebol/projects|HEAD
red/REP|HEAD
red/docs|HEAD""".splitlines()

ok = bad = 0
for spec in SPECS:
    repo, ref = spec.strip().split("|", 1)
    clone = os.path.join(work, repo.split("/")[-1])
    codeload_ref = "refs/tags/" + ref if ref.startswith("v") else ref
    url = f"https://codeload.github.com/{repo}/tar.gz/{codeload_ref}"
    pin = ref
    if ref == "HEAD":
        pin = subprocess.run(["git", "-C", clone, "rev-parse", "HEAD"],
                             capture_output=True, text=True).stdout.strip()
    ls = {}
    out = subprocess.run(["git", "-C", clone, "-c", "core.quotepath=false",
                          "ls-tree", "-r", pin], capture_output=True, text=True).stdout
    for line in out.splitlines():
        meta, path = line.split("\t", 1)
        ls[path] = meta.split()[2]
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "acquisition-reproduce/1.0"})
        data = urllib.request.urlopen(req, timeout=300).read()
    except Exception as e:
        print("FAIL", repo, ref, "->", e)
        bad += 1
        continue
    matched = extra = mismatch = 0
    with tarfile.open(fileobj=io.BytesIO(data)) as tf:
        for m in tf:
            if not m.isfile():
                continue
            rel = m.name.split("/", 1)[1]
            b = tf.extractfile(m).read()
            h = hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()
            if rel not in ls:
                extra += 1
            elif ls[rel] == h:
                matched += 1
            else:
                mismatch += 1
    missing = len(ls) - matched - mismatch
    good = mismatch == missing == extra == 0
    ok += good
    bad += (not good)
    print(("OK  " if good else "FAIL"), repo, ref, f"({matched}/{len(ls)}) sha256={hashlib.sha256(data).hexdigest()}")

print(f"\nverified: {ok} ok, {bad} failed")
sys.exit(1 if bad else 0)
PY
echo "done."
