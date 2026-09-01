# EV-01 CI evidence — current-head execution

## EV-01e instrumentation (awaiting CI)

`comp1a` (odd files 1–9) is four sequential compile units. Historical `run-all-comp1-a.red` is unchanged. CI `--phase all` runs `comp1a1`→`comp1a4` instead of the monolith.

| Partition | Files |
| --- | --- |
| `comp1a1` | preprocessor, conditional, path |
| `comp1a2` | url, function, type |
| `comp1a3` | select, evaluation |
| `comp1a4` | lexer |

Semantics: COMPLETE / FAILED / INCOMPLETE / NOT_RUN. No skip/PASS for unexecuted groups. Job timeout remains 20m. Duration on every `comp1aN` COMPLETE/FAILED. Slow ≠ hung.

This section is **not** a result. Fill from the next `push` run.

---

## EV-01d `comp1` partitions (commit `4d49b39`, run `33544163622`)

GitHub Check annotations for job `99977452017` (https://github.com/Abdus2023/Red-Cognition-/actions/runs/33544163622):

| Partition | State | Duration | Command |
| --- | --- | ---: | --- |
| Rebol identity | **COMPLETED exit=0** | 3s | `/opt/rebol/rebol -qws /artifacts/rebol-identity.r` |
| red-hello | **COMPLETED exit=0** | **339s** | `red.r tests/hello.red` |
| red-pre | **FAILED exit=1** | **371s** | `tests/run-all.r --batch --group pre` |
| **red-comp1a** | **START only (INCOMPLETE)** | until cancel (~199s) | `--group comp1a` |
| red-comp1b | no START | — | **NOT_RUN** |
| red-comp1c | no START | — | **NOT_RUN** |
| red-comp1d | no START | — | **NOT_RUN** |
| comp2 / interp / post / regression / red-system | no START | — | **NOT_RUN** |

Job `18:31:53Z`–`18:52:14Z` **cancelled** at 20m. Image build `18:32:14Z`–`18:36:56Z` PASS (~4m42s). Test step `18:36:56Z`–`18:52:08Z` cancelled (~15m12s). Artifact `red-container-test-results-33544163622` (12132 bytes).

Prefix cost inside the test step: identity 3s + hello 339s + pre 371s ≈ 713s. **`comp1a` occupied the leftover ~199s** until the deadline.

`comp1a` compile unit (odd indices 1–9 of `all-tests.txt`): preprocessor, conditional, path, url, function, type, select, evaluation, lexer.

### Discriminating conclusion

- `pre` again **completed** (FAIL 371s). Independent of the stall.
- `hello.red` **339s** — this host is slow; duration alone is not a hang.
- The first `comp1` partition that started and **did not terminate** is **`comp1a`**.
- `comp1b`–`comp1d` were **NOT_RUN**. Overall **INCOMPLETE**, not skip/PASS.
- AF_ALG still not implicated.

EV-01d: remaining budget is consumed inside **`tests/run-all.r --group comp1a`**. Next cut is inside that 9-file unit only.

---

## EV-01c group localization (commit `8b05636`, run `33532229557`)

GitHub Check annotations for job `99938034432` (https://github.com/Abdus2023/Red-Cognition-/actions/runs/33532229557):

| Phase | Result | Elapsed | Command |
| --- | --- | ---: | --- |
| Rebol identity | **COMPLETED exit=0** | 3s | `/opt/rebol/rebol -qws /artifacts/rebol-identity.r` |
| red-hello | **COMPLETED exit=0** | **288s** | `/opt/rebol/rebol -qws red.r tests/hello.red` |
| red-pre | START, then **FAILED exit=1** | **320s** | `tests/run-all.r --batch --group pre` |
| red-comp1 | **START only** (no COMPLETE) | until job cancel | `tests/run-all.r --batch --group comp1` |
| red-comp2 / interp / post / regression / red-system | no START | — | **NOT_RUN** (comp1 did not finish) |

Job `16:31:16Z`–`16:51:35Z` **cancelled** at 20m. Image build `16:31:32Z`–`16:35:35Z` PASS (~4m3s). Test step `16:35:35Z`–`16:51:30Z` cancelled (~15m55s). Artifact `red-container-test-results-33532229557` (10875 bytes).

Approximate remaining-budget split inside the test step: identity 3s + hello 288s + pre 320s ≈ 611s; **comp1 occupied the leftover ~344s** until the job deadline.

### Discriminating conclusion

- Identity and `hello.red` still complete (hello ~4m48s this host; slow, not hung).
- **`pre` is not the stall.** It finished in 320s with **exit 1** (test failures, not a hang). Failures in `pre` are **not** treated as the CI timeout cause and are **not** a license to patch Red semantics.
- The group that was still running when the 20-minute job died is **`comp1`** (`run-all-comp1.red`).
- `comp2`, `interp`, `post`, `regression`, and Red/System were **not reached**.
- Timeout is **INCOMPLETE**, not skip/PASS. AF_ALG is still **not** implicated by this trace.

This is EV-01c: remaining budget is consumed inside **`tests/run-all.r --group comp1`**. Next hierarchical step (not done here) would be a subgroup of `run-all-comp1.red`, not hundreds of per-test jobs, and not a timeout increase.

---

## EV-01b localization (commit `43f5fa7`, run `33528808889`)

GitHub Check annotations (readable without blob logs) for job `99926653096`:

| Phase | Result | Elapsed | Command |
| --- | --- | ---: | --- |
| Rebol identity | **COMPLETED exit=0** | 2s | `/opt/rebol/rebol -qws /artifacts/rebol-identity.r` |
| red-hello | **COMPLETED exit=0** | **226s** | `/opt/rebol/rebol -qws red.r tests/hello.red` |
| red | **START only** (no COMPLETE) | until job cancel | `/opt/rebol/rebol -qws tests/run-all.r --batch` |

Job `15:57:11Z`–`16:17:32Z` **cancelled** at 20m. Image `sha256:d499f39b0d9e1552e2ffed78c49704e1b4f78ffb32c26a01f87e98841c6bf5ee`. Test step `16:01:34Z`–`16:17:26Z` (~15m52s). Artifact published.

### Discriminating conclusion

- The 32-bit Rebol identity smoke **works**.
- The Red compiler **can compile and run** `tests/hello.red` in ~3m46s on this CI host.
- The 15-minute stall is **not** hello/bootstrap. It begins **after** hello, inside **`tests/run-all.r --batch`**.
- AF_ALG is **not** implicated by this trace (hello does not exercise crypto; run-all never completed).
- Red/System was **not reached**.

This is EV-01b: execution localized to the Red test suite, not the compiler smoke.

Do **not** patch Red source yet. Next diagnostic is suite partitioning (`run-all-comp1` / `comp2` / `interp`) with the same annotation pattern.

---



Observed 2026-09-01 via GitHub API. Azure blob log/artifact download from this environment fails with SSL EOF, so this file records **API-visible** facts only. It does not invent Red test results.

## Authoritative current-head run

| Field | Value |
| --- | --- |
| Commit | `57c939a6d6fdcaa43501c8eb7105ef17abaa2d9e` |
| Branch | `arena/01a05d50-red-cognition` |
| PR | https://github.com/Abdus2023/Red-Cognition-/pull/10 |
| Workflow | Red container tests |
| Run | `33521582438` |
| Job | `99901911946` |
| URL | https://github.com/Abdus2023/Red-Cognition-/actions/runs/33521582438 |
| Job started | `2026-09-01T14:46:46Z` |
| Job completed | `2026-09-01T15:07:04Z` |
| Job conclusion | **cancelled** |
| Annotation | `The job has exceeded the maximum execution time of 20m0s` |
| Artifact | `red-container-test-results-33521582438` (3400 bytes compressed) |

## Step timeline

| Step | Started | Completed | Result |
| --- | --- | --- | --- |
| Set up job | 14:46:46Z | 14:46:48Z | success |
| Check out repository | 14:46:48Z | 14:46:50Z | success |
| Enable i386 emulation | 14:46:50Z | 14:47:00Z | success |
| Set up Docker Buildx | 14:47:00Z | 14:47:03Z | success |
| Download and verify Rebol 2.7.8 bootstrap | 14:47:03Z | 14:47:04Z | success |
| Build 32-bit Rebol test image | 14:47:04Z | 14:51:18Z | success (~4m14s) |
| Run Red and Red/System container tests | 14:51:18Z | 15:07:00Z | **cancelled (~15m42s)** |
| Publish test reports | 15:07:00Z | 15:07:01Z | success |

## What this run proves

1. **Current merged-work HEAD was executed.** This is not the historical `cd00ea4` / `805e75ce` CI.
2. Rebol bootstrap download + SHA-256 verification **PASS**.
3. linux/386 image build **PASS**.
4. The instrumented runner **started** and remained in the test step for **15 minutes 42 seconds**.
5. GitHub cancelled the job at the **unchanged 20-minute** deadline.
6. Artifact upload still ran (`if: always()`).

## What this run does not prove

- Red suite PASS
- Red suite FAIL
- which Red test was running
- AF_ALG / crypto result
- Red/System was reached (it is sequential after Red)

The 3400-byte artifact is larger than the historical 804-byte timeout artifact, which is consistent with wrapper telemetry files being written. Blob download from this sandbox could not read the files.

## Follow-up run with in-process hello smoke (`dcc2974`)

| Field | Value |
| --- | --- |
| Commit | `dcc29746d90414995cb8b9022911243412a5b281` |
| Run | `33524579407` |
| Job | `99912027493` |
| URL | https://github.com/Abdus2023/Red-Cognition-/actions/runs/33524579407 |
| Job | 15:15:09Z–15:35:30Z **cancelled** (20m) |
| Image build | 15:15:31Z–15:19:52Z PASS (~4m21s) |
| Bundled test step | 15:19:52Z–15:35:24Z **cancelled (~15m32s)** |
| Artifact publish | success |

Hello was still inside the same GitHub step as `tests/run-all.r`, so this run cannot tell compiler-smoke hang from suite hang.

The runner now accepts `--phase identity|hello|red|red-system|all`. Updating `.github/workflows/red-container-tests.yml` was **rejected** from this session (`workflows` permission). The existing workflow still runs `--phase all` as one 20-minute step.

Runner-side localization (no workflow YAML): `run-container-tests.sh` now emits GitHub `::notice`/`::error` annotations per phase and bounds `hello` at 480s. If hello times out, the script exits 124 and **does not start** `tests/run-all.r`. Those annotations are readable via the Checks API without Azure blob logs.

- Job **fails ~12m** with hello TIMED_OUT annotation → stall is compiler/bootstrap
- Job **cancels at 20m** with hello COMPLETED annotation → stall is `tests/run-all.r`

Maintainer action still useful: apply the step split below from a GitHub identity that can write workflow files. Job `timeout-minutes: 20` stays unchanged.

```yaml
      - name: Rebol identity smoke
        id: identity
        timeout-minutes: 3
        continue-on-error: true
        run: |
          mkdir -p "$GITHUB_WORKSPACE/artifacts/test-run"
          tools/run-container-tests.sh --image red-cognition/rebol-bootstrap:2.7.8 \
            --out "$GITHUB_WORKSPACE/artifacts/test-run" --heartbeat-seconds 15 --phase identity

      - name: Red hello compiler smoke
        id: hello
        timeout-minutes: 8
        if: always()
        run: |
          tools/run-container-tests.sh --image red-cognition/rebol-bootstrap:2.7.8 \
            --out "$GITHUB_WORKSPACE/artifacts/test-run" --heartbeat-seconds 30 --phase hello

      - name: Red tests/run-all.r
        id: red
        timeout-minutes: 10
        if: steps.hello.outcome == 'success' || steps.hello.outcome == 'failure'
        run: |
          tools/run-container-tests.sh --image red-cognition/rebol-bootstrap:2.7.8 \
            --out "$GITHUB_WORKSPACE/artifacts/test-run" --heartbeat-seconds 30 --phase red

      - name: Red/System tests/run-all.r
        timeout-minutes: 8
        if: steps.red.outcome == 'success' || steps.red.outcome == 'failure'
        run: |
          tools/run-container-tests.sh --image red-cognition/rebol-bootstrap:2.7.8 \
            --out "$GITHUB_WORKSPACE/artifacts/test-run" --heartbeat-seconds 30 --phase red-system
```

Interpretation after that YAML is applied:

- `hello` **cancelled** at 8m → stall is compiler/bootstrap
- `hello` completed and `red` **cancelled** → stall is `tests/run-all.r`

## Earlier runs on this PR (not Red-phase evidence)

| Commit | Run | Test-step duration | Exit | Classification |
| --- | --- | --- | --- | --- |
| `ecfaedee` | `33519143570` | ~1s | 1 | wrapper `NameError` (`null` in Python) |
| `2f9cc07` | `33520059725` | ~1s | 1 | same wrapper defect still present |
| `c9214f9` | `33520852415` | ~7s | 2 | identity smoke was a hard gate |
| `57c939a` | `33521582438` | **15m42s** | cancelled | Red phase launched; job timeout |

Windows workflow on these commits still fails at `Set up job`. That remains CI infrastructure failure, not a Red verdict.

## EV-01 status

**EV-01a** (current-head launch) **PASS**. **EV-01b** (stall after hello inside `run-all.r`) **PASS**. **EV-01c** (which `run-all` group) **PASS → `comp1`**. **EV-01d** (internal `comp1`) **PASS → `comp1a`**.

Timeout is still 20 minutes. Do not raise it yet. Do not patch AF_ALG or Red expected results from `pre` exit 1.

## Next diagnostic (not a Red semantic patch)

EV-01e: hierarchical cut **inside `comp1a` only** (preprocessor … lexer). Do not split hundreds of tests. Do not treat timeout as skip/PASS. Do not raise the 20-minute job timeout.
