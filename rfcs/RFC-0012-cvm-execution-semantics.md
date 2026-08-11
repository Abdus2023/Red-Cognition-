<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #12, sub-message [115], 2026-08-10
  Verbatim source: knowledge-base/sources/message-012-original-part*.md
  Status in corpus: RFC-0012 CVM Execution Semantics v1.1 (Candidate for Ratification); final review [116] APPROVED — ready for ratification. Ratification record not present in corpus. NOTE: header parent citation reads 'RFC-0011 v1.2 (Candidate)' although RFC-0011 was ratified in [111] — discrepancy preserved as received.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0012 — Cognitive Virtual Machine (CVM) Execution Semantics**

**Version:** 1.1  

**Status:** Candidate for Ratification  

**Parent:** RFC-0011 Scheduler and Execution Model v1.2 (Candidate)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the execution semantics of the Cognitive Virtual Machine (CVM) in Red/Cognition.

The CVM is the execution engine responsible for interpreting and executing cognitive instructions in a deterministic, traceable, and provider-neutral manner. It serves as the bridge between the abstract cognitive model (defined in RFC-0001 through RFC-0011) and the concrete runtime execution environment.

### 2. Design Principles

The CVM follows these core principles:

- **Determinism** — Instruction execution must be reproducible given the same inputs and execution context.
- **Replay Equivalence** — Replayed executions must produce equivalent observable behaviour.
- **Provider Neutrality** — The CVM executes cognitive operations without embedding any specific reasoning or planning mechanism.
- **Capability-Aware Execution** — All instructions that may produce external effects are subject to capability enforcement.
- **Traceability** — Every instruction execution must produce a traceable record.
- **Isolation** — Execution contexts must be isolated from one another unless explicitly shared through capability-mediated mechanisms.

### 3. CVM Identity and Metadata

Every CVM instance is identified by a stable **CVMID**.

```
CVM {
    CVMID
    SupportedCISARevision
    ExecutionProfile
    Version
}
```

The `CVMID` **MUST** remain stable throughout the lifetime of the CVM instance. Changes to implementation or configuration **MUST** increment the version while preserving the `CVMID`.

### 4. Execution Context

The CVM maintains an execution context for each schedulable cognitive process. The minimum required state is:

```
ExecutionContext {
    InstructionPointer
    OperandStack
    RegisterSet
    WorkingMemoryReference
    CurrentAgent
    CurrentPlan
    CurrentGoal
    CapabilityContext
    TraceContext
}
```

The execution context **MUST** be serializable for checkpointing and restoration.

### 5. Instruction Execution Pipeline

The CVM executes instructions through the following deterministic pipeline:

```
Fetch
   ↓
Decode
   ↓
Validate
   ↓
Capability Check
   ↓
Execute
   ↓
Produce Effects
   ↓
Update Trace
   ↓
Advance Instruction Pointer
```

#### 5.1 Instruction Transaction Model

Each instruction executes as a transaction:

```
Begin
   ↓
Validate
   ↓
Capability Check
   ↓
Execute
   ↓
Generate Effects
   ↓
Commit
   ↓
Trace
```

On failure, the transaction aborts and the failure is recorded in the trace. Partial effects **MUST NOT** be committed.

### 6. Instruction Categories

The CVM supports instructions in the following categories:

- Data movement
- Cognitive operations
- Belief operations
- Goal operations
- Plan operations
- Memory operations
- Capability operations
- Control flow
- Effect generation
- Synchronisation

#### 6.1 Instruction Classes

Instructions **MAY** be classified by purity:

- `pure!` — No observable side effects
- `internal!` — Internal state mutation only
- `capability!` — Requires explicit capability authorization
- `external!` — Produces direct external state changes

### 7. Relationship to the Scheduler

The scheduler (RFC-0011) selects an execution context and passes it to the CVM.

The CVM executes the selected context until one of the following occurs:

- Instruction completion
- Voluntary yield
- Blocking on a resource or capability
- Preemption by the scheduler
- Termination

The scheduler **MUST** resume execution from the preserved instruction pointer and execution context.

The scheduler owns **when** execution happens. The CVM owns **how** execution happens.

### 8. Capability Enforcement

Every instruction that may produce an external effect **MUST** be subject to a capability check before execution.

Requirements:

- If the required capability is not present or invalid, execution of the instruction **MUST** fail.
- Capability failures **MUST** be recorded in the execution trace.
- Failed instructions **MUST NOT** produce partial effects.

### 9. Interaction with Memory

The CVM interacts with the memory tiers defined in RFC-0008 according to the following rules:

- **Working Memory**: Read/write access within the current execution context.
- **Semantic Memory**: Read access for knowledge lookup; write access only through capability-mediated effects.
- **Episodic Memory**: Append-only for traces and events.
- **Procedural Memory**: Read access for skill invocation.

### 10. Checkpoint Integration

The CVM **MUST** support checkpointing of the execution context.

A checkpoint **MUST** preserve at minimum:

- Instruction pointer
- Operand stack
- Register set
- Working Memory reference
- Capability context
- Trace context

Restoration from a checkpoint **MUST** resume execution from the exact instruction pointer and context that existed at the time of checkpoint creation.

### 11. Instruction Trace Contract

Every instruction execution **MUST** produce a trace entry:

```
InstructionTrace {
    TraceID,
    Timestamp,
    CVMID,
    AgentID,
    InstructionPointer,
    InstructionID,
    Opcode,
    Operands,
    Result,
    Effects
}
```

### 12. Replay and Determinism

Replayed executions **MUST** produce identical observable effects when given the same initial execution context and input.

A conforming implementation **MUST** ensure that:

- Instruction ordering is preserved during replay.
- Capability checks produce the same results.
- Effects are produced in the same order.
- Execution context is restored identically from checkpoints.

### 13. Conformance Requirements

A conforming CVM implementation **MUST**:

- Preserve execution context across instructions.
- Execute instructions deterministically.
- Enforce capability checks before external effects.
- Produce instruction-level traces.
- Support checkpointing and restoration of execution context.
- Preserve replay equivalence.
- Reject invalid or malformed instruction sequences.

### 14. Open Questions

The following areas require future specification:

- Concrete binary encoding of the Cognitive Instruction Set Architecture (CISA)
- Register architecture and operand model
- Just-in-time compilation and optimisation constraints
- Vector and parallel instruction execution
- Hardware acceleration interfaces

---

**RFC-0012 — Cognitive Virtual Machine (CVM) Execution Semantics v1.1** is now ready for **Final Ratification Review**.
