# Red-Cognition Agent Prompt Pack

**Purpose:** Give future coding agents a disciplined, reusable set of instructions for continuing development of [Abdus2023/Red-Cognition-](https://github.com/Abdus2023/Red-Cognition-), without losing repository context, verification evidence, or scope control.

These prompts are designed to be copied into a new agent session. Replace bracketed placeholders such as `[TASK]`, `[BRANCH]`, and `[COMMIT]` before use.

## 1. Repository context block

Paste this block at the beginning of every agent task:

```text
You are continuing work on the Red-Cognition repository:
https://github.com/Abdus2023/Red-Cognition-

Repository facts:
- Primary development branch: audio.
- The project combines the Red 0.6.4 language/toolchain source tree with Red-Cognition RFCs, specifications, governance material, and implementation tooling.
- The source bootstrap depends on a Rebol 2.7.8-compatible 32-bit Linux interpreter.
- The repository now contains a containerized test runner at tools/run-container-tests.sh.
- The repository contains a GitHub Actions workflow at .github/workflows/red-container-tests.yml.
- The standard container target is linux/386.
- The Rebol artifact must be provenance-checked by SHA-256 before use.
- Red/System has previously passed 10,560/10,560 assertions in the i386 container.
- The Red suite has previously exposed failures in hash/HMAC/PRF tests and one path-thru test.
- Linux Red crypto uses the AF_ALG kernel interface in runtime/crypto.reds.
- RFC/specification blockers must not be silently “fixed” by changing expected values.

Before changing anything:
1. Clone or fetch the repository and identify the exact branch and commit.
2. Read README.md, docs/IMPLEMENTATION-BASELINE.md, relevant RFCs, and the nearest source/test files.
3. Inspect git status and preserve unrelated user changes.
4. State the conceptual goal, the operational change, and the verification evidence required.
5. Do not claim a test passed unless it actually ran and its output was inspected.
```

## 2. Master continuation prompt

```text
Continue building Red-Cognition for this task:
[TASK]

Work as a rigorous repository maintainer. First reconstruct the current state from the checkout, commit history, README, implementation baseline, related specifications, source files, and existing tests. Do not rely on assumptions from previous agents.

Use this execution loop:
1. Define the intended behavior and acceptance criteria.
2. Identify the smallest coherent implementation boundary.
3. Locate the authoritative source files and existing conventions.
4. Make one reversible change at a time.
5. Add or update focused tests before broad tests where feasible.
6. Run deterministic validation, then the relevant suite.
7. Inspect failures instead of treating exit code alone as proof.
8. Separate code defects, environment defects, specification gaps, and test-harness defects.
9. Review the final diff for accidental files, generated artifacts, secrets, and unrelated edits.
10. Produce a handoff containing changed files, commands, results, known limitations, and the next recommended action.

Do not modify expected test vectors merely to obtain a green build. If behavior is underspecified, record the ambiguity and identify the required design decision.
```

## 3. Orientation and reconnaissance prompt

```text
Perform a technical reconnaissance of the current Red-Cognition checkout for this goal:
[GOAL]

Inspect:
- branch, commit, remote, and working-tree state;
- README and implementation baseline;
- relevant RFC/specification documents;
- source modules and their call graph;
- existing test entry points and output formats;
- CI workflow and container assumptions.

Return:
1. a concise architecture map;
2. the authoritative files for the requested behavior;
3. dependencies and hidden path/runtime assumptions;
4. a risk list;
5. a proposed implementation plan with explicit verification commands.

Do not edit files during reconnaissance unless explicitly asked.
```

## 4. Feature implementation prompt

```text
Implement this feature in Red-Cognition:
[FEATURE]

Requirements:
- Preserve existing Red and Red/System semantics unless the task explicitly changes them.
- Follow the local Red/System coding conventions and error-handling patterns.
- Prefer the smallest implementation that satisfies a documented acceptance criterion.
- Reuse existing abstractions before introducing new ones.
- Keep platform-specific behavior behind the existing target-selection boundaries.
- Add focused regression coverage for the new behavior.
- Do not commit generated binaries, downloaded bootstrap artifacts, transient logs, or local diagnostics unless the task explicitly requests an archive.

Before coding, identify the relevant source, tests, specification, and compatibility constraints. After coding, run syntax/static checks, focused tests, and the narrowest applicable full suite. Report exact commands and outcomes.
```

## 5. Bug diagnosis prompt

```text
Diagnose this failure without guessing:
[FAILURE MESSAGE OR TEST NAME]

Investigate in this order:
1. Reproduce the failure with the smallest possible test.
2. Confirm the exact runtime, architecture, interpreter, compiler, and commit.
3. Trace the failing value or control flow from the test into the implementation.
4. Compare the result with an independent reference where applicable.
5. Determine whether the root cause is code, ABI, OS capability, external service behavior, test expectation, or specification ambiguity.
6. Identify whether the failure affects compiled mode, interpreted mode, Red/System, or only one path.
7. Propose a minimal fix and explain why it preserves valid behavior.

For crypto failures, compare against Python hashlib or another independent standards-based reference. For kernel interfaces, test the underlying syscall or ABI directly before changing high-level code. Do not change expected vectors until the implementation and external reference have been disproven.
```

## 6. Rebol bootstrap and container prompt

```text
Set up or verify the Rebol 2.7.8 bootstrap for Red-Cognition in a reproducible 32-bit Linux container.

Constraints:
- Use linux/386.
- Use an approved Rebol 2.7.8-compatible artifact.
- Verify the artifact checksum before execution.
- Mount the repository at /red and use /red as the working directory.
- Set HOME explicitly to a writable deterministic path.
- Provide /lib/ld-linux.so.2 and the required i386 userspace libraries.
- Include Xvfb and GUI runtime libraries when running the complete suite.
- Do not download and execute an unverified artifact.

Verify:
- `file` reports a 32-bit Intel ELF interpreter.
- Rebol reports the expected version.
- `red.r` can compile the documented hello example.
- The test runner can execute both Red and Red/System entry points.
- Logs, exit codes, summaries, image metadata, and artifact hashes are preserved.

If the host lacks Docker, identify the exact external runtime requirement instead of simulating a successful run.
```

## 7. Test automation and parser prompt

```text
Improve or verify the test automation for Red-Cognition.

The runner must:
- execute tests/run-all.r and system/tests/run-all.r using the repository’s supported Rebol invocation;
- support linux/386 Docker execution;
- capture stdout/stderr separately for each suite;
- record each suite exit code;
- preserve Quick-Test logs before a subsequent suite overwrites them;
- emit summary.json and summary.md;
- fail when a suite exits nonzero;
- fail when logs contain explicit Rebol runtime errors, Quick-Test failure banners, failed assertion counts, or `not ok` results;
- avoid false green results when a runner exits 0 after reporting an access or runtime error;
- upload reports even when the test step fails.

Test the parser against real historical logs containing both passing and failing cases. Validate that a log such as `** Access Error:` is not reported as a passing suite.
```

## 8. Crypto and AF_ALG prompt

```text
Investigate or implement Linux crypto support in runtime/crypto.reds.

First establish:
- which target branch selects AF_ALG;
- the exact C declarations for socket, bind, accept, write, read, and close;
- the sockaddr_alg memory layout and field offsets;
- the kernel’s AF_ALG user-space availability, not merely the algorithm names in /proc/crypto;
- the expected digest and HMAC vectors from an independent implementation;
- behavior in both compiled and interpreted Red paths.

Build a minimal C or equivalent ABI probe using the same family, socket type, address layout, algorithm names, and read/write sequence. Use its result to distinguish kernel capability failure from Red/System ABI or buffer-handling failure.

Any fix must:
- check all syscall and I/O return values;
- avoid returning uninitialized or partially filled digest buffers;
- preserve correct digest vectors;
- provide an explicit error or an authorized fallback backend when AF_ALG is unavailable;
- include focused regression coverage;
- document platform prerequisites.

Do not replace valid vectors with values produced by a broken backend.
```

## 9. Specification and RFC traceability prompt

```text
Analyze this Red-Cognition RFC or requirement set:
[RFC OR REQUIREMENT ID]

Construct a traceability table with:
- requirement identifier;
- normative statement;
- source specification location;
- implementation location;
- test location;
- current status;
- unresolved assumptions;
- owner or decision required.

Separate:
1. conceptual gaps, where the intended behavior is undefined;
2. operational gaps, where the behavior is specified but not implemented;
3. formal/verification gaps, where implementation or evidence cannot yet prove the requirement.

Do not mark a requirement implemented solely because a similarly named file exists. Do not close conflicts by editing derived indexes without resolving the authoritative source.
```

## 10. GitHub Actions CI prompt

```text
Review or extend the Red-Cognition GitHub Actions workflow.

Verify:
- push triggers are present for the intended branches;
- manual dispatch is available when requested;
- workflow permissions are least-privilege;
- i386 emulation and Buildx are initialized correctly;
- Rebol is downloaded with retries and checksum verification;
- the Docker base image is pinned or its mutability is explicitly accepted;
- the Dockerfile receives the required Rebol build input;
- the runner uses the same repository paths and command forms validated locally;
- artifacts are uploaded with `if: always()`;
- test failures cause a failed job rather than a false success;
- workflow timeout and concurrency settings are appropriate;
- generated files are excluded from the Docker context.

If a workflow run is green, inspect its downloaded summary and logs. A green workflow is not sufficient evidence if the parser reported only a smoke subset or ignored runtime error markers.
```

## 11. CI run investigation prompt

```text
Investigate this GitHub Actions run:
[RUN URL OR RUN ID]

Collect:
- workflow commit and branch;
- job and step conclusions;
- runner image and architecture;
- Rebol artifact checksum and version;
- Docker image build result;
- exact test commands;
- suite exit codes;
- summary.json and Quick-Test logs;
- uploaded artifact names and contents.

Classify the outcome as exactly one of:
- CI integration failure;
- bootstrap/toolchain failure;
- container/OS capability failure;
- test-harness or parser failure;
- product/runtime failure;
- specification or expectation failure;
- genuine pass.

A genuine pass requires successful execution of the intended suite, no unparsed error markers, correct failure counts, and consistent evidence in logs and summaries.
```

## 12. Safe commit and push prompt

```text
Prepare the current Red-Cognition changes for commit and push.

Before staging:
- inspect `git status`;
- inspect the complete diff;
- identify generated files, downloaded artifacts, logs, credentials, and unrelated changes;
- preserve user-owned changes;
- confirm the target branch and remote.

Stage only these intentional files:
[FILES]

Run:
- syntax/static validation;
- focused tests;
- `git diff --cached --check`;
- any repository-specific validator.

Use a concise commit message that describes behavior, not the session history. Push without force unless the user explicitly authorizes a force push. If the remote has advanced, fetch and integrate it before retrying. Never discard another contributor’s remote work.

After pushing, verify that local HEAD equals origin/[BRANCH] and provide the commit URL.
```

## 13. Handoff prompt between agents

```text
Create a durable handoff for the next Red-Cognition agent.

Include:
- repository URL, branch, and exact commit;
- task objective and current phase;
- files changed and why;
- commands executed;
- exact test results and logs;
- environment/toolchain details;
- known failures and their classification;
- unresolved design or specification decisions;
- generated artifacts and their locations;
- whether changes were committed and pushed;
- the single highest-priority next action;
- commands the next agent should run first.

Do not write “tests pass” without naming the suite, assertion counts, commit, runtime, and evidence path.
```

## 14. Failure-recovery prompt

```text
Recover safely from this blocked or partially completed Red-Cognition task:
[BLOCKER]

Do not repeat the same failed command more than once without changing the diagnosis or method. Determine whether the blocker is:
- missing dependency;
- unavailable Docker/container capability;
- missing Rebol artifact;
- incorrect architecture or dynamic loader;
- repository divergence;
- failing code;
- invalid test invocation;
- false-positive parser behavior;
- insufficient GitHub permission;
- unresolved specification decision.

Preserve all useful logs. Clean only transient generated files. If a patch was attempted but not independently verified, revert or isolate it before reporting the repository state. End with a concrete next action and the exact prerequisite for completing it.
```

## 15. Compact agent checklist

Use this shorter prompt for routine continuation:

```text
Continue Red-Cognition work on [TASK].

1. Inspect branch, commit, remote, and git status.
2. Read the nearest README, baseline, RFC/spec, source, and tests.
3. State conceptual intent, operational change, and proof obligation.
4. Make the smallest reversible change.
5. Add focused regression coverage.
6. Run syntax/static checks and the relevant suite.
7. Inspect logs for hidden runtime errors and false-green conditions.
8. Separate code, environment, test, and specification failures.
9. Review the diff and exclude generated artifacts.
10. Commit/push only the intended files if authorized.
11. Report exact evidence and the next action.
```

## 16. Recommended agent sequence for the current repository

For the present state of Red-Cognition, future agents should normally use this order:

| Stage | Agent objective | Exit evidence |
|---|---|---|
| 1 | Reconstruct repository and CI state | Exact branch, commit, workflow, and clean intentional diff |
| 2 | Verify Rebol bootstrap and i386 image | Verified artifact hash, Rebol version, image architecture |
| 3 | Verify test runner correctness | Both suite commands run; parser catches runtime errors |
| 4 | Diagnose AF_ALG crypto behavior | Independent digest comparison and ABI probe |
| 5 | Choose backend resolution | AF_ALG host prerequisite or authorized fallback decision |
| 6 | Fix `path-thru` independently | Deterministic test or documented external dependency |
| 7 | Resolve RFC traceability gaps | Requirement-to-code-to-test mapping with owners |
| 8 | Run full CI | CI result matches logs and uploaded summaries |
| 9 | Commit and hand off | Reproducible commit, evidence, and explicit next task |

## 17. Final quality gate

Before an agent declares the task complete, it must answer all of these questions:

| Question | Required answer |
|---|---|
| What exact behavior was intended? | A precise requirement or test statement. |
| What files changed? | Complete list, including generated files excluded from commit. |
| What runtime executed the code? | Rebol version, architecture, image, and commit. |
| Which tests actually ran? | Exact commands and suite names. |
| Did the parser inspect real failure markers? | Yes, with evidence. |
| Were outputs independently checked? | Yes where ABI, crypto, serialization, or external behavior is involved. |
| Are remaining failures classified? | Code, environment, harness, or specification. |
| Is the result reproducible? | Commands, hashes, paths, and artifact locations provided. |
| Was anything pushed? | Remote branch and commit URL, or exact permission blocker. |
| What should the next agent do? | One prioritized next action. |

> **Core rule:** Never convert an unresolved execution, specification, or verification problem into a passing status by weakening the test, changing expected values, hiding errors, or committing opaque generated artifacts.
