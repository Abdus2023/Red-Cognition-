# Rebol & Red Acquisition — Collection Index

_Forensic acquisition per the "Rebol & Red Collection Agent — GitHub + Web Acquisition Protocol".
Final gate: **PARTIALLY_VERIFIED** (all GitHub-reachable material collected, pinned, and whole-tree
verified; every executable-binary channel is network-blocked from this environment — see
`logs/blocked-attempts.json` for all recorded attempts with verbatim errors)._

## Ledger

| Classification | Records |
|---|---|
| ARCHIVE (release/source trees, pinned + whole-tree verified) | 18 |
| BINARY (test fixtures; git-blob verified) | 4 |
| SOURCE (in-tree Red/System source) | 2 |
| TEST_SUITE | 2 |
| DOCUMENTATION | 5 |
| METADATA (registries, evidence, manifests) | 60 |
| **Total** | **92** |

## Layout

| Path | Contents |
|---|---|
| `red/releases/` | red/red tag archives v0.1.1 → v0.6.6 (12 tags; each whole-tree verified vs pinned commit) |
| `red/documentation/` | red/REP (BSD-3, in-tree LICENSE) + red/docs (license UNCLEAR) |
| `red/tests/` | Tier-1 test-fixture binaries from the v0.6.6 tree (git-blob verified) |
| `rebol/source/` | rebol/rebol (official R3), rebolsource/r3, ren-c, Oldes/Rebol3 (HEAD + release tag 3.22.1), rebol/projects |
| `rebol/documentation/` | rebolsource/rebol-syntax (license UNCLEAR) |
| `rebol/tests/` | rebolsource/rebol-test (official R2+R3 regression suite) |
| `manifests/` | authoritative evidence: artifacts.json (ledger), sha256sums.txt, verification + registry JSONs, reference-evidence/, history/, trees/ |
| `provenance/` | provenance graph + reconciliation tables (R1–R15) |
| `reports/` | collection-report.json (authoritative) + collection-report.md (with all stage addenda) |
| `logs/` | network events, search queries, blocked attempts (25+), execution evidence |
| `derived/` | ephemeral extraction area (gitignored; re-derivable via `acquisition-tools/common.py`) |

## Re-verification (any environment with GitHub access)

1. `sha256sum -c artifacts/manifests/sha256sums.txt` — evidence-layer integrity.
2. `acquisition-tools/reproduce_acquisition.sh` — re-downloads every archive from GitHub and
   whole-tree verifies against pinned refs (full re-derivation; codeload determinism already
   proven byte-identical on 2 samples).
3. `acquisition-tools/verify_tree.sh <clone> <ref> <archive>` — single-archive verifier.

## Key documented findings

- red/red GitHub releases carry **zero assets**; official binaries live on static.red-lang.org (blocked).
- Official CI downloads its Rebol bootstrap from `static.red-lang.org/tmp/rebol` (upstream URLs in `manifests/upstream-ci-rebol-urls.json`).
- Official Rebol 2.7.8 URL pattern: `rebol.com/downloads/v278/…` (official site source + distro recipes);
  reference hashes recorded: sha256 `b03b05fd…` (nix), md5 `97eb1a48…` (crux). License: **unfree EULA**.
- **Rebol 2.x source was never open-sourced**: no GitHub channel provides it (documented finding,
  `manifests/rebol2-source-finding.json`); only R3 lineage exists as source (Apache-2.0).
- red/red v0.6.4 commit independently confirmed by nixpkgs (`755eb943…`, MATCH).
- red tag v0.7 is a 2019 WIP side line, not a release (R10); ren-c has no versioned release tags
  (all its version-bearing tags are lineage-isolated build markers, R14).

## Status taxonomy

- provenance: VERIFIED / PARTIALLY_VERIFIED / PROVISIONAL / BLOCKED / UNVERIFIED / CONFLICTING
- integrity: HASHED / HASH_MATCHED / NO_REFERENCE_HASH
- license: CONFIRMED / PARTIALLY_CONFIRMED / UNCLEAR / MISSING
- bootstrap: BOOTSTRAP_CLAIMED + BOOTSTRAP_SOURCE_PRESENT only — nothing executed, NOT_REPRODUCED
