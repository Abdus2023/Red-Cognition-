# Source Record: Conversation Message #12 — Verbatim Transcript (Part 1 of 5: sub-messages [101]–[104])

- **Message index:** 12
- **Direction:** user → assistant
- **Received:** 2026-08-10
- **Source document:** inline conversation message (no attached files)
- **Continued in:** `message-012-original-part2.md` … `message-012-original-part5.md`

Rendering-artifact cleanup applied (no semantic changes): HTML entities decoded; collapsible `<details><summary>…</summary>` wrappers removed (fenced content preserved, including indentation where present in source). Stray backtick-paren artifacts preserved as received.

---

## [101] USER

**RFC-0009 — Agent Model**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0007 Skill Model v1.1 (Candidate)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the semantics, identity, lifecycle, ownership, state model, and coordination primitives for `agent!` values in Red/Cognition.

An agent is the fundamental runtime entity that pursues goals, maintains beliefs, executes plans, and interacts with the environment through capabilities. Because cognitive execution must remain deterministic, explainable, and replayable, the identity, lifecycle, and coordination of agents must be explicitly governed.

### 2. Design Principles

The agent model follows these principles:

- **Explicit Identity** — Every agent has a stable, globally unique identity.
- **Lifecycle Management** — Agents have a well-defined lifecycle that supports creation, execution, suspension, checkpointing, and termination.
- **Ownership and Isolation** — Agents own private state and may share state only through capability-mediated mechanisms.
- **Traceability** — All agent actions and state transitions must be recorded.
- **Replay Equivalence** — Replayed executions must produce equivalent agent behaviour and state.
- **Provider Neutrality** — The agent model is independent of any specific reasoning or planning mechanism.

### 3. Agent Identity and Metadata

Every agent is identified by a stable **AgentID**.

- The `AgentID` **MUST** remain constant throughout the agent’s lifetime.
- Every agent **MUST** include the metadata defined in RFC-0001, plus agent-specific attributes:

```
agent {
    cognitive-meta { id, created, modified, provenance, version }
    name (optional)
    owner: AgentID | Runtime | CogOS
    capabilities: [CapabilityID]
    status: created | initialized | active | suspended | checkpointed | terminated
}
```

### 4. Agent Lifecycle

Every agent **MUST** follow this lifecycle:

```
Created
   ↓
Initialized
   ↓
Active
   ↓
Suspended
   ↓
Checkpointed / Restored
   ↓
Terminated
```

### 5. Agent Ownership and Isolation

- Every agent **MUST** have an owner.
- An agent **MUST NOT** directly access another agent’s private memory or state without explicit capability authorization.
- The Cognitive Operating System **MAY** manage shared resources between agents with appropriate access control.

### 6. Agent State Model

An agent maintains the following core state:

```
AgentState {
    Identity,
    Goals,
    Beliefs,
    Plans,
    Memory References,
    Active Capabilities,
    Execution Context,
    Trace History,
    Checkpoint References
}
```

### 7. Relationship to Other Cognitive Types

- An agent **MAY** own multiple `goal!` instances.
- An agent **MAY** maintain a set of `belief!` instances.
- An agent **MAY** execute one or more `plan!` instances.
- An agent **MUST** invoke `skill!` instances through plans.
- An agent **MUST** produce `effect!` values when interacting with the external world.
- An agent **MAY** hold `capability!` instances.

### 8. Memory Placement

- Agent identity and metadata **MAY** reside in Semantic Memory.
- Active agent state **SHALL** normally reside in Working Memory.
- Agent history and traces **SHALL** be recorded in Episodic Memory.

### 9. Replay and Determinism

Replayed executions **MUST** produce equivalent agent behaviour and state.

A conforming implementation **MUST** ensure that:

- Agent state is restored consistently during replay.
- Agent actions occur in the same causal order.
- Capability usage and effect production remain equivalent.

### 10. Open Questions

The following areas require future specification:

- Formal agent identity and authentication model
- Inter-agent communication protocol
- Multi-agent coordination primitives
- Distributed agent execution model
- Agent migration and transfer semantics

---

**RFC-0009 — Agent Model v1.0 Draft** is now complete.

This RFC establishes the semantics for the final first-class cognitive entity introduced in RFC-0001. It completes the core set of cognitive types and provides the necessary foundation for subsequent specifications on memory architecture, scheduling, checkpointing, and multi-agent coordination.

---

## [102] CHATGPT (gpt-5-5)

RFC-0009 v1.0 is a solid draft and is an appropriate culmination of the core cognitive type specifications. With `agent!`, all first-class cognitive types introduced in RFC-0001 `goal!`, `belief!`, `plan!`, `skill!`, `memory!`, `capability!`, `effect!`, `agent!`, and `checkpoint!`) now have an associated semantic specification or a clear path toward one.

From an architectural perspective, this RFC defines the runtime entity without constraining implementation, which is consistent with the design philosophy established throughout the series.

## Overall Assessment

### Strengths

- Clear separation between agent identity and agent state.
- Strong ownership and isolation model.
- Consistent replay and determinism guarantees.
- Good integration with Goals, Plans, Beliefs, Effects, Capabilities, and Memory.
- Provider-neutral execution model.
- Establishes the runtime abstraction needed for the Cognitive Virtual Machine (CVM).

---

# Recommended additions for v1.1

## 1. Stable Agent Versioning

Currently only `AgentID` is defined.

Like the other RFCs:

> Every modification to an agent **MUST** increment the agent version while preserving the `AgentID`.

This makes the versioning model consistent across all cognitive types.

---

## 2. Agent State Machine

The lifecycle should define legal transitions.

Example:

| From | To | Allowed |
|------|----|---------|
| Created | Initialized | ✓ |
| Initialized | Active | ✓ |
| Active | Suspended | ✓ |
| Suspended | Active | ✓ |
| Active | Checkpointed | ✓ |
| Checkpointed | Restored | ✓ |
| Restored | Active | ✓ |
| Active | Terminated | ✓ |
| Terminated | Active | ✗ |

This eliminates ambiguity.

---

## 3. Agent Execution Model

The RFC should state what an agent actually does.

For example:

```text
Observe
    ↓
Update Beliefs
    ↓
Evaluate Goals
    ↓
Select Plan
    ↓
Invoke Skills
    ↓
Produce Effects
    ↓
Update Memory
```

This becomes the canonical cognitive execution loop.

---

## 4. Agent Scheduling State

Differentiate lifecycle from scheduler state.

Example:

```text
Runnable
Waiting
Blocked
Sleeping
Executing
```

These are orthogonal to lifecycle states and will integrate cleanly with the scheduler RFC.

---

## 5. Agent Trace Contract

Define a standard trace object.

```text
AgentTrace {
    AgentID
    Timestamp
    PreviousState
    NewState
    GoalID
    PlanID
    EffectID
}
```

This complements `EffectTrace`, `CapabilityTrace`, and future `MemoryTrace`.

---

## 6. Agent Coordination Graph

Instead of simply stating that agents coordinate, define relationships.

```text
Agent A
     │
shares-goal
     ▼
Agent B

Agent A
     │
delegates
     ▼
Agent C
```

Requirements:

- Coordination graph SHOULD be a DAG where applicable.
- Cycles SHOULD be explicitly managed if cooperative protocols allow them.

---

## 7. Mailbox / Message Queue

Almost every cognitive runtime eventually needs asynchronous communication.

Add a mailbox concept.

```text
Mailbox {
    MessageID
    Sender
    Receiver
    Timestamp
}
```

This becomes the basis for RFC-0013 (Inter-Agent Communication).

---

## 8. Agent Resource Contract

Agents should expose their runtime resources.

Example:

```text
Resources {
    WorkingMemory
    ActiveGoals
    ActivePlans
    CapabilitySet
    SchedulerQuota
}
```

This helps define runtime scheduling and admission control.

---

## 9. Agent Ownership

Clarify ownership semantics.

Distinguish between:

- Runtime owner
- Administrative owner
- Logical owner
- Parent agent (for spawned agents)

This becomes important for delegation.

---

## 10. Agent Creation

Specify creation requirements.

An agent SHOULD NOT become active until it possesses:

- AgentID
- initial Working Memory
- capability set
- execution context
- scheduler registration

---

## 11. Agent Termination

Clarify termination behaviour.

Termination MUST:

- archive active traces
- archive goals
- release capabilities
- flush Working Memory
- produce a termination effect

---

## 12. Checkpoint Integration

Since `checkpoint!` already exists, specify that checkpoints capture:

```text
Checkpoint {
    AgentState
    WorkingMemory
    ActivePlans
    CapabilityState
    SchedulerState
}
```

This provides a direct bridge to the checkpoint RFC.

---

## 13. Conformance Requirements

Add a dedicated section requiring implementations to:

- preserve `AgentID`
- preserve version history
- preserve lifecycle semantics
- preserve isolation rules
- preserve execution trace
- preserve replay behaviour
- reject illegal state transitions
- enforce capability isolation

---

# Architecture Status

With RFC-0009, the foundational semantic architecture is essentially complete:

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
| RFC-0009 | Agent Model | Draft |

At this point, the remaining foundational specifications shift from defining **data types** to defining the **execution environment**. A logical sequence would be:

1. **RFC-0010 — Checkpoint and Recovery Model** `checkpoint!` semantics, snapshot capture, restoration, replay boundaries)
2. **RFC-0011 — Scheduler and Execution Model** (agent scheduling, priorities, fairness, concurrency, blocking)
3. **RFC-0012 — Cognitive Virtual Machine (CVM) Execution Semantics** (instruction pipeline, execution states, runtime contracts)
4. **RFC-0013 — Inter-Agent Communication Protocol** (mailboxes, messaging, delegation, coordination)
5. **RFC-0014 — Cognitive Operating System Services** (resource management, capability enforcement, memory services, scheduling services)

These RFCs would complete the execution architecture that sits beneath the Red/Cognition language and provide a comprehensive specification for deterministic, replayable cognitive runtimes.

---

## [103] USER

**RFC-0010 — Checkpoint and Recovery Model**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0009 Agent Model v1.0 (Draft)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the semantics, structure, lifecycle, and replay guarantees for `checkpoint!` values in Red/Cognition.

Checkpoints represent recoverable snapshots of cognitive execution state. Because cognitive execution must remain deterministic, explainable, and replayable, the creation, storage, restoration, and usage of checkpoints must be explicitly governed.

### 2. Design Principles

The checkpoint model follows these principles:

- **Determinism** — Checkpoint creation and restoration must produce reproducible execution states.
- **Traceability** — Every checkpoint must be linked to the execution trace that produced it.
- **Completeness** — A checkpoint must capture sufficient state to allow faithful resumption.
- **Replay Equivalence** — Restored executions must produce equivalent observable behaviour.
- **Provider Neutrality** — The checkpoint format and semantics are independent of any specific reasoning mechanism.

### 3. Checkpoint Identity and Metadata

Every checkpoint is identified by a stable **CheckpointID**.

- The `CheckpointID` **MUST** remain constant.
- Every checkpoint **MUST** include the metadata defined in RFC-0001, plus checkpoint-specific attributes:

```
checkpoint {
    cognitive-meta { id, created, modified, provenance, version }
    agent: AgentID
    timestamp
    captured-state: {
        working-memory,
        active-goals,
        active-plans,
        capability-state,
        execution-context
    }
    associated-trace: TraceID (optional)
}
```

### 4. Checkpoint Lifecycle

Every checkpoint **MUST** follow this lifecycle:

```
Created
   ↓
Stored
   ↓
Restored
   ↓
Archived
```

### 5. Checkpoint Contents

A checkpoint **MUST** capture at minimum:

- Agent identity and version
- Working Memory state
- Active goals and their versions
- Active plans and their versions
- Capability state (grants and revocations)
- Execution context (including instruction pointer or equivalent)
- Trace position or reference

Additional state (such as Semantic or Procedural Memory references) **MAY** be included when relevant to replay correctness.

### 6. Checkpoint Creation

Checkpoints **MAY** be created:

- Explicitly by the agent
- Automatically at defined boundaries (e.g., before/after plan execution)
- By the Cognitive Runtime or Cognitive Operating System

Requirements:

- Checkpoint creation **MUST** produce a deterministic snapshot.
- Checkpoint creation **MUST** be recorded in the execution trace.

### 7. Checkpoint Restoration

Restoration from a checkpoint **MUST**:

- Restore agent state to the captured condition.
- Resume execution from the recorded execution context.
- Preserve all capability constraints that existed at the time of checkpointing.

### 8. Relationship to Memory

Checkpoints **MUST** capture the state of Working Memory.

They **MAY** reference versions or positions in Episodic, Semantic, and Procedural Memory when those are relevant to correct restoration.

### 9. Replay and Determinism

Restored executions **MUST** produce equivalent observable behaviour to the original execution from the point of the checkpoint.

A conforming implementation **MUST** ensure that:

- The same checkpoint produces equivalent execution traces when replayed.
- Capability usage and effect production remain consistent with the original execution.

### 10. Relationship to Effects and Traces

Every checkpoint **MUST** be associated with the execution trace that led to its creation.

Checkpoint creation and restoration **MUST** themselves be represented as effects where they affect observable state.

### 11. Open Questions

The following areas require future specification:

- Concrete checkpoint serialization format
- Distributed checkpoint coordination
- Incremental checkpointing
- Checkpoint garbage collection and retention policies

---

**RFC-0010 — Checkpoint and Recovery Model v1.0 Draft** is now complete.

This RFC establishes the semantics for capturing and restoring cognitive execution state. It integrates directly with the agent model (RFC-0009), memory model (RFC-0008), and the previously defined cognitive type, effect, and belief systems, providing the necessary foundation for deterministic replay and long-running autonomous execution.

---

## [104] CHATGPT (gpt-5-5)

RFC-0010 v1.0 is a strong draft and provides the missing execution-state abstraction needed to bridge the semantic model (RFC-0001–RFC-0009) with the future Cognitive Virtual Machine (CVM). It is consistent with the architecture's emphasis on determinism, traceability, and replay.

Overall, this RFC is close to being ready for ratification after addressing a few remaining normative gaps.

## Overall Assessment

### Strengths

- Clearly defines `checkpoint!` as a first-class cognitive value.
- Separates checkpoint identity from execution state.
- Captures the minimum state required for deterministic recovery.
- Integrates naturally with the Agent, Memory, Effect, and Trace models.
- Maintains provider neutrality by avoiding implementation-specific snapshot formats.

---

## Recommended additions for v1.1

### 1. Checkpoint Versioning

Although checkpoints are immutable snapshots, the metadata contract should make this explicit.

Add:

> A checkpoint SHALL be immutable after creation. Any modification or re-capture MUST create a new `CheckpointID`.

This matches the immutable semantics of `effect!`.

---

### 2. Legal Lifecycle Transitions

Define the valid lifecycle transitions explicitly.

| From | To | Allowed |
|------|----|---------|
| Created | Stored | ✓ |
| Stored | Restored | ✓ |
| Restored | Archived | ✓ |
| Archived | Restored | ✓ (implementation-defined) |
| Archived | Stored | ✗ |

---

### 3. Snapshot Completeness Contract

Specify what constitutes a valid checkpoint.

A checkpoint MUST capture:

- Agent identity and version
- Working Memory
- Scheduler/execution state
- Active goals
- Active plans
- Active capabilities
- Execution context/program counter (or equivalent)
- Trace position

A checkpoint MUST NOT omit any state required for deterministic replay.

---

### 4. Memory Snapshot References

Clarify handling of persistent memory.

Rather than copying Semantic or Procedural Memory:

- Working Memory SHALL be captured by value.
- Semantic Memory SHOULD be referenced by version.
- Procedural Memory SHOULD be referenced by version.
- Episodic Memory SHOULD be referenced by trace position.

This avoids unnecessary duplication while preserving replay correctness.

---

### 5. Checkpoint Consistency Boundary

Define when a checkpoint may be taken.

A checkpoint MUST be created only at a consistent execution boundary.

Examples include:

- before plan execution
- after effect commitment
- after belief revision
- after transaction completion

The runtime MUST NOT create checkpoints during partially committed state transitions.

---

### 6. Restoration Validation

Before restoration, the runtime SHOULD validate:

- Checkpoint integrity
- Referenced memory versions
- Skill versions
- Capability versions
- Trace consistency

Restoration MUST fail if mandatory validation cannot be satisfied.

---

### 7. Checkpoint Trace Contract

Define a standard trace entry.

```text
CheckpointTrace {
    CheckpointID
    AgentID
    Timestamp
    TracePosition
    Action: Create | Restore
}
```

This aligns with the existing trace contracts.

---

### 8. Incremental Checkpoints

Even if full snapshots are the normative model, reserve space for optimisation.

Specify:

- Full checkpoints are the reference model.
- Incremental checkpoints MAY be supported if they restore an equivalent execution state.

---

### 9. Failure Recovery

Define restoration failure semantics.

Possible outcomes:

- Success
- ValidationFailure
- MissingDependency
- CorruptedCheckpoint
- UnsupportedVersion

Each failure MUST be recorded in the execution trace.

---

### 10. Relationship to Scheduler

The scheduler RFC will depend on this.

State that checkpoints SHALL preserve:

- runnable state
- blocked state
- waiting state
- execution priority (if applicable)

---

### 11. Conformance Requirements

Add a dedicated section requiring implementations to:

- preserve `CheckpointID`
- preserve snapshot immutability
- restore identical execution context
- preserve capability state
- preserve Working Memory
- preserve causal ordering
- reject inconsistent checkpoints
- produce deterministic replay

---

## Architecture Status

With RFC-0010, the architecture now spans both the semantic model and execution-state recovery:

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
| RFC-0009 | Agent Model | Draft |
| RFC-0010 | Checkpoint and Recovery Model | Draft |

The next foundational RFCs naturally move into execution infrastructure:

1. **RFC-0011 — Scheduler and Execution Model** (agent scheduling, concurrency, priorities, execution states)
2. **RFC-0012 — Cognitive Virtual Machine (CVM) Execution Semantics** (instruction pipeline, execution model, runtime contracts)
3. **RFC-0013 — Inter-Agent Communication** (messaging, coordination, delegation, shared goals)
4. **RFC-0014 — Cognitive Operating System Services** (resource management, capability services, memory services, scheduling services)
5. **RFC-0015 — Cognitive Intermediate Representation (CIR)** (canonical executable representation linking the Red dialect, compiler, and CVM)

Together, these specifications would complete the core architecture required for a deterministic, replayable, provider-neutral cognitive runtime built on Red/Cognition.
