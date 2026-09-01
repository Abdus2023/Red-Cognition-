# Crypto Remediation Decision

## Confirmed failure

The Linux x86 runtime selects the AF_ALG implementation in `runtime/crypto.reds`. On this host, `socket(AF_ALG, SOCK_SEQPACKET, 0)` returns `EAFNOSUPPORT`. The implementation ignores the failure, continues through `bind`, `accept`, `write`, and `read`, and returns an uninitialized 64-byte buffer. This explains the malformed MD5, SHA, and HMAC values.

## Safe remediation boundary

No source patch was applied. Replacing the returned buffer with zeros, changing the digest length, or converting the failure to a generic exception would make the failure more explicit but would not restore cryptographic correctness. A valid remediation requires one of the following independently testable paths:

1. Execute on a Linux host whose kernel exposes AF_ALG and whose required algorithms are available under `/proc/crypto`.
2. Add and validate a supported alternate backend, such as an ABI-compatible OpenSSL implementation, with explicit library-version and symbol checks.
3. Implement or import a self-contained digest backend and verify it against the existing known-answer vectors, including HMAC vectors.
4. Add explicit error propagation to the AF_ALG path as a defensive change, while retaining a validated backend fallback for environments without AF_ALG.

The next implementation change should therefore be made in the repository’s normal development branch, accompanied by a targeted test that forces the backend-unavailable condition and by the existing checksum/HMAC known-answer tests. The current verification workspace remains evidence-only and does not claim that crypto remediation has been completed.

## Static review result

The proposal was checked against the repository without applying any changes. No matching canonical `TO_ERROR(script no-connect)` cleanup pattern was found in the searched Red/System sources, so the proposed error identifier and cleanup control flow remain review items rather than validated syntax. The repository status remains unchanged apart from its pre-existing `docs/implementation/full-pipeline-status.json` modification and untracked `.impl_controller/` directory.
