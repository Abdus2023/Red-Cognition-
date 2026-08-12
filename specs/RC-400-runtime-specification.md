<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #5, sub-message [55], 2026-08-10
  Verbatim source: knowledge-base/sources/message-005-original-part*.md
  Status in corpus: RC-400 Runtime Specification v1.0 (Draft); review [56] recommends v1.1 candidate after amendments.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates specs/ for specifications.
  Content below is the document text exactly as provided (no edits).
-->

**RC-400 Runtime Specification**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RC-300 Compiler Specification v1.0 (Candidate)  

**Authority:** Normative Specification  

**Date:** 2026-07-29

---

### 1. Introduction

RC-400 defines the runtime architecture for Red/Cognition. It specifies how the runtime executes Red programs, integrates cognitive execution, manages memory and agents, enforces capabilities, and provides the foundational services required by the Cognitive Runtime, Agent Runtime Shell, and higher layers.

This specification is normative. It defines *runtime behaviour and responsibilities*, not implementation mechanisms.

### 2. Runtime Philosophy

The Red/Cognition runtime follows the principle:

**The runtime executes cognition without embedding intelligence.**

This means:

- The runtime provides deterministic execution of cognitive operations.
- The runtime does not perform reasoning, planning, or decision-making.
- The runtime enforces capabilities and security boundaries.
- The runtime supports observability, traceability, and replay.

### 3. Runtime Architecture Model

The runtime is structured into the following major components:

```
Red Runtime
   ├── Core Execution Engine
   ├── Memory Manager
   ├── Scheduler
   └── Event System

Cognitive Runtime
   ├── Cognitive Execution Engine (CEC-1)
   ├── Memory Hierarchy Manager
   ├── Capability Enforcement
   ├── Trace & Checkpoint System
   └── Agent Lifecycle Manager
```

### 4. Red Runtime Integration

The Cognitive Runtime **MUST** be built on top of the Red Runtime.

Requirements:

- The Red Runtime **MUST** remain fully functional and independent.
- The Cognitive Runtime **MUST** use Red Runtime services for:
  - Block evaluation
  - Dialect dispatch
  - Macro expansion
  - Basic memory allocation
- The Cognitive Runtime **MUST NOT** bypass or alter Red Runtime semantics.

### 5. Cognitive Runtime Execution Model

The Cognitive Runtime **MUST** implement the Cognitive Execution Cycle (CEC-1) defined in RC-100:

```
Observe
   ↓
Interpret
   ↓
Retrieve Memory
   ↓
Reason
   ↓
Plan
   ↓
Act
   ↓
Verify
   ↓
Reflect
   ↓
Checkpoint
   ↓
Loop
```

The runtime **MUST** support deterministic execution of this cycle when required.

### 6. Memory Management

The runtime **MUST** implement the four-tier memory architecture defined in RC-100:

| Tier                | Management Responsibility          | Persistence     |
|---------------------|------------------------------------|-----------------|
| Working Memory      | Bounded context storage            | Ephemeral       |
| Episodic Memory     | Event and experience storage       | Persistent      |
| Semantic Memory     | Knowledge graph storage            | Persistent      |
| Procedural Memory   | Skill and capability storage       | Persistent      |

The runtime **MUST** support ownership tracking and mutation events for all memory tiers.

### 7. Scheduler Model

The runtime **MUST** provide a scheduler capable of managing:

- Cognitive execution cycles
- Agent scheduling
- Priority-based execution
- Capability-constrained scheduling

The scheduler **MUST** support both cooperative and preemptive modes where appropriate.

### 8. Agent Lifecycle

The runtime **MUST** support the full agent lifecycle:

```
Spawn
   ↓
Initialize (identity, capabilities, memory)
   ↓
Run (cognitive execution cycles)
   ↓
Checkpoint / Restore
   ↓
Terminate
```

Agent state **MUST** be observable and serializable.

### 9. Checkpoint and Replay System

The runtime **MUST** support deterministic checkpointing and replay.

Requirements:

- Every cognitive action **MUST** be checkpointable.
- Checkpoints **MUST** contain sufficient information for replay.
- Replayed execution **MUST** produce equivalent observable behaviour.

### 10. Capability Enforcement

The runtime **MUST** enforce the capability model defined in RC-100.

Requirements:

- All external effects **MUST** be mediated by capabilities.
- Capability grants **MUST** be auditable.
- Capability violations **MUST** produce traceable errors.

### 11. Event System

The runtime **MUST** provide a unified event system supporting:

- Internal cognitive events
- External system events
- Inter-agent messaging
- Capability-gated event delivery

Events **MUST** carry provenance and timestamp information.

### 12. Runtime Observability and Tracing

The runtime **MUST** support:

- Execution tracing
- Effect logging
- Capability usage auditing
- Deterministic replay metadata generation

Tracing **MUST** be available without modifying program semantics.

### 13. Red Compatibility Boundary

The runtime **MUST** guarantee that:

- All valid Red 1.x programs execute without modification.
- Cognitive features are strictly additive.
- No existing Red runtime behaviour is altered by the presence of cognitive services.

### 14. Open Questions

The following areas are deferred to future RFCs or specifications:

- Concrete memory layout and serialization formats
- Scheduler policy interfaces
- Inter-agent communication protocol
- Hardware acceleration interfaces
- Formal verification of runtime properties

---

**RC-400 Runtime Specification v1.0 Draft** is now complete.

**Next Recommended Step:** Proceed with **RC-500 Cognitive Runtime Specification** or begin drafting the first major RFCs (RFC-0001, RFC-0002, RFC-0003).
