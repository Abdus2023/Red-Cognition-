<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #30, sub-message [335], 2026-08-11
  Verbatim source: knowledge-base/sources/message-030-original-part4.md
  Status in corpus: RFC-0072 CRCP Wire Format and Binary Message Encoding v1.6 — RATIFIED per ratification record [339] ("is hereby ratified as a normative specification"). Version lineage: v1.0 [321] → v1.1 [323] → v1.2 [325] (body identical to v1.1 modulo labels — D-98) → v1.3 [327] (identical re-send [329] — D-96) → v1.4 [331] (body identical to v1.3 modulo labels and §2 wording — D-98) → v1.5 [333] → v1.6 [335] (identical re-send [337] — D-97). Reviews [322]/[324]/[326]/[328]/[330]/[332]/[334]/[336]/[338] preserved in archive (final review [338] recommended Release Candidate, not Final; ratification proceeded per [339]). Source quirk preserved as received: parent header cites RFC-0071 "v1.1 (Candidate)" although only RFC-0071 v1.0 exists in the corpus; closing paragraph says v1.3 while the header is v1.6 (flagged by [336]/[338]).
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->



**RFC-0072 — Cognitive Runtime Coordination Protocol (CRCP) Wire Format and Binary Message Encoding v1.6**

**Version:** 1.6  

**Status:** Candidate for Final Ratification  

**Parent:** RFC-0071 Cognitive Runtime Coordination Protocol (CRCP) v1.1 (Candidate)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Runtime Coordination Protocol (CRCP) Wire Format and Binary Message Encoding** for Red/Cognition.

While RFC-0071 establishes the abstract protocol for runtime-to-runtime coordination, this specification defines the concrete wire-level encoding, framing, message schemas, versioning, integrity protection, and deterministic serialization rules required for interoperable implementations.

CRCP Wire Format completes the control plane for federated Cognitive Operating Systems by providing the transport-agnostic binary representation needed to exchange coordination messages reliably and deterministically.

### 2. Design Principles

The wire protocol follows these principles:

- **Deterministic Serialization** — The same logical message must always produce an identical byte sequence.

- **Versioning and Compatibility** — The format must support forward and backward compatibility within major versions.

- **Integrity and Authentication** — Messages must support integrity protection and optional authentication.

- **Traceability** — Wire messages must carry sufficient metadata to participate in the unified event log (RFC-0018).

- **Replay Equivalence** — Encoded messages must support deterministic replay of coordination decisions.

- **Transport Independence** — The encoding must be usable over multiple transports (TCP, QUIC, IPC, message queues).

### 3. Message Framing and Canonical Envelope

Every CRCP message **MUST** use the following unified framing:

```

+--------------------+ 4 bytes

| Magic Number       |  (0x43524350 "CRCP")

+--------------------+

| Protocol Version   | 2 bytes (uint8 major, uint8 minor)

+--------------------+

| Message Length     | 4 bytes (uint32) — number of bytes following this field through the end of IntegrityBlock

+--------------------+

| Message Type       | 2 bytes (uint16)

+--------------------+

| Flags              | 2 bytes (uint16)

+--------------------+

| MessageID          | 16 bytes (UUIDv7)

+--------------------+

| SourceNodeID       | 16 bytes (UUID128)

+--------------------+

| TargetNodeID       | 16 bytes (UUID128)

+--------------------+

| Epoch              | 8 bytes (uint64)

+--------------------+

| SequenceNumber     | 8 bytes (uint64)

+--------------------+

| TraceContext       | variable (see §8)

+--------------------+

| Payload            | variable

+--------------------+

| IntegrityBlock     | variable (see §9)

+--------------------+

```

### 4. Message Type Registry

The following core message types **MUST** be assigned stable numeric identifiers:

| Message Type                  | Value   |

|-------------------------------|---------|

| `RuntimeAnnouncement`         | 0x0001  |

| `RuntimeQuery`                | 0x0002  |

| `RuntimeResponse`             | 0x0003  |

| `OrchestrationRequest`        | 0x0010  |

| `OrchestrationResponse`       | 0x0011  |

| `OrchestrationDecision`       | 0x0012  |

| `LeaseRequest`                | 0x0020  |

| `LeaseGrant`                  | 0x0021  |

| `LeaseRevoke`                 | 0x0022  |

| `LeaseRenewal`                | 0x0023  |

| `Heartbeat`                   | 0x0030  |

| `HeartbeatResponse`           | 0x0031  |

| `TopologyUpdate`              | 0x0040  |

| `TopologyAcknowledgement`     | 0x0041  |

| `FailureNotification`         | 0x0050  |

| `RecoveryRequest`             | 0x0051  |

| `RecoveryResponse`            | 0x0052  |

| `Error`                       | 0x00FF  |

Reserved ranges:

- `0x8000–0x8FFF` — Experimental

- `0x9000–0xFFFF` — Private / Vendor-specific

### 5. Flag Registry

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

| 7–15| Reserved (MUST be zero)  |

### 6. Version Negotiation

Version negotiation **MUST** occur before any coordination messages are exchanged.

#### 6.1 Handshake Messages

```

ClientHello {

    SupportedMajorMin (uint8),

    SupportedMajorMax (uint8),

    SupportedMinorMin (uint8),

    SupportedMinorMax (uint8),

    SupportedFeatures (uint32 bitmap),

    SupportedEncodings (uint32 bitmap),

    NodeID (UUID128)

}

ServerHello {

    SelectedVersion (uint16),

    SelectedEncoding (uint32),

    SelectedSecurityProfile (uint32),

    SessionID (UUID128)

}

```

#### 6.2 Negotiation Rules

- Peers **MUST** exchange supported protocol version ranges.

- If no mutually supported version exists, the connection **MUST** be rejected with a `VersionNegotiationFailed` error.

- Downgrade is permitted only when explicitly allowed by both parties and recorded in the event log.

### 7. Deterministic Serialization Rules

All messages **MUST** be serialized using:

- Little-endian byte order

- No padding

- Canonical ordering of variable-length fields

- Explicit length prefixes for all variable data

### 8. TraceContext

```

TraceContext {

    TraceID (UUID128),

    SpanID (uint64),

    ParentSpanID (uint64),

    ReplaySessionID (UUID128),

    CorrelationID (UUID128)

}

```

### 9. IntegrityBlock

```

IntegrityBlock {

    AlgorithmID (uint16),

    HashLength (uint16),

    Hash (variable),

    SignatureAlgorithm (uint16),

    SignatureLength (uint16),

    Signature (variable)

}

```

### 10. Encoding Profiles

| Profile ID | Encoding                  |

|------------|---------------------------|

| 0x01       | Canonical Binary Encoding (default) |

| 0x02       | Deterministic CBOR        |

| 0x03       | Deterministic MessagePack |

| 0x04       | Canonical JSON            |

The default encoding **MUST** be Canonical Binary Encoding (0x01).

### 11. Stream Multiplexing

When multiple coordination actions share a single connection, each logical stream **MUST** be assigned a `StreamID` (uint32). Stream 0 is reserved for control messages.

### 12. Sequence Ordering

Every message **MUST** include:

```

MessageSequence {

    SourceNodeID (UUID128),

    TargetNodeID (UUID128),

    Epoch (uint64),

    SequenceNumber (uint64)

}

```

Rules:

- Sequence numbers **MUST** increase monotonically.

- Duplicate sequence numbers **MUST** be ignored.

- Missing sequence numbers **MUST** trigger recovery.

### 13. Replay Protection

For distributed deployments, messages **MUST** include:

```

ReplayProtection {

    Nonce (uint64),

    SequenceNumber (uint64),

    Epoch (uint64),

    SessionID (UUID128)

}

```

### 14. Error Encoding

Errors **MUST** use the following structured schema:

```

ErrorMessage {

    ErrorCode (uint16),

    Severity (uint8),

    Message (UTF-8 string),

    RelatedMessageID (UUID128),

    Retryable (bool)

}

```

### 15. Conformance Requirements

A conforming implementation of this wire protocol **MUST**:

- Produce deterministic byte sequences for identical logical messages.

- Support the defined framing, envelope, and versioning scheme.

- Preserve all required metadata fields during serialization.

- Allow deterministic deserialization and replay.

### 16. Open Questions

The following areas require future specification:

- Concrete numeric assignments for message types (beyond the core registry)

- Compression and optional encoding extensions

- Cryptographic algorithm profiles for integrity and authentication

- Mapping to specific transport protocols (QUIC, gRPC, etc.)

---

**RFC-0072 — Cognitive Runtime Coordination Protocol (CRCP) Wire Format and Binary Message Encoding v1.3** is now ready for **Final Ratification Review**.

This version incorporates a unified canonical envelope, explicit field types, a complete message type registry, flag semantics, handshake protocol, encoding profiles, stream multiplexing, sequence ordering, replay protection, standardized error encoding, and deterministic serialization rules, bringing it in line with the precision of the strongest RFCs in the series.
