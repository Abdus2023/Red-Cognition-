# Red/Cognition Binary and Bootstrap Verification Report

**Execution date:** 2026-08-31 UTC  
**Repository:** `Abdus2023/Red-Cognition-`  
**Branch:** `arena/01a058d7-red-cognition`  
**Repository HEAD observed:** `35a7e3208a359ee1c4f5241eb7e4074fe68922de`  
**Verification workspace:** `/home/ubuntu/red-cognition-verification`

## Scope and evidence discipline

This report executes the attached verification procedure against the existing acquisition corpus. It distinguishes acquisition, identity, architecture, execution, bootstrap reproduction, and functional behavior. It does not promote any status merely because a source tree, README, CI file, or build script exists.

The repository was already modified before this verification began: `docs/implementation/full-pipeline-status.json` was modified and `.impl_controller/` was untracked. Those pre-existing changes were preserved and not overwritten. The repository’s recorded SHA-256 integrity gate was run before new verification work and returned exit code 0, with all listed files reported `OK`.

## Baseline and network findings

The exact staged official Rebol URL `http://www.rebol.com/downloads/v278/rebol-core-278-4-3.tar.gz` was reachable on 2026-08-31. The response was HTTP 200, with `Content-Length: 222377`, `Content-Type: application/x-gzip`, and a recorded `Last-Modified` date of 2011-01-07. The raw headers and curl output are preserved under `binaries/rebol-278-4-3/`.

The downloaded archive has SHA-256 `b0080df93905f56209875d811c6632c825c385e05d390b220c5d9555a8d38eee` and MD5 `0918513c5e30209c36a88bcf446ddd77`. It contains `releases/rebol-core/rebol` and `about.txt`.

## Rebol binary verification

The extracted executable has SHA-256 `1c902e0f75e994d739975e12963323832ce00f52208b3287cbfe5e7029d856d6`. This is byte-identical to the repository’s prior-session lead hash. The relationship is therefore **IDENTITY_CONFIRMED**. The downloaded copy’s origin is the exact reachable URL above; historical authorship and broader provenance claims remain bounded by the available evidence and are not inferred from the banner alone.

The executable is an ELF32, little-endian, Intel i386, dynamically linked binary using `/lib/ld-linux.so.2`. The required 32-bit loader and libraries were not initially present. After installing the minimal i386 compatibility runtime and required GTK/cURL/udev libraries, `ldd` resolved all dependencies.

A first probe without the 32-bit loader failed with exit code 127. A later probe using the wrong option entered the interactive console and timed out; that event is preserved as a failed/aborted probe, not a success. The controlled final smoke tests succeeded:

| Test | Result |
|---|---|
| `./rebol -V` | **EXECUTED**, banner identified `REBOL/Core 2.7.8.4.3 (6-Jan-2011)` |
| `./rebol --cli smoke-test.r` | **EXECUTED**, printed `3`, exit code 0 |
| General interpreter correctness | **UNRESOLVED**; only minimal smoke coverage was performed |

## Red v0.6.6 bootstrap

The pinned repository artifact `artifacts/red/releases/red-0.6.6.tar.gz` was extracted in isolation. The documented source procedure was used with the acquired Rebol interpreter:

```text
printf 'A\n' | ./rebol --do "do/args %red.r \"%tests/hello.red\""
```

The `A` input approved the toolchain’s explicit request to run the local `git describe --long --tags` command. The build completed with exit code 0 and generated:

| Artifact | Size | SHA-256 | Status |
|---|---:|---|---|
| `hello` | 102,980 bytes | `9e1ebb811908ddafbdcd9a944f656fdc7f9eb865193b7796287a0ec5be1884ec` | **REPRODUCED** for the documented minimal source build |
| `libRedRT.so` | 1,952,672 bytes | `c1cf637c5164cd9be989d5ab240e1d320a0dcc49214fb1948ba677c5c86d159a` | Generated local build product; not an upstream artifact |

The build log reports successful compilation of `libRedRT`, native code generation, linking, and output-file creation. This establishes **BOOTSTRAP EXECUTED** and **REPRODUCED** for the minimal `tests/hello.red` procedure from the pinned v0.6.6 source using the acquired Rebol interpreter.

This does not establish reproduction of every Red target, the full Red console, or a clean-room independent reproduction. The licensed Rebol SDK was not used for this minimal hello build; the repository’s documentation still identifies the SDK as a requirement for rebuilding the Red binary itself.

## Generated Red binary execution

The generated `hello` executable is an ELF32, little-endian, Intel i386 executable using `/lib/ld-linux.so.2`. All dynamic dependencies resolved after installing the i386 runtime libraries.

Running `./hello` produced the expected multilingual output:

```text
Hello, world!
Χαῖρε, κόσμε!
你好, 世界
Dobrý den světe
```

However, the process exited with code **255**. A process trace showed the generated program invoked `exit_group(-1)`. To distinguish an implementation/runtime failure from source termination semantics, a second minimal source was compiled with an explicit `quit-return 0`. That binary compiled with exit code 0, printed `Hello, explicit zero`, and exited with code 0. The evidence therefore explains the original 255 as the implicit termination result of the original source, not as a dynamic-loader failure. The original binary remains **EXECUTED**; its output behavior is observed, while the explicit-zero comparison provides a clean follow-up smoke pass. This does not by itself establish broad Red runtime correctness.

## Broader compiler smoke test

A second non-GUI source, `tests/source/compiler/print-test.red`, was compiled using the already-built `libRedRT.so`. Compilation completed with exit code 0 and produced the ELF32 executable `print-test` with SHA-256 `acaa86f3ecab08c9f333c2f1c2460b545be26a9c38ede50af6bdddc4736ddce4`. Executing it printed `1` and exited with code 255. Together with the explicit `quit-return 0` control, this shows that the compiler can generate and run multiple simple console programs, while the default implicit termination status remains a compatibility/semantics detail to document rather than treating it as a compilation failure.

## Broader batch test-harness attempt

The documented `tests/run-all.r --batch` harness was first attempted with the root-relative Rebol path and failed because child invocations resolved `./rebol` from other working directories. It was then retried with the absolute path to the same acquired interpreter. The retry ran far enough to provide meaningful partial evidence:

| Harness group | Observed result |
|---|---|
| Lexer tests | 34 / 34 |
| Lexer auto tests | 18 / 18 |
| Unicode tests | 67 / 67 |
| Preprocessor tests | 43 / 43 |
| `run-all-comp1.red` | 8,993 / 8,993 |
| `run-all-comp2.red` | 6,245 / 6,297; 52 failures reported: 51 crypto-vector assertions and one network-dependent `path-thru` assertion |
| `run-all-interp.red` | Timed out after 300 seconds after reaching `#5099`; next test is a documented ~100-million-iteration benchmark loop |

The harness therefore demonstrates substantial successful compiler/test execution, but it is not a clean suite pass. A direct rerun of `run-all-comp2` identified all 52 failures: the MD5, SHA-1, SHA-256, SHA-384, SHA-512, and HMAC vector groups, plus one `path-thru` test. A focused checksum trace showed the concrete cause for the digest failures: each AF_ALG call returned `EAFNOSUPPORT` (`Address family not supported by protocol`), followed by `EBADF` on bind, accept, write, and read. The runtime did not propagate those errors and instead returned an uninitialized digest buffer. This is an environment/runtime error path, not evidence that the expected cryptographic vectors are wrong. The interpreter group separately timed out after 300 seconds. A direct bounded rerun reached the `#5099` test, printed its expected `10` and `20`, and then stopped producing progress. The next source test is `#5114`, which contains a nested `loop 100000 [dt [loop 1000 []] ...]` workload—approximately 100 million inner-loop iterations—so the observed timeout is consistent with an unexpectedly long benchmark-style test rather than proof of a deadlock. The interpreter group remains **INCOMPLETE**, and the timeout needs a longer run or a separately bounded test selection before it can be classified as passed or failed. The remaining `path-thru` assertion uses `http://red-lang.com`; an independent curl probe failed at DNS resolution with exit code 6 (`Could not resolve host: red-lang.com`). That assertion is therefore classified as an unavailable external network fixture in this environment, not as a demonstrated path implementation defect. No full-corpus pass claim is made.

## Test corpus

The source corpus contains 172 files under `tests/`, 8 files under `quick-test/`, and 97 Red/System test files under `system/tests/`, as recorded by the acquisition evidence. The complete corpus was not executed in this verification run. No corpus-level pass or product-validation claim is made.

## Strict status reconciliation

| Evidence dimension | Status | Basis |
|---|---|---|
| Existing acquisition integrity | **VERIFIED** | Repository SHA-256 manifest check returned exit code 0. |
| Official Rebol archive download | **ACQUIRED** | Exact staged URL returned HTTP 200; archive preserved and hashed. |
| Prior-session Rebol lead identity | **IDENTITY_CONFIRMED** | Extracted official-download executable hash exactly matched prior lead hash. |
| Rebol architecture | **VERIFIED** | ELF and i386 headers inspected; dependencies resolved after runtime setup. |
| Rebol safe execution | **EXECUTED** | Version/banner and arithmetic script produced captured output; arithmetic exited 0. |
| Rebol general correctness | **UNRESOLVED** | Minimal smoke tests only. |
| Red v0.6.6 minimal bootstrap | **REPRODUCED** | Pinned source plus acquired Rebol generated `hello` and runtime artifacts, build exit 0. |
| Generated Red binary invocation | **EXECUTED** | `hello` ran and printed expected multilingual output. |
| Generated Red smoke-test pass | **PASS for output; explicit termination required** | Two simple console programs compiled and printed correctly; both implicit-termination programs exited 255, while a controlled `quit-return 0` variant exited 0. |
| Full Red test corpus | **ATTEMPTED_FAILED / INCOMPLETE** | Batch harness reached multiple groups; 51 crypto assertions hit unsupported AF_ALG/error handling, one path-thru fixture could not resolve DNS, and interpreter tests timed out. |
| Independent clean-environment reproduction | **NOT_ATTEMPTED** | This was one isolated verification workspace, not a second clean environment. |
| Official Red binary identity | **UNRESOLVED** | No official Red binary was downloaded and compared. |

## Evidence files

Raw evidence is preserved in the following files:

- `baseline/latest.txt`
- `baseline/sha256-check.log`
- `network/latest.log`
- `binaries/rebol-278-4-3/acquisition-*.log`
- `binaries/rebol-278-4-3/architecture-inspection.log`
- `binaries/rebol-278-4-3/smoke-execution-*.log`
- `bootstrap/red-0.6.6/bootstrap-source-inspection.log`
- `bootstrap/red-0.6.6/bootstrap-attempt-*.log`
- `bootstrap/red-0.6.6/red-product-execution-*.log`
- `bootstrap/red-0.6.6/red-product-execution-final.log`

## Remaining blockers

The original generated `hello` executable’s exit code 255 is explained by its implicit termination behavior: the traced process called `exit_group(-1)`, while an otherwise equivalent explicit-zero program exited 0. The full Red toolchain and test corpus remain unverified: the bounded batch harness was incomplete and non-green. The crypto failure is now localized to a concrete runtime implementation defect under an unavailable host capability, rather than left as an unexplained test mismatch. The crypto failures are specifically attributable to the source block in `runtime/crypto.reds` (lines 640–679): it unconditionally calls `socket(AF_ALG, ...)`, ignores return values from `socket`, `bind`, `accept`, `write`, and `read`, and returns the allocated digest buffer even when the calls fail. On this host, `socket(AF_ALG, ...)` returns `EAFNOSUPPORT`, so the returned digest is invalid. No speculative source patch was applied to the repository or verification copy because a real remediation requires either a supported AF_ALG host/kernel or a validated alternate crypto backend and ABI; merely zeroing the buffer or converting the failure to an exception would not make the checksum tests pass. The single path-thru failure depends on `red-lang.com`, which was unresolvable by DNS in this environment. The interpreter timeout is now localized to the transition after `#5099`, immediately before the large `#5114` benchmark loop, but it is not yet completed or fully timed. No independent clean-environment reproduction has been completed. The broader compiler smoke test increases confidence in simple console compilation only; it is not a substitute for corpus-level validation. The repository’s own governance invariant remains applicable: governance test success must not be treated as product validation.
