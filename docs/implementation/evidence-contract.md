# Implementation Pipeline — Evidence Contract

**Contract version:** 1.0  
**Controller version:** 1.1.0  
**Applies to:** the Red/Cognition implementation pipeline (Stage 5 of the five-stage
process: Extraction → Knowledge Base → Repository Organization → Planning →
Execution).

This document is the authoritative contract between the pipeline stages. It
binds the planner, controller, executor, and validator to a single tamper-evident
evidence chain. The controller implements **no** Red/Cognition product features;
it only schedules, contracts, executes-within-scope, validates, and records.

## 1. Stage contract

```
Planner ──implementation-plan.json──▶ Controller
   (Stage 4)        strict schema           (Stage 5 orchestrator)
                     fail-closed                  │
                                                  ├── classifications
                                                  ├── READY queue
                                                  └── execution contracts
                                                          │
                          contract ──────────────────────▶ Executor
                                                          │  (works ONLY inside
                                                          │   the contract scope)
                                                          │
                          declared validation ───────────▶ Validator
                                                          │  runs validation_commands
                                                          │  (shell=False, allowlisted)
                                                          │
                          EvidenceRecord (hash-chained) ─▶ Evidence log (JSONL)
                                                          │
                          PASS ──▶ Checkpoint + pipeline-status.json ──▶ Status
```

| Stage | Produced artifact | Consumed by | Fail-closed rule |
|---|---|---|---|
| Planner | `implementation-plan.json` (task defs) | Controller | unknown fields / malformed sub-objects / cycles / empty list → **REJECTED** |
| Controller | classifications + READY queue + execution contracts | Executor | non-READY task never receives a contract |
| Executor | work within `implementation_targets` | Validator | prohibited_scope / `.git` / escapes never written |
| Validator | `EvidenceRecord` (stdout/stderr/exit/result) | Evidence log | unsafe command → **BLOCKED**; PASS only if `exit==expected` |
| Evidence log | tamper-evident JSONL (hash chain) | Status | tamper/break → record and all later become **untrusted** |
| Status | checkpoint + `pipeline-status.json` | traceability | PASS without verified evidence → **demoted** |

## 2. Evidence record & integrity

Every validation produces one `EvidenceRecord` appended to `.impl_controller/evidence.jsonl`:

```
evidence_id, task_id, command, stdout, stderr, exit_status,
result{PASS|FAIL|BLOCKED|NOT_APPLICABLE}, failure_class, timestamp,
artifacts[], notes, expected_exit, prev_hash, record_hash
```

- `record_hash = sha256(canonical(record minus record_hash))`, chained via `prev_hash`.
- A PASS is trusted **only if**: the chain is intact from the genesis record to it,
  `result == PASS`, `exit_status == expected_exit` (integer), and `command` is non-empty.
- Tampering, removing, or malforming any line breaks the chain; that record and every
  later one become untrusted (fail closed). `verify_integrity()` reports
  `{total_records, trusted_records, intact, broken_at}`.

## 3. Manifest lifecycle

Task state machine (controller-computed each run unless terminal):

```
DISCOVERED → PLANNED → READY → IN_PROGRESS → PASS   (terminal success)
                            │            │
                            ↓            └──→ FAIL (reclassified next run)
                          BLOCKED
                            │
                (prerequisite change) ──▶ recompute → READY | BLOCKED
```

- **PASS / REJECTED / DEFERRED** are terminal (sticky).
- **BLOCKED** and **READY** are recomputed from data every run (never cached as truth).
- **PASS** is re-validated each run against authority + dependency state; drift demotes it.
- The only way a task reaches **PASS** is chain-verified PASS evidence with
  `exit_status == expected_exit`.

## 4. Blocker immutability policy

The four current blockers are **immutable** unless an *authoritative prerequisite*
changes. The controller enforces this by recomputing from data — it never lifts a
blocker on its own:

| Blocker | Lifts only when |
|---|---|
| RED-LEX-001 (TOOLCHAIN/ARCHITECTURE/PROVISIONING/AUTHORIZATION) | an approved Rebol 2.7.8-compatible executable is materialized and host-executable, or an authorized compatible environment is provided |
| LIBRED-001 (DEPENDENCY/TOOLCHAIN) | RED-LEX-001 reaches PASS (Red build available) |
| HASH-001 (INCOMPLETE_SPECIFICATION/TOOLCHAIN) | the `/hash` behavior is normatively specified **and** the toolchain is available |
| RFC0075-001 (SPECIFICATION_CONFLICT/INCOMPLETE_SPECIFICATION) | RFC-0075 receives authoritative reconciliation (schema, lifecycle, crypto, replay, source-authority) and the traceability validator passes |

No agent may edit these classifications directly; they are derived from manifest
data + evidence + environment on every run.

### 4.1 Pipeline-boundary invariants (adversarially validated)

The planner→controller→executor→validator→evidence→traceability boundary is
hardened against 20 pipeline attacks (`tests/test_pipeline_attacks.py`):

- **Tool availability = ground truth, not planner claim.** A required tool blocks
  unless it is *claimed* available **and** its executable is found on `PATH`
  (via a known id→binary map or the tool's `binary` field). Falsifying
  `available: true` cannot unblock a task.
- **Write-scope guard.** A validation command that modifies anything outside the
  declared `implementation_targets` invalidates the run (evidence → FAIL,
  INTEGRATION); the controller's own state/evidence/lock artifacts are excluded.
- **Requirement ↔ specification traceability.** A task whose `requirement_refs`
  lack any `specification_refs` is `BLOCKED — INSUFFICIENT_TASK_DEFINITION`.
- **Cwd-independence.** Runner default paths resolve against `--repo-root`, so
  the pipeline is invariant to the invoking working directory.

## 5. CI invocation

`.github/workflows/implementation-pipeline.yml` runs the pipeline on Linux/Python
**without** Rebol (the controller is stdlib-Python only):

```
python3 -m py_compile tools/impl_controller/*.py
python3 tools/impl-controller.py --self-test                       # 85 cases
python3 tools/run-implementation-pipeline.py --dry-run             # real frontier
python3 tools/validate_repository_index.py                         # integrity
python3 tools/validate_rfc_0075_traceability.py                    # expect FAIL=blocked
```

CI asserts: self-test 85/85 PASS, real frontier `READY=0 / PAUSED`, repository
index PASS, RFC-0075 FAIL (blocked). It does **not** attempt Rebol or product builds.

## 6. Traceability handoff

`pipeline-status.json` (written by the runner) carries, per task, the full chain:

```
requirement_refs → specification_refs → source_authority →
task_id → implementation_targets → validation_commands →
evidence_refs → status → blocker_class/blocker_reasons → provenance
```

plus the `stages` summary and `evidence_integrity` report. This is the durable
handoff between pipeline runs and the auditable record that no PASS was asserted
without executable evidence.

## 6.1 Execution → Observation → Validation → Evidence (Phase 22)

A successful exit status alone is **never** sufficient for PASS. Each validation
command records an **observation** into the (hash-chained) evidence:

```
Executor     → runs the declared command (shell=False, allowlisted, scope-guarded)
Observation  → target_hashes (deterministic target-state map) + observed_delta
Validator    → exit_status == expected_exit  (the command is the validator)
Evidence     → command result + observation + provenance, hash-chained
```

PASS additionally requires **result integrity**: the CURRENT target state must
match the state recorded at validation (`target_hashes` equality), and any
declared `expected_outputs` must currently exist with their declared hashes. If a
target is deleted/modified/replaced-by-symlink after validation, or a required
output is absent, PASS is withdrawn. Recovery reconstructs PASS only from
authoritative evidence + current observations — never from forged derived state.
See `execution-integrity-model.md`.

## 6.2 Criterion-level attestation (Phase 24)

For **strict** tasks (any criterion declares a `validator`), each criterion's
PASS is authorized only by its declared validator's evidence explicitly bound to
that criterion via the current contract:

```
requirement -> specification -> task -> criterion -> validator -> command
           -> observation -> criterion_evidence_id -> task status
```

`criterion_attestations` is a **derived view** (reuses command evidence + declared
coverage; no new storage). Each attested criterion gets a deterministic
`criterion_evidence_id = SHA256(canonical(contract_id, task_id, criterion_id,
validator, command_id, "PASS"))`. Closure is **per-criterion** for strict tasks;
command-level PASS never substitutes for criterion attestation. Legacy tasks
(no validators) are grandfathered. See `criterion-validation-model.md`.

## 7. Adding a task / resuming

- A new task is added to `implementation-plan.json` by the planner with full
  authority + requirement + validation + acceptance fields. Missing fields yield
  `BLOCKED — INSUFFICIENT_TASK_DEFINITION` (never guessed).
- **Semantic coverage (opt-in):** an acceptance criterion may declare a
  `validator` (the validation command id that covers it). When any criterion
  declares a validator, the controller enforces full criterion↔validator coverage
  at READY and per-command closure at PASS, so every criterion terminates in
  validator evidence: Requirement → Specification → Task → Criterion → Validator
  → Execution → Observation → Evidence. Tasks without declared validators use the
  legacy presence-based contract (grandfathered).
- On resume, the runner loads the checkpoint, recomputes dependencies, invalidates
  stale READY/IN_PROGRESS, and continues from the highest-priority valid READY task.
- Run: `python3 tools/run-implementation-pipeline.py --execute --allow-tool <tool>`.
