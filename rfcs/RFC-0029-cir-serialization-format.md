<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #16, sub-message [151], 2026-08-10
  Verbatim source: knowledge-base/sources/message-016-original-part*.md
  Status in corpus: RFC-0029 Cognitive IR Serialization Format (CIR-SER) v1.0 (Draft); review [152]: CIRModuleArtifact, artifact identity, deterministic build chain; 'cognitive equivalent of ELF/WASM'; v1.1 not present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0029 — Cognitive IR Serialization Format (CIR-SER)**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0028 Cognitive Intermediate Representation (CIR) v1.0 (Draft)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive IR Serialization Format (CIR-SER)** for Red/Cognition.

CIR-SER provides a deterministic, versioned, and portable binary (and textual) representation of the Cognitive Intermediate Representation (CIR) defined in RFC-0028. This format enables the exchange, storage, hashing, signing, and deterministic replay of compiled cognitive programs across different compilers, runtimes, and nodes.

### 2. Design Principles

CIR-SER follows these principles:

- **Determinism** — The same CIR structure must always produce the identical serialized representation.
- **Versioning** — The format must support forward and backward compatibility within major versions.
- **Traceability** — Serialization must preserve all provenance and metadata required for replay and auditing.
- **Simplicity** — The encoding should remain compact while remaining easy to generate and parse.
- **Security** — The format must support integrity verification and optional cryptographic signing.

### 3. Binary Module Structure

A serialized CIR module **MUST** follow this structure:

```
+--------------------+ 4 bytes
| Magic Number       |  (e.g., 0x43495231 "CIR1")
+--------------------+
| Format Version     | 2 bytes (major.minor)
+--------------------+
| ModuleID           | 16 bytes (UUID)
+--------------------+
| Version            | 2 bytes
+--------------------+
| CognitiveTypes     | variable
+--------------------+
| Graphs             | variable
+--------------------+
| Operations         | variable
+--------------------+
| Constraints        | variable
+--------------------+
| Metadata           | variable
+--------------------+
| Signature          | variable (optional)
+--------------------+
```

### 4. Versioning and Compatibility

- The format version **MUST** follow semantic versioning.
- Implementations **MUST** support all minor versions within a major version.
- Major version changes **MAY** introduce breaking changes, provided migration paths are defined.

### 5. Deterministic Serialization Rules

The encoding **MUST** guarantee deterministic output:

- Fixed little-endian byte order.
- No padding bytes.
- Canonical ordering of all variable-length sections.
- No implicit type coercion or normalization.

### 6. Graph Serialization

Each graph (GoalGraph, PlanGraph, EffectGraph, etc.) **MUST** be serialized as:

- Node list with stable identifiers
- Edge list with source/target references
- Version information for each node and edge

### 7. Operation Serialization

Each CIR operation **MUST** be serialized with:

- Operation type and identifier
- Inputs and outputs (with references)
- Declared capabilities and effects
- Memory access patterns
- Resource estimates
- Provenance metadata

### 8. Checkpoint and Replay Support

Serialized CIR programs **MUST** support:

- Instruction pointer preservation
- Operand stack and register state
- Trace position recording
- Capability context serialization

### 9. Security and Integrity

Serialized modules **MAY** include:

- Cryptographic hash of the module contents
- Digital signature from the issuing compiler or authority
- Capability-based signing tokens

### 10. Conformance Requirements

A conforming CIR-SER implementation **MUST**:

- Produce deterministic serialized output for the same CIR structure.
- Support the defined magic number and versioning scheme.
- Preserve all metadata and provenance during serialization.
- Allow deterministic deserialization and replay.

### 11. Open Questions

The following areas require future specification:

- Concrete numeric type codes for operations and graphs
- Compression options for large modules
- Integration with cryptographic signing and attestation (RFC-0022)
- Human-readable textual representation (CIR-TXT)

---

**RFC-0029 — Cognitive IR Serialization Format (CIR-SER) v1.0 Draft** is now complete.

This RFC provides the concrete representation layer for the Cognitive Intermediate Representation, enabling portable, deterministic, and verifiable exchange of compiled cognitive programs across the Red/Cognition ecosystem.
