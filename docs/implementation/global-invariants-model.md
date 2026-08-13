# Global Invariants Model (Stage-5, Phase 26)

**Date:** 2026-08-12 · **Controller:** 2.0.0

## Central principle

> AUTHORITATIVE INPUT → IMMUTABLE CONTRACT → CONTROLLED EXECUTION → OBSERVED
> RESULT → INTEGRITY-VERIFIED EVIDENCE → TASK CLOSURE → REQUIREMENT COVERAGE →
> DERIVED STATUS. Never reverse this direction.

## Authority model

| Artifact | Type | Authoritative? | Can authorize PASS? | Revalidated? |
|---|---|---|---|---|
| Evidence log (hash-chained, fsynced) | AUTHORITATIVE | YES | YES (via _authoritative_pass) | chain-verified |
| contract_id | IDENTITY | YES | (binds) | recomputed |
| manifest_identity | IDENTITY | YES | (binds) | recomputed |
| repository_identity + HEAD | IDENTITY | YES | (binds) | recomputed |
| target_hashes | OBSERVATION | YES | (result integrity) | recomputed |
| Task definition (manifest) | INPUT | YES | (defines contract) | loaded |
| Checkpoint | DERIVED (cache) | NO | NO | cross-checked, demoted |
| pipeline-status.json | DERIVED | NO | NO | never read by controller |
| Classifications | DERIVED | NO | NO | recomputed |
| criterion_attestations | DERIVED | NO | NO | recomputed |
| requirement_ledger | DERIVED | NO | NO | recomputed |
| coverage_identity | DERIVED | NO | NO | recomputed |
| Traceability report | DERIVED | NO | NO | recomputed |

## Data flow (unidirectional)

```
evidence → _authoritative_pass → auth_pass → classify_all → classifications
                                                              ↓
                                                    _build_report (derived fields)
                                                    (requirement_ledger, traceability,
                                                     criterion_attestations, coverage_id)
```

No derived field feeds back into `_authoritative_pass`. The PASS gate reads
ONLY authoritative sources.

## Global invariant matrix (GI-01..30)

| ID | Invariant | Status |
|---|---|---|
| GI-01 | Derived state cannot authorize PASS | PROVEN BY TEST |
| GI-02 | Derived state cannot authorize execution | PROVEN BY TEST |
| GI-03..07 | Evidence cannot cross contracts/tasks/requirements/criteria/graphs | PROVEN BY TEST |
| GI-08..16 | Semantic mutation invalidates identity | PROVEN BY TEST |
| GI-17..19 | Recovery cannot manufacture authority | PROVEN BY TEST |
| GI-20 | Reordering non-semantic declarations is identity-neutral | PROVEN BY TEST |
| GI-21 | Semantic changes are identity-sensitive | PROVEN BY TEST |
| GI-22 | Verified PASS retry is idempotent | PROVEN BY TEST |
| GI-23 | Criterion closure requires criterion-specific attestation | PROVEN BY TEST |
| GI-24..26 | Requirement satisfaction is derived, never authority | PROVEN BY TEST |
| GI-27 | Unknown semantic edges never become PASS | PROVEN BY TEST |
| GI-28 | Legacy tasks remain governed by grandfathered semantics | PROVEN BY TEST |
| GI-29 | Strict tasks cannot bypass semantic closure | PROVEN BY TEST |
| GI-30 | Cross-task evidence replay fails closed | PROVEN BY TEST |

## Honest terminology

- **PROVEN BY TEST:** all 30 invariants (22 GI cases + existing 298 cases).
- **FORMALLY SPECIFIED:** the authority/derived model and data-flow graph (this doc).
- **EMPIRICALLY VALIDATED:** 5× stability.
- **DOCUMENTED LIMITATION:** criterion text is documentation (not identity-bearing); legacy tasks grandfathered; requirement↔output semantic mapping not inferred.
