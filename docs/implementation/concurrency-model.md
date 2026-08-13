# Concurrency Model (Stage-5, Phase 28)

**Date:** 2026-08-12 · **Controller:** 2.0.0

## Central invariant

> ONE AUTHORITATIVE CONTRACT → ONE VALID EXECUTION STATE → ONE CONSISTENT
> EVIDENCE HISTORY.

## Concurrency model: process-local exclusive serialization

The controller acquires an **exclusive fcntl.flock** (`FileLock`) for ALL
non-dry-run operations, serializing the ENTIRE run:
```
acquire lock → classify → execute → append evidence → checkpoint → release lock
```

### Guarantees provided (PROVEN BY TEST)

| Property | Mechanism | Status |
|---|---|---|
| **SERIALIZATION** | fcntl.flock exclusive (non-blocking); denied → FAIL | PROVEN BY TEST |
| **IDEMPOTENCY** | per-command skip (pass_command_ids); verified PASS not re-executed | PROVEN BY TEST |
| **ATOMICITY** | evidence: append+flush+fsync; checkpoint: temp→fsync→os.replace | PROVEN BY TEST |
| **CONSISTENCY** | _authoritative_pass fixpoint recomputes from evidence each run | PROVEN BY TEST |
| **CONVERGENCE** | sequential/recovery runs converge to identical normalized state | PROVEN BY TEST |

### Properties NOT claimed

- **Not linearizable across hosts** — the lock is local-filesystem advisory.
- **Not thread-safe within a process** — fcntl locks are per-process; the
  controller is designed for process-level invocation (subprocess/CLI), not
  in-process threading.
- **Power-loss durability BEST-EFFORT** — fsync provides process/OS-crash
  durability but not power-loss guarantees on all filesystems.

## Transaction sequence

```
BEFORE MUTATING AUTHORITATIVE STATE
    ↓
ACQUIRE EXCLUSIVE LOCK (fcntl.flock, non-blocking)
    ↓
REVALIDATE CONTRACT (contract_id, manifest, HEAD, provenance)
    ↓
CLASSIFY (from evidence + provenance fixpoint)
    ↓
EXECUTE OR SKIP (per-command idempotency)
    ↓
APPEND ATOMIC EVIDENCE (flush + fsync + hash chain)
    ↓
CHECKPOINT (atomic temp→fsync→rename)
    ↓
RELEASE LOCK (finally)
```

## Lock lifecycle

- Acquired at `run()` start for non-dry-run.
- Released in `finally` block.
- fcntl locks released by OS on process death (SIGTERM/SIGKILL).
- Stale lock files are harmless; new processes open the file and acquire a fresh flock.

## Concurrency invariants (CC-I1..I10)

| ID | Invariant | Status |
|---|---|---|
| CC-I1 | Single execution (at most one per contract) | PROVEN BY TEST |
| CC-I2 | Evidence atomicity (fully valid or absent) | PROVEN BY TEST |
| CC-I3 | Chain integrity (concurrent writes cannot corrupt) | PROVEN BY TEST (serialized) |
| CC-I4 | Contract revalidation (mutation during run invalidates) | PROVEN BY TEST |
| CC-I5 | Mutation wins (stale validation cannot win) | PROVEN BY TEST |
| CC-I6 | Recovery safety (cannot overwrite newer evidence) | PROVEN BY TEST |
| CC-I7 | Retry safety (no duplicate verified PASS) | PROVEN BY TEST |
| CC-I8 | Derived-state independence (races don't affect authority) | PROVEN BY TEST |
| CC-I9 | Convergence (different schedules → equivalent state) | PROVEN BY TEST |
| CC-I10 | Fail closed (ambiguous state never PASS) | PROVEN BY TEST |
