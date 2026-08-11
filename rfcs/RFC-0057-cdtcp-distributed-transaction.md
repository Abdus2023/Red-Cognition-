<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #26, sub-message [265], 2026-08-11
  Verbatim source: knowledge-base/sources/message-026-original-part*.md
  Status in corpus: RFC-0057 CDTCP v1.3 (Candidate for Final Ratification); three successive iterations under the same version label: [261] → [263] (adds §7.1 Wire Message Schemas) → [265] (adds Prepared vote schema) (D-85/D-86); supersedes v1.0 [255], v1.1 [257], v1.2 [259] (preserved in archive). RATIFIED per review assessment [266] ("Ready for Ratification") and user ratification record [267]. Reviews [262]/[264]/[266] preserved in archive.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->


**RFC-0057 — Cognitive Distributed Transaction and Consistency Protocol (CDTCP) v1.3**

**Version:** 1.3  

**Status:** Candidate for Final Ratification  

**Parent:** RFC-0056 Cognitive Shared Memory and Knowledge Synchronization Protocol (CSMKSP) v1.0 (Draft)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Distributed Transaction and Consistency Protocol (CDTCP)** for Red/Cognition.

As multiple cognitive agents coordinate on shared goals and knowledge (RFC-0055 and RFC-0056), the system requires mechanisms to execute operations atomically across agents and domains while maintaining determinism, traceability, and replay equivalence. CDTCP establishes the transaction model, isolation levels, commit protocols, compensation mechanisms, and consistency guarantees for distributed cognitive operations.

This protocol completes the distributed cognition stack by adding a dedicated transaction layer that ensures coordinated, atomic, and recoverable multi-agent behavior.

### 2. Design Principles

CDTCP follows these principles:

- **Atomicity** — A distributed cognitive transaction must either fully commit or fully abort with compensation.

- **Determinism** — Transaction outcomes must be reproducible given the same inputs and state.

- **Traceability** — All transaction events must participate in the unified event log.

- **Replay Equivalence** — Replayed transactions must produce equivalent observable outcomes.

- **Capability Awareness** — Transaction participation and effects must be capability-gated.

- **Provider Neutrality** — The protocol must remain independent of specific reasoning mechanisms.

### 3. Transaction Manifest

Every cognitive transaction **MUST** begin with an immutable `TransactionManifest`:

```

TransactionManifest {

    TransactionID,

    CoordinatorID,

    Participants,

    IsolationLevel,

    RequiredCapabilities,

    ExpectedEffects,

    Timeout,

    Priority,

    Deadline,

    ReplayPolicy,

    RetryPolicy,

    VersionConstraints,

    TraceContext,

    CompensationPlan

}

```

### 4. Transaction Identifier Requirements

- `TransactionID` **MUST** be globally unique.

- A `TransactionID` **MUST NOT** be reused after completion.

- Participants **MUST** reject duplicate `BeginTransaction` messages for completed transactions.

### 5. Participant State Machine

Every transaction participant **MUST** follow this state machine:

```

Created

   ↓

Registered

   ↓

Prepared

   ↓

Ready

   ↓

Committed

   |

   ├── Aborted

   ├── Compensated

   └── TimedOut

```

### 6. Coordinator State Machine

The transaction coordinator **MUST** follow this state machine:

```

Created

   ↓

CollectingParticipants

   ↓

Preparing

   ↓

Committing

   |

   ├── Aborting

   ├── Recovering

   └── Compensating

   ↓

Archived

```

### 7. Standard Protocol Messages

CDTCP defines the following core message types:

- `BeginTransaction`

- `JoinTransaction`

- `Prepare`

- `Prepared`

- `Commit`

- `Committed`

- `Abort`

- `Aborted`

- `Compensate`

- `Compensated`

- `Heartbeat`

- `Status`

#### 7.1 Wire Message Schemas (Normative)

```

Prepare {

    TransactionID,

    Epoch,

    ParticipantID,

    ManifestHash

}

Prepared {

    TransactionID,

    Epoch,

    ParticipantID,

    Vote: Commit | Abort

}

Commit {

    TransactionID,

    Epoch,

    DecisionProof

}

Abort {

    TransactionID,

    Epoch,

    Reason

}

Compensate {

    TransactionID,

    Epoch,

    CompensationPlan

}

```

### 8. Transaction Log Schema

Every transaction decision **MUST** be recorded in a deterministic log:

```

TransactionLogEntry {

    TransactionID,

    ParticipantID,

    Phase,

    Timestamp,

    Epoch,

    Effects,

    Decision,

    TraceReference

}

```

### 9. Deterministic Ordering

Concurrent transactions **MUST** be ordered according to:

- The deterministic scheduler (RFC-0011)

- Effect ordering (RFC-0002)

- Distributed causal ordering (RFC-0023)

Replay **MUST** preserve the same ordering.

### 10. Isolation Semantics

CDTCP defines the following isolation levels:

| Level            | Description                                      | Uncommitted Visibility |

|------------------|--------------------------------------------------|------------------------|

| Read Uncommitted | May see uncommitted data                         | Allowed                |

| Read Committed   | Sees only committed data                         | Not allowed            |

| Repeatable Read  | Same reads return consistent results             | Not allowed            |

| Snapshot         | Operates on a consistent snapshot                | Not allowed            |

| Serializable     | Appears to execute sequentially                  | Not allowed            |

### 11. Commit Decision Rules

A transaction **MAY** commit only when all of the following are true:

- Every participant has reached the `Ready` state.

- All required capabilities remain valid.

- Replay constraints are satisfied.

- Policy evaluation has succeeded.

### 12. Commit Durability

A commit decision **MUST** be durably recorded before `Commit` messages are emitted.

### 13. Timeout Semantics

- Timeout **MUST** start at the beginning of the `Prepare` phase.

- Timeout **MUST** include any compensation phase.

- Timeout **MUST** reset upon receipt of a heartbeat.

- Timeout policy **MUST** be deterministic and declared in the `TransactionManifest`.

### 14. Failure Matrix

The protocol defines the following normative failure behaviors:

| Failure                  | Required Behavior                          |

|--------------------------|--------------------------------------------|

| Coordinator crash        | Recovery from checkpoint                   |

| Participant timeout      | Abort or compensation                      |

| Network partition        | Suspend until policy decision              |

| Replay mismatch          | Verification failure                       |

| Capability revoked       | Immediate abort                            |

### 15. Idempotency

The following messages **MUST** be idempotent:

- `Commit`

- `Abort`

- `Compensate`

### 16. Compensation Ordering

Compensation actions **MUST** be executed in reverse dependency order of the original transaction steps.

Nested compensation **MUST** be explicitly declared in the `CompensationPlan`.

### 17. Read-Only Participants

A participant that only performs read operations **MAY** respond with `ReadOnly` during the `Prepare` phase and transition directly to `Archived` upon receiving a `Commit` message.

### 18. Transaction Events

CDTCP defines the following standard events (integrated with RFC-0018):

- `TransactionCreated`

- `ParticipantJoined`

- `PrepareStarted`

- `PrepareSucceeded`

- `PrepareFailed`

- `CommitStarted`

- `Committed`

- `Aborted`

- `CompensationStarted`

- `CompensationCompleted`

- `TransactionArchived`

### 19. Security

CDTCP integrates with RFC-0022 (Identity and Trust) and RFC-0025 (Security Policy).

Requirements:

- Coordinator election **MUST** be authenticated.

- Transaction integrity **MUST** be protected.

- Replay protection tokens **MUST** be employed.

- Coordinator and participant identities **MUST** be verified.

### 20. Transaction Error Schema

```

TransactionError {

    Code,

    Category,

    Retryable,

    Participant,

    Phase,

    Cause,

    TraceReference

}

```

### 21. Standard CLI

A conforming implementation **SHOULD** provide the following commands:

```

cog tx begin

cog tx status

cog tx prepare

cog tx commit

cog tx abort

cog tx compensate

cog tx replay

cog tx verify

```

### 22. Conformance Profiles

CDTCP defines the following conformance profiles:

| Profile      | Capabilities                                      |

|--------------|---------------------------------------------------|

| **Minimal**  | Local transactions                                |

| **Developer**| Distributed prepare/commit                        |

| **Professional** | Compensation + replay                         |

| **Enterprise** | Consensus + policy enforcement                |

| **Verified** | Proof-backed transaction correctness              |

### 23. Verification Integration

Every transaction **SHOULD** produce or reference verification artifacts (RFC-0052), including:

- Transaction replay verification

- Compensation verification

- Isolation verification

- Determinism verification

- Transaction coverage metrics

### 24. Relationship to Other RFCs

CDTCP integrates with RFC-0002, RFC-0006, RFC-0023, RFC-0055, and RFC-0056.

### 25. Open Questions

The following areas require future specification:

- Concrete transaction log format

- Optimistic vs. pessimistic concurrency control

- Multi-domain transaction coordination

- Formal verification of compensation correctness

---

**RFC-0057 — Cognitive Distributed Transaction and Consistency Protocol (CDTCP) v1.3** is now ready for **Final Ratification Review**.

This version incorporates a normative `TransactionManifest`, participant state machine, coordinator state machine, standard protocol messages with wire schemas, transaction log schema, deterministic ordering rules, isolation semantics, commit decision rules, commit durability, timeout semantics, failure matrix, idempotency requirements, compensation ordering, read-only participant handling, transaction events, security requirements, transaction error schema, standard CLI, conformance profiles, and verification integration, bringing it in line with the precision of the strongest RFCs in the series.
