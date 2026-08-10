# RFC-0012 — Ergonomic Proof Elaboration Tactics for Capability Types

**RFC:** RFC-0012
**Title:** Ergonomic Proof Elaboration Tactics for Capability Types — Making `policy: dangerous` Usable
**Stable ID(s):** `RED-PROOF-ERGONOMIC-001`
**Origin:** OP-02 (Policy Proof Obligation Granularity) — `RED-COMPILER-ANALYSIS-001 §X.2` — ABAC conjunctions (Policy-as-Type, June 2025 + RHTT) become ergonomically heavyweight; Agda tactics vs Rust borrow-checker models insufficient for Red; programmers may abandon the type system.
**Evolution:** RFC-0006 §3.6 states `delete-directory: capability! [policy: dangerous]` requires a proof term; Analysis notes two precedent ergonomics (Agda elaboration, Rust borrow) but Red needs its own. This RFC is the engineering answer that was flagged Open.
**Final Representation:** This RFC + Capability Analysis pass elaboration tactics + dialect-embedded `authorisation` sugar that discharges proof obligations without manual proof-term boilerplate.
**Status:** `Draft` — P1 (adoption risk, not soundness; blocks friendly Policy-as-Type)
**Verification:** `dangerous` capability without token fails fast with *actionable* diagnostic; with token + tactic succeeds; complexity-tier examples compile with ≤2 extra tokens per declaration.

---

## 1. Abstract

Specifies how proof obligation discharge for `capability! [policy: ...]` becomes ergonomic enough that engineers prefer it over ad-hoc runtime checks — the difference between a theorem that is *true* and one that is *used*.

## 2. Specification (sketch, normative intent)

### 2.1 Complexity Tiers (normative)

```
Tier 0 — safe!       (no proof term; e.g., read-self)
Tier 1 — dangerous   (single authorisation token)
Tier 2 — ABAC conj   (e.g., policy: [role: reviewer  expiry: now+30m] — conjunction)
Tier 3 — temporal    (validity window + audit scope)
```

### 2.2 Tactics (normative categories)

- **Token inference:** `execute [delete %temp/]` inside `with-authorisation [delete: scope %temp/ expiry ...]` infers token for enclosed `dangerous` call — no explicit proof argument at call-site.
- **Elaboration:** Dialect sugar expands `with-authorisation` to the underlying dependent-type proof term; error messages show the *expanded* missing obligation, not just “type mismatch”.
- **Least-privilege default:** `capability!` defaults to `scope: narrow`; widening scope requires explicit `expand-scope` — making secure the ergonomic default (parallels Rust's default borrow check).

### 3. Consequences

- **Adoption:** Ergonomic discharge is the lever between `Proven` and `Adopted`.
- **Trade-off:** Sugar vs transparency — elaborated term is inspectable via `CIR` provenance (RFC-0006 §3.7).
- **Future:** Formal tactics may share code with Red's `Parse` dialect elaboration (see `lexer.r` dialect generation).

## 4. Traceability

- **OP:** OP-02 (High — adoption).
- **REQ:** REQ-015 (Policy-as-Type).
- **Formal model:** Policy-as-Type (June 2025) + RHTT.
