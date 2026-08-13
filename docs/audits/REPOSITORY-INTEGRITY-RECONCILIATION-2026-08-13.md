# Repository Integrity Reconciliation — 2026-08-13

**Document class:** Independent Repository Audit — reconciliation register
**Status:** Informational / Non-normative (records governance actions; does not modify frozen Stage 4/5 semantics)
**Baseline audited:** `4b06081ae5b13eb692968a1467e7a46ce6fd1f7a`
**Companion:** [Deep Analysis](RED-COGNITION-DEEP-ANALYSIS-2026-08-13.md) · [Project Invariants](../PROJECT-INVARIANTS.md) · [Ratification Registry](../governance/ratification-registry.md)

## Purpose

The deep analysis found a second, toolchain-independent class of defects. This
register reconciles them in the prescribed order, records every action with
evidence, and separates what is **mechanically resolvable now** from what
**requires owner/designer adjudication**.

Sequence honored:

```
FROZEN ARCHITECTURE (preserve) → INDEPENDENT AUDIT → CORRECTION/REGENERATION
→ RE-AUDIT → GATE A + VERTICAL SLICE
```

---

## 1. Defect register

| # | Defect | Evidence (exact) | Classification | Action taken |
|---|---|---|---|---|
| D1 | RFC-0075 internal terminology (CADFP vs CFCKEP) | `rfcs/RFC-0075-…md` lines 217, 227, 251, 263 use "CADFP"; provenance comment flags review [420] "highest-priority terminology fix" | Adjudicated (mechanical) | **Corrected** — 4 body occurrences → CFCKEP; archive preserved |
| D2 | RFC-0063 title wrong in derived index | `docs/RFC-INDEX.md` RFC-0063 row shows "RFC-0064 — CCC-VTP v1.0"; file itself is correct | Stale derived artifact + generator gap | **Fixed** — generator reads `# h1`/`## h2` titles; index regenerated |
| D3 | Ratification count drift (16 vs 17 vs 19/22) | `freeze-baseline.md`, `pipeline-report.md` say 16; 17 record files; KB audit #8 lists 19 RFCs + 3 RC | Counting heuristic bug + stale artifacts | **Fixed** — [Ratification Registry](../governance/ratification-registry.md) is now sole source; generators read it |
| D4 | Controller version drift (1.1.0 vs 2.0.0) | `__init__.py`=2.0.0; `controller-readme.md` §Hardening="v1.1.0"; `evidence-contract.md`="Controller version: 1.1.0" | Documentation drift | **Fixed** — docs reconciled to 2.0.0 |
| D5 | Referenced CI workflow missing | 13 docs reference `.github/workflows/implementation-pipeline.yml`; only `main.yml` exists | Documentation/infra drift | **Authored** — `.github/workflows/implementation-pipeline.yml` is written in the working tree and enforces Invariant 1. **AUTHORED ≠ PUBLISHED**: intentionally not committed here because the push credential lacks the GitHub `workflows` permission; publish unchanged once a `workflows`-scoped credential is available. Not relocated — moving it to bypass the authorization boundary would violate the controller's own principle |
| D6 | Self-test case count stale | `controller-readme.md` says "24 cases"; suite is 390 | Documentation drift | **Fixed** |
| D7 | Stale derived artifacts (heads/counts) | `pipeline-status.json` repo_head `438689ab`; `pipeline-report.md` HEAD `ec0c6ef` + "16 ratified"; `full-pipeline-status.json` `ratified:16` | Stale generation | **Fixed** — regenerated at `4b06081` |
| D8 | RFC-0075 candidate-vs-record divergence | `rfcs/` scaffold (Candidate; "Collaboration"; parent CRPDGSMP) vs `docs/specifications/…/RFC-0075-Ratification-Record.md` ("Ratified upon RFC-0074"; "Coordination"; parent "Federation Governance and Trust Framework") | Requires owner adjudication | **Deferred to owner** (CONFLICT-0075-004) |
| D9 | RFC-0075 discovery-scope overlap with RFC-0054 | CONFLICT-0075-002 (`cog agent register/discover` appears CADFP-oriented) | Requires owner adjudication | **Deferred to owner** |
| D10 | RFC-0075 determinism/replay vs missing canonical types | CONFLICT-0075-003 + GAP-001/004 | Requires normative authoring | **Deferred to designer** |
| D11 | 4 CRITICAL RFC-0075 gaps (schemas/lifecycle/crypto/replay) | `15-gaps.md` GAP-001…004 | Requires normative authoring | **Deferred to designer** — RFC0075-001 stays BLOCKED |
| D12 | RFC-0046/0047 ratified but no record file | KB audit #8 lists both; no `-ratification-record.md` in `rfcs/` | Scaffold-completeness gap | **Recorded in registry** (not fabricated) |

---

## 2. RFC-0075 adjudication (detail)

### CONFLICT-0075-001 — CADFP vs CFCKEP → **ADJUDICATED: CFCKEP is canonical**

- Canonical identity: filename, title, §§1–14, and the RFC-0054-unrelated
  provenance all name **CFCKEP** (Cognitive Federation, Collaboration, and
  Knowledge Exchange Protocol).
- The four body occurrences (lines 217, 227, 251, 263) each describe
  CFCKEP's own integrations/conformance profiles, not RFC-0054 (CADFP).
- The provenance comment already flags this as "the highest-priority
  terminology fix" per review [420].
- **Action:** corrected the four occurrences to CFCKEP. The verbatim archive
  (`knowledge-base/sources/`) retains the uncorrected original as provenance.
  `docs/traceability/rfc-0075/traceability.json` SHA-256 re-pinned;
  `16-conflicts.md` marks this conflict RESOLVED. (The machine inventory still
  records all four conflict IDs for provenance — the validator's `conflicts: 4`
  includes the resolved #1; three remain outstanding.)

### CONFLICT-0075-002 — discovery scope vs RFC-0054 → **DEFERRED (owner)**

`cog agent register/discover` and "local registration and discovery" (§17–18)
appear to be CADFP (RFC-0054) discovery behavior, not CFCKEP federation
exchange. Whether this content should move to RFC-0054 or be re-scoped as
CFCKEP behavior is an authority decision. Not invented here.

### CONFLICT-0075-003 — determinism/replay vs missing canonical types → **DEFERRED (designer)**

Determinism/replay are mandatory but canonical types/serialization/input
capture are absent. This cannot be "adjudicated" without authoring the missing
normative content (overlaps GAP-001/004).

### CONFLICT-0075-004 — candidate body vs divergent ratification record → **DEFERRED (owner)**

Two RFC-0075 documents exist with different titles ("Collaboration" vs
"Coordination"), different RFC-0074 parents (CRPDGSMP vs "Federation Governance
and Trust Framework"), different lifecycles (8-stage vs 5-stage) and different
profile sets (5 vs 3). The Ratification Registry does **not** adopt the
`docs/specifications/…` record; RFC-0075 remains a Candidate pending owner
adjudication.

### Critical gaps (remain BLOCKED)

GAP-0075-001 (normative schemas), 002 (lifecycle state machine), 003
(cryptographic profile), 004 (replay model) require new normative specification.
`RFC0075-001` remains **BLOCKED — SPECIFICATION_CONFLICT + INCOMPLETE_SPECIFICATION**.

---

## 3. Ratification-count reconciliation

Single source of truth established:
[`docs/governance/ratification-registry.{md,json}`](../governance/ratification-registry.md).

Authoritative count: **3 RC + 19 RFCs = 22 ratified documents** (17 record
files; 2 corpus-only; RFC-0072 conditional). The legacy substring heuristic
(`"Ratified" in status`) that produced "16" is retired; `run-full-pipeline.py`
now reads the registry.

## 4. Derived-artifact regeneration (post-correction)

- `tools/generate_repository_index.py` — `title()` now recognizes `# h1` /
  `## h2` in addition to `**bold**` titles; RFC-INDEX and companions regenerated.
- `tools/run-full-pipeline.py` — `ratified` derived from the registry;
  `full-pipeline-status.json` regenerated (HEAD `4b06081`, ratified 19).
- `tools/generate_report.py` — `pipeline-report.md` regenerated.
- `docs/traceability/rfc-0075/` — SHA-256 re-pinned; conflict register updated;
  validator re-run (remains FAIL — critical gaps, by design).

## 5. Re-audit results (this session)

| Check | Result |
|---|---|
| Controller suite | 390/390 PASS |
| Repository index validator | PASS |
| RFC-0075 traceability validator | FAIL — by design (4 critical gaps remain) |
| Ratification registry count | 22 (authoritative) |

## 6. Items requiring owner/designer input (not fabricated)

1. **CONFLICT-0075-002 / -004** — which RFC-0075 lineage is authoritative.
2. **GAP-0075-001…004** — author the normative schemas, lifecycle, crypto
   profile, and replay model.
3. **RFC-0046 / RFC-0047** — scaffold their missing ratification-record files
   from the corpus (or confirm they are intentionally corpus-only).
4. **Gate A** — provide/authorize the Rebol 2.7.8 execution path.
