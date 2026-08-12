<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #10, sub-message [97], 2026-08-10
  Verbatim source: knowledge-base/sources/message-010-original-part*.md
  Status in corpus: RFC-0007 Skill Model v1.1 (Candidate for Ratification); review [98] recommends v1.2 additions; v1.2 not present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0007 — Skill Model**

**Version:** 1.1  

**Status:** Candidate for Ratification  

**Parent:** RFC-0001 Cognitive Type System v1.2 (Ratified)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the semantics, lifecycle, metadata, relationships, and execution model for `skill!` values in Red/Cognition.

Skills represent compiled, reusable procedures or capabilities that can be invoked as part of plans. While plans describe *how* to achieve goals, skills represent the executable units that actually carry out the work. Because cognitive execution must remain deterministic, explainable, and replayable, the creation, versioning, invocation, and effects of skills must be explicitly governed.

### 2. Design Principles

The skill model follows these principles:

- **Compiled and Reusable** — A skill represents a pre-compiled unit of behaviour that can be invoked multiple times.
- **Effect Declaration** — Every skill **MUST** declare the effects it may produce.
- **Capability Awareness** — Skill invocation **MUST** respect required capabilities.
- **Determinism** — Skill execution must be reproducible given the same inputs and state.
- **Traceability** — Every skill invocation must produce a traceable execution record.
- **Provider Neutrality** — Skills may be implemented through any mechanism (symbolic, rule-based, learned, or human) provided they conform to the declared interface.

### 3. Skill Identity and Metadata

Every skill is identified by a stable **SkillID**.

- The `SkillID` **MUST** remain constant across versions.
- Every new version **MUST** increment the skill version while preserving the `SkillID`.
- Every skill **MUST** include the metadata defined in RFC-0001, plus skill-specific attributes:

```
skill {
    cognitive-meta { id, created, modified, provenance, version }
    name
    specification: [parameter]
    inputs: [parameter]
    outputs: [parameter]
    preconditions: [condition] (optional)
    postconditions: [condition] (optional)
    declared-effects: [EffectClass]
    required-capabilities: [CapabilityID] (optional)
    performance-metadata: { ... } (optional)
}
```

### 4. Skill Lifecycle

Every skill **MUST** follow this lifecycle:

```
Created
   ↓
Registered
   ↓
Active
   ↓
Deprecated
   ↓
Archived
```

**Legal status transitions**:

| From       | To         | Allowed |
|------------|------------|---------|
| Created    | Registered | ✓       |
| Registered | Active     | ✓       |
| Active     | Deprecated | ✓       |
| Deprecated | Archived   | ✓       |
| Archived   | Active     | ✗       |

### 5. Skill Interface Contract

Every skill **MUST** declare:

- Inputs
- Outputs
- Preconditions
- Postconditions
- Declared effects
- Required capabilities

This creates a complete executable contract for skill invocation.

### 6. Skill Purity Classification

Skills **MAY** be classified by purity:

- `pure!` — No observable side effects
- `internal!` — Internal state changes only
- `capability!` — Requires explicit capability authorization
- `external!` — Produces direct external state changes

### 7. Relationship to Plans and Effects

Skills are the executable units invoked by plans (RFC-0005).

Requirements:

- Each plan step **MUST** reference one or more skills.
- Skill execution **MUST** produce effects that are consistent with the skill’s declared effects.
- Effects produced by a skill **MUST** be traceable back to the invoking plan and originating goal.

### 8. Relationship to Capabilities

Skill invocation that produces external effects **MUST** be mediated by capabilities (RFC-0006).

Requirements:

- A skill **MAY** declare required capabilities.
- The Cognitive Runtime **MUST** verify required capabilities before allowing a skill to produce external effects.

### 9. Skill Invocation Identity

Every skill invocation **MUST** be identified by a **SkillInvocationID**.

Every invocation **MUST** record:

```
SkillInvocation {
    SkillInvocationID,
    SkillID,
    PlanID,
    GoalID,
    Timestamp,
    Inputs,
    Outputs,
    Effects,
    CapabilitiesUsed
}
```

### 10. Skill Failure Semantics

Skill execution **MAY** terminate in failure.

Requirements:

- Failures **MUST** produce trace entries.
- Failures **MAY** produce compensating effects.
- Failures **MUST** be replayable.

### 11. Memory Placement

- Active skill definitions **MAY** reside in Semantic Memory.
- Skill invocations and their traces **SHALL** normally reside in Episodic Memory.
- Compiled skill implementations **MAY** reside in Procedural Memory.

### 12. Replay and Determinism

Replayed executions **MUST** invoke skills in the same causal order and produce equivalent observable effects.

A conforming implementation **MUST** ensure that:

- The same inputs and state produce equivalent skill behaviour during replay.
- Skill versioning is respected (older versions may be required for exact replay).

### 13. Conformance Requirements

A conforming implementation **MUST**:

- Preserve `SkillID`.
- Preserve skill versioning.
- Enforce declared capabilities.
- Produce execution traces.
- Preserve skill identity during replay.
- Respect declared effects.

### 14. Open Questions

The following areas require future specification:

- Formal skill interface definition language
- Skill composition and chaining semantics
- Learned skill acquisition and verification
- Distributed skill execution model

---

**RFC-0007 — Skill Model v1.1** is now ready for **Final Ratification Review**.
