<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #8, sub-message [72], 2026-08-10
  Verbatim source: knowledge-base/sources/message-008-original-part*.md
  Status in corpus: RFC-0001 Ratification Record: ratified v1.2, Date 2026-07-29; accepts ADR-0005 (Cognitive Value Base Contract) and ADR-0006 (Semantic Graph as First-Class Model) — numbering conflicts with earlier ADR-0005/0006 recorded in KB traceability.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates specs/ and rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

## RFC-0001 — Cognitive Type System v1.2  

### Ratification Review Outcome

**Status:** ✅ Approved for Ratification  

**Decision:** Accept RFC-0001 v1.2 as the normative Cognitive Type System foundation for Red/Cognition.

---

# Ratification Record

**Document:** RFC-0001 — Cognitive Type System  

**Version:** 1.2  

**Status:** Ratified  

**Parent:** RC-200 Language Specification v1.0 (Ratified)  

**Authority:** Normative RFC  

**Date:** 2026-07-29  

---

## 1. Ratification Declaration

RFC-0001 Cognitive Type System v1.2 is hereby ratified as the initial normative definition of cognitive values within Red/Cognition.

From this point forward:

- Cognitive values **MUST** conform to the Cognitive Value Base Contract.
- Cognitive type identity **MUST** remain preserved across compilation, serialization, execution, and replay.
- Cognitive metadata and provenance **MUST** be retained throughout the lifecycle of cognitive values.
- Cognitive mutation and immutability rules **MUST** be enforced by conforming implementations.
- Cognitive relationships defined in this RFC become part of the Cognitive IR semantic model.

---

# 2. Ratified Cognitive Value Model

The following structure is now normative:

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

Every cognitive value is therefore:

```
Identity
   +
Metadata
   +
Semantic Type
   +
Versioned Schema
```

---

# 3. Ratified Cognitive Types

| Type | Status | Semantic Role |
|-|-|-|
| `goal!` | Ratified | Desired outcome representation |
| `belief!` | Ratified | Knowledge proposition with confidence |
| `plan!` | Ratified | Action structure toward goals |
| `skill!` | Ratified | Reusable executable capability |
| `memory!` | Ratified | Memory reference/value |
| `capability!` | Ratified | Permission and authority token |
| `effect!` | Ratified | Immutable state transition record |
| `agent!` | Ratified | Runtime cognitive entity |
| `checkpoint!` | Ratified | Recoverable execution snapshot |

---

# 4. Ratified Semantic Graph

The cognitive type graph is now part of the Cognitive IR contract:

```
goal!
  |
  | satisfied-by
  ▼
plan!
  |
  | executes
  ▼
skill!
  |
  | produces
  ▼
effect!
  |
  | updates
  ▼
belief!
```

Cardinality:

```
goal!      (1:N) plan!
plan!      (1:N) skill!
skill!     (1:N) effect!
effect!    (N:M) belief!
```

Implementations **MUST NOT** remove these semantic relationships.

---

# 5. Ratified Mutation Model

| Type | Mutation Rule |
|-|-|
| `goal!` | Mutable lifecycle |
| `belief!` | Append/revision history |
| `plan!` | Mutable with revision tracking |
| `skill!` | Immutable versioned object |
| `memory!` | Ownership-controlled reference model |
| `capability!` | Immutable security token |
| `effect!` | Immutable event |
| `agent!` | Runtime lifecycle managed |
| `checkpoint!` | Immutable snapshot |

---

# 6. Compiler and Runtime Impact

The following pipeline is now normative:

```
Red Source
    ↓
Dialect AST
    ↓
Cognitive IR
    ↓
Unified IR
    ↓
CVM
    ↓
Cognitive Runtime
```

The compiler:

- MUST preserve source representation.
- MUST preserve cognitive metadata.
- MUST preserve type identity.
- MUST NOT execute cognitive behaviour.

The runtime:

- MUST enforce lifecycle rules.
- MUST preserve provenance.
- MUST support serialization and replay.

---

# 7. Accepted Architecture Decisions

## ADR-0005 — Cognitive Value Base Contract

**Status:** Accepted

**Decision:**

All cognitive entities share a common metadata and schema contract.

**Reason:**

Provides:

- universal inspection
- deterministic serialization
- provenance tracking
- version migration

---

## ADR-0006 — Semantic Graph as First-Class Model

**Status:** Accepted

**Decision:**

Relationships between cognitive types are represented explicitly in Cognitive IR.

**Reason:**

Enables:

- explainability
- replay
- graph-based memory
- verification

---

# 8. RFC Dependencies Activated

RFC-0001 establishes dependencies for:

## RFC-0002 — Effect Ordering Model

Defines:

- effect sequencing
- conflict resolution
- transactional boundaries
- causal ordering

## RFC-0003 — Belief Revision System

Defines:

- belief update rules
- contradiction handling
- confidence adjustment
- provenance merging

---

# 9. Next Specification Phase

With:

- RC-000 Constitution
- RC-100 Architecture
- RC-200 Language
- RC-300 Compiler
- RC-400 Runtime
- RC-500 Cognitive Runtime
- RC-600 Agent Runtime Shell
- RC-700 Cognitive VM
- RC-800 Cognitive OS
- RC-900 Governance
- RFC-0001 Cognitive Type System

the foundation layer is now complete.

---

## Recommended Next Document

# RFC-0002 — Effect Ordering Model v1.0

Proposed scope:

1. Effect algebra
2. Effect dependency graph
3. Ordering guarantees
4. Conflict detection
5. Transaction boundaries
6. Rollback semantics
7. Capability interaction
8. Deterministic replay ordering
9. Parallel effect execution rules
10. Distributed effect coordination

---

**RFC-0001 Cognitive Type System v1.2 is ratified.**

The Red/Cognition project now moves from **type foundation** into **causality and execution semantics design**.

# Source Record: Conversation Message #8 — Verbatim Transcript (Part 4 of 5: sub-messages [73]–[76])

- **Message index:** 8 (continued) · **Part 3:** `message-008-original-part3.md` · **Cleanup:** as Part 1.
