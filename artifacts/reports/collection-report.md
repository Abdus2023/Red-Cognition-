# Rebol & Red Collection Report

_Generated: 2026-08-31T17:33:52Z — acquisition per `Rebol & Red Collection Agent — GitHub + Web Acquisition Protocol`_

## Final Gate: **PARTIALLY_VERIFIED**

> Substantial verified evidence exists (official upstream identity, immutable tag/commit resolution, pinned-hash archives, git lineage proof). Verification is incomplete because **every executable-binary channel (static.red-lang.org, rebol.com, archive.org, GitHub release-asset CDN) is blocked by the sandbox egress allowlist** — no binary acquisition, execution, or bootstrap reproduction was possible. No status was promoted without evidence; `COMPLETE`/`VERIFIED` was therefore **not** claimed.

## Collection Summary

| Metric | Value |
|---|---|
| Rebol artifacts discovered (GitHub, evidence-backed) | rebol org: 2 repos; rebolsource org: 5 repos; 'rebol2' search: 6 repos (none is an official R2 source tree) |
| Red artifacts discovered (GitHub, evidence-backed) | red org: 33 repos (incl. official red/red) |
| Rebol artifacts collected | 13 |
| Red artifacts collected | 7 |
| Red/System artifacts collected | 2 |
| Related metadata records (tree manifests) | 12 |
| Git repositories collected | 7 upstream + 1 fork working tree |
| Release archives collected | 2 |
| Source archives collected | 4 |
| Binaries collected (verified) | 3 |
| Binaries blocked/unverified | 1 |
| Source trees collected | 5 |
| Test suites collected | 2 |
| Documentation collected | 1 |
| Third-party artifacts | 6 |
| Unresolved artifacts | 1 |
| Interpreter binaries executed | 0 (NONE — see Execution Evidence) |

## Environment Constraint (evidence-backed)

Sandbox egress allows only `github.com`, `api.github.com`, `codeload.github.com`. All other hosts fail TLS (`curl` exit 35, SSL_ERROR_SYSCALL). Verbatim attempt logs: `artifacts/logs/execution/blocked-*.log`, structured list: `artifacts/logs/blocked-attempts.json` (21 recorded attempts).

## Version Matrix

| Project | Version | Source | Binary | Commit | Hash | Provenance | Status |
|---|---|---|---|---|---|---|---|
| RED | 0.6.6 (latest GitHub release) | tag archive (codeload, pinned) | NONE (blocked: static.red-lang.org; GitHub release has 0 assets) | 6942c7a02125 | sha256 23a02a53e0dcbf8da | VERIFIED | COLLECTED (source only) |
| RED | 0.6.4 | tag archive (codeload, pinned) | NONE (blocked) | 755eb943ccea | sha256 d69d69f332cc14886 | VERIFIED | COLLECTED (source only) |
| RED | 0.7 (tag, no release) | tag resolution only | NONE | abfa7affa32c | n/a | VERIFIED (identity) | RECORDED (not archived) |
| RED | master HEAD at acquisition | blobless clone evidence | NONE | b492f75752cc | n/a | VERIFIED (identity) | RECORDED |
| RED | 0.6.4-modified (workspace fork) | repository working tree | NONE | 742181a8b868 | n/a (tree manifest commi | PARTIALLY_VERIFIED | THIRD_PARTY fork; modified subset of v0.6.4 (248/530 files identical) |
| RED_SYSTEM | 0.6.6 (within red/red tree) | system/ + system/tests/ in v0.6.6 tree (97 test files) | NONE | 6942c7a02125 | same archive hash | VERIFIED | COLLECTED (source + tests, not executed) |
| REBOL | R3 2.101.0.3.1 (official source master) | rebol/rebol archive (pinned commit) | NONE (no GitHub releases exist; rebol.com blocked) | 25033f897b2b | sha256 ffe75f829fd414aa6 | VERIFIED | COLLECTED (source only) |
| REBOL | R3 (rebolsource historical) | rebolsource/r3 archive (pinned commit) | NONE (rebolsource.net blocked) | 98cdfcd6e439 | sha256 90932ec932e5f4dec | PARTIALLY_VERIFIED | TIER-2 historical; lineage to rebol/rebol proven by merge-base |
| REBOL | ren-c 2.102.0.0.0 (internal) | ren-c archive (pinned commit) | NONE (no GitHub releases; rebolsource.net blocked) | e31d5698d736 | sha256 273627e44f19e12e6 | PARTIALLY_VERIFIED | THIRD_PARTY continuation; lineage proven by merge-base; LGPL-3.0 relicensing recorded |
| REBOL | 3.22.1 (Oldes fork release; internal 3.22.53.5.4.3.1) | Oldes/Rebol3 archive (pinned commit) | NONE (release assets CDN blocked) | d5b237cea60d | sha256 45ab2a0712f3eb8ab | PROVISIONAL | THIRD_PARTY fork; version-scheme conflict recorded |
| REBOL | 2.7.8 (official binaries) | rebol.com (Tier 1) | NOT ACQUIRED - BLOCKED (TLS) | n/a | n/a | BLOCKED | NOT COLLECTED |
| REBOL | 2.7.8 (prior-session lead) | repo-internal zip, origin unrecorded | ELF32 binary held in derived/ | n/a | sha256 1c902e0f75e994d73 | UNVERIFIED | LEAD ONLY (not executed; ELF32 vs x86_64 host) |

## Collected Artifacts (exact)

| Project | Class | Filename | Version | Commit | SHA-256 (head) | Provenance | License |
|---|---|---|---|---|---|---|---|
| RED | ARCHIVE | red-0.6.6.tar.gz | 0.6.6 | commit 6942c | 23a02a53e0dcbf8da24c… | VERIFIED | CONFIRMED |
| RED | ARCHIVE | red-0.6.4.tar.gz | 0.6.4 | commit 755eb | d69d69f332cc14886177… | VERIFIED | CONFIRMED |
| REBOL | ARCHIVE | rebol-rebol-25033f897.tar.gz | R3 master | commit 25033 | ffe75f829fd414aa6146… | VERIFIED | CONFIRMED |
| REBOL | ARCHIVE | ren-c-e31d5698d.tar.gz | ren-c master | commit e31d5 | 273627e44f19e12e64ef… | VERIFIED | CONFIRMED |
| REBOL | ARCHIVE | rebolsource-r3-98cdfcd6e.tar.gz | R3 (rebolsource) | commit 98cdf | 90932ec932e5f4dece81… | VERIFIED | CONFIRMED |
| REBOL | ARCHIVE | Oldes-Rebol3-d5b237cea.tar.gz | 3.22.1-44-gd5b237ce | commit d5b23 | 45ab2a0712f3eb8abf39… | VERIFIED | CONFIRMED |
| REBOL | DOCUMENTATION | rebol-syntax-4ff113963.tar.gz | master | commit 4ff11 | 167850465379eced0f95… | VERIFIED | UNCLEAR |
| REBOL | TEST_SUITE | rebol-test-409ef5c22.tar.gz | master | commit 409ef | 681a68b89c4c285d930d… | VERIFIED | CONFIRMED |
| RED | BINARY | libRed.dll | 0.6.6 | commit 6942c | 5e523ee5adffaec63285… | VERIFIED | CONFIRMED |
| RED | BINARY | libstructlib.so | 0.6.6 | commit 6942c | 780f072d9a0324ab3ddd… | VERIFIED | CONFIRMED |
| RED | BINARY | structlib.dll | 0.6.6 | commit 6942c | aa85993d2c6a8b59bff1… | VERIFIED | CONFIRMED |
| RED | METADATA | red.git-evidence | n/a | b492f75752cc | 53943f4144ef36772e13… | VERIFIED | CONFIRMED |
| REBOL | METADATA | rebol_rebol.git-evidence | n/a | 25033f897b2b | 92ba62038f29858fe2ae… | VERIFIED | CONFIRMED |
| REBOL | METADATA | rebolsource_r3.git-evidence | n/a | 98cdfcd6e439 | 7742da0a97d9dc0e6bae… | PARTIALLY_VERIFIED | CONFIRMED |
| REBOL | METADATA | metaeducation_ren-c.git-evidence | n/a | e31d5698d736 | 7e9c7593c88071f9ff08… | PARTIALLY_VERIFIED | CONFIRMED |
| REBOL | METADATA | Oldes_Rebol3.git-evidence | n/a | d5b237cea60d | 9ece2b446293ed32de59… | PARTIALLY_VERIFIED | CONFIRMED |
| REBOL | METADATA | rebolsource_rebol-syntax.git-evidence | n/a | 4ff11396312d | 307785a097bd02cfbf53… | PARTIALLY_VERIFIED | UNCLEAR |
| REBOL | METADATA | rebolsource_rebol-test.git-evidence | n/a | 409ef5c2270a | 4c8e00a04ac25b974159… | PARTIALLY_VERIFIED | CONFIRMED |
| RED_SYSTEM | SOURCE | red-system-source@v0.6.6 | 0.6.6 (same tree as red/red v0.6.6) | 6942c7a02125 | 23a02a53e0dcbf8da24c… | VERIFIED | CONFIRMED |
| RED_SYSTEM | TEST_SUITE | red-system-tests@v0.6.6 | 0.6.6 | 6942c7a02125 | 23a02a53e0dcbf8da24c… | VERIFIED | CONFIRMED |
| RED | SOURCE | workspace-fork-tree | 0.6.4 (version.r claim) | 742181a8b868 | n/a | PARTIALLY_VERIFIED | CONFIRMED |
| REBOL | BINARY | rebol-2.7.8 (prior-session lead) | 2.7.8 (filename claim only - UNVERIFIED) | n/a | 1c902e0f75e994d73997… | UNVERIFIED | MISSING |
| RELATED | METADATA | Oldes_Rebol3__HEAD.lsr | n/a | n/a | 9ece2b446293ed32de59… | VERIFIED | n/a |
| RELATED | METADATA | metaeducation_ren-c__HEAD.lsr | n/a | n/a | 7e9c7593c88071f9ff08… | VERIFIED | n/a |
| RELATED | METADATA | rebol_rebol__HEAD.lsr | n/a | n/a | 92ba62038f29858fe2ae… | VERIFIED | n/a |
| RELATED | METADATA | rebolsource_r3__HEAD.lsr | n/a | n/a | 7742da0a97d9dc0e6bae… | VERIFIED | n/a |
| RELATED | METADATA | rebolsource_rebol-syntax__HEAD.lsr | n/a | n/a | 307785a097bd02cfbf53… | VERIFIED | n/a |
| RELATED | METADATA | rebolsource_rebol-test__HEAD.lsr | n/a | n/a | 4c8e00a04ac25b974159… | VERIFIED | n/a |
| RELATED | METADATA | red__HEAD.lsr | n/a | n/a | a42b0f3b777d2ccdd626… | VERIFIED | n/a |
| RELATED | METADATA | red__v0.6.3.lsr | n/a | n/a | ac5b8ffaacca2ae8dff8… | VERIFIED | n/a |
| RELATED | METADATA | red__v0.6.4.lsr | n/a | n/a | 8eaa28a80df147ab2d88… | VERIFIED | n/a |
| RELATED | METADATA | red__v0.6.6.lsr | n/a | n/a | b462d6b017f396d0b6b8… | VERIFIED | n/a |
| RELATED | METADATA | red__v0.7.lsr | n/a | n/a | 8f0f53d11d419e0b8058… | VERIFIED | n/a |
| RELATED | METADATA | workspace-fork__HEAD.lsr | n/a | n/a | 91303caf2789843e2958… | VERIFIED | n/a |

## Provenance Graph (key edges)

- **release->tag**: `GitHub release red/red v0.6.6 (published 2025-03-19)` → `tag v0.6.6` — github-discovery.json releases[].tag_name=v0.6.6; target_commitish=master
- **tag->commit**: `tag v0.6.6` → `commit 6942c7a021253150c3e3cf90428305892340db03` — git rev-parse v0.6.6^{commit} in blobless clone (git-collection.json)
- **commit->source-tree**: `commit 6942c7a021253150c3e3cf90428305892340db03` → `source tree (673 entries, red__v0.6.6.lsr)` — git ls-tree -r v0.6.6 deterministic manifest
- **source-tree->archive**: `tree of commit 6942c7a0...` → `artifacts/red/releases/red-0.6.6.tar.gz` — codeload.github.com/red/red/tar.gz/refs/tags/v0.6.6 (download pinned to tag->commit); version evidence encapper/version.r=0.6.6 inside
- **archive->binary**: `red-0.6.6.tar.gz tree (commit 6942c7a0...)` → `artifacts/red/tests/libRed-v0.6.6/libRed.dll` — git blob SHA-1 26e21ac96ad441a6888052538f8c468b50a67105 == git hash-object of downloaded bytes (verified)
- **upstream-tag->fork-tree**: `red/red tag v0.6.4 (commit 755eb943...)` → `workspace fork tree 742181a8...` — blob-SHA comparison: 248/530 upstream source files byte-identical; 253 differ; 334 fork-only; upstream rejects ref 742181a (not present)
- **upstream-repo->historical-repo**: `rebol/rebol master (25033f89..., 2014-03-03)` → `rebolsource/r3 HEAD (98cdfcd6...)` — git merge-base(rebolsource_r3 HEAD, rebol/rebol master) == 25033f89... -> rebol/rebol master is ancestor of rebolsource/r3 HEAD
- **historical-repo->continuation**: `rebolsource/r3 (98cdfcd6...)` → `metaeducation/ren-c HEAD (e31d5698d...)` — git merge-base(ren-c HEAD, rebolsource/r3 master) == d5d6908f... (2015-04-14); 10176 ren-c commits after fork point; GitHub metadata parent=rebolsource/r3
- **upstream-repo->fork**: `rebol/rebol master (25033f89...)` → `Oldes/Rebol3 HEAD (d5b237ce...)` — git merge-base(Oldes_Rebol3 HEAD, rebol/rebol master) == 25033f89... -> fork of official R3 master
- **license-text-identity**: `rebol/rebol LICENSE (sha256 c95bae1d...)` → `rebolsource/r3, rebol-test, Oldes/Rebol3 LICENSE files` — identical SHA-256 of LICENSE file content in all four archives (source-inspection.json)
- **license-text-divergence**: `rebolsource/r3 (Apache-2.0)` → `metaeducation/ren-c (LGPL-3.0)` — ren-c LICENSE sha256 1a45b1d0... = GNU LGPL v3 text; differs from lineage Apache-2.0
- **bootstrap-claim**: `red/red README (v0.6.4 line 12; v0.6.6 line 24)` → `Rebol2 interpreter required during bootstrap phase` — verbatim: 'except for a Rebol2 interpreter, required during the bootstrap phase' (v0.6.4) / 'required during the alpha stage' (v0.6.6); red.r + build/ present in trees
- **bootstrap-status**: `Red bootstrap chain` → `BOOTSTRAP_CLAIMED + BOOTSTRAP_SOURCE_PRESENT` — claim documented by upstream; build scripts present; NOTHING executed -> BOOTSTRAP_EXECUTED/REPRODUCED NOT established
- **no-release-assets**: `GitHub releases of red/red (v0.6.6, v0.6.4, v0.6.3)` → `assets=0` — github-discovery.json: all three releases have empty assets arrays; binaries are distributed via official site (blocked from this environment)

## Bootstrap Status (never collapsed)

| Aspect | Status |
|---|---|
| Red bootstrap (Rebol2 required for builds) | BOOTSTRAP_CLAIMED |
| red.r + build/ scripts present in v0.6.4/v0.6.6 trees | BOOTSTRAP_SOURCE_PRESENT |
| Any bootstrap binary collected | NO (all channels blocked) |
| Bootstrap executed / reproduced / independently verified | NOT ESTABLISHED (nothing executed) |

Verbatim upstream claim (v0.6.4 README line 12): _"…not depending on any third-party library, except for a Rebol2 interpreter, required during the bootstrap phase."_ (v0.6.6 README line 24: "…required during the alpha stage.")

## Reconciliation (conflicts surfaced, never silently resolved)


### R1 — Red v0.6.6 (latest release)

| Field | Source A | Source B | Result |
|---|---|---|---|
| Version (release name) | 0.6.6: Memory Management Improvements | tag v0.6.6 | MATCH |
| Version (embedded) | encapper/version.r = 0.6.6 (in tarball) | release name 0.6.6 | MATCH |
| Commit | release target_commitish=master | tag v0.6.6 -> 6942c7a0... | MATCH (tag is on master line) |
| Source | github.com/red/red (official) | codeload archive of tag | MATCH |
| License | repo metadata BSL-1.0 | BSD-3-License.txt + BSL-License.txt in tree | PARTIAL (both files present; SPDX metadata captures BSL only) |

### R2 — Red v0.6.4 vs workspace fork

| Field | Source A | Source B | Result |
|---|---|---|---|
| Version claim | upstream version.r = 0.6.4 | fork version.r = 0.6.4 | MATCH |
| Tree content | upstream 530 source files | 248 byte-identical / 253 differing / 334 fork-only | CONFLICT (fork is NOT byte-identical to v0.6.4; it is a modified subset) |
| Commit | 755eb943... (upstream v0.6.4) | 742181a8... (fork-only; rejected by upstream) | CONFLICT (fork commit not in upstream history) |
| License | BSD-3 (c) 2011 Nenad Rakocevic | same files carried in fork | MATCH |

### R3 — Red license text across versions

| Field | Source A | Source B | Result |
|---|---|---|---|
| BSD-3 text v0.6.4 | sha256 09b59353... (c) 2011 Nenad Rakocevic | - | NOTED |
| BSD-3 text v0.6.6 | sha256 e64d2571... (c) 2011-2019 Red Foundation | - | NOTED (text changed between versions; per-artifact license is CONFIRMED by its own tree) |

### R4 — R3 lineage versions

| Field | Source A | Source B | Result |
|---|---|---|---|
| rebol/rebol (official R3) | src/boot/version.r = 2.101.0.3.1 | no tags, no releases on GitHub | NOTED |
| rebolsource/r3 | src/boot/version.r = 2.101.0.3.1 | same as rebol/rebol | MATCH |
| metaeducation/ren-c | src/specs/version.r = 2.102.0.0.0 | no releases; atronix tags only | NOTED |
| Oldes/Rebol3 | internal .version = 3.22.53.5.4.3.1 | GitHub release/tag 3.22.1 | CONFLICT (different version schemes: internal 3.22.53.x vs tag 3.22.1 - recorded, not resolved) |

### R5 — R3 lineage licenses

| Field | Source A | Source B | Result |
|---|---|---|---|
| LICENSE text hash | rebol/rebol / rebolsource/r3 / rebol-test / Oldes-Rebol3 all sha256 c95bae1d... (Apache-2.0) | ren-c sha256 1a45b1d0... (LGPL-3.0) | CONFLICT (ren-c relicensed vs lineage; recorded with evidence) |
| rebolsource/rebol-syntax | no LICENSE file in repo | - | UNCLEAR |

### R6 — REBOL 2.7.8 official distribution

| Field | Source A | Source B | Result |
|---|---|---|---|
| Version claims | rebol.com download pages (via search-index snapshot): Core 2.7.8.3.1 / .4.2 / .4.3 / .4.10, View 2.7.8.x | direct fetch from rebol.com: BLOCKED (TLS) | UNVERIFIED (second-hand page content only; acquisition BLOCKED) |
| Binary availability | rebol.com/pub/platforms/... (URLs from page snippet) | all attempts TLS-blocked from sandbox | BLOCKED |

### R7 — Red binary distribution

| Field | Source A | Source B | Result |
|---|---|---|---|
| GitHub release assets | v0.6.6/v0.6.4/v0.6.3 assets=0 | official binaries hosted on static.red-lang.org | CONFLICT (expectation: release binaries on GitHub; reality: off-GitHub hosting) |
| static.red-lang.org | official download host | TLS-blocked from sandbox | BLOCKED |

## Execution Evidence

**None.** No artifact was executed this session. The only binary in custody besides test fixtures is the prior-session `rebol-2.7.8` lead (ELF32, provenance UNKNOWN) — execution not attempted (x86_64 host, untrusted origin). Records: `artifacts/logs/execution/execution-evidence.json`.

## Acquisition Problems

- **Network blocked (19 URLs)**: rebol.com (all), archive.org, web.archive.org, static.red-lang.org, www.red-lang.org, rebolsource.net, www.rebol.tech, deb.debian.org, snapshot.debian.org, raw/media/objects/release-assets.githubusercontent.com (⇒ GitHub release-asset downloads blocked)
- **Missing releases**: red/red: tag v0.7 exists with no GitHub release; rebol/rebol: no tags and no releases at all (official R3 distribution never mirrored on GitHub); metaeducation/ren-c: no GitHub releases (only atronix-* test tags); binaries live off-GitHub (blocked)
- **Conflicting versions**: Oldes/Rebol3 internal .version=3.22.53.5.4.3.1 vs release tag 3.22.1 (different schemes; unresolved by design); workspace fork claims 0.6.4 but is NOT byte-identical to upstream v0.6.4 (253 differing files, 334 fork-only files)
- **Missing/unclear licenses**: rebolsource/rebol-syntax: no LICENSE file (UNCLEAR); prior-session rebol-2.7.8 binary: no license claim (MISSING); Oldes/Rebol3: bundled third-party extensions not individually license-verified
- **Inaccessible historical artifacts**: rebol.com official REBOL 2.7.8 binaries + docs (TLS-blocked); Internet Archive copies of rebol.com binaries (blocked); rebolsource.net Ren-C/R3 historical builds (blocked); www.rebol.tech (blocked)
- **Execution gaps**: No artifact executed; no bootstrap reproduction attempted (no interpreter obtainable) -> BOOTSTRAP_EXECUTED / BOOTSTRAP_REPRODUCED / any EXECUTED claim: NONE

## Integrity & License Status

| Status | Count |
|---|---|
| HASHED (all preserved artifacts) | 30 |
| HASH_MATCHED (git blob verification) | 3 |
| NO_REFERENCE_HASH | 1 |
| License CONFIRMED | 19 |
| License UNCLEAR | 2 |
| License MISSING | 1 |

## Recommended Next Steps

1. Re-run acquisition from an unrestricted network and download: official REBOL 2.7.8 binaries (rebol.com/pub/platforms), official Red binaries (static.red-lang.org/dl/auto/, incl. the build matching v0.6.6), Oldes/Rebol3 release assets, and Internet Archive copies of rebol.com for cross-hashing.
2. Execute Red v0.6.6 Linux binary and a Rebol 2.7.8 Linux x86-64 binary with full execution logs; verify `version.r` claims against interpreter output.
3. Reproduce the Red bootstrap: build red.bin from the v0.6.6 tree using an official Rebol 2.7.8 interpreter; compare output hashes with the official binary (expected non-reproducible; record NOT_REPRODUCED unless matched).
4. Diff the workspace fork against upstream v0.6.4 (253 differing files) to attribute fork modifications.
5. Verify Oldes/Rebol3 bundled extension licenses individually (repo license covers the core tree only).
6. Collect red/red git object bundle (full clone) when storage/network permits; this session's clones were blobless.
