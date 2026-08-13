# Implementation Baseline — Existing Red Toolchain

**Date:** 2026-08-12  
**Last re-verification pass:** 2026-08-12 (toolchain new-evidence check; see §“Re-verification pass” below)  
**Selected unit:** tooling bootstrap for the existing lexer/compiler test baseline  
**Implementation status:** BLOCKED — no source behavior was changed. (Re-verification confirmed the blocker persists and refined its prerequisite; no feature/test/source change resulted.)

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

> **Refined by the 2026-08-12 re-verification pass (below):** the prerequisite is more precisely an **explicitly-approved, 64-bit-compatible Rebol interpreter materialized as an executable in this workspace** (or an approved authorization to install host 32-bit compatibility on top of the documented 32-bit artifact). Reachability of the upstream artifact is *not* the limiting factor; see below.

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

## Re-verification pass — new-evidence check (2026-08-12)

A full task-discovery + toolchain new-evidence re-probe (§18) was executed this cycle. The blocker PERSISTS, but its prerequisite is now precisely characterized. **No source, test, RFC, or specification file was changed by this pass; this section records evidence only.** No lexer implementation or test was invented.

### A. Local toolchain re-probe

| Probe | Result |
|---|---|
| `rebol`, `rebol-core`, `red`, `r3`, `r3-make`, `redbin` in PATH | Absent (all) |
| Vendored binaries / archives / SDK dirs in workspace | None |
| C toolchain present | `gcc` 12.2.0, GNU `make` 4.3, `ld`, `cc`, `git` 2.39.5, `python3` 3.11.2 |
| Host architecture | `x86_64` |
| 32-bit execution capability | **Absent** — no `/lib/ld-linux.so.2`, no `/lib32`, no `libc6-i386`, no `dpkg` foreign arch |

### B. Approved-artifact reachability (refined)

| Channel | Result |
|---|---|
| Raw `curl` HTTP to `static.red-lang.org` | **Empty reply (curl 52)** — egress-filtered; reproduces baseline |
| Raw `curl` HTTPS to `static.red-lang.org` / `rebol.com` / `google.com` | **TLS reset (curl 35, SSL_ERROR_SYSCALL)** — egress-filtered; reproduces baseline |
| DNS + TCP | `static.red-lang.org`→149.202.86.195; TCP 80/443 connect succeed, but payload is reset |
| Sandbox `fetch_page` tool (egress channel) to documented URL `https://static.red-lang.org/tmp/rebol` | **Succeeded** — artifact IS reachable upstream. Returned an **ELF 32-bit x86** image (`/lib/ld-linux.so.2`, `GLIBC_2.0/2.1`, `__libc_start_main`), i.e. exactly the artifact `.travis.yml` provisions. **However `fetch_page` returns markdown-escaped text and is not a faithful binary-transfer channel** — bytes are lossy (null/control bytes stripped, backslash escaping); a runnable interpreter cannot be reconstructed from it. |

### C. Alternate channels

| Channel | Result | Authorization |
|---|---|---|
| GitHub egress | `github.com`→HTTP 200; `api.github.com`→HTTP 200; `git ls-remote https://github.com/red/red.git HEAD`→`3ccdacd…` (succeeds) | Egress works, **but no GitHub-hosted Rebol is an approved artifact** under the authority hierarchy. The approved provisioning path is the documented CI source (`static.red-lang.org`). Pulling an arbitrary GitHub build/fork would violate toolchain discipline (§10) and “install unauthorized dependencies”. |
| 32-bit host compatibility | Not installable without `apt`/external packages — itself an unauthorized dependency provisioned outside the approved artifact input | Not authorized |

### D. Classification after re-verification

`TOOLCHAIN_BOOTSTRAP` — **BLOCKED (persists).** The limiting factor is **not** upstream reachability (the approved artifact exists and is fetchable upstream); it is the combination of (1) no faithful binary-transfer channel into this sandbox for the approved artifact, and (2) the host being 64-bit-only while the documented artifact is a 32-bit ELF. A 32-bit execution layer is not present and is not authorized.

### E. Effect on independent scopes

- **RFC-0075 CFCKEP:** unaffected by toolchain; remains **BLOCKED — SPECIFICATION_CONFLICT / INCOMPLETE_SPECIFICATION**. `tools/validate_rfc_0075_traceability.py` re-run this cycle → requirements 31 / mapped 0 / orphaned 31 / critical gaps 4 / conflicts 4 → **FAIL** (consistent with `docs/traceability/rfc-0075/{15-gaps,16-conflicts}.md`).
- **Runtime `/hash`:** implementation/validation path runs through the Red runtime compile (Rebol-driven); transitively toolchain-blocked in addition to its own specification incompleteness. **BLOCKED.**
- **Cognition runtime RFCs (RFC-0061 CISA … RFC-0064 CCC-VTP, ratified):** per RFC-0050 §1–§2 the CVM/CISA substrate is the Red runtime; no alternative substrate is authorized. **Transitively BLOCKED — TOOLCHAIN_BOOTSTRAP.**
- **Repository integrity / indexing infrastructure:** re-run this cycle — `tools/validate_repository_index.py` → **PASS** (338/338 indexed, 92 RFC files, 75 unique RFC ids, 39 wiki pages). No defect found; no repair warranted.

### F. Unchanged files

`lexer.r`, `compiler.r`, `red.r`, `runtime/**`, `tests/source/compiler/lexer-test.r`, all `rfcs/**`, all `specs/**`, all `docs/specifications/**`, all `docs/traceability/**` — unchanged by this pass.

## Toolchain resolution investigation (2026-08-12)

A focused toolchain-resolution probe (per the Toolchain Unblock Agent directive) examined whether an approved, reproducible, architecture-compatible Rebol execution path can be established. **Verdict: none exists.** No toolchain was provisioned; no test was executed.

### G.1 What Red requires (authoritative)
- Red’s compiler/linker are Rebol-2 and pinned to **2.7.8**: `build/build.r:50 if system/version = 2.7.8.3.1`; README L191 links `rebol.com/downloads/v278/*`; `.travis.yml` provisions 32-bit R2 (`static.red-lang.org/tmp/rebol`). R2 is the approved toolchain.

### G.2 Candidate inventory (each recorded with provenance/compat/authorization)
- **Official R2 278 Linux artifacts** (`rebol.com/download-view.html`): all Linux rows are **“Linux x86” (32-bit)** — 2.7.8.4.2 (libc6 2.3), 2.7.8.4.3 (libc6 2.5), 2.7.8.4.8 (ARM). **No x86_64/64-bit R2 Linux build exists.** Provenance: official. Host compat: **INCOMPATIBLE (32-bit).** Authorization: approved but unobtainable.
- **R2 source / buildable bootstrap:** none — Rebol 2 is closed-source, distributed as prebuilt binaries only (`rebolsource/rebol` → GitHub 404; community authority: “no open source compiler for Rebol [2]”). Priority-3 (source + bootstrap) **impossible** for R2.
- **`rebol/rebol` (official R3 source) releases:** `gh api repos/rebol/rebol/releases` → **no binary release assets**. R3 build requires a prebuilt `r3-make` bootstrap (4 code refs in tree; circular bootstrap). R3 is **not an authorized Red toolchain** (Red source is R2-only; no R3 build path; would alter the approved toolchain without authorization).
- **`red/red` vendored bootstrap:** `gh api repos/red/red/git/trees/master?recursive=1` filtered for `rebol`/`r3` → **none** (no vendored interpreter in the tree).

### G.3 Channel matrix (binary-transfer feasibility)
| Channel | Reachable | Faithful binary transfer? |
|---|---|---|
| `github.com` / `api.github.com` | HTTP 200 | HTML/JSON only; no binary CDN |
| `git clone` (git protocol) | works | **yes** — but no official repo vendors the R2 binary |
| `static.red-lang.org` | curl 52 (HTTP) / 35 (HTTPS) | blocked |
| `rebol.com` | curl 35 | blocked |
| `raw.githubusercontent.com` | curl 35 | blocked |
| `objects.githubusercontent.com` (release CDN) | curl 35 | blocked |
| `fetch_page` (sandbox egress) | retrieves text | **no** — markdown-escapes bytes, lossy |

### G.4 Host capability
x86_64; no `/lib/ld-linux.so.2`, no `/lib32`/`/usr/lib32`, no `libc6-i386`, no qemu-user, no binfmt 32-bit registration. `dpkg`/`apt` present but **installing 32-bit compat is unauthorized**.

### G.5 Classification
`TOOLCHAIN_BOOTSTRAP` — **BLOCKED — ARCHITECTURE** (primary: the only approved artifact family, R2 278, exists solely as 32-bit ELF; this 64-bit-only host cannot execute it; no official 64-bit R2 exists; R2 has no buildable source). Compounded by **PROVISIONING** (all official binary sources egress-blocked; no faithful channel carries an approved binary), **BOOTSTRAP** (R2 closed-source/binary-only; R3 circular and unauthorized), and **AUTHORIZATION** (no grant to install 32-bit compat or to substitute R3/unofficial Rebol).

### G.6 Required unblock input (exact)
One of, explicitly authorized:
1. A 64-bit (x86_64) Rebol 2.7.8-compatible interpreter placed at repository root — **such an artifact is not known to exist upstream**; or
2. Authorization + provisioning of host 32-bit compatibility (`libc6-i386`/`/lib/ld-linux.so.2`) so the approved 32-bit R2 artifact can execute; or
3. An explicit authorized decision to switch Red’s toolchain to Rebol 3 **and** an approved `r3-make` bootstrap artifact faithfully materialized in-sandbox; or
4. An explicitly authorized approved provisioning source/mirror that is reachable through a faithful binary channel in this environment.

No source, test, RFC, specification, or traceability file was changed by this investigation.
