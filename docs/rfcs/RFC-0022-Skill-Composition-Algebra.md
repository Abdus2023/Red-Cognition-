# RFC-0022 — Skill Composition Algebra (Semantic Pipes)

**RFC:** RFC-0022
**Title:** Skill Composition Algebra — DAG Composition vs Byte Pipes
**Stable ID(s):** `RED-SKILL-ALgebra-001`
**Origin:** OP-13 (Skill Composition Semantics) — `COGOS-FRAMEWORK-ANALYSIS-001 §V` — byte-stream pipes (`cat | grep | sort`) are clean; semantic skill composition (parallel DAG vs pipe) not formalised; LangGraph DAG analogy pending.
**Evolution:** RFC-0004 §3.8 noted skills (`Search Knowledge, Summarise, Write Code…`) internally invoke dozens of commands and compose via DAGs not pipes; RFC-0006 §3.2 showed DAG plans with parallelisation. This RFC makes the algebra normative.
**Final Representation:** This RFC + skill effect composition + DAG formalism + dispatch semantics.
**Status:** `Draft` — P2 (composability)
**Verification:** Skill DAG with independent `search + recall` parallelises; sequential `summarise → verify` remains ordered; effect set of composed skill is union of component effects.

---

## 1. Specification

### 1.1 Composition Operators (normative)

```
a >> b        ; sequence — effect set union, ordered
a || b        ; parallel — independent, dispatched concurrently (RFC-0006 parallelisation)
a ||> b       ; parallel-then-join — fan-out/fan-in with join capability
```

Byte pipe `|` is retained for Red's existing stream semantics; semantic composition uses `>>/||/||>` to distinguish effect-level composition (per RFC-0013 effect inference) from byte-level.

### 1.2 Effect Composition (normative)

`effect(skill a || b) = effect(a) ∪ effect(b)` — capability analysis of composed skill inherits the union of proof obligations (least-privilege preserved).

## 2. Traceability

- **OP:** OP-13 (Medium).
- **REQs:** REQ-010/014 (skill registry / parallelisation).

