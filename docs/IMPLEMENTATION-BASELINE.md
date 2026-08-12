# Implementation Baseline — Existing Red Toolchain

**Date:** 2026-08-12  
**Selected unit:** tooling bootstrap for the existing lexer/compiler test baseline  
**Implementation status:** BLOCKED — no source behavior was changed.

## Authority and selected scope

- `README.md` lines 185–205 documents running Red from source with a Rebol interpreter placed at repository root and invokes tests through `do/args %red.r`.
- `build/README.md` documents the Rebol SDK requirement for rebuilding a Red binary.
- `CONTRIBUTING.md` requires Quick Test coverage for code changes.
- Selected existing behavioral unit: `lexer.r`, exercised by `tests/source/compiler/lexer-test.r`.

No failing lexer behavior or documented missing lexer rule was identified during source review. Therefore no lexer implementation or test was invented.

## Baseline observations

| Check | Result |
|---|---|
| `red`, `r3`, or `rebol` executable available in checkout/PATH | No |
| Existing lexer test harness | `tests/source/compiler/lexer-test.r` (Rebol/Quick Test) |
| Test runner execution | Blocked: documented interpreter unavailable |
| Bootstrap attempt | Blocked: the documented Rebol download endpoints returned transport errors in this environment (`curl` error 52 over HTTP; error 35 over HTTPS) |
| Repository source modification | None |

## Required external prerequisite

Provide a working, compatible Rebol interpreter/toolchain as documented in `README.md`, or provide an approved accessible mirror/package source. Then run the existing baseline command from the README before selecting a defect-driven lexer change.

## Traceability

| Work item | Documentation | Existing source/test |
|---|---|---|
| Tooling bootstrap | `README.md` “Running Red from the sources”; `build/README.md` | `red.r`, `tests/source/compiler/lexer-test.r` |
| Lexer behavior (not modified) | `docs/specifications/red-deep-technical-spec/04-red-system-bnf-grammar.md` | `lexer.r` |

This baseline deliberately does not begin RFC-0075 implementation: its traceability package records unresolved schema, lifecycle, cryptographic, replay, and source-authority blockers.

## Approved-artifact workspace gate (continued inspection)

A repository-local inspection was completed before any further network bootstrap attempt:

| Search area | Result |
|---|---|
| executable candidates named `rebol`, `r3`, or `red` | None present in the workspace |
| vendored `.zip`, `.tar`, `.tar.gz`, `.tgz`, or `.7z` archives | None present in the workspace |
| local SDK/toolchain/bootstrap directories | None present in the workspace |
| CI/container definitions | `.travis.yml` and `.appveyor.yml` are present; no vendored artifact is present |

The CI definitions document a Red-hosted external provisioning path: `.travis.yml` downloads `https://static.red-lang.org/tmp/rebol` to `/bin/rebol` for its Linux CI container, while `.appveyor.yml` provisions a Windows `rebview.exe`. These are provenance evidence for CI, not already-present workspace artifacts. This baseline gate does not substitute or download an artifact without an explicitly available approved artifact input.

**Classification: BLOCKED — external prerequisite unavailable.** No artifact record, executable verification, or lexer harness execution can be produced because no compatible interpreter artifact is available locally. `lexer.r` and `tests/source/compiler/lexer-test.r` remain unchanged.
