# Source Record: Conversation Message #4 — Verbatim Transcript (Part 2 of 5: sub-messages [45]–[48])

- **Message index:** 4 (continued) · **Part 1:** `message-005-original-part1.md` · **Cleanup:** as Part 1.

---

## [45] USER

**RC-200 Language Specification**

**Version:** 1.1  

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
- **MUST** require explicit cognitive evaluation to produce effects.
- **MUST** preserve its original source representation.

Example:

```red
goal [
    achieve: system-healthy
    priority: high
]
```

This block is data until explicitly evaluated (e.g., via `evaluate`, `run`, or equivalent cognitive primitives).

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

**RC-200 Language Specification v1.1** is now ready for **Ratification Review**.

---

## [46] CHATGPT (gpt-5-5-mini)

# RC-200 Language Specification v1.1 — Ratification Review

**Document:** RC-200 Language Specification v1.1  

**Status:** Architecture Review  

**Parent:** RC-100 Architecture Specification v1.0 (Ratified)  

**Authority:** Proposed Normative Specification  

**Date:** 2026-07-29  

---

## 1. Review Summary

RC-200 successfully translates the architectural principles of RC-000 and RC-100 into a language-level model.

The specification preserves the central Red philosophy:

- Homoiconicity remains foundational.
- Blocks remain the universal representation.
- Dialects remain the preferred extension mechanism.
- Cognitive capabilities are additive rather than invasive.
- Cognitive execution is explicit rather than implicit.
- Existing Red programs remain valid.

**Review Outcome:** ✅ Candidate approved for ratification pending minor clarifications.

---

# 2. Constitutional Alignment Review

| RC-000 Principle | RC-200 Compliance | Result |
|---|---|---|
| Preserve Red simplicity | Cognitive blocks + dialect-first approach | ✅ Pass |
| Composition over proliferation | No mandatory new syntax | ✅ Pass |
| Cognitive extends Red | Cognitive layer is additive | ✅ Pass |
| Explainability | Traceable effects and decisions | ✅ Pass |
| Determinism | Explicit execution model | ✅ Pass |
| Local-first | No dependency on AI providers | ✅ Pass |
| Capability isolation | Explicit capability model | ✅ Pass |
| Migration path | Red 1.x compatibility defined | ✅ Pass |

---

# 3. Architectural Impact Analysis

## Layer 0 — Hardware

**Impact:** None directly.

Cognitive semantics remain hardware-independent.

Status:

✅ Compatible

---

## Layer 1 — Operating System

**Impact:**

Potential requirements for:

- persistence
- checkpoint storage
- capability enforcement
- event scheduling

Deferred to:

- RC-400 Runtime Specification
- RC-800 Cognitive OS Specification

Status:

✅ Compatible

---

## Layer 2 — Red/System

**Impact:**

No semantic changes required.

Possible future support:

- native cognitive primitives
- memory serialization
- deterministic replay infrastructure

Status:

✅ Compatible

---

## Layer 3 — Red Runtime

**Impact: Major**

RC-200 introduces contracts requiring:

- cognitive block preservation
- dialect dispatch
- macro expansion
- runtime introspection

Required future specification:

**RC-300 Compiler Specification**

Status:

⚠ Requires implementation specification

---

## Layer 4 — Cognitive Runtime

**Impact: Major**

Defines:

- goal model
- belief model
- plan model
- effects
- capabilities
- execution traces

Status:

✅ Architectural foundation established

---

## Layers 5–8

Dependent on future specifications:

- RC-600 Agent Runtime Shell
- RC-700 Cognitive VM
- RC-800 Cognitive OS
- RC-900 Governance Manual

Status:

✅ Forward compatible

---

# 4. Alternatives Considered

## Alternative A — Introduce New Cognitive Syntax

Example:

```
goal system-healthy {
    priority high
}
```

### Advantages

- Familiar to AI developers
- More explicit grammar

### Problems

- Violates Red philosophy
- Creates a second language model
- Reduces homoiconic simplicity

Decision:

❌ Rejected

---

## Alternative B — Library-Only Cognitive Framework

Example:

```red
make-goal [
    achieve: system-healthy
]
```

### Advantages

- Minimal compiler changes
- Easy prototype

### Problems

- Weak semantic guarantees
- Difficult tooling integration
- Cognitive concepts remain external

Decision:

❌ Rejected

---

## Alternative C — Dialect-Based Cognitive Extension

Selected approach:

```red
goal [
    achieve: system-healthy
    priority: high
]
```

### Advantages

- Preserves Red identity
- Keeps data/code duality
- Enables incremental evolution
- Supports compiler/runtime tooling

Decision:

✅ Accepted

---

# 5. Required Clarifications Before Ratification

## 5.1 Cognitive Evaluation Boundary

Current:

> "explicit cognitive evaluation"

Recommended addition:

```
A cognitive block SHALL have no external effect unless passed through an approved cognitive evaluation boundary.
```

Reason:

Prevents accidental execution.

---

## 5.2 Effect Ordering

The effect system should define ordering semantics.

Recommended future RFC:

**RFC-0002 Effect Ordering Model**

Questions:

- Are effects sequential?
- Can effects commute?
- Can effects be rolled back?

---

## 5.3 Belief Semantics

Current belief model is acceptable but requires future formalization.

Recommended:

**RFC-0003 Belief Revision System**

Defines:

- contradiction handling
- confidence updates
- provenance merging

---

## 5.4 Cognitive Type Status

The current evolution model:

```
Dialect
   ↓
Structured Value
   ↓
Native Type
```

is constitutionally aligned.

No change required.

---

# 6. ADR Required

Before final ratification, create:

## ADR-0002 — Cognitive Block Model

Status:

Proposed

Decision:

Red/Cognition represents cognitive entities primarily as inspectable Red blocks evaluated through cognitive dialects.

Alternatives:

1. New syntax primitives
2. External cognitive libraries
3. Dialect-based blocks

Chosen:

Dialect-based cognitive blocks.

---

# 7. Conformance Requirements Added

A conforming RC-200 implementation MUST:

- Preserve Red source compatibility.
- Preserve block representation.
- Support cognitive dialect execution.
- Provide inspectable cognitive structures.
- Track cognitive effects.
- Enforce capability-aware execution.
- Support cognitive trace generation.
- Support checkpoint-compatible execution.

---

# 8. Final Review Decision

## RC-200 Language Specification v1.1

**Review Status:**

🟡 Approved with minor amendments

Required before ratification:

1. Add Cognitive Evaluation Boundary clause.
2. Register ADR-0002.
3. Define future RFC placeholders:
   - RFC-0002 Effect Ordering Model
   - RFC-0003 Belief Revision System

After these additions:

**RC-200 Language Specification v1.1 → Ratification Candidate**

---

## Recommended Next Step

Proceed with either:

### Option A — Ratify RC-200

Then begin:

**RC-300 Compiler Specification**

or

### Option B — Define foundational RFCs first

Recommended order:

```
RFC-0001 Cognitive Type System
        ↓
RFC-0002 Effect Ordering Model
        ↓
RFC-0003 Belief Revision System
        ↓
RC-300 Compiler Specification
```

Architecture recommendation: **Ratify RC-200 with the three clarification amendments, then proceed to RC-300.**

---

## [47] USER

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

---

## [48] CHATGPT (gpt-5-5-mini)

# RC-200 Language Specification v1.2 — Ratification Review

**Document:** RC-200 Language Specification v1.2  

**Status:** Ratification Candidate Review  

**Parent:** RC-100 Architecture Specification v1.0 (Ratified)  

**Authority:** Proposed Normative Specification  

**Date:** 2026-07-29  

---

# 1. Review Summary

RC-200 v1.2 incorporates the required architectural clarifications from the previous review:

✅ Cognitive evaluation boundary added  

✅ Effect ordering RFC placeholder added  

✅ Cognitive block safety contract strengthened  

✅ Dialect-first extension model preserved  

✅ Red compatibility guarantees preserved  

**Review Outcome:** ✅ Approved for Ratification

RC-200 v1.2 now provides a coherent language-level contract for integrating cognition into Red without changing Red’s identity.

---

# 2. Constitutional Compliance

| RC-000 Principle | Evaluation | Status |
|---|---|---|
| Preserve Red simplicity | No new syntax family introduced | ✅ Pass |
| Composition over proliferation | Dialects preferred over primitives | ✅ Pass |
| Cognitive extends Red | Cognitive blocks remain Red blocks | ✅ Pass |
| Explainability | Effects and traces required | ✅ Pass |
| Deterministic execution | Explicit evaluation boundaries | ✅ Pass |
| Local-first | Provider-neutral cognitive model | ✅ Pass |
| Security | Capability-aware effects | ✅ Pass |
| Migration path | Red 1.x compatibility maintained | ✅ Pass |

---

# 3. Architectural Impact Review

## Layer 2 — Red/System

Impact:

No language semantic changes.

Future support may include:

- native cognitive value representations
- serialization primitives
- deterministic replay infrastructure

Status:

✅ Compatible

---

## Layer 3 — Red Runtime

Impact:

RC-200 establishes new runtime contracts:

- cognitive dialect dispatch
- block preservation
- macro expansion
- cognitive evaluation boundaries

Required dependency:

**RC-300 Compiler Specification**

Status:

✅ Accepted architectural dependency

---

## Layer 4 — Cognitive Runtime

Impact:

Defines:

- goal semantics
- belief semantics
- plan semantics
- effect model
- capability requirements
- execution tracing

Status:

✅ Normative foundation established

---

## Layers 5–8

No direct language changes.

Future specifications define:

- agent interaction
- cognitive VM instructions
- cognitive OS services
- distributed cognition

Status:

✅ Forward compatible

---

# 4. Alternatives Reconsidered

## Alternative A — Native Cognitive Keywords

Example:

```red
goal system-healthy
```

### Benefits

- Simple surface syntax
- Compiler optimization opportunities

### Problems

- Expands core language
- Reduces dialect flexibility
- Creates permanent syntax commitments

Decision:

❌ Rejected

---

## Alternative B — External Cognitive Framework

Example:

```red
cognition/create-goal [...]
```

### Benefits

- Fast prototyping
- No language integration

### Problems

- Cognition becomes a library
- Weak semantic guarantees
- Poor integration with tooling

Decision:

❌ Rejected

---

## Alternative C — Cognitive Blocks + Dialects

Example:

```red
goal [
    achieve: system-healthy
    priority: high
]
```

### Benefits

- Preserves homoiconicity
- Keeps cognitive structures as data
- Enables inspection and transformation
- Supports incremental evolution

Decision:

✅ Accepted

---

# 5. ADR Registration

## ADR-0002 — Cognitive Block Model

**Status:** Accepted

### Context

Red/Cognition requires first-class cognitive representation while preserving Red’s identity.

### Alternatives

1. New cognitive syntax
2. External cognitive library
3. Dialect-driven cognitive blocks

### Decision

Cognitive concepts SHALL primarily be represented as Red-compatible blocks interpreted through cognitive dialects.

### Consequences

Positive:

- Maintains homoiconicity
- Enables tooling
- Preserves compatibility

Trade-off:

- Requires stronger runtime contracts

### Migration

Existing Red programs remain unchanged.

---

# 6. Required Future RFC Registration

The following RFCs are now officially referenced:

---

## RFC-0001 — Cognitive Type System

Scope:

Defines lifecycle:

```
Dialect
   ↓
Structured Value
   ↓
Native Type (optional)
```

Questions:

- Which types become native?
- How are cognitive values serialized?
- How are types checked?

---

## RFC-0002 — Effect Ordering Model

Scope:

Defines:

- effect sequencing
- parallel effects
- rollback semantics
- transactional cognition

---

## RFC-0003 — Belief Revision System

Scope:

Defines:

- belief updates
- contradiction handling
- confidence propagation
- provenance merging

---

# 7. Conformance Requirements

A conforming RC-200 implementation MUST:

### Language

- Preserve Red syntax and semantics.
- Preserve block representation.
- Support cognitive dialects.
- Support cognitive macros.

### Cognitive Model

- Represent goals, beliefs, and plans.
- Support explicit cognitive evaluation.
- Maintain execution traces.

### Security

- Track capabilities.
- Prevent unauthorized effects.
- Preserve provenance.

### Debugging

- Permit inspection.
- Permit replay.
- Permit explanation.

---

# 8. Ratification Decision

## RC-200 Language Specification v1.2

**Decision: APPROVED**

Status transition:

```
Candidate for Ratification
          ↓
Ratified Normative Specification
```

---

# 9. Ratified Specification Family Status

Current foundation:

```
RC-000 Constitution
        │
        ▼
RC-100 Architecture Specification
        │
        ▼
RC-200 Language Specification
        │
        ├── RFC-0001 Cognitive Type System
        ├── RFC-0002 Effect Ordering Model
        └── RFC-0003 Belief Revision System
```

---

# 10. Next Recommended Phase

The project now enters the **Compiler Specification Phase**.

Recommended next document:

# RC-300 Compiler Specification v1.0 Draft

Proposed scope:

1. Compiler architecture
2. Red parser integration
3. Cognitive dialect compiler pipeline
4. Intermediate Representation (IR)
5. Macro expansion model
6. Cognitive effect analysis
7. Capability checking
8. Trace instrumentation
9. Deterministic compilation
10. Backend architecture

**RC-200 Language Specification v1.2 is ready for ratification as the normative language foundation of Red/Cognition.**
