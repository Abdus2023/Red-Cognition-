<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #32, sub-message [377], 2026-08-12
  Verbatim source: knowledge-base/sources/message-032-original-part5.md
  Status in corpus: RFC-0062 CVM-BF v1.3 (Candidate for Final Ratification). Message-#32 lineage: v1.0 [371] (re-presentation of the v1.0 body with Date 2026-07-29 and compact rendering — D-103 vs [303]/[288]/[302]) → v1.1 [373] (same version label as the previously scaffolded msg#29 [304] but a different body — same-label divergence, D-103) → v1.2 [375] (typed header fields, SectionEntry with SHA-256 hashes) → v1.3 [377] (Section Directory sorted by SectionID; identical re-send [379] — D-104). Reviews [372]/[374]/[376]/[378]; final ratification review [380] (CHATGPT gpt-5-5-mini): "Ratification Recommendation: ACCEPT" pending five amendments (IntegrityBlock structure, Constant encoding, section collision/overlap rules, loader validation sequence, version compatibility semantics). Subsequently RATIFIED per USER ratification record [381] (msg#33; Status: Ratified), scaffolded at RFC-0062-ratification-record.md; the ratification postdates this scaffold provenance's original message (#32), which is updated here at deep audit suite #8. Supersedes the [304]-based scaffold of msg#29 (magic CVMX retained; earlier CVMB variant [288] — C-18). Source quirk preserved as received: [380] heading "8. Loading Validation Pipeline — Approved with clarification**" stray bold-marker mismatch.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->



**RFC-0062 — Cognitive Virtual Machine Bytecode Format and Encoding (CVM-BF) v1.3**

**Version:** 1.3  
**Status:** Candidate for Final Ratification  
**Parent:** RFC-0061 — Cognitive Virtual Machine Instruction Set and Register Architecture (CISA-RA) v1.2 (Ratified)  
**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Virtual Machine Bytecode Format and Encoding (CVM-BF)** for Red/Cognition.

RFC-0061 establishes the abstract machine model of CISA (register architecture, operand model, opcode families, and instruction semantics). This specification defines the concrete executable representation required for portable, deterministic, and verifiable execution across all conforming Cognitive Virtual Machine (CVM) implementations.

CVM-BF enables:

- Storage and distribution of compiled cognitive programs
- Deterministic hashing and signing of bytecode
- Checkpointing and replay of execution state
- Hardware-agnostic execution
- Integration with the Cognitive Runtime and Cognitive Operating System

```
Cognitive Program
   ↓
CIR (RFC-0028)
   ↓
CISA Instructions (RFC-0013 + RFC-0061)
   ↓
CVM Bytecode (RFC-0062)
   ↓
CVM Execution (RFC-0060)
   ↓
Transactions + Security (RFC-0057 + RFC-0059)
```

### 2. Design Principles

CVM-BF follows these principles:

- **Deterministic Encoding** — The same CISA program must always produce an identical byte sequence.
- **Hardware Neutrality** — Bytecode must not depend on CPU architecture, operating system, or native ABI.
- **Verification First** — Bytecode must contain sufficient metadata for validation, capability analysis, security checks, and replay.
- **Forward Compatibility** — The format must support opcode and metadata extensions while preserving backward compatibility within major versions.
- **Traceability** — All serialization must preserve provenance and support deterministic replay.

### 3. CVM Bytecode Container Format

A CVM bytecode image **MUST** follow this structure:

```
+----------------------------+
| Magic                      |  "CVMX"
+----------------------------+
| Format Version             |
+----------------------------+
| Target CVM Version         |
+----------------------------+
| Flags                      |
+----------------------------+
| Module Identifier          |
+----------------------------+
| Section Directory          |
+----------------------------+
| Sections                   |
+----------------------------+
| Integrity Block            |
+----------------------------+
```

### 4. Magic Header

The first four bytes **MUST** contain the magic number:

```
0x43564D58   →   ASCII: CVMX
```

Readers **MUST** reject files with an invalid magic value.

### 5. Header Schema

```
CVMHeader {
    MagicNumber (4 bytes),
    FormatVersion (2 bytes),
    MinimumRuntimeVersion (2 bytes),
    ModuleID (16 bytes, UUID128),
    Flags (4 bytes),
    SectionCount (2 bytes),
    EntryPoint (8 bytes),
    IntegrityHash (32 bytes, SHA-256)
}
```

### 6. Section Directory

The Section Directory **MUST** contain one entry per section, sorted by `SectionID` in ascending order:

```
SectionEntry {
    SectionID (2 bytes),
    Offset (8 bytes),
    Length (4 bytes),
    Flags (2 bytes),
    Hash (32 bytes, SHA-256)
}
```

### 7. Instruction Binary Format

Each instruction **MUST** be encoded as:

```
+------------+
| Opcode     | 2 bytes (uint16)
+------------+
| Flags      | 2 bytes (uint16)
+------------+
| InstructionID | 8 bytes (uint64)
+------------+
| EffectClass | 1 byte (uint8)
+------------+
| CapabilityID | 4 bytes (uint32, optional)
+------------+
| OperandCount | 1 byte (uint8)
+------------+
| Operands   | variable
+------------+
```

### 8. Opcode Registry

CISA opcodes are allocated in the following ranges:

| Range          | Family          |
|----------------|-----------------|
| 0x0000–0x00FF  | Control         |
| 0x0100–0x01FF  | Arithmetic      |
| 0x0200–0x02FF  | Memory          |
| 0x0300–0x03FF  | Cognitive       |
| 0x0400–0x04FF  | Goal            |
| 0x0500–0x05FF  | Planning        |
| 0x0600–0x06FF  | Communication   |
| 0x0700–0x07FF  | Transaction     |
| 0x0800–0x08FF  | Security        |
| 0xFF00–0xFFFF  | Experimental    |

### 9. Initial Opcode Assignments (Examples)

**Control Family**

- `0x0000` — `NOP`
- `0x0001` — `HALT`
- `0x0002` — `YIELD`
- `0x0003` — `CALL`
- `0x0004` — `RETURN`
- `0x0005` — `JUMP`
- `0x0006` — `BRANCH`

**Arithmetic Family**

- `0x0100` — `ADD`
- `0x0101` — `SUB`
- `0x0102` — `MUL`
- `0x0103` — `DIV`
- `0x0104` — `COMPARE`
- `0x0105` — `HASH`

**Cognitive Family**

- `0x0300` — `BELIEF_ASSERT`
- `0x0301` — `BELIEF_QUERY`
- `0x0302` — `MEMORY_RECALL`
- `0x0303` — `INFER`
- `0x0304` — `OBSERVE`

**Transaction Family**

- `0x0700` — `TX_BEGIN`
- `0x0701` — `EFFECT_EMIT`
- `0x0702` — `TX_COMMIT`
- `0x0703` — `TX_ABORT`
- `0x0704` — `TX_COMPENSATE`

### 10. Operand Encoding

Operands are encoded as:

```
Operand {
    Type (1 byte),
    Length (2 bytes),
    Value (variable)
}
```

Supported operand types:

| Type | Meaning                    |
|------|----------------------------|
| 0x01 | Register                   |
| 0x02 | Immediate                  |
| 0x03 | Memory Reference           |
| 0x04 | Constant Pool Reference    |
| 0x05 | Capability Handle          |
| 0x06 | Effect Reference           |
| 0x07 | Belief Reference           |
| 0x08 | Goal Reference             |
| 0x09 | Plan Reference             |

### 11. Constant Pool

The constant pool stores immutable values used by the program:

```
ConstantPool {
    Count,
    Constants[]
}
```

Supported constant types include integers, floats, strings, hashes, symbols, and type descriptors.

### 12. Capability and Effect Manifests

Every bytecode module **MUST** declare:

- Required capabilities
- Declared effects and their classes
- Resource estimates

These manifests are used by the runtime for capability verification and policy evaluation before execution.

### 13. Verification Metadata

The verification section **SHOULD** contain:

```
VerificationInfo {
    TypeSafetyHash,
    ControlFlowHash,
    CapabilityRequirements,
    EffectSummary,
    CompilerSignature
}
```

### 14. Debug Information

An optional debug section **MAY** contain:

```
DebugInfo {
    SourceMap,
    InstructionLocations,
    SymbolTable,
    RegisterNames
}
```

### 15. Serialization Rules

CVM-BF serialization **MUST** use:

- Little-endian byte order
- Deterministic field ordering
- Explicit length prefixes
- No padding
- Canonical hashing for reproducibility

### 16. Security Requirements

Before loading bytecode, the CVM **MUST**:

1. Verify the magic number and format version.
2. Validate the integrity hash and optional signature.
3. Confirm all declared capabilities are available.
4. Verify that the bytecode is compatible with the target CVM and CISA revision.

Unsigned or invalid bytecode **MUST NOT** execute in secure or verified profiles.

### 17. Replay Compatibility

A conforming CVM-BF implementation **MUST** allow reconstruction of execution from:

- Bytecode image
- Initial register state
- Memory state
- Scheduler epoch
- Transaction context
- Security context

### 18. Conformance Profiles

| Profile      | Capability                                      |
|--------------|-------------------------------------------------|
| **Minimal**  | Load and execute verified bytecode              |
| **Developer**| Debug metadata + introspection                  |
| **Professional** | Transaction-aware modules                   |
| **Enterprise** | Signed and attested bytecode                |
| **Verified** | Formal proof metadata                           |

### 19. Relationship to Other RFCs

CVM-BF integrates with:

- RFC-0011 — Scheduler
- RFC-0012 — CVM Execution Semantics
- RFC-0013 — CISA
- RFC-0018 — Event Replay
- RFC-0028 — CIR
- RFC-0057 — CDTCP
- RFC-0058 — CTWP
- RFC-0059 — CTSTP
- RFC-0060 — CVM-IESS
- RFC-0061 — CISA-RA

### 20. Open Questions

Future specifications may address:

- Compressed bytecode formats
- Signed and attested bytecode packages
- Formal bytecode verifier specification
- WASM interoperability layer
- GPU/NPU instruction extensions
- Proof-carrying cognitive bytecode

---

**RFC-0062 — Cognitive Virtual Machine Bytecode Format and Encoding (CVM-BF) v1.3** is now ready for **Final Ratification Review**.

This version incorporates a complete container format, explicit section directory with integrity hashes, instruction encoding, opcode registry, operand encoding, capability and effect manifests, verification metadata, debug information, deterministic serialization rules, security requirements, replay compatibility, and conformance profiles, bringing it in line with the precision of the strongest RFCs in the series.
