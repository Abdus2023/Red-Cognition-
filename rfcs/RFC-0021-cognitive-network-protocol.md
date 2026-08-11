<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #14, sub-message [135], 2026-08-10
  Verbatim source: knowledge-base/sources/message-014-original-part*.md
  Status in corpus: RFC-0021 Cognitive Network Protocol (CNP) v1.0 (Draft); review [136]: cognitive network stack, CNP message envelope, six protocol families, migration transport, trust foundation.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0021 — Cognitive Network Protocol (CNP)**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0020 Distributed Cognitive Execution Protocol v1.0 (Draft)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Network Protocol (CNP)** for Red/Cognition.

CNP provides the communication, discovery, authentication, and routing layer that enables distributed cognitive execution across multiple nodes while preserving determinism, traceability, capability enforcement, and replay equivalence.

### 2. Design Principles

CNP follows these principles:

- **Determinism** — All protocol messages and responses must be reproducible given the same inputs.
- **Causality** — Message ordering must respect causal dependencies across nodes.
- **Capability Awareness** — All cross-node operations must be capability-gated.
- **Traceability** — Every message must carry provenance and participate in the global event log.
- **Replay Equivalence** — Replayed distributed executions must produce equivalent observable behaviour.
- **Provider Neutrality** — The protocol must remain independent of specific reasoning or planning mechanisms.

### 3. Node Identity and Discovery

Every participating node is identified by a stable **NodeID** (as introduced in RFC-0020).

CNP defines:

- Node discovery mechanisms (local broadcast, registry, or peer-to-peer)
- Node capability advertisement
- Version negotiation for supported CISA and RFC revisions

### 4. Message Format

All CNP messages **MUST** conform to the following structure:

```
CNPMessage {
    MessageID
    Timestamp
    SourceNodeID
    TargetNodeID (or broadcast)
    MessageType
    Payload
    CapabilityToken (optional)
    TraceReference
    Signature (optional)
}
```

### 5. Core Message Types

CNP supports the following core message categories:

- **Discovery**: `NodeAnnouncement`, `NodeQuery`, `NodeResponse`
- **Execution**: `RemoteCVMRequest`, `RemoteCVMResponse`, `ExecutionStateTransfer`
- **Capability**: `CapabilityDelegation`, `CapabilityRevocation`, `CapabilityVerification`
- **Event**: `EventPropagation`, `EventAcknowledgement`
- **Migration**: `AgentMigrationRequest`, `AgentMigrationResponse`, `StateTransfer`
- **Coordination**: `ConsensusProposal`, `ConsensusVote`, `ConsensusResult`

### 6. Authentication and Trust

All cross-node communication **MUST** be authenticated.

Requirements:

- Nodes **MUST** present verifiable identity (e.g., cryptographic certificates or capability-based tokens).
- Messages **MAY** be signed to ensure integrity.
- Capability tokens **MUST** be verified before granting remote access.

### 7. Capability Federation

Capabilities granted on one node **MUST** be enforceable on remote nodes.

CNP defines mechanisms for:

- Capability delegation across nodes
- Revocation propagation
- Scope verification on the receiving node

### 8. Event Propagation

The distributed event log (RFC-0018) is synchronized across nodes using CNP.

Requirements:

- Events **MUST** be propagated with causal metadata.
- Nodes **MUST** acknowledge receipt of events.
- Conflicting or out-of-order events **MUST** be resolved according to the causal ordering rules defined in RFC-0020.

### 9. Agent Migration Support

CNP provides the transport layer for agent migration (as introduced in RFC-0020).

Requirements:

- Migration requests **MUST** include a checkpoint and capability proof.
- The target node **MUST** validate the checkpoint and capabilities before accepting the agent.
- Migration events **MUST** be recorded in the global event log.

### 10. Fault Tolerance

CNP **MUST** support detection and recovery from node failures, including:

- Heartbeat and failure detection
- Event log reconciliation after node recovery
- Checkpoint-based state restoration on replacement nodes

### 11. Open Questions

The following areas require future specification:

- Concrete wire protocol (e.g., QUIC, gRPC, custom binary)
- Cryptographic identity and trust model
- Routing and topology management
- Quality-of-service guarantees for cognitive traffic

---

**RFC-0021 — Cognitive Network Protocol (CNP) v1.0 Draft** is now complete.

This RFC establishes the communication and coordination layer required for distributed cognitive execution, completing the transition from a single-node cognitive runtime to a distributed cognitive operating platform.
