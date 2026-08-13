# RFC-0021 — Attention Arbitration & Liveness Guarantees

**RFC:** RFC-0021
**Title:** Attention Arbitration & Liveness Guarantees — GWT Competition with Parity and Starvation Freedom
**Stable ID(s):** `RED-ATTENTION-001`
**Origin:** OP-12 (Attention Competition Deadlock / Cognitive Stagnation) — `CVM-ANALYSIS-001 §II` — improper attention → sycophancy/echo chambers/degeneration; attention is safety-critical but starvation semantics unspecified.
**Evolution:** RFC-0007 §3.4 introduced `ATTEND/COMPETE/BROADCAST/SUPPRESS/THRESHOLD` with GWT spotlight but omitted liveness guarantees. This RFC adds them.
**Final Representation:** This RFC + `COMPETE/BROADCAST` arbitration protocol + liveness parity guarantee + echo-chamber regression suite.
**Status:** `Draft` — P1 (safety)
**Verification:** Multi-agent sycophancy regression (no agent starved beyond fairness window); echo-chamber detection (diverse attention history maintained).

---

## 1. Specification

### 1.1 Arbitration (normative)

`COMPETE [entity ...]` ranks by `Attention Score (Importance/Urgency/Novelty/Risk)` per RFC-0007, but with **aging** — wait time boosts score to prevent starvation.

`BROADCAST` delivers winner to all modules (Global Workspace) within bounded ticks; suppressed entities re-enter competition next cycle, not discarded.

### 1.2 Liveness (normative)

Every `ATTEND`-registered agent receives `BROADCAST` at least once per fairness window `W` (configurable, default matches scheduler quantum). Violation → scheduler escalation.

## 2. Traceability

- **OP:** OP-12 (High — safety).
- **REQs:** REQ-018 (GWT attention).

