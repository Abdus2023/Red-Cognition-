# Specification-to-Execution Semantic Completeness Model (Stage-5)

**Date:** 2026-08-12 · **Controller:** 2.0.0

## Central invariant

> A task may become READY only when its executable contract is demonstrably
> sufficient to cover the authoritative acceptance criteria it claims to
> implement. Missing semantics is never inferred; ambiguity is never converted
> into READY.

## Coverage states (not interchangeable)

- **DECLARED** — requirement / specification / criterion / validator / target / expected-output / prohibited-behavior present in the manifest.
- **COVERED** — every acceptance criterion is mapped to a declared validator and every validator maps to ≥1 criterion (explicit criterion↔validator coverage).
- **VALIDATED** — every validator command has chain-verified PASS evidence bound to the current contract.
- **EVIDENCED** — the full chain (requirement→spec→task→criterion→validator→execution→observation→evidence) resolves.

## Opt-in semantic coverage

A task enters **strict coverage** mode when ANY acceptance criterion declares a
`validator` (the id of the validation command that covers it). In strict mode:

- every criterion must name a declared validation command (else
  `INSUFFICIENT_TASK_DEFINITION` — "criterion untested");
- every validation command must be referenced by ≥1 criterion (else
  `INSUFFICIENT_TASK_DEFINITION` — "command has no semantic purpose");
- READY requires this coverage in addition to all existing gates.

Tasks that declare no validators use the **legacy presence-based contract**
(grandfathered): READY requires non-empty criteria + non-empty validators, but no
criterion↔validator mapping is asserted or inferred. This keeps existing
manifests stable; new/strict tasks get full enforcement.

## READY predicate (additions bolded)

```
READY(t) :=
    requirement present ∧ specification present ∧ authority valid
  ∧ acceptance_criteria non-empty ∧ validation_commands non-empty
  ∧ (**semantic coverage complete IF strict mode**)
  ∧ tools available ∧ dependencies satisfied ∧ provenance valid ∧ no spec conflict
```

## PASS predicate (unchained by coverage)

```
PASS(t) ::= ... ∧ per-command closure (every command PASS)
```
In strict mode, because every criterion maps to a command and every command maps
to a criterion, per-command closure ⟹ **every acceptance criterion is
validated**. A criterion whose validator command lacks PASS evidence ⇒ closure
gap ⇒ not PASS (SC-14).

## Semantic contract identity

`contract_id` includes `criteria = sorted((criterion_id, validator_id))`, so any
criterion↔validator remap changes the contract ⇒ prior evidence is untrusted
(revalidation required). List ordering, JSON formatting, documentation, and
timestamps do NOT change identity.

## Mutation invalidation

Removing/remapping a requirement, specification, criterion, validator, target,
expected-output, prohibited-behavior, or dependency output is a semantic change
⇒ new contract_id ⇒ old PASS withdrawn.

## Recovery semantics

`recover()` recomputes PASS from authoritative evidence + current coverage. After
a semantic mutation, PASS ⇒ BLOCKED. After restoring the exact contract, prior
evidence is reusable ONLY if its contract_id matches and all evidence remains
valid. Recovery never manufactures missing coverage.

## Closure predicate

```
Requirement → Specification → Task → Criterion → Validator →
Execution → Observation → Evidence
```
Closure is COMPLETE only when every edge resolves, including (in strict mode)
every criterion terminating in validator evidence. A task with
requirement+spec+evidence but an untested criterion is NOT closed.

## Limitations (honest)

- criterion↔validator coverage is **opt-in** (declared by the planner); the
  controller enforces declared coverage, it does not infer it.
- requirement↔expected-output / requirement↔target semantic mapping is NOT
  modeled (FORMALLY SPECIFIED limitation); the controller verifies declared
  coverage and confinement, not that an output semantically satisfies a
  requirement.
- Coverage enforcement: **PROVEN BY TEST** for opt-in tasks; legacy presence
  contract is **EMPIRICALLY VALIDATED** (grandfathered).
