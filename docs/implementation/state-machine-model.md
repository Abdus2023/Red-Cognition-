# State-Machine Monotonicity Model (Stage-5, Phase 27)

**Date:** 2026-08-12 · **Controller:** 2.0.0

## Central invariant

> OBSOLETE AUTHORITY MUST NEVER BECOME VALID AGAIN WITHOUT A NEW VALID
> AUTHORITATIVE BASIS.

## State-transition model

```
UNKNOWN → BLOCKED → READY → IN_PROGRESS → PASS → INVALIDATED → BLOCKED/READY
```

Every transition is justified by **authoritative** state (evidence chain,
provenance, contract_id, target_hashes, authority docs). No transition is
justified by derived artifacts (checkpoint, pipeline-status, ledger,
traceability).

## Invalidation triggers

| Mutation | Effect | Mechanism |
|---|---|---|
| contract mutation (title, scope, etc.) | contract_id changes | old evidence's contract_id ≠ new |
| manifest mutation | manifest_identity changes | contract_id includes manifest_hash |
| criterion/validator mutation | criteria binding changes | contract_id includes criteria |
| target mutation | target_hashes differ | result-integrity check fails |
| expected-output mutation | contract_id changes | expected_outputs in contract_id |
| command mutation | command_identity changes | contract_id includes commands |
| dependency mutation | dependency_state changes | contract_id includes dep_state |
| HEAD mutation | head in contract_id changes | provenance binding fails |
| evidence deletion | no evidence to verify | _authoritative_pass empty |

## Recovery transitions

`recover() = run(dry_run=False, execute=False)`:
1. Load checkpoint (derived cache; rejected if corrupt).
2. Compute authoritative PASS from evidence + provenance (fixpoint).
3. Demote any checkpoint PASS not backed by authoritative evidence.
4. Reclassify all tasks from authoritative PASS set.
5. Invalidate stale IN_PROGRESS.
6. Save fresh atomic checkpoint.

**Recovery never manufactures authority.** It only demotes, recomputes, and
persists derived state.

## Retry transitions

- Verified PASS + retry → no execution (task not READY; per-command skip).
- Invalidated PASS + retry → re-execute (task READY again; fresh evidence).
- The executor skips commands with existing valid PASS evidence for the current
  contract (per-command idempotency).

## Reconciliation idempotence

`reconcile(reconcile(S)) = reconcile(S)`. Repeated reconciliation produces
identical normalized state. Recovery ×10 converges to the same fixpoint.

## PASS resurrection prohibition

Once PASS is invalidated (contract changed, evidence deleted, target mutated,
HEAD advanced, etc.), the task cannot return to PASS until:
1. The authoritative inputs are consistent (contract restored to a valid state).
2. Fresh valid evidence exists (newly executed under the current contract).

**Restoring the exact manifest** after a mutation does restore the contract_id,
making old evidence valid again — this is **correct behavior** (the evidence was
validly created under that contract; it was never forged). The evidence remains
authoritative; only its binding to the current contract was temporarily broken.

## Fail-closed semantics

Unknown, incomplete, contradictory, or stale authoritative state → BLOCKED /
NOT PASS. Never PASS. No exception.

## State invariants (SM-I1..I10)

| ID | Invariant | Status |
|---|---|---|
| SM-I1 | No PASS resurrection (without fresh authority) | PROVEN BY TEST |
| SM-I2 | Recovery non-authority | PROVEN BY TEST |
| SM-I3 | Derived-state irrelevance | PROVEN BY TEST |
| SM-I4 | Reconciliation idempotence | PROVEN BY TEST |
| SM-I5 | Recovery convergence | PROVEN BY TEST |
| SM-I6 | Mutation invalidation | PROVEN BY TEST |
| SM-I7 | Fresh authority requirement | PROVEN BY TEST |
| SM-I8 | Fail closed | PROVEN BY TEST |
| SM-I9 | Deterministic state | PROVEN BY TEST |
| SM-I10 | Seed preservation | PROVEN BY TEST |
