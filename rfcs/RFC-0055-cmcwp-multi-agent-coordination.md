<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #25, sub-message [251], 2026-08-11
  Verbatim source: knowledge-base/sources/message-025-original-part*.md
  Status in corpus: RFC-0055 CMCWP v1.0 (Draft). Proposed in [250] as the coordination plane. Review [252] recommends nine v1.1 additions (WorkflowManifest, coordination state machine, task lifecycle, message types, CoordinationManifest, failure recovery, role model, coordination events, deterministic scheduling); no v1.1 or ratification present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->


**RFC-0055 — Cognitive Multi-Agent Coordination and Workflow Protocol (CMCWP) v1.0 Draft**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0054 Cognitive Agent Discovery and Federation Protocol (CADFP) v1.0 (Draft)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Multi-Agent Coordination and Workflow Protocol (CMCWP)** for Red/Cognition.

While CADFP (RFC-0054) enables agents to discover and federate across domains, and CRAIP (RFC-0053) enables remote invocation, CMCWP defines the coordination layer that allows multiple cognitive agents to collaborate on shared goals, execute coordinated workflows, delegate tasks, and maintain consistent collective state.

CMCWP completes the transition from isolated or pairwise agent interaction to structured, multi-agent cognitive systems.

### 2. Design Principles

CMCWP follows these principles:

- **Goal-Oriented Coordination** — Multi-agent activity is organized around shared or dependent goals.

- **Deterministic Coordination** — Coordinated workflows must produce reproducible outcomes.

- **Capability Awareness** — All coordination actions must respect capability constraints.

- **Traceability** — All coordination events must participate in the unified event log.

- **Replay Equivalence** — Replayed coordinated executions must produce equivalent observable behaviour.

- **Provider Neutrality** — Coordination mechanisms must remain independent of specific reasoning implementations.

### 3. Core Primitives

CMCWP defines the following primitives:

- **Shared Goal** — A goal pursued by multiple agents.

- **Workflow** — A structured, possibly cyclic, sequence of coordinated tasks.

- **Task Delegation** — Transfer of responsibility for a goal or plan step from one agent to another.

- **Coordination Agreement** — A formal, versioned contract defining collaboration rules between agents.

- **Collective State** — Shared knowledge or progress maintained across a group of agents.

### 4. Multi-Agent Coordination Model

Agents coordinate through the following mechanisms:

#### 4.1 Shared Goals

Multiple agents **MAY** jointly pursue a single `goal!` (RFC-0004). Each participant **MUST** declare its role and contribution.

#### 4.2 Workflow Execution

Workflows **MAY** be represented as directed graphs (possibly with cycles) where nodes are tasks or sub-goals and edges represent dependencies or sequencing.

Workflows **MUST** be expressible using the planning semantics defined in RFC-0005.

#### 4.3 Task Delegation

An agent **MAY** delegate a task or sub-goal to another agent.

Requirements:

- Delegation **MUST** be capability-gated.

- The delegating agent **MUST** retain visibility into the delegated task’s progress.

- Delegation events **MUST** be recorded in the event log.

### 5. Coordination Agreements

Agents or organizations **MAY** enter into Coordination Agreements that define:

- Shared goals and success criteria

- Division of responsibilities

- Capability sharing rules

- Conflict resolution mechanisms

- Termination conditions

Agreements **MUST** be versioned and recorded in the event log.

### 6. Collective State Management

Agents participating in coordination **MAY** maintain a shared view of progress.

Requirements:

- Collective state **MUST** be stored in shared Semantic Memory with appropriate access control.

- Updates to collective state **MUST** be represented as effects (RFC-0002).

- All participants **MUST** observe the same state after a consensus round (RFC-0023).

### 7. Relationship to Other RFCs

CMCWP integrates with:

- RFC-0004 — Goal Lifecycle

- RFC-0005 — Planning Semantics

- RFC-0006 — Capability Model

- RFC-0023 — Distributed Consensus

- RFC-0040 — CGCDP (governance of shared goals)

- RFC-0041 — CIFP (cross-domain coordination)

- RFC-0053 — CRAIP (invocation of delegated tasks)

- RFC-0054 — CADFP (discovery of coordination partners)

### 8. Open Questions

The following areas require future specification:

- Formal workflow description language

- Distributed planning algorithms

- Multi-agent conflict resolution protocols

- Incentive and credit mechanisms for collaborative work

---

**RFC-0055 — Cognitive Multi-Agent Coordination and Workflow Protocol (CMCWP) v1.0 Draft** is now complete.

This RFC establishes the coordination layer required for multiple cognitive agents to collaborate on shared goals and workflows in a deterministic, traceable, and capability-aware manner. It completes the transition from pairwise remote invocation to structured multi-agent cognitive systems within the Red/Cognition platform.
