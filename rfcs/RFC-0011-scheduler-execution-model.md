<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #12, sub-message [109], 2026-08-10
  Verbatim source: knowledge-base/sources/message-012-original-part*.md
  Status in corpus: RFC-0011 Scheduler and Execution Model v1.2 content (Candidate for Final Ratification); RATIFIED per ratification document [111], Date 2026-07-29.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

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

# Source Record: Conversation Message #12 — Verbatim Transcript (Part 3 of 5: sub-messages [110]–[113])

- **Message index:** 12 (continued) · **Part 2:** `message-012-original-part2.md` · **Cleanup:** as Part 1. Note: sub-message [112] contains list-indented fenced blocks; indentation preserved as received.
