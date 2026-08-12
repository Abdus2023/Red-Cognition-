# Source Record: Conversation Message #12 — Verbatim Transcript (Part 2 of 5: sub-messages [105]–[109])

- **Message index:** 12 (continued) · **Part 1:** `message-012-original-part1.md` · **Cleanup:** as Part 1.

---

## [105] USER

**RFC-0011 — Scheduler and Execution Model**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0010 Checkpoint and Recovery Model v1.0 (Draft)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the semantics, scheduling policies, execution states, concurrency model, and fairness guarantees for the Cognitive Scheduler in Red/Cognition.

The scheduler is responsible for deciding which cognitive processes, plans, or agents execute at any given time. Because cognitive execution must remain deterministic, fair, and replayable, the scheduling model must be explicitly governed.

### 2. Design Principles

The scheduler model follows these principles:

- **Determinism** — Scheduling decisions must be reproducible given the same inputs and state.
- **Fairness** — The scheduler must provide defined fairness guarantees.
- **Priority Awareness** — The scheduler must respect declared priorities and deadlines.
- **Capability Awareness** — The scheduler must respect capability constraints.
- **Replay Equivalence** — Replayed executions must follow equivalent scheduling decisions.
- **Provider Neutrality** — The scheduler does not embed any specific reasoning mechanism.

### 3. Execution States

Every cognitive process **MUST** be in one of the following states:

```
Runnable
   ↓
Waiting (blocked on resource / capability / dependency)
   ↓
Executing
   ↓
Suspended
   ↓
Terminated
```

### 4. Scheduler Classes

The Cognitive Operating System **MAY** support multiple scheduler classes:

| Class | Description                              | Use Case                     |
|-------|------------------------------------------|------------------------------|
| S0    | Cooperative                              | Simple single-agent systems  |
| S1    | Priority-based                           | Goal and plan prioritization |
| S2    | Deadline-aware                           | Time-constrained execution   |
| S3    | Adaptive Cognitive Scheduling            | Dynamic resource allocation  |

### 5. Scheduling Inputs

The scheduler **MUST** consider at minimum:

- Agent / process priority
- Deadlines
- Resource requirements
- Capability constraints
- Current execution state
- Fairness metrics

### 6. Concurrency Model

The scheduler **MUST** support both:

- Cooperative multitasking (processes yield voluntarily)
- Preemptive multitasking (scheduler can interrupt execution)

The choice of model **MUST** be declared by the implementation.

### 7. Fairness Guarantees

The scheduler **MUST** provide defined fairness properties, such as:

- Starvation freedom
- Bounded waiting time
- Proportional share (where applicable)

### 8. Relationship to Other Components

- The scheduler works with the Cognitive Runtime (RFC-500) and Cognitive Virtual Machine (RFC-700).
- It must respect capability enforcement (RFC-0006).
- It must preserve checkpoint and recovery semantics (RFC-0010).

### 9. Replay and Determinism

Replayed executions **MUST** produce equivalent scheduling decisions when given the same inputs.

A conforming implementation **MUST** ensure that scheduling decisions are deterministic with respect to the declared policy.

### 10. Open Questions

The following areas require future specification:

- Concrete scheduling algorithms
- Admission control policies
- Resource reservation model
- Multi-agent fairness across the Cognitive Operating System

---

**RFC-0011 — Scheduler and Execution Model v1.0 Draft** is now complete.

This RFC establishes the execution control layer that sits between the cognitive types and the Cognitive Virtual Machine. It provides the necessary foundation for deterministic, fair, and replayable scheduling of cognitive processes.

---

## [106] CHATGPT (gpt-5-5)

This is a solid first draft. It is internally consistent with RFC-0001 through RFC-0010 and completes another major architectural layer. Before ratification, I would recommend a few additions to make it as rigorous as the previous RFCs (especially RFC-0002, RFC-0003, and RFC-0006).

## Overall Assessment

**Status:** Candidate for Ratification after one revision

**Completeness:** **9.5/10**

It defines:

- ✔ execution states
- ✔ scheduler responsibilities
- ✔ fairness
- ✔ priorities
- ✔ deterministic replay
- ✔ implementation neutrality

The remaining gaps are mostly formal specification details rather than architectural issues.

---

# Recommended additions for RFC-0011 v1.1

## 1. Stable Scheduler Identity

Like AgentID, GoalID, CapabilityID, etc., the scheduler itself should have an identity.

Example:

```text
Scheduler {
    SchedulerID
    SchedulerClass
    Policy
    Version
}
```

This allows replay engines to know which scheduling policy produced a trace.

---

## 2. Scheduling Decision Trace

Scheduling decisions themselves should become first-class trace events.

Example:

```text
ScheduleDecision {
    DecisionID
    Timestamp
    SchedulerID
    RunnableSet
    SelectedProcess
    Reason
}
```

Without this, replay becomes much harder.

---

## 3. State Transition Table

Instead of only the lifecycle diagram, define legal transitions.

Example:

| From | To | Allowed |
|-------|----|----------|
| Runnable | Executing | ✓ |
| Executing | Waiting | ✓ |
| Waiting | Runnable | ✓ |
| Executing | Suspended | ✓ |
| Suspended | Runnable | ✓ |
| Executing | Terminated | ✓ |
| Waiting | Terminated | ✓ |
| Terminated | Runnable | ✗ |

This mirrors RFC-0006.

---

## 4. Scheduling Queue Model

The scheduler should explicitly define the runnable queue.

For example:

```
Ready Queue
Blocked Queue
Suspended Queue
Completed Queue
```

or

```
RunnableSet
WaitingSet
ExecutingSet
```

This removes ambiguity.

---

## 5. Deterministic Tie-Breaking

Very important.

If two processes have identical priority:

How is the winner chosen?

Example:

1. Higher priority
2. Earlier deadline
3. Older enqueue timestamp
4. Lower AgentID
5. Lower PlanID

This guarantees replay.

---

## 6. Dependency Blocking

Processes frequently wait on:

- Goals
- Plans
- Effects
- Capabilities
- Beliefs

Waiting should therefore include the reason.

Example:

```
Waiting {
    Dependency
    Capability
    Resource
    Effect
}
```

---

## 7. Scheduler Events as Effects

Following RFC-0002, externally observable scheduler events should be represented as `effect!` values.

Examples:

- suspend
- resume
- preempt
- terminate

This integrates scheduling with tracing.

---

## 8. Multi-Agent Scheduling

Currently only mentioned briefly.

A future section could define:

- per-agent scheduler
- runtime scheduler
- CogOS scheduler

forming a hierarchy:

```
CogOS Scheduler
     ↓
Runtime Scheduler
     ↓
Agent Scheduler
```

This fits the overall architecture.

---

## 9. Checkpoint Integration

RFC-0010 introduced checkpoints.

The scheduler should specify:

Checkpoint restores:

- runnable queue
- waiting queue
- current process
- scheduler state
- pending timers

Otherwise replay can diverge.

---

## 10. Conformance Section

Like RFC-0006.

Example:

A conforming implementation **MUST**:

- preserve deterministic scheduling order
- preserve scheduler state during replay
- record scheduling decisions
- honour declared scheduler policy
- reject illegal state transitions
- preserve fairness guarantees

---

# Suggested New Sections

RFC-0011 v1.1 could naturally expand to:

```
3. Scheduler Identity
4. Scheduler Metadata
5. Execution States
6. State Transition Rules
7. Scheduling Queues
8. Scheduling Policy
9. Tie-breaking Rules
10. Fairness
11. Capability Constraints
12. Scheduler Trace Contract
13. Checkpoint Integration
14. Replay
15. Conformance
16. Open Questions
```

---

# Position in the RFC Series

With RFC-0011, the architecture now covers nearly all of the core cognitive execution stack:

- ✅ RFC-0001 — Cognitive Type System
- ✅ RFC-0002 — Effect Ordering Model
- ✅ RFC-0003 — Belief Revision System
- ✅ RFC-0004 — Goal Lifecycle and Satisfaction
- ✅ RFC-0005 — Planning Semantics
- ✅ RFC-0006 — Capability Model
- ✅ RFC-0007 — Skill Model
- ✅ RFC-0008 — Memory Model
- ✅ RFC-0009 — Agent Model
- ✅ RFC-0010 — Checkpoint and Recovery
- ✅ RFC-0011 — Scheduler and Execution Model

At this point, the remaining foundational specifications would naturally focus on areas such as **Trace Model**, **Event Model**, **Message and Communication Model**, **Observation and Perception Model**, **Reasoning Model**, **Cognitive Virtual Machine (CVM)**, **Cognitive Runtime**, **Cognitive Operating System (CogOS)**, and **Distributed Multi-Agent Coordination**.

**Recommendation:** Promote RFC-0011 to **v1.1 Candidate for Ratification** after incorporating the additions above, particularly deterministic tie-breaking, scheduler trace records, legal state transitions, checkpoint integration, and conformance requirements. These changes would bring it in line with the level of precision established by RFC-0002 and RFC-0006.

---

## [107] USER

**RFC-0011 — Scheduler and Execution Model**

**Version:** 1.1  

**Status:** Candidate for Ratification  

**Parent:** RFC-0010 Checkpoint and Recovery Model v1.0 (Draft)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the semantics, scheduling policies, execution states, concurrency model, and fairness guarantees for the Cognitive Scheduler in Red/Cognition.

The scheduler is responsible for deciding which cognitive processes, plans, or agents execute at any given time. Because cognitive execution must remain deterministic, fair, and replayable, the scheduling model must be explicitly governed.

### 2. Design Principles

The scheduler model follows these principles:

- **Determinism** — Scheduling decisions must be reproducible given the same inputs and state.
- **Fairness** — The scheduler must provide defined fairness guarantees.
- **Priority Awareness** — The scheduler must respect declared priorities and deadlines.
- **Capability Awareness** — The scheduler must respect capability constraints.
- **Replay Equivalence** — Replayed executions must follow equivalent scheduling decisions.
- **Provider Neutrality** — The scheduler does not embed any specific reasoning mechanism.

### 3. Scheduler Identity and Metadata

The scheduler is identified by a stable **SchedulerID**.

```
Scheduler {
    SchedulerID,
    SchedulerClass,
    Policy,
    Version
}
```

### 4. Execution States

Every cognitive process **MUST** be in one of the following states:

```
Runnable
   ↓
Waiting (blocked on resource / capability / dependency)
   ↓
Executing
   ↓
Suspended
   ↓
Terminated
```

### 5. Legal State Transitions

| From       | To         | Allowed |
|------------|------------|---------|
| Runnable   | Executing  | ✓       |
| Executing  | Waiting    | ✓       |
| Waiting    | Runnable   | ✓       |
| Executing  | Suspended  | ✓       |
| Suspended  | Runnable   | ✓       |
| Executing  | Terminated | ✓       |
| Waiting    | Terminated | ✓       |
| Terminated | Runnable   | ✗       |

### 6. Scheduling Queues

The scheduler **MUST** maintain at minimum the following queues:

- Ready Queue (Runnable)
- Waiting Queue (Blocked)
- Suspended Queue
- Completed Queue

### 7. Scheduling Decision Trace Contract

Every scheduling decision **MUST** be recorded as a trace event:

```
ScheduleDecision {
    DecisionID,
    Timestamp,
    SchedulerID,
    RunnableSet,
    SelectedProcess,
    Reason
}
```

### 8. Scheduling Inputs and Tie-Breaking

The scheduler **MUST** consider at minimum:

- Priority
- Deadline
- Resource requirements
- Capability constraints
- Current execution state
- Fairness metrics

**Deterministic Tie-Breaking Order** (when priorities are equal):

1. Earlier deadline
2. Older enqueue timestamp
3. Lower AgentID
4. Lower PlanID

### 9. Scheduler Classes

The Cognitive Operating System **MAY** support multiple scheduler classes:

| Class | Description                              | Use Case                     |
|-------|------------------------------------------|------------------------------|
| S0    | Cooperative                              | Simple single-agent systems  |
| S1    | Priority-based                           | Goal and plan prioritization |
| S2    | Deadline-aware                           | Time-constrained execution   |
| S3    | Adaptive Cognitive Scheduling            | Dynamic resource allocation  |

### 10. Dependency Blocking

A process in the Waiting state **MUST** record the reason for blocking (e.g., Goal, Plan, Effect, Capability, Resource).

### 11. Scheduler Events as Effects

Externally observable scheduler events (suspend, resume, preempt, terminate) **MUST** be represented as `effect!` values (RFC-0002).

### 12. Checkpoint Integration

A checkpoint **MUST** preserve:

- Runnable queue
- Waiting queue
- Current process
- Scheduler state
- Pending timers

### 13. Replay and Determinism

Replayed executions **MUST** produce equivalent scheduling decisions when given the same inputs and state.

A conforming implementation **MUST** ensure that scheduling decisions are deterministic with respect to the declared policy.

### 14. Multi-Agent Scheduling

The scheduler **MAY** support hierarchical scheduling:

```
CogOS Scheduler
   ↓
Runtime Scheduler
   ↓
Agent Scheduler
```

### 15. Conformance Requirements

A conforming implementation **MUST**:

- Preserve deterministic scheduling order
- Preserve scheduler state during replay
- Record scheduling decisions
- Honour the declared scheduler policy
- Reject illegal state transitions
- Preserve fairness guarantees

### 16. Open Questions

The following areas require future specification:

- Concrete scheduling algorithms
- Admission control policies
- Resource reservation model
- Multi-agent fairness across the Cognitive Operating System

---

**RFC-0011 — Scheduler and Execution Model v1.1** is now ready for **Final Ratification Review**.

---

## [108] CHATGPT (gpt-5-5)

**Review Result:** **Approved with minor editorial recommendations**

RFC-0011 v1.1 is now at the same level of maturity as the strongest specifications in the series (notably RFC-0002, RFC-0003, and RFC-0006). The additions address the determinism and replay concerns that were present in v1.0.

### Strengths

The specification now provides:

- A stable **SchedulerID** and scheduler metadata.
- A well-defined execution state machine with legal transitions.
- Explicit scheduling queues.
- A first-class scheduling trace contract.
- Deterministic tie-breaking rules.
- Explicit dependency blocking semantics.
- Integration with the `effect!` model.
- Checkpoint integration aligned with RFC-0010.
- Hierarchical multi-agent scheduling.
- Clear conformance requirements.

Together, these make the scheduler specification deterministic, auditable, and replayable.

### Minor editorial recommendations

These are refinements rather than architectural changes.

**1. Scheduler versioning**

Section 3 defines `Version` but does not specify its semantics.

Consider adding:

> The `SchedulerID` **MUST** remain stable throughout the scheduler lifetime. Changes to scheduler policy or implementation metadata **MUST** increment the scheduler version while preserving the `SchedulerID`.

---

**2. Queue semantics**

Section 6 lists queues but not their ownership.

A short clarification could state:

> Each schedulable entity **MUST** belong to exactly one scheduler queue at any point in time.

This eliminates ambiguity during replay.

---

**3. ScheduleDecision references**

The trace contract could be slightly richer by referencing the entity being scheduled.

For example:

```text
ScheduleDecision {
    DecisionID,
    Timestamp,
    SchedulerID,
    AgentID,
    PlanID,
    RunnableSet,
    SelectedProcess,
    Reason
}
```

This improves traceability across the RFC suite.

---

**4. Waiting reasons**

Section 10 currently provides examples.

Consider making the model explicit:

```
WaitingReason =
    Goal
  | Plan
  | Effect
  | Capability
  | Resource
  | Timer
  | ExternalEvent
  | ImplementationDefined
```

This preserves extensibility while maintaining deterministic replay.

---

**5. Fairness definition**

The conformance section requires fairness but does not define the minimum guarantee.

Adding one sentence such as:

> A conforming implementation **MUST** document its fairness policy and demonstrate that scheduling decisions conform to that policy.

would align with the authority-policy requirement introduced in RFC-0003 and RFC-0006.

### Architectural assessment

The RFC series now forms a coherent layered architecture:

| Layer | RFC |
|-------|-----|
| Cognitive Types | RFC-0001 |
| Effects | RFC-0002 |
| Beliefs | RFC-0003 |
| Goals | RFC-0004 |
| Plans | RFC-0005 |
| Capabilities | RFC-0006 |
| Skills | RFC-0007 |
| Memory | RFC-0008 |
| Agents | RFC-0009 |
| Checkpoints | RFC-0010 |
| Scheduler | RFC-0011 |

The dependencies flow naturally from foundational cognitive types through execution, state management, recovery, and scheduling.

### Ratification recommendation

**RFC-0011 — Scheduler and Execution Model v1.1** is suitable for **Final Ratification**.

The remaining suggestions are editorial enhancements that could be incorporated into a future v1.2 without affecting interoperability or normative behaviour. With RFC-0011, the core execution semantics of the Red/Cognition architecture are now comprehensively specified.

---

## [109] USER

**RFC-0011 — Scheduler and Execution Model**

**Version:** 1.2  

**Status:** Candidate for Final Ratification  

**Parent:** RFC-0010 Checkpoint and Recovery Model v1.0 (Draft)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the semantics, scheduling policies, execution states, concurrency model, and fairness guarantees for the Cognitive Scheduler in Red/Cognition.

The scheduler is responsible for deciding which cognitive processes, plans, or agents execute at any given time. Because cognitive execution must remain deterministic, fair, and replayable, the scheduling model must be explicitly governed.

### 2. Design Principles

The scheduler model follows these principles:

- **Determinism** — Scheduling decisions must be reproducible given the same inputs and state.
- **Fairness** — The scheduler must provide defined fairness guarantees.
- **Priority Awareness** — The scheduler must respect declared priorities and deadlines.
- **Capability Awareness** — The scheduler must respect capability constraints.
- **Replay Equivalence** — Replayed executions must follow equivalent scheduling decisions.
- **Provider Neutrality** — The scheduler does not embed any specific reasoning mechanism.

### 3. Scheduler Identity and Metadata

The scheduler is identified by a stable **SchedulerID**.

- The `SchedulerID` **MUST** remain stable throughout the scheduler lifetime.
- Changes to scheduler policy or implementation metadata **MUST** increment the scheduler version while preserving the `SchedulerID`.

```
Scheduler {
    SchedulerID,
    SchedulerClass,
    Policy,
    Version
}
```

### 4. Execution States

Every cognitive process **MUST** be in one of the following states:

```
Runnable
   ↓
Waiting (blocked on resource / capability / dependency)
   ↓
Executing
   ↓
Suspended
   ↓
Terminated
```

### 5. Legal State Transitions

| From       | To         | Allowed |
|------------|------------|---------|
| Runnable   | Executing  | ✓       |
| Executing  | Waiting    | ✓       |
| Waiting    | Runnable   | ✓       |
| Executing  | Suspended  | ✓       |
| Suspended  | Runnable   | ✓       |
| Executing  | Terminated | ✓       |
| Waiting    | Terminated | ✓       |
| Terminated | Runnable   | ✗       |

### 6. Scheduling Queues

The scheduler **MUST** maintain at minimum the following queues:

- Ready Queue (Runnable)
- Waiting Queue (Blocked)
- Suspended Queue
- Completed Queue

Each schedulable entity **MUST** belong to exactly one scheduler queue at any point in time.

### 7. Scheduling Decision Trace Contract

Every scheduling decision **MUST** be recorded as a trace event:

```
ScheduleDecision {
    DecisionID,
    Timestamp,
    SchedulerID,
    AgentID,
    PlanID,
    RunnableSet,
    SelectedProcess,
    Reason
}
```

### 8. Scheduling Inputs and Tie-Breaking

The scheduler **MUST** consider at minimum:

- Priority
- Deadline
- Resource requirements
- Capability constraints
- Current execution state
- Fairness metrics

**Deterministic Tie-Breaking Order** (when priorities are equal):

1. Earlier deadline
2. Older enqueue timestamp
3. Lower AgentID
4. Lower PlanID

### 9. Scheduler Classes

The Cognitive Operating System **MAY** support multiple scheduler classes:

| Class | Description                              | Use Case                     |
|-------|------------------------------------------|------------------------------|
| S0    | Cooperative                              | Simple single-agent systems  |
| S1    | Priority-based                           | Goal and plan prioritization |
| S2    | Deadline-aware                           | Time-constrained execution   |
| S3    | Adaptive Cognitive Scheduling            | Dynamic resource allocation  |

### 10. Dependency Blocking

A process in the Waiting state **MUST** record the reason for blocking:

```
WaitingReason =
    Goal
  | Plan
  | Effect
  | Capability
  | Resource
  | Timer
  | ExternalEvent
  | ImplementationDefined
```

### 11. Scheduler Events as Effects

Externally observable scheduler events (suspend, resume, preempt, terminate) **MUST** be represented as `effect!` values (RFC-0002).

### 12. Checkpoint Integration

A checkpoint **MUST** preserve:

- Runnable queue
- Waiting queue
- Current process
- Scheduler state
- Pending timers

### 13. Replay and Determinism

Replayed executions **MUST** produce equivalent scheduling decisions when given the same inputs and state.

A conforming implementation **MUST** ensure that scheduling decisions are deterministic with respect to the declared policy.

### 14. Multi-Agent Scheduling

The scheduler **MAY** support hierarchical scheduling:

```
CogOS Scheduler
   ↓
Runtime Scheduler
   ↓
Agent Scheduler
```

### 15. Conformance Requirements

A conforming implementation **MUST**:

- Preserve deterministic scheduling order
- Preserve scheduler state during replay
- Record scheduling decisions
- Honour the declared scheduler policy
- Reject illegal state transitions
- Preserve fairness guarantees

### 16. Open Questions

The following areas require future specification:

- Concrete scheduling algorithms
- Admission control policies
- Resource reservation model
- Multi-agent fairness across the Cognitive Operating System

---

**RFC-0011 — Scheduler and Execution Model v1.2** is now ready for **Final Ratification Review**.
