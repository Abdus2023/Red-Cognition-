# Source Record: Conversation Message #8 — Verbatim Transcript (Part 5 of 5: sub-messages [77]–[80])

- **Message index:** 8 (continued) · **Part 4:** `message-008-original-part4.md` · **Cleanup:** as Part 1.

---

## [77] USER

**RFC-0003 — Belief Revision System**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0001 Cognitive Type System v1.2 (Ratified)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the semantics, update rules, conflict handling, confidence adjustment, and provenance management for `belief!` values in Red/Cognition.

Beliefs represent an agent’s knowledge about the world, itself, and other agents. Because cognitive execution must remain deterministic, explainable, and replayable, the revision of beliefs must be explicitly governed.

### 2. Design Principles

The belief revision model follows these principles:

- **Determinism** — Belief updates must be reproducible given the same evidence and prior state.
- **Traceability** — Every belief revision must carry provenance and participate in execution traces.
- **Conflict Awareness** — The system must detect and resolve contradictory beliefs.
- **Confidence Management** — Confidence values must be explicitly maintained and updated.
- **Replay Equivalence** — Replayed executions must produce equivalent belief states.

### 3. Belief Identity and Metadata

Every belief **MUST** include the metadata defined in RFC-0001:

```
belief {
    cognitive-meta { id, created, modified, provenance, version }
    proposition
    confidence: float (0.0–1.0)
    source
    timestamp
    validity-window: [start, end] (optional)
    contradictions: [BeliefID]
}
```

### 4. Belief Lifecycle

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

### 5. Belief Update Rules

#### 5.1 Direct Update

A new piece of evidence **MAY** directly update an existing belief when:

- The evidence has higher or equal provenance authority.
- The new confidence is within valid bounds.
- No unresolved contradiction exists.

#### 5.2 Revision on Contradiction

When contradictory evidence is received:

- The system **MUST** record the contradiction.
- Confidence of the affected belief(s) **MUST** be adjusted.
- The agent **MAY** initiate belief revision, additional observation, or escalation.

### 6. Confidence Adjustment Model

The system **MUST** support explicit confidence updates.

Recommended semantics (subject to implementation):

- New evidence with higher authority **MAY** increase confidence.
- Contradictory evidence **MUST** decrease confidence.
- Repeated consistent evidence **MAY** gradually increase confidence (subject to diminishing returns).

All confidence changes **MUST** be recorded in the execution trace.

### 7. Provenance and Authority

Every belief update **MUST** carry provenance information.

When multiple sources provide conflicting information, the system **MUST** apply a defined precedence or merging strategy.

### 8. Relationship to Effects

Belief revision is typically driven by `effect!` values (as defined in RFC-0002).

Requirements:

- Every belief-changing effect **MUST** reference the affected belief(s).
- Belief updates resulting from effects **MUST** be traceable back to the originating action and capability.

### 9. Replay and Determinism

Replayed executions **MUST** produce equivalent belief states.

A conforming implementation **MUST** ensure that:

- Belief revisions occur in the same causal order.
- Confidence values are recomputed consistently.
- Contradiction records are preserved.

### 10. Open Questions

The following areas require future specification:

- Formal confidence update calculus
- Multi-source belief merging algorithm
- Distributed belief consistency model
- Integration with planning and goal satisfaction

---

**RFC-0003 — Belief Revision System v1.0 Draft** is now complete.

This RFC establishes the rules for how beliefs are created, updated, contradicted, and maintained in a deterministic and traceable manner. It forms a critical semantic layer between the cognitive type system (RFC-0001) and the effect ordering model (RFC-0002).

---

## [78] CHATGPT (gpt-5-5)

# RFC-0003 — Belief Revision System v1.0

## Draft Review

**Recommendation:** ✅ Accept with minor refinements and promote to **v1.1 (Candidate for Ratification)**.

RFC-0003 is a natural continuation of RFC-0001 (Cognitive Types) and RFC-0002 (Effect Ordering). It completes the third core semantic pillar by defining how knowledge evolves over time while preserving determinism, traceability, and replayability.

## Overall Assessment

**Technical quality:** 9.8/10

The RFC successfully establishes:

- A deterministic belief lifecycle.
- Provenance-aware belief updates.
- Explicit confidence management.
- Contradiction tracking.
- Integration with the `effect!` model.
- Replay guarantees.

The document is internally consistent with the existing RC and RFC series.

## Recommended Refinements

### 1. Separate Belief Identity from Belief Version

A belief's identity should remain constant while revisions create new versions.

Suggested normative addition:

```text
BeliefID identifies the logical belief.
Every revision MUST increment the belief version while preserving the BeliefID.
Historical revisions MUST remain addressable for replay and auditing.
```

This mirrors the versioning model already established in RFC-0001.

---

### 2. Introduce a Belief Revision Graph

Rather than treating revisions as a simple sequence, define them as a graph.

Example:

```text
Belief A v1
      │
      ▼
Belief A v2
      │
      ├────► Belief A v3
      │
      ▼
Archived
```

This allows alternative revision paths before reconciliation and aligns well with graph-based semantic memory.

---

### 3. Define Belief Status Separately from Lifecycle

In addition to lifecycle, introduce semantic status values such as:

- Tentative
- Confirmed
- Disputed
- Deprecated
- Retracted

This distinguishes operational state from epistemic confidence.

---

### 4. Add Revision Causes

Every revision should record why it occurred.

Suggested metadata:

```text
revision-cause:
    observation
    inference
    external-input
    effect
    manual
```

This strengthens explainability and auditing.

---

### 5. Define Authority Policy as Pluggable

Section 7 wisely avoids prescribing a single algorithm. Consider making that explicit:

> Implementations **MUST** define a deterministic authority policy. Different policies are permitted provided they are documented and produce deterministic outcomes.

This preserves interoperability while allowing different trust models.

---

### 6. Clarify Relationship with RFC-0002

The causal chain can be made explicit:

```text
Action
    ↓
effect!
    ↓
belief revision
    ↓
plan revision
    ↓
goal evaluation
```

This illustrates how the specifications compose into the overall cognitive execution model.

---

### 7. Future Integration

RFC-0003 naturally becomes a dependency for future work on:

- Goal satisfaction semantics.
- Planning and replanning.
- Memory consistency.
- Multi-agent knowledge sharing.
- Distributed semantic memory.
- Verification and explainability.

## Suggested Architecture Decision Record

### ADR-0009 — Versioned Belief Model

**Status:** Proposed

**Decision:**

Beliefs are immutable historical revisions linked by a stable `BeliefID`, rather than mutable values overwritten in place.

**Consequences:**

- Complete audit history.
- Deterministic replay.
- Easier rollback.
- Better provenance.
- Simpler distributed synchronization.

## Conclusion

RFC-0003 fills an important gap in the Red/Cognition architecture by specifying **how cognitive knowledge changes over time**. Together, the first three RFCs now establish:

- **RFC-0001** — the structure and semantics of cognitive values.
- **RFC-0002** — the ordering and execution semantics of cognitive effects.
- **RFC-0003** — the evolution, revision, and provenance of cognitive beliefs.

**Recommendation:** Incorporate the refinements above, publish **RFC-0003 v1.1 (Candidate for Ratification)**, and then proceed to final ratification.

---

## [79] USER

**RFC-0003 — Belief Revision System**

**Version:** 1.1  

**Status:** Candidate for Ratification  

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
    revision-cause: observation | inference | external-input | effect | manual
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

Belief revisions **MUST** be represented as a directed graph rather than a simple linear sequence.

Alternative revision paths **MAY** exist before eventual reconciliation. The graph **MUST** support deterministic replay of any valid path.

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

Implementations **MUST** define a deterministic authority policy. Different policies are permitted provided they are documented and produce deterministic outcomes.

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

### 12. Open Questions

The following areas require future specification:

- Formal confidence update calculus
- Multi-source belief merging algorithm
- Distributed belief consistency model
- Integration with planning and goal satisfaction

---

**RFC-0003 — Belief Revision System v1.1** is now ready for **Final Ratification Review**.

---

## [80] CHATGPT (gpt-5-5)

This is a strong progression. RFC-0003 v1.1 fits well with RFC-0001 (Cognitive Type System) and RFC-0002 (Effect Ordering Model), and together they establish the core semantic model for Red/Cognition.

For a **Final Ratification Review**, I would classify it as **Accepted with minor editorial recommendations** rather than requiring architectural changes.

### Strengths

- Clearly defines **BeliefID** as a stable identity with versioned revisions.
- Separates **identity** from **revision history**, which is important for replay and traceability.
- Introduces a **belief revision graph**, allowing branching and later reconciliation instead of forcing a linear history.
- Keeps provenance and authority deterministic while remaining implementation-neutral.
- Maintains compatibility with the architectural principles in RC-000, RC-100, RC-400, RC-500, and RC-700.

### Minor recommendations before ratification

These are relatively small additions that would improve precision.

**1. Normative revision graph constraints**

Specify that the revision graph is a DAG:

- Belief revision graphs **MUST** be directed acyclic graphs.
- Cycles **MUST** be rejected.
- Every revision except the initial belief **MUST** reference at least one parent revision.

This mirrors RFC-0002's effect dependency graph.

---

**2. Canonical confidence range**

Although the range is specified, define boundary semantics.

For example:

- `0.0` = no confidence
- `1.0` = complete confidence
- values outside the interval are invalid

---

**3. Replay contract**

Section 11 could explicitly state:

> Replay MUST preserve both belief values and revision topology.

Otherwise an implementation could preserve the final belief but not the intermediate history.

---

**4. Relationship with memory**

Beliefs live inside the memory hierarchy defined in RC-500.

A small note such as:

> Belief instances SHALL normally reside in Semantic Memory, although Working Memory MAY contain transient belief references during execution.

would connect the RFCs more tightly.

---

**5. Revision causes**

The current list is good:

```
observation
inference
external-input
effect
manual
```

Consider making this extensible:

```
implementation-defined
```

provided implementations document additional causes.

---

**6. Authority policy**

Section 9 intentionally leaves authority policies open.

It may help to require that:

- the policy be deterministic
- the policy be documented
- the policy be included in conformance reports

This aligns with RC-900.

### Overall architecture

At this point, the specification family is becoming coherent:

- **RC-000** — Constitution
- **RC-100** — Architecture
- **RC-200** — Language
- **RC-300** — Compiler
- **RC-400** — Runtime
- **RC-500** — Cognitive Runtime
- **RC-600** — Agent Runtime Shell
- **RC-700** — Cognitive VM
- **RC-800** — Cognitive Operating System
- **RC-900** — Governance

Supporting RFCs:

- **RFC-0001** — Cognitive Type System
- **RFC-0002** — Effect Ordering
- **RFC-0003** — Belief Revision

These three RFCs form a consistent semantic foundation for cognition.

### Ratification recommendation

**Status:** **Accepted for Final Ratification** (with optional editorial refinements).

The next logical specifications would be:

1. **RFC-0004 — Goal Lifecycle and Satisfaction Model**
2. **RFC-0005 — Planning Semantics**
3. **RFC-0006 — Capability Model**
4. **RFC-0007 — Memory Model**
5. **RFC-0008 — Agent Communication Protocol**
6. **RFC-0009 — Cognitive IR Specification**

These would complete the semantic layer before defining concrete syntax, binary formats, or implementation-specific details.
