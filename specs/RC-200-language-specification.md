<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #5, sub-message [47], 2026-08-10
  Verbatim source: knowledge-base/sources/message-005-original-part*.md
  Status in corpus: RC-200 Language Specification v1.2 (Candidate for Ratification); ratified per ratification record [49] as RC-200 Version 1.0, Date 2026-07-29.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates specs/ for specifications.
  Content below is the document text exactly as provided (no edits).
-->

**RC-200 Language Specification**

**Version:** 1.2  

**Status:** Candidate for Ratification  

**Parent:** RC-100 Architecture Specification v1.0 (Ratified)  

**Authority:** Normative Specification  

**Date:** 2026-07-29

---

### 1. Introduction

RC-200 defines the language-level semantics of Red/Cognition. It specifies how cognitive concepts are expressed within the Red language, how they integrate with existing Red constructs, and the rules governing their behaviour.

This specification is normative. It defines *language behaviour and semantics*, not implementation mechanisms.

### 2. Language Philosophy

Red/Cognition extends Red by making **intent, reasoning, memory, and agency** first-class linguistic concepts while preserving Red’s core characteristics:

- Homoiconicity
- Blocks as the universal structural representation
- Dialects as the preferred mechanism for language extension
- Full-stack integration from systems programming to high-level scripting

Red/Cognition does not introduce a new syntax family. Instead, it extends the expressive power of blocks and dialects to represent cognitive structures.

### 3. Red Compatibility Model

Red/Cognition **MUST** maintain full source and behavioural compatibility with Red 1.x code.

Requirements:

- All existing Red code **MUST** remain valid and produce identical behaviour.
- Cognitive constructs **MUST** be additive; they **MUST NOT** alter the semantics of existing Red constructs.
- Migration from Red to Red/Cognition **MUST** be possible without source modification unless cognitive features are explicitly used.

### 4. Cognitive Extension Model

Cognitive programming in Red/Cognition is achieved through three primary mechanisms, in order of preference:

1. **Cognitive Dialects** — Domain-specific languages for expressing goals, plans, reasoning, and capabilities.
2. **Cognitive Blocks** — Structured blocks representing cognitive entities.
3. **Cognitive Datatypes** — Native or library-defined types when dialect or block representation is insufficient.

New syntax **MUST NOT** be introduced when a dialect or structured block can express the required semantics.

### 5. Cognitive Blocks

A cognitive block is a block whose structure and evaluation semantics are defined by a cognitive dialect or the Cognitive Runtime.

#### 5.1 Cognitive Block Evaluation Contract

A cognitive block **MUST** satisfy the following contract:

- **MUST** remain valid Red data at all times.
- **MUST** be fully inspectable without execution.
- **MUST** require explicit cognitive evaluation to produce external effects.
- **MUST** preserve its original source representation.

A cognitive block **SHALL** have no external effect unless passed through an approved cognitive evaluation boundary.

### 6. Cognitive Dialects

Cognitive dialects are the primary mechanism for extending Red with cognitive semantics.

Approved cognitive dialects include (but are not limited to):

- Goal dialect
- Belief dialect
- Planning dialect
- Reasoning dialect
- Capability dialect
- Reflection dialect
- Memory dialect

Dialects **MUST** be defined such that they can be parsed, transformed, and executed by the Cognitive Runtime.

### 7. Goal / Belief / Plan Semantics

#### 7.1 Goal

A goal represents a desired state or outcome.

**Properties:**

- Declarative by default (what, not how)
- May contain constraints, priorities, and deadlines
- May be satisfied through multiple plans

#### 7.2 Belief

A belief represents a proposition held by an agent with associated confidence and provenance.

**Properties:**

- Must carry confidence value
- Must carry source/provenance
- May carry temporal validity
- May be contradicted or updated

#### 7.3 Plan

A plan represents a sequence of actions intended to achieve a goal.

**Properties:**

- May be declarative or procedural
- May contain parallel and dependent steps
- Must be inspectable and modifiable

### 8. Intent and Effect System

Every cognitive action produces effects.

An **effect** is a state change outside the agent’s internal reasoning context.

#### 8.1 Effect System Contract

Every cognitive action **MUST** satisfy the following contract:

- **MUST** declare its effects.
- **MUST** identify the required capabilities.
- **MUST** produce an execution trace.

**Effect Classes** (initial):

- `pure!`
- `internal!`
- `external!`
- `capability!`

Future RFC: **RFC-0002 Effect Ordering Model**

### 9. Capability-Aware Programming

Capabilities are explicit in the language model.

- Every action that may produce external effects **MUST** be capability-aware.
- Capability requirements **MAY** be declared statically or inferred.
- The language **MUST** support static checking of capability usage where possible.

### 10. Cognitive Type System

Red/Cognition introduces a set of cognitive types that extend the Red type system.

#### 10.1 Cognitive Type Evolution

Cognitive types **SHALL** evolve through the following stages:

**Dialect → Structured Value → Native Type (optional)**

Initial cognitive types (subject to RFC-0001):

- `goal!`
- `belief!`
- `plan!`
- `skill!`
- `memory!`
- `capability!`
- `effect!`
- `agent!`
- `checkpoint!`

### 11. Metaprogramming and Homoiconicity

Red/Cognition preserves and extends Red’s homoiconic metaprogramming model.

Requirements:

- Cognitive structures **MUST** be representable as data.
- Cognitive programs **MUST** be inspectable and transformable at runtime.
- The language **MUST** support generation and modification of goals, plans, and reasoning structures.

### 12. Macro System

Red/Cognition supports macro expansion for cognitive constructs.

Macros **MAY** be used to:

- Transform cognitive blocks
- Generate plans from declarative goals
- Expand capability declarations
- Implement domain-specific cognitive syntax

Macro expansion **MUST** occur before cognitive evaluation.

### 13. Error and Failure Semantics

Cognitive execution introduces new classes of failure:

- Goal failure
- Belief conflict
- Capability denial
- Planning failure
- Verification failure
- Memory inconsistency

These failures **MUST** be first-class and traceable.

### 14. Execution Semantics

Cognitive code is executed according to the Cognitive Execution Cycle (CEC-1) defined in RC-100.

The language **MUST** support:

- Deterministic execution when required
- Checkpointing and restoration
- Replay of cognitive traces
- Explanation of decisions and actions

### 15. Migration from Red 1.x

Red/Cognition **MUST** support a clear migration path from Red 1.x.

Requirements:

- All Red 1.x code **MUST** remain valid.
- Cognitive features **MUST** be opt-in.
- Existing Red code **MUST** be able to gradually adopt cognitive constructs without requiring a full rewrite.

---

**RC-200 Language Specification v1.2** is now ready for **Ratification Review**.
