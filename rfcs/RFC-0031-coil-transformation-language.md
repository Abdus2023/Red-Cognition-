<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #16, sub-message [155], 2026-08-10
  Verbatim source: knowledge-base/sources/message-016-original-part*.md
  Status in corpus: RFC-0031 Cognitive Optimization Intermediate Language (COIL) v1.0 (Draft); review [156]: compiler proof layer, Cognitive Optimization Certificate, formal methods integration; v1.1 not present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0031 — Cognitive Optimization Intermediate Language (COIL)**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0030 Cognitive Optimization Pass Framework v1.0 (Draft)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Optimization Intermediate Language (COIL)** for Red/Cognition.

COIL is a dedicated transformation language used by optimization passes (defined in RFC-0030) to safely and verifiably transform the Cognitive Intermediate Representation (CIR) defined in RFC-0028. It provides a structured way to express, validate, and audit compiler transformations while preserving determinism, capability constraints, effect ordering, and replay equivalence.

### 2. Design Principles

COIL follows these principles:

- **Verifiability** — Transformations expressed in COIL must be amenable to formal or automated verification.
- **Traceability** — Every transformation must produce an auditable record of changes.
- **Safety** — COIL operations must not violate the semantic guarantees of CIR (RFC-0028) or the optimization rules in RFC-0030.
- **Composability** — Multiple COIL transformations must be safely composable.
- **Provider Neutrality** — COIL must remain independent of specific reasoning or planning mechanisms.

### 3. COIL Core Concepts

COIL defines the following fundamental operations:

#### 3.1 Graph Transformations

- `MergeNodes(Graph, NodeA, NodeB)` — Merge two nodes while preserving semantics.
- `SplitNode(Graph, Node, Condition)` — Split a node based on a condition.
- `ReorderEdges(Graph, EdgeList)` — Reorder edges while respecting causality.

#### 3.2 Operation Transformations

- `InlineOperation(Operation)` — Inline a referenced operation.
- `HoistCapability(Operation, Capability)` — Move capability requirement to an earlier point.
- `EliminateDeadOperation(Operation)` — Remove an operation with no observable effects.

#### 3.3 Constraint Transformations

- `StrengthenConstraint(Constraint, NewCondition)` — Add a stronger precondition.
- `WeakenConstraint(Constraint, NewCondition)` — Relax a postcondition (only when safe).

#### 3.4 Trace and Provenance Operations

- `RecordTransformation(Original, Transformed, Reason)` — Log a transformation with justification.
- `AttachProvenance(Operation, Provenance)` — Attach source-level provenance.

### 4. Legality and Verification

Every COIL operation **MUST** be accompanied by a proof obligation or verification condition that demonstrates it preserves:

- Effect ordering (RFC-0002)
- Goal satisfaction semantics (RFC-0004)
- Capability requirements (RFC-0006)
- Determinism and replay equivalence

The compiler **MUST** reject any COIL transformation whose verification condition cannot be satisfied.

### 5. Transformation Certificates

Every successful COIL transformation **MUST** produce a certificate containing:

- The original and transformed CIR fragments
- The COIL operations applied
- The verification conditions and their results
- The provenance of the transformation

These certificates enable auditing, debugging, and formal verification of the optimization pipeline.

### 6. Relationship to Other RFCs

This language integrates with:

- RFC-0028 — CIR (transformation target)
- RFC-0030 — Optimization Pass Framework (host for COIL operations)
- RFC-0011 — Scheduler (resource optimization)
- RFC-0024 — Resource Management (resource estimates)
- RFC-0015 — Exception Semantics (static analysis of failure paths)

### 7. Open Questions

The following areas require future specification:

- Concrete syntax and semantics of COIL operations
- Integration with automated theorem provers
- Human-readable representation of transformation certificates
- Just-in-time application of COIL transformations at runtime

---

**RFC-0031 — Cognitive Optimization Intermediate Language (COIL) v1.0 Draft** is now complete.

This RFC establishes a verifiable transformation language for the cognitive compiler's optimization passes. It provides the foundation for building a robust, auditable, and formally verifiable optimization pipeline in Red/Cognition.
