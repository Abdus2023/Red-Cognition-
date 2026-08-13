# Gate A — BLOCKED_TOOLCHAIN_ABSENT — Provisioning Request

**Date:** 2026-08-13T11:56:00Z
**Branch actual:** arena/019ffaed-red-cognition
**Branch requested:** arena/019ffad2-red-cognition — NOT FOUND REMOTELY (discrepancy reported)
**HEAD:** f860bbe075f26e0d3365c645d12a01097f81ef58 (audio)
**Controller:** impl_controller v2.0.0, 390/390 self-test PASS, frontier PAUSED, READY 0 BLOCKED 4
**Evidence integrity:** intact true, total_records 0

## Gate state machine observed

```
TOOLCHAIN_ABSENT
    |
    | executable discovered -> not observed
    v
TOOLCHAIN_PRESENT = false
    |
    v
VERSION_VERIFIED = false
    |
    v
COMPATIBILITY_VERIFIED = false
    |
    v
TOOLCHAIN_AUTHORIZED = false
    |
    v
READY = false
```

Result: GATE_A = BLOCKED_TOOLCHAIN_ABSENT

## Probes executed 2026-08-13

| Probe | Result |
|-------|--------|
| `which rebol` | absent |
| `/bin/rebol` `/usr/bin/rebol` `./rebol` | absent |
| `ls /lib/ld-linux.so.2` | absent — host has no 32-bit loader |
| `/lib64/ld-linux-x86-64.so.2 -> /lib/x86_64-linux-gnu/ld-linux-x86-64.so.2` | present (x86_64 only) |
| `uname -m` | x86_64 |
| `cat /etc/os-release` | Debian 12 bookworm |
| `curl http://static.red-lang.org/tmp/rebol` | Remote end closed / empty reply (curl 52) — egress-filtered |
| `curl https://static.red-lang.org/tmp/rebol` | TLS EOF / SSL error syscall (curl 35) — egress-filtered |
| Python socket to 149.202.86.195:80 | empty reply |
| Python socket to 149.202.86.195:443 with TLS | EOF |
| Python urllib http/https to same | Remote closed / TLS EOF |
| GitHub egress `api.github.com` | HTTP 200 (GitHub channel works, but no approved artifact per IMPLEMENTATION-BASELINE §C) |
| Tool registry `rebol-278` per controller | available:false, binary:"", evidence docs/IMPLEMENTATION-BASELINE.md §A,§G.1-G.4 |
| Controller `tool_path_available("rebol")` | shutil.which("rebol") = None |

This reproduces baseline §A,B,G classification.

## Required official artifact (authoritative)

- Red compiler/linker pinned to Rebol 2.7.8 per `build/build.r:50 if system/version = 2.7.8.3.1`
- README L191 links `rebol.com/downloads/v278/*`
- `.travis.yml` provisions `https://static.red-lang.org/tmp/rebol` (32-bit x86 ELF `/lib/ld-linux.so.2`)
- Official Linux artifacts from `rebol.com/download-view.html` are **Linux x86 (32-bit)** only: 2.7.8.4.2, 2.7.8.4.3, no x86_64 build
- R2 is closed-source — no source/bootstrap possible (baseline §G.2)
- R3 source exists but is **not authorized Red toolchain** (Red source R2-only)

## Minimal authorized provisioning action to make Gate A READY

**Option A — Approved 32-bit execution (preferred, matches CI):**

1. Place approved artifact, faithfully transferred (binary-identical), at repository root:
   - Path: `./rebol` or PATH `rebol`
   - Must be ELF 32-bit x86, interpreter `/lib/ld-linux.so.2`, linked against GLIBC_2.0/2.1
   - Executable bit set, runs `./rebol --version` or enters REPL `>>`
   - SHA-256 recorded in evidence
2. Provision host 32-bit compatibility (authorized):
   - `dpkg --add-architecture i386` + `apt-get install libc6-i386` OR equivalent,
   - OR `qemu-i386` + `binfmt_misc` shim, authorized as alternative execution,
   - Evidence: `ls -l /lib/ld-linux.so.2`, `ldd ./rebol` succeeds.
3. Authorization record updated in `docs/IMPLEMENTATION-BASELINE.md` or governance registry granting host 32-bit install.

**Option B — Approved 64-bit Rebol 2.7.8:**

- If an officially sanctioned 64-bit Linux build of Rebol 2.7.8 exists or is ratified, place it at same path, with same version check, no 32-bit libs needed, and record its provenance as approved.

**Option C — Faithful binary-transfer channel into sandbox:**

- Provide a channel that can carry the approved 32-bit artifact without markdown escaping / control-byte stripping (e.g., `curl` with proxy, `wget`, `git-lfs`, base64-encoded artifact verified by hash, or pre-placed in container image).
- Channel must be authorized and hash-verified — no lossy fetch_page.

**What NOT to do (forbidden):**

- Do not vendor arbitrary GitHub build/fork of Rebol/R3 (violates toolchain discipline §10, "install unauthorized dependencies").
- Do not use mocked executable that prints fake version.
- Do not substitute R3 / r3-make / Red binary for Rebol.
- Do not modify lexer.r / compiler.r / red.r to bypass Rebol.
- Do not manually set `available:true` in tool_registry without executable on PATH (controller checks ground truth via `shutil.which`).

## After provisioning

Once Gate A becomes READY:

1. Controller re-probe: `python3 tools/run-implementation-pipeline.py --dry-run` should show `RED-LEX-001` READY (or BLOCKED only by remaining declared blockers if any).
2. Execute: `python3 tools/run-implementation-pipeline.py --execute --allow-tool rebol-278`
3. Expected contract: `LEX-BASELINE` command `rebol -qws tests/source/compiler/lexer-test.r` exit 0
4. Evidence `EVD-RED-LEX-001` hash-chained:
   - task_id, requirement_ids, toolchain_identity (hash, version, arch), host_identity, command, exit_code, stdout, stderr, timestamp, environment, observed_state, verdict
5. Checkpoint, then LIBRED-001 (depends on RED-LEX-001 PASS) becomes frontier.

## RFC-0075 independent blocker (for completeness)

- Validation: `python3 tools/validate_rfc_0075_traceability.py` → FAIL (requirements 31 mapped 0 critical_gaps 4 conflicts 4)
- Conflicts: CONFLICT-0075-001 resolved 2026-08-13 (CADFP→CFCKEP terminology), CONFLICT-0075-002 discovery vs federation exchange, CONFLICT-0075-003 determinism/replay without canonical types, CONFLICT-0075-004 lifecycle 8-stage vs 5-stage, KnowledgeExchange vs KnowledgeExchangeObject, 5 profiles vs 3 profiles, parent title divergence.
- Gaps: GAP-0075-001 schemas/wire format, GAP-0075-002 lifecycle guards, GAP-0075-003 crypto trust, GAP-0075-004 replay boundary.
- Even with Gate A READY, RFC0075-001 remains BLOCKED_SPEC_CONFLICT per governance — must not implement disputed behavior; requires authoritative RFC reconciliation, not coding.

## Decision

**B — PROVISION** — No product code implementation authorized. Stop at Gate A. Preserve failure as evidence.

Next authorized transition: external provisioning of Rebol 2.7.8 as above.
