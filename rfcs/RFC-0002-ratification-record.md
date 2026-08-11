<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #8, sub-message [76], 2026-08-10
  Verbatim source: knowledge-base/sources/message-008-original-part*.md
  Status in corpus: RFC-0002 Ratification Record: ratified v1.1, Date 2026-07-29; accepts ADR-0007 (Effect Graph Execution Model) and ADR-0008 (Replay Equivalence Principle) — numbering conflicts with msg#5 [60] ADR-0007/0008 recorded in KB traceability.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates specs/ and rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

# RFC-0002 — Effect Ordering Model v1.1

## Final Ratification Review

**Decision:** ✅ **Approved for Ratification**

RFC-0002 v1.1 is internally consistent, aligns with the previously ratified RC-000 through RC-900 specifications and RFC-0001, and is suitable to become the normative specification governing effect semantics in Red/Cognition.

---

# Ratification Record

**Document:** RFC-0002 — Effect Ordering Model  

**Version:** 1.1  

**Status:** Ratified  

**Authority:** Normative RFC  

**Parent:** RFC-0001 Cognitive Type System v1.2 (Ratified)  

**Date:** 2026-07-29

---

## 1. Ratification Declaration

RFC-0002 — Effect Ordering Model v1.1 is hereby ratified as the normative specification governing the creation, ordering, execution, coordination, replay, and lifecycle of `effect!` values within Red/Cognition.

From this point forward:

- All implementations **MUST** conform to the effect ordering model defined herein.
- Every externally observable cognitive action **MUST** be represented by one or more `effect!` values.
- Effect ordering semantics become part of the Cognitive Runtime, Cognitive Virtual Machine (CVM), and Cognitive IR contracts.
- Deterministic replay **MUST** preserve the observable behaviour defined by this specification.

---

## 2. Ratified Effect Model

The following concepts are now normative:

- Effect identity
- Effect lifecycle
- Effect metadata contract
- Effect classification
- Temporal ordering
- Causal ordering
- Dependency graph semantics
- Transactional execution
- Rollback and compensation
- Deterministic replay
- Parallel execution
- Distributed coordination

---

## 3. Ratified Effect Lifecycle

The lifecycle is established as the normative execution state machine:

```text
Created
   ↓
Validated
   ↓
Authorized
   ↓
Scheduled
   ↓
Executing
   ↓
Committed
   ↓
Archived
```

Where supported by the effect class, rollback and compensation introduce controlled transitions without altering the primary lifecycle.

---

## 4. Ratified Effect Dependency Graph

The Effect Dependency Graph is defined as a **Directed Acyclic Graph (DAG)**.

A conforming implementation:

- **MUST** reject cyclic dependencies.
- **MUST** preserve causal relationships.
- **MUST** execute prerequisite effects before dependent effects.
- **MAY** execute independent branches concurrently.

This graph becomes the canonical execution model for Cognitive IR and CVM scheduling.

---

## 5. Ratified Ordering Semantics

Two independent ordering dimensions are now normative:

- **Temporal Order** — chronological execution sequence.
- **Causal Order** — semantic dependency between effects.

An implementation **MUST** preserve causal order even when temporal execution is parallelized.

---

## 6. Ratified Transaction Model

Transactions are established as first-class execution boundaries.

A transaction:

- groups related effects,
- commits atomically with respect to observable external state,
- either completes successfully or resolves through rollback or compensation,
- participates fully in execution traces.

---

## 7. Ratified Replay Contract

Replay semantics are now part of the Red/Cognition execution model.

A conforming implementation **MUST** ensure that:

- execution traces are replayable,
- effect ordering is preserved,
- externally observable behaviour remains equivalent to the original execution,
- implementation-specific scheduling differences do not alter semantic outcomes.

---

## 8. Accepted Architecture Decisions

### ADR-0007 — Effect Graph Execution Model

**Status:** Accepted

**Decision:**

Effect execution is defined by a Directed Acyclic Graph rather than a linear instruction stream.

**Consequences:**

- enables safe parallelism,
- simplifies dependency analysis,
- supports deterministic replay,
- provides a foundation for distributed scheduling.

---

### ADR-0008 — Replay Equivalence Principle

**Status:** Accepted

**Decision:**

Replay correctness is defined by **observable behavioural equivalence**, not by reproducing identical internal scheduling.

**Consequences:**

- allows implementation flexibility,
- preserves deterministic semantics,
- supports heterogeneous runtime implementations.

---

## 9. Specification Impact

RFC-0002 extends the normative behaviour of:

- **RC-300** — Compiler Specification (effect analysis and lowering)
- **RC-400** — Runtime Specification (effect scheduling)
- **RC-500** — Cognitive Runtime (effect execution)
- **RC-700** — Cognitive Virtual Machine (instruction semantics)
- **RC-800** — Cognitive Operating System (distributed coordination)

Implementations of these specifications **SHOULD** be updated to reference RFC-0002 where effect semantics are defined.

---

## 10. Future RFC Dependencies

RFC-0002 establishes the foundation for:

- **RFC-0003 — Belief Revision System**
- **RFC-0004 — Capability System**
- **RFC-0005 — Cognitive IR Specification**
- **RFC-0006 — Transaction and Checkpoint Model**
- **RFC-0007 — Scheduler Semantics**
- **RFC-0008 — Distributed Coordination Protocol**

---

## Final Assessment

RFC-0002 completes the second foundational RFC of the Red/Cognition architecture.

Together:

- **RFC-0001** defines **what cognitive values are**.
- **RFC-0002** defines **how cognitive effects are ordered, coordinated, and replayed**.

This establishes a coherent semantic basis for deterministic cognitive execution across the compiler, runtime, Cognitive Virtual Machine, and Cognitive Operating System.

**Decision:** **RFC-0002 — Effect Ordering Model v1.1 is hereby ratified as a normative specification of the Red/Cognition project.**

# Source Record: Conversation Message #8 — Verbatim Transcript (Part 5 of 5: sub-messages [77]–[80])

- **Message index:** 8 (continued) · **Part 4:** `message-008-original-part4.md` · **Cleanup:** as Part 1.
