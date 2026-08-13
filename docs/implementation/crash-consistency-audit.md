# Crash-Consistency Audit (Stage-5)

**Date:** 2026-08-12 · **Controller:** 2.0.0 · **Phase:** audit only (no code changes here)

This audit enumerates every durable artifact, in-memory transition, persistence
boundary, and crash window in the Stage-5 pipeline, and classifies each artifact
as AUTHORITATIVE, DERIVED, NEVER AUTHORITATIVE, or UNKNOWN (fail-closed).

## 1. Durable artifacts (on disk)

| Artifact | Path (default) | Class | Written by |
|---|---|---|---|
| implementation plan | `docs/implementation/implementation-plan.json` | **AUTHORITATIVE** (planner) | planner (human/approved) |
| evidence chain | `.impl_controller/evidence.jsonl` (configurable) | **AUTHORITATIVE** | controller executor (append+fsync) |
| repository identity | `<repo>/.impl_controller/repo.identity` | AUTHORITATIVE (identity) | controller (first run) |
| checkpoint | `<state>` (default `.impl_controller/state.json`) | **DERIVED** (cache) | controller `StateStore.save` |
| checkpoint temp | `<state>.tmp` | transient | controller (atomic-rename scratch) |
| execution lock | `<state dir>/controller.lock` | DERIVED (lease) | controller `FileLock` |
| pipeline-status | `docs/implementation/pipeline-status.json` | **DERIVED** | pipeline runner |
| traceability report | (inside pipeline-status / controller report) | **DERIVED** | controller |
| repository HEAD | git object DB | AUTHORITATIVE (state) | git |

## 2. In-memory state transitions (not persisted until a boundary)

| Transition | API | Persisted? |
|---|---|---|
| READY → IN_PROGRESS | `StateStore.begin()` | **in-memory only** (until `save`) |
| IN_PROGRESS → PASS | `StateStore.finish_pass()` | in-memory (until `save`) |
| IN_PROGRESS → FAIL | `StateStore.finish_fail()` | in-memory (until `save`) |
| reclassification (BLOCKED/READY/…) | `StateStore.invalidate_stale()` | in-memory (until `save`) |
| contract build | `build_execution_contract()` | in-memory (report only) |
| classification | `classify_all()` | in-memory (recomputed each run) |
| READY queue / traceability | controller report | in-memory (DERIVED) |

Key: a crash between `begin()` and `save()` leaves **no** persisted IN_PROGRESS,
so it can never manufacture PASS.

## 3. Persistence / fsync / atomic-rename boundaries

| Boundary | Mechanism | Crash window |
|---|---|---|
| evidence commit | `EvidenceLog.append`: write line → `flush` → `fsync` | a crash before fsync ⇒ line may be lost ⇒ no authoritative PASS (fail-closed) |
| checkpoint commit | `StateStore.save`: temp → `flush` → `fsync` → `os.replace` | `os.replace` is atomic; a crash leaves either the old or the new checkpoint, never a partial file; a stale `.tmp` is ignored by `load` and overwritten next save |
| pipeline-status | runner writes whole file (non-atomic) | **DERIVED** — corruption/loss never affects PASS (controller never reads it) |

## 4. Lock acquisition / release

- `FileLock` (`fcntl.flock`, exclusive) acquired in `run()` for non-dry-run writes;
  released in `finally`. Lease path = `<state dir>/controller.lock`.
- POSIX guarantee: `flock` is released by the OS on process death (SIGTERM/SIGKILL).
  The lock *file* may remain after SIGKILL, but the lease is free; a retrying
  process opens the existing file and acquires the flock.
- Mutual exclusion therefore holds across crashes (REQUIRED, POSIX).

## 5. Evidence commit semantics

`append` is the **only** path that creates authoritative execution evidence. A
record is authoritative only after flush+fsync and only if the hash chain
(`prev_hash`/`record_hash`) verifies from the genesis record, with no duplicate
`evidence_id`. PASS reads only `verified_records()`.

## 6. Checkpoint commit semantics

Atomic temp→fsync→rename. The checkpoint is a **cache** of derived state; on
every run it is cross-checked against the authoritative evidence chain
(`_authoritative_pass`) and any checkpoint PASS not backed by valid evidence is
**demoted**. Corrupt/truncated/invalid-JSON checkpoints are rejected
(`StateStore.load` → clean rebuild).

## 7. Derived artifacts

checkpoint · READY queue · pipeline-status.json · traceability report · contract
(report). All are regenerated from authoritative inputs each run.

## 8. Recovery paths

- `Controller.recover()` = `run(dry_run=False, execute=False)`: load plan +
  provenance → recompute authoritative PASS from verified evidence (contract_id
  match + closure + authority + deps) → demote unbacked checkpoint PASS →
  invalidate stale READY/IN_PROGRESS → atomic checkpoint save.
- `StateStore.load` rejects corrupt checkpoints.
- `EvidenceLog.verified_records` rejects broken chains / duplicates / bad UTF-8.

## 9. Possible crash windows (and outcome)

| Window | Durable result | Recovered classification |
|---|---|---|
| before begin | nothing | READY/BLOCKED (no PASS) |
| after begin, before evidence | nothing durable | READY/BLOCKED (no PASS) |
| during command (SIGKILL) | no evidence | READY/BLOCKED (no PASS); lease released |
| after evidence, before checkpoint | evidence committed | PASS (true positive, evidence-authoritative) |
| during checkpoint save | old-or-new checkpoint (atomic) | consistent with evidence |
| after checkpoint | checkpoint+evidence | PASS |
| during pipeline-status write | partial/missing status | **DERIVED** — ignored; no effect on PASS |

## 10. Authority classification

**AUTHORITATIVE:** implementation manifest · task definition · execution contract
inputs · evidence chain · provenance (repo identity, HEAD, manifest identity,
validator) · repository state.

**DERIVED:** checkpoint · READY queue · pipeline-status.json · traceability
report · contract (report view).

**NEVER AUTHORITATIVE:** exit code alone · cached/checkpoint PASS · stale
checkpoint · stale pipeline-status · user-provided tool-availability claim
(PATH-verified) · in-memory IN_PROGRESS.

**UNKNOWN → fail closed** (no field is guessed; missing authority ⇒ BLOCKED).

## 11. Findings (genuine gaps to validate/fix in later phases)

- The model is already crash-consistent by construction (atomic checkpoint,
  fsync evidence, evidence-authoritative PASS, flock-on-death). The remaining
  work of this phase is to **prove** it with a dedicated crash-consistency +
  recovery-fixpoint suite (TC-01..TC-30) and to formalize the transaction model.
- Honest durability: `fsync` is BEST-EFFORT/ENVIRONMENT-SPECIFIC vs power loss;
  fail-closed semantics (no false PASS on lost evidence) are REQUIRED and hold.
