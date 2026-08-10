# RFC-0006 — Cognitive Compiler and Cognitive Intermediate Representation (CIR)

**RFC:** RFC-0006
**Title:** Cognitive Compiler — Intent as Compilation Target, CIR (Goal→Intent→Task→Capability→Execution), DAG Plans, and Verified Compilation
**Stable ID(s):** `RED-COMPILER-001`, `RED-COMPILER-ANALYSIS-001`
**Origin:** MSG-06 (Refactoring the Red Compiler) — adds `Intent Analysis → Planning Analysis → Capability Analysis` to `Source→Lexer→Parser→AST→Semantic→Codegen`; introduces **Cognitive Intermediate Representation (CIR)**.
**Evolution:** Grounded in Analysis §§I–II via 1,600-trace failure analysis (41.8% spec failures), PlanCompiler DAG+topological compilation, growing-context cost (3.6× tokens), hybrid routing benchmarks (1.8–3.7×), RHTT Policy-as-Type theorem; extends with cognitive PGO (PASTE speculative), full pipeline diagram with 4 new passes, ergonomic proof obligations, and three critical compiler problems (effect termination, proof granularity, CIR version mismatch / cognitive lock file) per Analysis §§X–XI.
**Final Representation:** This RFC + Cognitive Compiler pipeline (5 passes: Intent / Effect / Capability / Planning / Optimisation) + CIR emitter (4 graphs: Intent→Task→Capability→Exec → Red IR / Red/System / WASM).
**Status:** `Draft` (spec; PlanCompiler exists at framework level, not language level)
**Authors:** Conversation MSG-06 + Analyzer MSG-06 + Auditor
**Verification:** DAG acyclicity + budget + completeness compile tests; parallel 1.8–3.7× speedup benchmark; `policy: dangerous` proof-obligation reject/accept; growing-context vs single-pass token count audit.

---

## 1. Abstract

Makes *intent* a compilation target: the compiler asks not only “Is this program valid?” but “What is this program trying to accomplish?” and validates reasoning structures before spending tokens.

## 2. Motivation

79% of production agent failures (1,600 traces, 7 frameworks) are specification/coordination failures, not infrastructure — exactly what a compiler catching intent before inference can address. Growing-context agents replay 3.6× tokens at 3.5× cost vs a single compiled deterministic pass. This RFC is that pass, stated at the language level.

## 3. Specification

### 3.1 Compiler Pipeline Extension (normative)

```
Source → Lexer → Parser → AST → Semantic Analysis → Intent Analysis [NEW] → Effect Inference [NEW] → Capability Analysis [NEW] → Planning Analysis [NEW] → Intent Optimisation [NEW] → CIR Emission → (Red IR | Red/System | WASM)
```

- **Intent Analysis:** goal type classification (achievement vs procedural), declarative goal completeness, ambiguity detection.
- **Effect Inference:** derive effect signatures (`observe! remember! modify! communicate! reason! execute! learn!`) per block; propagate through call graph (see §3.5 termination).
- **Capability Analysis:** policy type checking, proof obligation generation, least-privilege validation, permission scope verification (see §3.6).
- **Planning Analysis:** goal→DAG expansion, dependency resolution, parallelisation detection, cycle detection (acyclicity proof).
- **Intent Optimisation:** goal simplification, duplicate goal elimination, plan fusion (parallel steps), reasoning budget optimisation, skill selection (model routing) + profile-guided speculative paths (PASTE).

### 3.2 Cognitive Intermediate Representation — 6-Stage Lowering (normative)

```
Goal ──► Intent Graph ──► Task Graph ──► Capability Graph ──► Execution Graph ──► Machine Code
                  (Intent→Task→Capability→Execution as CIR facets)
```

- First lowers to **reasoning structures**, not instructions; enables optimisation before token spend.
- Intent Graph: highest abstraction (goals + declarative completeness).
- Task DAG: parallelism explicit (the `Plans Become Dataflow Graphs` section — sequential `A→B→C` becomes `Observe├→Analyse, ├→Retrieve Memory →Generate Plan→Execute`).
- Capability Graph: policies bound.
- Execution Graph: models assigned.

Backends: `Red IR` (interpreted), `Red/System` (compiled), `WASM/Native` (embedded).

### 3.3 Plans Become Dataflow Graphs (normative)

A cognitive program naturally forms a dependency graph; topological compilation allows **cost and feasibility validation before any tool call fires** (validated by PlanCompiler pre-type, Apr 2026). Parallel execution collapses cumulative latency to the single slowest call.

### 3.4 Native Goal Scheduler (normative, shared with RFC-0004)

```red
Goal { Priority, Deadline, Dependencies, Confidence, Cost, Policies }
```

Scheduling becomes a language feature (not app concern), with utility-function per task across model tiers. `red/cognition` tuple per Analysis §VI.

### 3.5 Effect Inference & Totality (normative, Open Problem OP-03)

Recursive plans (`reflect → improve plan → re-execute`) may not terminate; effect inference through call graph requires **totality proof** or structural constraint `no recursive plan without explicit base case` (analogous to dependent-type totality). Compiler must enforce or lint.

### 3.6 Policies Become Types & Effects (normative)

Early compiler optimisations `constant folding` etc. are augmented with cognitive passes:

```red
delete-directory: capability! [policy: dangerous]
analyse: func [repo [repository!]][effects [observe remember reason]]
```

A `dangerous` capability without an authorisation token **does not type-check** — proof term required. Complex ABAC conjunctions require **ergonomic proof elaboration** (OP-02: Agda tactics vs Rust-borrow models — Red needs its own answer). Effects enable static permission checking + test isolation.

### 3.7 CIR Version Mismatch / Cognitive Lock File (normative, Open Problem OP-04)

When world-state changes invalidate a compiled plan, recompile-on-drift regenerates against current reality. But skill registry / capability policies / model availability may have drifted between compile and recompile — the CIR needs a **stable queryable environment snapshot** (cognitive lock file, analogous to dependency lock file). No classical compiler equivalent.

## 4. Consequences

- **Deterministic artifact:** same inputs → same execution path → predictable per-case cost, audit trail generated with decision (not reconstructed after).
- **Performance lever:** static parallelisation detection delivers 1.8–3.7× wall-clock speedup + up to 6× cost reduction purely at compile time.
- **Trade-off:** Proof ergonomics vs abandonment risk; termination requires discipline; lock file is novel engineering.

## 5. Traceability

- **RFC Origin Map rows:** R23–R30 (CIR, DAG, intent optimisation, planner as pass, policies-as-types, effects, goal scheduler, self-modifying plans, multi-agent).
- **REQ IDs:** REQ-013 (CIR 4 graphs), REQ-014 (5 passes + parallelisation), REQ-015 (policy-as-type), REQ-016 prerequisite (CIR → CVM).
- **ADRs:** ADR-005 (CIR as typed DAG), ADR-006 (Policy-as-Type), ADR-009 (self-modifying plans, not code), ADR-010 (three compilers — unified in RFC-0008).
- **Formal models:** PlanCompiler + DAG Plan-and-Execute + PASTE speculative; IR theory (front/middle/back) + Intent-Driven IR Optimisation (Feb 2026); RHTT dependent types; 1,600-trace failure analysis + 306-practitioner survey.
- **Open problems:** OP-02 (proof granularity), OP-03 (termination), OP-04 (lock file).

## 6. Dependencies

- **Upstream:** RFC-0002 (Red core), RFC-0005 (16 types are the CIR vocabulary).
- **Downstream:** RFC-0007 (CVM executes CIR), RFC-0008 (three compilers unify here + RFC-0002).

## 7. Appendix — Wiki Source Mapping

- `Red-Compiler-Refactoring.md` (359 lines) — §§ core evolution through complete vision.
- `Red-Compiler-Analysis.md` (290 `wc -l`, 30k rendered) — §§ I–XI grounding, full pipeline diagram, three critical problems, synthesis — artefacts carry provenance/proof/parallelism/model bindings/history.
