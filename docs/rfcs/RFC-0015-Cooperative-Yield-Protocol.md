# RFC-0015 — Cooperative Yield Protocol for Goal Blocks

**RFC:** RFC-0015
**Title:** Cooperative Yield Protocol for Goal Blocks — Explicit Yield Points for Non-Preemptible LLM Inference
**Stable ID(s):** `RED-YIELD-001`
**Origin:** OP-05 (Cooperative Scheduling vs Preemption) — `COGOS-ANALYSIS-001 §X.1` — LLM inference is non-preemptible; goal scheduler must be cooperative with explicit yield points; discipline nonexistent in any framework (68% of practitioners limit to ≤10 steps).
**Evolution:** RFC-0004 §3.1 introduced Goal Scheduler tuple `Priority/Deadline/Dependency/Confidence/Cost/Policies/Budget`; RFC-0006 §3.4 made scheduler a language feature but flagged cooperative vs preemptive as Open Question (ADR: preemptive rejected). This RFC chooses cooperative and specifies the yield syntax.
**Final Representation:** This RFC + `yield` dialect + Goal Scheduler checkpoint semantics + `yield-required` lint pass.
**Status:** `Draft` — P1 (liveness)
**Verification:** Goal block without yield on ≥5-step path lints; scheduler respects yield → fair interleaving vs no-yield starvation benchmark.

---

## 1. Specification

### 1.1 `yield` (normative)

```red
goal review-pr [
    observe %changes
    yield                          ; scheduler checkpoint — may interleave other goals
    plan  [inspect architecture]
    yield [priority high]          ; optional hint: urgency, budget-remaining
    verify
]
```

- `yield` is a **cooperation point**, not a cancellation. Semantics: current goal's `Confidence`/`Budget`/`Priority` snapshot is published to Goal Scheduler; scheduler may elect to continue or interleave another goal (utility-function per RFC-0004 §3.10). Without `yield`, a long goal monopolises the LLM.

### 1.2 Lint Rule (normative)

Every `goal!`/`plan!` block whose static step count ≥ `N` (default 5 — configurable, matches 68% practitioner threshold) **must** contain at least one `yield`. Missing yield → compile-time lint (warning in Tier 0, error in Tier 1 with `policy: strict`).

### 1.3 Scheduler Hint (informative)

`yield [priority high]` / `yield [budget low]` are hints, not directives — scheduler remains authoritative. Enables attention-aware scheduling (RFC-0007 GWT spotlight) without coupling goal logic to scheduler internals.

## 2. Consequences

- **Liveness:** Cooperative yield is the only liveness-compatible discipline for non-preemptible inference.
- **Trade-off:** Yield placement is programmer burden — mitigated by lint + future `PGO` suggesting hot-path yields (PASTE pattern-aware).

## 3. Traceability

- **OP:** OP-05 (High — liveness).
- **REQs:** REQ-006 (goal scheduler).
- **Dependencies:** RFCs 0004/0006/0007.

