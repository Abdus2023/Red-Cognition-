#!/usr/bin/env python3
"""
Stage 06 — Reports.
  artifacts/reports/collection-report.json
  artifacts/reports/collection-report.md
  artifacts/manifests/sha256sums.txt (regenerated last, excludes artifacts/derived/)
"""
import hashlib, json, os, time

ROOT = "/home/user/Red-Cognition-"
A = os.path.join(ROOT, "artifacts")
MAN, PROV, REP = (os.path.join(A, d) for d in ("manifests", "provenance", "reports"))
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def load(p):
    with open(p) as f:
        return json.load(f)

arts = load(os.path.join(MAN, "artifacts.json"))["artifacts"]
recon = load(os.path.join(PROV, "reconciliation.json"))
prov = load(os.path.join(PROV, "provenance.json"))
blocked = load(os.path.join(A, "logs", "blocked-attempts.json"))

def cnt(pred):
    return sum(1 for a in arts if pred(a))

reb = [a for a in arts if a["project"] == "REBOL"]
red = [a for a in arts if a["project"] == "RED"]
rs = [a for a in arts if a["project"] == "RED_SYSTEM"]
third_party = [a for a in arts if a.get("official") is False or a.get("provenance_status_reason", "").startswith("third-party") or "fork" in (a.get("provenance_status_reason") or "")]
unresolved = [a for a in arts if a.get("provenance_status") in ("UNVERIFIED", "BLOCKED", "CONFLICTING")]

report = {
 "generated_at": NOW, "final_gate": "PARTIALLY_VERIFIED",
 "final_gate_rationale": ("Substantial verified evidence exists (official upstream identity, immutable tag/commit resolution, "
                          "pinned-hash archives, git lineage proof). Verification is incomplete because every executable-binary "
                          "channel (static.red-lang.org, rebol.com, archive.org, GitHub release-asset CDN) is blocked by the "
                          "sandbox egress allowlist, so no binary acquisition, execution, or bootstrap reproduction was possible."),
 "collection_summary": {
  "rebol_artifacts_collected": len(reb),
  "red_artifacts_collected": len(red),
  "red_system_artifacts_collected": len(rs),
  "related_metadata_records": cnt(lambda a: a["project"] == "RELATED"),
  "git_repositories_collected": 7,
  "git_working_trees_collected": 1,
  "release_archives_collected": cnt(lambda a: a["classification"] == "ARCHIVE" and "releases/" in a.get("path", "")),
  "source_archives_collected": cnt(lambda a: a["classification"] == "ARCHIVE" and "source/" in a.get("path", "")),
  "binaries_collected": cnt(lambda a: a["classification"] == "BINARY" and a.get("provenance_status") == "VERIFIED"),
  "binaries_blocked_or_unverified": cnt(lambda a: a["classification"] == "BINARY") - cnt(lambda a: a["classification"] == "BINARY" and a.get("provenance_status") == "VERIFIED"),
  "source_trees_collected": cnt(lambda a: a["classification"] == "ARCHIVE" and "source/" in a.get("path", "")) + 1,
  "test_suites_collected": cnt(lambda a: a["classification"] == "TEST_SUITE"),
  "documentation_collected": cnt(lambda a: a["classification"] == "DOCUMENTATION"),
  "third_party_artifacts": len(third_party),
  "unresolved_artifacts": len(unresolved),
  "interpreter_binaries_executed": 0,
  "execution_evidence_records": 0,
 },
 "version_matrix": [
  {"project": "RED", "version": "0.6.6 (latest GitHub release)", "source": "tag archive (codeload, pinned)", "binary": "NONE (blocked: static.red-lang.org; GitHub release has 0 assets)", "commit": "6942c7a021253150c3e3cf90428305892340db03", "hash": "sha256 6c9f8dbf25e8bfb0eeb8d06a41e13ecab8ba2a5460cfb1425a53f7ee1a4a29c0", "provenance": "VERIFIED", "status": "COLLECTED (source only)"},
  {"project": "RED", "version": "0.6.4", "source": "tag archive (codeload, pinned)", "binary": "NONE (blocked)", "commit": "755eb943ccea9e78c2cab0f20b313a52404355cb", "hash": "sha256 2b5f3de16f14e273dc4d9062367bd86e87b4ecdb49bde62a09b52ebf7de7cee2", "provenance": "VERIFIED", "status": "COLLECTED (source only)"},
  {"project": "RED", "version": "0.7 (tag, no release)", "source": "tag resolution only", "binary": "NONE", "commit": "abfa7affa32cc908893545aabff7953a02de6009", "hash": "n/a", "provenance": "VERIFIED (identity)", "status": "RECORDED (not archived)"},
  {"project": "RED", "version": "master HEAD at acquisition", "source": "blobless clone evidence", "binary": "NONE", "commit": "b492f75752cc6b3abb8136825e9448ced9a357f2", "hash": "n/a", "provenance": "VERIFIED (identity)", "status": "RECORDED"},
  {"project": "RED", "version": "0.6.4-modified (workspace fork)", "source": "repository working tree", "binary": "NONE", "commit": "742181a8b868309b9fbebbf94e8355b8ac1eac06", "hash": "n/a (tree manifest committed)", "provenance": "PARTIALLY_VERIFIED", "status": "THIRD_PARTY fork; modified subset of v0.6.4 (248/530 files identical)"},
  {"project": "RED_SYSTEM", "version": "0.6.6 (within red/red tree)", "source": "system/ + system/tests/ in v0.6.6 tree (97 test files)", "binary": "NONE", "commit": "6942c7a021253150c3e3cf90428305892340db03", "hash": "same archive hash", "provenance": "VERIFIED", "status": "COLLECTED (source + tests, not executed)"},
  {"project": "REBOL", "version": "R3 2.101.0.3.1 (official source master)", "source": "rebol/rebol archive (pinned commit)", "binary": "NONE (no GitHub releases exist; rebol.com blocked)", "commit": "25033f897b2bd466068d7663563cd3ff64740b94", "hash": "sha256 2fc66ae8e3e6db08765c047192aa0819f4103b6b7d0f7b9e6a11c1f7ba5836bd", "provenance": "VERIFIED", "status": "COLLECTED (source only)"},
  {"project": "REBOL", "version": "R3 (rebolsource historical)", "source": "rebolsource/r3 archive (pinned commit)", "binary": "NONE (rebolsource.net blocked)", "commit": "98cdfcd6e439390756868b390b0ff8aa01d84551", "hash": "sha256 c1a5ad24b08e78e0de3bc4bfb40bea3ca8dc2dbd24eefea3e0f7fbe3ac91a590", "provenance": "PARTIALLY_VERIFIED", "status": "TIER-2 historical; lineage to rebol/rebol proven by merge-base"},
  {"project": "REBOL", "version": "ren-c 2.102.0.0.0 (internal)", "source": "ren-c archive (pinned commit)", "binary": "NONE (no GitHub releases; rebolsource.net blocked)", "commit": "e31d5698d73678d797df319eb855b3995716d9f1", "hash": "sha256 c682eb8646c62c1fda5f4e5561d9f7c8ea76eb9ee10f8bef1c67a1e5b8b1a9b9", "provenance": "PARTIALLY_VERIFIED", "status": "THIRD_PARTY continuation; lineage proven by merge-base; LGPL-3.0 relicensing recorded"},
  {"project": "REBOL", "version": "3.22.1 (Oldes fork release; internal 3.22.53.5.4.3.1)", "source": "Oldes/Rebol3 archive (pinned commit)", "binary": "NONE (release assets CDN blocked)", "commit": "d5b237cea60d06b72c59bb6dbed0022b482f4c57", "hash": "sha256 4b8465c4b52e0a1de3ff9c1ca86b7f7ba98b6efae41a68a3ba10a3cb78d99c06", "provenance": "PROVISIONAL", "status": "THIRD_PARTY fork; version-scheme conflict recorded"},
  {"project": "REBOL", "version": "2.7.8 (official binaries)", "source": "rebol.com (Tier 1)", "binary": "NOT ACQUIRED - BLOCKED (TLS)", "commit": "n/a", "hash": "n/a", "provenance": "BLOCKED", "status": "NOT COLLECTED"},
  {"project": "REBOL", "version": "2.7.8 (prior-session lead)", "source": "repo-internal zip, origin unrecorded", "binary": "ELF32 binary held in derived/", "commit": "n/a", "hash": "sha256 1c902e0f75e994d739975e12963323832ce00f52208b3287cbfe5e7029d856d6", "provenance": "UNVERIFIED", "status": "LEAD ONLY (not executed; ELF32 vs x86_64 host)"},
 ],
 "acquisition_problems": {
  "network_blocked": [a["url"] for a in blocked["attempts"] if a["result"] == "NETWORK_BLOCKED"],
  "not_found": [a for a in blocked["attempts"] if a["result"] == "NOT_FOUND"],
  "missing_releases": [
   "red/red: tag v0.7 exists with no GitHub release",
   "rebol/rebol: no tags and no releases at all (official R3 distribution never mirrored on GitHub)",
   "metaeducation/ren-c: no GitHub releases (only atronix-* test tags); binaries live off-GitHub (blocked)",
  ],
  "conflicting_versions": [
   "Oldes/Rebol3 internal .version=3.22.53.5.4.3.1 vs release tag 3.22.1 (different schemes; unresolved by design)",
   "workspace fork claims 0.6.4 but is NOT byte-identical to upstream v0.6.4 (253 differing files, 334 fork-only files)",
  ],
  "missing_licenses": [
   "rebolsource/rebol-syntax: no LICENSE file (UNCLEAR)",
   "prior-session rebol-2.7.8 binary: no license claim (MISSING)",
   "Oldes/Rebol3: bundled third-party extensions not individually license-verified",
  ],
  "corrupted_archives": [],
  "incomplete_source_trees": [
   "red/red clones are blobless (no blob content locally); full bytes available via committed tag archives and GitHub",
  ],
  "inaccessible_historical_artifacts": [
   "rebol.com official REBOL 2.7.8 binaries + docs (TLS-blocked)",
   "Internet Archive copies of rebol.com binaries (blocked)",
   "rebolsource.net Ren-C/R3 historical builds (blocked)",
   "www.rebol.tech (blocked)",
  ],
  "execution_gaps": [
   "No artifact executed; no bootstrap reproduction attempted (no interpreter obtainable) -> BOOTSTRAP_EXECUTED / BOOTSTRAP_REPRODUCED / any EXECUTED claim: NONE",
  ],
 },
 "counts_reconciliation_note": ("rebol_artifacts_collected includes 1 UNVERIFIED lead binary and 6 METADATA records; "
                                "red_artifacts_collected includes 3 verified test-fixture binaries."),
}

report["collection_summary"]["rebol_artifacts_collected"] = len(reb)
report["collection_summary"]["red_artifacts_collected"] = len(red)
report["collection_summary"]["red_system_artifacts_collected"] = len(rs)
# discovered counts from the discovery manifest
disc2 = load(os.path.join(MAN, "github-discovery.json"))
report["collection_summary"]["discovered"] = {
    "red_org_repositories_on_github": len(disc2.get("red_org_repos") or []),
    "rebol_org_repositories_on_github": len(disc2.get("rebol_org") or []),
    "rebolsource_org_repositories_on_github": 5,
    "github_search_queries_run": list(disc2.get("searches", {}).keys()),
}
# fix version matrix hashes from the real manifest, by explicit row order
hashmap = {a["filename"]: a["sha256"] for a in arts if a.get("sha256")}
ROW_ARCHIVE = {0: "red-0.6.6.tar.gz", 1: "red-0.6.4.tar.gz",
               6: "rebol-rebol-25033f897.tar.gz", 7: "rebolsource-r3-98cdfcd6e.tar.gz",
               8: "ren-c-e31d5698d.tar.gz", 9: "Oldes-Rebol3-d5b237cea.tar.gz"}
for i, fn in ROW_ARCHIVE.items():
    if fn in hashmap:
        report["version_matrix"][i]["hash"] = "sha256 " + hashmap[fn]
report["version_matrix"][4]["hash"] = "n/a (tree manifest committed)"  # workspace fork

with open(os.path.join(REP, "collection-report.json"), "w") as f:
    json.dump(report, f, indent=2)

# ---------------------------------------------------------------- markdown
def md_table(rows, headers):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)

cs = report["collection_summary"]
md = []
md.append("# Rebol & Red Collection Report\n")
md.append(f"_Generated: {NOW} — acquisition per `Rebol & Red Collection Agent — GitHub + Web Acquisition Protocol`_\n")
md.append("## Final Gate: **PARTIALLY_VERIFIED**\n")
md.append("> Substantial verified evidence exists (official upstream identity, immutable tag/commit resolution, pinned-hash "
          "archives, git lineage proof). Verification is incomplete because **every executable-binary channel "
          "(static.red-lang.org, rebol.com, archive.org, GitHub release-asset CDN) is blocked by the sandbox egress "
          "allowlist** — no binary acquisition, execution, or bootstrap reproduction was possible. No status was promoted "
          "without evidence; `COMPLETE`/`VERIFIED` was therefore **not** claimed.\n")
md.append("## Collection Summary\n")
md.append(md_table([
 ["Rebol artifacts discovered (GitHub, evidence-backed)", "rebol org: 2 repos; rebolsource org: 5 repos; 'rebol2' search: 6 repos (none is an official R2 source tree)"],
 ["Red artifacts discovered (GitHub, evidence-backed)", "red org: 33 repos (incl. official red/red)"],
 ["Rebol artifacts collected", len(reb)], ["Red artifacts collected", len(red)],
 ["Red/System artifacts collected", len(rs)],
 ["Related metadata records (tree manifests)", cs["related_metadata_records"]],
 ["Git repositories collected", "7 upstream + 1 fork working tree"],
 ["Release archives collected", cs["release_archives_collected"]],
 ["Source archives collected", cs["source_archives_collected"]],
 ["Binaries collected (verified)", cs["binaries_collected"]],
 ["Binaries blocked/unverified", cs["binaries_blocked_or_unverified"]],
 ["Source trees collected", cs["source_trees_collected"]],
 ["Test suites collected", cs["test_suites_collected"]],
 ["Documentation collected", cs["documentation_collected"]],
 ["Third-party artifacts", cs["third_party_artifacts"]],
 ["Unresolved artifacts", cs["unresolved_artifacts"]],
 ["Interpreter binaries executed", "0 (NONE — see Execution Evidence)"],
], ["Metric", "Value"]))
md.append("\n## Environment Constraint (evidence-backed)\n")
md.append("Sandbox egress allows only `github.com`, `api.github.com`, `codeload.github.com`. All other hosts fail TLS "
          "(`curl` exit 35, SSL_ERROR_SYSCALL). Verbatim attempt logs: `artifacts/logs/execution/blocked-*.log`, "
          "structured list: `artifacts/logs/blocked-attempts.json` (21 recorded attempts).\n")
md.append("## Version Matrix\n")
md.append(md_table([[r["project"], r["version"], r["source"], r["binary"], (r["commit"] or "n/a")[:12], (r["hash"] or "n/a")[:24], r["provenance"], r["status"]] for r in report["version_matrix"]],
                   ["Project", "Version", "Source", "Binary", "Commit", "Hash", "Provenance", "Status"]))
md.append("\n## Collected Artifacts (exact)\n")
md.append(md_table([[a["project"], a["classification"], a["filename"], a.get("version") or "n/a",
                     (a.get("commit") or "n/a")[:12] if a.get("commit") else "n/a",
                     (a["sha256"][:20] + "…") if a.get("sha256") else "n/a",
                     a.get("provenance_status", "n/a"), a.get("license_status", "n/a")] for a in arts],
                   ["Project", "Class", "Filename", "Version", "Commit", "SHA-256 (head)", "Provenance", "License"]))
md.append("\n## Provenance Graph (key edges)\n")
md.append("\n".join(f"- **{e['relationship']}**: `{e['source']}` → `{e['target']}` — {e['evidence']}" for e in prov["graph"]))
md.append("\n## Bootstrap Status (never collapsed)\n")
md.append(md_table([
 ["Red bootstrap (Rebol2 required for builds)", "BOOTSTRAP_CLAIMED"],
 ["red.r + build/ scripts present in v0.6.4/v0.6.6 trees", "BOOTSTRAP_SOURCE_PRESENT"],
 ["Any bootstrap binary collected", "NO (all channels blocked)"],
 ["Bootstrap executed / reproduced / independently verified", "NOT ESTABLISHED (nothing executed)"],
], ["Aspect", "Status"]))
md.append("\nVerbatim upstream claim (v0.6.4 README line 12): _\"…not depending on any third-party library, except for a "
          "Rebol2 interpreter, required during the bootstrap phase.\"_ (v0.6.6 README line 24: \"…required during the alpha stage.\")\n")
md.append("## Reconciliation (conflicts surfaced, never silently resolved)\n")
for t in recon["tables"]:
    md.append(f"\n### {t['id']} — {t['artifact']}\n")
    md.append(md_table(t["rows"], ["Field", "Source A", "Source B", "Result"]))
md.append("\n## Execution Evidence\n")
md.append("**None.** No artifact was executed this session. The only binary in custody besides test fixtures is the "
          "prior-session `rebol-2.7.8` lead (ELF32, provenance UNKNOWN) — execution not attempted (x86_64 host, untrusted "
          "origin). Records: `artifacts/logs/execution/execution-evidence.json`.\n")
md.append("## Acquisition Problems\n")
ap = report["acquisition_problems"]
md.append(f"- **Network blocked ({len(ap['network_blocked'])} URLs)**: rebol.com (all), archive.org, web.archive.org, "
          "static.red-lang.org, www.red-lang.org, rebolsource.net, www.rebol.tech, deb.debian.org, snapshot.debian.org, "
          "raw/media/objects/release-assets.githubusercontent.com (⇒ GitHub release-asset downloads blocked)")
md.append(f"- **Missing releases**: " + "; ".join(ap["missing_releases"]))
md.append(f"- **Conflicting versions**: " + "; ".join(ap["conflicting_versions"]))
md.append(f"- **Missing/unclear licenses**: " + "; ".join(ap["missing_licenses"]))
md.append(f"- **Inaccessible historical artifacts**: " + "; ".join(ap["inaccessible_historical_artifacts"]))
md.append(f"- **Execution gaps**: " + "; ".join(ap["execution_gaps"]))
md.append("\n## Integrity & License Status\n")
md.append(md_table([
 ["HASHED (all preserved artifacts)", len([a for a in arts if a.get("integrity_status") == "HASHED"])],
 ["HASH_MATCHED (git blob verification)", len([a for a in arts if a.get("integrity_status") == "HASH_MATCHED"])],
 ["NO_REFERENCE_HASH", len([a for a in arts if a.get("integrity_status") == "NO_REFERENCE_HASH"])],
 ["License CONFIRMED", len([a for a in arts if a.get("license_status") == "CONFIRMED"])],
 ["License UNCLEAR", len([a for a in arts if a.get("license_status") == "UNCLEAR"])],
 ["License MISSING", len([a for a in arts if a.get("license_status") == "MISSING"])],
], ["Status", "Count"]))
md.append("\n## Recommended Next Steps\n")
md.append("1. Re-run acquisition from an unrestricted network and download: official REBOL 2.7.8 binaries (rebol.com/pub/platforms), "
          "official Red binaries (static.red-lang.org/dl/auto/, incl. the build matching v0.6.6), Oldes/Rebol3 release assets, "
          "and Internet Archive copies of rebol.com for cross-hashing.")
md.append("2. Execute Red v0.6.6 Linux binary and a Rebol 2.7.8 Linux x86-64 binary with full execution logs; verify "
          "`version.r` claims against interpreter output.")
md.append("3. Reproduce the Red bootstrap: build red.bin from the v0.6.6 tree using an official Rebol 2.7.8 interpreter; "
          "compare output hashes with the official binary (expected non-reproducible; record NOT_REPRODUCED unless matched).")
md.append("4. Diff the workspace fork against upstream v0.6.4 (253 differing files) to attribute fork modifications.")
md.append("5. Verify Oldes/Rebol3 bundled extension licenses individually (repo license covers the core tree only).")
md.append("6. Collect red/red git object bundle (full clone) when storage/network permits; this session's clones were blobless.")

with open(os.path.join(REP, "collection-report.md"), "w") as f:
    f.write("\n".join(md) + "\n")

# regenerate sha256sums.txt LAST (covers manifests, provenance, reports, logs; excludes derived/)
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

print(f"report written; sha256 lines={len(sums)}")
