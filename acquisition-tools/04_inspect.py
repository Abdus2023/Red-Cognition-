#!/usr/bin/env python3
"""
Stage 04 — Derived inspection (originals untouched; extraction into artifacts/derived/).
 - extract each archive copy into artifacts/derived/extracted/
 - record version claims (content of version files) and license evidence
 - ELF-class check of the prior-session rebol-2.7.8 lead (untrusted)
Output: artifacts/manifests/source-inspection.json
"""
import hashlib, json, os, shutil, subprocess, tarfile, time

ROOT = "/home/user/Red-Cognition-"
DER = os.path.join(ROOT, "artifacts", "derived", "extracted")
MAN = os.path.join(ROOT, "artifacts", "manifests")

def now(): return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()

def find(names, base):
    out = []
    for dirpath, dirnames, filenames in os.walk(base):
        for fn in filenames:
            if fn.lower() in names: out.append(os.path.join(dirpath, fn))
    return out

def head(p, n=4):
    try:
        with open(p, "r", errors="replace") as f: return "".join([next(f, "") for _ in range(n)]).strip()[:400]
    except Exception as e: return f"<unreadable: {e}>"

out = {"collected_at": now(), "archives": []}

ARCHIVES = [
    ("red-0.6.6", "artifacts/red/releases/red-0.6.6.tar.gz", "RED",
     ["version.r"], ["license", "license.txt", "bsl-license.txt", "bsd-3-license.txt", "copying", "readme.md"]),
    ("red-0.6.4", "artifacts/red/releases/red-0.6.4.tar.gz", "RED",
     ["version.r"], ["license", "license.txt", "bsl-license.txt", "bsd-3-license.txt", "copying", "readme.md"]),
    ("rebol-rebol-25033f897", "artifacts/rebol/source/rebol-rebol-25033f897.tar.gz", "REBOL",
     ["version.r", "version", "version.h"], ["license", "copying", "readme.md"]),
    ("ren-c-e31d5698d", "artifacts/rebol/source/ren-c-e31d5698d.tar.gz", "REBOL",
     ["version.r", "version"], ["license", "copying", "readme.md"]),
    ("rebolsource-r3-98cdfcd6e", "artifacts/rebol/source/rebolsource-r3-98cdfcd6e.tar.gz", "REBOL",
     ["version.r", "version"], ["license", "copying", "readme.md"]),
    ("Oldes-Rebol3-d5b237cea", "artifacts/rebol/source/Oldes-Rebol3-d5b237cea.tar.gz", "REBOL",
     ["version.r", "version"], ["license", "copying", "readme.md"]),
    ("rebol-syntax-4ff113963", "artifacts/rebol/documentation/rebol-syntax-4ff113963.tar.gz", "REBOL",
     [], ["license", "copying", "readme.md"]),
    ("rebol-test-409ef5c22", "artifacts/rebol/tests/rebol-test-409ef5c22.tar.gz", "REBOL",
     [], ["license", "copying", "readme.md"]),
]

for name, arel, project, version_files, license_files in ARCHIVES:
    src = os.path.join(ROOT, arel)
    dest = os.path.join(DER, name)
    rec = {"archive": arel, "archive_sha256": sha256_file(src), "project": project,
           "extracted_to": os.path.relpath(dest, ROOT), "extracted_at": now(),
           "note": "extraction is a derived copy for inspection; preserved archive above is the acquisition original"}
    os.makedirs(dest, exist_ok=True)
    with tarfile.open(src, "r:gz") as tf:
        tf.extractall(dest)
    members = os.listdir(dest)
    rec["top_level"] = members
    top = os.path.join(dest, members[0]) if len(members) == 1 else dest
    # bootstrap-relevant build files present in red trees
    if project == "RED":
        build_marks = {}
        for rel in ["red.r", "compiler.r", "lexer.r", "build/build.md", "build/README.md", "quick-test/run-all.r", "run-all.r"]:
            p = os.path.join(top, rel)
            build_marks[rel] = {"present": os.path.exists(p),
                                "sha256": sha256_file(p) if os.path.exists(p) else None,
                                "size": os.path.getsize(p) if os.path.exists(p) else None}
        rec["bootstrap_build_files"] = build_marks
    vf = {fn.lower() for fn in version_files}
    rec["version_evidence"] = []
    for p in find(vf, top):
        rec["version_evidence"].append({"path": os.path.relpath(p, top), "content": head(p, 6)[:400],
                                        "sha256": sha256_file(p)})
    lf = {fn.lower() for fn in license_files}
    rec["license_evidence"] = []
    for p in find(lf, top):
        rec["license_evidence"].append({"path": os.path.relpath(p, top), "sha256": sha256_file(p),
                                        "size": os.path.getsize(p), "head": head(p, 3)})
    # count files
    n = sum(len(fs) for _, _, fs in os.walk(top))
    rec["file_count"] = n
    out["archives"].append(rec)
    print(f"{name}: files={n} version_evidence={len(rec['version_evidence'])} license_evidence={len(rec['license_evidence'])}")
    for v in rec.get("version_evidence", [])[:3]:
        print("   version:", v["path"], "=", " | ".join(v["content"].split("\n")[:2])[:120])
    for l in rec.get("license_evidence", [])[:3]:
        print("   license:", l["path"], l["sha256"][:16], repr(l["head"][:80]))

# ---- prior-session rebol-2.7.8 lead (UNTRUSTED origin) ----
lead = {"role": "prior-session artifact found inside repo zip artifacts/archives/red-cognition-test-artifacts.zip; "
               "no acquisition URL recorded -> provenance UNKNOWN", "provenance_status": "UNVERIFIED"}
zpath = os.path.join(ROOT, "artifacts", "archives", "red-cognition-test-artifacts.zip")
lead["container_zip_sha256"] = sha256_file(zpath)
dest = os.path.join(ROOT, "artifacts", "derived", "from-previous-session")
os.makedirs(dest, exist_ok=True)
subprocess.run(["unzip", "-q", "-o", zpath, "red-cognition-test-artifacts/downloaded/*", "-d", dest], check=True)
p = os.path.join(dest, "red-cognition-test-artifacts", "downloaded", "rebol-2.7.8")
lead["sha256"] = sha256_file(p)
lead["size"] = os.path.getsize(p)
with open(p, "rb") as f: hdr = f.read(20)
lead["elf"] = {"magic": hdr[:4].decode(errors="replace"), "class": {1: "ELF32", 2: "ELF64"}.get(hdr[4], str(hdr[4])),
               "endian": {1: "LE", 2: "BE"}.get(hdr[5], str(hdr[5]))}
lead["execution_feasibility"] = "ELF32 on x86_64-only host without i386 loader -> execution NOT attempted" if hdr[4] == 1 else "ELF64 - could be executed"
out["previous_session_lead"] = lead
print("lead:", json.dumps(lead["elf"]), lead["sha256"][:16])

with open(os.path.join(MAN, "source-inspection.json"), "w") as f:
    json.dump(out, f, indent=2)
print("done")
