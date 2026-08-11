<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #8, sub-message [75], 2026-08-10
  Verbatim source: knowledge-base/sources/message-008-original-part*.md
  Status in corpus: RFC-0002 Effect Ordering Model v1.1 (Candidate); RATIFIED per ratification record [76], Date 2026-07-29.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates specs/ and rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0002 — Effect Ordering Model**

**Version:** 1.1  

**Status:** Candidate for Ratification  

**Parent:** RFC-0001 Cognitive Type System v1.2 (Ratified)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the semantics, ordering rules, dependency model, conflict handling, transactional behaviour, and replay guarantees for `effect!` values in Red/Cognition.

Effects represent the observable consequences of cognitive actions. Because cognitive execution must remain deterministic, explainable, and replayable, the ordering and interaction of effects must be explicitly governed.

### 2. Design Principles

The effect ordering model follows these principles:

- **Determinism** — Given the same state and inputs, effect ordering must be reproducible.
- **Traceability** — Every effect must carry provenance and participate in an execution trace.
- **Capability Mediation** — All external effects must be authorized by capabilities.
- **Conflict Awareness** — The system must detect and handle conflicting effects.
- **Replay Equivalence** — Replayed executions must produce equivalent externally observable behaviour.

### 3. Effect Identity

Every effect **MUST** possess a globally unique **Effect Identifier (Effect ID)**.

The Effect ID **MUST** remain stable throughout:

- Serialization
- Checkpointing
- Restoration
- Distributed propagation
- Replay

### 4. Effect Classes

Effects are classified into four primary classes:

| Class          | Description                              | External State Change | Rollback / Compensation |
|----------------|------------------------------------------|-----------------------|-------------------------|
| `pure!`        | No observable side effects               | No                    | N/A                     |
| `internal!`    | Internal state changes only              | No                    | Yes                     |
| `capability!`  | Effects requiring explicit authorization | Yes                   | Controlled              |
| `external!`    | Direct external state changes            | Yes                   | Limited                 |

### 5. Effect Lifecycle

Every effect **MUST** follow this lifecycle:

```
Created
   ↓
Validated
   ↓
Authorized
   ↓
Scheduled
   ↓
Executing
   ↓
Committed
   ↓
Archived
```

Rollback or compensation transitions are permitted where supported by the effect class and declared in the effect metadata.

### 6. Effect Metadata Contract

Every effect **MUST** include the following metadata:

```
effect {
    id: EffectID
    type: effect-class
    provenance: source
    capability: capability-reference (optional)
    timestamp: timestamp
    dependencies: [EffectID]
    replay-policy: deterministic | best-effort
}
```

### 7. Effect Ordering Rules

#### 7.1 Ordering Types

- **Temporal Order**: The chronological order in which effects occur.
- **Causal Order**: The dependency relationship between effects.

Two effects may share the same temporal window while remaining causally independent.

#### 7.2 Effect Dependency Graph

The Effect Dependency Graph **MUST** form a **Directed Acyclic Graph (DAG)**.

Circular dependencies are invalid and **MUST** be rejected during analysis or execution.

### 8. Conflict Detection and Resolution

The system **MUST** detect the following conflict types:

- Direct Conflict
- Capability Conflict
- Temporal Conflict
- Causal Conflict

Resolution strategies include rejection, serialization with retry, explicit transactional boundaries, or human/agent-mediated resolution.

### 9. Transactional Boundaries

Effects **MAY** be grouped into transactional units.

A transaction:

- Executes as an atomic unit with respect to external state.
- Either commits all effects or rolls back/compensates to a consistent prior state.
- Must be explicitly declared or inferred from capability usage.

### 10. Rollback and Compensation

The system **MUST** support rollback or compensation for effects where possible.

- `pure!` and `internal!` effects are generally rollback-safe.
- `capability!` and `external!` effects **MUST** declare rollback or compensation support in their metadata.
- Compensation actions **MUST** themselves be represented as effects.

### 11. Deterministic Replay

Replayed executions **MUST** produce equivalent externally observable behaviour.

A conforming implementation **MUST** replay an execution trace such that externally observable behaviour is equivalent to the original execution, even if internal scheduling differs where permitted by this specification.

### 12. Parallel Effect Execution

Effects **MAY** execute in parallel when:

- No causal dependency exists.
- No resource conflict is detected.
- Capability constraints permit concurrent execution.

The runtime **MUST** guarantee that parallel execution does not violate sequential semantics when observed through traces.

### 13. Distributed Effect Coordination

In distributed settings, the system **MUST** provide:

- Causal ordering across nodes
- Conflict detection across distributed effect streams
- Consistent checkpointing across multiple agents

### 14. Open Questions

The following areas require future specification:

- Concrete syntax for declaring transactional boundaries
- Formal effect algebra
- Distributed consensus protocol for effect ordering
- Optimization of effect graphs

---

**RFC-0002 — Effect Ordering Model v1.1** is now ready for **Final Ratification Review**.
