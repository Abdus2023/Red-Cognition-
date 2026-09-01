# Bootstrap Model Documentation

## Authoritative Bootstrap Status Summary

| Stage | Presence | Prerequisite | Executed | Result |
|---|---|---|---|---|
| **Stage 0** (Rebol 2 Interpreter) | PRESENT (binary in repo archive) | MET | BLOCKED (host 32-bit loader missing) | VERIFIED (Identity & SHA-256 confirmed) |
| **Stage 1** (Red Compiler Bootstrap) | PRESENT (`compiler.r`, `red.r`) | MET | HISTORICAL_EVIDENCE | MINIMALLY REPRODUCED |
| **Stage 2** (Red/System & Runtime Bootstrap) | PRESENT-LOCAL (249 `.reds` files) | MET | BLOCKED (Execution environment unavailable) | BLOCKED / PENDING |
| **Stage 3** (Red-Cognition Tooling) | PRESENT | NOT_MET | NOT_ATTEMPTED | BLOCKED-BY-STAGE-2 |

## Overall Bootstrap Chain Status

- **Complete bootstrap chain**: `PARTIALLY_VERIFIED`
- **Overall technical status**: `PARTIALLY_VERIFIED`
- **Authoritative Finding**: The repository contains the required Rebol, Red, and Red/System source foundation, but Stage 2 execution remains blocked because a usable Rebol 2 execution environment could not be established.

---

## Detailed Stage Analysis

### Stage 0: Rebol 2 Interpreter

- **Required Interpreter**: Rebol 2.7.8.4.3
- **Version**: 2.7.8.4.3 (6-Jan-2011)
- **Host Requirements**: 32-bit compatibility runtime (i386 architecture, `/lib/ld-linux.so.2`, `libc6:i386`, `libm.so.6`)
- **Target Platform**: Linux x86 (ELF32)
- **Input Artifacts**: Verified Rebol 2.7.8.4.3 binary
- **Expected Hashes**:
  - Rebol binary SHA-256: `1c902e0f75e994d739975e12963323832ce00f52208b3287cbfe5e7029d856d6`
  - Rebol archive SHA-256: `b0080df93905f56209875d811c6632c825c385e05d390b220c5d9555a8d38eee`
- **Identity Status**: `VERIFIED` (SHA-256 byte-identical to official release)
- **Execution Status**: `BLOCKED` in current host environment (64-bit Debian 12 without `libc6-i386` and network-isolated package management)

### Stage 1: Red Compiler Bootstrap

- **Required Interpreter**: Rebol 2.7.8.4.3 (Stage 0 output)
- **Version**: Red v0.6.6 (pinned)
- **Input Artifacts**: `%compiler.r`, `%red.r`, `%boot.red`
- **Output Artifacts**: Red executable, `libRedRT.so`
- **Authoritative Invocation Command**:
  ```bash
  printf 'A\n' | ./rebol --do "do/args %red.r \"%tests/hello.red\""
  ```
- **Historical Evidence**: Minimal build previously produced `hello` binary (102,980 bytes, SHA-256: `9e1ebb81...`) and `libRedRT.so`
- **Execution Status in Current Session**: `BLOCKED` (due to Stage 0 host runtime unavailability)
- **Status**: `MINIMALLY REPRODUCED`

### Stage 2: Red/System & Runtime Bootstrap

- **Required Components**: Red compiler (`%compiler.r`), Red/System compiler (`%system/compiler.r`), Red/System source files (249 `.reds` files)
- **Prerequisite Status**: `MET` (Red/System source present locally in repository under `.reds` extension)
- **Target Requirements**: Red/System compilation and runtime generation
- **Execution Attempt**:
  ```bash
  printf 'A\n' | ./rebol --do "do/args %red.r \"%tests/hello.red\""
  ```
  - **Exit Code**: `127`
  - **Stderr**: `/bin/bash: line 1: ./rebol: cannot execute: required file not found`
- **Failure Classification**: `HOST_LIMITATION` / `MISSING_DEPENDENCY` / `NETWORK_LIMITATION`
- **Status**: `BLOCKED / PENDING`

### Stage 3: Red-Cognition Tooling

- **Required Components**: Self-hosted Red runtime & compiler (Stage 2 output)
- **Input Artifacts**: Red-Cognition specifications, dialects, verification tools
- **Prerequisite Status**: `NOT_MET` (Requires Stage 2 execution verification)
- **Execution Status**: `NOT_ATTEMPTED`
- **Status**: `BLOCKED-BY-STAGE-2`

---

## Bootstrap Dependencies & Environmental Constraints

### Toolchain & Runtime Requirements

| Component | Required Version | Local Status | Execution Status |
|---|---|---|---|
| Rebol 2 Interpreter | 2.7.8.4.3 | PRESENT (archived) | BLOCKED (ELF32 loader missing) |
| Red Compiler Source | `compiler.r` | PRESENT (BSD-3) | AWAITING_STAGE_0 |
| Red/System Source | 249 `.reds` files | PRESENT-LOCAL | AWAITING_STAGE_0 |
| Dynamic Linker | `/lib/ld-linux.so.2` | MISSING (64-bit host) | BLOCKED |
| 32-bit glibc | `libc6:i386` | MISSING (offline/egress blocked) | BLOCKED |

### Network Isolation Evidence

| Upstream Endpoint | Purpose | Access Result |
|---|---|---|
| `http://www.rebol.com/downloads/v278/` | Official Rebol 2 binary | BLOCKED (curl exit 52 - empty reply) |
| `https://static.red-lang.org/tmp/rebol` | Upstream CI Rebol binary | BLOCKED (curl exit 35 - TLS failure) |
| `http://deb.debian.org/debian` | Debian `libc6-i386` package | BLOCKED (apt-get exit 100 - connection failed) |

---

## Offline & Epistemic Assessment

- **SOURCE-AVAILABLE**: `YES` (All Red, Red/System, and Rebol bootstrap sources and archived binaries are present)
- **BUILD-AVAILABLE**: `PARTIAL` (Minimal Red v0.6.6 bootstrap historically reproduced; Stage 2 pending execution)
- **BOOTSTRAP-AVAILABLE**: `BLOCKED` (Execution environment lacks 32-bit compatibility runtime)
- **FINAL EPISTEMIC STATUS**: `PARTIALLY_VERIFIED`
