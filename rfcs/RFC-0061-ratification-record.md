<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #29, sub-message [301], 2026-08-11
  Verbatim source: knowledge-base/sources/message-029-original-part1.md
  Status in corpus: formal ratification record for RFC-0061 CISA-RA v1.2 (Status: Ratified; ratification declaration; ratified components; status-table snapshot conflicts with corpus ratification events per C-17, preserved verbatim). Supersedes the msg#27 [300]-based scaffold (final ratification review "Decision: APPROVED; Status: RATIFIED", retained in archive — D-95). Source quirks preserved as received: missing opening parentheses in two "Ratified Components" bullets ("...`G`, `M`, `C`, `T`, `S` registers)" and "...etc.)").
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->



**RFC-0061 — Cognitive Virtual Machine Instruction Set and Register Architecture (CISA-RA) v1.2 — Ratification Record**

**Document:** RFC-0061 — Cognitive Virtual Machine Instruction Set and Register Architecture (CISA-RA)  

**Version:** 1.2  

**Status:** **Ratified**  

**Authority:** Normative Specification  

**Parent:** RFC-0060 — Cognitive Virtual Machine Instruction Execution and Scheduling Semantics (CVM-IESS) v1.1 (Candidate)  

**Date:** 2026-07-29

---

### Ratification Declaration

**RFC-0061 — Cognitive Virtual Machine Instruction Set and Register Architecture (CISA-RA) v1.2** is hereby ratified as a normative specification of the Red/Cognition platform.

From this point forward:

- All conforming CVM implementations **MUST** adhere to the register architecture, operand model, instruction encoding, opcode classification, and execution semantics defined in this RFC.

- CISA instructions **MUST** be implemented in accordance with the register classes, addressing modes, and transaction/security integration rules specified herein.

- Future RFCs that extend the CVM instruction set **MUST** maintain compatibility with the foundational model established by this specification.

### Ratified Components

The following are now part of the normative CVM instruction architecture:

- Five-class register architecture `G`, `M`, `C`, `T`, `S` registers) with mutability rules

- Stable `CVMID` and execution metadata

- Instruction format with `InstructionID`, `EncodingVersion`, `Opcode`, operands, capability requirements, and effect class

- Opcode family classification (Control, Arithmetic, Memory, Cognitive, Goal, Planning, Communication, Transaction, Security, Experimental)

- Core instruction set examples `LOAD`, `STORE`, `BELIEF_ASSERT`, `GOAL_CREATE`, `PLAN_EXECUTE`, `CAP_VERIFY`, `EFFECT_EMIT`, `OBSERVE`, `INFER`, etc.)

- Instruction transaction model (Begin → Validate → Authorize → Execute → Effects → Commit → Trace)

- Memory model (Local / Working / Shared) with transaction requirements

- Effect descriptor model for instructions that produce external state changes

- Deterministic serialization and replay compatibility requirements

- Conformance profiles (Minimal, Developer, Professional, Enterprise, Verified)

### Current Ratified / Near-Ratified Foundation

| RFC       | Topic                                      | Status             |

|-----------|--------------------------------------------|--------------------|

| RFC-0001  | Cognitive Type System                      | Ratified           |

| RFC-0002  | Effect Ordering Model                      | Ratification-ready |

| RFC-0003  | Belief Revision System                     | Ratification-ready |

| RFC-0004  | Goal Lifecycle and Satisfaction            | Ratification-ready |

| RFC-0005  | Planning Semantics                         | Draft              |

| RFC-0006  | Capability Model                           | Ratification-ready |

| RFC-0007  | Skill Model                                | Ratification-ready |

| RFC-0008  | Memory Model                               | Draft              |

| RFC-0009  | Agent Model                                | Draft              |

| RFC-0010  | Checkpoint and Recovery Model              | Draft              |

| RFC-0011  | Scheduler and Execution Model              | Ratified           |

| RFC-0012  | CVM Execution Semantics                    | Ratified           |

| **RFC-0061** | **CVM Instruction Set and Register Architecture** | **Ratified**    |

| RFC-0013–0014, 0018, 0057–0059 | Supporting execution, wire, and security layers | Ratified / Candidate |

### Architectural Completion

With RFC-0061 ratified, the Red/Cognition execution substrate is now complete at the instruction-set level:

```

Cognitive Program

   ↓

CIR (RFC-0028)

   ↓

CISA Instructions (RFC-0013 + RFC-0061)

   ↓

CVM Execution + Scheduler (RFC-0012 + RFC-0060)

   ↓

Transaction Boundaries (RFC-0057)

   ↓

Security Enforcement (RFC-0059)

   ↓

Effects, Memory, and Traces (RFC-0002, 0008, 0018)

   ↓

Deterministic Replay and Verification

```

### Next Phase

The logical next specification is **RFC-0062 — Cognitive Virtual Machine Bytecode Format and Encoding (CVM-BF)**, which would define the concrete binary encoding, opcode numeric assignments, operand encoding, and serialization rules for CISA instructions, completing the executable representation layer beneath RFC-0061.

Would you like me to proceed with drafting **RFC-0062**?
