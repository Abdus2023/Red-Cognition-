<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #10, sub-message [87], 2026-08-10
  Verbatim source: knowledge-base/sources/message-010-original-part*.md
  Status in corpus: RFC-0005 Planning Semantics v1.0 (Draft); review [88] accepted with minor revisions and recommended v1.1 — v1.1 document not present in corpus (recorded as missing item).
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0005 — Planning Semantics**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0004 Goal Lifecycle and Satisfaction Model v1.1 (Ratified)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the semantics, lifecycle, relationships, and execution model for `plan!` values in Red/Cognition.

Plans represent the *how* of achieving goals. While goals describe desired outcomes (RFC-0004), plans describe the structured sequences of actions intended to realize those outcomes. Because cognitive execution must remain deterministic, explainable, and replayable, the creation, validation, revision, and execution of plans must be explicitly governed.

### 2. Design Principles

The planning semantics model follows these principles:

- **Goal-driven** — Plans exist to satisfy goals and are evaluated in that context.
- **Determinism** — Plan selection and execution must be reproducible given the same goal, beliefs, and world state.
- **Traceability** — Every plan step and revision must be linked to the originating goal and resulting effects.
- **Capability Awareness** — Plans must respect declared capability requirements.
- **Replay Equivalence** — Replayed executions must follow equivalent plan structures and produce equivalent observable outcomes.

### 3. Plan Identity and Versioning

Every plan is identified by a stable **PlanID**.

- The `PlanID` **MUST** remain constant across revisions.
- Every revision **MUST** increment the plan version while preserving the `PlanID`.
- Historical versions **MUST** remain addressable for replay and auditing.

### 4. Plan Metadata Contract

Every plan **MUST** include the metadata defined in RFC-0001, plus planning-specific attributes:

```
plan {
    cognitive-meta { id, created, modified, provenance, version }
    goal: GoalID
    steps: [step]
    dependencies: [PlanID] (optional)
    preconditions: [condition] (optional)
    expected-effects: [EffectID] (optional)
    required-capabilities: [CapabilityID] (optional)
    status: draft | validated | executable | running | completed | failed | abandoned
}
```

### 5. Plan Lifecycle

Every plan **MUST** follow this lifecycle:

```
Draft
   ↓
Validated
   ↓
Executable
   ↓
Running
   ↓
Completed / Failed / Abandoned
```

### 6. Relationship to Goals

Plans exist to satisfy goals (RFC-0004).

Requirements:

- A plan **MUST** be associated with exactly one goal.
- A goal **MAY** have zero or more associated plans.
- A plan **MUST NOT** be considered successful unless its associated goal is satisfied.

### 7. Relationship to Skills and Effects

Plans are executed through skills and produce effects (RFC-0001, RFC-0002).

Requirements:

- Each plan step **MUST** reference one or more skills.
- Execution of plan steps **MUST** produce traceable effects.
- The set of expected effects declared in a plan **MUST** be consistent with the effects produced during execution.

### 8. Planning as a Process

Planning is the invocation of one or more planning mechanisms (symbolic, rule-based, learned, or human) to generate or revise a plan for a given goal.

The Cognitive Runtime and Cognitive Virtual Machine **MUST** support the invocation of planning mechanisms without embedding any specific planning algorithm.

### 9. Plan Revision and Replanning

Plans **MAY** be revised during execution.

Requirements:

- Plan revisions **MUST** preserve the original `PlanID` while incrementing the version.
- Replanning **MUST** be triggered by belief changes, effect outcomes, or capability revocation.
- All plan revisions **MUST** be recorded in the execution trace.

### 10. Replay and Determinism

Replayed executions **MUST** follow equivalent plan structures.

A conforming implementation **MUST** ensure that:

- The same goal and belief state produce equivalent plan structures during replay.
- Plan revisions occur in the same causal order.
- Execution of plan steps produces equivalent observable effects.

### 11. Open Questions

The following areas require future specification:

- Formal plan validation calculus
- Multi-plan conflict resolution for a single goal
- Learned vs. symbolic planning integration
- Distributed planning across multiple agents

---

**RFC-0005 — Planning Semantics v1.0 Draft** is now complete.

This RFC establishes the semantic foundation for how plans are created, executed, revised, and linked to goals and effects. It forms the next critical layer in the cognitive execution model after goal lifecycle (RFC-0004), belief revision (RFC-0003), and effect ordering (RFC-0002).
