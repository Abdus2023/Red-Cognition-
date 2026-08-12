<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #5, sub-message [53], 2026-08-10
  Verbatim source: knowledge-base/sources/message-005-original-part*.md
  Status in corpus: RC-300 Compiler Specification v1.1 (Candidate for Ratification); review [54] APPROVED FOR RATIFICATION; ratification record not present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates specs/ for specifications.
  Content below is the document text exactly as provided (no edits).
-->

**RC-300 Compiler Specification**

**Version:** 1.1  

**Status:** Candidate for Ratification  

**Parent:** RC-200 Language Specification v1.0 (Ratified)  

**Authority:** Normative Specification  

**Date:** 2026-07-29

---

### 1. Introduction

RC-300 defines the compiler architecture for Red/Cognition. It specifies how the compiler processes Red source code, integrates cognitive constructs, generates intermediate representations, and produces executable output while maintaining compatibility with Red and the architectural principles defined in RC-000 and RC-100.

This specification is normative. It defines *compiler behaviour and responsibilities*, not implementation mechanisms.

### 2. Compiler Philosophy

The Red/Cognition compiler follows a core principle:

**The compiler must compile cognition without becoming a cognitive engine.**

This means:

- The compiler analyses and transforms cognitive constructs.
- The Cognitive Runtime executes cognitive behaviour.
- The compiler does not embed intelligence providers.
- The compiler remains deterministic and reproducible.

### 3. Compiler Architectural Position

The compiler exists primarily between:

```
Source Language Layer
           │
           ▼
Red/Cognition Compiler
           │
           ▼
Runtime Layers (Red Runtime + Cognitive Runtime + Cognitive VM)
```

The compiler:

- **MUST NOT** own runtime state.
- **MUST NOT** execute cognitive decisions.
- **MUST NOT** contain agent memory.
- **MUST NOT** perform planning.
- **MUST NOT** depend on external intelligence providers.

**Compiler responsibility:** Transform intentional programs into executable representations while preserving semantic transparency.

### 4. Compiler Component Model

The compiler is structured into replaceable subsystems:

```
Compiler Kernel
   ├── Frontend
   ├── Analysis
   └── Backend
```

Each component **MUST** expose stable interfaces according to the Layer Interface Contract Model (LICM) defined in RC-100.

### 5. Source Representation Contract

The compiler **MUST** preserve:

- Original block structure
- Source locations
- Symbol identity
- Dialect boundaries
- Macro expansion history

The compiler **MUST** support traceability between every stage:

```
Source
   ↓
AST
   ↓
Expanded AST
   ↓
IR
```

### 6. Dual IR Pipeline

The compiler defines three intermediate representations:

```
Red AST
   │
   ├── Red IR          (standard Red computation)
   │
   └── Cognitive IR    (goals, plans, beliefs, effects)
           │
           ▼
     Unified IR
```

The **Cognitive Intermediate Representation (CIR)** **MUST** represent:

- Goals (with constraints, priorities, deadlines, capabilities, effects)
- Plans (with steps, dependencies, preconditions)
- Beliefs (with propositions, confidence, provenance, timestamp)
- Effects (with type, target, strength)

CIR **MUST** remain:

- Deterministic
- Serializable
- Inspectable
- Replayable

### 7. Compilation Determinism Model

The compiler supports the following determinism levels:

| Level | Meaning                              | Requirement                     |
|-------|--------------------------------------|---------------------------------|
| D0    | Best effort                          | Default                         |
| D1    | Reproducible compilation             | Identical input → identical output |
| D2    | Bit-identical output                 | Stronger reproducibility        |
| D3    | Verified deterministic compilation   | Formally verified               |

A conforming implementation **MUST** declare its supported determinism level.

### 8. Dialect Compiler Protocol (DCP)

Every cognitive dialect **SHOULD** provide:

- Parser
- Validator
- Lowering Rules
- Type Rules
- Effect Rules
- Metadata Generator

### 9. Compilation Security Rules

The compiler **MUST NOT**:

- Execute generated plans
- Access agent capabilities
- Modify external state
- Invoke autonomous actions

The compiler **MAY**:

- Validate capability requirements
- Simulate static properties
- Generate verification metadata

### 10. Cognitive Compilation Pipeline

The cognitive compilation pipeline consists of:

1. Cognitive Block Detection
2. Dialect Lowering
3. Intent Analysis
4. Effect Extraction
5. Capability Analysis
6. Trace Instrumentation
7. Macro Expansion
8. Optimization
9. Backend Code Generation

### 11. Runtime Interface Generation

The compiler **MUST** generate the necessary metadata for the Cognitive Runtime, including:

- Cognitive IR representation
- Declared effects and required capabilities
- Checkpoint metadata
- Execution trace schema

### 12. Backend Architecture

The compiler supports multiple backends:

- Red/System native code generation
- Red bytecode targets
- Cognitive Virtual Machine targets
- Future hardware acceleration targets

All backends **MUST** preserve the semantics defined in RC-200.

### 13. Red Compatibility Boundary

The compiler **MUST** guarantee that:

- All valid Red 1.x programs compile without modification.
- Cognitive features are strictly additive.
- No existing Red semantics are altered by cognitive compilation paths.

### 14. Architecture Decision Records

**ADR-0003 — Dual Representation Compiler Architecture**  

**Status:** Accepted

**Decision:** Red/Cognition adopts separated Red IR and Cognitive IR pipelines connected through a Unified IR boundary.

**ADR-0004 — Compiler/Cognition Separation**  

**Status:** Accepted

**Decision:** The compiler transforms cognitive structures but does not execute cognition.

### 15. Open Questions

The following areas are deferred to future RFCs or specifications:

- Concrete definition of the Cognitive IR format
- Formal effect ordering semantics (RFC-0002)
- Static verification of cognitive properties
- Cognitive type inference rules
- Compiler plugin and dialect extension model

---

**RC-300 Compiler Specification v1.1** is now ready for **Ratification Review**.
