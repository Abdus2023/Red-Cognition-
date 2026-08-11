<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #26, sub-message [275], 2026-08-11
  Verbatim source: knowledge-base/sources/message-026-original-part*.md
  Status in corpus: RFC-0058 Cognitive Transaction Wire Protocol and Message Encoding v1.2 (Candidate for Final Ratification) - second v1.2 iteration [275] adding normative envelope/registry/flags/handshake/encoding/multiplexing/ordering/replay/error-code sections; supersedes first v1.2 [273], v1.1 [271], v1.0 [269] (preserved in archive; normative bodies of [269]/[271]/[273] identical - D-87/D-88; closing-paragraph claims of features absent from the [271]/[273] bodies were flagged by review [272] - contradiction C-15). RATIFIED per review decision [276] ("Decision: APPROVED FOR RATIFICATION"; "STATUS: RATIFICATION APPROVED"), user ratification record [277], and confirmation [278].
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->


**RFC-0058 — Cognitive Transaction Wire Protocol and Message Encoding v1.2**

**Version:** 1.2  

**Status:** Candidate for Final Ratification  

**Parent:** RFC-0057 Cognitive Distributed Transaction and Consistency Protocol (CDTCP) v1.3 (Ratified)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Transaction Wire Protocol and Message Encoding** for Red/Cognition.

While CDTCP (RFC-0057) specifies the abstract protocol messages, state machines, and semantics for distributed cognitive transactions, this specification defines the concrete wire format, framing, serialization rules, versioning, integrity protection, and encoding requirements needed for interoperable implementations.

### 2. Design Principles

The wire protocol follows these principles:

- **Deterministic Serialization** — The same logical message must always produce an identical byte sequence.

- **Versioning and Compatibility** — The protocol must support forward and backward compatibility.

- **Integrity and Authentication** — Messages must support integrity protection and optional authentication.

- **Traceability** — Wire messages must carry sufficient metadata to participate in the unified event log (RFC-0018).

- **Replay Equivalence** — Encoded messages must support deterministic replay.

- **Transport Independence** — The encoding must be usable over multiple transports (TCP, QUIC, IPC, message queues).

### 3. Message Framing

Every CDTCP message **MUST** use the following framing:

```

+--------------------+ 4 bytes

| Magic Number       |  (e.g., 0x43445450 "CDTP")

+--------------------+

| Protocol Version   | 2 bytes (major.minor)

+--------------------+

| Message Length     | 4 bytes

+--------------------+

| Message Type       | 2 bytes

+--------------------+

| Flags              | 2 bytes

+--------------------+

| TransactionID      | 16 bytes

+--------------------+

| Epoch              | 8 bytes

+--------------------+

| Payload            | variable

+--------------------+

| Integrity / Auth   | variable (optional)

+--------------------+

```

### 4. Canonical Envelope

Every message **MUST** conform to the following envelope structure:

```

CDTPEnvelope {

    MagicNumber,

    ProtocolVersion,

    MessageType,

    Flags,

    MessageID,

    TransactionID,

    Epoch,

    SenderID,

    CoordinatorID,

    TraceContext,

    PayloadLength,

    Payload,

    IntegrityBlock

}

```

### 5. Message Type Registry

The following message types **MUST** be assigned stable numeric identifiers:

| Message Type          | Value   |

|-----------------------|---------|

| `BeginTransaction`    | 0x0001  |

| `JoinTransaction`     | 0x0002  |

| `Prepare`             | 0x0003  |

| `Prepared`            | 0x0004  |

| `Commit`              | 0x0005  |

| `Committed`           | 0x0006  |

| `Abort`               | 0x0007  |

| `Aborted`             | 0x0008  |

| `Compensate`          | 0x0009  |

| `Compensated`         | 0x000A  |

| `Heartbeat`           | 0x000B  |

| `Status`              | 0x000C  |

| `Error`               | 0x00FF  |

Reserved ranges:

- `0x8000–0x8FFF` — Experimental

- `0x9000–0xFFFF` — Private / Vendor-specific

### 6. Flag Registry

The `Flags` field **MUST** follow this bit layout:

| Bit | Meaning                  |

|-----|--------------------------|

| 0   | Authenticated            |

| 1   | Encrypted                |

| 2   | Compressed               |

| 3   | ReplayProtected          |

| 4   | PriorityMessage          |

| 5   | ControlMessage           |

| 6   | Streaming                |

| 7–15| Reserved                 |

### 7. Version Negotiation

Version negotiation **MUST** occur before any transaction messages are exchanged.

#### 7.1 Handshake Messages

```

ClientHello {

    SupportedMajorMin,

    SupportedMajorMax,

    SupportedMinorMin,

    SupportedMinorMax,

    SupportedFeatures,

    SupportedEncodings,

    NodeID

}

ServerHello {

    SelectedVersion,

    SelectedEncoding,

    SelectedSecurityProfile,

    SessionID

}

```

#### 7.2 Negotiation Rules

- Peers **MUST** exchange supported protocol version ranges.

- If no mutually supported version exists, the connection **MUST** be rejected with a `VersionNegotiationFailed` error.

- Downgrade is permitted only when explicitly allowed by both parties and recorded in the event log.

### 8. Deterministic Serialization Rules

All messages **MUST** be serialized using:

- Little-endian byte order

- No padding

- Canonical ordering of variable-length fields

- Explicit length prefixes for all variable data

### 9. Encoding Profiles

Implementations **MAY** support the following encoding profiles:

| Profile ID | Encoding                  |

|------------|---------------------------|

| 0x01       | Canonical Binary Encoding (default) |

| 0x02       | CBOR                      |

| 0x03       | MessagePack (deterministic) |

| 0x04       | JSON (canonical)          |

The default encoding **MUST** be Canonical Binary Encoding (0x01).

### 10. Stream Multiplexing

When multiple transactions share a single connection, each transaction **MUST** be assigned a `StreamID`.

```

Connection

   |

   +-- Stream 1: Transaction A

   +-- Stream 2: Transaction B

   +-- Stream 3: Heartbeats

```

### 11. Sequence Ordering

Every message **MUST** include:

```

MessageSequence {

    TransactionID,

    SenderID,

    Epoch,

    SequenceNumber

}

```

Rules:

- Sequence numbers **MUST** increase monotonically.

- Duplicate sequence numbers **MUST** be ignored.

- Missing sequence numbers **MUST** trigger recovery.

### 12. Replay Protection

For distributed deployments, messages **MUST** include:

```

ReplayProtection {

    Nonce,

    SequenceNumber,

    Epoch,

    SessionID

}

```

### 13. Error Encoding

Errors **MUST** use the `TransactionError` schema defined in RFC-0057, with the following standardized error codes:

| Code   | Meaning                        |

|--------|--------------------------------|

| 0x0001 | InvalidManifest                |

| 0x0002 | UnsupportedVersion             |

| 0x0003 | CapabilityDenied               |

| 0x0004 | TransactionExpired             |

| 0x0005 | ReplayDetected                 |

| 0x0006 | IntegrityFailure               |

| 0x0007 | AuthenticationFailure          |

| 0x0008 | ProtocolViolation              |

| 0x0009 | VersionNegotiationFailed       |

### 14. Conformance Requirements

A conforming implementation of this wire protocol **MUST**:

- Produce deterministic byte sequences for identical logical messages.

- Support the defined framing, envelope, and versioning scheme.

- Preserve all required metadata fields during serialization.

- Allow deterministic deserialization and replay.

### 15. Open Questions

The following areas require future specification:

- Concrete numeric assignments for message types

- Compression and optional encoding extensions

- Cryptographic algorithm profiles for integrity and authentication

- Mapping to specific transport protocols (QUIC, gRPC, etc.)

---

**RFC-0058 — Cognitive Transaction Wire Protocol and Message Encoding v1.2** is now ready for **Final Ratification Review**.

This version incorporates a canonical envelope, message type registry, flag registry, handshake protocol, encoding profiles, stream multiplexing, sequence ordering, replay protection, and standardized error codes, bringing it in line with the precision of the strongest RFCs in the series.
