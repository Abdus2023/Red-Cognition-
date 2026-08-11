<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #8, sub-message [71], 2026-08-10
  Verbatim source: knowledge-base/sources/message-008-original-part*.md
  Status in corpus: RFC-0001 Cognitive Type System v1.2 (Candidate for Final Ratification); RATIFIED per ratification record [72], Date 2026-07-29.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates specs/ and rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0001 — Cognitive Type System**

**Version:** 1.2  

**Status:** Candidate for Final Ratification  

**Parent:** RC-200 Language Specification v1.0 (Ratified)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the initial set of cognitive types for Red/Cognition and establishes the semantic foundation for representing goals, beliefs, plans, skills, memory, capabilities, effects, agents, and checkpoints as first-class values.

### 2. Design Principles

- Dialect-first evolution
- Full inspectability as data
- Mandatory traceability and provenance
- Preservation of Red compatibility
- Provider neutrality

### 3. Cognitive Value Base Contract

Every cognitive value **MUST** conform to the following base structure:

```
cognitive-value {
    cognitive-meta {
        id: UUID
        created: timestamp
        modified: timestamp
        provenance: source
        version: integer
    }
    type: cognitive-type
    schema-version: integer
}
```

### 4. Proposed Cognitive Types

| Type            | Category     | Initial Form              | Evolution Path       | Mutation Model          | Owner       |
|-----------------|--------------|---------------------------|----------------------|-------------------------|-------------|
| `goal!`         | Intent       | Structured block/object   | Native (optional)    | Mutable lifecycle       | Agent       |
| `belief!`       | Knowledge    | Structured block/object   | Native (optional)    | Append/revision         | Agent/System|
| `plan!`         | Procedure    | Structured block/object   | Native (optional)    | Mutable with history    | Agent       |
| `skill!`        | Procedure    | Object / compiled         | Native               | Versioned immutable     | System      |
| `memory!`       | Knowledge    | Object                    | Native               | Reference-controlled    | Agent/System|
| `capability!`   | Security     | Object                    | Native               | Immutable token         | System      |
| `effect!`       | Event        | Structured value          | Native               | Immutable event         | System      |
| `agent!`        | Entity       | Object                    | Native               | Persistent entity       | Runtime     |
| `checkpoint!`   | Snapshot     | Object / serialized       | Native               | Immutable snapshot      | Runtime     |

### 5. Type Identity and Introspection

Every cognitive value **MUST** support:

```red
type-of value   ; returns the cognitive type (e.g., goal!, belief!)
```

### 6. Semantic Relationships and Cardinality

Cognitive types form the following graph:

```
goal! (1:N) ──satisfied-by──▶ plan!
plan! (1:N) ──executes──────▶ skill!
skill! (1:N) ──produces─────▶ effect!
effect! (N:M) ──updates─────▶ belief!
```

### 7. Mutation and Immutability Rules

| Type            | Mutation Model              | Notes                                      |
|-----------------|-----------------------------|--------------------------------------------|
| `goal!`         | Mutable lifecycle           | State transitions allowed                  |
| `belief!`       | Append/revision             | Historical versions preserved              |
| `plan!`         | Mutable with history        | Revisions recorded                         |
| `skill!`        | Versioned immutable         | New version creates new instance           |
| `capability!`   | Immutable                   | Cannot be modified after issuance          |
| `effect!`       | Immutable                   | Cannot be modified after creation          |
| `checkpoint!`   | Immutable                   | Cannot be modified after creation          |

### 8. Lifecycle Semantics

Each type carries a defined lifecycle state machine (detailed in the full specification).

### 9. Compiler Integration

The compiler **MUST** map cognitive types through the following pipeline while preserving source representation:

```
Red Source → Dialect AST → Cognitive IR → Unified IR → CVM / Runtime
```

### 10. Serialization, Equality, and Hashing

All cognitive types **MUST** support stable serialization, deterministic equality, and hashing suitable for semantic memory.

### 11. Conformance Requirements

A conforming implementation **MUST**:

- Preserve cognitive type identity
- Preserve metadata and provenance
- Preserve mutation/immutability rules
- Preserve semantic relationships
- Support deterministic serialization

### 12. Open Questions

Deferred to future RFCs:

- Exact construction syntax
- Interaction with Red type system
- Formal equality/hashing semantics
- Integration with RFC-0002 and RFC-0003

---

**RFC-0001 v1.2** is now ready for **Final Ratification**. 

Once ratified, the next recommended document is **RFC-0002 — Effect Ordering Model**.
