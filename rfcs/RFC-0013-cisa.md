<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #12, sub-message [119], 2026-08-10
  Verbatim source: knowledge-base/sources/message-012-original-part*.md
  Status in corpus: RFC-0013 Cognitive Instruction Set Architecture (CISA) v1.1 (Candidate for Ratification); review [120] deems it architecturally mature and ready for final ratification. Ratification record not present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0013 — Cognitive Instruction Set Architecture (CISA)**

**Version:** 1.1  

**Status:** Candidate for Ratification  

**Parent:** RFC-0012 Cognitive Virtual Machine (CVM) Execution Semantics v1.1 (Candidate)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Instruction Set Architecture (CISA)** for the Cognitive Virtual Machine (CVM) in Red/Cognition.

CISA is the instruction-level interface between the abstract cognitive model and the executable semantics of the CVM. It specifies the format, semantics, register model, and encoding rules for cognitive instructions.

### 2. Design Principles

CISA follows these core principles:

- **Determinism** — Every instruction must produce reproducible results given the same inputs and execution context.
- **Traceability** — Every instruction execution must be fully traceable.
- **Capability Awareness** — Instructions that may produce external effects must declare capability requirements.
- **Provider Neutrality** — CISA defines *what* operations are performed, not *how* reasoning or planning is implemented.
- **Replay Equivalence** — Instruction sequences must be replayable while preserving observable behaviour.
- **Simplicity** — The instruction set should remain minimal while expressive enough to represent cognitive operations.

### 3. Instruction Format

Every CISA instruction **MUST** conform to the following structure:

```
Instruction {
    InstructionID
    EncodingVersion
    Opcode
    OperandCount
    OperandTypes: [type]
    AddressingMode
    CapabilityRequirement: CapabilityClass (optional)
    EffectClass: pure! | internal! | capability! | external!
}
```

- `InstructionID` provides a stable identity for each individual instruction instance.
- `EncodingVersion` enables forward and backward compatibility between CISA revisions.

### 4. Register Architecture

The CVM defines five classes of registers:

| Register Class | Purpose                              | Suggested Count | Mutability                  |
|----------------|--------------------------------------|-----------------|-----------------------------|
| **G-registers** | General-purpose cognitive registers | 16              | Mutable                     |
| **M-registers** | Memory references                   | 8               | Reference only              |
| **C-registers** | Capability context                  | 8               | Runtime controlled          |
| **T-registers** | Trace and provenance state          | 8               | Write-only by trace engine  |
| **S-registers** | Scheduler interaction               | 4               | Scheduler controlled        |

### 5. Opcode Families

CISA organizes instructions into the following families:

#### 5.1 Data Movement

- `LOAD`, `STORE`, `MOVE`, `SWAP`

#### 5.2 Belief Operations

- `BELIEF_ASSERT`, `BELIEF_RETRACT`, `BELIEF_QUERY`, `BELIEF_UPDATE`

#### 5.3 Goal Operations

- `GOAL_CREATE`, `GOAL_ACTIVATE`, `GOAL_SATISFY`, `GOAL_FAIL`, `GOAL_ARCHIVE`

#### 5.4 Plan Operations

- `PLAN_CREATE`, `PLAN_VALIDATE`, `PLAN_EXECUTE`, `PLAN_REVISE`, `PLAN_ABORT`

#### 5.5 Memory Operations

- `MEM_READ`, `MEM_WRITE`, `MEM_APPEND`, `MEM_CHECKPOINT`, `MEM_RESTORE`

#### 5.6 Capability Operations

- `CAP_REQUEST`, `CAP_RELEASE`, `CAP_VERIFY`

#### 5.7 Effect Operations

- `EFFECT_EMIT`, `EFFECT_COMMIT`

#### 5.8 Control Flow

- `BRANCH`, `JUMP`, `CALL`, `RETURN`, `YIELD`

#### 5.9 Observation and Reflection

- `OBSERVE`, `INFER`, `REFLECT`, `EXPLAIN`

### 6. Instruction Transaction Model

Every instruction executes as an atomic transaction:

```
Begin
   ↓
Validate
   ↓
Capability Check
   ↓
Execute
   ↓
Generate Effects
   ↓
Commit
   ↓
Trace
```

On failure, the transaction aborts with no partial effects committed.

### 7. Instruction Purity and Effect Mapping

Every instruction **MUST** declare its `EffectClass`:

- `pure!`
- `internal!`
- `capability!`
- `external!`

### 8. Binary Representation

CISA instructions **MUST** be encoded in a versioned binary format.

Requirements:

- The encoding **MUST** be deterministic.
- The format **MUST** include version information.
- Implementations **MUST** support forward and backward compatibility within a major version.

A future companion specification (RFC-0014) will define the concrete binary encoding.

### 9. Relationship to Previous RFCs

CISA instructions **MUST** be consistent with RFC-0001 through RFC-0012.

### 10. Conformance Requirements

A conforming CISA implementation **MUST**:

- Implement the instruction format and categories defined in this RFC.
- Enforce capability checks for `capability!` and `external!` instructions.
- Produce deterministic instruction traces.
- Support checkpointing and restoration of execution context.
- Preserve replay equivalence.

### 11. Open Questions

The following areas require future specification:

- Concrete binary encoding of CISA instructions (RFC-0014)
- Register file size and allocation rules
- Vector and parallel instruction extensions
- Hardware acceleration interfaces
- Just-in-time compilation and optimisation model
- Cognitive exception model

---

**RFC-0013 — Cognitive Instruction Set Architecture (CISA) v1.1** is now ready for **Final Ratification Review**.
