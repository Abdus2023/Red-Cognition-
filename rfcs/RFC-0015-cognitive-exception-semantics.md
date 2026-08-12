<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #14, sub-message [123], 2026-08-10
  Verbatim source: knowledge-base/sources/message-014-original-part*.md
  Status in corpus: RFC-0015 Cognitive Exception and Failure Semantics v1.0 (Draft); review [124] recommends ExceptionID + failure state machine for v1.1; v1.1 not present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0015 — Cognitive Exception and Failure Semantics**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0013 Cognitive Instruction Set Architecture (CISA) v1.1 (Candidate)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the exception model, failure semantics, error propagation, recovery mechanisms, and rollback behaviour for the Cognitive Virtual Machine (CVM) and the broader Red/Cognition execution environment.

Because cognitive execution must remain deterministic, explainable, and replayable, failures cannot be handled arbitrarily. Every failure must be traceable, recoverable where possible, and consistent across replays.

### 2. Design Principles

The cognitive exception model follows these principles:

- **Determinism** — Failures must occur reproducibly given the same inputs and state.
- **Traceability** — Every failure must produce a complete execution trace.
- **Recoverability** — Failures should support rollback or compensation where semantically valid.
- **Capability Awareness** — Failures related to capabilities must be explicitly represented.
- **Replay Equivalence** — Replayed executions must produce equivalent failure behaviour.
- **Isolation** — Failures in one execution context must not corrupt unrelated contexts.

### 3. Exception Hierarchy

The CVM defines the following exception categories:

| Category                | Description                                      | Recoverable? | Example                              |
|-------------------------|--------------------------------------------------|--------------|--------------------------------------|
| **ValidationError**     | Instruction or operand validation failure        | Yes          | Invalid operand type                 |
| **CapabilityError**     | Required capability missing or revoked           | Yes          | File write without capability        |
| **MemoryError**         | Memory access violation or exhaustion            | Limited      | Invalid memory reference             |
| **SkillError**          | Skill execution failure                          | Yes          | Skill precondition not met           |
| **PlanError**           | Plan execution failure                           | Yes          | Plan step dependency failure         |
| **GoalError**           | Goal satisfaction or failure condition           | Limited      | Deadline violated                    |
| **RuntimeError**        | Internal runtime or CVM failure                  | No           | Internal state corruption            |
| **ExternalError**       | Failure originating from the external world      | Limited      | Sensor failure, network timeout      |

### 4. Exception Propagation

When an exception occurs:

1. The current instruction transaction is aborted.
2. Any partial effects are rolled back (where supported).
3. The exception is recorded in the execution trace.
4. Control is transferred to the exception handler or scheduler.

Exceptions **MUST** propagate through the following path:

```
Instruction
   ↓
CVM Exception Handler
   ↓
Cognitive Runtime
   ↓
Scheduler / Agent Runtime Shell
```

### 5. Rollback and Compensation

- `pure!` and `internal!` effects are generally rollback-safe.
- `capability!` and `external!` effects **MUST** declare rollback or compensation support.
- Compensation actions **MUST** themselves be represented as effects.

### 6. Exception Trace Contract

Every exception **MUST** produce a trace entry:

```
ExceptionTrace {
    TraceID,
    Timestamp,
    CVMID,
    AgentID,
    InstructionID,
    ExceptionCategory,
    ErrorCode,
    Message,
    CapabilityContext,
    RecoveryAction
}
```

### 7. Recovery Semantics

Recovery actions **MAY** include:

- Retry the failed instruction
- Execute a compensation effect
- Abort the current plan
- Fail the current goal
- Suspend the agent
- Escalate to a human operator

All recovery actions **MUST** be recorded in the execution trace.

### 8. Relationship to Other RFCs

This model integrates with:

- RFC-0002 — Effect Ordering (rollback and compensation effects)
- RFC-0004 — Goal Lifecycle (goal failure states)
- RFC-0005 — Planning Semantics (plan failure and replanning)
- RFC-0006 — Capability Model (capability errors)
- RFC-0007 — Skill Model (skill failures)
- RFC-0010 — Checkpoint and Recovery (restoration after failure)
- RFC-0011 — Scheduler (scheduling after failure)
- RFC-0012 — CVM Execution Semantics (instruction-level failures)

### 9. Replay and Determinism

Replayed executions **MUST** produce equivalent failure behaviour.

A conforming implementation **MUST** ensure that:

- The same failure conditions produce the same exception category and error code.
- Recovery actions occur in the same causal order.
- Trace records of failures are preserved.

### 10. Open Questions

The following areas require future specification:

- Formal exception codes and error taxonomy
- Distributed exception propagation
- Just-in-time compilation of exception handlers
- Hardware exception model for accelerated CVMs

---

**RFC-0015 — Cognitive Exception and Failure Semantics v1.0 Draft** is now complete.

This RFC establishes the error handling and recovery model for the Cognitive Virtual Machine and the broader Red/Cognition execution environment. It completes the execution semantics layer and provides the necessary foundation for robust, deterministic, and explainable cognitive execution.
