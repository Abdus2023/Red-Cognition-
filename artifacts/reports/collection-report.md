# Rebol & Red Collection Report

_Generated: 2026-08-31T17:53:04Z — acquisition per `Rebol & Red Collection Agent — GitHub + Web Acquisition Protocol`_

## Final Gate: **PARTIALLY_VERIFIED**

> Substantial verified evidence exists (official upstream identity, immutable tag/commit resolution, pinned-hash archives, git lineage proof). Verification is incomplete because **every executable-binary channel (static.red-lang.org, rebol.com, archive.org, GitHub release-asset CDN) is blocked by the sandbox egress allowlist** — no binary acquisition, execution, or bootstrap reproduction was possible. No status was promoted without evidence; `COMPLETE`/`VERIFIED` was therefore **not** claimed.

## Collection Summary

| Metric | Value |
|---|---|
| Rebol artifacts discovered (GitHub, evidence-backed) | rebol org: 2 repos; rebolsource org: 5 repos; 'rebol2' search: 6 repos (none is an official R2 source tree) |
| Red artifacts discovered (GitHub, evidence-backed) | red org: 33 repos (incl. official red/red) |
| Rebol artifacts collected | 16 |
| Red artifacts collected | 15 |
| Red/System artifacts collected | 3 |
| Related metadata records (tree manifests) | 13 |
| Git repositories collected | 7 upstream + 1 fork working tree |
| Release archives collected | 4 |
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
| RED | ARCHIVE | red-0.6.3.tar.gz | 0.6.3 | 6a43c767fa2e | 2ec78c1683a631494236… | VERIFIED | CONFIRMED |
| RED | METADATA | red-tags-registry.json | n/a | n/a | 6bf9b9c629d1a8dcf7a2… | VERIFIED | n/a |
| REBOL | METADATA | oldes-tags-registry.json | n/a | n/a | 9efbeee606c2e0dddf69… | VERIFIED | n/a |
| RED | METADATA | upstream-ci-rebol-urls.json | n/a | n/a | 7c74312bc784c30c4bda… | VERIFIED | n/a |
| REBOL | METADATA | oldes-bundled-license-evidence.json | n/a | n/a | d7bb7f730205c148f2a9… | VERIFIED | n/a |
| REBOL | METADATA | rebol-vs-rebolsource-r3-diff.json | n/a | n/a | 48313049963640c1f4d5… | VERIFIED | n/a |
| RED | ARCHIVE | red-0.6.5.tar.gz | 0.6.5 | 3bafef220366 | fdd330557b88406124cc… | VERIFIED | CONFIRMED |
| RED | METADATA | red-compiler-relocation.json | n/a | n/a | 39ce6f846a23abcec801… | VERIFIED | n/a |
| RED | METADATA | bootstrap-procedure-evidence.json | n/a | n/a | 88c5467799de85756a55… | VERIFIED | n/a |
| RED_SYSTEM | METADATA | red-system-inventory.json | n/a | n/a | 1f903aa9f3b50e3e58ff… | VERIFIED | n/a |
| RED | METADATA | fork-diff-magnitudes.json | n/a | n/a | 128fbdb0039c3d5bb12d… | VERIFIED | n/a |
| RELATED | METADATA | continuation-verification.json | n/a | n/a | 1269683304e5fbeee93a… | VERIFIED | n/a |
| RED | METADATA | fork-vs-upstream-v0.6.4.json | n/a | n/a | 7689d70f9866bc325d7d… | VERIFIED | n/a |

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
- **archive->git-tree (whole-tree verification)**: `red-0.6.6.tar.gz` → `pinned commit 6942c7a02125…` — git blob SHA-1 of all 673 archive members == git ls-tree blob SHAs of pinned commit
- **archive->git-tree (whole-tree verification)**: `red-0.6.4.tar.gz` → `pinned commit 755eb943ccea…` — git blob SHA-1 of all 538 archive members == git ls-tree blob SHAs of pinned commit
- **archive->git-tree (whole-tree verification)**: `rebol-rebol-25033f897.tar.gz` → `pinned commit 25033f897b2b…` — git blob SHA-1 of all 220 archive members == git ls-tree blob SHAs of pinned commit
- **archive->git-tree (whole-tree verification)**: `ren-c-e31d5698d.tar.gz` → `pinned commit e31d5698d736…` — git blob SHA-1 of all 1082 archive members == git ls-tree blob SHAs of pinned commit
- **archive->git-tree (whole-tree verification)**: `rebolsource-r3-98cdfcd6e.tar.gz` → `pinned commit 98cdfcd6e439…` — git blob SHA-1 of all 221 archive members == git ls-tree blob SHAs of pinned commit
- **archive->git-tree (whole-tree verification)**: `rebol-syntax-4ff113963.tar.gz` → `pinned commit 4ff11396312d…` — git blob SHA-1 of all 4 archive members == git ls-tree blob SHAs of pinned commit
- **archive->git-tree (whole-tree verification)**: `rebol-test-409ef5c22.tar.gz` → `pinned commit 409ef5c2270a…` — git blob SHA-1 of all 27 archive members == git ls-tree blob SHAs of pinned commit
- **fork->upstream (file-level attribution)**: `workspace fork 742181a` → `red/red tag v0.6.4 (755eb943)` — 251 identical / 258 differing / 609 fork-only / 29 missing; full lists in manifests/fork-vs-upstream-v0.6.4.json
- **archive->git-tree (whole-tree verification)**: `Oldes-Rebol3-d5b237cea.tar.gz` → `pinned commit d5b237cea60d…` — git blob SHA-1 of all 900 archive members == git ls-tree blob SHAs of pinned commit
- **archive->git-tree (whole-tree verification)**: `red-0.6.5.tar.gz` → `pinned commit 3bafef220366…` — git blob SHA-1 of all 638 archive members == git ls-tree blob SHAs of pinned commit 3bafef2203661bbcaafec8b859405ba7235a5981 (HASH_MATCHED (whole tree))
- **file-relocation**: `root compiler.r/lexer.r (v0.6.4)` → `encapper/compiler.r + encapper/lexer.r (v0.6.5)` — blob-sha genealogy: root files absent from v0.6.5; encapper/ copies present with DIFFERENT blob SHAs (content changed during move) — manifests/red-compiler-relocation.json
- **procedure-evidence**: `documented bootstrap/rebuild procedures` → `Rebol2/Rebol-SDK dependency claims` — verbatim quotes with line numbers + file hashes in manifests/bootstrap-procedure-evidence.json
- **archive->git-tree (whole-tree verification)**: `red-0.6.3.tar.gz` → `pinned commit 6a43c767fa2e…` — git blob SHA-1 of all 503 archive members == git ls-tree blob SHAs of pinned commit
- **ci-evidence**: `official red/red CI configs (pinned refs)` → `Rebol interpreter download/bootstrap URLs` — 8 CI files carry upstream URLs, e.g. v0.6.4 .travis.yml: 'curl -o /bin/rebol https://static.red-lang.org/tmp/rebol' (manifests/upstream-ci-rebol-urls.json)
- **bundled-license-evidence**: `Oldes/Rebol3 pinned tree (d5b237ce…)` → `bundled brotli/deflate/lz4 license material` — in-tree survey: license files + source-header copyright lines recorded with hashes (manifests/oldes-bundled-license-evidence.json)
- **tag-registry**: `red/red + Oldes/Rebol3 clones` → `complete tag registries` — 30 red tags + 30 Oldes tags with commit/tree/date/subject/file-count (manifests/*-tags-registry.json)

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
| Oldes bundled extension licenses (survey) | 4 LICENSE-type files found in committed tree (root LICENSE + NOTICE + more) | dirs with bundled third-party code but no LICENSE file remain UNCLEAR | PARTIAL (recorded) |

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

### R11 — Red compiler relocation genealogy

| Field | Source A | Source B | Result |
|---|---|---|---|
| v0.6.4 (2018) | root compiler.r 52749054…, root lexer.r 4ea75997…, root boot.red | - | BASELINE |
| v0.6.5 (2024 tag, no release) | root copies absent | encapper/compiler.r dfb08bcb… + encapper/lexer.r 0c0d7c83… (different SHAs => content changed in move) | RELOCATION + MODIFICATION |
| v0.6.6 (2025 release) | - | encapper/ copies b46486e3…/ae72c727… (further evolved) | CONTINUED |
| v0.7 (2019 WIP tag) | root compiler.r 5deb5448…, root lexer.r 0299995a… | - | OLD LINE (predates relocation) |

### R12 — Fork modification magnitude (workspace vs upstream v0.6.4)

| Field | Source A | Source B | Result |
|---|---|---|---|
| Differing files analyzed | 258 of 258 | {'light(<=10)': 67, 'moderate(<=100)': 99, 'heavy(>100)': 84, 'binary': 8} | RECORDED |
| Heaviest changes | modules/view/backends/windows/draw.reds (+2233/-3035); runtime/redbin.reds (+1985/-349); modules/view/backends/windows/base.reds (+993/-824) | full list in manifests/fork-diff-magnitudes.json | RECORDED |

### R8 — Continuation integrity verification (whole-tree)

| Field | Source A | Source B | Result |
|---|---|---|---|
| red-0.6.6.tar.gz | archive files=673 | tree entries=673 | HASH_MATCHED (whole tree) |
| red-0.6.4.tar.gz | archive files=538 | tree entries=538 | HASH_MATCHED (whole tree) |
| red-0.6.5.tar.gz | archive files=638 | tree entries=638 | HASH_MATCHED (whole tree) |
| red-0.6.3.tar.gz | archive files=503 | tree entries=503 | HASH_MATCHED (whole tree) |
| rebol-rebol-25033f897.tar.gz | archive files=220 | tree entries=220 | HASH_MATCHED (whole tree) |
| ren-c-e31d5698d.tar.gz | archive files=1082 | tree entries=1082 | HASH_MATCHED (whole tree) |
| rebolsource-r3-98cdfcd6e.tar.gz | archive files=221 | tree entries=221 | HASH_MATCHED (whole tree) |
| Oldes-Rebol3-d5b237cea.tar.gz | archive files=900 | tree entries=900 | HASH_MATCHED (whole tree) |
| rebol-syntax-4ff113963.tar.gz | archive files=4 | tree entries=4 | HASH_MATCHED (whole tree) |
| rebol-test-409ef5c22.tar.gz | archive files=27 | tree entries=27 | HASH_MATCHED (whole tree) |

### R9 — rebol/rebol vs rebolsource/r3 (both pinned)

| Field | Source A | Source B | Result |
|---|---|---|---|
| Tree content | identical=183 | differing=37; only-in-rebolsource=1 | MATCH (lineage: rebolsource/r3 HEAD is descendant; mostly identical) |

### R10 — red/red tag v0.7 anomaly

| Field | Source A | Source B | Result |
|---|---|---|---|
| Tag date | v0.7 -> commit abfa7aff dated 2019-09-11 (WIP: Win: Implementing TLS by Schannel.) | v0.6.6 released 2025-03-19 | CONFLICT (v0.7 tag predates v0.6.5/v0.6.6 in time; it is NOT a newer release line) |
| Commit deltas | v0.6.6..v0.7 = 23 commits; v0.7..v0.6.6 = 4939 commits | v0.7 is a diverged 2019 WIP line | RECORDED (facts only; no resolution asserted) |

### R13 — Upstream CI bootstrap URLs (pinned-tree evidence)

| Field | Source A | Source B | Result |
|---|---|---|---|
| v0.6.4 .travis.yml | # Linux: hook up qemu, build 32bit image including curl and rebol | - | EVIDENCE (upstream-authored URL) |
| v0.6.4 .appveyor.yml | ## Download Rebol v276 | - | EVIDENCE (upstream-authored URL) |
| v0.6.6 .appveyor.yml | ## Download Rebol v276 | - | EVIDENCE (upstream-authored URL) |
| v0.6.6 CI/Linux-32/Dockerfile | RUN apt-get update && apt-get -y install curl && curl -o /bin/rebol https://static.red-lang.org/tmp/rebol && chmod +x /b | - | EVIDENCE (upstream-authored URL) |
| v0.6.6 CI/Linux-gtk/Dockerfile | RUN apt-get update && apt-get -y install curl libcurl4 libgtk-3-0 xvfb && curl -o /bin/rebol https://static.red-lang.org | - | EVIDENCE (upstream-authored URL) |
| v0.7 .travis.yml | # Linux: hook up qemu, build 32bit image including curl and rebol | - | EVIDENCE (upstream-authored URL) |
| v0.7 .appveyor.yml | ## Download Rebol v276 | - | EVIDENCE (upstream-authored URL) |
| HEAD .appveyor.yml | ## Download Rebol v276 | - | EVIDENCE (upstream-authored URL) |

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
| HASHED (all preserved artifacts) | 33 |
| HASH_MATCHED (git blob verification) | 13 |
| NO_REFERENCE_HASH | 1 |
| License CONFIRMED | 21 |
| License UNCLEAR | 2 |
| License MISSING | 1 |

## Recommended Next Steps

1. Re-run acquisition from an unrestricted network and download: official REBOL 2.7.8 binaries (rebol.com/pub/platforms), official Red binaries (static.red-lang.org/dl/auto/, incl. the build matching v0.6.6), Oldes/Rebol3 release assets, and Internet Archive copies of rebol.com for cross-hashing.
2. Execute Red v0.6.6 Linux binary and a Rebol 2.7.8 Linux x86-64 binary with full execution logs; verify `version.r` claims against interpreter output.
3. Reproduce the Red bootstrap: build red.bin from the v0.6.6 tree using an official Rebol 2.7.8 interpreter; compare output hashes with the official binary (expected non-reproducible; record NOT_REPRODUCED unless matched).
4. Diff the workspace fork against upstream v0.6.4 (253 differing files) to attribute fork modifications.
5. Verify Oldes/Rebol3 bundled extension licenses individually (repo license covers the core tree only).
6. Collect red/red git object bundle (full clone) when storage/network permits; this session's clones were blobless.

## Continuation Addendum (stage 09)

_Generated: 2026-08-31T17:53:01Z_

### Release series complete: v0.6.3 collected

- `artifacts/red/releases/red-0.6.3.tar.gz` (1,748,647 B, sha256 `2ec78c1683a63149423661b35571ee4b74306217ab944b23f86efe7f0b216a6c`) → tag v0.6.3 commit `6a43c767…` (2017 release "macOS GUI backend", no assets). Whole-tree verification: **HASH_MATCHED (whole tree)** (503/503). Series 0.6.3→0.6.6 now fully collected; **10/10 preserved archives are whole-tree HASH_MATCHED**.

### Upstream CI bootstrap URLs (pinned-tree evidence, recon R13)

- `v0.6.4` `.travis.yml`:80 — “# Linux: hook up qemu, build 32bit image including curl and rebol”
- `v0.6.4` `.travis.yml`:89 — “curl -o /bin/rebol https://static.red-lang.org/tmp/rebol &&”
- `v0.6.4` `.appveyor.yml`:7 — “## Download Rebol v276”
- `v0.6.6` `.appveyor.yml`:7 — “## Download Rebol v276”
- `v0.6.6` `CI/Linux-32/Dockerfile`:3 — “RUN apt-get update && apt-get -y install curl && curl -o /bin/rebol https://static.red-lang.org/tmp/rebol && chmod +x /bin/rebol”
- `v0.6.6` `CI/Linux-gtk/Dockerfile`:4 — “RUN apt-get update && apt-get -y install curl libcurl4 libgtk-3-0 xvfb && curl -o /bin/rebol https://static.red-lang.org/tmp/rebol && chmod +x /bin/rebol”
- `v0.7` `.travis.yml`:102 — “# Linux: hook up qemu, build 32bit image including curl and rebol”
- `v0.7` `.travis.yml`:111 — “curl -o /bin/rebol https://static.red-lang.org/tmp/rebol &&”

These are **upstream-authored** URLs inside pinned official trees — stronger acquisition targets than third-party hints; all still unreachable from this sandbox (rechecked).

### Tag registries

- red/red: **30 tags** registered (commit/tree/date/subject/file-count) — e.g. v0.6.4=538 files, v0.6.5=638, v0.6.6=673.
- Oldes/Rebol3: **30 tags** registered.

### Oldes bundled third-party license evidence (in-tree)

- **brotli** (104 files): no LICENSE file. `src/core/brotli/common/constants.c:1` “/* Copyright 2013 Google Inc. All Rights Reserved.”
- **deflate** (41 files): src/core/deflate/COPYING. `src/core/deflate/common_defs.h:4` “* Copyright 2016 Eric Biggers”
- **lz4** (5 files): src/core/lz4/LICENSE. `src/core/lz4/lz4.c:3` “Copyright (c) Yann Collet. All rights reserved.”

### rebol/rebol vs rebolsource/r3 — full diff breakdown

- 37 differing files; by top dir: `{'src': 37}`; full blob-SHA pairs in `manifests/rebol-vs-rebolsource-r3-diff.json`.

### Status impact

- Final gate remains **PARTIALLY_VERIFIED**. Source-side verification now covers the complete collected series with whole-tree blob proof, complete tag registries, and upstream CI URL evidence for future binary acquisition.

## Continuation Addendum (stage 10)

_Generated: 2026-08-31T17:55:41Z_

### Acquisition reproducibility: REPRODUCED (codeload determinism)

- `red-0.6.6.tar.gz` and `red-0.6.3.tar.gz` were **re-fetched from codeload and are byte-identical** to the stored copies (SHA-256 match). Anyone with GitHub access can re-verify every recorded archive hash independently. Evidence: `manifests/acquisition-determinism.json`, `logs/execution/acquisition-determinism.log`.

### Official documentation repositories collected (Tier 1)

- **https://github.com/red/REP** — RED Enhancement Process; HEAD `95d96a64ab8c` (52 commits, 8 files); archive `red_rep-95d96a64a.tar.gz` (sha256 `4a8fa3a1143646af…`); license: **CONFIRMED** (metadata: BSD-3-Clause (repo metadata); in-tree: ['LICENSE'])
- **https://github.com/red/docs** — Red-related user documentation repository; HEAD `e62721663f34` (1271 commits, 325 files); archive `red_docs-e62721663.tar.gz` (sha256 `21d4024101e5e341…`); license: **UNCLEAR** (metadata: null (GitHub metadata); in-tree: no LICENSE file)

### Red test corpus inventory @ v0.6.6 (not executed)

- `tests/`: **172** files across 59 subdirs; largest: `tests/source` (105), `tests/libRed` (6), `tests/TUI` (5), `tests/align-test.red` (1)
- `quick-test/`: **8** files

### Report maintenance

- The base report's Version Matrix is now **derived dynamically from the artifact manifest** (8 archive rows), so it stays authoritative as the collection grows (0.6.3/0.6.5 rows no longer live only in addenda).

### Status impact

- Final gate remains **PARTIALLY_VERIFIED**. All GitHub-hostable material is collected or covered by pinned evidence; binaries/execution remain blocked.

## Continuation Addendum (stage 11)

_Generated: 2026-08-31T17:59:01Z_

### Release-asset registries (metadata persisted; downloads blocked)

- **Oldes/Rebol3**: all 29 releases + 1074 asset URLs/sizes persisted (`manifests/oldes-rebol3-releases-registry.json`) — durable acquisition targets.
- **ren-c**: 7 tags registered; merge-base ancestry shows **0/7 tags are reachable from ren-c master** (nor from the rebolsource/r3 fork point) — the atronix-* version tags are lineage-isolated build markers. ren-c master has **no versioned release tags** (recon R14).

### rebol/projects collected (official org, historical)

- HEAD `23a251573a49` archived (`rebol-projects-master.tar.gz`, sha256 `9478eb38a8f1ba75…`) + tree manifest. "Rebol related sources, but not part of build" (last push 2013-08-19).

### Collection index + verifier

- `artifacts/README.md` — layout, key manifests, **re-verification guide**, status taxonomy.
- `acquisition-tools/verify_tree.sh` — reusable whole-tree verifier (clone + ref + archive).

### Status impact

- Final gate remains **PARTIALLY_VERIFIED**. The acquisition layer is now self-describing: a third party can re-verify every claim from the repository alone.

## Continuation Addendum (stage 12)

_Generated: 2026-08-31T18:04:19Z_

### Reference-evidence registry (recon R15)

- 8 sources captured to `manifests/reference-evidence/` with hashes+quotes: **official red/web-red download page source (Tier 1)**, nixpkgs, CRUX ports (+md5sums), AUR, exercism runner, red-docker, TIO setup.
- **Cross-source identity MATCH**: nixpkgs pins red/red to rev `755eb943…` — byte-identical to our resolved v0.6.4 commit.
- **Reference hashes** for future download: rebol-core-278-4-2.tar.gz sha256 `b03b05fd070da8fa5186246a2febd02d7406305a65155cdaff3f1ac097b1757f` (nix, decoded) and md5 `97eb1a48…` (crux); view-278-4-2 md5 `86e33003…`.
- **License finding**: Rebol 2.7.8 is **unfree (custom REBOL EULA)** per nixpkgs+AUR — the bootstrap binary is NOT covered by Red's BSD/BSL; redistribution restricted.

### Official URL pattern corrected

- The official pattern is `rebol.com/downloads/v278/…` (confirmed by official site source + every distro recipe); the earlier `/pub/platforms/` targets came from outdated docs. All corrected URLs attempted: still TLS-blocked (logged).

### Vendored-binary sweep

- 6 repos swept via trees API: **no GitHub-hosted Rebol 2 binary exists** in them; all build recipes download from rebol.com at build time. qemu-i386: not installed. Execution/bootstrap reproduction remain NOT_PERFORMED — now proven by sweep, not assumed.

### Red tag-series completion: 8 archives collected, 8/8 whole-tree HASH_MATCHED

**v0.6.0** (428/428); **v0.6.1** (437/437); **v0.6.2** (470/470); **v0.5.4** (365/365); **v0.4.3** (323/323); **v0.3.3** (273/273); **v0.2.6** (129/129); **v0.1.1** (20/20)

red/red archive coverage now spans v0.1.1 → v0.6.6 (12 tag archives), every one pinned and whole-tree verified.

### Commit-history manifests

red.git=15921; rebol.git=308; r3.git=533; ren-c.git=10485; Rebol3.git=4675; rebol-syntax.git=45; rebol-test.git=460; REP=52; docs=1271; projects=4 — complete commit-SHA lists persisted as durable history-existence evidence.

### Status impact

- Final gate remains **PARTIALLY_VERIFIED**; acquisition targets for the binary phase are now exact (official URLs + reference hashes), so the next environment with egress can verify-or-fail immediately.

## Final Gate Summary (consolidated, stage 13)

_Generated: 2026-08-31T18:07:23Z. This section consolidates the protocol §22 fields as of the final stage; the per-stage addenda above remain the detailed record._

| Required field | Value |
|---|---|
| Rebol artifacts collected | 24 (incl. 1 UNVERIFIED lead binary, registries, reference evidence) |
| Red artifacts collected | 30 (12 release archives v0.1.1→v0.6.6, docs, fixtures) |
| Red/System artifacts collected | 3 (source + 97-file test suite @ v0.6.6, not executed) |
| Git repositories collected | 10 (7 primary + red/REP + red/docs + rebol/projects; all with HEAD/commit manifests, 32,844 commit SHAs persisted) |
| Release archives collected | 17 |
| Binaries collected | 4 verified test fixtures; interpreter binaries 0 (blocked) |
| Source trees collected | 17 pinned archive trees + workspace fork tree |
| Third-party artifacts | ren-c, Oldes/Rebol3, rebolsource/*, workspace fork (all marked) |
| Unresolved artifacts | rebol-2.7.8 prior-session lead (UNVERIFIED); red/docs + rebol-syntax licenses (UNCLEAR); Oldes version-scheme conflict (R4); v0.7 tag anomaly (R10); ren-c tag isolation (R14) |
| Whole-tree HASH_MATCHED archives | 22 |
| Execution evidence | hash-manifest self-checks + codeload determinism re-fetch (2/2); NO interpreter executed |
| Reproducibility | acquisition layer REPRODUCED (byte-identical re-fetch); language build NOT_REPRODUCED (no attempt possible) |
| **Final gate** | **PARTIALLY_VERIFIED** |

**Remaining BLOCKED work (with exact targets prepared):** rebol.com/downloads/v278/ binaries (reference hashes ready), static.red-lang.org Red binaries + CI Rebol bootstrap, GitHub release assets (29 releases/1,074 assets registered), Internet Archive copies; then execution + bootstrap reproduction per `logs/execution/execution-evidence.json` next steps.

## Continuation Addendum (stage 14)

_Generated: 2026-08-31T18:11:00Z_

### Reproduction: executed end-to-end (execution evidence)

- `reproduce_acquisition.sh` **was executed**: 10 fresh clones, **22/22 archives re-downloaded and whole-tree verified against pinned refs**, exit 0, 19s. Log with per-archive SHA-256s: `logs/execution/reproduction-run.log`. Claim upgraded: acquisition **REPRODUCED end-to-end by the committed script** (previously only 2 samples).

### Historical material: red/RS-fossil-mirror collected (Tier-2, THIRD_PARTY)

- Mirrors of the **Fossil repositories at red.esperconsultancy.nl** (Red's pre-GitHub primary hosting; pushes ceased 2015-03-23). Org-hosted but a fork of `kealist/RS-fossil-mirror`; 148 entries across 17 projects (6502, C-library, GLib, GTK, GTK-Champlain, GTK-WebKit, JSON, Java…). License UNCLEAR at mirror level; marked THIRD_PARTY.

### Fork attribution refined

- Of the workspace fork's 258 differing files: **87 match upstream v0.6.5 exactly**, **0 match v0.6.6 exactly** (forward-ported upstream code), **171 are fork-original modifications**.

### Egress recheck

- rebol.com/downloads/v278/… still blocked (curl exit 52).

### Status impact

- Final gate remains **PARTIALLY_VERIFIED**; the reproduction dimension is now execution-proven for the acquisition layer.

