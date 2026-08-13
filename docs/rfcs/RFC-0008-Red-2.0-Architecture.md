# RFC-0008 — Red 2.0 Cognitive Computing Architecture

**RFC:** RFC-0008
**Title:** Red 2.0 — One Language from Hardware to Intelligence: Three Compilers, Intent Contracts, and Cognitive GC
**Stable ID(s):** `RED-20-001`, `RED-20-ANALYSIS-001`
**Origin:** MSG-08 (Red 2.0: A Cognitive Computing Architecture) — extends slogan “One language from system programming to scripting” to “One language from hardware to intelligence” with the full diagram `Human Intent→Natural Language→Cognitive Dialects→Intent Compiler→Cognitive Optimiser→CIR→Cognitive Runtime→Memory/Reasoning/Capability→Red Core→Red/System→Machine→Hardware`.
**Evolution:** Analysis implies cognitive PGO speculative (PASTE), utility-function scheduler, trust assertion “Everything is a Trust Assertion” (GTG-1002), microkernel synthesis; no new correction to the stack — synthesis of RFCs 0003–0007 into one housing.
**Final Representation:** This RFC + Red 2.0 Unified Stack (three compilers + intent contracts + knowledge-flow/provenance + multi-objective optimisation + cognitive GC).
**Status:** `Draft` (vision; individual layers are Draft/Partially Implemented elsewhere)
**Authors:** Conversation MSG-08 + Analyzer + Auditor
**Verification:** Three-compiler separation `syntax vs semantic vs intent` golden-file (valid/sensible/accomplishes), intent contract completeness, knowledge-flow provenance chain, cognitive GC curation.

---

## 1. Abstract

Houses the cognitive lineage (RFCs 0003–0007) inside Red’s original full-stack housing, extending the language’s ambition from system programming through scripting to **cognitive computing**: intent is compiled, verified, and executed as a first-class compilation target.

## 2. Motivation

Without this RFC, the lineage is 5 isolated layers. This RFC states their unity as one toolchain where “computation becomes one subsystem of cognition” — the narrative that justifies Red/Cognition as an extension (like Red/System downward) rather than a separate project.

## 3. Specification

### 3.1 Unifying Diagram (normative, synthesis)

```
Human Intent → Natural Language → Cognitive Dialects → Intent Compiler → Cognitive Optimiser → CIR (Intent→Task→Capability→Exec)
      │
      └─► Cognitive Runtime / Agent Kernel
              ├─ Memory        ├─ Reasoning      ├─ Capability
              └─────────────────┴───────────────┘
                          │
                       Red Core
                          │
                      Red/System
                          │
                   Native Machine Code → Hardware
```

### 3.2 Three Compilers (normative)

| Compiler | Question Answered | Passes |
|---|---|---|
| **Syntax Compiler** | *Is this valid Red?* | Lexer, Parser (block tree) |
| **Semantic Compiler** | *Does this program make sense?* | Type checking, Binding, Scope |
| **Intent Compiler** | *Does this accomplish the stated objective?* | Declarative goal completeness, ambiguity detection (see RFC-0006 Intent Analysis) |

Each layer answers a different question — conflating them loses verification.

### 3.3 Intent Contracts (normative)

Function contracts `func[x [integer!]]` become intent contracts:

```
goal [purpose: "Summarise repository"  expected-output: report!  quality >= 95%  deadline: 5 minutes  budget: low]
```

Runtime understands **expectations**, not just inputs.

### 3.4 Cognitive Types, Knowledge Flow, Provenance (normative, synthesis)

Cognitive types `Fact/Observation/Belief/Hypothesis/Prediction/Decision/Evidence/Goal/Constraint/Policy/Capability` interrelate via **knowledge flow** `Observation→Evidence→Inference→Decision→Action` with **provenance graph** `Sensor→Observation→Reasoning Step→Decision→Action`, enabling explainability and auditing (see RFC-0007 CVM `EXPLAIN`).

### 3.5 Cognitive Optimisation & GC (normative)

- **Optimisation target** shifts from CPU cycles to multi-objective: `Reasoning Cost / Model Cost / Memory Cost / Execution Cost / Latency / Risk / Energy / Confidence`.
- **Cognitive GC** cures `Working Memory→Still Relevant? → Keep / Compress→Summarise→Archive→Forget`.

## 4. Consequences

- **Housing:** Red remains one language: `Scripts→Applications→GUI→System Programming` extended to `Machine Resources→System Programming→Application Programming→DSLs→Intent Programming→Goal Programming→Autonomous Cognitive Systems`.
- **No duplicate spec:** This RFC normatively references RFC-0006 for CIR details and RFC-0007 for CVM details; deviations are non-normative sketches.

## 5. Traceability

- **RFC Origin Map rows:** R36–R37 (toolchain + 3 compilers + intent contracts).
- **REQ IDs:** REQ-022 (Red toolchain invariants) remains `Implemented`; Red 2.0 itself adds no new REQ beyond unifying R36/R37.
- **ADR:** ADR-010 (Three Compilers) — normative here.
- **Formal models:** No new external model beyond synthesis; PGO speculative (PASTE) and trust assertion (GTG-1002) implications from Analyses.

## 6. Dependencies

- **Upstream:** RFCs 0002–0007 (all); RFC-0009 (Red deep spec as substrate).
- **Downstream:** None normative; informs `docs/wiki/Red-and-AI-Agents.md` synthesis (MSG-10) as single-file entry point for this unified view.

## 7. Appendix — Wiki Source Mapping

- `Red-2.0-Cognitive-Computing-Architecture.md` (`RED-20-001`, 380 lines) — §§ Human Intent→CIR diagram, three compilers, contracts, types, knowledge flow, optimisation, GC.
- `Red-2.0-Analysis.md` (`RED-20-ANALYSIS-001`, 279 lines) — PGO speculative, utility scheduler, trust assertion.

