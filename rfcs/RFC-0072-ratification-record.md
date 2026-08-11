<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #31, sub-message [353], 2026-08-11
  Verbatim source: knowledge-base/sources/message-031-original-part4.md
  Status in corpus: final revised ratification record for RFC-0072 CRCP Wire Format v1.6 (Status: Ratified; provisional-effectiveness note pending parent RFC-0071 ratification; ratified components; Current Red/Cognition RFC Status table — snapshot conflicts with corpus ratification events per C-19, preserved verbatim; Registry Governance; Protocol Evolution Policy; Change Control; Normative References; Related Specifications; Conformance Profile; approved for publication per [352]/[354]/[356]/[358]/[360]). Revision arc: original record [339] (msg#30; identical re-sends [341]/[343]/[345]/[347] — D-99) → revision [349] (parent-dependency note, renamed status heading + RFC-0060/0061 rows, registry governance, evolution policy, references, conformance profile) → [351] (+ Change Control) → [353] (Change Control moved before Normative References; identical re-sends [355]/[357]/[359] — D-100); supersedes the [339]-based scaffold of msg#30 (D-95 lineage extended; [339] retained in archive). Source quirks preserved as received: missing opening parentheses in two "Ratified Components" bullets ("...structure `CRCPEnvelope`)" and "...handshake `ClientHello` / `ServerHello`)") — flagged by every review [346]–[358] but never corrected in the corpus; [360] nevertheless states the editorial issues "have been corrected" (X-140).
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->



**RFC-0072 — Cognitive Runtime Coordination Protocol (CRCP) Wire Format and Binary Message Encoding v1.6 — Ratification Record**

**Document:** RFC-0072 — Cognitive Runtime Coordination Protocol (CRCP) Wire Format and Binary Message Encoding  

**Version:** 1.6  

**Status:** **Ratified**  

**Authority:** Normative Specification  

**Parent:** RFC-0071 Cognitive Runtime Coordination Protocol (CRCP) v1.1 (Candidate)  

**Date:** 2026-07-29

---

### Ratification Declaration

**RFC-0072 — Cognitive Runtime Coordination Protocol (CRCP) Wire Format and Binary Message Encoding v1.6** is hereby ratified as a normative specification of the Red/Cognition platform.

**Note on parent dependency:** Ratification of RFC-0072 is considered effective upon ratification of its parent specification, RFC-0071. Until RFC-0071 reaches Ratified status, implementations of RFC-0072 are expected to treat it provisionally.

From this point forward:

- All conforming implementations **MUST** adhere to the unified canonical envelope, explicit field types, message type registry, flag semantics, handshake protocol, encoding profiles, stream multiplexing, sequence ordering, replay protection, standardized error encoding, and deterministic serialization rules defined in this RFC.

- CRCP messages **MUST** be exchanged using the framing, versioning, and integrity mechanisms specified herein.

- Implementations **MUST** support at least the Canonical Binary Encoding profile for interoperability.

### Ratified Components

The following are now part of the normative wire protocol model:

- Magic number and protocol versioning

- Canonical envelope structure `CRCPEnvelope`)

- Message type registry with stable numeric assignments

- Flag registry and semantics

- Version negotiation handshake `ClientHello` / `ServerHello`)

- Encoding profiles (Canonical Binary, CBOR, MessagePack, JSON)

- Stream multiplexing model

- Sequence ordering and duplicate suppression

- Replay protection requirements

- Standard error encoding

- Deterministic serialization rules (little-endian, no padding, canonical ordering)

- Transport independence with mandatory properties

### Current Red/Cognition RFC Status

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

| RFC-0013  | CISA                                       | Candidate          |

| RFC-0014  | CISA Binary Encoding                       | Draft              |

| RFC-0015  | Exception and Failure Semantics            | Draft              |

| RFC-0016  | Cognitive Runtime Architecture             | Draft              |

| RFC-0017  | Runtime Interface and Service Model        | Draft              |

| RFC-0018  | Event Log and Deterministic Replay         | Draft              |

| RFC-0019  | Cognitive Operating System Architecture    | Draft              |

| RFC-0020  | Distributed Cognitive Execution Protocol   | Draft              |

| RFC-0021  | Cognitive Network Protocol                 | Draft              |

| RFC-0022  | Cognitive Identity and Trust Framework     | Draft              |

| RFC-0023  | Distributed Consensus and Causal Agreement | Draft              |

| RFC-0024  | Cognitive Resource Management and Quota    | Draft              |

| RFC-0025  | Cognitive Security Policy Language         | Draft              |

| RFC-0026  | Cognitive Hardware Acceleration Model      | Draft              |

| RFC-0027  | Cognitive Compiler and Toolchain           | Draft              |

| RFC-0028  | Cognitive Intermediate Representation      | Draft              |

| RFC-0029  | CIR Serialization Format                   | Draft              |

| RFC-0030  | Cognitive Optimization Pass Framework      | Draft              |

| RFC-0031  | Cognitive Optimization Intermediate Language | Draft            |

| RFC-0032  | Cognitive Optimization Verification Framework | Draft           |

| RFC-0033  | Cognitive Proof-Carrying Program Format    | Draft              |

| RFC-0034  | Cognitive Package Registry and Trust Distribution | Draft       |

| RFC-0035  | Cognitive Sandbox and Execution Isolation  | Draft              |

| RFC-0036  | Cognitive Build Reproducibility and Supply Chain | Draft       |

| RFC-0037  | Cognitive Software Lifecycle and Evolution | Draft              |

| RFC-0038  | Cognitive Marketplace and Agent Economy    | Draft              |

| RFC-0039  | Cognitive Identity Economy and Ownership   | Draft              |

| RFC-0040  | Cognitive Governance and Collective Decision | Draft            |

| RFC-0041  | Cognitive Interoperability and Federation  | Draft              |

| RFC-0042  | Cognitive Autonomous Deployment Protocol   | Ratified           |

| RFC-0043  | Cognitive Language Specification           | Draft              |

| RFC-0044  | Cognitive Standard Library                 | Candidate          |

| RFC-0045  | Cognitive Tooling and Developer Experience | Candidate          |

| RFC-0046  | Cognitive Observability and Diagnostics    | Final Candidate    |

| RFC-0047  | Cognitive Package Manager and Workspace    | Final Candidate    |

| RFC-0048  | Cognitive Foreign Function Interface       | Final Candidate    |

| **RFC-0053** | **Cognitive Remote Agent Invocation Protocol** | **Ratified**    |

| **RFC-0057** | **Cognitive Distributed Transaction and Consistency Protocol** | **Ratified**    |

| **RFC-0058** | **Cognitive Transaction Wire Protocol and Message Encoding** | **Ratified**    |

| **RFC-0059** | **Cognitive Transaction Security and Trust Profile** | **Ratified**    |

| RFC-0060  | CVM Instruction Execution and Scheduling   | Candidate          |

| RFC-0061  | CVM Instruction Set and Register Architecture | Planned         |

### Registry Governance

New assignments to protocol registries defined by RFC-0072 (Message Types, Flags, Encoding Profiles, Error Codes) **SHALL** require either:

- a subsequently ratified RFC, or

- approval by the designated protocol registry authority.

### Protocol Evolution Policy

- Major version increments **MAY** introduce incompatible wire-format changes.

- Minor version increments **MUST** remain backward compatible within the same major version.

- Experimental features **MUST** remain within reserved registry ranges.

- Deprecated fields remain reserved until a future major revision.

### Change Control

Following ratification, substantive modifications to RFC-0072 **SHALL** require publication of a new revision or superseding RFC. Editorial corrections that do not alter normative behavior **MAY** be issued as errata.

### Normative References

- RFC-0071 — Cognitive Runtime Coordination Protocol

- RFC-0018 — Event Log and Deterministic Replay

### Related Specifications

- RFC-0058 — Cognitive Transaction Wire Protocol and Message Encoding

- RFC-0059 — Cognitive Transaction Security and Trust Profile

- RFC-0041 — Cognitive Interoperability and Federation

### Conformance Profile (Minimal Interoperable Implementation)

A conforming implementation **SHALL**:

- Implement `ClientHello` / `ServerHello` negotiation

- Support Canonical Binary Encoding

- Implement deterministic serialization

- Validate replay protection metadata

- Recognize all mandatory message types

- Reject unsupported major protocol versions

### Next Phase

The logical next specification is **RFC-0061 — Cognitive Virtual Machine Instruction Set and Register Architecture (CISA-RA)**, which would define the concrete register model, operand semantics, and instruction encoding details that sit beneath the execution semantics established in RFC-0060, completing the executable representation layer of the Cognitive Virtual Machine.

---

**RFC-0072 v1.6 is hereby ratified.**
