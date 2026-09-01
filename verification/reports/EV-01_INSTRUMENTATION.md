# EV-01 Instrumentation Commit

**Baseline frozen:** `805e75ce2848b2f19e21e86cfe5933eb16337080`  
**Purpose:** make Red container execution observable without changing Red/Rebol semantics.  
**Job timeout:** **20 minutes, unchanged.**

This commit is Work Order 1 / gate EV-01. It is **not** a Red repair, **not** an AF_ALG patch, and **not** a verification-status upgrade.

## Allowed changes made

- CI logging and process supervision
- timeout / cancellation diagnostics
- continuous artifact preservation
- exit-status and execution-state records
- environment / commit / image identity metadata
- a Rebol identity smoke check (environment, not Red tests)

## Changes not made

- no Red source changes
- no Red/System semantic changes
- no crypto implementation changes
- no expected-test-result changes
- no failure suppression or skip conversion
- no global timeout increase
- no provenance-claim changes
- no conflict-register edits
- no physical monorepo migration

The existing workflow still:

- checks out the repository
- enables i386 / Buildx
- verifies Rebol SHA-256 `1c902e0f75e994d739975e12963323832ce00f52208b3287cbfe5e7029d856d6`
- builds `red-cognition/rebol-bootstrap:2.7.8`
- runs `tools/run-container-tests.sh --out artifacts/test-run`
- uploads that directory even on cancellation

## Files

| File | Role |
| --- | --- |
| `tools/run-container-tests.sh` | Stream stdout, heartbeat, execution JSON, partial logs on signal |
| `.github/workflows/red-container-tests.yml` | Record GitHub/Rebol/image identity; keep `timeout-minutes: 20` |
| `verification/reports/EV-01_EXECUTION_OBSERVABILITY_CHECKPOINT.md` | Frozen diagnosis from `805e75ce` |
| `verification/reports/EV-01_INSTRUMENTATION.md` | This contract |

## Runner behaviour after this commit

```
identity smoke
   ↓
Red tests/run-all.r     (streamed + heartbeat)
   ↓
Red/System system/tests/run-all.r
   ↓
summary.json / summary.md
```

While a suite runs the wrapper now:

1. prints the exact command, commit, image, platform, and container name
2. streams container output (`tee`) and translates CR progress to newlines **only on the live log**
3. emits `==> <suite> still running: Ns` every 60 seconds
4. copies `quick-test.log` into the artifact directory during the run, not only after exit
5. records `docker top` when available
6. writes `<suite>.execution.json` with `STARTED` / `RUNNING` / `COMPLETED` / `FAILED` / `TIMED_OUT` / `CANCELLED`
7. writes a partial `summary.md` so cancellation still leaves attributable evidence

## Why `quick-test.log` is the critical artifact

`tests/run-all.r` uses quiet mode. Progress is often a carriage-return `prin` on stdout, while file summaries are appended to `quick-test/quick-test.log`.

The previous runner redirected Docker stdout to a file and `cat` that file **only after Docker exited**. It copied `quick-test.log` **only after the suite returned**. GitHub's 20-minute cancel therefore produced an ~804-byte artifact with no Red progress.

That is an observability defect, not evidence that Red produced no progress.

## States the runner may report

```
NOT_STARTED
STARTED
RUNNING
COMPLETED
FAILED
TIMED_OUT
CANCELLED
INFRASTRUCTURE_ERROR
INCOMPLETE
```

A timeout remains a valid EV-01 result if the artifact identifies:

- exact commit SHA
- Rebol SHA-256
- image identity
- exact Red command
- last heartbeat / last `quick-test.log` tail
- elapsed time
- that Red did not return

**Completion is not PASS.** PASS still requires both Red suites to finish with exit 0 and no failure markers.

## AF_ALG / RFC-0075 / conflicts

Unchanged and still separate:

- AF_ALG: failed / not remediated
- RFC-0075: 4 critical gaps
- conflict register: 389 open
- Red-Cognition product: not validated

## Next evidence

A fresh GitHub Actions run of **this** commit, not `805e75ce`.

Required fields:

```
commit = NEW_SHA
run_id = NEW_RUN_ID
Rebol SHA-256 verified
image built
identity smoke result
Red started
last observable marker
termination
artifact
```
