# Semantic Determinism & Idempotent Execution Report (Stage-5)

**Date:** 2026-08-12 · **Controller:** 2.0.0 · **Phase:** determinism & idempotency
**Scope:** controller infrastructure only — no Red/Cognition product implementation.

## Final invariants (mechanically enforced)

- **Determinism:** identical authoritative inputs ⇒ identical contract_id ⇒ identical execution decision ⇒ identical normalized result.
- **Idempotency:** VERIFIED PASS ⇒ RETRY ⇒ NO execution ⇒ NO duplicate evidence ⇒ SAME PASS.
- **Invalidation:** any semantic input change ⇒ new contract_id ⇒ old evidence untrusted ⇒ revalidation required.
- **Authority:** derived state can summarize authoritative state; it can NEVER authorize PASS.

## 1–2. Audit & nondeterminism inventory

See `determinism-audit.md`. Every source classified AUTHORITATIVE / DERIVED /
NONDETERMINISTIC-BY-DESIGN / FORBIDDEN-NONDETERMINISM; UNKNOWN fails closed.

## 3. Canonicalization rules

See `determinism-model.md`. All non-semantic list fields sorted in identity
hashing; command ORDER non-semantic (set of independent checks), command CONTENT
semantic. JSON key order and Python hash-seed cannot reach identity.

## 4. Semantic vs diagnostic inputs

Semantic: PATH-resolved tool presence, declared tool version, command content,
HEAD, manifest identity, validator, repository identity, dependency PASS state.
Diagnostic (never affects identity/PASS): PWD, TERM, hostname, PID, timestamps,
env, stdout/stderr, per-instance evidence UUID.

## 5. Contract identity rules

`contract_id = SHA256(canonical(validator, repository_identity, HEAD,
manifest_identity, task_id, sorted(requirements/specs/tools+versions/targets/
prohibited/criteria), sorted(command_identity set), dependency_state))`.

## 6. Idempotency model

`semantic_execution_identity` = contract_id (+ per-command command_identity),
deterministic. `execution_instance_id` = evidence UUID (operational only). A
verified PASS task is never re-executed; a verified command is skipped on retry.

## 7. Partial execution semantics

`cmd1 PASS / cmd2 FAIL` ⇒ NOT PASS; cmd1 evidence durable and not re-run; cmd2
runs on retry; closure is per-command (every command needs verified PASS
evidence bound to the current contract_id).

## 8–9. Retry semantics & adversarial tests

`tests/test_determinism.py` (31 cases): DET-01..30 (reorder = same contract;
semantic change = different; noise excluded; PATH/version/HEAD/manifest/
validator/task/dep/target/criteria invalidation; ×10 dry-run/recovery/contract
determinism; evidence/traceability/status serialization; cwd/process-ordering
independence) + IDEMP (retry verified PASS = no dup; ×10 stable) + partial
execution (cmd1 skip on retry) + SIGKILL-then-retry (no second execution).

## Genuine defect found & fixed

**DEFECT:** `manifest_identity` hashed `task.to_dict()` verbatim, preserving
non-semantic list declaration order ⇒ reordering requirements/specs/tools/
commands changed `manifest_hash` ⇒ changed `contract_id` (DET-03..07 failed).
**Fix:** identity hashing now canonicalizes (sorts) all non-semantic list fields
(`_canonical_task_dict`); commands are a sorted set of `command_identity`.
**Regression:** DET-03..07 (+ all reorder cases). Also bound declared tool
version into contract_id (DET-14) and made closure per-command (fixes a latent
multi-command PASS bug; Phase 5 partial-execution idempotency).

## 10. Property tests

Reorder permutations (JSON keys, deps, requirements, specs, tools, commands) ⇒
identical contract_id; semantic changes ⇒ different. Every input classified
SEMANTIC / NONSEMANTIC / OPERATIONAL / DIAGNOSTIC in the audit.

## 11. Stability runs

Complete self-test: 228/228 PASS. Five consecutive full runs below.

## 12. CI results

CI extended with determinism + idempotency + retry steps (Rebol-independent).

## 13. Real-repository frontier (unchanged)

```
READY=0  BLOCKED=4  PASS=0  FAIL=0  IN_PROGRESS=0  PAUSED=true
RED-LEX-001 [TOOLCHAIN, ARCHITECTURE, PROVISIONING, AUTHORIZATION]
LIBRED-001  [DEPENDENCY, TOOLCHAIN]
HASH-001    [INCOMPLETE_SPECIFICATION, TOOLCHAIN]
RFC0075-001 [SPECIFICATION_CONFLICT, INCOMPLETE_SPECIFICATION]
```

## 14. Scope verification

Only infrastructure files changed (see commit). No Red source/tests, runtime,
RFCs, specifications, RFC-0075, or Rebol/toolchain artifacts modified.

## Files changed

```
tools/impl_controller/provenance.py   (canonical manifest_identity, command_identity,
                                       per-command closure, tool_versions in ctx)
tools/impl_controller/model.py        (Tool.version)
tools/impl_controller/manifest.py     (parse version)
tools/impl_controller/evidence.py     (command_id field, pass_command_ids)
tools/impl_controller/controller.py   (per-command idempotent skip, command_id binding)
tools/impl_controller/tests/test_determinism.py            (new, 31 cases)
tools/impl_controller/tests/test_provenance_attacks.py     (closure ev → command_id)
docs/implementation/determinism-audit.md / -model.md / -report.md
docs/implementation/pipeline-status.json (regenerated)
.github/workflows/implementation-pipeline.yml (determinism CI)
```

## Product scope

No product implementation performed. Red/RFC-0075/specifications/Rebol unchanged.
RFC-0075 remains independently blocked.
