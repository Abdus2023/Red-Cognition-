# Global Invariants Report (Stage-5, Phase 26)

**Date:** 2026-08-12 · **Controller:** 2.0.0 · **Scope:** infrastructure only.

## 1. Audit result

Phases 17–25 compose into one coherent authority-preserving state machine. Data
flow is strictly unidirectional: authoritative → derived. No derived artifact
feeds back into the PASS gate. All 30 global invariants hold.

## 2. Authority model

See `global-invariants-model.md`. Key boundary: `_authoritative_pass()` (the PASS
gate) reads only authoritative sources (evidence chain, provenance, target_hashes,
authority docs). The report's derived fields (requirement_ledger,
criterion_attestations, coverage_identity, traceability, pipeline-status) are
computed AFTER classification and never influence it.

## 3. Genuine defects discovered

**1 genuine controller defect:** `coverage_identity` did not sort the requirements
list → reordering requirements changed the identity (GI-T27). Fixed: sort by
requirement id.

## 4. Rejected hypotheses

- Criterion TEXT is documentation, not identity-bearing (GI-T31): the contract_id
  binds criterion ID + validator binding, not the text. Changing text alone is
  non-semantic. TEST SPECIFICATION ERROR — fixed the test to mutate the ID.
- Pipeline-status forgery (GI-T01/20): the controller never reads pipeline-status;
  forging it has no effect. EXPECTED BEHAVIOR.

## 5. Test-harness defects

- GI-T38: `_synth(d+"_2")` created a non-existent parent dir. TEST-HARNESS DEFECT.
  Rewritten with proper subdirectory.

## 6. Minimal fixes

`provenance.coverage_identity`: added `payload = sorted(payload, key=lambda r: r["id"])`.

## 7. New tests

`tests/test_global_invariants.py` — 22 cases (GI-T01..44): authority attacks,
provenance replay, semantic mutation, derived-state attacks, recovery, determinism,
semantic distinction, closure, idempotency, seed regression, task-PASS≠requirement.

## 8. Full regression: **320/320 PASS** (298 prior + 22 global-invariants)
## 9. Five-run stability: **5/5 × 320/320 PASS**
## 10. Recovery/fixpoint: recover×10 fixpoint PROVEN BY TEST
## 11. Mutation matrix: GI-T11..16 PASS
## 12. Evidence replay: GI-T06..10 PASS
## 13. Real frontier: `READY=0 / BLOCKED=4 / PAUSED=true`
## 14. Seed: byte-for-byte unchanged
## 15. Validators: repo-index PASS; RFC-0075 FAIL (blocked)
## 16. Docs: `global-invariants-model.md`, this report
## 17. CI: step 2i added
## 18. Scope: clean — no product files
## 19. Commit: (below)
## 20. Limitations: criterion text is documentation; legacy grandfathered; epistemic boundary maintained

## Files changed

```
tools/impl_controller/provenance.py     (coverage_identity sort fix)
tools/impl_controller/tests/test_global_invariants.py (new, 22 cases)
docs/implementation/global-invariants-model.md / -report.md
docs/implementation/pipeline-status.json (regenerated)
.github/workflows/implementation-pipeline.yml (global-invariants CI)
```

## Product scope
No product implementation performed. Red/RFC-0075/specifications/Rebol unchanged.
