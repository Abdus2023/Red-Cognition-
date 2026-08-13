# Criterion-Level Validation Report (Stage-5, Phase 24)

**Date:** 2026-08-12 · **Controller:** 2.0.0 · **Scope:** infrastructure only.

## 1. Audit findings

The PASS path used per-COMMAND closure (every command has PASS evidence) plus
declared criterion→validator coverage. Together these *implied* every criterion
was attested, but the criterion→evidence edge was **implicit** (not per-criterion)
and there was no deterministic `criterion_evidence_id`. Traceability could not
point to a specific criterion's attestation.

## 2. Confirmed defect (traceability/attestation explicitness)

Closure reported command-level gaps even for strict tasks; it did not explicitly
prove per-criterion attestation. **Fix (backward-compatible):** added
`criterion_attestations` — a derived per-criterion view that reuses command
evidence + declared coverage (no new storage, no inference). Strict tasks now use
**per-criterion closure**; each attested criterion carries a deterministic
`criterion_evidence_id`. Legacy tasks unaffected.

## 3. Rejected hypotheses

- CV-05/06/07 (criterion evidence references wrong validator/contract/task):
  these reduce to command-evidence provenance binding (already handled); with
  per-criterion closure, a criterion whose validator's evidence has the wrong
  binding is simply `NO_CRITERION_ATTESTATION`. Not a separate defect.
- Adding `criterion_id` as a stored field on EvidenceRecord: rejected — a command
  covering multiple criteria would make it ambiguous. Criterion attestation is a
  derived view (correct, non-redundant).

## 4. Fixes
- `provenance.criterion_attestations(task, contract_id, task_evidence, ctx)`.
- `closure_gaps`: strict tasks → per-criterion attestation closure; legacy →
  per-command (unchanged).
- `controller._traceability`: includes `criterion_attestations` per task.

## 5. Attack matrix (CV-01..28)
`tests/test_criterion_validation.py` (23 cases): validator-must-execute; exit-0-
insufficient-alone; strict-no-validator BLOCKED; criterion-evidence-absent not
PASS; wrong-validator/contract/task not attested; per-criterion evidence id;
forged-PASS chain break; one-PASS-one-absent not PASS; one-FAIL not PASS;
validator-reuse permitted; criterion-reorder same contract; mapping-changed
different contract; criterion-deleted/validator-changed invalidate; stale-
checkpoint demoted; crash-no-invented-PASS; recovery ×10 fixpoint; complete
synthetic READY→PASS; missing-evidence READY-not-PASS; real-repo + seed
unchanged.

## 6–9. Mutation / recovery / determinism / stability
Criterion validator remap → contract_id change → old PASS withdrawn (PROVEN BY
TEST). Recovery ×10 fixpoint. Criterion-reorder → same contract_id. 5× stability
(see below).

## 10. Real repository
```
READY=0  BLOCKED=4  PASS=0  FAIL=0  IN_PROGRESS=0  PAUSED=true
Seed classifications byte-for-byte unchanged (legacy mode, no validators).
```

## Terminology
- **PROVEN BY TEST:** per-criterion closure, criterion_evidence_id, mutation
  invalidation, recovery fixpoint, seed unchanged.
- **FORMALLY SPECIFIED:** criterion-attestation model (this doc).
- **DOCUMENTED LIMITATION:** criterion evidence is derived (reuses command
  evidence); legacy tasks grandfathered.

## Files changed
```
tools/impl_controller/provenance.py  (criterion_attestations; per-criterion closure)
tools/impl_controller/controller.py  (criterion_attestations in traceability + import)
tools/impl_controller/tests/test_criterion_validation.py (new, 23 cases)
docs/implementation/criterion-validation-model.md / -report.md
docs/implementation/evidence-contract.md (criterion attestation handoff)
docs/implementation/pipeline-status.json (regenerated)
.github/workflows/implementation-pipeline.yml (criterion-validation CI)
```

## Product scope
No product implementation performed. Red/RFC-0075/specifications/Rebol unchanged.
RFC-0075 remains independently blocked.
