#!/usr/bin/env python3
"""
Stage 03 — Download stage.
All downloads pinned to immutable refs (tag or full commit SHA).
 - Source/release archives via codeload.github.com (allowed egress)
 - Small binary test fixtures via api.github.com git/contents + git/blobs
Every download is logged; originals are stored byte-for-byte; SHA-256 computed.
Output: artifacts/manifests/downloads.json
"""
import base64, hashlib, json, os, subprocess, time, urllib.request, urllib.error

ROOT = "/home/user/Red-Cognition-"
LOGS = os.path.join(ROOT, "artifacts", "logs")
MAN = os.path.join(ROOT, "artifacts", "manifests")
TOKEN = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()

def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def log_net(rec):
    rec = {"ts": now(), **rec}
    with open(os.path.join(LOGS, "network-events.log"), "a") as f:
        f.write(json.dumps(rec) + "\n")

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

results = {"collected_at": now(), "downloads": [], "failures": []}

def download(url, dest, origin, meta):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {TOKEN}" if "api.github.com" in url else "AcquisitionAgent/1.0",
        "User-Agent": "rebol-red-acquisition-agent/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        with open(dest, "wb") as f:
            f.write(data)
        entry = {"url": url, "dest": os.path.relpath(dest, ROOT), "http_status": 200,
                 "size": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                 "sha1": hashlib.sha1(data).hexdigest(), "retrieved_at": now(),
                 "origin": origin, **meta}
        results["downloads"].append(entry)
        log_net({"url": url, "http_status": 200, "size": len(data), "action": "download"})
        print(f"OK  {dest} ({len(data)} bytes)")
    except urllib.error.HTTPError as e:
        results["failures"].append({"url": url, "http_status": e.code, "reason": e.reason,
                                    "status": "FETCH_FAILED", "attempted_at": now()})
        log_net({"url": url, "http_status": e.code, "action": "download-failed"})
        print(f"FAIL {url} -> HTTP {e.code}")
    except Exception as e:
        results["failures"].append({"url": url, "http_status": None, "reason": str(e),
                                    "status": "NETWORK_BLOCKED", "attempted_at": now()})
        log_net({"url": url, "http_status": "ERROR", "detail": str(e), "action": "download-failed"})
        print(f"FAIL {url} -> {e}")

# ---- pinned archives via codeload (git ref = full commit SHA or tag) ----
ARCHIVES = [
    # (url_ref, dest, origin, project, classification, version_claim, pinned_ref, repo)
    ("https://codeload.github.com/red/red/tar.gz/refs/tags/v0.6.6",
     "artifacts/red/releases/red-0.6.6.tar.gz",
     "https://github.com/red/red (GitHub auto-generated tag archive, codeload)",
     "RED", "ARCHIVE", "0.6.6", "tag v0.6.6 -> commit 6942c7a021253150c3e3cf90428305892340db03", "red/red"),
    ("https://codeload.github.com/red/red/tar.gz/refs/tags/v0.6.4",
     "artifacts/red/releases/red-0.6.4.tar.gz",
     "https://github.com/red/red (GitHub auto-generated tag archive, codeload)",
     "RED", "ARCHIVE", "0.6.4", "tag v0.6.4 -> commit 755eb943ccea9e78c2cab0f20b313a52404355cb", "red/red"),
    ("https://codeload.github.com/rebol/rebol/tar.gz/25033f897b2bd466068d7663563cd3ff64740b94",
     "artifacts/rebol/source/rebol-rebol-25033f897.tar.gz",
     "https://github.com/rebol/rebol (official R3 source, pinned to master HEAD at acquisition time)",
     "REBOL", "ARCHIVE", "R3 master", "commit 25033f897b2bd466068d7663563cd3ff64740b94", "rebol/rebol"),
    ("https://codeload.github.com/metaeducation/ren-c/tar.gz/e31d5698d73678d797df319eb855b3995716d9f1",
     "artifacts/rebol/source/ren-c-e31d5698d.tar.gz",
     "https://github.com/metaeducation/ren-c (Ren-C continuation fork of rebolsource/r3) - THIRD_PARTY relative to rebol.com",
     "REBOL", "ARCHIVE", "ren-c master", "commit e31d5698d73678d797df319eb855b3995716d9f1", "metaeducation/ren-c"),
    ("https://codeload.github.com/rebolsource/r3/tar.gz/98cdfcd6e439390756868b390b0ff8aa01d84551",
     "artifacts/rebol/source/rebolsource-r3-98cdfcd6e.tar.gz",
     "https://github.com/rebolsource/r3 (historical R3 source host, pre-ren-c) - Tier 2 historical",
     "REBOL", "ARCHIVE", "R3 (rebolsource)", "commit 98cdfcd6e439390756868b390b0ff8aa01d84551", "rebolsource/r3"),
    ("https://codeload.github.com/Oldes/Rebol3/tar.gz/d5b237cea60d06b72c59bb6dbed0022b482f4c57",
     "artifacts/rebol/source/Oldes-Rebol3-d5b237cea.tar.gz",
     "https://github.com/Oldes/Rebol3 (independent R3 fork with extended features) - THIRD_PARTY",
     "REBOL", "ARCHIVE", "3.22.1-44-gd5b237ce", "commit d5b237cea60d06b72c59bb6dbed0022b482f4c57", "Oldes/Rebol3"),
    ("https://codeload.github.com/rebolsource/rebol-syntax/tar.gz/4ff11396312d0ccd8490191571206f628be79e8e",
     "artifacts/rebol/documentation/rebol-syntax-4ff113963.tar.gz",
     "https://github.com/rebolsource/rebol-syntax (formal Rebol syntax specification) - Tier 2 historical",
     "REBOL", "DOCUMENTATION", "master", "commit 4ff11396312d0ccd8490191571206f628be79e8e", "rebolsource/rebol-syntax"),
    ("https://codeload.github.com/rebolsource/rebol-test/tar.gz/409ef5c2270a766a6262d883e6fc5ea9d1ec6234",
     "artifacts/rebol/tests/rebol-test-409ef5c22.tar.gz",
     "https://github.com/rebolsource/rebol-test (official Rebol regression test suite) - Tier 2 historical",
     "REBOL", "TEST_SUITE", "master", "commit 409ef5c2270a766a6262d883e6fc5ea9d1ec6234", "rebolsource/rebol-test"),
]
for url, dest, origin, project, cls, ver, ref, repo in ARCHIVES:
    download(url, os.path.join(ROOT, dest), origin,
             {"project": project, "classification": cls, "version_claim": ver,
              "pinned_ref": ref, "repository": f"https://github.com/{repo}"})

# ---- small binary test fixtures from red/red @ v0.6.6 via contents API ----
FIXTURES = [
    ("tests/libRed/libRed.dll", "artifacts/red/tests/libRed-v0.6.6/libRed.dll"),
    ("system/tests/source/units/libs/libstructlib.so", "artifacts/red/tests/libstruct-v0.6.6/libstructlib.so"),
    ("system/tests/source/units/libs/structlib.dll", "artifacts/red/tests/libstruct-v0.6.6/structlib.dll"),
]
for path, dest in FIXTURES:
    api = f"https://api.github.com/repos/red/red/contents/{path}?ref=v0.6.6"
    req = urllib.request.Request(api, headers={
        "Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json",
        "User-Agent": "rebol-red-acquisition-agent/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            meta = json.loads(r.read())
        blob_sha = meta.get("sha")
        size = meta.get("size")
        if size is not None and size > 1_000_000:
            # contents API caps at 1MB -> use git/blobs endpoint (also api.github.com)
            bapi = f"https://api.github.com/repos/red/red/git/blobs/{blob_sha}"
            req2 = urllib.request.Request(bapi, headers={
                "Authorization": f"token {TOKEN}", "User-Agent": "rebol-red-acquisition-agent/1.0"})
            with urllib.request.urlopen(req2, timeout=120) as r2:
                bmeta = json.loads(r2.read())
            data = base64.b64decode(bmeta["content"])
        else:
            data = base64.b64decode(meta["content"])
        full = os.path.join(ROOT, dest)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as f:
            f.write(data)
        results["downloads"].append({
            "url": api, "dest": dest, "http_status": 200, "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "sha1": hashlib.sha1(data).hexdigest(), "retrieved_at": now(),
            "origin": "https://github.com/red/red blob (via api.github.com)",
            "project": "RED", "classification": "BINARY",
            "version_claim": "0.6.6", "pinned_ref": "tag v0.6.6 -> commit 6942c7a021253150c3e3cf90428305892340db03",
            "repository": "https://github.com/red/red", "git_blob_sha1": blob_sha,
            "role": "test fixture (prebuilt test-support binary shipped in upstream tree)"})
        log_net({"url": api, "http_status": 200, "size": len(data), "action": "blob-download"})
        print(f"OK  {dest} ({len(data)} bytes, blob {blob_sha[:12]})")
    except Exception as e:
        results["failures"].append({"url": api, "reason": str(e), "status": "FETCH_FAILED", "attempted_at": now()})
        print(f"FAIL {path}: {e}")

# ---- cross-check: git blob sha1 recorded must equal 'git hash-object' of stored bytes ----
for d in results["downloads"]:
    if "git_blob_sha1" in d:
        p = os.path.join(ROOT, d["dest"])
        o = subprocess.run(["git", "hash-object", p], capture_output=True, text=True).stdout.strip()
        d["git_hash_object_check"] = {"computed": o, "expected": d["git_blob_sha1"],
                                      "match": o == d["git_blob_sha1"]}
        print(f"blob-integrity {d['dest']}: match={o == d['git_blob_sha1']}")

with open(os.path.join(MAN, "downloads.json"), "w") as f:
    json.dump(results, f, indent=2)
print(f"\ndownloads={len(results['downloads'])} failures={len(results['failures'])}")
