# Source Record: Conversation Message #8 — Verbatim Transcript (Part 3 of 5: sub-messages [69]–[72])

- **Message index:** 8 (continued) · **Part 2:** `message-008-original-part2.md` · **Cleanup:** as Part 1.

---

## [69] USER

**RFC-0001 — Cognitive Type System**

**Version:** 1.1  

**Status:** Candidate for Ratification  

**Parent:** RC-200 Language Specification v1.0 (Ratified)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the initial set of cognitive types for Red/Cognition. These types extend the Red type system to support first-class representation of goals, beliefs, plans, skills, memory, capabilities, effects, agents, and checkpoints.

The goal of this RFC is to establish a stable semantic foundation that can be implemented initially through dialects and structured values, with a clear evolution path toward native datatypes where appropriate.

### 2. Design Principles

The cognitive type system follows these principles:

- **Dialect-first evolution** — Types begin as structured blocks or objects and may become native types later.
- **Inspectability** — All cognitive types must remain fully inspectable as data.
- **Traceability** — Every cognitive value must support provenance and history.
- **Compatibility** — Existing Red values and semantics must remain unchanged.
- **Provider neutrality** — No type should embed a specific intelligence mechanism.

### 3. Cognitive Type Categories

Cognitive types are organized into the following categories:

| Category       | Purpose                              | Examples                     |
|----------------|--------------------------------------|------------------------------|
| Intent         | Desired outcomes and objectives      | `goal!`                      |
| Knowledge      | Propositions and facts               | `belief!`, `memory!`         |
| Procedure      | Action sequences and capabilities    | `plan!`, `skill!`            |
| Security       | Permissions and access control       | `capability!`                |
| Event          | State changes and observations       | `effect!`                    |
| Entity         | Runtime participants                 | `agent!`                     |
| Snapshot       | Recoverable execution state          | `checkpoint!`                |

### 4. Proposed Cognitive Types

| Type            | Category     | Initial Representation     | Evolution Path          | Mutation Model          | Owner      |
|-----------------|--------------|----------------------------|-------------------------|-------------------------|------------|
| `goal!`         | Intent       | Structured block/object    | Native (optional)       | Mutable lifecycle       | Agent      |
| `belief!`       | Knowledge    | Structured block/object    | Native (optional)       | Append/revision         | Agent/System |
| `plan!`         | Procedure    | Structured block/object    | Native (optional)       | Mutable with history    | Agent      |
| `skill!`        | Procedure    | Object / compiled form     | Native                  | Versioned immutable     | System     |
| `memory!`       | Knowledge    | Object                     | Native                  | Reference-controlled    | Agent/System |
| `capability!`   | Security     | Object                     | Native                  | Immutable token         | System     |
| `effect!`       | Event        | Structured value           | Native                  | Immutable event         | System     |
| `agent!`        | Entity       | Object                     | Native                  | Persistent entity       | Runtime    |
| `checkpoint!`   | Snapshot     | Object / serialized form   | Native                  | Immutable snapshot      | Runtime    |

### 5. Common Cognitive Metadata Contract

All cognitive types **MUST** include the following metadata:

```
cognitive-meta {
    id: UUID,
    created: timestamp,
    modified: timestamp,
    provenance: source,
    version: integer
}
```

This ensures every cognitive value supports traceability, versioning, and explainability.

### 6. Type Semantics and Relationships

#### 6.1 Core Type Semantics

- `goal!`*: Represents a declarative desired outcome with optional constraints, priority, deadline, and required capabilities.
- `belief!`*: Represents a proposition held with confidence, source, timestamp, and optional validity window.
- `plan!`*: Represents a structured sequence of actions with dependencies and expected effects.
- `skill!`*: Represents a compiled, reusable procedure with declared effects and performance metadata.
- `capability!`*: Represents an explicit, revocable permission with scope and optional expiration.
- `effect!`*: Represents a declared or observed state change (must be immutable after creation).
- `agent!`*: Represents a runtime entity with identity, capabilities, and state.
- `checkpoint!`*: Represents a recoverable snapshot of execution state (immutable).

#### 6.2 Type Relationships

Cognitive types form a semantic graph:

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

These relationships **MUST** be preserved in the Cognitive IR and CVM execution model.

### 7. Mutation and Immutability Rules

| Type            | Mutation Model              | Notes                                      |
|-----------------|-----------------------------|--------------------------------------------|
| `goal!`         | Mutable lifecycle           | May transition through states              |
| `belief!`       | Append/revision model       | Historical versions preserved              |
| `plan!`         | Mutable with history        | Changes recorded as revisions              |
| `skill!`        | Versioned immutable         | New versions create new `skill!`           |
| `capability!`   | Immutable token             | Cannot be modified after issuance          |
| `effect!`       | Immutable event             | Cannot be modified after creation          |
| `checkpoint!`   | Immutable snapshot          | Cannot be modified after creation          |
| `memory!`       | Reference-controlled        | Controlled by memory ownership rules       |
| `agent!`        | Persistent entity           | Lifecycle-managed by runtime               |

### 8. Type Lifecycle Semantics

Each type has a defined lifecycle:

- `goal!`*: Created → Active → Planning → Executing → Satisfied/Failed → Archived
- `belief!`*: Created → Confirmed/Updated → Contradicted → Deprecated
- `plan!`*: Draft → Validated → Executable → Running → Completed/Failed

### 9. Compiler Integration

The compiler **MUST** map cognitive types as follows:

```
Red Source (cognitive block)
   ↓
Dialect AST
   ↓
Cognitive IR
   ↓
CVM Execution / Red Runtime
```

The compiler **MUST** preserve source representation and support inspection of cognitive types at all stages.

### 10. Serialization and Equality

All cognitive types **MUST** support:

- Stable, versioned serialization
- Deterministic equality
- Hashing suitable for semantic memory use

### 11. Open Questions

The following require future RFCs:

- Exact construction syntax for each type
- Interaction with Red type system `to`, `make`, `is`)
- Formal equality and hashing semantics
- Integration with effect ordering (RFC-0002)
- Belief revision semantics (RFC-0003)

---

**RFC-0001 — Cognitive Type System v1.1** is now ready for **Ratification Review**.

---

## [70] CHATGPT (gpt-5-5-mini)

# RFC-0001 — Cognitive Type System v1.1  

## Ratification Review

**Status:** Candidate for Ratification  

**Review Result:** ✅ Architecturally consistent with RC-200, RC-300, RC-500, and RC-700  

**Recommendation:** Proceed to Ratification with minor normative clarifications.

---

# 1. Summary Assessment

RFC-0001 successfully establishes the semantic foundation for cognitive values in Red/Cognition.

The RFC resolves several previously open architectural questions:

| Area | Resolution |
|-|-|
| Type evolution | Dialect → Structured Value → Native Type |
| Traceability | Common metadata contract |
| Provenance | Required for all cognitive values |
| Mutation model | Explicit per-type rules |
| Compiler mapping | Cognitive IR integration |
| Runtime mapping | CVM semantic preservation |
| Provider neutrality | Maintained |

The RFC correctly avoids introducing artificial syntax and preserves the Red philosophy:

```text
Code = Data
Data = Inspectable
Inspectable = Transformable
```

---

# 2. Ratified Architectural Contribution

If approved, RFC-0001 introduces:

## ADR-0005 — Dialect-First Cognitive Type Evolution

**Status:** Accepted

**Decision:**

Cognitive concepts shall initially exist as dialect-defined structures before optional promotion to native datatypes.

Rationale:

- Avoids premature VM coupling.
- Preserves Red compatibility.
- Enables experimentation.
- Allows multiple implementations.

---

# 3. Recommended Normative Clarifications

The RFC is already strong, but three additions are recommended before final ratification.

---

## 3.1 Add Cognitive Value Base Contract

Currently:

```text
goal!
belief!
plan!
skill!
...
```

share metadata implicitly.

A formal base contract should be added:

```
cognitive-value {
    cognitive-meta
    type
    schema-version
}
```

Where:

```
cognitive-meta {
    id
    created
    modified
    provenance
    version
}
```

Required fields:

| Field | Purpose |
|-|-|
| id | Stable identity |
| created | Creation timestamp |
| modified | Last revision |
| provenance | Origin and authority |
| version | Schema/version tracking |

---

## 3.2 Add Cognitive Type Identity Rules

Recommended:

Every cognitive value MUST expose:

```
type-of(value)
```

Example:

```red
type-of goal-value
== goal!
```

The implementation mechanism remains undefined, but semantic identity is required.

---

## 3.3 Add Relationship Cardinality

The semantic graph should define relationship rules.

Current:

```
goal!
 |
 satisfied-by
 |
plan!
```

Recommended extension:

```
goal!
    1:N
       |
       ▼
    plan!

plan!
    1:N
       |
       ▼
    skill!

skill!
    1:N
       |
       ▼
    effect!

effect!
    N:M
       |
       ▼
    belief!
```

Meaning:

- A goal may have multiple plans.
- A plan may contain multiple skills.
- A skill may produce multiple effects.
- Effects may update multiple beliefs.

---

# 4. Compiler Compatibility Review

RFC-0001 aligns with RC-300.

The pipeline:

```
Red Source
    |
    ▼
Cognitive Dialect
    |
    ▼
Dialect AST
    |
    ▼
Cognitive IR
    |
    ▼
Unified IR
    |
    ▼
CVM / Runtime
```

is correct.

Important invariant preserved:

> The compiler understands cognitive structures but does not execute cognition.

---

# 5. Runtime Compatibility Review

RFC-0001 aligns with RC-500.

Memory interaction:

```
belief!
      |
      ▼
Semantic Memory

effect!
      |
      ▼
Episodic Memory

skill!
      |
      ▼
Procedural Memory

goal!/plan!
      |
      ▼
Working Memory
```

This maps cleanly to the four-tier memory topology.

---

# 6. Security Review

`capability!` design is consistent with RC-100:

```
Agent
 |
 | requests
 ▼
capability!
 |
 | authorizes
 ▼
effect!
 |
 | modifies
 ▼
external state
```

Important invariant:

```
No capability
        =
No external effect
```

This should remain constitutional.

---

# 7. Recommended Final RFC Additions

Before ratification:

Add section:

## 12. Cognitive Type Conformance

A conforming implementation:

MUST:

- Preserve cognitive type identity.
- Preserve metadata.
- Preserve provenance.
- Preserve deterministic serialization.
- Preserve mutation rules.
- Preserve semantic relationships.

MAY:

- Implement types as blocks.
- Implement types as objects.
- Implement types as native datatypes.

---

# Final Recommendation

Current status:

```
RFC-0001 v1.1
Candidate for Ratification
```

Recommended update:

```
RFC-0001 v1.2
Candidate for Final Ratification
```

with:

1. Cognitive Value Base Contract  
2. Type Identity Rules  
3. Relationship Cardinality  
4. Conformance Section  

After those additions:

```
RFC-0001 — Cognitive Type System
Status: RATIFIED
```

would become the foundational semantic layer for:

```
RC-200 Language
       |
       ▼
RC-300 Compiler
       |
       ▼
RC-500 Cognitive Runtime
       |
       ▼
RC-700 Cognitive VM
```

The next logical RFC after ratification remains:

**RFC-0002 — Effect Ordering Model**

because `effect!` is now defined, but its ordering, dependency, rollback, and conflict semantics remain intentionally deferred.

---

## [71] USER

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

---

## [72] CHATGPT (gpt-5-5-mini)

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
