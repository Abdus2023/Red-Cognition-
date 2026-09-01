# Provenance Documentation

## Repository Provenance

This repository (`Abdus2023/Red-Cognition-`) preserves the complete technical lineage from Rebol through Red to Red-Cognition, with explicit provenance recording for all imported or retained upstream artifacts.

## Rebol Provenance

| Artifact | Origin | Upstream URL | Retrieval Date | SHA-256 | Provenance Confidence |
|---|---|---|---|---|---|
| Rebol 2.7.8.4.3 binary | Rebol project | `http://www.rebol.com/downloads/v278/rebol-core-278-4-3.tar.gz` | 2026-08-31 | `1c902e0f75e994d739975e12963323832ce00f52208b3287cbfe5e7029d856d6` | IDENTITY_CONFIRMED |
| Rebol archive | Rebol project | `http://www.rebol.com/downloads/v278/rebol-core-278-4-3.tar.gz` | 2026-08-31 | `b0080df93905f56209875d811c6632c825c385e05d390b220c5d9555a8d38eee` | ACQUIRED |
| Rebol executable | Rebol project | Same as above | 2026-08-31 | `1c902e0f75e994d739975e12963323832ce00f52208b3287cbfe5e7029d856d6` | BYTE_FOR_BYTE_IDENTITY |

**Rebol Provenance Notes**:
- Downloaded archive has SHA-256 `b0080df93905f56209875d811c6632c825c385e05d390b220c5d9555a8d38eee` and MD5 `0918513c5e30209c36a88bcf446ddd77`
- Extracted executable has SHA-256 `1c902e0f75e994d739975e12963323832ce00f52208b3287cbfe5e7029d856d6`
- Byte-identical to the known verified reference hash
- Current session execution blocked by host 32-bit ELF loader absence

## Red Provenance

| Artifact | Origin | Upstream URL | Version | License | Provenance Confidence |
|---|---|---|---|---|---|
| `compiler.r` | Red Foundation | `https://github.com/red/red` | N/A (in-repo) | BSD-3 | PRESERVED |
| `red.r` | Red Foundation | `https://github.com/red/red` | N/A (in-repo) | BSD-3 | PRESERVED |
| `boot.red` | Red Foundation | `https://github.com/red/red` | N/A (in-repo) | BSL-1.0 | PRESERVED |
| `libRed/libRed.red` | Red Foundation | `https://github.com/red/red` | N/A (in-repo) | BSL-1.0 | PRESERVED |
| `system/compiler.r` | Red Foundation | `https://github.com/red/red` | N/A (in-repo) | BSD-3 | PRESERVED |
| Red v0.6.6 release | Red Foundation | `https://github.com/red/red/releases/tag/v0.6.6` | v0.6.6 | BSL-1.0 | PINNED |

**Red Provenance Notes**:
- `compiler.r` header: "Copyright (C) 2011-2018 Red Foundation. All rights reserved. License: BSD-3"
- `red.r` header: "Copyright (C) 2011-2018 Red Foundation, Andreas Bolka. All rights reserved. License: BSD-3"
- `system/compiler.r` header: "Copyright (C) 2011-2018 Red Foundation. All rights reserved. License: BSD-3"
- `boot.red` header: "Copyright (C) 2011-2018 Red Foundation. All rights reserved. License: Boost Software License, Version 1.0"
- `libRed/libRed.red` header: "Copyright (C) 2016-2018 Red Foundation. All rights reserved. License: Boost Software License, Version 1.0"

## Red-System Provenance

| Artifact | Origin | Status | File Count |
|---|---|---|---|
| Red/System source files | Red Foundation | PRESENT-LOCAL (`.reds` extension) | 249 `.reds` files |
| System compiler & runtime | Red Foundation | PRESENT-LOCAL (`system/` directory) | 70 `.reds` files |
| Red runtime descriptions | Red Foundation | PRESENT-LOCAL (`runtime/` directory) | 106 `.reds` files |
| Module runtime backends | Red Foundation | PRESENT-LOCAL (`modules/` directory) | 63 `.reds` files |

**Red-System Notes**:
- Red/System source is PRESENT in the repository under the `.reds` extension (not `.rs`).
- Previous "MISSING" classification was an inventory search error looking for `.rs` instead of `.reds` (per Red/System specification section 17.1).
- 249 total `.reds` files are present across `environment/`, `modules/`, `quick-test/`, `runtime/`, `system/`, and `tests/`.

## Bootstrap Lineage & Stage Status

| Stage | Required Interpreter | Input Artifacts | Output Artifacts | Epistemic Status |
|---|---|---|---|---|
| **Stage 0** (Rebol 2) | Rebol 2.7.8.4.3 | Verified binary | `do/args %red.r "..."` capability | VERIFIED (Identity confirmed; host execution blocked) |
| **Stage 1** (Red compiler) | Rebol bootstrap | `%compiler.r`, `%red.r` | `hello` binary + `libRedRT.so` | MINIMALLY REPRODUCED |
| **Stage 2** (Red/System & Runtime) | Red compiler | 249 `.reds` files | Self-hosted Red compiler & runtime | BLOCKED / PENDING |
| **Stage 3** (Red-Cognition) | Red runtime | Red scripts, specs | Verification reports | BLOCKED-BY-STAGE-2 |

## Authoritative Finding

> The repository contains the required Rebol, Red, and Red/System source foundation, but Stage 2 execution remains blocked because a usable Rebol 2 execution environment could not be established.
