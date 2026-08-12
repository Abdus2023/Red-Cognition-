<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #10, sub-message [85], 2026-08-10
  Verbatim source: knowledge-base/sources/message-010-original-part*.md
  Status in corpus: RFC-0004 Goal Lifecycle and Satisfaction Model v1.1 (Candidate); RATIFIED per final review [86], Date 2026-07-29.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0004 — Goal Lifecycle and Satisfaction Model**

**Version:** 1.1  

**Status:** Candidate for Ratification  

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

### 3. Goal Identity and Versioning

Every goal is identified by a stable **GoalID**.

- The `GoalID` **MUST** remain constant across all revisions and state transitions.
- Every modification **MUST** increment the goal version while preserving the `GoalID`.
- Historical versions **MUST** remain addressable for replay and auditing.

### 4. Goal Metadata Contract

Every goal **MUST** include the metadata defined in RFC-0001, plus goal-specific attributes:

```
goal {
    cognitive-meta { id, created, modified, provenance, version }
    target
    priority: float (optional)
    constraints: [constraint] (optional)
    deadline: timestamp (optional)
    required-capabilities: [CapabilityID] (optional)
    status: pending | active | planning | executing | satisfied | failed | archived
    satisfied-by: [EffectID] (optional)
    supporting-beliefs: [BeliefID] (optional)
    completion-time: timestamp (optional)
}
```

### 5. Goal Lifecycle

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

**Notes:**

- Backward transitions are prohibited unless restored from a checkpoint.
- Terminal states are: **Satisfied**, **Failed**, and **Archived**.

### 6. Goal Satisfaction Model

A goal is considered **satisfied** when its target condition evaluates to true under the current belief state and all declared constraints are met.

Requirements:

- Satisfaction **MUST** be evaluated against the agent’s current belief set.
- Satisfaction **MUST** respect the goal’s declared constraints and required capabilities.
- Satisfaction **MUST** be deterministic given the same belief state.

### 7. Goal Failure Model

A goal is considered **failed** when:

- All viable plans have been exhausted without achieving the target.
- A hard constraint or deadline has been violated.
- An unrecoverable contradiction in supporting beliefs has occurred.

Failure **MUST** be recorded with the responsible cause(s).

### 8. Goal Dependency Graph

Goals **MAY** depend on other goals.

Requirements:

- Goal dependencies **MUST** form a Directed Acyclic Graph (DAG).
- Cycles **MUST** be rejected.
- A goal **MUST NOT** be satisfied before its prerequisite goals are satisfied.

### 9. Relationship to Plans and Effects

Goals are satisfied through plans (as defined in RFC-0001 and future planning RFCs).

Requirements:

- A goal **MAY** have zero or more associated plans.
- Plan execution **MUST** produce effects that are traceable back to the originating goal.
- Goal satisfaction **MUST** be driven by observed effects (RFC-0002).

### 10. Relationship to Beliefs

Goal evaluation and satisfaction **MUST** be based on the agent’s current belief state (RFC-0003).

A goal **MAY** become unsatisfiable if supporting beliefs are contradicted or retracted.

### 11. Goal Ownership

Goals **MAY** be classified by ownership:

- **Personal goal** — Owned by a single agent.
- **Shared goal** — Jointly pursued by multiple agents.
- **System goal** — Managed by the Cognitive Operating System.

### 12. Memory Placement

Goal instances **SHALL** normally reside in Working Memory while active and **MAY** be archived into Episodic Memory upon completion or failure.

### 13. Replay and Determinism

Replayed executions **MUST** reach equivalent goal states (satisfied or failed) given the same initial conditions and belief evolution.

A conforming implementation **MUST** preserve:

- Goal identity and version across replays.
- The causal chain from actions → effects → belief updates → goal state transitions.

### 14. Open Questions

The following areas require future specification:

- Formal goal satisfaction calculus
- Multi-goal dependency and conflict resolution
- Goal prioritization and scheduling semantics
- Integration with planning (RFC-0005)

---

**RFC-0004 — Goal Lifecycle and Satisfaction Model v1.1** is now ready for **Final Ratification Review**.
