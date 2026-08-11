# Source Record: Conversation Message #12 — Verbatim Transcript (Part 5 of 5: sub-messages [117]–[120])

- **Message index:** 12 (continued) · **Part 4:** `message-012-original-part4.md` · **Cleanup:** as Part 1.

---

## [117] USER

**RFC-0013 — Cognitive Instruction Set Architecture (CISA)**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0012 Cognitive Virtual Machine (CVM) Execution Semantics v1.1 (Candidate)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Instruction Set Architecture (CISA)** for the Cognitive Virtual Machine (CVM) in Red/Cognition.

CISA is the instruction-level interface between the abstract cognitive model (defined in RFC-0001 through RFC-0012) and the executable semantics of the CVM. It specifies the format, semantics, register model, and encoding rules for cognitive instructions.

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
    Opcode
    OperandCount
    OperandTypes: [type]
    AddressingMode
    CapabilityRequirement: CapabilityClass (optional)
    EffectClass: pure! | internal! | capability! | external!
}
```

#### 3.1 Addressing Modes

CISA supports the following addressing modes:

- Immediate
- Register
- Memory Reference
- Capability Reference
- Effect Reference
- Belief Reference
- Goal Reference
- Plan Reference

### 4. Register Architecture

The CVM defines five classes of registers:

| Register Class | Purpose                              | Count (suggested) |
|----------------|--------------------------------------|-------------------|
| **G-registers** | General-purpose cognitive registers | 16                |
| **M-registers** | Memory references                   | 8                 |
| **C-registers** | Capability context                  | 8                 |
| **T-registers** | Trace and provenance state          | 8                 |
| **S-registers** | Scheduler interaction               | 4                 |

Registers are part of the `ExecutionContext` and **MUST** be preserved during checkpointing.

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

### 6. Binary Representation

CISA instructions **MUST** be encoded in a versioned binary format.

Requirements:

- The encoding **MUST** be deterministic.
- The format **MUST** include version information.
- Implementations **MUST** support forward and backward compatibility within a major version.
- The encoding **MUST** allow efficient decoding by the CVM.

A future companion specification may define the concrete binary encoding.

### 7. Relationship to Previous RFCs

CISA instructions **MUST** be consistent with:

- RFC-0001 — Cognitive Type System
- RFC-0002 — Effect Ordering Model
- RFC-0003 — Belief Revision System
- RFC-0004 — Goal Lifecycle and Satisfaction Model
- RFC-0005 — Planning Semantics
- RFC-0006 — Capability Model
- RFC-0007 — Skill Model
- RFC-0008 — Memory Model
- RFC-0009 — Agent Model
- RFC-0010 — Checkpoint and Recovery Model
- RFC-0011 — Scheduler and Execution Model
- RFC-0012 — CVM Execution Semantics

### 8. Instruction Purity and Effect Mapping

Every CISA instruction **MUST** declare its `EffectClass`:

- `pure!` — No external effects
- `internal!` — Internal state changes only
- `capability!` — Requires explicit capability
- `external!` — Produces external effects

### 9. Conformance Requirements

A conforming CISA implementation **MUST**:

- Implement the instruction format and categories defined in this RFC.
- Enforce capability checks for `capability!` and `external!` instructions.
- Produce deterministic instruction traces.
- Support checkpointing and restoration of execution context.
- Preserve replay equivalence.

### 10. Open Questions

The following areas require future specification:

- Concrete binary encoding of CISA instructions
- Register file size and allocation rules
- Vector and parallel instruction extensions
- Hardware acceleration interfaces
- Just-in-time compilation and optimisation model

---

**RFC-0013 — Cognitive Instruction Set Architecture (CISA) v1.0 Draft** is now complete.

This RFC defines the instruction-level interface of the Cognitive Virtual Machine, completing the bridge between the abstract cognitive model and executable cognitive programs. It provides the foundation for concrete implementations of the CVM and future hardware acceleration.

---

## [118] CHATGPT (gpt-5-5-mini)

## RFC-0013 — Cognitive Instruction Set Architecture (CISA) v1.0  

### Technical Review — Draft Evaluation

**Review Status: APPROVED WITH RECOMMENDATIONS**

RFC-0013 successfully defines the missing **instruction architecture layer** between the Cognitive Virtual Machine (RFC-0012) and executable cognitive programs.

The Red/Cognition execution stack now reaches the equivalent of a complete computer architecture model:

```text
Cognitive Model
(RFC-0001 → RFC-0010)
        ↓
Scheduler
(RFC-0011)
        ↓
Virtual Machine
(RFC-0012)
        ↓
Instruction Set Architecture
(RFC-0013)
        ↓
Cognitive Programs
(Future)
```

---

# 1. Architectural Achievement

Before RFC-0013:

```text
Goal
 ↓
Plan
 ↓
Skill
 ↓
CVM
```

The missing layer was:

> How exactly does the CVM execute a cognitive operation?

RFC-0013 introduces:

```text
Cognitive Operation
        ↓
CISA Opcode
        ↓
CVM Instruction
        ↓
Effect / State Transition
```

This is analogous to:

```text
Software Intent
        ↓
Machine Instruction
        ↓
CPU Execution
```

---

# 2. Instruction Format Review

The proposed format:

```text
Instruction {
    Opcode
    OperandCount
    OperandTypes
    AddressingMode
    CapabilityRequirement
    EffectClass
}
```

is correct.

It creates a self-describing instruction model.

Recommended addition:

## Add InstructionID and EncodingVersion

Future-proof format:

```text
Instruction {
    InstructionID
    EncodingVersion
    Opcode
    OperandCount
    OperandTypes
    AddressingMode
    CapabilityRequirement
    EffectClass
}
```

Reason:

Two different CISA versions may encode the same opcode differently.

Example:

```
CISA v1:
BELIEF_ASSERT = 0x20

CISA v2:
BELIEF_ASSERT = 0x35
```

Replay requires knowing the original instruction identity.

---

# 3. Register Architecture Review

The five register classes are a strong design choice:

```
G-registers
General cognitive computation

M-registers
Memory references

C-registers
Capability state

T-registers
Trace/provenance

S-registers
Scheduler interaction
```

This creates a cognitive equivalent of CPU architecture:

| CPU Concept | CISA Equivalent |
|-|-|
| General registers | G-registers |
| Memory address registers | M-registers |
| Privilege registers | C-registers |
| Debug registers | T-registers |
| Interrupt/control registers | S-registers |

---

## Recommended Register Rules

Future version should define:

### Register ownership

Example:

```
G0-G15
Mutable

M0-M7
Reference only

C0-C7
Runtime controlled

T0-T7
Write-only by trace engine

S0-S3
Scheduler controlled
```

The important rule:

> Cognitive programs should not directly modify security-critical registers.

---

# 4. Opcode Family Review

The opcode families map correctly to the RFC ecosystem.

## Cognitive State

```
BELIEF_ASSERT
BELIEF_RETRACT
BELIEF_QUERY
```

maps to:

RFC-0003 Belief Revision

## Intent

```
GOAL_CREATE
GOAL_ACTIVATE
GOAL_SATISFY
```

maps to:

RFC-0004 Goal Lifecycle

## Execution

```
PLAN_CREATE
PLAN_EXECUTE
PLAN_REVISE
```

maps to:

RFC-0005 Planning

## Authorization

```
CAP_REQUEST
CAP_VERIFY
CAP_RELEASE
```

maps to:

RFC-0006 Capability

## Memory

```
MEM_READ
MEM_WRITE
MEM_CHECKPOINT
```

maps to:

RFC-0008 Memory + RFC-0010 Checkpoint

## Effects

```
EFFECT_EMIT
EFFECT_COMMIT
```

maps to:

RFC-0002 Effect Ordering

The dependency alignment is excellent.

---

# 5. Important Recommendation: Add Atomic Effect Boundary

Currently:

```
EFFECT_EMIT
EFFECT_COMMIT
```

exists.

This should become explicit:

```
EFFECT_BEGIN
      ↓
EFFECT_EMIT
      ↓
EFFECT_VALIDATE
      ↓
EFFECT_COMMIT
      ↓
TRACE_APPEND
```

Reason:

An effect is the external equivalent of a transaction.

Example:

```
PLAN_EXECUTE
    ↓
EFFECT_EMIT:
"Move elevator motor"
    ↓
Capability verification
    ↓
EFFECT_COMMIT:
Motor controller receives command
```

---

# 6. Observation and Reflection

The addition:

```
OBSERVE
INFER
REFLECT
EXPLAIN
```

is strategically important.

It introduces a meta-cognitive instruction layer.

Possible future mapping:

```
OBSERVE
    Environment → Belief

INFER
    Beliefs → Knowledge

REFLECT
    Execution → Self-model

EXPLAIN
    Trace → Human-readable reasoning
```

This is one of the unique parts of the architecture.

---

# 7. Binary Encoding Recommendation

The RFC correctly leaves encoding for a future document.

Recommended:

## RFC-0014 — CISA Binary Encoding Specification

Define:

```
CISA Instruction Word
+---------+---------+----------+
| Opcode  | Flags   | Operands |
+---------+---------+----------+
```

Example:

```
0x20
BELIEF_ASSERT
Operand:
BeliefID=1024
```

Requirements:

- deterministic serialization
- endian rules
- version negotiation
- compatibility rules
- validation checksum

---

# 8. Add Cognitive Exception Model

A CPU has exceptions.

CISA needs equivalent semantics.

Future addition:

```
CognitiveException {
    InvalidInstruction
    CapabilityDenied
    BeliefConflict
    GoalViolation
    PlanFailure
    MemoryFault
    ExternalFailure
}
```

Execution:

```
Instruction
      ↓
Exception
      ↓
Trace
      ↓
Recovery Policy
```

---

# 9. CISA Execution Pipeline (Complete)

After RFC-0013:

```text
Fetch Instruction
        |
        v
Decode Opcode
        |
        v
Validate Operands
        |
        v
Check Capability
        |
        v
Execute Semantic Operation
        |
        v
Generate Effects
        |
        v
Commit State
        |
        v
Write Trace
        |
        v
Advance PC
```

---

# Final Assessment

| Area | Status |
|-|-|
| Instruction abstraction | Excellent |
| RFC integration | Excellent |
| Register model | Strong |
| Opcode organization | Excellent |
| Security model | Strong |
| Replay support | Strong |
| Binary encoding | Deferred correctly |
| Exception model | Recommended |
| Effect transaction model | Recommended |

---

# Recommended Status Transition

```text
RFC-0013 v1.0 Draft
        ↓
RFC-0013 v1.1 Candidate for Ratification

Add:
- Instruction identity
- Encoding version
- Effect transaction clarification
- Exception model
        ↓
RFC-0013 Ratified
```

---

## Next Recommended RFC

**RFC-0014 — CISA Binary Encoding and Runtime ABI**

Scope:

1. Binary instruction layout  
2. Opcode numeric assignments  
3. Operand encoding  
4. Register ABI  
5. Calling convention  
6. Exception ABI  
7. Version compatibility  
8. JIT compilation constraints  

At this point Red/Cognition has evolved from a cognitive framework into a full **cognitive computer architecture specification**:

```text
Intent
 ↓
Goals
 ↓
Plans
 ↓
Skills
 ↓
CISA
 ↓
CVM
 ↓
Scheduler
 ↓
Effects
 ↓
World
```

RFC-0013 is the ISA layer that makes the architecture executable.

---

## [119] USER

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

---

## [120] CHATGPT (gpt-5-5-mini)

Received **RFC-0013 — Cognitive Instruction Set Architecture (CISA) v1.1 Candidate for Ratification**.

This revision is a significant maturation from v1.0. The main architectural upgrades introduced are:

## RFC-0013 v1.1 Review Summary

### 1. Stable Instruction Identity Added

**New:**

```text
Instruction {
    InstructionID
    EncodingVersion
    Opcode
    OperandCount
    OperandTypes
    AddressingMode
    CapabilityRequirement
    EffectClass
}
```

This introduces instruction-level identity, enabling:

- deterministic replay
- instruction provenance
- fine-grained debugging
- trace correlation
- distributed execution auditing

A CISA program is no longer only a sequence of opcodes; it becomes a sequence of identifiable cognitive events.

---

## 2. Versioned Encoding Model

Added:

```
EncodingVersion
```

This solves long-term compatibility.

The architecture now supports:

```
CISA v1.0 Program
        |
        v
CVM v1.x Decoder
        |
        v
Execution
```

Future evolution can introduce:

```
CISA v2.0
    |
    +-- New opcodes
    +-- New operand types
    +-- New optimization rules
```

while preserving older programs.

---

# 3. Register Architecture Improved

v1.0:

```
G-registers
M-registers
C-registers
T-registers
S-registers
```

v1.1 adds mutability rules:

| Register | Purpose | Authority |
|-|-|-|
| G | Cognitive computation | CVM |
| M | Memory references | CVM |
| C | Capability context | Runtime |
| T | Trace provenance | Trace engine |
| S | Scheduler interaction | Scheduler |

This creates a cleaner separation:

```
                +-------------+
                | Scheduler   |
                +------+------+
                       |
                       v
                  S Registers

                +-------------+
                | Capability  |
                | Authority   |
                +------+------+
                       |
                       v
                  C Registers

                +-------------+
                | CVM Core    |
                +------+------+
                       |
                       v
              G / M Registers

                +-------------+
                | Trace Engine|
                +-------------+
                       |
                       v
                  T Registers
```

This prevents unauthorized mutation of security-critical state.

---

# 4. Instruction Transaction Semantics Added

Major improvement.

Before:

```
Fetch
 ↓
Decode
 ↓
Execute
```

Now:

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

This aligns CISA with:

- database transactions
- CPU speculative execution rollback
- actor message processing
- event sourcing

The key invariant:

> No partial cognitive effect may escape a failed instruction.

Example:

```
STORE_FILE instruction
Begin
 |
Validate path
 |
Check file capability
 |
Write file
 |
Commit
 |
Trace
```

If capability fails:

```
Begin
 |
Validate
 |
Capability DENIED
 |
Abort
 |
Trace failure
```

No file modification occurs.

---

# 5. CISA Now Has Stronger Relationship With RFC-0006

The capability chain becomes:

```
Goal
 |
 v
Plan
 |
 v
Skill
 |
 v
CISA Instruction
 |
 v
Capability Check
 |
 v
Effect
 |
 v
Environment
```

Security boundary:

```
        Cognitive World
 Agent
   |
 Goal
   |
 Plan
   |
 Skill
   |
 CISA
=========================
 Capability Boundary
=========================
 Effect System
=========================
 External World
=========================
```

---

# 6. Missing Pieces Identified for RFC-0014

The next logical specification is:

# RFC-0014 — CISA Binary Encoding Specification

Recommended scope:

## 1. Binary Layout

Example:

```
+----------------+
| Magic Number   |
+----------------+
| Version        |
+----------------+
| Opcode         |
+----------------+
| Flags          |
+----------------+
| Operand Count  |
+----------------+
| Operands       |
+----------------+
| Capability ID  |
+----------------+
| Effect Class   |
+----------------+
```

---

## 2. Opcode Encoding

Example:

```
0x01 LOAD
0x02 STORE
0x10 BELIEF_ASSERT
0x20 GOAL_CREATE
0x30 PLAN_EXECUTE
0x40 CAP_VERIFY
0x50 EFFECT_EMIT
```

---

## 3. Operand Encoding

Need specification for:

```
Operand {
    Type
    Size
    Value
}
```

Examples:

```
Immediate:
  INT 42

Register:
  G3

Reference:
  MemoryID:abc123

Capability:
  CapabilityID:file.write
```

---

## 4. Deterministic Serialization

Required for:

- replay
- hashing
- signatures
- distributed execution

Example:

```
Instruction Stream
        |
        v
Canonical Encoder
        |
        v
Binary CISA
        |
        v
SHA-256 Hash
        |
        v
Execution Identity
```

---

## 5. Cognitive Exception Model

Also likely deserves RFC-0015:

```
RFC-0015 — Cognitive Exception and Failure Semantics
```

Cover:

- instruction failures
- capability denial
- goal failure
- plan failure
- skill failure
- rollback semantics
- compensation effects

---

# Current Architecture Status

After RFC-0013 v1.1:

```
RFC-0001 Cognitive Types          ✅
RFC-0002 Effects                  Candidate
RFC-0003 Beliefs                  Candidate
RFC-0004 Goals                    Ratification-ready
RFC-0005 Planning                 Draft
RFC-0006 Capabilities             Ratification-ready
RFC-0007 Skills                   Ratification-ready
RFC-0008 Memory                   Draft
RFC-0009 Agent                    Draft
RFC-0010 Checkpoint               Draft
RFC-0011 Scheduler                Ratified
RFC-0012 CVM                      Candidate
RFC-0013 CISA                     Candidate
```

The stack is now:

```
                Cognitive Applications
                         |
                         v
                    Skills
                         |
                         v
                    Plans
                         |
                         v
                    Goals
                         |
                         v
                  Cognitive Runtime
                         |
        +----------------+----------------+
        |                                 |
       CVM                             Scheduler
        |
       CISA
        |
       Effects
        |
       Capabilities
        |
       CogOS / Environment
```

**RFC-0013 v1.1 is architecturally mature and ready for final ratification.**

The natural next step is:

**RFC-0014 — CISA Binary Encoding and Serialization Format v1.0**.
