# Provenance & Traceability-Closure Hardening Report

**Date:** 2026-08-12 · **Controller version:** 2.0.0 · **Phase:** Stage-5 provenance closure
**Scope:** controller infrastructure only — no Red/Cognition product implementation.

## Central invariant (now mechanically true)

> NO IMPLEMENTATION RESULT IS TRUSTED UNLESS ITS REQUIREMENT, SPECIFICATION,
> TASK, CONTRACT, EXECUTION, VALIDATION, EVIDENCE, REPOSITORY STATE, AND
> TRACEABILITY CHAIN ALL AGREE.

A successful command alone is **never** sufficient for PASS.

## 1. Attack matrix

| # | Attack | Expected | Actual | Result |
|---|---|---|---|---|
| A1 | requirement missing | BLOCKED | BLOCKED/INSUFFICIENT | ✅ |
| A2 | requirement w/o authority | closure open | gaps | ✅ |
| B5-10 | spec removed/outside/dir | BLOCKED | BLOCKED/INSUFFICIENT | ✅ |
| C11-14 | contract reused across tasks | not PASS | contract_id task-specific; binding mismatch | ✅ |
| D15-20 | evidence contract mismatch / foreign task | untrusted | closure gaps; ignored | ✅ |
| E21-25 | manifest/command change after contract | contract_id changes | cid differs | ✅ |
| F26-28 | evidence from other repo/head | not PASS | repo_identity/HEAD in cid → differs | ✅ |
| G31-35 | PASS w/ mismatched exit / validator | untrusted | validated_pass ∅ / closure gap | ✅ |
| H36-45 | closure: missing edge | open | closure_gaps non-empty | ✅ |
| R1 | replay evidence → mutated manifest | not PASS | PASS invalidated | ✅ |
| R2 | replay evidence → advanced HEAD | not PASS | PASS invalidated | ✅ |
| M | per-component mutation (manifest/spec/cmd) | invalidates PASS | each invalidates | ✅ |

(45 numbered attacks collapse to the distinct properties above; all pass via
`tests/test_provenance_attacks.py`, 23 cases.)

## 2–6. Discovered defects / root causes / fixes / regressions

The **root defect** this phase closed: PASS previously rested on (chain-PASS
evidence) ∧ (def intact) ∧ (authority) ∧ (deps) — it did **not** bind evidence
to *which contract/repo/commit/manifest* it validated. A successful command's
evidence could be replayed across tasks/repos/commits/manifests.

**Fix (minimal):** a single deterministic `contract_id` cryptographically
binding the immutable execution inputs, recorded in evidence and re-verified at
reclassification, plus a traceability-closure check.

| Defect | Reproducer | Root cause | Fix | Regression test |
|---|---|---|---|---|
| PA-CONTRACT | reuse one task's evidence for another | no contract identity | `contract_identity_for` (SHA-256 over repo+HEAD+manifest+task+deps+tools+commands+targets); evidence binds `contract_id` | `C_TaskContract`, `D_Evidence` |
| PA-REPO | replay evidence across repos | no repo/HEAD binding | `repo_identity` (per-working-tree UUID) + `head` folded into contract_id | `F_RepositoryProvenance`, `ReplayResistance` |
| PA-MANIFEST | contract from manifest A accepted under B | no manifest identity | `manifest_identity` (SHA-256 over execution-relevant manifest) folded into contract_id | `E_ContractIntegrity`, replay-mutated-manifest |
| PA-CLOSURE | PASS without full chain | no closure check | `closure_gaps` (req→spec→task→contract→evidence); required for PASS | `H_Closure`, `SyntheticMutation` |

No existing safety rule was weakened.

## 7. Contract identity model

`contract_id = SHA256(canonical(validator, repository_identity, HEAD,
manifest_identity, task_id, requirements, specifications, dependency_state,
tools, allowed_tools, commands[+expected_exit], criteria, targets,
prohibited))`. Deterministic over immutable inputs. Evidence stores it; PASS
requires the evidence's `contract_id` to equal the task's CURRENT `contract_id`.

## 8. Evidence identity model

Each `EvidenceRecord` binds: `evidence_id, task_id, contract_id,
repository_identity, head, manifest_hash, validator, command, expected_exit,
exit_status, result`, chained via `prev_hash`/`record_hash` (SHA-256). A PASS is
trusted only if the chain is intact to it AND it is structurally valid
(`exit_status == expected_exit`, non-empty command) AND its `contract_id`
matches the current contract.

## 9. Repository identity model

`repository_identity` = stable per-working-tree UUID stored at
`<repo>/.impl_controller/repo.identity` (no network; two checkouts differ).
`head` = current git HEAD commit. Both fold into `contract_id`, so evidence
generated under one repo/commit cannot satisfy another.

## 10. Traceability closure rules

`closure_gaps(task, contract_id, evidence, ctx)` returns empty (CLOSED) only
when every edge resolves: requirement → specification → task →
contract(execution) → validation → evidence(a chain-PASS record bound to the
current `contract_id` and `task_id`, validator identity correct). Any missing
edge ⇒ OPEN ⇒ task cannot remain PASS.

## 11. Replay-resistance results

- valid evidence (task A) → replayed into task B: **fail closed** (contract_id/task binding mismatch).
- valid evidence (commit A) → replayed into commit B: **fail closed** (HEAD in contract_id).
- contract (manifest A) → executed under manifest B: **fail closed** (manifest_hash in contract_id).

All proven by `ReplayResistance` + `E_ContractIntegrity` + `F_RepositoryProvenance`.

## 12. Deterministic-run results

3 identical synthetic runs produced identical `manifest_identity`,
`contract_id`, normalized graph/classification/traceability/provenance_context
(timestamps permitted to differ). (`Determinism.test_three_runs_identical`.)

## 13. CI results

CI runs the full self-test (now 137 cases incl. provenance), real-repo dry-run,
traceability-closure + provenance-context assertions, determinism check,
repository-index PASS, RFC-0075 FAIL. No Rebol required.

## 14. Real-repository frontier

```
READY = 0   BLOCKED = 4   PASS = 0   FAIL = 0   IN_PROGRESS = 0   PAUSED = true
provenance_context = {repo_identity: repo-07aa…, head: 44de279…,
                      manifest_hash: aad90c…, validator: impl_controller}
RED-LEX-001  BLOCKED [TOOLCHAIN, ARCHITECTURE, PROVISIONING, AUTHORIZATION]
LIBRED-001   BLOCKED [DEPENDENCY, TOOLCHAIN]
HASH-001     BLOCKED [INCOMPLETE_SPECIFICATION, TOOLCHAIN]
RFC0075-001  BLOCKED [SPECIFICATION_CONFLICT, INCOMPLETE_SPECIFICATION]
traceability: 4 tasks, all carry contract_id, all closure=OPEN (no evidence edge)
evidence integrity = true   blockers byte-for-byte semantically unchanged
```

## 15. Files changed

```
tools/impl_controller/provenance.py             (new) identity + closure model
tools/impl_controller/evidence.py               (provenance fields on EvidenceRecord)
tools/impl_controller/contract.py               (immutable contract_id)
tools/impl_controller/controller.py             (provenance ctx, binding, closure-gated PASS)
tools/impl_controller/__init__.py               (exports, v2.0.0)
tools/impl_controller/tests/test_provenance_attacks.py  (new, 23 cases)
docs/implementation/provenance-hardening-report.md      (this report)
docs/implementation/pipeline-status.json        (regenerated, v2.0.0)
.github/workflows/implementation-pipeline.yml   (provenance/closure/determinism checks)
```

## 16. Product scope

**No product implementation was performed.** Red implementation, Red tests,
runtime, RFC-0075, all RFCs/specifications, and traceability artifacts are
unchanged. Rebol/toolchain unchanged (still BLOCKED). RFC-0075 remains an
independent specification blocker (validator FAIL preserved).
