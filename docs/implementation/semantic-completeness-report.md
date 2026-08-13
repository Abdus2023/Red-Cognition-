# Semantic Completeness Report (Stage-5, Phase 23)

**Date:** 2026-08-12 · **Controller:** 2.0.0 · **Scope:** infrastructure only.

## 1. Audit

The READY gate and closure checked **presence** of requirement_refs,
specification_refs, acceptance_criteria, and validation_commands, but did NOT
verify **semantic coverage** — that each acceptance criterion is validated by a
declared validator, nor that validators map to criteria. SC-02/03/07/14/19 could
occur for tasks that did not declare a criterion↔validator mapping.

## 2. Confirmed defect (genuine, backward-compatible fix)

A task could become READY/PASS with acceptance criteria not covered by any
validator (a contract semantically weaker than its requirements). **Fix
(opt-in):** `AcceptanceCriterion.validator` declares the covering command; when
any criterion declares a validator the task is in **strict coverage** mode and
the controller enforces full criterion↔validator coverage (every criterion→valid
command; every command→≥1 criterion) at READY, and per-command closure at PASS
⟹ every criterion validated. The mapping is bound into `contract_id` so remapping
invalidates prior evidence.

This is **opt-in** so the four seed tasks (no declared validators) retain their
classifications byte-for-byte; legacy presence-based contract is grandfathered.

## 3. Rejected hypotheses (not defects — documented limitations)

- requirement↔expected-output / requirement↔target semantic mapping (SC-05/06/13)
  is NOT modeled — the controller verifies declared coverage and path
  confinement, not that an output semantically satisfies a requirement. Inferring
  such mapping is forbidden ("do not infer missing semantics").
- SC-08/09 (multi-requirement collapse / silent cross-task coverage) require a
  global requirement-coverage ledger across tasks — out of scope; documented.

## 4. Fixes
- `model.AcceptanceCriterion.validator`.
- `manifest` parses `validator`.
- `engine._coverage_gaps` (strict-mode coverage) wired into `self_blockers`
  (READY gate → INSUFFICIENT).
- `contract_id` criteria = `sorted((id, validator))` (semantic).

## 5. Attack matrix (SC subset)
`tests/test_semantic_completeness.py` (13 cases): missing requirement (SC-01);
strict-covered READY; criterion-without-validator BLOCKED (SC-03); orphan
validator BLOCKED (SC-07); validator-not-a-command BLOCKED; legacy non-strict
READY (grandfathered); partial validator FAIL (SC-14); validator-remap mutation
invalidates; recovery after mutation then restore; semantic-equivalent ⇒ same
contract_id; semantic-different validator ⇒ different contract_id; real-repo
frontier unchanged.

## 6. Mutation / recovery
SC mutation: criterion↔validator remap ⇒ contract_id change ⇒ old PASS withdrawn
(PROVEN BY TEST). Recovery after mutation ⇒ BLOCKED; restore exact contract ⇒
prior evidence reusable iff contract_id matches.

## 7. Determinism
Semantic-equivalent manifests ⇒ identical contract_id; semantic-different
(validator remap) ⇒ different (PROVEN BY TEST).

## 8. Limitations
Opt-in coverage (not inferred); requirement↔output mapping not modeled
(FORMALLY SPECIFIED limitation); multi-requirement cross-task ledger out of scope.

## 9. Real repository
```
READY=0  BLOCKED=4  PASS=0  FAIL=0  IN_PROGRESS=0  PAUSED=true
RED-LEX-001 [TOOLCHAIN, ARCHITECTURE, PROVISIONING, AUTHORIZATION]
LIBRED-001  [DEPENDENCY, TOOLCHAIN]
HASH-001    [INCOMPLETE_SPECIFICATION, TOOLCHAIN]
RFC0075-001 [SPECIFICATION_CONFLICT, INCOMPLETE_SPECIFICATION]
```
Classifications byte-for-byte unchanged (seed tasks have no declared validators
⇒ legacy mode ⇒ unaffected).

## 10. CI
Extended with a semantic-completeness step (Linux, stdlib, no Rebol).

## Terminology
- **PROVEN BY TEST:** opt-in coverage enforcement, mutation invalidation,
  determinism, recovery.
- **FORMALLY SPECIFIED:** coverage/closure/identity predicates (this model).
- **EMPIRICALLY VALIDATED:** 5× stability.
- **UNVERIFIED:** requirement↔output semantic mapping (out of scope).

## Files changed
```
tools/impl_controller/model.py     (AcceptanceCriterion.validator)
tools/impl_controller/manifest.py  (parse validator)
tools/impl_controller/engine.py    (_coverage_gaps in self_blockers)
tools/impl_controller/provenance.py (criteria include validator in contract_id)
tools/impl_controller/tests/test_semantic_completeness.py (new, 13 cases)
docs/implementation/semantic-completeness-model.md / -report.md
docs/implementation/evidence-contract.md (closure handoff update)
docs/implementation/pipeline-status.json (regenerated)
.github/workflows/implementation-pipeline.yml (SC CI step)
```

## Product scope
No product implementation performed. Red/RFC-0075/specifications/Rebol unchanged.
RFC-0075 remains independently blocked.
