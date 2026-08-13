# Implementation Execution Controller

An executable, deterministic, **fail-closed** controller that transforms an
implementation plan (task manifest) into an executable task queue. It is
**Stage-5 infrastructure** for the five-stage pipeline:

```
Extraction → Knowledge Base → Repository Organization → Planning → Execution
```

The controller implements **no** Red/Cognition product features. Its job is to
model, classify, schedule, contract, and record evidence for implementation
tasks so that execution can resume deterministically the moment a legitimate
unblocking event occurs.

- **Language/runtime:** Python 3 standard library only (no PyYAML, no pytest).
- **Entry point:** `python3 tools/impl-controller.py ...`
- **Manifest (input):** `docs/implementation/implementation-plan.json`
- **Reports/checkpoints/evidence:** written only on demand (dry-run writes nothing).

## Command summary

```
python3 tools/impl-controller.py --self-test                       # unit suite (24 cases)
python3 tools/impl-controller.py --dry-run                         # classify+queue+contracts, writes nothing
python3 tools/impl-controller.py --dry-run --report OUT.json       # also write report
python3 tools/impl-controller.py                                   # plan mode: persist checkpoint
python3 tools/impl-controller.py --execute --allow-tool python3    # run validation for top READY task
```

Flags: `--manifest`, `--repo-root`, `--state`, `--evidence`, `--report`,
`--dry-run`, `--execute`, `--allow-tool` (repeatable), `--self-test`, `--quiet`.

Exit codes: `0` = controller success (PAUSED is success); `1` = validation
FAIL; `2` = manifest error; `3` = controller error.

## Task schema (minimum, extensible)

`task_id, title, description, priority, plan_order, scope,
source_authority[], requirement_refs[], specification_refs[],
implementation_targets[], dependency_refs[], required_tools[],
validation_commands[], acceptance_criteria[], evidence_refs[],
spec_conflicts[], spec_gaps[], declared_blockers[], allowed_tools[],
prohibited_scope[], provenance, rejected, deferred`.

Missing authoritative fields are **never guessed**; they surface as
`INSUFFICIENT_TASK_DEFINITION`.

## Dependency engine (deterministic, fail-closed)

For each task (precedence selects the *primary* blocker; all reasons are
reported):

```
rejected                       -> REJECTED
validated_pass                 -> PASS (terminal)
deferred                       -> DEFERRED
spec_conflicts | spec_gaps     -> BLOCKED  SPECIFICATION_CONFLICT | INCOMPLETE_SPECIFICATION
any dependency not PASS        -> BLOCKED  DEPENDENCY
required tool unavailable      -> BLOCKED  TOOLCHAIN
authority missing/not-on-disk  -> BLOCKED  INSUFFICIENT_TASK_DEFINITION
declared blocker unsatisfied   -> BLOCKED  <declared category>
else                           -> READY
```

Authority is verified by **file existence** (`source_authority[].doc` must
exist in the repo). PASS is the only state that satisfies a `PASS`
dependency, and PASS is never auto-promoted — it requires recorded evidence.

## READY queue ordering (documented metadata only)

`priority` (asc) → `dependency_depth` (asc) → `plan_order` (asc) → `task_id`.
No task is selected because it "looks useful"; no priority is manufactured.

## Execution contract

Generated **only** for READY tasks (`build_execution_contract` refuses
non-READY tasks — fail closed). It constrains scope, allowed files,
authoritative requirements, satisfied dependencies, validation commands,
acceptance criteria, prohibited scope, and required evidence.

## Checkpoint / resume

`StateStore` persists per-task state to JSON. On restart it reloads,
recomputes dependencies, and **invalidates stale READY/IN_PROGRESS** states
(`invalidate_stale`); terminal PASS/REJECTED/DEFERRED are preserved. The
controller never assumes prior state is still valid.

## Evidence model

Append-only JSONL (`EvidenceLog`). A PASS is never asserted without a captured
command + exit status. Records: `evidence_id, task_id, command, stdout, stderr,
exit_status, result{PASS|FAIL|BLOCKED|NOT_APPLICABLE}, failure_class,
timestamp, artifacts[]`. `--execute` refuses shell-metacharacter or
non-allowlisted commands.

## Failure classes

SPECIFICATION · DEPENDENCY · TOOLCHAIN · ENVIRONMENT · IMPLEMENTATION · TEST ·
INTEGRATION · AUTHORIZATION · INFRASTRUCTURE (plus documented sub-reasons
ARCHITECTURE / PROVISIONING / INCOMPLETE_SPECIFICATION / etc.). One class is
never converted into another merely to continue.

## Current frontier (dry-run)

Against `docs/implementation/implementation-plan.json` the controller reports
`frontier = PAUSED`, `READY = 0`, all four documented scopes correctly blocked:

| Task | Primary | Reasons |
|---|---|---|
| RED-LEX-001 | TOOLCHAIN | TOOLCHAIN, ARCHITECTURE, PROVISIONING, AUTHORIZATION |
| LIBRED-001 | DEPENDENCY | DEPENDENCY, TOOLCHAIN |
| HASH-001 | INCOMPLETE_SPECIFICATION | INCOMPLETE_SPECIFICATION, TOOLCHAIN |
| RFC0075-001 | SPECIFICATION_CONFLICT | SPECIFICATION_CONFLICT, INCOMPLETE_SPECIFICATION |

These classifications are **preserved, not altered**. RFC-0075 is kept
independent of the Rebol/toolchain blocker. See `dry-run-report.json`.

## Files

```
tools/impl-controller.py            launcher (keeps tools/ a non-package)
tools/impl_controller/
  __init__.py  model.py  manifest.py  engine.py  queue.py
  contract.py  evidence.py  checkpoint.py  controller.py  cli.py  __main__.py
  safety.py    validate_command + validate_targets (fail-closed)
  locking.py   FileLock (exclusive lease; fcntl, no external deps)
  tests/test_controller.py           24 cases (8 mandated + fail-closed/extras)
  tests/test_hardening.py            61 adversarial cases (categories A..N)
docs/implementation/
  implementation-plan.json           seed manifest (documented blockers)
  controller-readme.md               this document
  dry-run-report.json                last dry-run output (validation artifact)
```

## Pipeline integration (Stage-5 wiring)

The controller is wired into the repository pipeline as the Stage-5 orchestrator:

- **Runner:** `python3 tools/run-implementation-pipeline.py [--dry-run|--execute --allow-tool T]`
  — performs the planner gate (strict manifest load) → controller (classify/queue/
  contract) → executor/validator → writes the durable `pipeline-status.json`.
- **Evidence contract:** [`evidence-contract.md`](evidence-contract.md) — the
  planner→controller→executor→validator→status handoff, evidence schema, manifest
  lifecycle, and blocker-immutability policy.
- **Status/traceability artifact:** `pipeline-status.json` — per-task chain
  (requirement→spec→task→source→validation→evidence→status), `stages` summary,
  `evidence_integrity`, and `blocker_policy`.
- **CI:** `.github/workflows/implementation-pipeline.yml` — Linux/Python, no Rebol;
  asserts self-test PASS, real frontier `READY=0/PAUSED`, repository-index PASS,
  RFC-0075 FAIL (blocked).

The four current blockers are immutable unless an authoritative prerequisite
changes (tool availability, spec reconciliation, dependency PASS, or a new
authorized requirement).

## Hardening (v1.1.0) — adversarial safety properties

Validated by `tests/test_hardening.py` (61 cases). The controller fails closed:
uncertainty is never transformed into permission.

- **Manifest safety** — strict schema: unknown fields, malformed sub-objects
  (validation commands / blockers / deps / criteria), type errors, duplicate
  ids, unknown deps, duplicate evidence refs, and empty task lists are rejected;
  dependency cycles are detected and reported with the chain.
- **Command safety** — `safety.validate_command`: rejects shell metacharacters
  (`; & | > < $ backtick`), control chars / null, non-bare or path-containing
  executables, absolute/`..` arguments, and **shell-interpreter executables**
  (`sh bash dash …`) even if allowlisted; an empty allowlist authorizes nothing.
  Validation runs with `shell=False` (no shell at all).
- **Path safety** — `safety.validate_targets` confines implementation targets
  to the repo; rejects absolute, `..`, `~`, `.git/*`, and symlink escapes.
- **Authority safety** — authority docs must be readable files inside the repo
  (directories, unreadable, missing, and out-of-repo refs are rejected); drift
  (authority deleted after READY) reclassifies to BLOCKED.
- **Evidence integrity** — append-only JSONL with a SHA-256 hash chain
  (`prev_hash`/`record_hash`). A PASS is trusted only if the chain is intact to
  that record AND it is structurally valid (`exit_status == expected_exit`,
  non-empty command). Tampering, removal, or malformed lines break the chain
  and all subsequent records become untrusted (fail closed).
- **Checkpoint safety** — PASS is evidence-authoritative: a checkpoint claiming
  PASS without chain-verified evidence is demoted; corrupt/truncated checkpoints
  start clean; stale READY/IN_PROGRESS are invalidated each run.
- **PASS re-validation** — a PASS is re-checked every run against authority +
  dependency state; mutating a task's authority or invalidating a dependency
  demotes a prior PASS ("never assume previous state is valid").
- **Concurrency safety** — non-dry-run runs acquire an exclusive `FileLock`
  (`fcntl.flock`); a second controller on the same state is denied the lease.
- **Determinism** — classifications, blocking reasons, READY queue, and
  contracts are identical across runs given identical inputs (only timestamps
  vary).
- **Interruption safety** — a crash after `begin()` before evidence leaves the
  task non-PASS; resume recomputes and clears stale IN_PROGRESS.
