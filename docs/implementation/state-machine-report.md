# State-Machine Report (Stage-5, Phase 27)

**Date:** 2026-08-12 · **Controller:** 2.0.0 · **Scope:** infrastructure only.

## 1. Audit
The state machine is monotonic: every transition is justified by authoritative state. PASS is derived from evidence+provenance+closure+result-integrity via a fixpoint (_authoritative_pass). No derived artifact feeds back. Recovery demotes stale PASS. Retry skips verified commands.

## 2. Genuine defects
**None found.** All 24 state-machine attacks pass against the current implementation.

## 3. Test-specification errors (fixed)
- Authority-flip test assumed "restore exact manifest → still NOT PASS" — but contract_id is deterministic: restoring the exact manifest restores the contract_id, making old evidence valid again (correct behavior). Rewritten to delete evidence (not just mutate manifest), so restore doesn't resurrect.
- SM-30 expected `python3 -V` to restore a mutated target — the command doesn't modify the target. Fixed to restore the target manually before retry.

## 4. Authority boundary
`_authoritative_pass` reads only: evidence chain + provenance + target_hashes + authority docs. Report derived fields (requirement_ledger, criterion_attestations, coverage_identity, traceability, pipeline-status) never feed into PASS determination.

## 5. Invalidation matrix (SM-01..10)
All PASS → mutation → NOT PASS: contract/manifest/criterion/validator/target/command/HEAD/dependency. PROVEN BY TEST.

## 6. Evidence resurrection (SM-11..20)
Delete/replay/forge evidence or derived artifacts → fail closed. PROVEN BY TEST.

## 7. Recovery (SM-21..28)
Crash before/during/after execution → recover → no manufactured PASS; ×10 fixpoint. PROVEN BY TEST.

## 8. Authority-flip proof (SM-J1)
VALID PASS → delete evidence → corrupt derived → recover → NOT PASS → restore manifest → NOT PASS → fresh execute → PASS. PROVEN BY TEST.

## 9. Full regression: **344/344 PASS** (320 prior + 24 state-machine)
## 10. Five-run stability: **5/5 × 344/344 PASS**
## 11. Recovery fixpoint: ×10 fixpoint PROVEN BY TEST
## 12. Real repository: `READY=0 / BLOCKED=4 / PAUSED=true`
## 13. Seed: byte-for-byte unchanged
## 14. Validators: repo-index PASS; RFC-0075 FAIL (blocked)
## 15. Scope: clean
## 16. Commit: (below)

## Files changed
```
tools/impl_controller/tests/test_state_machine.py (new, 24 cases)
docs/implementation/state-machine-model.md / -report.md
docs/implementation/pipeline-status.json (regenerated)
.github/workflows/implementation-pipeline.yml (state-machine CI)
```

## Product scope
No product implementation performed. Red/RFC-0075/specifications/Rebol unchanged.
