<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #8, sub-message [61], 2026-08-10
  Verbatim source: knowledge-base/sources/message-008-original-part*.md
  Status in corpus: RC-700 Cognitive Virtual Machine Specification v1.0 (Draft); review [62] recommends v1.1 candidate with 5 additions; v1.1/ratification record not present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates specs/ and rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RC-700 Cognitive Virtual Machine Specification**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RC-600 Agent Runtime Shell Specification v1.0 (Draft)  

**Authority:** Normative Specification  

**Date:** 2026-07-29

---

### 1. Introduction

RC-700 defines the Cognitive Virtual Machine (CVM) layer of the Red/Cognition architecture. It specifies the instruction set, execution model, and runtime services required to execute cognitive operations in a deterministic, inspectable, and provider-neutral manner.

This specification is normative. It defines *cognitive virtual machine behaviour and responsibilities*, not implementation mechanisms.

### 2. Cognitive Virtual Machine Philosophy

The Cognitive Virtual Machine follows the principle:

**The CVM executes cognitive operations as first-class, deterministic instructions without embedding intelligence.**

This means:

- The CVM provides a defined instruction set for cognitive operations.
- The CVM executes instructions deterministically when required.
- The CVM does not perform reasoning or planning.
- The CVM supports traceability, checkpointing, and replay.

### 3. Relationship to Lower Layers

The CVM **MUST** be built on top of the Cognitive Runtime (Layer 4) and the general Runtime services defined in RC-400.

Requirements:

- The CVM **MUST** use Cognitive Runtime services for memory, capabilities, tracing, and agent lifecycle.
- The CVM **MUST NOT** bypass the Cognitive Runtime contracts.
- The CVM **MUST** respect the Layer Interface Contract Model (LICM).

### 4. Cognitive Instruction Set Architecture (CISA)

The CVM defines a Cognitive Instruction Set Architecture (CISA).

#### 4.1 Core Cognitive Instructions

The following instructions **MUST** be supported:

| Instruction     | Purpose                                      | Arguments                          |
|-----------------|----------------------------------------------|------------------------------------|
| `OBSERVE`       | Capture external state or event              | Source, Parameters                 |
| `RECALL`        | Retrieve memory                              | Query, Memory Tier                 |
| `INFER`         | Perform reasoning                            | Beliefs, Goal, Constraints         |
| `PLAN`          | Generate or modify plan                      | Goal, Constraints, Current Plan    |
| `EXECUTE`       | Execute an action through capability         | Capability, Arguments              |
| `VERIFY`        | Check outcome against expected state         | Expected, Actual                   |
| `REFLECT`       | Update beliefs and plans from outcome        | Trace, Outcome                     |
| `CHECKPOINT`    | Create recoverable execution state           | —                                  |
| `RESTORE`       | Restore from checkpoint                      | Checkpoint Reference               |
| `EXPLAIN`       | Generate explanation of decision or action   | Target, Format                     |

#### 4.2 Instruction Properties

Every CISA instruction **MUST**:

- Be deterministic when given the same inputs and state.
- Carry provenance and timestamp metadata.
- Be subject to capability checks where applicable.
- Produce traceable effects.

### 5. Execution Model

The CVM executes the Cognitive Execution Cycle (CEC-1) using CISA instructions.

The CVM **MUST** support:

- Deterministic execution of instruction sequences.
- Interruption and resumption at instruction boundaries.
- Checkpointing of execution state.
- Replay from checkpoints and traces.

### 6. State Management

The CVM **MUST** maintain execution state including:

- Current instruction pointer
- Working memory references
- Active capabilities
- Execution trace
- Checkpoint references

State **MUST** be serializable and restorable.

### 7. Capability Integration

All instructions that produce external effects **MUST** be subject to capability enforcement.

The CVM **MUST**:

- Check required capabilities before instruction execution.
- Record capability usage in the execution trace.
- Prevent execution on capability violation.

### 8. Traceability and Explainability

The CVM **MUST** generate execution traces for all instructions.

Requirements:

- Every instruction execution **MUST** produce a trace entry.
- Traces **MUST** include instruction, arguments, effects, and capability context.
- The CVM **MUST** support deterministic replay from traces.

### 9. Provider Neutrality

The CVM **MUST** remain provider-neutral.

Requirements:

- The CVM **MUST NOT** depend on any specific intelligence provider.
- The CVM **MUST** support multiple implementations of reasoning, planning, and memory access through stable instruction semantics.

### 10. Red Compatibility Boundary

The CVM **MUST** guarantee that:

- All valid Red 1.x programs execute without modification when using Red Runtime paths.
- CVM instructions are additive and do not alter Red semantics.
- Cognitive execution remains optional.

### 11. Open Questions

The following areas are deferred to future RFCs or specifications:

- Concrete binary encoding of CISA instructions
- Formal semantics of individual instructions
- Optimization and scheduling of CISA programs
- Hardware acceleration interfaces for CVM
- Multi-agent CVM coordination primitives

---

**RC-700 Cognitive Virtual Machine Specification v1.0 Draft** is now complete.

**Next Recommended Step:** Begin drafting **RC-800 Cognitive Operating System Specification** or proceed with the first major RFCs.
