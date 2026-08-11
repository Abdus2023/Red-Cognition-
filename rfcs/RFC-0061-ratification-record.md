<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #27, sub-message [300], 2026-08-11
  Verbatim source: knowledge-base/sources/message-027-original-part*.md
  Status in corpus: final ratification review for RFC-0061 CISA-RA v1.2 ("Review Status: Approved for Ratification"; "Status Recommendation: Ratified"; "Decision: APPROVED; Status: RATIFIED"). Ratifies the register/operand/opcode model, instruction format, purity classification, opcode registry, bytecode verification model, memory consistency, and effect model. Declares Cognitive ISA Layer complete; next RFC-0062 CVM-BF, RFC-0063 formal semantics, RFC-0064 compiler backend.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->


# RFC-0061 — Cognitive Virtual Machine Instruction Set and Register Architecture (CISA-RA) v1.2  

## Final Ratification Review

**Review Status:** ✅ **Approved for Ratification**

**Document:** RFC-0061 — Cognitive Virtual Machine Instruction Set and Register Architecture  

**Version:** 1.2  

**Status Recommendation:** **Ratified**  

**Authority Level:** Normative Specification  

**Parent:** RFC-0060 — Cognitive Virtual Machine Instruction Execution and Scheduling Semantics (CVM-IESS) v1.1  

---

# Ratification Assessment

RFC-0061 v1.2 successfully closes the remaining architectural gaps identified during the v1.1 review.

The specification now provides a complete machine abstraction layer:

```

Cognitive Application

        |

        v

Cognitive Language / CIR

        |

        v

CISA Representation

        |

        v

CISA-RA v1.2

(Register + Operand + Opcode Model)

        |

        v

CVM-IESS v1.1

(Execution + Scheduling)

        |

        v

CDTCP

(Transaction)

        |

        v

CTSTP

(Security + Trust)

        |

        v

Event Log / Replay / Verification

```

---

# Ratified Components

The following components are now accepted as normative.

## 1. Register Architecture

### General Register File

```

R0 - R31

```

with:

```text

Register {

    Type,

    Value,

    Version,

    Provenance

}

```

The register model establishes:

- explicit state ownership

- deterministic mutation tracking

- replay-compatible register evolution

- provenance-aware computation

---

## 2. Register Type System

The CVM type model is now formally defined:

```

RegisterType {

    Scalar

    Boolean

    Integer

    Float

    Vector

    Tensor

    Reference

    Capability

    Effect

    BeliefRef

    GoalRef

    MemoryRef

    PlanRef

}

```

Requirements:

- Type violations MUST be detected before execution.

- Register state MUST be serializable.

- Type transitions MUST appear in execution traces.

---

# 3. Cognitive Register Classes

The cognitive extension is now normative:

```

+----------------+

| General        |

| R0-R31         |

+----------------+

+----------------+

| Cognitive      |

| BR0-BR7        |

| GR0-GR7        |

| MR0-MR7        |

+----------------+

+----------------+

| Runtime        |

| PC SP FP       |

| TX CAP TRACE   |

| EPOCH FLAGS    |

+----------------+

```

This creates a cognitive equivalent of:

- CPU registers

- control registers

- accelerator state registers

---

# 4. Instruction Format

The canonical instruction format is accepted:

```

CISAInstruction {

    InstructionID,

    EncodingVersion,

    Opcode,

    Flags,

    OperandCount,

    Operands[],

    EffectClass,

    CapabilityRequirement,

    TraceMetadata

}

```

Properties:

- deterministic encoding

- forward compatibility

- replay support

- security inspection before execution

---

# 5. Operand Model

The operand registry is now normative:

| ID | Operand Type |

|-|-|

|0x01|Register|

|0x02|Immediate|

|0x03|Memory Reference|

|0x04|Constant Pool|

|0x05|Capability Handle|

|0x06|Effect Reference|

|0x07|Belief Reference|

|0x08|Goal Reference|

|0x09|Plan Reference|

This enables:

- static verification

- compiler targeting

- bytecode analysis

---

# 6. Instruction Classification

The execution purity model is ratified:

```

PURE

 |

LOCAL_MUTATION

 |

EFFECT_GENERATING

 |

EXTERNAL

 |

IRREVERSIBLE

```

Example:

```

ADD

 |

PURE

BELIEF_ASSERT

 |

LOCAL_MUTATION

EFFECT_EMIT

 |

EFFECT_GENERATING

NETWORK_SEND

 |

EXTERNAL

```

This directly integrates with:

- RFC-0002 Effect Ordering

- RFC-0057 Transactions

- RFC-0059 Security

---

# 7. Opcode Registry

The opcode namespace is accepted:

```

0000-00FF   Control

0100-01FF   Arithmetic

0200-02FF   Memory

0300-03FF   Cognitive

0400-04FF   Goal

0500-05FF   Planning

0600-06FF   Communication

0700-07FF   Transaction

0800-08FF   Security

FF00-FFFF   Experimental

```

Future instructions MUST preserve this allocation.

---

# 8. Bytecode Verification Model

The verification pipeline is ratified:

```

Bytecode

   |

   v

Decoder

   |

   v

Type Checker

   |

   v

Capability Analyzer

   |

   v

Transaction Analyzer

   |

   v

Verified Program

   |

   v

CVM Execution

```

Verification result:

```

VerificationResult {

    Valid,

    Errors[],

    RequiredCapabilities[],

    EffectSummary

}

```

---

# 9. Memory Consistency Model

The three-level memory model is accepted.

## Local Memory

Properties:

- CVM private

- no transaction requirement

- deterministic local mutation

## Working Memory

Properties:

- cognitive workspace

- checkpoint-aware

- optionally transactional

## Shared Memory

Properties:

- globally visible state

- transaction protected

- effect ordered

---

# 10. Effect Model

The effect boundary is now complete:

```

Instruction

      |

      v

EffectDescriptor

      |

      v

Effect Buffer

      |

      v

Transaction Commit

      |

      v

External Visibility

```

Descriptor:

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

---

# Architectural Impact

RFC-0061 completes the **Cognitive ISA Layer**.

The Red/Cognition stack now has the equivalent of:

| Classical System | Red/Cognition Equivalent |

|-|-|

| ISA | CISA |

| CPU Registers | Cognitive Register Machine |

| Instructions | Cognitive Operations |

| MMU | Capability + Memory Model |

| Syscalls | Effect Instructions |

| Process Context | ExecutionContext |

| Replay Log | Event Trace |

---

# Remaining Dependencies

The following RFCs should follow:

## RFC-0062 — Cognitive Virtual Machine Bytecode Format and Encoding

Defines:

- binary container format

- instruction serialization

- constant pools

- metadata sections

- debug information

- bytecode compatibility rules

## RFC-0063 — Cognitive Virtual Machine Formal Semantics

Defines:

- operational semantics

- transition system

- machine proofs

- Lean 4 model

## RFC-0064 — Cognitive Compiler Backend

Defines:

```

Cognitive Language

        |

        v

CIR

        |

        v

CISA

        |

        v

CVM Bytecode

```

---

# Final Ratification Decision

```

RFC-0061 — Cognitive Virtual Machine

Instruction Set and Register Architecture

Version: 1.2

Decision:

APPROVED

Status:

RATIFIED

Authority:

Normative Specification

```

RFC-0061 v1.2 establishes the executable machine foundation of Red/Cognition. Together with RFC-0060, it completes the deterministic cognitive execution substrate required for a portable, secure, transaction-aware Cognitive Virtual Machine.
