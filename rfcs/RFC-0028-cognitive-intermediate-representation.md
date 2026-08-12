<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #16, sub-message [149], 2026-08-10
  Verbatim source: knowledge-base/sources/message-016-original-part*.md
  Status in corpus: RFC-0028 Cognitive Intermediate Representation (CIR) v1.0 (Draft); review [150]: multi-graph IR, CIROperation, compiler passes; v1.1 not present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0028 — Cognitive Intermediate Representation (CIR)**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0027 Cognitive Compiler and Toolchain Architecture v1.0 (Draft)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Intermediate Representation (CIR)** for Red/Cognition.

CIR serves as the central, implementation-independent representation used by the cognitive compiler (RFC-0027) to analyze, optimize, and generate executable CISA programs (RFC-0013). It sits between the high-level cognitive program representation (dialects, structured blocks, or future high-level syntax) and the low-level CISA binary encoding.

### 2. Design Principles

CIR follows these core principles:

- **Determinism** — The same source program must produce a deterministic CIR representation.
- **Traceability** — CIR must preserve source-level provenance and structure for debugging and replay.
- **Provider Neutrality** — CIR must not embed assumptions about specific reasoning or planning mechanisms.
- **Capability Awareness** — CIR must explicitly represent capability requirements and effects.
- **Replay Support** — CIR must support deterministic replay when combined with appropriate checkpoints and traces.
- **Modularity** — CIR must allow independent analysis and optimization passes.

### 3. CIR Structure

A CIR program is organized as a module containing the following components:

```
CIRModule {
    Identity,
    CognitiveTypes,
    Graphs: {
        GoalGraph,
        PlanGraph,
        EffectGraph,
        CapabilityGraph,
        MemoryAccessGraph
    },
    Operations: [
        Observe,
        Infer,
        Remember,
        Plan,
        Execute,
        Reflect,
        Checkpoint
    ],
    Constraints: {
        CapabilityRequirements,
        ResourceRequirements,
        DeterminismRules
    }
}
```

### 4. Cognitive Graphs

CIR represents relationships between cognitive entities using directed graphs. These graphs **MUST** be Directed Acyclic Graphs (DAGs) unless cycles are explicitly declared and handled.

Key graphs include:

- **GoalGraph** — Dependencies and satisfaction relationships between goals.
- **PlanGraph** — Execution dependencies and revision history of plans.
- **EffectGraph** — Causal ordering and dependencies of effects (aligned with RFC-0002).
- **CapabilityGraph** — Inheritance and delegation relationships between capabilities (aligned with RFC-0006).
- **MemoryAccessGraph** — Read/write relationships between operations and memory tiers (aligned with RFC-0008).

### 5. Operations

CIR defines a set of core operations that correspond to the instruction categories in CISA (RFC-0013):

- **Observe** — Capture external state or events.
- **Infer** — Perform reasoning over beliefs.
- **Remember** — Update memory (episodic, semantic, or procedural).
- **Plan** — Generate or revise plans for goals.
- **Execute** — Invoke skills or produce effects.
- **Reflect** — Update beliefs or plans based on outcomes.
- **Checkpoint** — Create a recoverable execution state.

Each operation **MUST** declare its required capabilities, expected effects, and memory access patterns.

### 6. Constraints

CIR programs **MUST** carry explicit constraints that the compiler and runtime can verify:

- **Capability Requirements** — The set of capabilities needed for execution.
- **Resource Requirements** — Expected consumption of execution time, memory, and other resources (aligned with RFC-0024).
- **Determinism Rules** — Whether the program must execute deterministically and at what level (aligned with RFC-0011 and RFC-0012).

### 7. Relationship to Other RFCs

CIR integrates with:

- RFC-0001 through RFC-0009 — Cognitive type and semantic models
- RFC-0011 — Scheduler (resource and capability constraints for scheduling)
- RFC-0012 — CVM Execution Semantics (target instruction semantics)
- RFC-0013 — CISA (instruction generation target)
- RFC-0015 — Exception Semantics (static analysis of failure paths)
- RFC-0016 — Cognitive Runtime Architecture (runtime services)
- RFC-0026 — Hardware Acceleration (backend selection and constraints)

### 8. Open Questions

The following areas require future specification:

- Concrete serialization format for CIR
- Formal verification of CIR programs
- Optimization pass specifications
- Integration with high-level cognitive programming languages

---

**RFC-0028 — Cognitive Intermediate Representation (CIR) v1.0 Draft** is now complete.

This RFC establishes the central intermediate representation used by the cognitive compiler to analyze, optimize, and generate executable cognitive programs. It provides the structural foundation needed for robust compilation, static analysis, and deterministic execution in Red/Cognition.
