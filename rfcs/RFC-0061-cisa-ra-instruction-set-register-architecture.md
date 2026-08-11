<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #27, sub-message [299], 2026-08-11
  Verbatim source: knowledge-base/sources/message-027-original-part*.md
  Status in corpus: RFC-0061 CISA-RA v1.2; RATIFIED per final ratification review [300] ("Decision: APPROVED; Status: RATIFIED"). v1.2 text is this USER draft [299]. Earlier v1.0 proposal [286], v1.1 draft [297], v1.1 ratification record [287], and v1.1 review [298] preserved in archive.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->


**RFC-0061 — Cognitive Virtual Machine Instruction Set and Register Architecture (CISA-RA) v1.2**

**Version:** 1.2  

**Status:** Candidate for Final Ratification  

**Parent:** RFC-0060 Cognitive Virtual Machine Instruction Execution and Scheduling Semantics (CVM-IESS) v1.1 (Candidate)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Virtual Machine Instruction Set and Register Architecture (CISA-RA)** for Red/Cognition.

RFC-0013 defines the Cognitive Instruction Set Architecture (CISA) conceptually. RFC-0060 defines how instructions execute inside the Cognitive Virtual Machine.

This specification defines the concrete machine-level model:

- Register architecture

- Operand model

- Instruction encoding

- Opcode classes

- Execution semantics

- Memory interaction

- Effect generation interface

CISA-RA establishes the hardware-neutral instruction foundation for all conforming CVM implementations.

```

Cognitive Program

   ↓

CIR / CISA Representation

   ↓

CISA Instruction Encoding

   ↓

CVM Register Machine

   ↓

RFC-0060 Execution Engine

   ↓

Transactions + Security

```

### 2. Design Principles

CISA-RA follows these principles:

- **Deterministic Execution** — Identical instruction streams **MUST** produce identical machine state transitions.

- **Explicit State** — All computational state **MUST** be represented explicitly (registers, memory references, execution context, transaction context). Hidden mutable state is prohibited.

- **Capability-Aware Instructions** — Instructions capable of producing external effects **MUST** declare required capability, effect class, and security level.

- **Replay Compatibility** — Instruction execution **MUST** be reconstructable from bytecode, register state, memory state, scheduler epoch, and transaction state.

### 3. CVM Machine Model

A CVM instance consists of:

```

CVM {

    Register File,

    Operand Stack,

    Local Memory,

    Shared Memory Interface,

    Effect Buffer,

    Transaction Context,

    Security Context,

    Trace Context

}

```

### 4. Register Architecture

A CVM **MUST** provide the following logical registers.

#### 4.1 General Purpose Registers

`R0–R31` — 32 general-purpose registers.

Each register:

```

Register {

    Type,

    Value,

    Version,

    Provenance

}

```

#### 4.2 Special Registers

| Register | Purpose                  | Authority          |

|----------|--------------------------|--------------------|

| **PC**   | Program Counter          | CVM                |

| **SP**   | Stack Pointer            | CVM                |

| **FP**   | Frame Pointer            | CVM                |

| **TX**   | Transaction Context      | Runtime            |

| **CAP**  | Capability Context       | Runtime            |

| **TRACE**| Trace Cursor             | Trace Engine       |

| **EPOCH**| Scheduler Epoch          | Scheduler          |

| **FLAGS**| Execution Flags          | CVM                |

#### 4.3 Cognitive Registers

CISA introduces specialized cognitive registers:

- **Belief Registers** `BR0–BR7`) — References to belief state.

- **Goal Registers** `GR0–GR7`) — References to active goals.

- **Memory Registers** `MR0–MR7`) — Handles to semantic/episodic memory.

### 5. Operand Model

CISA operands support:

- Immediate

- Register

- Memory Reference

- Constant Pool

- Capability Handle

- Effect Reference

- Belief Reference

- Goal Reference

- Plan Reference

Example:

```

ADD R1, R2, R3     ; R1 = R2 + R3

```

### 6. Instruction Encoding

Default encoding:

```

+------------+

| Opcode     | 2 bytes

+------------+

| Flags      | 2 bytes

+------------+

| Operand A  |

+------------+

| Operand B  |

+------------+

| Operand C  |

+------------+

| Metadata   |

+------------+

```

All fields use:

- Little-endian encoding

- Deterministic ordering

- Explicit lengths

- No padding

### 7. Opcode Classes

CISA opcodes are grouped into families:

| Range          | Class          |

|----------------|----------------|

| 0x0000–0x00FF  | Control        |

| 0x0100–0x01FF  | Arithmetic     |

| 0x0200–0x02FF  | Memory         |

| 0x0300–0x03FF  | Cognitive      |

| 0x0400–0x04FF  | Goal           |

| 0x0500–0x05FF  | Planning       |

| 0x0600–0x06FF  | Communication  |

| 0x0700–0x07FF  | Transaction    |

| 0x0800–0x08FF  | Security       |

| 0xFF00–0xFFFF  | Experimental   |

### 8. Core Instruction Set (Examples)

**Control Family**

- `NOP`, `HALT`, `YIELD`, `CALL`, `RETURN`, `JUMP`, `BRANCH`

**Arithmetic Family**

- `ADD`, `SUB`, `MUL`, `DIV`, `COMPARE`, `HASH`

**Memory Family**

- `LOAD`, `STORE`, `ALLOC`, `FREE`, `READ`, `WRITE`

**Cognitive Family**

- `BELIEF_ASSERT`, `BELIEF_QUERY`, `MEMORY_RECALL`, `INFER`, `OBSERVE`

**Goal Family**

- `GOAL_CREATE`, `GOAL_UPDATE`, `GOAL_CHECK`, `GOAL_COMPLETE`

**Transaction Family**

- `TX_BEGIN`, `EFFECT_EMIT`, `TX_COMMIT`, `TX_ABORT`, `TX_COMPENSATE`

**Security Family**

- `CAP_VERIFY`, `IDENTITY_VERIFY`, `POLICY_EVAL`, `ATTEST`

### 9. Effect Model

Effect-producing instructions **MUST** emit:

```

EffectDescriptor {

    EffectID,

    InstructionID,

    CapabilityRequired,

    TransactionID,

    DeterminismClass,

    CompensationHandler

}

```

Effects are buffered until transaction commit.

### 10. Memory Model

CISA defines three logical memory spaces:

- **Local Memory** — No transaction required

- **Working Memory** — Transaction optional

- **Shared Memory** — Transaction required

### 11. Instruction Verification

Before execution:

```

Decode

   ↓

Opcode Validation

   ↓

Operand Validation

   ↓

Capability Check

   ↓

Transaction Check

   ↓

Execute

```

Invalid instructions **MUST** generate `InstructionVerificationFailed`.

### 12. Debug and Introspection Model

A CVM **SHOULD** expose:

```

cog cvm inspect

cog cvm registers

cog cvm trace

cog cvm disassemble

cog cvm replay

```

### 13. Conformance Profiles

| Profile      | Capability                              |

|--------------|-----------------------------------------|

| **Minimal**  | Core register VM                        |

| **Developer**| Full CISA execution                     |

| **Professional** | Transaction-aware VM                |

| **Enterprise** | Secure distributed CVM               |

| **Verified** | Formal instruction verification       |

### 14. Relationship to Existing RFCs

CISA-RA integrates with RFC-0011, RFC-0012, RFC-0013, RFC-0028, RFC-0057, RFC-0058, RFC-0059, and RFC-0060.

### 15. Open Questions

Future specifications:

- Complete opcode table with numeric assignments

- Formal bytecode verifier

- Register typing rules

- Vector/tensor instruction extensions

- Formal semantics in a theorem prover (e.g., Lean 4)

---

**RFC-0061 — Cognitive Virtual Machine Instruction Set and Register Architecture (CISA-RA) v1.2** is now ready for **Final Ratification Review**.

This version incorporates a register type system, formal instruction header, operand encoding, instruction purity classification, opcode registry, bytecode verification model, memory consistency clarification, and cognitive instruction examples, bringing it in line with the precision of the strongest RFCs in the series.
