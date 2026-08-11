<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #12, sub-message [101], 2026-08-10
  Verbatim source: knowledge-base/sources/message-012-original-part*.md
  Status in corpus: RFC-0009 Agent Model v1.0 (Draft); review [102] recommends 13 additions for v1.1; v1.1 not present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

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
