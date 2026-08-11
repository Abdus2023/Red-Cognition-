<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #23, sub-message [239], 2026-08-11
  Verbatim source: knowledge-base/sources/message-023-original-part*.md
  Status in corpus: RFC-0053 CRAIP v1.1 (Candidate for Ratification); supersedes v1.0 draft of sub-message [237] (preserved in archive). Reviews: [238] (v1.0: Draft, 85-90%), [240] (v1.1: 95-98%, recommends v1.2; "would not ratify v1.1 immediately"). Source quirk preserved as received: stray closing parenthesis after RemoteInvocationFailed in §13 (flagged in [240] §8). No ratification decision present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->


**RFC-0053 — Cognitive Remote Agent Invocation Protocol (CRAIP) v1.1**

**Version:** 1.1  

**Status:** Candidate for Ratification  

**Parent:** RFC-0052 Cognitive Testing and Verification Framework (CTVF) v1.2 (Candidate)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Remote Agent Invocation Protocol (CRAIP)** for Red/Cognition.

CRAIP specifies the mechanisms for invoking, coordinating, and communicating with remote cognitive agents across process, machine, and organizational boundaries. It builds on the distributed execution foundation (RFC-0020), network protocol (RFC-0021), identity and trust framework (RFC-0022), foreign function interface (RFC-0048), and verification framework (RFC-0052), while integrating with the broader architecture defined in RFC-0050.

The protocol ensures that remote cognitive interactions remain deterministic, capability-aware, traceable, and replayable.

### 2. Design Principles

CRAIP follows these principles:

- **Determinism** — Remote invocations must produce reproducible results given the same inputs, state, and environment.

- **Capability-Oriented Invocation** — All remote operations must be explicitly authorized through capabilities.

- **Provider Neutrality** — The protocol must remain independent of specific reasoning or planning mechanisms.

- **Replay Equivalence** — Replayed remote executions must produce equivalent observable behaviour.

- **Authenticated Communication** — All cross-agent interactions must be authenticated and authorized.

- **Traceability** — All remote operations must participate in the unified event log.

### 3. Invocation Model

CRAIP supports the following invocation patterns:

- **Request/Response** — Synchronous invocation with a single result.

- **Asynchronous Invocation** — Fire-and-forget or callback-based invocation.

- **Streaming** — Continuous result streams from long-running cognitive operations.

- **Event Subscription** — Subscription to remote events and state changes.

- **Broadcast** — One-to-many invocation across multiple agents or domains.

- **Delegated Execution** — Invocation where one agent delegates authority to another.

### 4. Agent Identity and Discovery

Every remote invocation **MUST** involve stable, verifiable identities (RFC-0022).

Requirements:

- Agents **MUST** advertise supported capabilities, CISA revision, and RFC conformance.

- Discovery **MUST** support endpoint resolution, version negotiation, and trust establishment.

- All discovery and identity operations **MUST** be recorded in the event log.

#### 4.1 Agent Manifest

Agents **MUST** publish an `AgentManifest`:

```

AgentManifest {

    AgentID,

    Version,

    SupportedMethods,

    Capabilities,

    SupportedRFCs,

    RuntimeVersion,

    SecurityLevel,

    Endpoint

}

```

### 5. Invocation Contract

Every remote invocation **MUST** be accompanied by an `InvocationManifest`:

```

InvocationManifest {

    InvocationID,

    AgentID,

    CallerID,

    ProtocolVersion,

    Method,

    Parameters,

    RequiredCapabilities,

    ExpectedEffects,

    Timeout,

    Priority,

    Deadline,

    ReplayPolicy,

    TraceContext,

    AuthenticationContext,

    VersionConstraints

}

```

### 6. Protocol State Machine

Every remote invocation **MUST** follow this state machine:

```

Created

   ↓

Authenticated

   ↓

Authorized

   ↓

Scheduled

   ↓

Executing

   ↓

Completed

   |

   ├── Failed

   ├── Cancelled

   └── TimedOut

```

### 7. Protocol Messages

CRAIP defines the following core message types:

- **Request** — Initiate a remote cognitive operation.

- **Response** — Return the result of a completed operation.

- **Error** — Report failure using a structured error schema.

- **Cancellation** — Request termination of an in-progress invocation.

- **Heartbeat** — Maintain connection state for long-running operations.

- **Event** — Deliver asynchronous notifications or state changes.

#### 7.1 Standard Error Schema

```

RemoteError {

    Code,

    Category,

    Message,

    Retryable,

    CapabilityViolation,

    TraceReference,

    Cause

}

```

### 8. Capability and Policy Enforcement

All remote invocations **MUST** pass through capability and policy checks before execution.

Requirements:

- The `InvocationManifest` **MUST** declare required capabilities.

- The receiving agent **MUST** verify capabilities against its local policy (RFC-0025).

- Capability violations **MUST** produce traceable errors and participate in the event log.

### 9. Deterministic Replay Requirements

Replayed remote invocations **MUST** produce equivalent observable behaviour.

Requirements:

- All non-deterministic external inputs **MUST** be recorded during the original execution.

- Replays **MUST** use recorded values rather than re-invoking external systems.

- Invocation ordering **MUST** respect the causal ordering defined in RFC-0002 and RFC-0023.

### 10. Security Model

CRAIP integrates with the identity and trust framework (RFC-0022) and security policy language (RFC-0025).

Requirements:

- All messages **MUST** be authenticated.

- Sensitive payloads **MAY** be encrypted.

- Replay protection mechanisms **MUST** be employed.

- Mutual authentication **MAY** be required for high-trust interactions.

### 11. Transport Bindings

CRAIP is defined abstractly and **MAY** be bound to multiple transports, provided they satisfy the following mandatory properties:

- Reliable delivery

- Message ordering (within a single invocation)

- Framing

- Integrity protection

- Authentication support

- Flow control

### 12. Failure Semantics

CRAIP defines the following failure handling mechanisms:

- Timeouts

- Retries with deterministic backoff

- Cancellation propagation

- Partial failure handling

- Idempotency guarantees where applicable

- Compensation actions for failed remote operations

### 13. Observability

CRAIP integrates with the observability protocol (RFC-0046).

Requirements:

- Trace context **MUST** be propagated across remote invocations.

- Lifecycle events `RemoteInvocationStarted`, `RemoteInvocationCompleted`, `RemoteInvocationFailed`) **MUST** be emitted.

- Structured diagnostics **MUST** be produced for failures and policy violations.

- `TraceContext` **MUST** include `TraceID`, `ParentInvocation`, `Epoch`, `SpanID`, `DeterminismLevel`, `CapabilityContext`, and `ReplaySessionID`.

### 14. Standard CLI

A conforming implementation **SHOULD** provide the following commands:

```

cog invoke

cog agent discover

cog agent list

cog trace remote

cog replay remote

cog verify remote

```

### 15. Conformance Profiles

CRAIP defines the following conformance profiles:

| Profile       | Capabilities                                      |

|---------------|---------------------------------------------------|

| **Minimal**   | Basic request/response invocation                 |

| **Developer** | Minimal + asynchronous + streaming                |

| **Distributed** | Developer + event subscription + broadcast    |

| **Enterprise**| Distributed + delegated execution + policy enforcement |

| **Federation**| Enterprise + cross-domain trust negotiation       |

### 16. Relationship to Other RFCs

CRAIP integrates with RFC-0020, RFC-0021, RFC-0022, RFC-0048, RFC-0050, and RFC-0052.

### 17. Open Questions

The following areas require future specification:

- Cross-federation routing and discovery

- Remote macro execution semantics

- Distributed scheduling coordination

- Multi-party coordination protocols

---

**RFC-0053 — Cognitive Remote Agent Invocation Protocol (CRAIP) v1.1** is now ready for **Final Ratification Review**.

This version incorporates a normative protocol state machine, richer `InvocationManifest`, standardized error model, `AgentManifest` for discovery, version negotiation rules, transport property requirements, distributed tracing schema, verification artifact integration, and a conformance matrix, bringing it in line with the precision of the strongest RFCs in the series.
