<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #10, sub-message [93], 2026-08-10
  Verbatim source: knowledge-base/sources/message-010-original-part*.md
  Status in corpus: RFC-0006 Capability Model v1.2 (Candidate for Final Ratification); final review [94] recommendation: Ratify / approved for Final Ratification. Ratification record not present in corpus. Supersedes v1.0 [89] and v1.1 [91] (preserved in archive).
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0006 — Capability Model**

**Version:** 1.2  

**Status:** Candidate for Final Ratification  

**Parent:** RFC-0004 Goal Lifecycle and Satisfaction Model v1.1 (Ratified)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the semantics, lifecycle, metadata, relationships, and enforcement model for `capability!` values in Red/Cognition.

Capabilities represent explicit, revocable permissions that mediate an agent’s ability to produce external effects. Because cognitive execution must remain secure, deterministic, explainable, and replayable, the creation, granting, revocation, and usage of capabilities must be explicitly governed.

### 2. Design Principles

The capability model follows these principles:

- **Explicitness** — Capabilities are first-class values that must be explicitly granted and referenced.
- **Least Privilege** — Agents should hold only the minimum capabilities required to achieve their goals.
- **Revocability** — Capabilities can be revoked at any time by their granting authority.
- **Auditability** — All capability grants, revocations, and usages must be traceable.
- **Provider Neutrality** — The capability model is independent of any specific reasoning or planning mechanism.

### 3. Capability Identity and Metadata

Every capability is identified by a stable **CapabilityID**.

- The `CapabilityID` **MUST** remain constant across the capability lifecycle.
- Every modification to a capability, including revocation, expiration, delegation metadata, or administrative updates, **MUST** increment the capability version while preserving the `CapabilityID`.
- Every capability **MUST** include the following metadata:

```
capability {
    cognitive-meta { id, created, modified, provenance, version }
    type: capability-type
    scope
    owner: AgentID | Runtime | CogOS
    granted-to: AgentID
    granted-by: authority
    delegated-from: CapabilityID (optional)
    expiration: timestamp (optional)
    status: active | revoked | expired
}
```

**Scope immutability**: Scope **MUST** be immutable after capability issuance.

### 4. Capability Lifecycle

Every capability **MUST** follow this lifecycle:

```
Created
   ↓
Granted
   ↓
Active
   ↓
Revoked / Expired
```

**Legal status transitions**:

| From     | To        | Allowed |
|----------|-----------|---------|
| Created  | Granted   | ✓       |
| Granted  | Active    | ✓       |
| Active   | Revoked   | ✓       |
| Active   | Expired   | ✓       |
| Revoked  | Active    | ✗       |
| Expired  | Active    | ✗       |

### 5. Capability Types and Scope

Capabilities **MAY** be classified by type. Every capability **MUST** declare its scope.

Capability inheritance and dependency relationships **MUST** form a Directed Acyclic Graph (DAG). Cycles **MUST** be rejected.

### 6. Capability Resolution Order

Before an effect executes, the system **MUST** verify the following in deterministic order:

1. Capability exists
2. Status == Active
3. Scope is valid
4. Not expired
5. Not revoked
6. Policy allows the action

Evaluation **MUST** terminate at the first failed validation step, and the failure reason **MUST** be recorded in the execution trace.

### 7. Capability Grants, Revocations, and Effects

Capability grants and revocations **MUST** themselves be represented as `effect!` values (RFC-0002).

### 8. Capability Enforcement

The Cognitive Runtime and Cognitive Operating System **MUST** enforce capability checks before allowing external effects.

Requirements:

- Capability checks **MUST** occur before effect execution.
- Capability violations **MUST** produce traceable errors.
- Capability usage **MUST** be recorded in execution traces.

### 9. Capability Trace Contract

Every capability usage **MUST** produce a trace entry:

```
CapabilityTrace {
    CapabilityID,
    AgentID,
    EffectID,
    Timestamp,
    Decision: Allow | Deny
}
```

### 10. Capability Ownership and Delegation

Capabilities distinguish between **owner** and **grantee**.

Capabilities **MAY** be delegable. Delegated capabilities **MUST** preserve provenance and **MUST** reference the granting capability via `delegated-from`.

### 11. Memory Placement

- Active capabilities **SHALL** reside in Working Memory.
- Capability definitions **MAY** reside in Semantic Memory.
- Revoked and expired capabilities **SHOULD** be archived in Episodic Memory.

### 12. Relationship to Beliefs

Capability grants and revocations **MAY** update an agent’s beliefs about its own permissions and the permissions of other agents.

### 13. Replay and Determinism

Replayed executions **MUST** respect the same capability constraints that existed during the original execution.

A conforming implementation **MUST** ensure that:

- Capability checks occur at the same points in the causal chain.
- Revoked capabilities remain revoked during replay.
- Capability violations produce equivalent error behaviour.

### 14. Conformance Requirements

A conforming implementation **MUST**:

- Preserve `CapabilityID`.
- Enforce capability checks before external effects.
- Record every grant, revocation, and usage.
- Preserve capability state during replay.
- Reject invalid capability transitions.
- Include its authority policy in conformance reports.

### 15. Open Questions

The following areas require future specification:

- Formal capability algebra
- Capability delegation and transfer semantics
- Distributed capability management
- Capability auditing and verification protocols

---

**RFC-0006 — Capability Model v1.2** is now ready for **Final Ratification**.
