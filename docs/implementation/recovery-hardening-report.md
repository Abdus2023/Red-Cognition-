# Failure-Injection & Transactional-Recovery Hardening Report

**Date:** 2026-08-12 · **Controller:** 2.0.0 · **Phase:** Stage-5 transactional recovery
**Scope:** controller infrastructure only — no Red/Cognition product implementation.

## Central invariant (now mechanically enforced)

> CRASHING AT ANY POINT MUST NEVER TURN AN UNCOMMITTED OR UNVERIFIED EXECUTION
> INTO A TRUSTED IMPLEMENTATION RESULT.

## 1. State machine

```
DISCOVERED → PLANNED → READY → IN_PROGRESS → PASS   (terminal)
                              │            │
                              ↓            └──→ FAIL (reclassified)
                            BLOCKED
```

Explicit `ALLOWED_TRANSITIONS` (checkpoint.py). Security-critical: **PASS is
reachable ONLY via IN_PROGRESS** — never directly from READY, never from a
checkpoint `validated_pass` flag, never from an executor exit code alone.

## 2. Transaction boundaries (what is persisted)

| Boundary | Persisted? | Mechanism |
|---|---|---|
| `begin()` (READY→IN_PROGRESS) | **in-memory only** | not persisted until save (a crash leaves no false PASS) |
| evidence append | **durable** | flush + fsync + hash-chained JSONL line |
| `finish_pass/finish_fail` | in-memory | applied at next save |
| checkpoint save | **atomic** | temp → flush → fsync → `os.replace` |

PASS is **derived** every run from the evidence log + provenance; the checkpoint
is a cross-checked cache, never an authority.

## 3–4. Failure-injection matrix & crash points

(26 cases in `tests/test_recovery_attacks.py`; all PASS.)

| Crash point | Expected | Result |
|---|---|---|
| after contract, before executor | no PASS; READY/BLOCKED | ✅ |
| while IN_PROGRESS (in-memory) | no PASS; recoverable | ✅ |
| executor killed / timeout / no evidence | no PASS | ✅ |
| executor non-zero exit | FAIL evidence, no PASS | ✅ |
| evidence truncated / partial line | chain breaks; untrusted | ✅ |
| evidence committed, checkpoint not | evidence-authoritative PASS (true positive) | ✅ |
| checkpoint saved, evidence lost | demoted; no PASS | ✅ |
| checkpoint truncated / invalid JSON | rebuilt clean | ✅ |
| checkpoint PASS w/o evidence | demoted | ✅ |
| validator PASS, dies before evidence | no PASS | ✅ |
| stale-contract PASS | contract_id mismatch; no PASS | ✅ |
| SIGKILL mid-execution (subprocess) | no PASS; lease released; recoverable | ✅ |

## 5. Evidence commit semantics

`append()` writes one JSONL line, flushes, and fsyncs the fd. Evidence becomes
authoritative only after the durable write; a checkpoint may reference it only
afterwards. Duplicate `evidence_id` aborts the trusted chain at the duplicate.

**Durability guarantee provided:** flush + `fsync` (strongest the Python stdlib
exposes). This is durable against process crash/kill and OS crash, and is
**BEST-EFFORT / ENVIRONMENT-SPECIFIC** against power loss on filesystems/hardware
that lie about fsync. The fail-closed *semantic* (no false PASS on lost evidence)
is **REQUIRED** and holds regardless: lost evidence ⇒ no authoritative PASS ⇒
checkpoint claims demoted.

## 6. Checkpoint commit semantics

Atomic via temp file → flush → fsync → `os.replace`. A crash mid-write never
yields a half-written checkpoint: the previous checkpoint remains until the
rename completes atomically. Malformed/impossible checkpoints are rejected
(JSON/UTF-8 robust read) → rebuilt from evidence.

## 7. Recovery algorithm

`Controller.recover()` = `run(dry_run=False, execute=False)`: load manifest +
provenance context → compute authoritative PASS from the verified evidence chain
(contract_id match + closure + authority + deps) → demote any checkpoint PASS
not backed by valid evidence → invalidate stale READY/IN_PROGRESS → persist a
fresh atomic checkpoint. Executes nothing; duplicates no evidence.

## 8. Idempotence

`recover()` ×3 from identical failure states: identical normalized output, no
duplicate evidence, no resurrected invalid PASS, no altered valid PASS
(`F_Recovery.test_idempotent_recovery_no_duplicate_evidence`,
`DeterministicRecovery.test_three_recoveries_identical`). ✅

## 9. Concurrency

`fcntl.flock` exclusive lease on writes. Mutual exclusion proven; a process
killed (SIGKILL) releases the flock via OS semantics (the lock *file* may
remain but the lease dies with the process), so a retrying process acquires the
lease and recovers — no double execution, no duplicate PASS evidence. ✅

## 10–11. SIGTERM / SIGKILL

Real subprocess SIGKILL mid-execution (`ConcurrencyLease.test_sigkill_releases_lock`):
the killed controller left no evidence and no committed checkpoint; recovery
acquired the lease and the task was not PASS. SIGTERM/SIGKILL both release
`fcntl` locks on process death (REQUIRED, POSIX-guaranteed).

## 12. Corruption results

Zero-byte / half-JSON / invalid-UTF-8 / malformed hash / wrong prev_hash / wrong
record_hash / truncated checkpoint / duplicate evidence_id → all fail closed
(`Corruption`, `EvidenceDuplication`, `D_CheckpointCorruption`). ✅

## 13. Provenance preservation

After recovery, PASS still requires the v2.0 provenance chain (requirement,
spec, task, contract_id, manifest, repository, HEAD, validator, evidence,
closure) to agree. Recovered PASS retains closed traceability + provenance
context (`ProvenancePreservation`). ✅

## 14. Deterministic recovery

3 recoveries from an identical corrupted-checkpoint state produce identical
normalized task state / classification / contract identity / provenance /
traceability (timestamps may differ). ✅

## 15. CI

Self-test (now 163 cases incl. recovery/SIGKILL/corruption) + real-repo dry-run
+ determinism + repo-index PASS + RFC-0075 FAIL. SIGKILL is REQUIRED on Linux
runners; filesystem power-loss durability is labeled BEST-EFFORT/ENVIRONMENT-
SPECIFIC. No Rebol required.

## 16. Real-repository frontier

```
READY = 0   BLOCKED = 4   PASS = 0   FAIL = 0   IN_PROGRESS = 0   PAUSED = true
RED-LEX-001 / LIBRED-001 / HASH-001 / RFC0075-001 : BLOCKED (unchanged)
evidence integrity = true
```

## Defects found & fixed

| Defect | Reproducer | Root cause | Fix | Regression |
|---|---|---|---|---|
| non-atomic checkpoint | crash mid-`save` truncates | direct `write_text` | temp→flush→fsync→`os.replace` | `D_CheckpointCorruption` |
| non-durable evidence | append not fsynced | no fsync | flush+fsync on append | (semantic) `C_EvidenceCheckpointCommit` |
| duplicate evidence_id trusted | same id appended twice | no dup check | chain aborts at duplicate id | `EvidenceDuplication`, `test_e13` (updated) |
| implicit recovery only | no explicit entry | — | `Controller.recover()` | `F_Recovery`, `DeterministicRecovery` |
| illegal-transition undocumented | — | — | explicit `ALLOWED_TRANSITIONS` | `StateMachine` |

One existing test (`test_e13`) encoded the old "duplicates trusted" contract and
was updated to the new authoritative contract (duplicate = integrity failure).

## 17. Files changed

```
tools/impl_controller/checkpoint.py            (atomic save, ALLOWED_TRANSITIONS)
tools/impl_controller/evidence.py              (fsync, robust UTF-8 read, dup-id detection)
tools/impl_controller/controller.py            (recover())
tools/impl_controller/tests/test_recovery_attacks.py   (new, 26 cases)
tools/impl_controller/tests/test_hardening.py  (test_e13 → new dup-id contract)
docs/implementation/recovery-hardening-report.md (this report)
docs/implementation/pipeline-status.json       (regenerated)
.github/workflows/implementation-pipeline.yml  (recovery/durability CI labels)
```

## 18. Product scope

**No product implementation was performed.** Red implementation, Red tests,
runtime, RFC-0075, all RFCs/specifications, and traceability artifacts are
unchanged. Rebol/toolchain unchanged (still BLOCKED). RFC-0075 remains an
independent specification blocker.
