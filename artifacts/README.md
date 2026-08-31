# Rebol & Red Acquisition — Collection Index

_Forensic acquisition per the "Rebol & Red Collection Agent — GitHub + Web Acquisition Protocol".
Final gate: **PARTIALLY_VERIFIED** (all GitHub-reachable material collected, pinned, and whole-tree
verified; every executable-binary channel is network-blocked from this environment — see
`logs/blocked-attempts.json` for 21+ recorded attempts with verbatim TLS errors)._

## Layout

| Path | Contents |
|---|---|
| `releases/` (red) | red/red tag archives v0.6.3, v0.6.4, v0.6.5, v0.6.6 — each whole-tree verified against its pinned commit (git blob SHA-1 of every member == `git ls-tree`) |
| `source/` (rebol) | rebol/rebol @25033f89 (official R3), rebolsource/r3 @98cdfcd6, ren-c @e31d5698, Oldes/Rebol3 @d5b237ce, rebol/projects (historical org material) |
| `documentation/` (red) | red/REP @95d96a64 (BSD-3, in-tree LICENSE), red/docs @e6272166 (license UNCLEAR) |
| `documentation/` (rebol) | rebolsource/rebol-syntax @4ff11396 (license UNCLEAR) |
| `tests/` | rebolsource/rebol-test @409ef5c2; red test-fixture binaries @v0.6.6 (git-blob verified) |
| `manifests/` | machine-readable evidence (see below) |
| `provenance/` | provenance graph + reconciliation tables |
| `reports/` | collection-report.json (authoritative) + collection-report.md (human) |
| `logs/` | network events, search queries, blocked attempts, execution evidence |
| `derived/` | ephemeral extraction area (gitignored; re-derivable via `acquisition-tools/common.py`) |

## Key manifests

| File | Purpose |
|---|---|
| `manifests/artifacts.json` | **Authoritative artifact ledger** (56 records: 9 archives, 4 binaries) |
| `manifests/sha256sums.txt` | hash manifest over all committed evidence — `sha256sum -c artifacts/manifests/sha256sums.txt` |
| `manifests/git-collection.json` | clone evidence: HEADs, tag->commit/tree resolution, describe, per-ref tree manifests |
| `manifests/continuation-verification.json` | whole-tree archive verification results (10/10 HASH_MATCHED) |
| `manifests/red-tags-registry.json` / `oldes-tags-registry.json` / `ren-c-tags-registry.json` | complete tag registries with commit/tree/date/subject |
| `manifests/oldes-rebol3-releases-registry.json` | all releases + asset URLs/sizes (binaries blocked) |
| `manifests/upstream-ci-rebol-urls.json` | official CI's own Rebol download URLs (static.red-lang.org/tmp/rebol) |
| `manifests/fork-vs-upstream-v0.6.4.json` + `fork-diff-magnitudes.json` | workspace fork attribution vs upstream |
| `manifests/bootstrap-procedure-evidence.json` | verbatim line-numbered Rebol2/SDK bootstrap claims |
| `manifests/acquisition-determinism.json` | codeload re-fetch byte-identity proof (REPRODUCED) |

## How to re-verify (any environment with GitHub access)

1. `sha256sum -c artifacts/manifests/sha256sums.txt` — integrity of the evidence layer.
2. Whole-tree verification: `acquisition-tools/verify_tree.sh <clone-dir> <pinned-ref> <archive.tar.gz>`
   (recomputes git blob SHA-1 of every archive member vs `git ls-tree` of the ref).
3. Re-fetch any `releases/*.tar.gz` from `https://codeload.github.com/red/red/tar.gz/refs/tags/<tag>`
   and compare SHA-256 — proven byte-deterministic (2/2 samples).

## Status taxonomy in use

- provenance: VERIFIED / PARTIALLY_VERIFIED / PROVISIONAL / BLOCKED / UNVERIFIED / CONFLICTING
- integrity: HASHED / HASH_MATCHED / NO_REFERENCE_HASH
- license: CONFIRMED / PARTIALLY_CONFIRMED / UNCLEAR / MISSING
- bootstrap: BOOTSTRAP_CLAIMED + BOOTSTRAP_SOURCE_PRESENT only — nothing executed, NOT_REPRODUCED
