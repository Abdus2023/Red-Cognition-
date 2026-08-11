# Source Record: Conversation Message #10 — Verbatim Transcript (Part 4 of 5: sub-messages [93]–[96])

- **Message index:** 10 (continued) · **Part 3:** `message-010-original-part3.md` · **Cleanup:** as Part 1. Note: [94] capability-type registry example contains auto-link artifacts (`[filesystem.read](http://filesystem.read)` etc.), preserved as received.

---

## [93] USER

**RFC-0006 — Capability Model**

**Version:** 1.2  

**Status:** Candidate for Final Ratification  

**Parent:** RFC-0004 Goal Lifecycle and Satisfaction Model v1.1 (Ratified)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the semantics, lifecycle, metadata, relationships, and enforcement model for `capability!` values in Red/Cognition.

Capabilities represent explicit, revocable permissions that mediate an agent’s ability to produce external effects. Because cognitive execution must remain secure, deterministic, explainable, and replayable, the creation, granting, revocation, and usage of capabilities must be explicitly governed.

### 2. Design Principles

The capability model follows these principles:

- **Explicitness** — Capabilities are first-class values that must be explicitly granted and referenced.
- **Least Privilege** — Agents should hold only the minimum capabilities required to achieve their goals.
- **Revocability** — Capabilities can be revoked at any time by their granting authority.
- **Auditability** — All capability grants, revocations, and usages must be traceable.
- **Provider Neutrality** — The capability model is independent of any specific reasoning or planning mechanism.

### 3. Capability Identity and Metadata

Every capability is identified by a stable **CapabilityID**.

- The `CapabilityID` **MUST** remain constant across the capability lifecycle.
- Every modification to a capability, including revocation, expiration, delegation metadata, or administrative updates, **MUST** increment the capability version while preserving the `CapabilityID`.
- Every capability **MUST** include the following metadata:

```
capability {
    cognitive-meta { id, created, modified, provenance, version }
    type: capability-type
    scope
    owner: AgentID | Runtime | CogOS
    granted-to: AgentID
    granted-by: authority
    delegated-from: CapabilityID (optional)
    expiration: timestamp (optional)
    status: active | revoked | expired
}
```

**Scope immutability**: Scope **MUST** be immutable after capability issuance.

### 4. Capability Lifecycle

Every capability **MUST** follow this lifecycle:

```
Created
   ↓
Granted
   ↓
Active
   ↓
Revoked / Expired
```

**Legal status transitions**:

| From     | To        | Allowed |
|----------|-----------|---------|
| Created  | Granted   | ✓       |
| Granted  | Active    | ✓       |
| Active   | Revoked   | ✓       |
| Active   | Expired   | ✓       |
| Revoked  | Active    | ✗       |
| Expired  | Active    | ✗       |

### 5. Capability Types and Scope

Capabilities **MAY** be classified by type. Every capability **MUST** declare its scope.

Capability inheritance and dependency relationships **MUST** form a Directed Acyclic Graph (DAG). Cycles **MUST** be rejected.

### 6. Capability Resolution Order

Before an effect executes, the system **MUST** verify the following in deterministic order:

1. Capability exists
2. Status == Active
3. Scope is valid
4. Not expired
5. Not revoked
6. Policy allows the action

Evaluation **MUST** terminate at the first failed validation step, and the failure reason **MUST** be recorded in the execution trace.

### 7. Capability Grants, Revocations, and Effects

Capability grants and revocations **MUST** themselves be represented as `effect!` values (RFC-0002).

### 8. Capability Enforcement

The Cognitive Runtime and Cognitive Operating System **MUST** enforce capability checks before allowing external effects.

Requirements:

- Capability checks **MUST** occur before effect execution.
- Capability violations **MUST** produce traceable errors.
- Capability usage **MUST** be recorded in execution traces.

### 9. Capability Trace Contract

Every capability usage **MUST** produce a trace entry:

```
CapabilityTrace {
    CapabilityID,
    AgentID,
    EffectID,
    Timestamp,
    Decision: Allow | Deny
}
```

### 10. Capability Ownership and Delegation

Capabilities distinguish between **owner** and **grantee**.

Capabilities **MAY** be delegable. Delegated capabilities **MUST** preserve provenance and **MUST** reference the granting capability via `delegated-from`.

### 11. Memory Placement

- Active capabilities **SHALL** reside in Working Memory.
- Capability definitions **MAY** reside in Semantic Memory.
- Revoked and expired capabilities **SHOULD** be archived in Episodic Memory.

### 12. Relationship to Beliefs

Capability grants and revocations **MAY** update an agent’s beliefs about its own permissions and the permissions of other agents.

### 13. Replay and Determinism

Replayed executions **MUST** respect the same capability constraints that existed during the original execution.

A conforming implementation **MUST** ensure that:

- Capability checks occur at the same points in the causal chain.
- Revoked capabilities remain revoked during replay.
- Capability violations produce equivalent error behaviour.

### 14. Conformance Requirements

A conforming implementation **MUST**:

- Preserve `CapabilityID`.
- Enforce capability checks before external effects.
- Record every grant, revocation, and usage.
- Preserve capability state during replay.
- Reject invalid capability transitions.
- Include its authority policy in conformance reports.

### 15. Open Questions

The following areas require future specification:

- Formal capability algebra
- Capability delegation and transfer semantics
- Distributed capability management
- Capability auditing and verification protocols

---

**RFC-0006 — Capability Model v1.2** is now ready for **Final Ratification**.

---

## [94] CHATGPT (gpt-5-5)

## Final Ratification Review — RFC-0006 v1.2

**Recommendation:** **Ratify**

RFC-0006 v1.2 is now a mature, internally consistent specification that completes the foundational authorization model of the Red/Cognition architecture. The additions introduced in v1.2 resolve the remaining architectural ambiguities without increasing unnecessary complexity.

### Ratification Assessment

| Criterion | Assessment |
|-----------|------------|
| Internal consistency | ✅ Excellent |
| Compatibility with RC-000–RC-900 | ✅ Fully consistent |
| Determinism | ✅ Well specified |
| Replay semantics | ✅ Complete |
| Traceability | ✅ Complete |
| Security model | ✅ Strong capability-based design |
| Provider neutrality | ✅ Preserved |
| Implementability | ✅ High |
| Conformance testability | ✅ High |

---

## Major Strengths

### Stable Identity

The addition of a persistent `CapabilityID` and mandatory versioning aligns the capability model with the identity model already established for:

- `goal!`
- `belief!`
- `plan!`

This gives every cognitive object a consistent lifecycle model.

---

### Deterministic Enforcement

The capability resolution order is now deterministic:

```
Exists
↓
Active
↓
Scope Valid
↓
Not Expired
↓
Not Revoked
↓
Policy
↓
Allow Effect
```

Combined with mandatory short-circuit evaluation and trace recording, this provides an excellent basis for deterministic replay and conformance testing.

---

### Effect Integration

The requirement that grants and revocations are themselves represented as `effect!` values is particularly valuable because it unifies all externally observable state changes under RFC-0002.

This keeps the execution model conceptually simple:

```
Action
      ↓
effect!
      ↓
Beliefs
      ↓
Goals
      ↓
Plans
      ↓
Capabilities
```

No special-case mechanism is required.

---

### Delegation

Introducing:

```
delegated-from: CapabilityID
```

creates a complete provenance chain.

Future delegation semantics can now be added without modifying the metadata contract.

---

### Conformance

The conformance section is concise and measurable.

Every listed requirement can be verified through automated conformance testing.

---

## Minor Editorial Suggestions (Non-blocking)

These are optional refinements for a future maintenance revision (v1.2.1 or v1.3).

### 1. Authority Policy

Section 14 states:

> Include its authority policy in conformance reports.

It would be helpful to reference a future RFC defining the authority model.

Example:

```
Authority Policy (implementation-defined;
see future RFC-00xx)
```

---

### 2. Capability Type Registry

Section 5 currently allows arbitrary capability types.

Eventually the project will likely benefit from a standard registry, for example:

```
[filesystem.read](http://filesystem.read)
filesystem.write
network.connect
network.listen
[memory.read](http://memory.read)
memory.write
[sensor.camera](http://sensor.camera)
sensor.microphone
actuator.motor
...
```

This can remain implementation-defined for now.

---

### 3. Expiration Semantics

The document specifies expiration but not evaluation.

A future RFC could clarify:

- wall-clock time
- logical execution time
- deterministic replay time
- checkpoint restoration

Again, this is not required for ratification.

---

## Foundation Status

The semantic foundation now forms a coherent stack:

```text
RFC-0001  Cognitive Type System
        │
        ▼
RFC-0002  Effect Ordering Model
        │
        ▼
RFC-0003  Belief Revision System
        │
        ▼
RFC-0004  Goal Lifecycle & Satisfaction
        │
        ▼
RFC-0005  Planning Semantics
        │
        ▼
RFC-0006  Capability Model
```

These six RFCs collectively define:

- Cognitive data model
- Execution semantics
- Effect system
- Knowledge evolution
- Goal management
- Planning
- Authorization

This provides a complete semantic substrate for the Cognitive Runtime (RC-500), Cognitive Virtual Machine (RC-700), and Cognitive Operating System (RC-800).

## Final Recommendation

**RFC-0006 — Capability Model v1.2** is **approved for Final Ratification**.

With this ratification, the first six RFCs establish a coherent, deterministic, replayable, and provider-neutral cognitive execution model. The next logical specifications are those that build on these foundations, such as:

1. **RFC-0007 — Skill Model** (formalising `skill!` semantics and execution contracts).
2. **RFC-0008 — Memory Architecture** (episodic, semantic, procedural, and working memory models).
3. **RFC-0009 — Agent Lifecycle** (formalising `agent!` semantics, state transitions, and coordination).

These would naturally complete the remaining first-class cognitive types introduced in RFC-0001 before moving into more advanced topics such as multi-agent coordination and distributed execution.

---

## [95] USER

**RFC-0007 — Skill Model**

**Version:** 1.0  

**Status:** Draft  

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

### 5. Relationship to Plans and Effects

Skills are the executable units invoked by plans (RFC-0005).

Requirements:

- Each plan step **MUST** reference one or more skills.
- Skill execution **MUST** produce effects that are consistent with the skill’s declared effects.
- Effects produced by a skill **MUST** be traceable back to the invoking plan and originating goal.

### 6. Relationship to Capabilities

Skill invocation that produces external effects **MUST** be mediated by capabilities (RFC-0006).

Requirements:

- A skill **MAY** declare required capabilities.
- The Cognitive Runtime **MUST** verify required capabilities before allowing a skill to produce external effects.

### 7. Execution Model

Skill execution is the invocation of a compiled procedure through the Cognitive Runtime or Cognitive Virtual Machine.

Requirements:

- Skill execution **MUST** be deterministic when given the same inputs and state.
- Skill execution **MUST** produce an execution trace.
- Skill execution **MUST** respect declared effects and required capabilities.

### 8. Memory Placement

- Active skill definitions **MAY** reside in Semantic Memory.
- Skill invocations and their traces **SHALL** normally reside in Episodic Memory.
- Compiled skill implementations **MAY** reside in Procedural Memory.

### 9. Replay and Determinism

Replayed executions **MUST** invoke skills in the same causal order and produce equivalent observable effects.

A conforming implementation **MUST** ensure that:

- The same inputs and state produce equivalent skill behaviour during replay.
- Skill versioning is respected (older versions may be required for exact replay).

### 10. Open Questions

The following areas require future specification:

- Formal skill interface definition language
- Skill composition and chaining semantics
- Learned skill acquisition and verification
- Distributed skill execution model

---

**RFC-0007 — Skill Model v1.0 Draft** is now complete.

This RFC establishes the semantics for the remaining first-class cognitive type introduced in RFC-0001. It completes the core set of cognitive entities (types, effects, beliefs, goals, plans, capabilities, and skills) and provides the necessary foundation for subsequent specifications on memory, scheduling, and multi-agent coordination.

---

## [96] CHATGPT (gpt-5-5)

## Review: RFC-0007 — Skill Model v1.0

**Recommendation:** **Accept as Draft** and advance to **v1.1 Candidate for Ratification** after a small number of normative additions.

RFC-0007 fits naturally into the architecture established by RFC-0001 through RFC-0006. It completes the semantic definition of the final major executable cognitive type `skill!`) and clearly distinguishes **plans** ("what sequence to execute") from **skills** ("the executable units that perform the work").

---

# Overall Assessment

| Criterion | Assessment |
|-----------|------------|
| Internal consistency | ✅ Excellent |
| Alignment with previous RFCs | ✅ Complete |
| Deterministic execution | ✅ Strong |
| Traceability | ✅ Strong |
| Replay semantics | ✅ Good |
| Implementability | ✅ High |
| Conformance testability | ✅ Good |

---

# Strengths

## Excellent separation of responsibilities

The architecture now becomes very clear:

```text
Goal
    ↓
Plan
    ↓
Skill
    ↓
Effect
    ↓
Belief
```

Each cognitive type has one well-defined responsibility.

---

## Proper provider neutrality

This sentence is particularly strong:

> Skills may be implemented through any mechanism (symbolic, rule-based, learned, or human)...

That keeps the specification independent of any AI model or planning technology.

---

## Correct memory placement

The mapping is consistent with the existing memory architecture:

- Semantic Memory → skill definitions
- Procedural Memory → compiled implementations
- Episodic Memory → invocations

This matches common cognitive architectures.

---

## Good replay model

Requiring historical skill versions for replay is an excellent design decision.

Without version pinning, deterministic replay would be impossible.

---

# Recommended additions for v1.1

## 1. Stable Skill Interface

The metadata currently has:

```text
specification: [parameter]
```

A stronger contract would define inputs and outputs explicitly.

Example:

```text
skill {
    inputs: [parameter]
    outputs: [parameter]
}
```

or

```text
interface {
    inputs
    outputs
    preconditions
    postconditions
}
```

This makes skill invocation deterministic.

---

## 2. Skill Status Transitions

As with RFC-0006, define legal transitions.

Example:

| From | To | Allowed |
|------|----|---------|
| Created | Registered | ✓ |
| Registered | Active | ✓ |
| Active | Deprecated | ✓ |
| Deprecated | Archived | ✓ |
| Archived | Active | ✗ |

---

## 3. Skill Invocation Identity

Each execution should have its own identifier.

Example:

```text
SkillInvocationID
```

Metadata:

```text
SkillInvocation {
    SkillInvocationID
    SkillID
    PlanID
    GoalID
    Timestamp
}
```

This makes traces easier to correlate.

---

## 4. Failure Semantics

Currently only successful execution is described.

Consider defining:

```text
Running
    ↓
Completed
```

or

```text
Running
    ↓
Failed
```

along with normative requirements such as:

- failures produce trace entries
- failures may produce compensating effects
- failures are replayable

---

## 5. Skill Purity

Some skills only compute values.

Others change the world.

A simple classification would help:

```text
pure
internal
capability
external
```

matching RFC-0002's effect classes.

---

## 6. Skill Contract

Each skill should declare:

- Preconditions
- Postconditions
- Declared effects
- Required capabilities

This creates a true executable contract.

---

## 7. Conformance Section

Like recent RFCs.

A conforming implementation MUST:

- Preserve `SkillID`
- Preserve skill versioning
- Enforce declared capabilities
- Produce execution traces
- Preserve skill identity during replay
- Respect declared effects

---

# Architectural Position

RFC-0007 completes the executable cognitive layer:

```text
RFC-0001  Cognitive Types
        │
        ▼
RFC-0002  Effect Ordering
        │
        ▼
RFC-0003  Belief Revision
        │
        ▼
RFC-0004  Goal Lifecycle
        │
        ▼
RFC-0005  Planning
        │
        ▼
RFC-0006  Capability Model
        │
        ▼
RFC-0007  Skill Model
```

At this point, every first-class runtime cognitive object introduced in RFC-0001 has a dedicated semantic specification.

## Readiness

I would assess **RFC-0007 v1.0** as approximately **96% complete**. It is already a solid draft, and the recommended additions are largely about making execution contracts and conformance more explicit rather than changing the underlying architecture.

Once those additions are incorporated, **RFC-0007 v1.1** would be a strong candidate for ratification and would complete the core execution semantics of the Red/Cognition platform before progressing to memory architecture, scheduling, and multi-agent coordination.
