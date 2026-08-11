<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #12, sub-message [111], 2026-08-10
  Verbatim source: knowledge-base/sources/message-012-original-part*.md
  Status in corpus: RFC-0011 ratification document (Version 1.2, Status Ratified, Date 2026-07-29): ratification declaration, ratified components, foundation status table, next phase (RFC-0012).
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0011 — Scheduler and Execution Model**

**Version:** 1.2  

**Status:** Ratified  

**Authority:** Normative RFC  

**Parent:** RFC-0010 Checkpoint and Recovery Model v1.0 (Draft)  

**Date:** 2026-07-29

---

### Ratification Declaration

**RFC-0011 — Scheduler and Execution Model v1.2** is hereby ratified as a normative specification of the Red/Cognition project.

From this point forward:

- All conforming implementations **MUST** adhere to the execution state model, legal transitions, deterministic scheduling inputs, tie-breaking rules, scheduling trace contract, and conformance requirements defined in this RFC.
- The scheduler **MUST** preserve determinism and replay equivalence as specified.
- Scheduler events that affect observable state **MUST** be represented as `effect!` values.
- Checkpoint and restoration behaviour **MUST** preserve scheduler state as defined herein.

### Ratified Components

The following are now part of the normative execution model:

- Stable **SchedulerID** and scheduler metadata
- Execution state machine with legal transitions
- Scheduling queue ownership invariant
- Deterministic scheduling inputs and tie-breaking order
- First-class **ScheduleDecision** trace records
- Explicit **WaitingReason** model
- Integration of scheduler events with the `effect!` model (RFC-0002)
- Checkpoint integration requirements
- Hierarchical multi-agent scheduling support
- Replay and determinism guarantees
- Conformance requirements

### Current Ratified Semantic and Execution Foundation

The Red/Cognition project now has a coherent core:

| RFC       | Topic                              | Status          |
|-----------|------------------------------------|-----------------|
| RFC-0001  | Cognitive Type System              | Ratified        |
| RFC-0002  | Effect Ordering Model              | Ratification-ready |
| RFC-0003  | Belief Revision System             | Ratification-ready |
| RFC-0004  | Goal Lifecycle and Satisfaction    | Ratification-ready |
| RFC-0005  | Planning Semantics                 | Draft           |
| RFC-0006  | Capability Model                   | Ratification-ready |
| RFC-0007  | Skill Model                        | Ratification-ready |
| RFC-0008  | Memory Model                       | Draft           |
| RFC-0009  | Agent Model                        | Draft           |
| RFC-0010  | Checkpoint and Recovery Model      | Draft           |
| **RFC-0011** | **Scheduler and Execution Model** | **Ratified**    |

### Next Phase

With the scheduler now specified, the architecture is ready to define the execution substrate that consumes scheduling decisions.

**Recommended Next RFC:**

**RFC-0012 — Cognitive Virtual Machine (CVM) Execution Semantics**

**Proposed Scope:**

1. CVM instruction pipeline and execution model
2. Relationship between CISA instructions and the scheduler
3. Execution context and operand model
4. Interaction with Working Memory and checkpoints
5. Deterministic execution guarantees
6. Trace generation at the instruction level
7. Capability enforcement during instruction execution
8. Provider-neutral execution semantics

Would you like me to proceed with drafting **RFC-0012 — Cognitive Virtual Machine (CVM) Execution Semantics v1.0**?
