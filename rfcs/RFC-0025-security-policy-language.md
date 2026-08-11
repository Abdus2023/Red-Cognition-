<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #16, sub-message [143], 2026-08-10
  Verbatim source: knowledge-base/sources/message-016-original-part*.md
  Status in corpus: RFC-0025 Cognitive Security Policy Language (CSPL) v1.0 (Draft); review [144]: policy engine, PolicyDecisionEvent, PolicyError, Policy VM proposal (RFC-0025.1); v1.1 not present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0025 — Cognitive Security Policy Language (CSPL)**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0024 Cognitive Resource Management and Quota Model v1.0 (Draft)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Security Policy Language (CSPL)** for Red/Cognition.

As the number of agents, capabilities, resources, and distributed nodes grows, the system requires a formal, deterministic, and auditable way to express security policies. CSPL provides a declarative language for defining rules that govern capability usage, resource allocation, trust relationships, and effect authorization across the Cognitive Operating System.

### 2. Design Principles

CSPL follows these principles:

- **Determinism** — Policy evaluation must produce reproducible results given the same inputs and state.
- **Traceability** — All policy decisions must be recorded in the event log.
- **Capability Integration** — Policies must integrate with the capability model (RFC-0006).
- **Replay Equivalence** — Replayed executions must produce equivalent policy decisions.
- **Provider Neutrality** — The policy language must remain independent of specific reasoning mechanisms.
- **Least Privilege** — Policies should enable fine-grained control aligned with the principle of least privilege.

### 3. Policy Structure

A CSPL policy consists of the following elements:

```
Policy {
    PolicyID
    Scope: [Agent | Node | Domain | System]
    Rules: [Rule]
    Priority
    Version
}
```

Each rule has the form:

```
Rule {
    Subject,
    Action,
    Resource,
    Condition,
    Effect: Allow | Deny
}
```

### 4. Core Policy Domains

CSPL supports policies in the following domains:

- **Capability Policies** — Control which capabilities may be granted or used.
- **Resource Policies** — Enforce quotas and usage limits.
- **Trust Policies** — Define identity and attestation requirements.
- **Effect Policies** — Authorize or restrict classes of effects.
- **Agent Policies** — Govern agent lifecycle and coordination.
- **Domain Policies** — Define boundaries between trust domains.

### 5. Policy Evaluation Model

Policy evaluation follows this deterministic order:

1. Collect applicable policies for the subject, action, and resource.
2. Evaluate conditions in priority order.
3. Apply the first matching rule (Allow or Deny).
4. Record the decision and provenance in the event log.

If no rule matches, the default is **Deny**.

### 6. Relationship to Other RFCs

CSPL integrates with:

- RFC-0006 — Capability Model (authorization decisions)
- RFC-0022 — Identity and Trust Framework (subject verification)
- RFC-0024 — Resource Management (quota enforcement)
- RFC-0011 — Scheduler (policy-aware scheduling)
- RFC-0015 — Exception Semantics (policy violation handling)
- RFC-0018 — Event Log (recording policy decisions)

### 7. Policy Trace Contract

Every policy decision **MUST** produce a trace entry:

```
PolicyDecisionTrace {
    TraceID,
    Timestamp,
    PolicyID,
    Subject,
    Action,
    Resource,
    Decision: Allow | Deny,
    Reason
}
```

### 8. Replay and Determinism

Replayed executions **MUST** produce equivalent policy decisions.

A conforming implementation **MUST** ensure that:

- The same policy set and inputs produce the same decision.
- Policy decisions are recorded with sufficient context for replay.

### 9. Open Questions

The following areas require future specification:

- Concrete syntax and semantics of the policy language
- Policy distribution and synchronization across nodes
- Formal verification of policy sets
- Conflict resolution between overlapping policies

---

**RFC-0025 — Cognitive Security Policy Language (CSPL) v1.0 Draft** is now complete.

This RFC establishes a declarative, deterministic policy layer that governs authorization, resource usage, and trust across the entire Red/Cognition stack. It provides the governance foundation needed for secure, auditable, and replayable multi-agent cognitive systems.
