# Execution Result Integrity Report (Stage-5, Phase 22)

**Date:** 2026-08-12 · **Controller:** 2.0.0 · **Scope:** infrastructure only.

## 1. Audit findings

PASS previously rested on (chain-verified PASS evidence) + closure + provenance
+ authority + deps. It bound the validator's *exit status* and a *negative*
write-scope guard, but did **no positive result verification**: the declared
target state / required outputs were not bound to PASS. So a command that exited
0 without producing/retaining the intended result could PASS (EI-01/03/13/15).

## 2. Confirmed defect (genuine)

**Exit-status-only validation.** A successful command did not require the
implementation result to exist or persist. **Fix:** introduced an observation
model — evidence records `target_hashes` (deterministic target-state map) +
`observed_delta`, both hash-chained; PASS now additionally requires
**result integrity** (current target state == recorded) and **expected_outputs**
(declared required outputs exist with declared hashes). A command exiting 0 with
an absent/wrong/deleted/symlinked target no longer PASSes.

## 3. Rejected hypotheses (not defects — re-proven)

- B/D/E/G/H/I/J/M/P: out-of-scope writes, HEAD/contract/repo/manifest/commit
  replay, validator-command modification, partial multi-command — all already
  handled by scope guard / provenance binding / per-command closure (re-proven
  by EI-04/09/19/17 and the existing suites).
- K: symlink replacement — now additionally caught by `target_hashes` (`link:`
  encoding) — promoted to a covered case.

## 4. Fixes (minimal)
- `safety.target_hashes` (deterministic target-state map incl. symlink encoding).
- `EvidenceRecord.target_hashes` + `observed_delta` (chained).
- `Task.expected_outputs` + `ExpectedOutput` (positive required-output contract).
- Controller: records the observation at execute; PASS requires result integrity
  (target state still holds) + expected_outputs satisfied; execute-time
  `expected_outputs` check before `finish_pass`.
- `contract_id` / `manifest_identity` bind `expected_outputs` (semantic,
  order-independent).

## 5. Attack matrix (EI-01..40)
`tests/test_execution_integrity.py` (21 cases). Outcomes: exit-0-with-absent /
wrong-hash / deleted / symlinked / contradictory-delta target ⇒ not PASS
(EI-01/02/03/05/12/13); expected-output-disappears ⇒ not PASS; undeclared write
⇒ FAIL (EI-04); validator-command/contract change ⇒ invalidate (EI-09/19);
observation tampering ⇒ chain break (EI-31); partial multi-command ⇒ not PASS
(EI-17); stale checkpoint ⇒ demoted (EI-25); incomplete traceability ⇒ OPEN
(EI-34); determinism (EI-35); execute→validate→recover→validate converges
(EI-36); crash boundaries never manufacture PASS (EI-37/38/39); recovery cannot
manufacture observation (EI-40). Cross-repo/manifest/commit replay already
covered by the provenance suite (EI-27/28/29 re-proven there).

## 6. Regression tests
All EI cases are regression tests for the result-integrity model. Two
test-harness bugs fixed (git-init dir; unlink guard) — not controller defects.

## 7. Crash tests
EI-37/38/39 (no-evidence + corrupt-checkpoint recovery ⇒ no PASS); EI-40
(recovery cannot re-establish PASS after the observed result is destroyed).
Real SIGKILL coverage lives in the recovery/crash-consistency suites.

## 8. Determinism
`target_hashes` is a pure function of file content; `observed_delta` is sorted.
EI-35: 3× identical normalized output. Semantic changes (target/output/
validator/command/HEAD/manifest) invalidate.

## 9. CI
Extended with an execution-integrity step (Linux, stdlib, no Rebol).

## 10. Real repository
```
READY=0  BLOCKED=4  PASS=0  FAIL=0  IN_PROGRESS=0  PAUSED=true
blockers byte-for-byte unchanged.
```

## 11. Remaining risks
- `expected_outputs` hashes are planner-declared (the controller verifies them,
  not discovers them). Runtime tool-version probing is still not implemented
  (declared version is bound); documented as a known limitation.
- Filesystem power-loss durability is BEST-EFFORT (fsync); fail-closed
  semantics are REQUIRED.

## Files changed
```
tools/impl_controller/safety.py     (target_hashes)
tools/impl_controller/evidence.py   (target_hashes, observed_delta fields)
tools/impl_controller/model.py      (expected_outputs, ExpectedOutput)
tools/impl_controller/manifest.py   (parse expected_outputs)
tools/impl_controller/provenance.py (expected_outputs in contract/manifest identity)
tools/impl_controller/controller.py (observation recording, result-integrity PASS gate)
tools/impl_controller/tests/test_execution_integrity.py (new, 21 cases)
docs/implementation/execution-integrity-model.md / -report.md
docs/implementation/evidence-contract.md (handoff update)
docs/implementation/pipeline-status.json (regenerated)
.github/workflows/implementation-pipeline.yml (EI CI step)
```

## Product scope
No product implementation performed. Red/RFC-0075/specifications/Rebol unchanged.
RFC-0075 remains independently blocked.
