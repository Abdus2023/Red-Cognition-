# Source Record: Conversation Message #10 — Verbatim Transcript (Part 3 of 5: sub-messages [89]–[92])

- **Message index:** 10 (continued) · **Part 2:** `message-010-original-part2.md` · **Cleanup:** as Part 1. Note: sub-message [91] arrived with trailing-whitespace artifacts on many lines (including inside fenced blocks); preserved exactly as received.

---

## [89] USER

**RFC-0006 — Capability Model**

**Version:** 1.0  

**Status:** Draft  

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

Every capability **MUST** include the metadata defined in RFC-0001, plus capability-specific attributes:

```
capability {
    cognitive-meta { id, created, modified, provenance, version }
    type: capability-type
    scope
    granted-to: AgentID
    granted-by: authority
    expiration: timestamp (optional)
    status: active | revoked | expired
}
```

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

### 5. Capability Types and Scope

Capabilities **MAY** be classified by type (e.g., file access, network access, memory access, sensor access, actuator control).

Every capability **MUST** declare its scope, which defines the resources or actions it authorizes.

### 6. Relationship to Effects and Goals

Capabilities mediate the production of effects (RFC-0002) and the satisfaction of goals (RFC-0004).

Requirements:

- An effect that changes external state **MUST** reference the authorizing capability.
- A goal **MAY** declare required capabilities.
- Execution of a plan step **MUST** verify the required capability before producing an external effect.

### 7. Capability Enforcement

The Cognitive Runtime and Cognitive Operating System **MUST** enforce capability checks before allowing external effects.

Requirements:

- Capability checks **MUST** occur before effect execution.
- Capability violations **MUST** produce traceable errors.
- Capability usage **MUST** be recorded in execution traces.

### 8. Capability Revocation

Capabilities **MAY** be revoked at any time by their granting authority.

Revocation **MUST**:

- Immediately invalidate the capability.
- Prevent further use of the revoked capability.
- Be recorded in the execution trace.

### 9. Relationship to Beliefs

Capability grants and revocations **MAY** update an agent’s beliefs about its own permissions and the permissions of other agents.

### 10. Replay and Determinism

Replayed executions **MUST** respect the same capability constraints that existed during the original execution.

A conforming implementation **MUST** ensure that:

- Capability checks occur at the same points in the causal chain.
- Revoked capabilities remain revoked during replay.
- Capability violations produce equivalent error behaviour.

### 11. Open Questions

The following areas require future specification:

- Formal capability algebra
- Capability delegation and transfer semantics
- Distributed capability management
- Capability auditing and verification protocols

---

**RFC-0006 — Capability Model v1.0 Draft** is now complete.

This RFC establishes the security and authorization foundation for cognitive execution. It forms a critical layer that governs how agents interact with the external world through the effect system (RFC-0002) and goal satisfaction process (RFC-0004).

---

## [90] CHATGPT (gpt-5-5)

This is a strong continuation of the Red/Cognition specification family. RFC-0006 fits naturally after RFC-0005 and provides the security model that the previous RFCs already reference. From an architectural perspective, it is internally consistent with RC-500 through RC-800.

For **Final Ratification**, I would recommend a few normative refinements to make the specification easier to implement and verify.

### Strengths

- Clearly establishes `capability!` as a first-class cognitive type.
- Separates authorization from reasoning, preserving provider neutrality.
- Aligns with the deterministic and replayable execution model established in RFC-0002.
- Integrates cleanly with Goals, Plans, Effects, and the Cognitive Runtime.
- Uses explicit lifecycle semantics consistent with earlier RFCs.

### Recommended additions for v1.1

**1. Stable Capability Identity**

Like `GoalID`, `BeliefID`, and `PlanID`, define a stable identifier.

```text
Every capability SHALL possess a stable CapabilityID.
The CapabilityID MUST remain constant throughout the capability lifecycle,
including serialization, checkpointing, restoration, and replay.
```

---

**2. Capability Ownership**

Explicitly distinguish ownership from usage.

```text
owner: AgentID | Runtime | CogOS
delegatee: AgentID (optional)
```

This becomes important once delegation is introduced.

---

**3. Capability Graph**

Capabilities naturally form dependencies.

Example:

```text
filesystem
      │
      ├── read
      ├── write
      └── delete
```

Normative rule:

> Capability inheritance MUST form a Directed Acyclic Graph (DAG).

---

**4. Capability Resolution Order**

Before an effect executes:

```text
Capability Exists
        ↓
Status == Active
        ↓
Scope Valid
        ↓
Not Expired
        ↓
Not Revoked
        ↓
Policy Allows
        ↓
Effect Executes
```

This defines deterministic enforcement.

---

**5. Delegation Semantics**

Reserve future compatibility.

```text
Capabilities MAY be delegable.
Delegated capabilities MUST preserve provenance
and MUST reference the granting capability.
```

---

**6. Capability Trace Contract**

Every capability use should produce a trace entry.

Example:

```text
CapabilityTrace {
    CapabilityID
    AgentID
    EffectID
    Timestamp
    Decision: Allow | Deny
}
```

This greatly improves explainability.

---

**7. Memory Placement**

To match previous RFCs:

```text
Active capabilities SHALL reside in Working Memory.
Capability definitions MAY reside in Semantic Memory.
Revoked and expired capabilities SHOULD be archived in Episodic Memory.
```

---

**8. Conformance Section**

Like RFC-0001.

A conforming implementation MUST:

- Preserve CapabilityID.
- Enforce capability checks before external effects.
- Record every grant, revocation, and usage.
- Preserve capability state during replay.
- Reject invalid capability transitions.

---

## Architectural dependency chain

The RFC series now forms a coherent semantic stack:

```text
RFC-0001  Cognitive Types
        │
        ▼
RFC-0002  Effect Ordering
        │
        ▼
RFC-0003  Belief Revision
        │
        ▼
RFC-0004  Goal Lifecycle
        │
        ▼
RFC-0005  Planning Semantics
        │
        ▼
RFC-0006  Capability Model
```

This sequence cleanly defines the core cognitive semantics before moving into higher-level topics such as skills, memory architecture, scheduling, and multi-agent coordination.

Overall, I would assess **RFC-0006 v1.0** as approximately **95% complete**. With the additions above—particularly `CapabilityID`, conformance requirements, memory placement, deterministic enforcement order, and trace contracts—it would be ready for **v1.1 Candidate for Final Ratification** and would complete the foundational semantic model of the Red/Cognition architecture.

---

## [91] USER

**RFC-0006 — Capability Model**    

**Version:** 1.1      

**Status:** Candidate for Ratification      

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

- Every capability **MUST** include the metadata defined in RFC-0001, plus capability-specific attributes:    

```
capability {    
    cognitive-meta { id, created, modified, provenance, version }    
    type: capability-type    
    scope    
    owner: AgentID | Runtime | CogOS    
    granted-to: AgentID    
    granted-by: authority    
    expiration: timestamp (optional)    
    status: active | revoked | expired    
}    
```

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

### 5. Capability Types and Scope    

Capabilities **MAY** be classified by type (e.g., file access, network access, memory access, sensor access, actuator control).    

Every capability **MUST** declare its scope, which defines the resources or actions it authorizes.    

### 6. Capability Graph    

Capabilities **MAY** form dependency relationships.    

Requirements:    

- Capability inheritance **MUST** form a Directed Acyclic Graph (DAG).    

- Cycles **MUST** be rejected.    

- A dependent capability **MUST NOT** be granted before its prerequisite capabilities are active.    

### 7. Capability Resolution Order    

Before an effect executes, the system **MUST** verify the following in order:    

1. Capability exists    

2. Status == Active    

3. Scope is valid    

4. Not expired    

5. Not revoked    

6. Policy allows the action    

7. Effect executes    

### 8. Relationship to Effects and Goals    

Capabilities mediate the production of effects (RFC-0002) and the satisfaction of goals (RFC-0004).    

Requirements:    

- An effect that changes external state **MUST** reference the authorizing capability.    

- A goal **MAY** declare required capabilities.    

- Execution of a plan step **MUST** verify the required capability before producing an external effect.    

### 9. Capability Enforcement    

The Cognitive Runtime and Cognitive Operating System **MUST** enforce capability checks before allowing external effects.    

Requirements:    

- Capability checks **MUST** occur before effect execution.    

- Capability violations **MUST** produce traceable errors.    

- Capability usage **MUST** be recorded in execution traces.    

### 10. Capability Revocation    

Capabilities **MAY** be revoked at any time by their granting authority.    

Revocation **MUST**:    

- Immediately invalidate the capability.    

- Prevent further use of the revoked capability.    

- Be recorded in the execution trace.    

### 11. Capability Trace Contract    

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

### 12. Capability Ownership and Delegation    

Capabilities distinguish between **owner** and **grantee**.    

Capabilities **MAY** be delegable. Delegated capabilities **MUST** preserve provenance and **MUST** reference the granting capability.    

### 13. Memory Placement    

- Active capabilities **SHALL** reside in Working Memory.    

- Capability definitions **MAY** reside in Semantic Memory.    

- Revoked and expired capabilities **SHOULD** be archived in Episodic Memory.    

### 14. Relationship to Beliefs    

Capability grants and revocations **MAY** update an agent’s beliefs about its own permissions and the permissions of other agents.    

### 15. Replay and Determinism    

Replayed executions **MUST** respect the same capability constraints that existed during the original execution.    

A conforming implementation **MUST** ensure that:    

- Capability checks occur at the same points in the causal chain.    

- Revoked capabilities remain revoked during replay.    

- Capability violations produce equivalent error behaviour.    

### 16. Conformance Requirements    

A conforming implementation **MUST**:    

- Preserve `CapabilityID`.    

- Enforce capability checks before external effects.    

- Record every grant, revocation, and usage.    

- Preserve capability state during replay.    

- Reject invalid capability transitions.    

### 17. Open Questions    

The following areas require future specification:    

- Formal capability algebra    

- Capability delegation and transfer semantics    

- Distributed capability management    

- Capability auditing and verification protocols    

---    

**RFC-0006 — Capability Model v1.1** is now ready for **Final Ratification Review**.

---

## [92] CHATGPT (gpt-5-5)

**Review: RFC-0006 — Capability Model v1.1**

This revision addresses the major architectural gaps identified in the draft and is consistent with the rest of the Red/Cognition specification family. It now provides a coherent normative model for capability-based authorization that integrates cleanly with RFC-0001 through RFC-0005 and the RC-500–RC-800 architecture.

### Ratification Assessment

**Status:** **Ready for Final Ratification**, with a few optional editorial refinements suitable for a future v1.2 rather than blocking ratification.

### Strengths

The specification now includes:

- Stable `CapabilityID` identity and lifecycle.
- A well-defined metadata contract.
- Deterministic capability resolution order.
- Explicit capability dependency graph (DAG).
- Clear separation of ownership and grant semantics.
- Trace contract for auditing.
- Memory placement consistent with the cognitive memory model.
- Conformance requirements.
- Replay guarantees aligned with RFC-0002 and RFC-0003.

This makes the capability model sufficiently complete for compiler, runtime, CVM, and CogOS implementations.

### Minor Normative Recommendations

These are improvements rather than deficiencies.

#### 1. Versioning Rule

The specification introduces `version` in metadata but does not explicitly define when it changes.

Consider adding:

> Every modification to a capability, including revocation, expiration, delegation metadata, or administrative updates, **MUST** increment the capability version while preserving the `CapabilityID`.

This mirrors the identity/versioning model used by goals, beliefs, and plans.

---

#### 2. Status Transition Table

Instead of only the lifecycle diagram, define legal transitions.

Example:

| From | To | Allowed |
|------|----|---------|
| Created | Granted | ✓ |
| Granted | Active | ✓ |
| Active | Revoked | ✓ |
| Active | Expired | ✓ |
| Revoked | Active | ✗ |
| Expired | Active | ✗ |

This improves conformance testing.

---

#### 3. Delegation Provenance

The delegation section could specify:

```text
delegated-from: CapabilityID
```

This creates a deterministic delegation chain suitable for auditing and replay.

---

#### 4. Capability Resolution Failures

The resolution order is excellent, but the specification could explicitly require deterministic failure.

For example:

> Evaluation **MUST** terminate at the first failed validation step, and the failure reason **MUST** be recorded in the execution trace.

This ensures identical behaviour across implementations.

---

#### 5. Capability Scope

The `scope` field could benefit from a normative statement.

For example:

> Scope **MUST** be immutable after capability issuance.

Changing scope after issuance would complicate replay and auditing.

---

#### 6. Capability Effects

Because RFC-0002 models effects as first-class entities, it would be useful to state:

> Capability grants and revocations are themselves represented as `effect!` values.

That keeps every externally observable state change within the effect model.

### Specification Maturity

Current maturity of the foundational RFC series:

| RFC | Topic | Maturity |
|------|-------|----------:|
| RFC-0001 | Cognitive Types | 100% |
| RFC-0002 | Effect Ordering | 99% |
| RFC-0003 | Belief Revision | 99% |
| RFC-0004 | Goal Lifecycle | 98% |
| RFC-0005 | Planning Semantics | 95% |
| RFC-0006 | Capability Model | 98% |

### Overall Assessment

RFC-0006 now completes the core semantic foundation for the Red/Cognition cognitive model:

```text
RFC-0001  Cognitive Types
        │
        ▼
RFC-0002  Effect Ordering
        │
        ▼
RFC-0003  Belief Revision
        │
        ▼
RFC-0004  Goal Lifecycle
        │
        ▼
RFC-0005  Planning Semantics
        │
        ▼
RFC-0006  Capability Model
```

With these six RFCs, the project now has a coherent semantic core covering:

- First-class cognitive values
- Deterministic effect execution
- Belief evolution
- Goal management
- Planning semantics
- Capability-based authorization

I would recommend **ratifying RFC-0006 v1.1** as the baseline specification. The remaining suggestions are refinements that can be incorporated in a future v1.2 without affecting the architecture or implementation model.
