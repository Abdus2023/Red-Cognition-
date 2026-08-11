# Source Record: Conversation Message #10 — Verbatim Transcript (Part 5 of 5: sub-messages [97]–[100])

- **Message index:** 10 (continued) · **Part 4:** `message-010-original-part4.md` · **Cleanup:** as Part 1. Source quirks preserved (unmatched backtick-parens in [98]/[99]/[100] prose).

---

## [97] USER

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

---

## [98] CHATGPT (gpt-5-5)

This is a strong evolution from v1.0. RFC-0007 v1.1 is internally consistent with RFC-0001 through RFC-0006 and completes the specification of `skill!` as a first-class cognitive type.

For a final ratified specification (v1.2), there are a few normative gaps worth closing so later RFCs (Memory, Scheduler, Agent, CVM) have less ambiguity.

### Strengths

- Stable `SkillID` with versioning.
- Explicit interface contract (inputs, outputs, pre/postconditions).
- Clear lifecycle.
- Separation between definition `SkillID`) and execution `SkillInvocationID`).
- Capability enforcement aligned with RFC-0006.
- Effect declaration aligned with RFC-0002.
- Replay guarantees aligned with previous RFCs.
- Memory placement consistent with the cognitive memory architecture.

---

## Recommended additions for v1.2

### 1. Immutable Skill Definitions

A compiled skill should behave similarly to immutable code.

Instead of allowing arbitrary modification:

> Every new version MUST increment the skill version...

Add:

> A registered skill definition SHALL be immutable. Any semantic modification MUST create a new version while preserving the SkillID.

This matches the immutable treatment already used for `effect!`.

---

### 2. Deterministic Invocation Contract

Skill replay currently says "same inputs".

Specify exactly what determines execution.

```
A skill invocation is uniquely determined by:
- SkillID
- Skill Version
- Inputs
- Runtime Context
- Capability Set
- Relevant Belief State
```

This prevents replay ambiguity.

---

### 3. Skill Dependency Graph

Real skills invoke other skills.

Add:

```
Skill A
    |
    | invokes
    ▼
Skill B
```

Requirements:

- Dependency graph MUST be a DAG.
- Cycles MUST be rejected.
- Recursive execution MUST be explicitly declared if supported.

This mirrors previous DAG-based RFCs.

---

### 4. Invocation Lifecycle

Current RFC only defines the lifecycle of the skill definition.

Invocation should also have one.

```
Created
    ↓
Validated
    ↓
Authorized
    ↓
Executing
    ↓
Completed / Failed
    ↓
Archived
```

This aligns perfectly with Effects.

---

### 5. Skill Trace Contract

Instead of only `SkillInvocation`, define a trace object.

```
SkillTrace {
    SkillInvocationID
    SkillID
    PlanID
    GoalID
    StartTime
    EndTime
    Status
    EffectsProduced
    CapabilitiesUsed
}
```

This integrates directly into execution traces.

---

### 6. Purity Enforcement

Currently skills are merely classified.

Instead add normative behaviour.

For example:

- `pure!` MUST NOT emit `external!` effects.
- `internal!` MUST NOT modify external state.
- `capability!` MUST declare required capabilities.
- `external!` MUST pass capability validation before execution.

This removes ambiguity.

---

### 7. Skill Registration

The lifecycle begins with "Registered" but never specifies registration.

Define that registration MUST validate:

- interface
- declared effects
- capability declarations
- metadata completeness
- version consistency

---

### 8. Relationship to Beliefs

A skill may consume beliefs.

Add:

- Skills MAY declare required beliefs.
- Skills MAY produce belief-changing effects.
- Belief changes MUST occur only through `effect!` values.

This keeps RFC-0003 authoritative.

---

### 9. Relationship to Memory

Currently only placement is defined.

Specify access.

```
Skills MAY
- read Working Memory
- read Semantic Memory
- append Episodic Memory

Skills MUST NOT directly mutate Semantic Memory.
All memory modifications MUST occur through effects.
```

This is a strong architectural rule.

---

### 10. Conformance

Add:

A conforming implementation MUST:

- preserve `SkillInvocationID`
- preserve invocation order during replay
- reject invalid interface contracts
- reject undeclared external effects
- reject capability violations before execution
- preserve execution provenance

---

## Overall Assessment

The current RFC series now forms a coherent cognitive architecture:

| RFC | Domain | Status |
|------|--------|--------|
| RFC-0001 | Cognitive Type System | Complete |
| RFC-0002 | Effect Ordering | Complete |
| RFC-0003 | Belief Revision | Complete |
| RFC-0004 | Goal Lifecycle | Complete |
| RFC-0005 | Planning Semantics | Draft |
| RFC-0006 | Capability Model | Complete |
| RFC-0007 | Skill Model | Candidate |

Together, these documents define the core semantic model for Red/Cognition: a goal-oriented cognitive system in which plans invoke versioned skills, skills produce ordered effects, effects update beliefs, capabilities authorize external actions, and all state transitions remain deterministic, traceable, replayable, and suitable for execution by the Cognitive Virtual Machine (CVM).

The next logical specifications are:

1. **RFC-0008 — Memory Model** (Working, Semantic, Episodic, Procedural Memory)
2. **RFC-0009 — Agent Model** `agent!` lifecycle and coordination)
3. **RFC-0010 — Checkpoint and Recovery Model**
4. **RFC-0011 — Cognitive Scheduler**
5. **RFC-0012 — Cognitive Virtual Machine (CVM) Execution Semantics**

These would complete the foundational architecture before moving on to higher-level language syntax and runtime implementation.

---

## [99] USER

**RFC-0008 — Memory Model**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0007 Skill Model v1.1 (Candidate)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the architecture, semantics, ownership, access rules, and persistence model for the four-tier cognitive memory system in Red/Cognition.

The memory model provides the foundation for storing, retrieving, and managing knowledge, experiences, procedures, and current context across cognitive agents. Because cognitive execution must remain deterministic, explainable, and replayable, the memory architecture must be explicitly governed.

### 2. Design Principles

The memory model follows these principles:

- **Determinism** — Memory operations must produce reproducible results given the same inputs and state.
- **Ownership** — Every memory entry has a defined owner (agent, runtime, or system).
- **Traceability** — All memory mutations must be recorded with provenance.
- **Replay Equivalence** — Replayed executions must observe equivalent memory states.
- **Layered Isolation** — Different memory tiers have distinct access patterns and persistence requirements.

### 3. Memory Tiers

Red/Cognition defines four memory tiers:

| Tier                | Purpose                              | Persistence     | Ownership       | Mutation Events |
|---------------------|--------------------------------------|-----------------|-----------------|-----------------|
| **Working Memory**  | Current execution context            | Ephemeral       | Per agent       | Yes             |
| **Episodic Memory** | Events, experiences, and traces      | Persistent      | Per agent       | Yes             |
| **Semantic Memory** | Knowledge, concepts, and facts       | Persistent      | Shared          | Yes             |
| **Procedural Memory** | Skills, compiled procedures, and capabilities | Persistent | Shared     | Yes             |

### 4. Memory Access Rules

#### 4.1 Working Memory

- **Read/Write**: Agent may freely read and write.
- **Scope**: Limited to current execution context.
- **Eviction**: Bounded capacity; older entries may be evicted.

#### 4.2 Episodic Memory

- **Read**: Agent may read its own episodes.
- **Write**: Agent may append new episodes (via `effect!`).
- **Mutation**: Historical episodes are immutable after creation.

#### 4.3 Semantic Memory

- **Read**: Agents may read shared knowledge.
- **Write**: Controlled by capability or system policy.
- **Mutation**: Updates create new versions or revisions.

#### 4.4 Procedural Memory

- **Read**: Agents and runtime may read compiled skills.
- **Write**: Controlled by system registration process.
- **Mutation**: New versions create new `skill!` entries.

### 5. Memory Ownership and Isolation

- Every memory entry **MUST** have an owner.
- Agents **MUST NOT** directly access another agent’s private memory without capability authorization.
- The Cognitive Operating System **MAY** manage shared semantic and procedural memory with appropriate access control.

### 6. Memory Mutation and Effects

All memory mutations that affect external observability or agent state **MUST** be represented as `effect!` values (RFC-0002).

Requirements:

- Memory writes that change observable state **MUST** produce effects.
- Effects **MUST** carry provenance linking them to the originating action.

### 7. Replay and Determinism

Replayed executions **MUST** observe equivalent memory states.

A conforming implementation **MUST** ensure that:

- Memory reads during replay return values consistent with the original execution trace.
- Memory mutations occur in the same causal order.
- Checkpoint restoration restores memory state to a replayable condition.

### 8. Relationship to Other Cognitive Types

- **Goals** `goal!`) normally reside in Working Memory while active.
- **Beliefs** `belief!`) normally reside in Semantic Memory.
- **Plans** `plan!`) normally reside in Working Memory while active.
- **Skills** `skill!`) are stored in Procedural Memory.
- **Effects** `effect!`) are appended to Episodic Memory.

### 9. Open Questions

The following areas require future specification:

- Concrete memory storage formats and serialization
- Distributed memory consistency model
- Memory garbage collection and forgetting policies
- Privacy and access control for shared memory

---

**RFC-0008 — Memory Model v1.0 Draft** is now complete.

This RFC establishes the architectural foundation for how cognitive agents store, access, and manage different types of knowledge and experience. It integrates directly with the cognitive type system (RFC-0001), effect model (RFC-0002), and the previously defined cognitive runtime and virtual machine layers.

---

## [100] CHATGPT (gpt-5-5)

RFC-0008 v1.0 is a natural continuation of RFC-0001 through RFC-0007. It establishes the cognitive memory architecture without prescribing a storage implementation, which is consistent with the provider-neutral philosophy of the specification.

Overall, I would consider this a solid draft. Before ratification, however, there are several normative areas that would benefit from clarification.

## Overall Assessment

**Strengths**

- Defines a clear four-tier memory architecture.
- Separates persistence from execution semantics.
- Consistent with previous RFCs regarding determinism, provenance, and replay.
- Keeps storage implementation independent.
- Aligns naturally with the cognitive type system.

---

## Recommended additions for v1.1

### 1. Memory Identity

Every memory object should have a stable identity.

```text
memory {
    MemoryID
    cognitive-meta { ... }
    tier
    owner
    status
}
```

Requirements:

- MemoryID MUST remain stable.
- Every revision MUST increment version.
- Historical versions MUST remain addressable.

---

### 2. Memory Lifecycle

Currently only tiers are defined.

A memory object should also have a lifecycle.

```text
Created
    ↓
Active
    ↓
Updated
    ↓
Archived
    ↓
Deleted (optional)
```

Deletion should normally be logical rather than physical.

---

### 3. Memory Access Contract

Instead of only describing read/write permissions, define a standard interface.

```text
read
write
append
update
archive
forget
```

Each operation should specify:

- required capability
- trace requirement
- replay semantics

---

### 4. Memory Reference Model

Objects should reference memory instead of copying data.

For example:

```text
goal
   ↓
belief
   ↓
memory
```

Introduce:

- MemoryReference
- MemoryEntry
- MemorySnapshot

This will simplify checkpoints later.

---

### 5. Working Memory Semantics

Working Memory deserves stronger guarantees.

Specify that it:

- is agent-local
- is execution-scoped
- is automatically reconstructed during replay
- is never authoritative

The authoritative data remains in Semantic/Episodic Memory.

---

### 6. Episodic Memory

Specify append-only semantics.

Normative statement:

> Episodic Memory SHALL be append-only.

Existing entries MUST NOT be modified.

Corrections become new episodes.

This matches the immutable `effect!` model.

---

### 7. Semantic Memory

Specify belief revision behaviour.

Instead of replacing beliefs:

- revisions create new versions
- previous versions remain accessible
- retrieval policy is implementation-defined but deterministic

This aligns with RFC-0003.

---

### 8. Procedural Memory

Specify registration.

Only registered skills should exist here.

Add:

- validation
- version verification
- capability declaration verification
- interface verification

---

### 9. Memory Dependency Graph

Relationships should form a graph.

```text
Working
     │
     ▼
Semantic

Working
     │
     ▼
Procedural

Effects
     │
     ▼
Episodic
```

This graph will later support checkpointing.

---

### 10. Memory Consistency

Define consistency guarantees.

Working Memory:

- immediate consistency

Semantic Memory:

- deterministic consistency

Procedural Memory:

- version consistency

Episodic Memory:

- append consistency

---

### 11. Memory Snapshot Contract

Since `checkpoint!` already exists, memory should define snapshots.

```text
MemorySnapshot {
    SnapshotID
    Timestamp
    WorkingMemory
    SemanticVersion
    ProceduralVersion
    EpisodicPosition
}
```

This becomes the bridge to the checkpoint RFC.

---

### 12. Forgetting

Currently listed as an open question.

Introduce normative rules.

Forgetting MUST:

- preserve provenance
- preserve replay correctness
- never invalidate historical traces

This allows safe garbage collection.

---

### 13. Capability Integration

Specify capability requirements.

Example:

| Operation | Capability |
|-----------|------------|
| Read Semantic | optional |
| Modify Semantic | required |
| Register Skill | required |
| Read Other Agent Memory | required |
| Archive Memory | system |

---

### 14. Memory Trace

Every mutation should produce a trace.

```text
MemoryTrace {
    MemoryID
    Tier
    Operation
    AgentID
    Timestamp
    Provenance
}
```

This complements `EffectTrace` and `CapabilityTrace`.

---

### 15. Conformance Requirements

A conforming implementation SHOULD explicitly guarantee that it:

- preserves `MemoryID`
- preserves version history
- preserves ownership
- records every mutation
- preserves replay equivalence
- enforces access control
- prevents cross-agent memory violations without capability authorization

## Architecture Status

With RFC-0008, the architecture now covers nearly all foundational cognitive abstractions:

| RFC | Subject | Status |
|------|---------|--------|
| RFC-0001 | Cognitive Type System | Ratified |
| RFC-0002 | Effect Ordering | Ratification-ready |
| RFC-0003 | Belief Revision | Ratification-ready |
| RFC-0004 | Goal Lifecycle | Ratification-ready |
| RFC-0005 | Planning Semantics | Draft |
| RFC-0006 | Capability Model | Ratification-ready |
| RFC-0007 | Skill Model | Ratification-ready |
| RFC-0008 | Memory Model | Draft |

The next logical RFCs would be:

1. **RFC-0009 — Agent Model** `agent!` identity, lifecycle, ownership, coordination)
2. **RFC-0010 — Checkpoint and Recovery Model** `checkpoint!` semantics, snapshots, replay, restoration)
3. **RFC-0011 — Scheduler and Execution Model** (task scheduling, concurrency, priorities, fairness)
4. **RFC-0012 — Cognitive Virtual Machine (CVM) Execution Semantics** (execution pipeline, instruction model, runtime behaviour)

These would complete the core execution model before defining concrete language syntax, compiler behaviour, or implementation-specific runtime details.
