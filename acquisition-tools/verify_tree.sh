#!/usr/bin/env bash
# Whole-tree verification: does a stored codeload archive match a pinned git ref?
# usage: verify_tree.sh <clone-dir> <ref> <archive.tar.gz>
set -euo pipefail
CLONE="$1"; REF="$2"; ARCHIVE="$3"
comm -3 \
  <(git -C "$CLONE" -c core.quotepath=false ls-tree -r "$REF" | awk '{print $3"\t"$2}' | sort) \
  <(tar -tzf "$ARCHIVE" | tail -n +2 | sort) >/dev/null && echo "path-set: OK" || echo "path-set: DIFFERS"
python3 - "$CLONE" "$REF" "$ARCHIVE" <<'PY'
import hashlib, subprocess, sys, tarfile
clone, ref, archive = sys.argv[1:4]
ls = {}
out = subprocess.run(["git", "-C", clone, "-c", "core.quotepath=false", "ls-tree", "-r", ref],
                     capture_output=True, text=True).stdout
for line in out.splitlines():
    meta, path = line.split("\t", 1)
    ls[path] = meta.split()[2]
matched = missing = extra = mismatch = 0
with tarfile.open(archive) as tf:
    for m in tf:
        if not m.isfile(): continue
        rel = m.name.split("/", 1)[1]
        data = tf.extractfile(m).read()
        b = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
        if rel not in ls: extra += 1
        elif ls[rel] == b: matched += 1
        else: mismatch += 1
missing = len(ls) - matched - mismatch
print(f"matched={matched} mismatch={mismatch} missing={missing} extra={extra}")
sys.exit(0 if (mismatch == 0 and missing == 0 and extra == 0) else 1)
PY
