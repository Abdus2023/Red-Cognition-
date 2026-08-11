<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #18, sub-message [164], 2026-08-10
  Verbatim source: knowledge-base/sources/message-018-original-part*.md
  Status in corpus: RFC-0035 CSEIM v1.0 (Draft); drafted within review message [164]. No separate formal draft/review/ratification in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

RFC-0034 completes the **verified cognitive software distribution layer**. The next logical RFC should move from **distribution trust** to **execution isolation**.

The natural continuation is:

# RFC-0035 — Cognitive Sandbox and Execution Isolation Model (CSEIM)

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0034 Cognitive Package Registry and Trust Distribution Protocol (CPR-TDP) v1.0 (Draft)  

**Date:** 2026-07-29  

---

# 1. Introduction

This RFC defines the **Cognitive Sandbox and Execution Isolation Model (CSEIM)** for Red/Cognition.

After a cognitive package has been distributed and verified through CPR-TDP (RFC-0034), the runtime must provide a secure execution environment where cognitive programs, agents, and skills operate under controlled boundaries.

CSEIM defines the isolation architecture, sandbox semantics, resource boundaries, effect mediation, capability enforcement, and deterministic execution guarantees required for safe execution of CPCPF artifacts.

The sandbox ensures that untrusted or partially trusted cognitive software cannot bypass:

- Capability restrictions
- Security policies
- Resource quotas
- Memory boundaries
- Event logging
- Replay requirements

---

# 2. Design Principles

CSEIM follows these principles:

## Isolation

Every cognitive execution environment MUST operate inside a defined isolation boundary.

Isolation applies to:

- Memory
- Capabilities
- Effects
- Hardware resources
- Network access
- Persistent storage

---

## Capability Mediation

No cognitive program may directly access system resources.

All access MUST pass through:

- Capability checks (RFC-0006)
- Security policies (RFC-0025)
- Resource quotas (RFC-0024)

---

## Deterministic Execution

Sandbox execution MUST preserve:

- Deterministic scheduling
- Replay compatibility
- Event trace completeness

---

## Fault Containment

A failing cognitive process MUST NOT corrupt:

- Other agents
- Shared memory
- System services
- Global event history

---

## Provider Neutrality

The sandbox MUST support multiple:

- CVM implementations
- Hardware accelerators
- Execution backends
- Cognitive languages

---

# 3. Cognitive Sandbox Model

A sandbox instance is defined as:

```
CognitiveSandbox {
    SandboxID,
    AgentID,
    CVMInstance,
    MemoryNamespace,
    CapabilitySet,
    ResourceQuota,
    PolicyContext,
    EffectGateway,
    TraceContext,
    SecurityLevel
}
```

---

# 4. Isolation Domains

CSEIM defines multiple isolation domains:

## 4.1 Memory Isolation

Each cognitive process MUST have:

- Private working memory
- Controlled episodic access
- Policy-governed semantic memory access
- Audited procedural memory access

Shared memory MUST be accessed through controlled interfaces.

---

## 4.2 Capability Isolation

Capabilities MUST be scoped to:

- Agent identity
- Sandbox identity
- Execution context

Example:

```
CapabilityGrant {
    CapabilityID,
    Subject: SandboxID,
    Scope,
    Expiration,
    ResourceLimit
}
```

---

## 4.3 Effect Isolation

All external effects MUST pass through an Effect Gateway.

Examples:

- Network requests
- File operations
- Hardware actions
- External APIs

Flow:

```
Cognitive Program
       |
       v
Effect Gateway
       |
       v
Capability Check
       |
       v
Policy Evaluation
       |
       v
External Effect
```

---

# 5. Sandbox Lifecycle

A sandbox follows this lifecycle:

```
Create
  |
Verify CPCPF Artifact
  |
Initialize CVM
  |
Attach Capabilities
  |
Allocate Resources
  |
Execute
  |
Checkpoint
  |
Suspend / Resume
  |
Terminate
```

All lifecycle transitions MUST generate events in RFC-0018.

---

# 6. Execution Modes

CSEIM defines three execution modes:

## 6.1 Verified Mode

Used for:

- T4/T5 trusted packages
- Formally verified cognitive programs

Properties:

- Maximum optimization
- Hardware acceleration allowed
- Extended privileges possible

---

## 6.2 Restricted Mode

Used for:

- T2/T3 packages
- External cognitive modules

Properties:

- Limited capabilities
- Strict quotas
- Mandatory tracing

---

## 6.3 Experimental Mode

Used for:

- T0/T1 packages
- Development environments

Properties:

- No production effects
- Complete isolation
- Simulation-only execution

---

# 7. Resource Isolation

The sandbox MUST enforce RFC-0024 quotas:

```
SandboxQuota {
    CPUBudget,
    MemoryLimit,
    StorageLimit,
    NetworkLimit,
    CapabilityUsageLimit,
    EffectLimit
}
```

Quota violations MUST:

1. Generate an exception event.
2. Trigger policy evaluation.
3. Suspend or terminate execution if required.

---

# 8. Deterministic Replay

A sandbox MUST preserve:

- Initial state
- Capability state
- Resource state
- Event position
- CVM state

Replay MUST reconstruct:

```
Original Sandbox State
          +
     Event Log
          +
   Checkpoints
          =
Equivalent Execution
```

---

# 9. Hardware Isolation

Hardware acceleration (RFC-0026) MUST be mediated through sandbox controls.

Requirements:

- Accelerator access requires capability authorization.
- Hardware state MUST be checkpointable.
- Attestation MUST be verified when required.
- Hardware failures MUST be contained.

---

# 10. Multi-Agent Isolation

Multiple agents MAY execute concurrently.

The sandbox MUST prevent:

- Unauthorized memory access
- Capability leakage
- Trace contamination
- Resource starvation

Inter-agent communication MUST use:

- CNP (RFC-0021)
- Capability delegation
- Event propagation

---

# 11. Security Events

The following events MUST be generated:

```
SandboxViolation
CapabilityDenied
QuotaExceeded
UnauthorizedEffectAttempt
IsolationFailure
SandboxTerminated
```

Each event MUST include:

- SandboxID
- AgentID
- TraceID
- Policy decision
- Provenance

---

# 12. Relationship to Other RFCs

CSEIM integrates with:

- RFC-0018 — Cognitive Event Log
- RFC-0019 — Cognitive Operating System
- RFC-0021 — Cognitive Network Protocol
- RFC-0022 — Identity and Trust Framework
- RFC-0024 — Resource Management
- RFC-0025 — Security Policy Language
- RFC-0026 — Hardware Acceleration
- RFC-0033 — CPCPF
- RFC-0034 — CPR-TDP

---

# 13. Open Questions

Future specifications:

- Formal sandbox security proofs
- WASM-based CVM isolation backend
- Trusted execution environment integration
- Zero-copy secure memory sharing
- Distributed sandbox migration
- Confidential cognitive execution

---

**RFC-0035 — Cognitive Sandbox and Execution Isolation Model (CSEIM) v1.0 Draft**

This RFC establishes the execution security layer of Red/Cognition. Combined with CPCPF and CPR-TDP, it creates a complete chain:

```
Cognitive Source
       |
       v
Compiler
       |
       v
CIR
       |
       v
Proof-Carrying Artifact
       |
       v
Trusted Registry
       |
       v
Secure Cognitive Sandbox
       |
       v
Deterministic Execution
```

The next logical RFC after RFC-0035 would be:

**RFC-0036 — Cognitive Build Reproducibility and Supply Chain Protocol (CBR-SCP)**

which would complete the missing link between **source → compiler → verified artifact → registry → execution**.

# Source Record: Conversation Message #18 — Verbatim Transcript (Part 2 of 5: sub-messages [165]–[168])

- **Message index:** 18 (continued) · **Part 1:** `message-018-original-part1.md` · **Cleanup:** as Part 1. Note: sub-message [167] contains RFC-0038 followed by a duplicated RFC-0034 (CPR-TDP) text identical to [163] — preserved as received (duplicate logged).
