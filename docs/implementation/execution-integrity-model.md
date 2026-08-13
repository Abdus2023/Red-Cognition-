# Execution Result Integrity & Validator Trust Model (Stage-5)

**Date:** 2026-08-12 · **Controller:** 2.0.0

## Central invariant

> A successful exit status is never, by itself, sufficient evidence that the
> declared implementation result actually occurred. PASS is bound to the
> validator's **observed state transition** and any declared required outputs.

## Boundary

```
Contract → Executor → Observation → Validator → Evidence → PASS
```

## 1. Execution
The executor runs each declared validation command (`shell=False`, allowlisted,
scope-guarded). A command "succeeds" iff `exit_status == expected_exit`.

## 2. Observation
For each command the controller records an **observation** bound into the
evidence hash chain:
- `target_hashes` — deterministic state map of declared `implementation_targets`
  (`None` if absent; `<sha256>` for a regular file; `link:<sha256>` for a symlink
  so a regular→symlink swap is detected);
- `observed_delta` — sorted repo-relative paths changed by the command
  (excluding controller artifacts).

## 3. Validation
The validator is the declared command; its result is `exit_status ==
expected_exit`. The observation is the independent witness that the intended
state now exists.

## 4. Evidence
`EvidenceRecord` carries: command result + `target_hashes` + `observed_delta` +
provenance (contract_id, command_id, repo_identity, HEAD, manifest_hash,
validator) — all hash-chained. Tampering any field breaks the chain.

## 5. PASS predicate

```
PASS(t) :=
      command_pass(every command)         # exit_status == expected_exit
    ∧ validator_bound(contract_id/cmd)    # per-command closure
    ∧ result_integrity                    # current target_hashes == recorded
    ∧ expected_outputs_present            # declared outputs exist w/ declared hash
    ∧ target_scope_valid                  # no out-of-scope writes
    ∧ provenance_valid                    # repo/HEAD/manifest/validator agree
    ∧ traceability_closed                 # full chain resolves
```

No single component independently authorizes PASS. Exit status alone is
insufficient.

## 6. Repository delta semantics
ALLOWED: changes within `implementation_targets`. FORBIDDEN: undeclared paths,
protected paths (`.git`, `~`, absolute, escapes) — rejected by `validate_targets`
at load and by the write-scope guard at execution. Insufficient scope ⇒
`BLOCKED — INSUFFICIENT_TASK_DEFINITION` (scope is never silently broadened).

## 7. Validator trust
EXECUTOR = "the command exited successfully"; VALIDATOR = "the intended state
now exists" (observed via `target_hashes`/`expected_outputs`); CONTROLLER = "the
complete evidence chain proves the task's intended state." A validator PASS from
another contract/repo/HEAD/manifest/commit is rejected (provenance binding).

## 8. Crash boundaries
A crash before observation / before validation / before checkpoint never
manufactures PASS. A crash after validation establishes PASS only if the durable
observation + validator evidence are independently sufficient and
provenance-valid (reconstructed from authoritative evidence, never forged
derived state).

## 9. Recovery semantics
`recover()` recomputes PASS from the verified evidence chain + current
`target_hashes`/`expected_outputs`. If the observed target state no longer
matches (target deleted/modified/symlinked) or a required output is absent,
PASS is withdrawn. Recovery never manufactures observations.

## 10. Determinism
Identical repo state + contract + validator + expected outputs ⇒ identical
normalized observation (`target_hashes` are a pure function of file content;
`observed_delta` is sorted). Reordering non-semantic data does not alter
identity; changing target/expected-output/validator/command/tool-version/HEAD/
manifest semantics invalidates the prior result.

## 11. Fail-closed rules
Missing authority ⇒ BLOCKED. Missing required output ⇒ not PASS. Out-of-scope
write ⇒ evidence FAIL. Tampered observation ⇒ chain break ⇒ untrusted.
Forged/stale derived status ⇒ ignored (controller never reads pipeline-status).
UNKNOWN ⇒ fail closed.

## Terminology (honest)
- **PROVEN BY TEST**: the EI/determinism/crash suites establish each property above.
- **FORMALLY SPECIFIED**: the PASS predicate and delta semantics are specified here.
- **EMPIRICALLY VALIDATED**: 5× stability runs.
- **BEST-EFFORT**: fsync durability vs power loss (not claimed stronger).
