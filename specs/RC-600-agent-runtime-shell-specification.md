<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #5, sub-message [59], 2026-08-10
  Verbatim source: knowledge-base/sources/message-005-original-part*.md
  Status in corpus: RC-600 Agent Runtime Shell Specification v1.0 (Draft); review [60] recommends v1.1 candidate after amendments.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates specs/ for specifications.
  Content below is the document text exactly as provided (no edits).
-->

**RC-600 Agent Runtime Shell Specification**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RC-500 Cognitive Runtime Specification v1.0 (Draft)  

**Authority:** Normative Specification  

**Date:** 2026-07-29

---

### 1. Introduction

RC-600 defines the Agent Runtime Shell layer of the Red/Cognition architecture. It specifies the services and interfaces required to support both interactive and autonomous execution of cognitive agents, built on top of the Cognitive Runtime.

This specification is normative. It defines *agent runtime shell behaviour and responsibilities*, not implementation mechanisms.

### 2. Agent Runtime Shell Philosophy

The Agent Runtime Shell follows the principle:

**The Agent Runtime Shell provides the primary execution surface for agents without embedding intelligence or decision-making.**

This means:

- The shell manages agent lifecycle, interaction, and observability.
- The shell does not perform reasoning or planning.
- The shell exposes the Cognitive Runtime through stable, inspectable interfaces.
- The shell supports both human-in-the-loop and fully autonomous operation.

### 3. Relationship to Lower Layers

The Agent Runtime Shell **MUST** be built on top of the Cognitive Runtime (Layer 4) and the general Runtime services defined in RC-400.

Requirements:

- The Agent Runtime Shell **MUST** use Cognitive Runtime services for execution, memory, capabilities, and tracing.
- The Agent Runtime Shell **MUST NOT** bypass the Cognitive Runtime or violate its contracts.
- The Agent Runtime Shell **MUST** respect the Layer Interface Contract Model (LICM).

### 4. Core Responsibilities

The Agent Runtime Shell **MUST** provide the following services:

#### 4.1 Agent Lifecycle Management

- Creation, initialization, execution, suspension, checkpointing, restoration, and termination of agents.

#### 4.2 Interactive Execution Surface

- Support for REPL-style, command-driven, and conversational interaction with agents.

#### 4.3 Autonomous Execution Mode

- Support for goal-driven, event-driven, and scheduled autonomous agent execution.

#### 4.4 Observability and Explainability

- Execution tracing
- Agent state inspection
- Capability usage auditing
- Deterministic replay interfaces

#### 4.5 Human-in-the-Loop Integration

- Mechanisms for human oversight, intervention, and approval of agent actions.

### 5. Agent Model

An agent in the Agent Runtime Shell is defined as a runtime entity with the following properties:

```
Agent {
    Identity,
    Capabilities,
    Goals,
    Beliefs,
    Plans,
    Memory References,
    Execution State,
    Trace History,
    Checkpoint State
}
```

The shell **MUST** support the full agent lifecycle as defined in RC-500.

### 6. Execution Modes

The Agent Runtime Shell **MUST** support at least two primary execution modes:

#### 6.1 Interactive Mode

- Human-driven execution
- REPL, command, or conversational interfaces
- Immediate feedback and inspection

#### 6.2 Autonomous Mode

- Goal-driven and event-driven execution
- Scheduled or continuous operation
- Minimal human intervention

The shell **MUST** allow seamless transition between these modes.

### 7. Human-in-the-Loop Requirements

The Agent Runtime Shell **MUST** support human oversight through:

- Action approval workflows
- Capability-constrained execution
- Real-time state inspection
- Intervention and override mechanisms

### 8. Observability Requirements

The Agent Runtime Shell **MUST** expose:

- Full execution traces
- Agent internal state (goals, beliefs, plans, memory)
- Capability usage history
- Deterministic replay capabilities

### 9. Red Compatibility Boundary

The Agent Runtime Shell **MUST** guarantee that:

- All valid Red 1.x programs can execute without modification.
- Cognitive agent features are additive.
- Existing Red execution behaviour remains unchanged.

### 10. Open Questions

The following areas are deferred to future RFCs or specifications:

- Concrete agent identity and authentication model
- Inter-agent communication protocol
- Human oversight policy interfaces
- Multi-agent coordination primitives
- Distributed agent execution model

---

**RC-600 Agent Runtime Shell Specification v1.0 Draft** is now complete.

**Next Recommended Step:** Begin drafting **RC-700 Cognitive Virtual Machine Specification** or proceed with the first major RFCs.
