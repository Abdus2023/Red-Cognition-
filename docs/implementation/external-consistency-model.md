# External State Consistency Model (Stage-5, Phase 29)

**Date:** 2026-08-12 · **Controller:** 2.0.0

## Central invariant

> NO AUTHORITATIVE STATE CHANGE MAY LEAVE OLD EVIDENCE AUTHORIZED. NO EXTERNAL
> STATE MAY SILENTLY CHANGE THE MEANING OF AN EXISTING PASS.

## External state classification

| State | Classification | Identity-bound? | Mutation detected? |
|---|---|---|---|
| HEAD (git commit) | AUTHORITATIVE | YES (in contract_id) | contract_id change → evidence invalid |
| manifest content | AUTHORITATIVE | YES (manifest_hash in contract_id) | same |
| repository identity | AUTHORITATIVE | YES (repo_identity in contract_id) | same |
| target file state | AUTHORITATIVE (observation) | YES (target_hashes in evidence) | revalidated each PASS check |
| tool version | AUTHORITATIVE | YES (tool_versions in contract_id) | contract_id change |
| validation command | AUTHORITATIVE | YES (command_identity in contract_id) | same |
| criterion→validator | AUTHORITATIVE | YES (criteria in contract_id) | same |
| PATH availability | ENVIRONMENTAL | YES (classification-time check) | BLOCKED if tool missing |
| PID / hostname / env vars | ENVIRONMENTAL | NO (non-identity) | never affects PASS |
| timestamps | OPERATIONAL | NO (excluded from identity) | never affects PASS |
| checkpoint | DERIVED | NO | cross-checked, demoted |
| pipeline-status | DERIVED | NO | never read by controller |

## TOCTOU boundary

The execute loop acquires an exclusive fcntl lock. Within the lock:
1. `target_hashes` computed (post-command observation).
2. Evidence appended (flush + fsync).

A TOCTOU window of microseconds exists between (1) and (2) for **external**
(non-controller) file mutations. This window is **fail-closed**: on the next
run, `_authoritative_pass` recomputes `target_hashes` and demotes PASS if the
current state doesn't match the recorded observation.

No concurrent controller can exploit the window (fcntl lock serializes all
controllers).

## Mutation detection

Every external state mutation that could affect PASS is detected:

| Mutation | Detection mechanism | Result |
|---|---|---|
| HEAD change | head in contract_id | old evidence contract_id ≠ new → invalid |
| manifest change | manifest_hash in contract_id | same |
| target modified/deleted/symlinked | target_hashes revalidation | current ≠ recorded → demoted |
| command changed | command_identity in contract_id | contract_id change |
| criterion remapped | criteria in contract_id | contract_id change |
| tool version changed | tool_versions in contract_id | contract_id change |
| repo identity changed | repo_identity in contract_id | contract_id change |

## Recovery after external mutation

```
external mutation
    ↓
recover()
    ↓
_authoritative_pass recomputes
    ↓
contract_id / target_hashes mismatch
    ↓
stale PASS demoted
    ↓
BLOCKED / READY (re-attemptable)
```

Fresh PASS requires: new execution under the current contract + target state match.

## Honest terminology

- **PROVEN BY TEST:** all 21 EC cases (mutation, substitution, replay, recovery, determinism, seed).
- **FORMALLY SPECIFIED:** external-state classification table (this doc).
- **DOCUMENTED LIMITATION:** TOCTOU window is fail-closed (caught on next run, not prevented in-process for external mutations). Process-local lock (not cross-host). Power-loss durability BEST-EFFORT.
