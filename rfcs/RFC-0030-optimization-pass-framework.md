<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #16, sub-message [153], 2026-08-10
  Verbatim source: knowledge-base/sources/message-016-original-part*.md
  Status in corpus: RFC-0030 Cognitive Optimization Pass Framework v1.0 (Draft); review [154]: OptimizationPass model, goal/capability/effect-aware optimization, COIL proposal; v1.1 not present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0030 — Cognitive Optimization Pass Framework**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0029 Cognitive IR Serialization Format (CIR-SER) v1.0 (Draft)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Optimization Pass Framework** for Red/Cognition.

The framework specifies the structure, legality rules, ordering, and safety guarantees for optimization passes that operate on the Cognitive Intermediate Representation (CIR) defined in RFC-0028. These passes transform cognitive programs to improve efficiency, reduce resource usage, or simplify execution while preserving determinism, traceability, capability constraints, and replay equivalence.

### 2. Design Principles

The optimization framework follows these principles:

- **Semantic Preservation** — Optimizations must not alter the observable semantics of the original program.
- **Determinism** — Optimized programs must remain deterministic and replayable.
- **Capability Awareness** — Optimizations must respect and preserve declared capability requirements.
- **Effect Safety** — Optimizations must not introduce, remove, or reorder effects in ways that violate the rules defined in RFC-0002.
- **Traceability** — Optimization decisions must be recorded so that the transformation from original to optimized program remains explainable.
- **Provider Neutrality** — Optimization passes must not embed assumptions about specific reasoning or planning mechanisms.

### 3. Optimization Pass Structure

An optimization pass is defined as a transformation that takes a valid CIR module and produces a new valid CIR module. Every pass **MUST** specify:

- **Input Requirements** — The CIR properties the pass expects.
- **Output Guarantees** — The properties the transformed CIR will satisfy.
- **Legality Conditions** — When the pass may be safely applied.
- **Effect on Traces** — How the pass affects execution traces and replay.
- **Capability Impact** — How the pass affects capability requirements.

### 4. Categories of Optimization Passes

The framework recognizes the following categories of passes:

| Category                    | Purpose                                      | Examples                              |
|-----------------------------|----------------------------------------------|---------------------------------------|
| **Simplification**          | Reduce complexity of cognitive structures    | Goal merging, plan simplification     |
| **Capability Minimization** | Reduce or consolidate capability requirements| Capability hoisting, redundant check removal |
| **Effect Scheduling**       | Reorder effects while preserving causality   | Independent effect reordering         |
| **Memory Optimization**     | Improve memory access patterns               | Working memory reduction, memory access coalescing |
| **Resource Optimization**   | Reduce estimated resource consumption        | Instruction count reduction, energy-aware scheduling |
| **Determinism Strengthening** | Increase determinism level of the program | Removal of non-deterministic paths    |

### 5. Legality and Safety Rules

Every optimization pass **MUST** obey the following rules:

- The pass **MUST NOT** violate the Effect Ordering Model (RFC-0002).
- The pass **MUST NOT** increase the set of required capabilities unless explicitly allowed by policy.
- The pass **MUST NOT** alter the observable goal satisfaction semantics (RFC-0004).
- The pass **MUST** preserve the ability to produce equivalent execution traces during replay.

### 6. Pass Ordering and Dependencies

Optimization passes **MAY** declare dependencies on other passes.

The compiler **MUST** ensure that passes are executed in an order that respects their dependencies and legality conditions.

### 7. Traceability of Optimizations

Every optimization pass **MUST** record its application in a way that allows reconstruction of the original program from the optimized version during replay or debugging.

### 8. Relationship to Other RFCs

This framework integrates with:

- RFC-0002 — Effect Ordering Model (effect safety)
- RFC-0004 — Goal Lifecycle (goal semantics preservation)
- RFC-0006 — Capability Model (capability requirements)
- RFC-0011 — Scheduler (resource optimization)
- RFC-0024 — Resource Management (resource estimates)
- RFC-0028 — CIR (transformation target)

### 9. Open Questions

The following areas require future specification:

- Concrete set of standard optimization passes
- Formal verification of optimization correctness
- Interaction with hardware acceleration (RFC-0026)
- Just-in-time optimization model

---

**RFC-0030 — Cognitive Optimization Pass Framework v1.0 Draft** is now complete.

This RFC establishes the structure and safety rules for optimization passes operating on CIR. It provides the foundation for building a robust, deterministic, and auditable optimization pipeline in the cognitive compiler.
