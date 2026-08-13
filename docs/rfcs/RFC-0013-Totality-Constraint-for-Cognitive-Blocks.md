# RFC-0013 — Totality and Recursion Constraints for Cognitive Blocks

**RFC:** RFC-0013
**Title:** Totality and Recursion Constraints for Cognitive Blocks — Effect Inference Termination
**Stable ID(s):** `RED-TOTALITY-001`
**Origin:** OP-03 (Effect Inference Termination) — `RED-COMPILER-ANALYSIS-001 §X.1` — recursive `reflect → improve plan → re-execute` creates a recursive effect computation; effect inference may not terminate; depends on `RED-COMPILER-001 § Cognitive Effects` (`observe! remember! modify! communicate! reason! execute! learn!`).
**Evolution:** RFC-0006 §3.5 flagged totality vs structural constraint (`no recursive plan without explicit base case`). This RFC chooses the enforcement.
**Final Representation:** This RFC + totality checker (lint/compile phase) + lint rule `no-recursive-cognitive-block-without-base`.
**Status:** `Draft` — P1 (compiler soundness)
**Verification:** Self-referential `plan improve [reflect improve plan]` without base case is rejected; with `on-failure` + explicit termination condition compiles and effect set is finite.

---

## 1. Specification

### 1.1 Normative Rule (lint + type phase)

```
A cognitive block (`reason` / `plan` / `reflect`) that transitively calls itself
is well-formed IFF:
  (a) it has an explicit base case (pattern match on confidence / budget / iteration-count), and
  (b) its effect set is finite modulo widening (fixed-point or `unknown!` over-approximation requires annotation).
```

### 1.2 Enforcement Phases

- **Intent Analysis** — syntactic recursion detection (call-graph construction).
- **Effect Inference** — fixed-point iteration with iteration bound + widening; bound expiry requires `effects [unknown!]` annotation, making unsoundness explicit and reviewable.

### 2. Consequences

- **Soundness:** Termination proof burden is explicit, not hidden.
- **Trade-off:** Some valid recursive plans require annotation — the ergonomic cost of OP-02's sibling; accepted as the Rust-borrow-style “learn the checker” cost.

## 3. Traceability

- **OP:** OP-03 (High — soundness).
- **REQ:** REQ-014 (Effect Inference).
- **Formal model:** Dependent-type totality (Agda/Idris) as precedent.

