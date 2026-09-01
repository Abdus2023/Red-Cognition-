# EV-01 — Execution Observability Checkpoint

**Baseline HEAD:** `805e75ce2848b2f19e21e86cfe5933eb16337080`  
**Branch:** `audio`  
**Date:** 2026-09-01  
**Disposition:** PARTIALLY VERIFIED — execution materialized but not complete  
**Next gate:** EV-01 diagnostic CI commit → fresh GitHub Actions execution  

This document freezes the post-PR-#8 verification state and the CI timeout diagnosis. It is an evidence checkpoint, not a status upgrade. Historical CI evidence for PR head `cd00ea4` must not be treated as execution authority for merge commit `805e75ce`.

---

## 1. What changed materially

The project has moved from a primarily static acquisition/provenance exercise into a much more sophisticated execution-verification and reconciliation phase.

The new audit corpus now records:

### Acquisition / provenance

The earlier acquisition work reached a substantial closure state:

- 117 provenance records
- 137-file hash manifest
- whole-tree verification of collected Red tag archives
- official Red wiki material collected
- upstream drift checks
- provenance graph and reconciliation records
- Rebol/Red distribution-channel research
- binary/header identification
- explicit blocked-network attempts

The acquisition ledger's final consistency audit reported **0 hash mismatches**, **0 missing paths**, and **0 dangling provenance references**.

That is a meaningful strengthening of the provenance layer.

---

## 2. The monorepo consolidation is now much more rigorous

The current audit reports **1,310 tracked source/control files**.

The generated classification currently includes:

| Area | Count |
| --- | ---: |
| Documentation | 353 |
| RFC | 101 |
| Specification | 90 |
| Red/System source | 65 |
| Red runtime | 163 |
| Red compiler | 28 |
| Red tests | 240 |
| Red-Cognition | 115 |
| Red tooling | 33 |
| Red source | 22 |
| Red fixtures | 16 |
| Rebol source | 4 |
| Rebol bootstrap | 1 |
| Binary | 30 |
| Archive | 30 |

The important architectural decision is still non-destructive:

> the historical Red tree has not been physically flattened/reorganized merely to make the desired monorepo layout look cleaner.

The new architecture document explicitly describes the proposed `rebol/`, `red/`, `red-cognition/`, and `verification/` areas as a **logical overlay**, while preserving the existing upstream source paths.

That is the correct approach for a provenance-sensitive repository.

---

## 3. Upstream Red comparison is now much deeper

The repository explicitly fetched upstream Red v0.6.4 and compared local content against the pinned upstream commit:

`755eb943ccea9e78c2cab0f20b313a52404355cb`

The current comparison gives:

- **251** files identical at the same path
- **13** files whose content exists upstream under another path/name
- **258** same-path files diverged
- **781** local-only/non-upstream files

This is important:

- The repository is **not** simply a pristine Red v0.6.4 checkout.
- The audit does **not** incorrectly classify all 258 differences as either bugs or intentional modifications.
- They remain subject to provenance/maintainer review.

That distinction is exactly what we want.

---

## 4. The conflict register has become a major finding

Current conflict register:

**389 open conflicts**

| Conflict class | Count |
| --- | ---: |
| Upstream same-path divergence | 258 |
| Binary provenance gaps | 60 |
| Same-filename related variants | 57 |
| Upstream relocation/rename | 13 |
| RFC-0075 traceability failure | 1 |

No artifacts were automatically deleted, merged, or selected as authoritative.

This is particularly significant because several apparent "duplicates" are actually platform/runtime variants:

- `runtime/platform/linux.reds`
- `system/runtime/linux.reds`
- Android variants
- GTK/macOS variants
- compiler/test variants
- historical test variants

So **389 conflicts ≠ 389 bugs**.

They are unresolved provenance/layout/authority questions.

The correct next operation is **resolution, not deletion**.

For each conflict:

```
IDENTIFY
   ↓
ESTABLISH ORIGIN
   ↓
ESTABLISH AUTHORITY
   ↓
CLASSIFY
   ↓
OWNER DECISION if required
   ↓
ONLY THEN migrate/merge
```

That prevents the classic monorepo mistake of interpreting "same filename" as "same artifact."

---

## 5. The biggest new development: actual Rebol execution evidence

This is the most important update relative to the previous `1fb0923` state.

The newer verification material reports that the previously blocked Rebol environment was actually provisioned in the separate verification workspace.

The reported evidence says:

- Rebol 2.7.8.4.3 archive acquired
- executable identity matched the expected SHA-256
- 32-bit runtime dependencies were installed
- controlled Rebol identification executed
- arithmetic smoke tests executed
- Red v0.6.6 bootstrap was reproduced
- simple hello and print-test programs compiled
- controlled `quit-return 0` produced exit code 0

So the previous statement:

> “Stage 0 execution blocked because the host lacks the 32-bit runtime”

is no longer the complete picture.

There is now evidence of controlled Rebol execution in the dedicated verification environment.

However—and this is crucial—the evidence must remain classified according to **where and how** it was obtained.

The repository's own newer evidence explicitly separates:

- acquisition
- identity
- controlled execution
- bootstrap reproduction
- functional testing
- CI execution

That prevents the old epistemic mistake of converting one successful smoke test into "full bootstrap verified."

---

## 6. Red bootstrap has also advanced substantially

The newer verification report claims:

- Red v0.6.6
- Minimal bootstrap reproduced
- Two console programs were compiled successfully

More importantly, the broader compiler harness produced:

> **8,993 / 8,993 assertions passed**

for `run-all-comp1.red`.

The second group produced:

> **6,245 / 6,297 assertions passed**

with:

- 51 cryptographic failures
- 1 network-dependent path-thru failure

That is vastly stronger evidence than the previous purely historical/minimal-bootstrap state.

But it still does **not** constitute a clean full-suite pass.

---

## 7. The crypto failure was actually diagnosed

This is another major update.

The failure is localized to:

`runtime/crypto.reds`

The Linux AF_ALG implementation reportedly does not correctly propagate failures from:

- `socket`
- `bind`
- `accept`
- `write`
- `read`

On the verification host:

`socket(AF_ALG, SOCK_SEQPACKET, 0)`

returns:

`EAFNOSUPPORT`

The current implementation then continues and ultimately returns an invalid/uninitialized digest buffer.

That explains the malformed:

- MD5
- SHA
- HMAC

results.

This is much stronger than merely saying "crypto tests failed."

It is a reproduced functional failure with a plausible source-level root cause.

---

## 8. But the AF_ALG fix is NOT complete

This must remain absolutely explicit.

The latest remediation record says:

- AF_ALG remediation: **NOT APPLIED**
- Verified source fix: **NONE**
- Remediation commit: **NONE**
- Push: **NONE**

A defensive patch proposal exists, but it was deliberately **not applied** because its Red/System error construction and cleanup semantics were not sufficiently validated against canonical project conventions.

That is exactly the right epistemic treatment.

The proposed fix itself would not automatically make cryptographic functionality correct; it would primarily make backend failure explicit and safe.

A genuine fix requires either:

1. working AF_ALG support,
2. a validated alternate crypto backend, or
3. a self-contained implementation validated against the complete known-answer vectors.

**Do not merge AF_ALG with the CI timeout.** They are two separate execution findings.

### Finding 1 — Red suite timeout

```
CI
 └── Red execution
       └── does not complete
```

### Finding 2 — cryptographic failure

```
Red/System
 └── AF_ALG backend
       └── EAFNOSUPPORT
```

The second was observed during broader local execution.

The first is a CI execution-completion problem.

They may ultimately interact, but **we must not assume that the timeout is caused by AF_ALG** until execution evidence establishes that connection.

---

## 9. CI is still the hard authority

This remains the most important governance constraint.

The latest observed CI evidence says:

### Windows

- Run `33504164011`
- **FAILED**
- All Windows jobs failed at **Set up job**, before repository checkout / Red execution.

Therefore: this is **CI infrastructure failure**, not evidence that Red itself failed.

### Red container

- Run `33504164166`

The important sequence was:

| Step | Result |
| --- | --- |
| setup | PASS |
| checkout | PASS |
| i386 emulation | PASS |
| Docker Buildx | PASS |
| Rebol bootstrap download | PASS |
| SHA-256 verification | PASS |
| 32-bit image build | PASS |
| Red / Red-System test execution | **CANCELLED** (timed out) |
| report publishing | PASS |

The job exceeded its configured **20-minute** maximum.

The repository explicitly says **not** to interpret this as a successful Red test run.

### Critical lineage mismatch

`CI_EVIDENCE.md` says its observed PR head was:

`cd00ea4c3b500913d08019924a2ff9a5b40766b9`

while the current merged `audio` HEAD is:

`805e75ce2848b2f19e21e86cfe5933eb16337080`

Therefore:

> The CI evidence currently committed is historical evidence for the PR head, not CI evidence for the current merge commit.

Live status lookup for `805e75ce...` currently returns **no status checks**.

**Do not say “the current audio HEAD passed CI.”**

```
PR #8 HEAD
cd00ea4
   │
   ├── CI observed
   │      ├── Windows → SETUP FAILURE
   │      └── Container → TIMEOUT
   │
   ▼
MERGED
805e75c
   │
   └── current audio HEAD
          │
          └── NO CURRENT CHECK STATUS OBSERVED
```

This is not a contradiction. It is an evidence-lineage issue.

The next meaningful verification event is therefore:

**fresh CI execution against `805e75ce`**

—not another static re-audit.

---

## 10. Current local validation picture

The latest post-merge local audit is also stronger.

### PASS

- source-audit inventory generation
- supplemental manifests
- SHA-256 verification
- monorepo audit validator
- Python source compilation
- repository index validation
- upstream Red comparison
- binary/archive inventory
- risk report generation
- conflict register generation
- logical path-map generation

The monorepo audit validator reported:

**20 checks / 0 errors**

and the SHA-256 manifest passed.

### FAIL

`validate_rfc_0075_traceability.py` reported:

**4 unresolved critical gaps**

This remains a real failure and is not being hidden.

### BLOCKED

`python3 -m pytest tools/impl_controller/tests`

because pytest is unavailable in the environment.

This is correctly classified as **dependency-blocked**, not "tests failed."

### NOT RUN

Local Red/Rebol suites in that particular consolidation workspace.

That distinction matters because the separate `/home/ubuntu/red-cognition-verification` execution evidence should not automatically be relabeled as execution in every other workspace.

---

## 11. Important stale-artifact problem discovered

There is an interesting integrity/governance issue in the current state.

`docs/PROJECT-INVARIANTS.md` still contains the older invariant:

```
specified(1467) > implemented(1) > executed(0) > tested(0)
> validated(0) > evidenced(0) > formally_verified(0)
```

and says:

> Product code executed / tested / validated / evidenced = 0

That was correct for the earlier project-wide Red-Cognition product state, but it must not be casually interpreted as contradicting the new Rebol/Red toolchain execution evidence.

The document's purpose is to distinguish **product validation** from **governance/toolchain validation**.

That distinction should now be preserved carefully.

In other words:

- Toolchain execution has advanced.
- Product implementation validation has **not** thereby advanced.

That is completely consistent with the project's invariant:

**390 governance tests PASS ≠ product validation.**

Do **not** update a status document from `executed: 0` to `executed: 1` merely because the separate verification workspace successfully ran Rebol.

Instead distinguish:

```
TOOLCHAIN EXECUTION
    Rebol controlled execution = YES

RED-COGNITION PRODUCT EXECUTION
    = NOT ESTABLISHED
```

---

## 12. Current epistemic status

Updated assessment:

| Layer | Status |
| --- | --- |
| Repository integrity | PASS / strongly established |
| Acquisition provenance | HIGH CONFIDENCE / substantially verified |
| Rebol identity | VERIFIED |
| Rebol controlled execution | EXECUTED in dedicated verification environment |
| Red v0.6.6 bootstrap | REPRODUCED at minimal/console level |
| Red compiler broader tests | PARTIALLY EXECUTED / PARTIALLY PASSED (8,993/8,993; 6,245/6,297) |
| Cryptography | FUNCTIONALLY FAILED for current AF_ALG environment |
| AF_ALG remediation | NOT VERIFIED / NOT APPLIED |
| Full Red/Rebol suite | NOT VERIFIED |
| GitHub Actions | NOT PASSED |
| RFC-0075 | BLOCKED (4 critical unresolved gaps) |
| Red-Cognition product implementation | Still not validated |

Toolchain success must not be confused with product success.

---

## 13. The major conceptual transition

The repository has crossed an important boundary:

```
OLD STATE
─────────
acquisition
   ↓
hash/inventory
   ↓
bootstrap blocked
   ↓
PARTIALLY VERIFIED
```

Now it is closer to:

```
ACQUISITION
    │
    ▼
PROVENANCE / HASH INTEGRITY
    │
    ▼
REBOL 2 IDENTITY ───────── VERIFIED
    │
    ▼
CONTROLLED REBOL EXECUTION ───────── EXECUTED
    │
    ▼
RED v0.6.6 BOOTSTRAP ───────── REPRODUCED
    │
    ▼
BROAD RED TESTING
    ├── 8,993/8,993 PASS
    ├── 6,245/6,297 PASS
    ├── crypto failure
    └── network fixture failure
    │
    ▼
FULL EXECUTION ───────── INCOMPLETE
    │
    ▼
CI ───────── NOT PASSED
    │
    ▼
RED-COGNITION PRODUCT ───────── NOT VALIDATED
```

That is the correct updated mental model.

---

## Bottom line (post-refresh)

Yes — the repository has materially advanced.

The previous `1fb0923` picture should no longer be treated as the current state.

The strongest new evidence is:

> Rebol execution is no longer merely theoretically blocked; controlled execution and Red bootstrap reproduction have now been demonstrated in a dedicated verification environment.

But the project has not reached "fully verified":

```
INTEGRITY: PASS
PROVENANCE: STRONG / VERIFIED LAYERS
REBOL EXECUTION: EXECUTED
RED BOOTSTRAP: REPRODUCED
RED TESTING: PARTIAL
CRYPTO: FAILED
FULL SUITE: INCOMPLETE
RFC-0075: BLOCKED
CI: NOT PASSED
RED-COGNITION PRODUCT: NOT VALIDATED
```

And, critically, no AF_ALG remediation should be declared fixed until an actual repository commit compiles and the relevant known-answer tests execute successfully.

The current evidence therefore warrants a more advanced **PARTIALLY VERIFIED** state, not a full verification upgrade.

More precise phrasing:

> **PARTIALLY VERIFIED — repository integrity and provenance baseline established; controlled toolchain execution evidence exists; historical CI provisioning verified; current merged HEAD has no fresh execution evidence; full Red/Rebol execution and CI remain unverified.**

That is more rigorous than simply saying "CI failed," because the **current commit has not actually been tested**.

The old CI run failed/cancelled. The current merge is **untested**.

Those are epistemically different states, and that distinction must be preserved.

---

## 14. Direct GitHub Actions structure (run `33504164166`)

For the previously observed Red container run `33504164166`, GitHub reports:

- setup: **PASS**
- checkout: **PASS**
- i386 emulation: **PASS**
- Docker Buildx: **PASS**
- Rebol bootstrap download + verification: **PASS**
- 32-bit Rebol image build: **PASS**
- **Red / Red-System test execution: CANCELLED**
- test-report publishing: **PASS**

The underlying job `99844172388` confirms exactly the same sequence. This is direct workflow-step evidence rather than merely trusting the prose audit.

GitHub currently reports **no PR-triggered workflow runs associated with SHA `805e75ce`**.

Therefore:

**There is still no execution authority for the current `audio` HEAD.**

The old CI run proves that the workflow *can provision* the Rebol environment and construct the 32-bit image. It does **not** prove that `805e75ce` passes the tests.

```
                 805e75ce
               current audio HEAD
                      │
                      ▼
              ┌───────────────┐
              │ Static audit  │
              │    PASS       │
              └───────┬───────┘
                      │
                      ▼
         provenance / inventory /
         manifests / architecture
                      │
                      │
              separate evidence
                      │
                      ▼
              ┌───────────────┐
              │ Historical CI │
              │  NOT PASSED   │
              └───────┬───────┘
                      │
         provisioning succeeded
                      │
                      ▼
              test execution
                  CANCELLED
```

---

## 15. The CI timeout is now diagnosable from the actual job log

The actual job log for run `33504164166` changes the diagnosis significantly.

### What the log proves

The container was successfully constructed and was genuinely capable of executing the 32-bit environment:

- QEMU `linux/386` installed successfully.
- Rebol binary downloaded.
- SHA-256 verification returned **`rebol: OK`**.
- `file rebol` identified a valid **ELF 32-bit i386 executable**.
- The Debian i386 image was built successfully.
- The resulting image contained the Rebol binary.
- BuildKit completed successfully.

Then the actual test command started:

```
tools/run-container-tests.sh \
  --image red-cognition/rebol-bootstrap:2.7.8 \
  --out artifacts/test-run
```

and reported:

```
==> Running red
```

It then remained in that operation for roughly **15 minutes 52 seconds** before GitHub cancelled it at the 20-minute job limit.

So this is **not merely "Docker didn't work."**

The test runner actually entered the Red execution phase.

### New execution classification

| Gate | Finding |
| --- | --- |
| GitHub runner | **PASS** |
| i386 emulation | **PASS** |
| Rebol acquisition | **PASS** |
| Rebol SHA-256 identity | **PASS** |
| ELF32 loader environment | **PASS** |
| Docker image build | **PASS** |
| Rebol/Red test invocation | **STARTED** |
| Red test completion | **NOT ACHIEVED** |
| Red test result | **UNKNOWN** |
| CI job | **FAILED/CANCELLED by timeout** |

This is more precise than calling the entire container execution simply "blocked."

The test **did execute far enough to enter `red`**, but we do not have a completed result.

### The timeout is probably inside `red`

```
setup
  ↓
download Rebol
  ↓
verify Rebol
  ↓
build image
  ↓
run-container-tests.sh
  ↓
==> Running red
  ↓
[~15m52s with no completion]
  ↓
GitHub timeout
```

Therefore the next investigation should target:

**`tools/run-container-tests.sh` → the exact command launched after `==> Running red`**

rather than Docker provisioning.

### Non-blocking CI-quality issues

The Docker build emits:

```
FromPlatformFlagConstDisallowed: FROM --platform flag should not use constant value "linux/386"
```

This is a **warning**, not the cause of the timeout.

It should eventually be cleaned up, but it is not currently a verification blocker.

Similarly, the Node 20 deprecation warnings are environmental/action-maintenance issues, not evidence that Red failed.

Keep these separate:

```
REAL BLOCKER
 └── Red test invocation does not complete

NON-BLOCKING TECHNICAL DEBT
 ├── Dockerfile constant --platform warning
 └── GitHub Action Node 20 deprecation
```

### The artifact is particularly interesting

The test-report artifact was actually created:

`red-container-test-results-33504164166`

and GitHub says it contained **2 files**, only **804 bytes** total.

That means the timeout did not prevent the workflow's reporting stage from running.

If it contains partial output, we may be able to identify:

- the exact Red command,
- the last test reached,
- whether the process was waiting,
- whether output buffering hid progress,
- whether a specific suite hung,
- whether the test runner spawned a child process.

### Do **not** increase the timeout blindly yet

First determine **what `Running red` actually invokes**.

Because if the command is hanging on one specific Red test, increasing the timeout merely hides the defect.

The correct sequence is:

1. inspect `tools/run-container-tests.sh`;
2. identify the exact `red` invocation;
3. inspect the test ordering;
4. inspect whether output is buffered;
5. inspect the 804-byte artifact;
6. reproduce the exact command in the same i386 container;
7. establish whether the first failing/hanging test is deterministic;
8. only then modify timeout/test partitioning.

### Ideal result

Turn the monolithic:

```
Run Red and Red/System container tests
```

into independently observable phases:

```
Rebol smoke
Red bootstrap
Red compiler smoke
Red/System tests
runtime tests
crypto tests
network tests
full regression
```

Then a 20-minute ceiling cannot erase the evidence of *where* execution stopped.

### Updated classification of the CI defect

**The CI environment has been materially validated as capable of provisioning and launching the 32-bit Rebol/Red execution path.**

But:

**The Red suite has not completed, and no test-pass conclusion is justified.**

The failure is now best classified as:

### **EXECUTION STARTED → RED TEST PHASE TIMEOUT → RESULT UNDETERMINED**

rather than simply:

### `EXECUTION BLOCKED`.

---

## 16. Exact current runner architecture (`805e75ce`)

Inspection of the current `805e75ce` versions of both the container runner and its GitHub Actions workflow gives a concrete finding stronger than the earlier hypothesis.

### Finding: the timeout is externally imposed

The workflow has:

```
timeout-minutes: 20
```

and invokes:

`tools/run-container-tests.sh`

The script itself has **no execution timeout** around either suite. It runs:

```
Red
  ↓
Red/System
```

sequentially and waits for each Docker invocation to return.

Therefore the previous CI timeout means:

> GitHub Actions killed the job while the first Red suite was still running.

It does **not** demonstrate that the Red suite itself has an internal 20-minute timeout or that it reached a particular test and stopped there.

### The exact execution architecture

```
GitHub Actions
   │
   │ timeout = 20 min
   ▼
run-container-tests.sh
   │
   ├── docker run
   │      │
   │      └── Rebol -qws tests/run-all.r --batch
   │
   ├── wait indefinitely
   │
   ├── capture stdout.log
   │
   └── only after Red exits:
          │
          ▼
       Red/System
```

The first suite is:

```
/opt/rebol/rebol -qws tests/run-all.r --batch
```

inside:

`linux/386`

with the repository mounted at `/red`.

Therefore **Red/System never even gets a chance** in that CI run if Red does not terminate.

### Second observability problem: output buffering

The runner redirects the complete Red process output to:

`red.stdout.log`

and only executes:

```
cat "$log"
```

after Docker exits.

So while Red is running, GitHub's live log does not receive Red's incremental output.

That means:

```
==> Running red
```

followed by silence does **not** mean Red itself produced no progress.

It means the wrapper is buffering the output in a file.

This is probably the single most important diagnostic weakness in the current workflow.

### What we know vs. what we don't

**What we know**

```
Red process launched
        ↓
process did not return before GitHub's 20-minute deadline
        ↓
GitHub cancelled job
```

**What we DON'T know**

- Which Red test was running?
- Did compilation finish?
- Was a test executing?
- Was it waiting?
- Was it deadlocked?
- Was it CPU-bound?
- Was output merely buffered?
- Did it spawn a child?

Those questions remain unanswered.

> The timeout is real, but the hang location is currently unknown.

### Structural weakness of the summary stage

The current script's final Python stage computes `overall_pass` from the exit codes and parsed failure markers.

That is good only if both suites complete.

If GitHub kills the job before the Python summary stage, there is no complete authoritative summary.

So the CI layer currently has a structural weakness:

> abnormal termination can destroy the highest-value diagnostic state unless the shell runner continuously persists it.

The existing artifact upload with `if: always()` is helpful, but it cannot recover data that was never flushed into the output artifact before the job was terminated.

### Most precise description of the CI defect

> The current container workflow successfully provisions the i386 Rebol environment and launches `tests/run-all.r`, but the Red suite does not return within the workflow's 20-minute job deadline. Because the runner buffers the suite's output until process exit, the current evidence does not localize the execution stall.

Next step: **instrument `tools/run-container-tests.sh` rather than modifying Red blindly.**

---

## 17. Frozen baseline

```
HEAD: 805e75ce2848b2f19e21e86cfe5933eb16337080
BRANCH: audio

INTEGRITY          PASS
PROVENANCE         SUBSTANTIALLY VERIFIED
MONOREPO AUDIT     PASS
REBOL IDENTITY     VERIFIED
REBOL EXECUTION    EXECUTED
RED BOOTSTRAP      REPRODUCED
RED TESTING        PARTIAL
CI CURRENT HEAD    NO FRESH RESULT
AF_ALG             FAILED / UNREMEDIATED
RFC-0075           BLOCKED
PRODUCT            NOT VALIDATED
```

That should now be treated as the **frozen baseline**.

Do not rewrite historical reports to make them appear to describe a future run.

The evidence relationship should remain:

```
805e75ce
   │
   ├── static/provenance evidence
   │
   └── historical CI evidence
          └── Red execution timed out
```

Any new diagnostic commit becomes a new evidence generation point.

There is now **no justification for another giant static audit**.

---

## 18. Independent tracks

### Track A — CI execution (highest priority)

The previous run proves:

```
GitHub runner
   ↓
i386
   ↓
Rebol
   ↓
Docker
   ↓
Red
   ↓
TIMEOUT
```

The current merge commit has no fresh result.

A useful run must record:

```
commit SHA
workflow run ID
job ID
container image digest
Red executable identity
test command
start timestamp
end timestamp
exit code
timeout status
test progress
artifacts
```

The important field is **commit SHA**.

Every conclusion must be attached to the exact commit that executed.

Possible causes of no workflow on the merge include:

1. merge commits do not trigger the relevant workflow,
2. workflow configuration only responds to PR events,
3. the branch protection/check configuration is not attached to `audio`,
4. workflow trigger/path filtering excludes the merge,
5. a workflow dispatch/re-run is required,
6. the merge occurred without a new execution-producing commit.

Establish which one is actually true before changing anything.

### Track B — Red timeout

The timeout should be treated as an independent defect until proven otherwise.

Investigation hierarchy:

```
1. Does Red start?
        ↓ yes
2. Does the entrypoint load?
        ↓
3. Does compilation begin?
        ↓
4. Which test group is reached?
        ↓
5. Which test is last observed?
        ↓
6. What process is waiting?
        ↓
7. Why?
```

If the runner currently executes one enormous test command, the first improvement should be **observability**, not functionality.

### Track C — AF_ALG

The crypto issue is already sufficiently localized to become its own work item.

```
AF_ALG
  ↓
socket()
  ↓
EAFNOSUPPORT
  ↓
error not propagated safely
  ↓
invalid/uninitialized digest
  ↓
51 crypto failures
```

**Do not mark this repaired.**

Correct remediation lifecycle:

```
diagnosis
   ↓
minimal patch
   ↓
compile
   ↓
focused crypto vectors
   ↓
full crypto suite
   ↓
CI execution
   ↓
verified
```

Until the last stages occur, the status remains **NOT VERIFIED**.

### Track D — RFC-0075

This should **not** be mixed into the Red execution repair.

There are four critical traceability gaps.

That is a governance/documentation failure, not evidence that the runtime is broken.

```
Runtime execution
        ≠
RFC traceability
```

Resolve the four mappings independently and preserve their evidence.

### Track E — 389 conflicts

This is the largest structural queue, but it should **not** be attacked by mass normalization.

```
258 upstream divergence
60 binary provenance
57 same-name variants
13 relocation/rename
1 RFC-0075
```

Each conflict should eventually reach one of:

```
IDENTICAL
INTENTIONAL DIVERGENCE
UPSTREAM VARIANT
LOCAL VARIANT
DUPLICATE
SUPERSEDED
OWNER DECISION REQUIRED
```

No deletion merely because two paths look similar.

Prioritize:

#### Tier 1 — correctness-sensitive

- upstream same-path divergences affecting executable code
- compiler/runtime variants
- binaries required for bootstrap
- RFC-0075-related conflict

#### Tier 2 — provenance

- 60 binary provenance gaps

#### Tier 3 — structural

- same-filename variants
- relocations
- documentation-only divergence

### Track F — physical monorepo migration

This should remain **last**.

The logical architecture is already defined.

Physical movement should happen only after:

```
source hash
   ↓
record provenance
   ↓
move
   ↓
destination hash
   ↓
record old → new path
   ↓
validate manifests
   ↓
validate build/test references
```

Otherwise we risk turning a clean provenance problem into a migration problem.

The older documentation apparently described a physical structure like:

```
rebol/
red/
red-cognition/
verification/
```

The new architecture explicitly corrects this:

```
CURRENT CHECKOUT
        │
        ├── historical Red tree remains in place
        │
        ├── provenance preserved
        │
        └── conceptual monorepo map
                 │
                 └── NOT YET MOVED
```

The migration policy requires:

**hash before → move → hash after → record old/new path → record transformation**

before physical relocation.

---

## 19. Verification ladder

```
                 ┌─────────────────────────┐
                 │  FULLY VERIFIED         │
                 └────────────▲────────────┘
                              │
                    complete CI execution
                              │
                 ┌────────────┴────────────┐
                 │  EXECUTION VERIFIED     │
                 └────────────▲────────────┘
                              │
                    complete test suite
                              │
                 ┌────────────┴────────────┐
                 │  EXECUTION MATERIALIZED │
                 └────────────▲────────────┘
                              │
                   controlled execution
                              │
                 ┌────────────┴────────────┐
                 │  PARTIALLY VERIFIED     │
                 └────────────▲────────────┘
                              │
                   provenance + static
                              │
                 ┌────────────┴────────────┐
                 │  ACQUIRED / ARCHIVED    │
                 └─────────────────────────┘
```

The repository is currently between:

**PARTIALLY VERIFIED**

and

**EXECUTION MATERIALIZED**.

It has meaningful execution evidence, but not complete execution authority for the current merged state.

### Two evidence planes

```
             RED-COGNITION
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
  PROVENANCE PLANE       EXECUTION PLANE
        │                     │
  SHA-256               GitHub Actions
  inventories           exact commit
  upstream mapping      runtime
  conflict register     test result
        │                     │
        └──────────┬──────────┘
                   ▼
              GOVERNANCE
```

The provenance plane is already strong.

The execution plane is where the current work belongs.

---

## 20. Execution gates

### EV-01 — Current-HEAD execution materialization

The purpose is **not yet to prove Red passes**.

It is to prove that the current repository can produce a complete, attributable execution record.

```
805e75ce / successor commit
        ↓
GitHub Actions
        ↓
Rebol identity
        ↓
i386 environment
        ↓
Red invocation
        ↓
observable test progress
        ↓
termination
        ↓
exit status
        ↓
artifact
```

#### Minimum acceptance criteria

| Criterion | Required |
| --- | --- |
| Exact commit SHA recorded | YES |
| Rebol SHA-256 verified | YES |
| i386 environment verified | YES |
| Exact Red command recorded | YES |
| stdout/stderr continuously preserved | YES |
| Test progress observable | YES |
| Process termination observed | YES |
| Exit status captured | YES |
| Partial output preserved on timeout | YES |
| Artifact attached to run | YES |

A timeout can therefore be a **valid EV-01 diagnostic result** if it tells us exactly where execution stopped.

Pass condition is **not** “all tests pass.”

The first pass condition is:

> **We can determine exactly how far the current Red execution gets and why it terminates or fails to terminate.**

Required evidence checklist:

```
[ ] exact commit
[ ] exact Rebol hash
[ ] exact Docker image
[ ] exact Red command
[ ] live output
[ ] suite start
[ ] suite termination
[ ] exit code
[ ] elapsed time
[ ] partial/full logs
[ ] artifact
```

### EV-02 — Red test completion

Once EV-01 gives us a reproducible execution path:

```
Red suite
   ↓
complete
   ↓
zero unexplained failures
   ↓
zero infrastructure ambiguity
```

Only then can we say:

**Red execution verified for that exact commit.**

### EV-03 — Crypto

```
AF_ALG backend
      ↓
known-answer vectors
      ↓
MD5 SHA HMAC
      ↓
PASS
```

If AF_ALG is unavailable on the runner, the expected behavior must itself be explicit.

There are two different valid outcomes:

#### Backend unavailable

```
AF_ALG unavailable → clean capability error → test classified SKIP/ENVIRONMENTAL
```

#### Backend available

```
AF_ALG available → vectors execute → PASS
```

What is **not acceptable** is the current behavior where backend failure propagates into an apparently valid but incorrect digest.

### EV-04 — RFC traceability

The four RFC-0075 gaps should be resolved with evidence records, not prose assertions.

For every requirement:

```
RFC requirement
      ↓
implementation/artifact
      ↓
verification method
      ↓
verification result
      ↓
evidence reference
```

Then rerun the traceability validator.

The gate is:

**4 critical gaps → 0 critical gaps.**

### EV-05 — conflict closure

Do not demand `389 → 0` before execution can proceed.

Instead establish a controlled disposition:

```
389 OPEN
   ↓
classify
   ↓
owner decision where required
   ↓
resolved / intentionally retained
```

The important invariant is:

> **Every remaining conflict has an explicit disposition.**

An intentionally divergent upstream file does not need to be deleted merely to make the count zero.

### EV-06 — physical consolidation

Only after provenance and execution are stable should physical paths be moved.

Every migration needs:

```
old path
old hash
new path
new hash
transformation
provenance reference
```

Then regenerate:

- manifests
- repository index
- conflict register
- audit reports

The physical migration is therefore a **derived operation**, not the source of truth.

### EV-07 / EV-08 numbering (project-control ledger)

```
EV-00  Repository baseline
       805e75ce
       COMPLETE

EV-01  Current-head execution observability
       PENDING

EV-02  Red completion
       BLOCKED BY EV-01

EV-03  Red/System completion
       BLOCKED BY EV-02

EV-04  Crypto correctness
       INDEPENDENT / FAILED CURRENTLY

EV-05  RFC-0075 traceability
       BLOCKED / 4 GAPS

EV-06  Conflict disposition
       389 OPEN

EV-07  Physical consolidation
       DEFERRED

EV-08  Red-Cognition implementation
       NOT STARTED AS VALIDATED PRODUCT
```

---

## 21. Execution contract for the diagnostic commit

### Allowed

- CI logging
- process supervision
- timeout diagnostics
- artifact preservation
- test-stage boundaries
- exit-status propagation
- environment metadata

### Not allowed

- Red source changes
- Red/System semantic changes
- crypto implementation changes
- changing expected test results
- suppressing failures
- converting failures into skips
- increasing the global timeout merely to obtain a green check
- changing provenance claims

This makes the next commit **epistemically clean**.

### Failure-transparent runner

Current architecture:

```
run Red
   ↓
wait
   ↓
if Red exits:
    print log
```

Desired architecture:

```
start Red
   ↓
stream output
   ↓
record heartbeat
   ↓
record process state
   ↓
preserve partial output
   ↓
wait for termination
   ↓
record exit/signal
```

A CI system should never turn “we don't know what happened” into “test failed” or “test passed.”

It should produce:

**EXECUTION INCOMPLETE — cause/data available.**

### Explicit execution-state vocabulary

Recommended runner states:

```
NOT_STARTED
STARTED
RUNNING
COMPLETED
FAILED
TIMED_OUT
CANCELLED
INFRASTRUCTURE_ERROR
```

Then the final report can distinguish:

```
Red:
  state = TIMED_OUT
  exit_code = unavailable
  completion = false
```

instead of treating timeout as an ordinary test failure.

### Separate process failure from test failure

There are three fundamentally different cases:

#### Test failure

```
Red exits normally
exit = non-zero
test framework reports failures
```

#### Runtime failure

```
Red process crashes
signal / abnormal exit
```

#### Execution timeout

```
Red remains running
CI terminates job
no final test result
```

These must never be collapsed into one status.

### Machine-readable execution record

The runner should ultimately emit something equivalent to:

```json
{
  "commit": "...",
  "rebol_sha256": "...",
  "image": "...",
  "architecture": "linux/386",
  "suite": "red",
  "command": "...",
  "started_at": "...",
  "ended_at": "...",
  "state": "...",
  "exit_code": null,
  "signal": null,
  "log": "red.stdout.log"
}
```

The exact schema should follow the repository's existing evidence conventions rather than introducing a competing format.

The important principle is:

> **The report describes what actually happened; it does not infer what should have happened.**

### Preserve CI vs local reproduction

After EV-01, we may obtain:

```
LOCAL Red hangs at test X
```

That is excellent diagnostic evidence.

But it remains **LOCAL EXECUTION EVIDENCE** until GitHub executes the same relevant commit.

Conversely:

```
CI Red hangs at test X
```

is authoritative evidence that the CI environment reproduced the problem.

The strongest state is:

```
CI failure
   ↕
local reproduction
```

with the same:

- commit
- architecture
- input
- command
- failure location

### Two-level timeout (later, from observed duration)

Eventually the runner should distinguish:

```
GLOBAL CI DEADLINE
        │
        └── protects GitHub job

SUITE DEADLINE
        │
        └── protects individual Red phase
```

For example:

```
CI job
 ├── setup
 ├── Red suite [bounded]
 ├── Red/System suite [bounded]
 └── reporting
```

This prevents a single suite from consuming the entire CI budget and leaving no opportunity for subsequent evidence.

**The actual timeout values should be chosen from observed execution duration, not guessed now.**

The existing two-suite design is already useful:

```
RED
   ↓
RED/SYSTEM
```

First make the existing boundary observable.

If Red completes, we automatically learn whether Red/System is reached.

If Red doesn't complete, the problem is conclusively localized to the first phase.

---

## 22. Recommended diagnostic runner improvements

The wrapper should:

1. emit the exact command;
2. stream stdout/stderr using `tee`;
3. record the Docker PID;
4. periodically emit elapsed time;
5. install a cleanup trap;
6. produce diagnostics when the process is terminated;
7. optionally support a per-suite timeout;
8. preserve the partial log.

Conceptually:

```
==> Running red
    image=...
    script=tests/run-all.r
    platform=linux/386
    started=...

[streamed Red output]

==> red still running: 60s
==> red still running: 120s
...
```

Then if GitHub kills the job:

```
==> RED SUITE DID NOT COMPLETE
==> elapsed=...
==> partial log preserved
```

Change container execution from:

```
docker ... >"$log" 2>&1
```

to an equivalent arrangement that simultaneously:

- preserves the complete file;
- streams output to the Actions log.

Conceptually:

```
docker ... 2>&1 | tee "$log"
```

while preserving the correct Docker exit status with `pipefail`.

This alone may immediately expose the stopping point.

Before launching, record:

```
suite=red
script=tests/run-all.r
image=red-cognition/rebol-bootstrap:2.7.8
platform=linux/386
rebol=/opt/rebol/rebol
commit=805e75ce...
```

The current workflow already uses `if: always()` for artifact publication, which is good.

But the runner should ensure that the partial log is continuously written rather than relying on a final `cat`.

### Better still: split the execution

Current:

```
Red
  └── tests/run-all.r
       ↓
Red/System
  └── system/tests/run-all.r
```

Recommended:

```
RED
 ├── bootstrap
 ├── compiler
 ├── runtime
 ├── crypto
 └── network

RED/SYSTEM
 ├── compiler
 ├── runtime
 └── platform
```

Each phase gets:

- its own start/end
- exit code
- log
- duration
- artifact
- explicit status

Then a single problematic test cannot hide every other result.

**Do not increase the 20-minute timeout yet.**

Suppose the suite contains an infinite loop:

```
20 min → timeout
60 min → timeout
120 min → timeout
```

Increasing the timeout only delays discovery.

If instead the suite legitimately takes 25 minutes, the evidence will tell us that too.

So the correct order is:

**observe → reproduce → classify → repair → rerun.**

The current workflow itself is otherwise reasonably conservative:

- checks out the repository
- enables i386
- verifies the Rebol SHA-256
- builds the 32-bit image
- invokes the repository runner
- uploads test artifacts even after failure

That means we don't need a wholesale CI redesign.

We need **better execution telemetry**.

---

## 23. Work orders

### Work Order 1 — CI observability

**Scope:** `.github/workflows/red-container-tests.yml` + `tools/run-container-tests.sh`

Do only diagnostic changes:

- identify exact commit
- identify Rebol binary hash
- print container/image identity
- print exact command
- stream Red output
- retain complete logs
- capture exit code
- capture elapsed time
- preserve diagnostics on cancellation

**No Red source changes.**

### Work Order 2 — Fresh CI

Push the diagnostic-only change.

Then inspect the resulting GitHub Actions run.

The evidence must be attached to the **new commit**, not `805e75ce`.

Expected evidence:

```
commit = NEW_SHA
run = NEW_RUN_ID
job = NEW_JOB_ID

Rebol = SHA VERIFIED
container = BUILT
Red = STARTED

last observable stage = ?
termination = ?
exit code = ?
```

#### Decision tree after the run

**If Red completes**

Immediately record:

```
RED EXECUTION = COMPLETE
```

Then classify its actual result:

```
PASS
FAIL
PARTIAL
```

Do not infer PASS from completion.

A successful completion does **not** automatically mean **Red suite PASS**.

It means **Red suite EXECUTION COMPLETED**.

The test result must be separately established.

Then the previous timeout was likely:

- unusually slow execution,
- output/runner interaction,
- resource variability,
- or a transient infrastructure condition.

**If Red fails**

Capture the first deterministic failure.

Then reproduce **only that failure** locally.

Example:

```
CI:
  test X → failure

Local:
  test X → same failure
```

Only after that do we patch.

**If Red hangs**

This is the highest-value outcome for diagnosis.

Use the final streamed marker to isolate:

```
suite
  ↓
group
  ↓
test
  ↓
runtime operation
```

Then reproduce it in the same 32-bit environment.

**If infrastructure fails**

Classify it separately:

```
CI INFRASTRUCTURE FAILURE
```

No Red verdict.

### Work Order 3 — AF_ALG

After Red execution is understood, create a separate remediation branch/commit.

The patch must answer the actual failure:

```
socket(AF_ALG)
        ↓
EAFNOSUPPORT
        ↓
what should Red/System do?
```

The expected behavior must be explicit.

A backend that cannot be used should produce a controlled failure—not undefined digest output.

Then run:

```
MD5 vectors
SHA vectors
HMAC vectors
```

and only afterward the broader crypto tests.

The first successful AF_ALG repair requires:

```
source patch
   ↓
compile
   ↓
MD5 vectors
   ↓
SHA vectors
   ↓
HMAC vectors
   ↓
full crypto group
   ↓
fresh CI
```

### Work Order 4 — RFC-0075

Resolve the four critical gaps one by one.

| Requirement | Artifact | Evidence | Status |
| --- | --- | --- | --- |
| RFC-0075-01 | … | … | RESOLVED |
| RFC-0075-02 | … | … | RESOLVED |
| RFC-0075-03 | … | … | RESOLVED |
| RFC-0075-04 | … | … | RESOLVED |

Then run the existing validator.

Acceptance: **0 critical gaps.**

Do **not** use execution progress to close the four traceability gaps.

### Work Order 5 — conflict register

Do not bulk-resolve.

Prioritize executable artifacts:

1. compiler
2. runtime
3. Red/System
4. bootstrap
5. binaries
6. tests
7. documentation

Every decision should preserve:

```
origin
authority
path
hash
relationship
decision
```

### Work Order 6 — monorepo migration

Only after the above is stable.

The migration should be **hash-preserving** wherever possible.

For example:

```
red-old/path/foo.reds
      SHA256 = X
           ↓
red/runtime/foo.reds
      SHA256 = X
```

If the hash changes, the transformation must be explicitly documented.

### Work Order 7 — Red-Cognition itself

This is the point where we finally distinguish the acquired toolchain from the actual project.

The first product-level milestone should be a **single vertical slice**, not a massive implementation.

```
RFC/spec
   ↓
implementation
   ↓
compile
   ↓
test
   ↓
CI
   ↓
evidence
```

That creates the first genuine:

**specified → implemented → executed → tested → evidenced**

transition for Red-Cognition.

---

## 24. Outcome table after EV-01

| Observation | Interpretation |
| --- | --- |
| Red completes + exit 0 | Red phase completed successfully |
| Red completes + test failures | Functional failure |
| Red crashes | Runtime/process failure |
| Red hangs + reproducible marker | Localizable execution defect |
| Red hangs + no progress | Further process-level diagnosis |
| Docker dies | Container/infrastructure failure |
| GitHub cancels before runner starts | CI admission/infrastructure |
| Workflow completes but artifact missing | Reporting defect |

No status upgrade occurs merely because the workflow becomes greener.

Then the first source-level repair becomes evidence-driven.

Suppose EV-01 shows:

```
last marker: compiler test 417
```

Then the next task is no longer “Fix Red timeout.”

It becomes “Investigate compiler test 417 and the operation immediately preceding the hang.”

That is a dramatically smaller problem.

Likewise, if the evidence ends at:

```
loading runtime/crypto.reds
```

then the AF_ALG hypothesis becomes more relevant.

If it ends in:

```
network test
```

then the existing network-dependent failure becomes relevant.

**The evidence determines the branch.**

---

## 25. After timeout isolation

The order should be:

1. Isolate hang — **No semantic patch yet.**
2. Reproduce locally — same image, same architecture, same command.
3. Identify cause — potential classes:
   - Red compiler infinite loop
   - Red/System runtime deadlock
   - process invocation issue
   - filesystem assumption
   - stdin interaction
   - network dependency
   - test-order dependency
   - architecture-specific behavior
   - output buffering
   - resource exhaustion
4. Apply smallest fix — only after cause is demonstrated.
5. Run focused test: `failing test → PASS`
6. Run surrounding group: `group → PASS`
7. Run full suite: `full suite → completion`
8. Push — only then does GitHub Actions become the authoritative final gate.

---

## 26. Status model going forward

Stop using one global “verified/not verified” label.

Use:

```
PROVENANCE
  VERIFIED

INTEGRITY
  VERIFIED

TOOLCHAIN IDENTITY
  VERIFIED

TOOLCHAIN EXECUTION
  PARTIALLY VERIFIED

CI EXECUTION
  CURRENT HEAD UNVERIFIED

RED FUNCTIONALITY
  PARTIALLY EXECUTED

CRYPTO
  FAILED / UNREMEDIATED

RFC TRACEABILITY
  BLOCKED

CONFLICT RECONCILIATION
  OPEN

PRODUCT IMPLEMENTATION
  NOT VALIDATED
```

This is much harder to misinterpret.

### Layer table (authoritative)

| Layer | Status |
| --- | --- |
| Repository integrity | PASS |
| Acquisition provenance | SUBSTANTIALLY VERIFIED |
| Monorepo inventory | VERIFIED/GENERATED |
| Logical architecture map | ESTABLISHED |
| Physical monorepo migration | NOT PERFORMED |
| Upstream Red comparison | EXECUTED |
| Conflict reconciliation | OPEN — 389 records |
| Rebol identity | VERIFIED |
| Rebol controlled execution | EXECUTED in verification environment |
| Red bootstrap | REPRODUCED |
| Red compiler tests | PARTIAL |
| Crypto | FAILED — AF_ALG backend issue |
| AF_ALG remediation | NOT APPLIED |
| Full Red suite | NOT VERIFIED |
| RFC-0075 | FAILED / 4 critical gaps |
| PR #8 | MERGED |
| Current audio CI | NO CURRENT STATUS EVIDENCE |
| Historical PR CI | FAILED / TIMEOUT |
| Red-Cognition product validation | NOT ESTABLISHED |

---

## 27. Evidence classification ledger

| Evidence | Authority |
| --- | --- |
| SHA-256 / provenance | repository audit |
| Static inventory | repository audit |
| Local Red execution | diagnostic |
| Local AF_ALG failure | diagnostic |
| Historical GitHub Actions | CI execution evidence |
| Current `805e75ce` CI | **not established** |
| New CI commit after diagnostic change | **execution authority** |

This prevents an especially dangerous mistake:

> modifying the CI workflow and then treating the workflow's own newly generated output as proof that the underlying software is correct.

The workflow can establish execution. The test results establish correctness.

---

## 28. Final verification roadmap

```
                         CURRENT
                            │
                            ▼
                    PARTIALLY VERIFIED
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
          EV-01 EXECUTION          PROVENANCE
          MATERIALIZATION          MAINTAIN
                │
                ▼
          EV-02 RED TESTS
                │
          ┌─────┴─────┐
          ▼           ▼
       PASS         FAIL
          │           │
          │      isolate/repair
          │           │
          └─────┬─────┘
                ▼
             EV-03
             CRYPTO
                │
                ▼
             EV-04
          RFC-0075
                │
                ▼
             EV-05
           CONFLICTS
                │
                ▼
             EV-06
        PHYSICAL MIGRATION
                │
                ▼
       RED-COGNITION IMPLEMENTATION
                │
                ▼
        PRODUCT VALIDATION
```

Priority order remains:

**CI execution → timeout diagnosis → crypto failure → RFC-0075 → conflict reconciliation → physical migration.**

Most important: the next proof should be execution materialization on the current merged `audio` HEAD, not another inventory report.

The repository has reached the point where further static analysis has diminishing value compared with obtaining fresh execution/CI evidence.

---

## 29. Immediate objective (locked)

### **EV-01 → diagnostic CI commit → fresh GitHub Actions execution**

Not:

- another provenance sweep
- another static inventory
- an AF_ALG patch
- mass conflict resolution
- physical file migration
- or a verification-status upgrade

Once the fresh run exists, the next decision should be made **from its actual execution trace**.

The next commit should make the Red execution observable; the next CI run should make the defect reproducible.

We've finished the **reconnaissance phase**.

The next phase is:

**Controlled execution experiment → evidence capture → localized defect → minimal repair.**

No more status upgrades based on static inspection.

No more calling historical CI evidence "current."

No more treating provisioning success as software success.

And no more changing runtime code before the actual failing execution path is identified.

---

## Current disposition

**PARTIALLY VERIFIED — STATIC/PROVENANCE BASELINE STRONG; CONTROLLED TOOLCHAIN EXECUTION ESTABLISHED; CURRENT RED CI EXECUTION INCOMPLETE; ROOT CAUSE OF THE CI RED-PHASE TIMEOUT NOT YET LOCALIZED.**

Do **not** upgrade the repository to “verified.”

The correct state remains:

> **PARTIALLY VERIFIED — integrity/provenance strong; controlled Rebol/Red execution demonstrated; current merged-head CI completion unverified; Red full-suite completion unresolved; AF_ALG remediation unresolved; RFC-0075 unresolved; Red-Cognition product validation not established.**

The next meaningful proof is **a fresh GitHub Actions execution with sufficient telemetry to identify the Red execution boundary**.

**`805e75ce` remains the authoritative repository baseline.**

The repository is healthy enough that the next work should be **controlled execution engineering**, not more speculative restructuring.

And the key principle remains unchanged:

> **A successful setup is evidence that the environment works. It is not evidence that Red works. A completed passing test on the exact commit is evidence that the tested behavior works. CI is the authority for that execution claim.**
