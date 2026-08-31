#!/usr/bin/env python3
"""
Stage 17 — Forensic identification sweep (static analysis only; no execution).
 A. Egress: formal attempt on the upstream-CI bootstrap URL static.red-lang.org/tmp/rebol.
 B. Lead binary identification: embedded banner extraction (ELF header + strings).
 C. Fixture binaries: header identification (PE machine / ELF class+machine).
 D. Verification path for the lead recorded (compare vs official 278-4-3 tarball
    binary once rebol.com is reachable; tarball identity hashes already on file
    for 4-2; 4-3 tarball is the exact build the banner claims).
 Ledger (lead record upgraded with embedded_identification), provenance,
 addendum, sums, self-check.
"""
import hashlib, json, os, re, subprocess, time
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

# ---- A. CI bootstrap URL attempt ----
URL = "https://static.red-lang.org/tmp/rebol"
_, _, rc = run(["curl", "-s", "-m", "15", "-o", "/dev/null", URL])
with open(os.path.join(LOGS, "execution", "blocked-static-red-lang-org-tmp-rebol.log"), "w") as f:
    f.write(f"attempt: {URL} (upstream CI bootstrap URL, red/red v0.6.4 .travis.yml:89)\n"
            f"date: {NOW}\ncurl exit: {rc}\n")
bl = load(os.path.join(A, "logs", "blocked-attempts.json"))
if not any(a["url"] == URL for a in bl["attempts"]):
    bl["attempts"].append({"url": URL,
        "purpose": "REBOL interpreter used by official Red CI (v0.6.4 .travis.yml:89)",
        "result": "NETWORK_BLOCKED" if rc != 0 else "REACHABLE (changed!)",
        "detail": f"curl exit {rc}", "attempted_at": NOW})
save(bl, os.path.join(A, "logs", "blocked-attempts.json"))
print(f"A. CI bootstrap URL: exit {rc}")

# ---- B. lead identification ----
lead_zip = os.path.join(ROOT, "artifacts", "archives", "red-cognition-test-artifacts.zip")
lead_rel = "artifacts/derived/from-previous-session/red-cognition-test-artifacts/downloaded/rebol-2.7.8"
lead_path = os.path.join(ROOT, lead_rel)
if not os.path.exists(lead_path):
    run(["unzip", "-q", "-o", lead_zip, "red-cognition-test-artifacts/downloaded/*",
         "-d", os.path.join(ROOT, "artifacts/derived/from-previous-session/")])
data = open(lead_path, "rb").read()
banner = []
for r in re.findall(rb"[\x20-\x7e]{6,}", data):
    t = r.decode()
    if re.search(r"REBOL/Core|2\.7\.8|Copyright 20", t):
        banner.append(t)
ident = {"artifact": "rebol-2.7.8 (prior-session lead)",
         "sha256": hashlib.sha256(data).hexdigest(), "size": len(data),
         "elf": {"class": {1: "ELF32", 2: "ELF64"}[data[4]],
                  "endian": {1: "LE", 2: "BE"}[data[5]],
                  "e_type": {2: "EXEC", 3: "DYN"}.get(int.from_bytes(data[16:18], "little")),
                  "e_machine": {3: "i386", 62: "x86_64"}.get(int.from_bytes(data[18:20], "little"))},
         "embedded_banner": sorted(set(banner)),
         "identification": "REBOL/Core 2.7.8.4.3 (6-Jan-2011), Linux x86 libc6-2.5 build per rebol.com official download table",
         "identification_method": "STATIC string/ELF-header analysis only — NOT executed",
         "provenance_status": "UNVERIFIED",
         "status_note": ("identification is NOT attribution: the banner self-claims the official 278-4-3 build, "
                         "but this copy's origin/re constructive integrity remain unknown"),
         "verification_path": None}
ident["verification_path"] = ("once rebol.com is reachable: download "
    "http://www.rebol.com/downloads/v278/rebol-core-278-4-3.tar.gz, extract, compare sha256 of "
    "releases/rebol-core/rebol against " + ident["sha256"] + " (tarball-level reference hashes for "
    "sibling builds 4-2 are already on file)")
save({"generated_at": NOW, **ident}, os.path.join(MAN, "lead-binary-identification.json"))
print("B. lead:", ident["identification"])

# ---- C. fixture headers ----
def header_id(path):
    d = open(path, "rb").read(64)
    if d[:2] == b"MZ":
        pe = int.from_bytes(d[0x3C:0x40], "little")
        f = open(path, "rb"); f.seek(pe); sig = f.read(6); f.close()
        if sig[:4] == b"PE\0\0":
            machine = int.from_bytes(sig[4:6], "little")
            return {"format": "PE", "machine": {0x14C: "i386", 0x8664: "x86_64"}.get(machine, hex(machine))}
    if d[:4] == b"\x7fELF":
        return {"format": "ELF", "class": {1: "ELF32", 2: "ELF64"}.get(d[4]),
                "endian": {1: "LE", 2: "BE"}.get(d[5]),
                "e_machine": {3: "i386", 62: "x86_64", 40: "arm", 183: "aarch64"}.get(
                    int.from_bytes(d[18:20], "little" if d[5] == 1 else "big"), "unknown")}
    return {"format": "unknown"}
fix = []
for p in ["artifacts/red/tests/libRed-v0.6.6/libRed.dll",
          "artifacts/red/tests/libstruct-v0.6.6/libstructlib.so",
          "artifacts/red/tests/libstruct-v0.6.6/structlib.dll"]:
    full = os.path.join(ROOT, p)
    fix.append({"path": p, "sha256": sha256_file(full), **header_id(full)})
    print("C.", os.path.basename(p), fix[-1])
save({"generated_at": NOW, "method": "header magic + machine fields only (no execution)", "binaries": fix},
     os.path.join(MAN, "fixture-binary-identification.json"))

# ---- ledger ----
arts = load(os.path.join(MAN, "artifacts.json"))
for a in arts["artifacts"]:
    if a.get("filename") == "rebol-2.7.8 (prior-session lead)":
        a["identification"] = ident["identification"]
        a["identification_method"] = ident["identification_method"]
        a["embedded_banner"] = ident["embedded_banner"]
        a["elf"] = ident["elf"]
        a["verification_path"] = ident["verification_path"]
        a["notes"] = ("LEAD identified via embedded banner as REBOL/Core 2.7.8.4.3 (6-Jan-2011), consistent with "
                      "the official rebol.com build 278-4-3; provenance remains UNVERIFIED (identification != attribution)")
NEW = {"lead-binary-identification.json", "fixture-binary-identification.json"}
arts["artifacts"] = [a for a in arts["artifacts"] if a.get("filename") not in NEW]
def mrec(fn, project, origin, notes, classification="METADATA"):
    p2 = os.path.join(MAN, fn)
    return {"project": project, "version": None, "classification": classification, "origin": origin,
            "filename": fn, "path": f"artifacts/manifests/{fn}", "sha256": sha256_file(p2),
            "size": os.path.getsize(p2), "retrieved_at": NOW, "provenance_status": "VERIFIED",
            "integrity_status": "HASHED", "license_status": "n/a", "notes": notes}
arts["artifacts"].append(mrec("lead-binary-identification.json", "REBOL",
    "stage 17 static identification (banner + ELF header)", ident["identification"] + " — provenance UNVERIFIED"))
arts["artifacts"].append(mrec("fixture-binary-identification.json", "RED",
    "stage 17 header identification of committed fixture binaries",
    "; ".join(f"{os.path.basename(f['path'])}={f['format']}/{f.get('machine') or f.get('e_machine')}" for f in fix)))
arts["record_count"] = len(arts["artifacts"])
save(arts, os.path.join(MAN, "artifacts.json"))

# provenance
prov = load(os.path.join(PROV, "provenance.json"))
_seen = {(e["relationship"], e["source"], e["target"]) for e in prov["graph"]}
def edge(rel, s2, t, evd, status="ESTABLISHED"):
    if (rel, s2, t) in _seen: return
    prov["graph"].append({"relationship": rel, "source": s2, "target": t, "evidence": evd, "status": status})
edge("identification", "rebol-2.7.8 lead (1c902e0f…)", "REBOL/Core 2.7.8.4.3 (6-Jan-2011) — official build 278-4-3 identity",
     "embedded banner strings + ELF32/i386 header; static analysis only; identification is NOT attribution",
     status="PARTIAL")
save(prov, os.path.join(PROV, "provenance.json"))

# ---- report + addendum + sums ----
run(["python3", os.path.join(ROOT, "acquisition-tools/06_report.py")])
add = []
add.append("\n## Continuation Addendum (stage 17 — forensic identification sweep)\n")
add.append(f"_Generated: {NOW}_\n")
add.append("### Lead binary identified via embedded banner (static analysis only)\n")
add.append(f"- The prior-session `rebol-2.7.8` lead self-identifies as **{ident['identification']}** "
           f"(banner: \"REBOL/Core 2.7.8.4.3 (6-Jan-2011)\", \"Copyright 2011 REBOL Technologies\"; ELF32 LE i386 EXEC). "
           "This **upgrades the lead from filename-claimed to banner-identified**, consistent with the official "
           "rebol.com build 278-4-3 — but provenance remains **UNVERIFIED** (identification is not attribution). "
           "Verification path recorded: hash-compare against the official 278-4-3 tarball's binary once reachable.\n")
add.append("### Fixture binaries header-identified\n")
add.append("; ".join(f"`{os.path.basename(f['path'])}` = {f['format']}/{f.get('machine') or f.get('e_machine')}" for f in fix) +
           " — machine types recorded from headers (no execution).\n")
add.append("### CI bootstrap URL formally attempted\n")
add.append(f"- `static.red-lang.org/tmp/rebol` (the interpreter official Red CI downloads, v0.6.4 `.travis.yml:89`): "
           f"curl exit {rc} — blocked, logged as a distinct attempt.\n")
add.append("### Status impact\n")
add.append("- Final gate remains **PARTIALLY_VERIFIED**; the only UNVERIFIED artifact in the collection is now precisely identified with a concrete one-step verification path.\n")
_mdp = os.path.join(REP, "collection-report.md")
_md = open(_mdp).read()
_md = _md.split("\n## Continuation Addendum (stage 17")[0].rstrip() + "\n"
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
print(f"stage 17 complete; records={arts['record_count']} sha_lines={len(sums)}")
