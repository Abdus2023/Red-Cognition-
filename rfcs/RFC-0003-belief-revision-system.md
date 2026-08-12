<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #10, sub-message [81], 2026-08-10
  Verbatim source: knowledge-base/sources/message-010-original-part*.md
  Status in corpus: RFC-0003 Belief Revision System v1.2 (Candidate for Final Ratification); RATIFIED per review decision [82] ("RFC-0003 — Belief Revision System v1.2 is Ratified"), Date 2026-07-29. NOTE: this file supersedes the previously scaffolded v1.1 text (corpus [79], preserved in archive message-008-part5).
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0003 — Belief Revision System**

**Version:** 1.2  

**Status:** Candidate for Final Ratification  

**Parent:** RFC-0001 Cognitive Type System v1.2 (Ratified)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the semantics, update rules, conflict handling, confidence adjustment, provenance management, and replay guarantees for `belief!` values in Red/Cognition.

Beliefs represent an agent’s knowledge about the world, itself, and other agents. Because cognitive execution must remain deterministic, explainable, and replayable, the revision of beliefs must be explicitly governed.

### 2. Design Principles

The belief revision model follows these principles:

- **Determinism** — Belief updates must be reproducible given the same evidence and prior state.
- **Traceability** — Every belief revision must carry provenance and participate in execution traces.
- **Conflict Awareness** — The system must detect and resolve contradictory beliefs.
- **Confidence Management** — Confidence values must be explicitly maintained and updated.
- **Replay Equivalence** — Replayed executions must produce equivalent belief states.

### 3. Belief Identity and Versioning

Every belief is identified by a stable **BeliefID**.

- The `BeliefID` **MUST** remain constant across all revisions.
- Every revision **MUST** increment the belief version while preserving the `BeliefID`.
- Historical revisions **MUST** remain addressable for replay and auditing.

### 4. Belief Metadata Contract

Every belief **MUST** include the metadata defined in RFC-0001, plus revision-specific information:

```
belief {
    cognitive-meta { id, created, modified, provenance, version }
    proposition
    confidence: float (0.0–1.0)
    source
    timestamp
    validity-window: [start, end] (optional)
    contradictions: [BeliefID]
    revision-cause: observation | inference | external-input | effect | manual | implementation-defined
    status: tentative | confirmed | disputed | deprecated | retracted
}
```

### 5. Belief Lifecycle and Status

Every belief **MUST** follow this lifecycle:

```
Created
   ↓
Confirmed / Updated
   ↓
Contradicted
   ↓
Deprecated / Archived
```

In addition to lifecycle state, every belief carries a semantic status:

- **Tentative**
- **Confirmed**
- **Disputed**
- **Deprecated**
- **Retracted**

### 6. Belief Revision Graph

Belief revisions **MUST** be represented as a directed acyclic graph (DAG).

- Every revision except the initial belief **MUST** reference at least one parent revision.
- Cycles **MUST** be rejected.
- Alternative revision paths **MAY** exist before eventual reconciliation.

### 7. Belief Update Rules

#### 7.1 Direct Update

A new piece of evidence **MAY** directly update an existing belief when:

- The evidence has higher or equal provenance authority.
- The new confidence is within valid bounds.
- No unresolved contradiction exists.

#### 7.2 Revision on Contradiction

When contradictory evidence is received:

- The system **MUST** record the contradiction (including the contradicting `BeliefID`).
- Confidence of the affected belief(s) **MUST** be adjusted.
- The agent **MAY** initiate belief revision, additional observation, or escalation.

### 8. Confidence Adjustment Model

The system **MUST** support explicit confidence updates.

All confidence changes **MUST** be recorded in the execution trace, including the revision cause and source.

### 9. Provenance and Authority

Every belief update **MUST** carry provenance information.

Implementations **MUST** define a deterministic authority policy. Different policies are permitted provided they are documented and produce deterministic outcomes. The policy **MUST** be included in conformance reports.

### 10. Relationship to Effects

Belief revision is typically driven by `effect!` values (as defined in RFC-0002).

Requirements:

- Every belief-changing effect **MUST** reference the affected belief(s).
- Belief updates resulting from effects **MUST** be traceable back to the originating action and capability.

### 11. Replay and Determinism

Replayed executions **MUST** produce equivalent belief states.

A conforming implementation **MUST** ensure that:

- Belief revisions occur in the same causal order.
- Confidence values are recomputed consistently.
- Contradiction records are preserved.
- The revision topology is preserved.

### 12. Memory Placement

Belief instances **SHALL** normally reside in Semantic Memory, although Working Memory **MAY** contain transient belief references during execution.

### 13. Open Questions

The following areas require future specification:

- Formal confidence update calculus
- Multi-source belief merging algorithm
- Distributed belief consistency model
- Integration with planning and goal satisfaction

---

**RFC-0003 — Belief Revision System v1.2** is now ready for **Final Ratification**.
