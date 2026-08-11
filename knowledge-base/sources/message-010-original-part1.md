# Source Record: Conversation Message #10 — Verbatim Transcript (Part 1 of 5: sub-messages [81]–[84])

- **Message index:** 10
- **Direction:** user → assistant
- **Received:** 2026-08-10
- **Source document:** inline conversation message (no attached files)
- **Continued in:** `message-010-original-part2.md` … `message-010-original-part5.md`

Rendering-artifact cleanup applied (no semantic changes): HTML entities decoded; collapsible `<details><summary>…</summary>` wrappers removed (fenced content preserved). Source quirks preserved as received (e.g., stray backtick artifacts like `` `MUST`, `SHALL`, `MAY`) `` in [82], unmatched parens in [96]/[98]/[99]/[100] prose, trailing-whitespace artifacts in [91]).

---

## [81] USER

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

---

## [82] CHATGPT (gpt-5-5)

**Ratification Review — RFC-0003 v1.2**

**Decision:** **Ratified**

**Status after review:** **RFC-0003 — Belief Revision System v1.2 (Ratified)**

RFC-0003 v1.2 successfully incorporates the remaining architectural recommendations and is internally consistent with the Red/Cognition specification family.

### Conformance Assessment

| Area | Result |
|-------|--------|
| Consistency with RC-000 Constitution | ✓ Pass |
| Consistency with RC-100 Architecture | ✓ Pass |
| Compatibility with RC-200 Language | ✓ Pass |
| Compatibility with RC-300 Compiler | ✓ Pass |
| Compatibility with RC-400 Runtime | ✓ Pass |
| Compatibility with RC-500 Cognitive Runtime | ✓ Pass |
| Compatibility with RC-700 CVM | ✓ Pass |
| Compatibility with RFC-0001 Cognitive Types | ✓ Pass |
| Compatibility with RFC-0002 Effect Ordering | ✓ Pass |

### Strengths

RFC-0003 now provides a complete normative foundation for belief management by defining:

- Stable **BeliefID** with versioned revisions.
- A **DAG-based belief revision model**, preventing cyclic revision histories.
- Deterministic provenance and authority handling.
- Explicit lifecycle and semantic status.
- Trace-preserving replay requirements.
- Memory placement within the RC-500 four-tier memory hierarchy.
- Extensible revision causes while maintaining deterministic conformance.
- A clear linkage between `effect!` and `belief!`, integrating with RFC-0002.

### Normative Quality

The document consistently uses RFC 2119 terminology `MUST`, `SHALL`, `MAY`) and avoids implementation-specific constraints, making it suitable as a normative specification.

### Remaining Deferred Work

The remaining open questions are appropriate for future RFCs:

- Formal confidence update calculus
- Multi-source belief merge algorithms
- Distributed belief consistency
- Integration with planning and goal satisfaction

These are implementation and semantic refinements rather than prerequisites for ratification.

### Current Ratified Semantic Core

The Red/Cognition project now has a coherent semantic foundation:

#### Core Specifications

- **RC-000** — Constitution
- **RC-100** — Architecture
- **RC-200** — Language
- **RC-300** — Compiler
- **RC-400** — Runtime
- **RC-500** — Cognitive Runtime
- **RC-600** — Agent Runtime Shell
- **RC-700** — Cognitive Virtual Machine
- **RC-800** — Cognitive Operating System
- **RC-900** — Governance

#### Ratified RFCs

- **RFC-0001** — Cognitive Type System
- **RFC-0002** — Effect Ordering Model
- **RFC-0003** — Belief Revision System

Together, these define the foundational semantics for cognitive values, effect execution, and belief evolution while preserving determinism, traceability, replayability, and compatibility with Red.

### Recommended Next RFC Sequence

With the semantic core established, the next logical specifications are:

1. **RFC-0004 — Goal Lifecycle and Satisfaction Model**
2. **RFC-0005 — Planning Semantics**
3. **RFC-0006 — Capability Model**
4. **RFC-0007 — Memory Model**
5. **RFC-0008 — Agent Communication Protocol**
6. **RFC-0009 — Cognitive Intermediate Representation (CIR) Specification**

These RFCs would complete the behavioural semantics needed before defining concrete syntax, binary encodings, optimisation strategies, or implementation-specific interfaces.

**Final Decision:** **RFC-0003 — Belief Revision System v1.2 is Ratified.**

---

## [83] USER

**RFC-0004 — Goal Lifecycle and Satisfaction Model**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0001 Cognitive Type System v1.2 (Ratified)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the lifecycle, state transitions, satisfaction conditions, and failure semantics for `goal!` values in Red/Cognition.

Goals represent the primary unit of intent in the cognitive system. Because cognitive execution must remain deterministic, explainable, and replayable, the lifecycle and satisfaction of goals must be explicitly governed.

### 2. Design Principles

The goal lifecycle model follows these principles:

- **Declarative by default** — A goal primarily describes *what* should be achieved, not *how*.
- **Determinism** — Goal satisfaction and failure must be reproducible given the same world state and evidence.
- **Traceability** — Every goal state transition must be recorded and linked to the responsible effects and beliefs.
- **Replay Equivalence** — Replayed executions must reach equivalent goal states.
- **Capability Awareness** — Goal satisfaction must respect capability constraints.

### 3. Goal Identity and Metadata

Every goal **MUST** include the metadata defined in RFC-0001:

```
goal {
    cognitive-meta { id, created, modified, provenance, version }
    target
    priority: float (optional)
    constraints: [constraint] (optional)
    deadline: timestamp (optional)
    required-capabilities: [CapabilityID] (optional)
    status: pending | active | planning | executing | satisfied | failed | archived
}
```

### 4. Goal Lifecycle

Every goal **MUST** follow this lifecycle:

```
Created (Pending)
   ↓
Active
   ↓
Planning
   ↓
Executing
   ↓
Satisfied / Failed
   ↓
Archived
```

### 5. Goal Satisfaction Model

A goal is considered **satisfied** when its target condition evaluates to true under the current belief state and all declared constraints are met.

Requirements:

- Satisfaction **MUST** be evaluated against the agent’s current belief set.
- Satisfaction **MUST** respect the goal’s declared constraints and required capabilities.
- Satisfaction **MUST** be deterministic given the same belief state.

### 6. Goal Failure Model

A goal is considered **failed** when:

- All viable plans have been exhausted without achieving the target.
- A hard constraint or deadline has been violated.
- An unrecoverable contradiction in supporting beliefs has occurred.

Failure **MUST** be recorded with the responsible cause(s).

### 7. Relationship to Plans and Effects

Goals are satisfied through plans (as defined in RFC-0001 and future planning RFCs).

Requirements:

- A goal **MAY** have zero or more associated plans.
- Plan execution **MUST** produce effects that are traceable back to the originating goal.
- Goal satisfaction **MUST** be driven by observed effects (RFC-0002).

### 8. Relationship to Beliefs

Goal evaluation and satisfaction **MUST** be based on the agent’s current belief state (RFC-0003).

A goal **MAY** become unsatisfiable if supporting beliefs are contradicted or retracted.

### 9. Replay and Determinism

Replayed executions **MUST** reach equivalent goal states (satisfied or failed) given the same initial conditions and belief evolution.

A conforming implementation **MUST** preserve:

- Goal identity and version across replays.
- The causal chain from actions → effects → belief updates → goal state transitions.

### 10. Open Questions

The following areas require future specification:

- Formal goal satisfaction calculus
- Multi-goal dependency and conflict resolution
- Goal prioritization and scheduling semantics
- Integration with planning (RFC-0005)

---

**RFC-0004 — Goal Lifecycle and Satisfaction Model v1.0 Draft** is now complete.

This RFC establishes the rules for how goals are created, pursued, satisfied, and failed in a deterministic and traceable manner. It forms a critical semantic layer connecting the cognitive type system (RFC-0001), effect ordering (RFC-0002), and belief revision (RFC-0003).

---

## [84] CHATGPT (gpt-5-5)

# Ratification Review — RFC-0004 v1.0

**Decision:** **Accepted with Minor Revisions**

**Status:** **Candidate for Ratification** (recommended as **v1.1** after incorporating the editorial changes below)

RFC-0004 is consistent with the architecture established by RC-000 through RC-900 and integrates cleanly with RFC-0001 (Cognitive Types), RFC-0002 (Effect Ordering), and RFC-0003 (Belief Revision). It successfully establishes `goal!` as the primary unit of intent while preserving determinism, traceability, and replayability.

## Conformance Assessment

| Area | Result |
|-------|--------|
| RC-000 Constitution | ✓ Pass |
| RC-100 Architecture | ✓ Pass |
| RC-200 Language | ✓ Pass |
| RFC-0001 Cognitive Types | ✓ Pass |
| RFC-0002 Effect Ordering | ✓ Pass |
| RFC-0003 Belief Revision | ✓ Pass |
| RC-500 Cognitive Runtime | ✓ Pass |
| RC-700 Cognitive VM | ✓ Pass |

## Strengths

The RFC clearly defines:

- Stable goal identity.
- A deterministic lifecycle.
- Explicit satisfaction and failure semantics.
- Integration with beliefs, plans, and effects.
- Replay guarantees.
- Separation of declarative intent ("what") from planning ("how").

This aligns well with the overall Red/Cognition philosophy.

---

# Recommended additions before ratification

## 1. Stable GoalID

Like beliefs and effects, goals should define a stable identifier.

Add to Section 3:

> Every goal SHALL possess a stable **GoalID**.
>
> The GoalID MUST remain constant across serialization, checkpointing, restoration, distributed execution, and replay.

This keeps identity semantics consistent across all cognitive types.

---

## 2. Goal Versioning

Since goals can change state and constraints, define revision semantics.

For example:

- Every modification increments the goal version.
- Historical revisions remain addressable.
- Lifecycle transitions are revisions.

This mirrors RFC-0003.

---

## 3. Goal State Machine

Current lifecycle:

```
Pending
↓
Active
↓
Planning
↓
Executing
↓
Satisfied / Failed
↓
Archived
```

Specify that:

- backward transitions are prohibited unless restored from a checkpoint;
- terminal states are:
  - Satisfied
  - Failed
  - Archived.

This removes ambiguity.

---

## 4. Goal Dependency Graph

Goals often depend on other goals.

Add:

```
Goal A
   │
depends-on
   ▼
Goal B
```

Normative rules:

- Goal dependencies MUST form a DAG.
- Cycles MUST be rejected.
- Dependent goals cannot be satisfied before prerequisites.

This complements RFC-0002's Effect DAG and RFC-0003's Belief DAG.

---

## 5. Satisfaction Metadata

Instead of only storing status, record why satisfaction occurred.

Example:

```text
goal-result {
    satisfied-by: [EffectID]
    supporting-beliefs: [BeliefID]
    completion-time
}
```

This greatly improves explainability.

---

## 6. Unsatisfied vs Failed

Currently there is only "Failed."

Consider distinguishing:

- **Unsatisfied**
  - still achievable
  - waiting for planning/resources
- **Failed**
  - impossible under current constraints

This is useful for long-running autonomous agents.

---

## 7. Goal Ownership

Define ownership explicitly.

Example:

- personal goal
- shared goal
- system goal

This becomes important for multi-agent execution.

---

## 8. Relationship to Memory

As RFC-0003 specifies memory placement, RFC-0004 could add:

> Goal instances SHALL normally reside in Working Memory while active and MAY be archived into Episodic Memory upon completion or failure.

This integrates naturally with RC-500.

## Overall assessment

RFC-0004 completes the third pillar of the cognitive semantic model:

- **Beliefs** describe what the agent considers true.
- **Goals** describe what the agent intends to achieve.
- **Effects** describe what actually changes.

Planning (RFC-0005) will then connect beliefs to goals by defining *how* goals are achieved.

## Recommendation

After incorporating the recommended additions, I would recommend:

**RFC-0004 — Goal Lifecycle and Satisfaction Model v1.1**

**Status:** **Ratified**

At that point, the semantic foundation would include:

- ✓ RFC-0001 — Cognitive Type System
- ✓ RFC-0002 — Effect Ordering Model
- ✓ RFC-0003 — Belief Revision System
- ✓ RFC-0004 — Goal Lifecycle and Satisfaction Model

leaving **RFC-0005 — Planning Semantics** as the next key specification to complete the core cognitive execution model.
