# Determinism Model (Stage-5)

**Date:** 2026-08-12 · **Controller:** 2.0.0

## Identity

```
D = canonical(authoritative_inputs)
contract_id = SHA256(D)
```

Two executions are semantically equivalent iff these are identical:

```
canonical(requirements)      canonical(specifications)     canonical(task)
canonical(dependencies)      canonical(tools + versions)   canonical(commands)
canonical(criteria)          canonical(targets)            canonical(prohibited)
repository_identity          HEAD                          manifest_identity
validator_identity           dependency_state (sorted PASS deps)
```

Timestamps and process-local metadata MUST NOT affect contract identity.

## Canonicalization rules (non-semantic → sorted)

requirements, specifications, tools(+declared version), allowed_tools,
implementation_targets, prohibited_scope, criteria, dependency_refs,
declared_blockers, evidence_refs, spec_conflicts, spec_gaps — all sorted.
**validation_commands** are treated as an unordered SET of independent checks
(sorted by `command_identity`); their CONTENT (id/command/expected_exit) is
semantic, their ORDER is not. No field is sorted "blindly" — only fields whose
order does not affect the PASS predicate (all checks must pass; order is
irrelevant) are canonicalized.

## Semantic vs diagnostic inputs

| SEMANTIC (changes ⇒ new contract ⇒ old evidence untrusted) | DIAGNOSTIC (never affects identity/PASS) |
|---|---|
| PATH-resolved tool presence; declared tool version; command content; HEAD; manifest identity; validator; repository identity; dependency PASS state; requirement/spec/target/criteria content | PWD (repo-relative targets); TERM/colors; hostname; PID; timestamps; env vars; stdout/stderr text; per-instance evidence UUID |

## normalize(result)

Removes ONLY explicitly nondeterministic metadata:
`generated_at`, `timestamp`, `last_checkpoint`, `updated_at`, `started_at`,
evidence `evidence_id` (UUID), and `repo_head` for non-git working trees.
Compared (deterministic): `graph`, `classifications` (state/blocker_class/
reasons), `provenance_context` (repo_identity, head, manifest_hash,
validator), `frontier`, `traceability` (incl. contract_id, closure).

## Idempotency model

- `semantic_execution_identity` = `contract_id` (+ per-command `command_identity`).
  Deterministic over authoritative inputs.
- `execution_instance_id` = the evidence `evidence_id` (UUID). Operational only;
  never participates in semantic identity.
- VERIFIED PASS + RETRY ⇒ no execution, no new evidence, same PASS.
- Per-command: a command with verified PASS evidence for the current contract is
  never re-executed; only unverified commands run on retry.

## Partial execution

`cmd1 PASS / cmd2 FAIL` ⇒ task NOT PASS; cmd1 evidence durable and not re-run;
cmd2 may run on retry. PASS requires EVERY command to have verified PASS
evidence bound to the current contract_id (closure is per-command).
