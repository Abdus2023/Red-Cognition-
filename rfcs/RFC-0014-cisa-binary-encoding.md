<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #14, sub-message [121], 2026-08-10
  Verbatim source: knowledge-base/sources/message-014-original-part*.md
  Status in corpus: RFC-0014 CISA Binary Encoding and Serialization Format v1.0 (Draft); review [122] coherent, establishes executable binary foundation; no ratification in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0014 — CISA Binary Encoding and Serialization Format**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0013 Cognitive Instruction Set Architecture (CISA) v1.1 (Candidate)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the concrete binary encoding, serialization rules, and version compatibility requirements for the Cognitive Instruction Set Architecture (CISA) defined in RFC-0013.

CISA instructions must be represented in a deterministic, versioned binary format to support compilation, execution by the Cognitive Virtual Machine (CVM), checkpointing, and deterministic replay.

### 2. Design Principles

The binary encoding follows these principles:

- **Determinism** — The same instruction sequence must always produce the identical binary representation.
- **Versioning** — The format must support forward and backward compatibility within major versions.
- **Simplicity** — The encoding should remain compact while remaining easy to decode.
- **Traceability** — The encoding must preserve all instruction metadata required for tracing.
- **Replay Equivalence** — Binary-encoded programs must be replayable while preserving observable behaviour.

### 3. Binary Instruction Format

Every CISA instruction **MUST** be encoded using the following structure:

```
+--------------------+ 4 bytes
| Magic Number       |  (e.g., 0x43534131 "CISA1")
+--------------------+
| Encoding Version   | 2 bytes (major.minor)
+--------------------+
| InstructionID      | 16 bytes (UUID)
+--------------------+
| Opcode             | 2 bytes
+--------------------+
| Flags              | 2 bytes
+--------------------+
| Operand Count      | 1 byte
+--------------------+
| Operand Types      | variable
+--------------------+
| Operands           | variable
+--------------------+
| Capability ID      | 16 bytes (optional)
+--------------------+
| Effect Class       | 1 byte
+--------------------+
```

### 4. Magic Number and Versioning

- The magic number **MUST** identify the format as CISA.
- The encoding version **MUST** follow semantic versioning (major.minor).
- Implementations **MUST** support all minor versions within a major version.
- Major version changes **MAY** introduce breaking changes.

### 5. Opcode Encoding

Opcodes **MUST** be assigned unique 2-byte numeric values.

Example initial assignments:

| Opcode              | Value   |
|---------------------|---------|
| `LOAD`              | 0x0001  |
| `STORE`             | 0x0002  |
| `MOVE`              | 0x0003  |
| `BELIEF_ASSERT`     | 0x0010  |
| `BELIEF_RETRACT`    | 0x0011  |
| `GOAL_CREATE`       | 0x0020  |
| `GOAL_SATISFY`      | 0x0021  |
| `PLAN_EXECUTE`      | 0x0030  |
| `CAP_VERIFY`        | 0x0040  |
| `EFFECT_EMIT`       | 0x0050  |
| `OBSERVE`           | 0x0060  |
| `INFER`             | 0x0061  |

### 6. Operand Encoding

Each operand **MUST** be prefixed with its type:

```
Operand {
    Type (1 byte)
    Size (2 bytes)
    Value (variable)
}
```

Supported operand types include:

- Immediate (integer, float, boolean)
- Register reference
- Memory reference (UUID)
- Belief reference
- Goal reference
- Plan reference
- Capability reference
- Effect reference

### 7. Deterministic Serialization

The encoding **MUST** guarantee deterministic output:

- Fixed endianness (little-endian).
- No padding bytes.
- Canonical ordering of operands.
- No implicit type coercion.

### 8. Checkpoint and Replay Support

Binary-encoded CISA programs **MUST** support:

- Instruction pointer preservation
- Operand stack serialization
- Register state preservation
- Trace position recording

### 9. Conformance Requirements

A conforming CISA binary implementation **MUST**:

- Produce deterministic binary output for the same instruction sequence.
- Support the defined magic number and versioning scheme.
- Preserve all instruction metadata during serialization.
- Allow deterministic replay from the binary representation.

### 10. Open Questions

The following areas require future specification:

- Concrete numeric opcode assignments
- Compression options for large programs
- Cryptographic signing of CISA binaries
- Just-in-time compilation format

---

**RFC-0014 — CISA Binary Encoding and Serialization Format v1.0 Draft** is now complete.

This RFC provides the concrete representation layer for CISA instructions, enabling compilation, storage, transmission, and deterministic execution by the Cognitive Virtual Machine.
