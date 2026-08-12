<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #10, sub-message [99], 2026-08-10
  Verbatim source: knowledge-base/sources/message-010-original-part*.md
  Status in corpus: RFC-0008 Memory Model v1.0 (Draft); review [100] recommends 15 additions for v1.1; v1.1 not present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

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
