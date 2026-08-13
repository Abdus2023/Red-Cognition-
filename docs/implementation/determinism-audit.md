# Determinism Audit (Stage-5)

**Date:** 2026-08-12 · **Controller:** 2.0.0 · **Phase:** audit only

Inventory of every potential source of nondeterminism and its classification.
Any UNKNOWN source fails closed (cannot affect contract_id or PASS).

## Nondeterminism inventory

| Source | Where it could leak | Classification | Handling |
|---|---|---|---|
| dict/set iteration | contract_id payload, manifest_identity | FORBIDDEN | `canonical()` = `json.dumps(sort_keys=True)`; all list inputs sorted |
| JSON key order | manifest parse → identity | NONDET-BY-DESIGN (ignored) | canonical sort_keys; `_canonical_task_dict` sorts list fields |
| task/dep/spec/req/tool/command declaration order | manifest_identity, contract_id | FORBIDDEN (non-semantic) | all sorted in identity hashing |
| command ORDER | contract_id | NONSEMANTIC | sorted set of `command_identity`; command CONTENT is semantic |
| filesystem ordering | classify/traceability | FORBIDDEN | iterate `manifest.tasks` (manifest order, deterministic); dep_state sorted |
| PATH lookup | tool availability | SEMANTIC (contract input via classification) | `shutil.which`; absence ⇒ TOOLCHAIN block |
| environment variables | — | DIAGNOSTIC | not an identity input |
| current working directory | runner defaults | NONSEMANTIC | defaults resolve against `--repo-root` |
| timestamps | report/evidence/checkpoint | NONDET-BY-DESIGN | excluded from identity; removed by `normalize` |
| process IDs | — | DIAGNOSTIC | not an input |
| hostnames | — | DIAGNOSTIC | not an input |
| random IDs / UUIDs | evidence_id, repo_identity | OPERATIONAL (per-instance) | excluded from semantic identity; repo_identity stable per working tree |
| temporary paths | state/evidence/lock dirs | OPERATIONAL | not an identity input |
| command stdout/stderr | evidence | DIAGNOSTIC | recorded; not an identity input (exit status is) |
| locale | JSON serialization | FORBIDDEN | canonical uses `ensure_ascii=False`, UTF-8 |
| Python hash randomization | set/dict iteration | FORBIDDEN | no unordered iteration reaches identity (all sorted/canonical) |
| repository HEAD | provenance | SEMANTIC | bound into contract_id |
| tool version (declared) | provenance | SEMANTIC | bound into contract_id via `tool_versions` |
| validator identity | provenance | SEMANTIC (constant) | bound into contract_id; mismatch ⇒ closure gap |

## Classification key

- **AUTHORITATIVE** — manifest, task definition, contract inputs, evidence chain, provenance, repo state.
- **DERIVED** — checkpoint, READY queue, pipeline-status, traceability, contract report.
- **NONDETERMINISTIC-BY-DESIGN** — timestamps, per-instance UUIDs (excluded from identity; removed by normalize).
- **FORBIDDEN-NONDETERMINISM** — any input-order or hash-seed sensitivity in identity/PASS (eliminated by canonicalization).
- **UNKNOWN → fail closed.**

## Finding (genuine defect fixed this phase)

`manifest_identity` previously hashed `task.to_dict()` verbatim, preserving
non-semantic list declaration order — so reordering requirements/specs/tools/
commands changed `manifest_hash` ⇒ changed `contract_id`. **Fixed:** identity
hashing now canonicalizes (sorts) all non-semantic list fields. Command order is
non-semantic (independent checks); command content is semantic.
