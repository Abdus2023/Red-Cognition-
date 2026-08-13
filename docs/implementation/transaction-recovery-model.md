# Transaction & Recovery Model (Stage-5)

**Date:** 2026-08-12 · **Controller:** 2.0.0

## Authoritative transaction

```
Task Definition  (AUTHORITATIVE — implementation plan)
       ↓
Contract         (deterministic contract_id over immutable inputs)
       ↓
Execution        (executor runs declared validation within the contract)
       ↓
Validation       (command captured: stdout/stderr/exit vs expected_exit)
       ↓
Evidence Commit  (append + flush + fsync + hash chain)   ← durability point
       ↓
Checkpoint Commit (atomic temp→fsync→rename)             ← durability point
       ↓
Derived Status   (PASS/READY/BLOCKED/… — recomputed from evidence)
       ↓
Traceability     (derived report — regenerated each run)
```

## Governing rule

**A derived artifact MUST NEVER promote an execution to PASS.**

Checkpoints, READY queues, pipeline-status, and traceability reports are derived.
They summarize authoritative state; they never authorize it. PASS is computed
exclusively from the authoritative execution record (evidence chain) bound to
the task's current contract via provenance.

## Formal PASS predicate

```
PASS(t) :=
      valid_task(t)              ∧   # defined: authority, requirement, spec,
                                    # validation commands, acceptance criteria
      valid_contract(t)          ∧   # contract_id recomputed == evidence contract_id
      valid_provenance(t)        ∧   # repo identity + HEAD + manifest identity
                                    # + validator identity all match evidence
      valid_dependencies(t)      ∧   # every PASS dependency is authoritatively PASS
      valid_execution(t)         ∧   # execution occurred within the contract scope
                                    # (no out-of-scope writes)
      valid_validation(t)        ∧   # exit_status == expected_exit; command non-empty
      valid_evidence_chain(t)    ∧   # hash chain intact to the record; no duplicate id
      valid_repository_state(t)  ∧   # authority docs present/readable/in-repo
      valid_manifest_identity(t) ∧   # manifest_hash matches the evidence's manifest
      traceability_closure(t)        # requirement→spec→task→contract→evidence closed
```

If any clause is false ⇒ the task is **not PASS** (BLOCKED / FAIL / READY per the
classifier). No single clause is sufficient on its own — in particular,
`valid_validation` (a successful command) alone is never sufficient.

## Recovery fixpoint

`recover(S) = S'` where `S'` is the state recomputed purely from authoritative
inputs. Convergence:

```
normalize(recover(S)) == normalize(recover(recover(S))) == normalize(recover³(S)) == …
```

Recovery NEVER: manufactures PASS · resurrects invalidated PASS · duplicates
evidence · consumes evidence twice · bypasses provenance/dependencies/
authorization · modifies task definitions · promotes derived state to authority.

Normalization (for determinism checks) excludes only explicitly nondeterministic
fields: `generated_at`, `timestamp`, `last_checkpoint`, `updated_at`,
`started_at`, evidence `evidence_id` (UUID), `repo_head` only when the working
tree is non-git, and per-record timestamps. All security-relevant fields
(classification, reasons, contract_id, manifest_hash, graph, frontier,
traceability closure) are deterministic and compared.

## Pipeline fixpoint (no oscillation)

`run(); recover(); run(); recover(); …` converges to identical normalized
output. The pipeline cannot oscillate `READY→PASS→READY→PASS` or
`PASS→READY→PASS` unless an authoritative prerequisite (tool availability, spec
reconciliation, dependency PASS, manifest, HEAD, authority) actually changes.

## Authority vs derived (summary)

| AUTHORITATIVE | DERIVED | NEVER AUTHORITATIVE |
|---|---|---|
| manifest, task def, contract inputs, evidence chain, provenance, repo state | checkpoint, READY queue, pipeline-status, traceability | exit code, cached PASS, stale checkpoint/report, availability claim, in-memory IN_PROGRESS |
