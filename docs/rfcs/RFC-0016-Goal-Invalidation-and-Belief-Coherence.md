# RFC-0016 — Goal Invalidation & Belief Coherence Protocol (MESI for Cognition)

**RFC:** RFC-0016
**Title:** Goal Invalidation & Belief Coherence Protocol — A MESI-Like Coherence for Cognitive State
**Stable ID(s):** `RED-COHERENCE-001`
**Origin:** OP-06 (Goal Coherence Under World Change) — `COGOS-ANALYSIS-001 §X.2` + `COGOS-FRAMEWORK-ANALYSIS-001 §VII` — over weeks, business conditions shift, dependencies emerge; single agent's progress must invalidate other agents' stale goals or they duplicate/contradict + OP-08 (Collective False Memory) — `CVM-ANALYSIS-001 §VIII Guarantee 3` — locally consistent + globally contradictory beliefs consolidate via `SYNCHRONISE/MERGE`.
**Evolution:** RFC-0004 §3.9 introduced `invalidate-goal(trigger: world-state-changed)` as a new primitive (cache-coherence analog); RFC-0007 §§3.1/3.6 specified `SYNCHRONISE/MERGE` + cognitive lock file (RFC-0014) as the env-coherence sibling. This RFC unifies both as one coherence protocol.
**Final Representation:** This RFC + `invalidate-goal` + `SYNCHRONISE/MERGE` coherence states `Modified/Exclusive/Shared/Invalid` adapted for beliefs/goals.
**Status:** `Draft` — P0 (correctness/safety; co-closes OP-06 + OP-08)
**Verification:** Multi-agent goal-staleness test (agent A progresses, agent B's cached goal → Invalid before execute) + collective false-memory stress (contradictory beliefs → MERGE arbitration produces consistent global state).

---

## 1. Specification

### 1.1 `invalidate-goal` (normative)

```red
invalidate-goal my-plan trigger [world: git.push  on: %src/cogos.red changed]
```

Trigger condition is a **world-state predicate** (event-bus pattern, RFC-0003 event sources). Invalidation is *eager* — a goal holding a stale world view must not execute; scheduler marks `State=Invalid`.

### 1.2 Belief/Goal Coherence States (normative, MESI adaptation)

| State | Meaning (cognitive) | May Read | May Execute | Transition on Conflict |
|---|---|---|---|---|
| **M**odified | Agent holds locally updated belief/goal not yet shared | Yes | Yes | Broadcast on SYNCHRONISE → S |
| **E**xclusive | Agent holds sole copy, clean | Yes | Yes | Another agent's competing update → S |
| **S**hared | Multiple agents hold same version (clean) | Yes | **No** (verify first) | Conflicting write → I |
| **I**nvalid | Stale — world changed after this copy | No | **No** — must MERGE/REPLAN | Re-fetch after MERGE → S/E |

Shared→Execute requires `VERIFY` (RFC-0007 CISA) or `MERGE` arbitration.

### 1.3 Arbitration: `SYNCHRONISE`/`MERGE` (normative)

- **SYNCHRONISE [agents]** — publishes local Modified beliefs to shared semantic store (RFC-0004 knowledge graph) with provenance.
- **MERGE [belief ...]** — conflict resolution via cognitive anchoring / alignment (collective false-memory literature) — at minimum, conflicting beliefs are flagged as `I`nvalid until a higher-confidence provenance wins (e.g., `source: 'user` at `confidence: 1.0` anchors over inference).

## 2. Consequences

- **Correctness:** Without this, long-lived multi-agent systems pursue subtly wrong objectives (duplicate work, contradictory memory consolidation).
- **Trade-off:** Coherence traffic (SYNCHRONISE broadcasts) vs staleness — tuned by attention-based `BROADCAST` (RFC-0007 GWT).

## 3. Traceability

- **OPs:** OP-06 + OP-08 (co-closed), P0.
- **REQs:** REQ-009/020 (reflection/GC) + REQ-021 (MESI coherence).
- **Formal model:** MESI cache coherence + collective false-memory anchoring (2026).

