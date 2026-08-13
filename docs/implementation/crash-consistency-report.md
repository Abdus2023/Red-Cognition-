# Crash-Consistency & Recovery-Fixpoint Report (Stage-5)

**Date:** 2026-08-12 · **Controller:** 2.0.0 · **Phase:** transactional crash-consistency
**Scope:** controller infrastructure only — no Red/Cognition product implementation.

## Final invariant (mechanically enforced)

```
AUTHORITATIVE EXECUTION RECORD: Requirement→Spec→Task→Contract→Execution→
Validation→Evidence→Provenance   ⇒   DERIVED STATE (Checkpoint + Traceability
⇒ Pipeline Status). Derived state can summarize authoritative state; it can
NEVER authorize state.
```

## 1. Audit findings

(`docs/implementation/crash-consistency-audit.md`) Every durable artifact, in-memory
transition, persistence/fsync/atomic-rename boundary, lock, evidence/checkpoint
commit, derived artifact, recovery path, and crash window enumerated and classified
AUTHORITATIVE / DERIVED / NEVER AUTHORITATIVE / UNKNOWN(fail-closed). The pipeline is
crash-consistent by construction: atomic checkpoint, fsync evidence, evidence-
authoritative PASS, flock-on-death.

## 2. Attack matrix (TC-01..TC-30) — all PASS

(`tools/impl_controller/tests/test_crash_consistency.py`, 34 cases incl. fixpoint.)
Each TC specifies setup / injected failure / durable state / expected authority /
recovered state / classification / PASS-permitted. Summary of outcomes:

| Group | Cases | Outcome |
|---|---|---|
| crash before/during/after execution | TC-01..04, TC-28 | no false PASS; recoverable |
| checkpoint/evidence disagreement | TC-05..09 | evidence-authoritative; no false PASS |
| duplicate/corrupt evidence | TC-08, TC-10 | chain breaks; untrusted |
| provenance drift (HEAD/manifest/validator/dep/task/contract) | TC-11..16, TC-23..26 | contract_id mismatch ⇒ not PASS |
| SIGKILL + concurrency | TC-03, TC-17, TC-18 | lease released on death; mutual exclusion |
| derived artifacts never authoritative | TC-20..22, TC-27, TC-29..30 | pipeline-status forged/stale/partial ignored |
| cross-repo/commit/manifest replay | TC-24..26 | not PASS |

## 3–5. Genuine defects / fixes / regressions

**No new controller defects were found in this phase** — the model was already
crash-consistent from prior phases. One **test-harness** flaw was fixed:
`TC-18` raced two processes whose overlap was not guaranteed (both could
legitimately succeed sequentially). Rewritten to deterministically hold the lease
externally and assert the concurrent attempt is denied (exit 1). Suite now stable
across repeated runs (4× full suite, 197/197 each).

## 6. Crash-injection results

Real subprocess SIGKILL during execution (TC-03, TC-17): killed controller left
no evidence and no committed checkpoint; recovery acquired the freed lease and
the task was not PASS. POSIX guarantee: `flock` released on SIGTERM/SIGKILL.
Honest scope: precise mid-rename kills are not deterministic, so durable-state
outcomes are asserted; the execution window is killed for real. **No power-loss
guarantees claimed.**

## 7. Recovery-fixpoint results

`recover()` ×1 / ×3 / ×10 from an identical corrupted-checkpoint state: identical
normalized output, **no duplicate evidence across 10 recoveries**, no resurrected
invalid PASS. `run();recover();run();recover();…` converges with **no oscillation**
(RecoveryFixpoint). ✅

## 8. Evidence/checkpoint reconciliation

evidence PASS + checkpoint absent ⇒ PASS (A); checkpoint PASS + evidence absent/FAIL
⇒ NOT PASS (B,C); evidence PASS + changed dependency/HEAD/manifest/contract/validator
⇒ BLOCKED (D-H); evidence PASS + stale traceability ⇒ regenerated, never trusted (I).

## 9. Provenance results

Recovered PASS retains the full v2.0 provenance chain (requirement, spec, task,
contract_id, manifest, repository, HEAD, validator, evidence, closure). Evidence
is reused after a crash ONLY when its contract/provenance identity still matches.

## 10. Deterministic normalization

Normalization compares `graph`, `classifications`, `provenance_context`,
`frontier`, `traceability` (incl. contract_id, closure). It excludes ONLY
nondeterministic metadata: timestamps (`generated_at`, `timestamp`,
`last_checkpoint`, `updated_at`, `started_at`), evidence `evidence_id` (UUID),
and `repo_head` for non-git working trees. pipeline_run_1 == 2 == 3 and
recovery_run_1 == 2 == 3. ✅

## 11. CI results

CI runs: full self-test (197), recovery/crash-injection (26), crash-consistency
fixpoint (34), real-repo dry-run + frontier assertion, repo-index PASS, RFC-0075
FAIL. SIGKILL REQUIRED on Linux runners; fsync vs power loss BEST-EFFORT/
ENVIRONMENT-SPECIFIC. No Rebol required.

## 12. Real-repository frontier (unchanged)

```
READY=0  BLOCKED=4  PASS=0  FAIL=0  IN_PROGRESS=0  PAUSED=true
RED-LEX-001  [TOOLCHAIN, ARCHITECTURE, PROVISIONING, AUTHORIZATION]
LIBRED-001   [DEPENDENCY, TOOLCHAIN]
HASH-001     [INCOMPLETE_SPECIFICATION, TOOLCHAIN]
RFC0075-001  [SPECIFICATION_CONFLICT, INCOMPLETE_SPECIFICATION]
```

## 13. Scope verification

Only infrastructure files changed (see below). No Red source/tests, runtime,
RFCs, specifications, RFC-0075, or Rebol/toolchain artifacts modified.

## 14. Git commit

This phase committed: audit doc, transaction model, crash-consistency suite,
CI extension, report, regenerated pipeline-status.

## Files changed

```
docs/implementation/crash-consistency-audit.md        (new — Phase 1 audit)
docs/implementation/transaction-recovery-model.md     (new — Phase 2 model)
tools/impl_controller/tests/test_crash_consistency.py (new — 34 cases: TC-01..30 + fixpoint)
.github/workflows/implementation-pipeline.yml         (crash-consistency CI step)
docs/implementation/crash-consistency-report.md       (this report)
docs/implementation/pipeline-status.json              (regenerated)
```

## Product scope

**No product implementation was performed.** Red implementation, Red tests,
runtime, RFC-0075, all RFCs/specifications, and traceability artifacts unchanged.
Rebol/toolchain unchanged (still BLOCKED). RFC-0075 remains independently blocked.
