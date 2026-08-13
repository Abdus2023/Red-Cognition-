# Criterion-Level Validation Attestation Model (Stage-5, Phase 24)

**Date:** 2026-08-12 · **Controller:** 2.0.0

## Central invariant

A criterion is PASS-authorized only by (its declared validator's) evidence
**explicitly bound to that criterion** via the current contract. Command-level
PASS never substitutes for criterion attestation.

## Command evidence vs criterion evidence

- **Command evidence** = proof that a validator *command* executed (exit status,
  stdout, contract_id, command_id, observation, chain).
- **Criterion evidence (attestation)** = proof that the declared criterion
  received a valid attestation from its declared validator under the current
  contract. This is a **derived view** (reuses command evidence + declared
  criterion→validator coverage; no new storage, no inference).

## criterion_attestations(task, contract_id, task_evidence, ctx)

For each strict criterion, derives:
- `criterion_id`, `validator` (declared), `command_id` (command_identity of the
  validator command);
- `attested` = the validator command has chain-verified PASS evidence bound to
  (contract_id, task_id);
- `criterion_evidence_id` = `SHA256(canonical(contract_id, task_id,
  criterion_id, validator, command_id, "PASS"))` — deterministic, per-criterion;
- `gap` = `NO_CRITERION_ATTESTATION` when not attested.

Legacy tasks (no declared validators) return `[]` (Phase-23 grandfathering).

## Closure (per-criterion for strict tasks)

`closure_gaps` uses **per-criterion attestation closure** for strict tasks
(every criterion must terminate in validator evidence) and per-command closure
for legacy tasks. Strict coverage makes these equivalent, but per-criterion
yields explicit criterion→evidence edges + ids.

## PASS predicate (strict)

```
PASS(t) ::= authoritative_task_definition ∧ authoritative_contract
          ∧ provenance_valid ∧ execution_complete
          ∧ criterion_closure_complete (every criterion attested)
          ∧ result_integrity_valid ∧ expected_outputs_valid
          ∧ dependency_valid ∧ repository_state_valid ∧ evidence_chain_valid
```

The system proves *"the declared validator successfully attested this criterion
under this exact contract."* It does **not** prove *"the human criterion is
logically correct"* — that epistemic boundary is not crossed.

## Traceability

```
requirement → specification → task → criterion → validator → command
          → observation → criterion_evidence_id → task status
```

Every criterion carries a deterministic `criterion_evidence_id`; missing edges
are explicit (`closure = OPEN` with `NO_CRITERION_ATTESTATION`).

## Mutation invalidation

Changing a criterion's validator mapping changes `contract_id` (criteria are
identity-bearing) ⇒ prior evidence untrusted ⇒ revalidation required.

## Limitations

- criterion→evidence binding reuses command evidence (derived, not a parallel
  evidence store);
- a validator covering multiple criteria attests all of them by declaration
  (CV-12, permitted);
- legacy tasks (no validators) are grandfathered — PROVEN BY TEST for strict
  tasks; EMPIRICALLY VALIDATED for legacy.
