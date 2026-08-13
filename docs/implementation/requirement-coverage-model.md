# Requirement Coverage Model (Stage-5, Phase 25)

**Date:** 2026-08-12 · **Controller:** 2.0.0

## Central invariant

> TASK PASS does NOT imply REQUIREMENT SATISFIED. The requirement ledger is
> DERIVED from authoritative task PASS state — it can never authorize PASS.

## Graph

```
REQUIREMENT → SPECIFICATION → OBLIGATION → TASK → CRITERION → VALIDATOR
           → COMMAND → OBSERVATION → EVIDENCE → TASK PASS
           → REQUIREMENT COVERAGE → REQUIREMENT STATUS (DERIVED)
```

## DECLARED vs DERIVED

- **DECLARED** (authoritative): requirement id, specification_refs, coverage
  (obligation→task bindings) in the manifest. Deterministic `coverage_identity`
  = `SHA256(canonical(requirement graph))`.
- **DERIVED** (never authoritative): requirement status
  (SATISFIED / PARTIAL / BLOCKED / NO_COVERAGE) computed each run from the
  authoritative task PASS set.

## Requirement statuses

```
SATISFIED   = ALL coverage tasks PASS
PARTIAL     = SOME coverage tasks PASS (but not all)
BLOCKED     = NO coverage tasks PASS
NO_COVERAGE = requirement declares no coverage tasks
```

## READY gate (tasks)

Unchanged — a task's READY/PASS is independent of requirement status. The
requirement ledger observes task state; it never influences it.

## Mutation invalidation

Changing the coverage graph (adding/removing obligations, reassigning tasks)
changes `coverage_identity`. A task's `contract_id` remains the execution-
contract identity (distinct from `coverage_identity`). An invalidated task
PASS → requirement status recomputed (SATISFIED → PARTIAL or BLOCKED).

## Recovery

The ledger is recomputed each run from authoritative task state. A forged/stale/
deleted ledger is harmless (never trusted as authority). Recovery ×N converges.

## Limitations

- Requirement coverage is **opt-in** (declared in the manifest). The controller
  verifies declared coverage, never infers partitioning.
- The controller does NOT prove a requirement is conceptually correct or that a
  task semantically satisfies a requirement — that is a planner/review
  responsibility (epistemic boundary).
