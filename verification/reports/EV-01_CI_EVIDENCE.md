# EV-01 CI evidence — current-head execution

## EV-01c instrumentation (awaiting CI)

`tests/run-all.r` accepts `--group pre|comp1|comp2|interp|post|regression` (default: all groups, historical order). `tools/run-container-tests.sh --phase all` now runs those groups **sequentially** after identity + hello:

1. `red-pre` — lexer / unicode / preprocessor extras
2. `red-comp1` — `run-all-comp1.red`
3. `red-comp2` — `run-all-comp2.red`
4. `red-interp` — `run-all-interp.red`
5. `red-post` — post extras
6. `red-regression` — compiler regression scripts
7. `red-system` — only if every Red group **completed** (not skipped)

A hang does **not** become a skip or PASS: the running group stays `STARTED`/`TIMED_OUT`; later groups are recorded `NOT_RUN`; overall stays `INCOMPLETE`. Job `timeout-minutes: 20` is unchanged. No AF_ALG / Red semantic patch.

Checks annotations (budget ~10): identity COMPLETE, hello COMPLETE, **group START only**. Last START names the group that consumed the remaining budget.

This section is **not** a result. Fill the table from the next `push` run.

| Group | Expected annotation | Result |
| --- | --- | --- |
| rebol-identity | COMPLETE | *(pending)* |
| red-hello | COMPLETE (~226s) | *(pending)* |
| red-pre | START, then COMPLETE or last START | *(pending)* |
| red-comp1 | START only if pre completed | *(pending)* |
| red-comp2 | START only if comp1 completed | *(pending)* |
| red-interp | START only if comp2 completed | *(pending)* |
| red-post / regression / red-system | NOT_RUN unless earlier groups finished | *(pending)* |

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

**EV-01 diagnostic pass condition (observability of current-head Red launch) is met at the job-step level.**

**EV-01 log-localization is not met** until the streamed heartbeat / `quick-test.log` / execution JSON can be read.

Timeout is still 20 minutes. Do not raise it yet.

## Next diagnostic (not a Red semantic patch)

Insert a `red.r tests/hello.red` compiler smoke **before** `tests/run-all.r`.

- If hello hangs: the stall is compiler/bootstrap, not the full suite.
- If hello completes and `run-all.r` then occupies the remaining budget: the stall is in the suite.
