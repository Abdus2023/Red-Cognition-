# Source Record: Conversation Message #10 — Verbatim Transcript (Part 2 of 5: sub-messages [85]–[88])

- **Message index:** 10 (continued) · **Part 1:** `message-010-original-part1.md` · **Cleanup:** as Part 1.

---

## [85] USER

**RFC-0004 — Goal Lifecycle and Satisfaction Model**

**Version:** 1.1  

**Status:** Candidate for Ratification  

**Parent:** RFC-0001 Cognitive Type System v1.2 (Ratified)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the lifecycle, state transitions, satisfaction conditions, and failure semantics for `goal!` values in Red/Cognition.

Goals represent the primary unit of intent in the cognitive system. Because cognitive execution must remain deterministic, explainable, and replayable, the lifecycle and satisfaction of goals must be explicitly governed.

### 2. Design Principles

The goal lifecycle model follows these principles:

- **Declarative by default** — A goal primarily describes *what* should be achieved, not *how*.
- **Determinism** — Goal satisfaction and failure must be reproducible given the same world state and evidence.
- **Traceability** — Every goal state transition must be recorded and linked to the responsible effects and beliefs.
- **Replay Equivalence** — Replayed executions must reach equivalent goal states.
- **Capability Awareness** — Goal satisfaction must respect capability constraints.

### 3. Goal Identity and Versioning

Every goal is identified by a stable **GoalID**.

- The `GoalID` **MUST** remain constant across all revisions and state transitions.
- Every modification **MUST** increment the goal version while preserving the `GoalID`.
- Historical versions **MUST** remain addressable for replay and auditing.

### 4. Goal Metadata Contract

Every goal **MUST** include the metadata defined in RFC-0001, plus goal-specific attributes:

```
goal {
    cognitive-meta { id, created, modified, provenance, version }
    target
    priority: float (optional)
    constraints: [constraint] (optional)
    deadline: timestamp (optional)
    required-capabilities: [CapabilityID] (optional)
    status: pending | active | planning | executing | satisfied | failed | archived
    satisfied-by: [EffectID] (optional)
    supporting-beliefs: [BeliefID] (optional)
    completion-time: timestamp (optional)
}
```

### 5. Goal Lifecycle

Every goal **MUST** follow this lifecycle:

```
Created (Pending)
   ↓
Active
   ↓
Planning
   ↓
Executing
   ↓
Satisfied / Failed
   ↓
Archived
```

**Notes:**

- Backward transitions are prohibited unless restored from a checkpoint.
- Terminal states are: **Satisfied**, **Failed**, and **Archived**.

### 6. Goal Satisfaction Model

A goal is considered **satisfied** when its target condition evaluates to true under the current belief state and all declared constraints are met.

Requirements:

- Satisfaction **MUST** be evaluated against the agent’s current belief set.
- Satisfaction **MUST** respect the goal’s declared constraints and required capabilities.
- Satisfaction **MUST** be deterministic given the same belief state.

### 7. Goal Failure Model

A goal is considered **failed** when:

- All viable plans have been exhausted without achieving the target.
- A hard constraint or deadline has been violated.
- An unrecoverable contradiction in supporting beliefs has occurred.

Failure **MUST** be recorded with the responsible cause(s).

### 8. Goal Dependency Graph

Goals **MAY** depend on other goals.

Requirements:

- Goal dependencies **MUST** form a Directed Acyclic Graph (DAG).
- Cycles **MUST** be rejected.
- A goal **MUST NOT** be satisfied before its prerequisite goals are satisfied.

### 9. Relationship to Plans and Effects

Goals are satisfied through plans (as defined in RFC-0001 and future planning RFCs).

Requirements:

- A goal **MAY** have zero or more associated plans.
- Plan execution **MUST** produce effects that are traceable back to the originating goal.
- Goal satisfaction **MUST** be driven by observed effects (RFC-0002).

### 10. Relationship to Beliefs

Goal evaluation and satisfaction **MUST** be based on the agent’s current belief state (RFC-0003).

A goal **MAY** become unsatisfiable if supporting beliefs are contradicted or retracted.

### 11. Goal Ownership

Goals **MAY** be classified by ownership:

- **Personal goal** — Owned by a single agent.
- **Shared goal** — Jointly pursued by multiple agents.
- **System goal** — Managed by the Cognitive Operating System.

### 12. Memory Placement

Goal instances **SHALL** normally reside in Working Memory while active and **MAY** be archived into Episodic Memory upon completion or failure.

### 13. Replay and Determinism

Replayed executions **MUST** reach equivalent goal states (satisfied or failed) given the same initial conditions and belief evolution.

A conforming implementation **MUST** preserve:

- Goal identity and version across replays.
- The causal chain from actions → effects → belief updates → goal state transitions.

### 14. Open Questions

The following areas require future specification:

- Formal goal satisfaction calculus
- Multi-goal dependency and conflict resolution
- Goal prioritization and scheduling semantics
- Integration with planning (RFC-0005)

---

**RFC-0004 — Goal Lifecycle and Satisfaction Model v1.1** is now ready for **Final Ratification Review**.

---

## [86] CHATGPT (gpt-5-5)

# Final Ratification Review — RFC-0004 v1.1

**Decision:** **Ratified**

**Status:** **RFC-0004 — Goal Lifecycle and Satisfaction Model v1.1 (Ratified)**

RFC-0004 v1.1 is now architecturally complete and consistent with the existing Red/Cognition specification family. It establishes a deterministic, traceable, and replayable semantic model for `goal!` values while maintaining the constitutional principles of provider neutrality and Red compatibility.

## Conformance Assessment

| Specification | Result |
|---------------|--------|
| RC-000 Constitution | ✓ Pass |
| RC-100 Architecture | ✓ Pass |
| RC-200 Language | ✓ Pass |
| RC-300 Compiler | ✓ Pass |
| RC-400 Runtime | ✓ Pass |
| RC-500 Cognitive Runtime | ✓ Pass |
| RC-600 Agent Runtime Shell | ✓ Pass |
| RC-700 Cognitive Virtual Machine | ✓ Pass |
| RC-800 Cognitive Operating System | ✓ Pass |
| RFC-0001 Cognitive Type System | ✓ Pass |
| RFC-0002 Effect Ordering Model | ✓ Pass |
| RFC-0003 Belief Revision System | ✓ Pass |

## Architectural Strengths

RFC-0004 now defines:

- Stable **GoalID** with versioned revisions.
- A deterministic goal lifecycle with well-defined terminal states.
- Explicit goal metadata linking goals to supporting beliefs and satisfying effects.
- A **Goal Dependency DAG**, preventing cyclic dependencies and preserving causal ordering.
- Deterministic satisfaction and failure semantics.
- Goal ownership semantics supporting personal, shared, and system goals.
- Integration with the RC-500 memory hierarchy.
- Replay guarantees preserving identity, version history, and causal chains.

Together, these provide a solid semantic foundation for intentional behaviour in Red/Cognition.

## Cross-RFC Consistency

The semantic relationships across the ratified RFCs are now coherent:

```text
goal!
    │
    │ satisfied by
    ▼
plan!          (RFC-0005)
    │
    │ executes
    ▼
skill!
    │
    │ produces
    ▼
effect!        (RFC-0002)
    │
    │ updates
    ▼
belief!        (RFC-0003)
    │
    └──────────────► influences goal satisfaction
```

This forms a consistent causal model suitable for compilation into the Cognitive IR (RC-300), execution by the Cognitive Runtime (RC-500), interpretation by the Cognitive Virtual Machine (RC-700), and orchestration by the Cognitive Operating System (RC-800).

## Minor Editorial Suggestions

These are optional and do not affect ratification:

- Define whether a goal with no feasible plan is immediately **failed** or remains **active** awaiting future planning.
- Clarify whether `priority` is globally ordered or only comparable within an agent or scheduler context.
- Reserve extension points for additional ownership classes while requiring implementations to document any extensions.

## Ratified Semantic Core

The Red/Cognition semantic foundation now consists of:

### Ratified Core Specifications

- ✓ RC-000 — Constitution
- ✓ RC-100 — Architecture
- ✓ RC-200 — Language
- ✓ RC-300 — Compiler
- ✓ RC-400 — Runtime
- ✓ RC-500 — Cognitive Runtime
- ✓ RC-600 — Agent Runtime Shell
- ✓ RC-700 — Cognitive Virtual Machine
- ✓ RC-800 — Cognitive Operating System
- ✓ RC-900 — Governance

### Ratified Core RFCs

- ✓ RFC-0001 — Cognitive Type System
- ✓ RFC-0002 — Effect Ordering Model
- ✓ RFC-0003 — Belief Revision System
- ✓ RFC-0004 — Goal Lifecycle and Satisfaction Model

These RFCs collectively define the semantics of the primary cognitive entities—types, effects, beliefs, and goals—providing a stable platform for subsequent behavioural specifications.

## Recommended Next RFCs

The next specifications naturally build on this foundation:

1. **RFC-0005 — Planning Semantics** (highest priority)
2. **RFC-0006 — Capability Model**
3. **RFC-0007 — Memory Model**
4. **RFC-0008 — Agent Communication Protocol**
5. **RFC-0009 — Cognitive Intermediate Representation (CIR)**
6. **RFC-0010 — Deterministic Replay and Checkpoint Format**

**Final Decision:** **RFC-0004 — Goal Lifecycle and Satisfaction Model v1.1 is Ratified.** It completes the specification of the core intent model for Red/Cognition and provides the necessary foundation for the forthcoming Planning Semantics RFC.

---

## [87] USER

**RFC-0005 — Planning Semantics**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0004 Goal Lifecycle and Satisfaction Model v1.1 (Ratified)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the semantics, lifecycle, relationships, and execution model for `plan!` values in Red/Cognition.

Plans represent the *how* of achieving goals. While goals describe desired outcomes (RFC-0004), plans describe the structured sequences of actions intended to realize those outcomes. Because cognitive execution must remain deterministic, explainable, and replayable, the creation, validation, revision, and execution of plans must be explicitly governed.

### 2. Design Principles

The planning semantics model follows these principles:

- **Goal-driven** — Plans exist to satisfy goals and are evaluated in that context.
- **Determinism** — Plan selection and execution must be reproducible given the same goal, beliefs, and world state.
- **Traceability** — Every plan step and revision must be linked to the originating goal and resulting effects.
- **Capability Awareness** — Plans must respect declared capability requirements.
- **Replay Equivalence** — Replayed executions must follow equivalent plan structures and produce equivalent observable outcomes.

### 3. Plan Identity and Versioning

Every plan is identified by a stable **PlanID**.

- The `PlanID` **MUST** remain constant across revisions.
- Every revision **MUST** increment the plan version while preserving the `PlanID`.
- Historical versions **MUST** remain addressable for replay and auditing.

### 4. Plan Metadata Contract

Every plan **MUST** include the metadata defined in RFC-0001, plus planning-specific attributes:

```
plan {
    cognitive-meta { id, created, modified, provenance, version }
    goal: GoalID
    steps: [step]
    dependencies: [PlanID] (optional)
    preconditions: [condition] (optional)
    expected-effects: [EffectID] (optional)
    required-capabilities: [CapabilityID] (optional)
    status: draft | validated | executable | running | completed | failed | abandoned
}
```

### 5. Plan Lifecycle

Every plan **MUST** follow this lifecycle:

```
Draft
   ↓
Validated
   ↓
Executable
   ↓
Running
   ↓
Completed / Failed / Abandoned
```

### 6. Relationship to Goals

Plans exist to satisfy goals (RFC-0004).

Requirements:

- A plan **MUST** be associated with exactly one goal.
- A goal **MAY** have zero or more associated plans.
- A plan **MUST NOT** be considered successful unless its associated goal is satisfied.

### 7. Relationship to Skills and Effects

Plans are executed through skills and produce effects (RFC-0001, RFC-0002).

Requirements:

- Each plan step **MUST** reference one or more skills.
- Execution of plan steps **MUST** produce traceable effects.
- The set of expected effects declared in a plan **MUST** be consistent with the effects produced during execution.

### 8. Planning as a Process

Planning is the invocation of one or more planning mechanisms (symbolic, rule-based, learned, or human) to generate or revise a plan for a given goal.

The Cognitive Runtime and Cognitive Virtual Machine **MUST** support the invocation of planning mechanisms without embedding any specific planning algorithm.

### 9. Plan Revision and Replanning

Plans **MAY** be revised during execution.

Requirements:

- Plan revisions **MUST** preserve the original `PlanID` while incrementing the version.
- Replanning **MUST** be triggered by belief changes, effect outcomes, or capability revocation.
- All plan revisions **MUST** be recorded in the execution trace.

### 10. Replay and Determinism

Replayed executions **MUST** follow equivalent plan structures.

A conforming implementation **MUST** ensure that:

- The same goal and belief state produce equivalent plan structures during replay.
- Plan revisions occur in the same causal order.
- Execution of plan steps produces equivalent observable effects.

### 11. Open Questions

The following areas require future specification:

- Formal plan validation calculus
- Multi-plan conflict resolution for a single goal
- Learned vs. symbolic planning integration
- Distributed planning across multiple agents

---

**RFC-0005 — Planning Semantics v1.0 Draft** is now complete.

This RFC establishes the semantic foundation for how plans are created, executed, revised, and linked to goals and effects. It forms the next critical layer in the cognitive execution model after goal lifecycle (RFC-0004), belief revision (RFC-0003), and effect ordering (RFC-0002).

---

## [88] CHATGPT (gpt-5-5)

# Ratification Review — RFC-0005 v1.0

**Decision:** **Accepted with Minor Revisions**

**Status:** **Candidate for Ratification** (recommended as **v1.1** after incorporating the refinements below)

RFC-0005 completes the fourth pillar of the Red/Cognition semantic model by defining how `plan!` values bridge declarative goals and executable behaviour. It is consistent with the architectural principles established by the RC specifications and the previously ratified RFCs.

## Conformance Assessment

| Specification | Result |
|---------------|--------|
| RC-000 Constitution | ✓ Pass |
| RC-100 Architecture | ✓ Pass |
| RC-200 Language | ✓ Pass |
| RC-300 Compiler | ✓ Pass |
| RC-400 Runtime | ✓ Pass |
| RC-500 Cognitive Runtime | ✓ Pass |
| RC-700 Cognitive Virtual Machine | ✓ Pass |
| RFC-0001 Cognitive Type System | ✓ Pass |
| RFC-0002 Effect Ordering | ✓ Pass |
| RFC-0003 Belief Revision | ✓ Pass |
| RFC-0004 Goal Lifecycle | ✓ Pass |

## Strengths

RFC-0005 successfully defines:

- Stable **PlanID** with revision history.
- A deterministic plan lifecycle.
- A one-to-one relationship between a plan and its governing goal.
- Explicit linkage between plans, skills, and effects.
- Provider-neutral planning semantics.
- Deterministic replay requirements.
- A clear distinction between planning mechanisms and the runtime that invokes them.

This is fully aligned with the principle that the runtime and CVM execute cognitive operations without embedding a specific planning implementation.

---

# Recommended additions before ratification

## 1. Plan Dependency Graph

The metadata includes `dependencies`, but the graph semantics should be made normative.

Add:

> Plan dependencies **MUST** form a Directed Acyclic Graph (DAG).
>
> Cycles **MUST** be rejected.
>
> A dependent plan **MUST NOT** enter the *Running* state until all prerequisite plans have reached their required completion state.

This mirrors the DAG requirements in RFC-0002 and RFC-0003.

---

## 2. Plan Step Identity

Each step should have a stable identifier.

Example:

```text
step {
    StepID
    skill
    preconditions
    expected-effects
    status
}
```

This improves tracing, checkpointing, and replay.

---

## 3. Plan Validation

Section 5 includes **Validated**, but the criteria are undefined.

Specify that validation **MUST** verify at least:

- structural correctness;
- dependency consistency;
- capability availability;
- precondition consistency;
- absence of dependency cycles.

---

## 4. Plan Execution State

Consider defining execution semantics more precisely.

For example:

```text
Executable
      ↓
Running
      ↓
Suspended
      ↓
Running
      ↓
Completed
```

with:

- suspension;
- checkpoint;
- restoration.

This aligns with RC-500 and RC-700.

---

## 5. Plan Ownership

Like goals, plans should define ownership.

Possible classes:

- Agent plan
- Shared plan
- System plan

This becomes important for cooperative planning.

---

## 6. Memory Placement

To align with RC-500:

> Active plans **SHALL** normally reside in Working Memory.
> Historical plans **MAY** be archived into Episodic Memory.

---

## 7. Plan Revision Graph

Rather than a linear revision history:

- revisions **MUST** form a DAG;
- branches **MAY** exist;
- replay **MUST** preserve revision topology.

This mirrors the belief revision model.

---

## 8. Relationship to Goal Satisfaction

Currently:

> a plan is not successful unless its goal is satisfied.

Consider adding the converse clarification:

> Goal satisfaction is determined by observed effects and supporting beliefs, not merely by plan completion.

This keeps goal semantics governed by RFC-0004.

## Overall assessment

RFC-0005 integrates cleanly with the existing semantic model:

```text
goal!
      │
      │ satisfied by
      ▼
plan!
      │
      │ executes
      ▼
skill!
      │
      │ produces
      ▼
effect!
      │
      │ updates
      ▼
belief!
      │
      └──────────────► influences future planning
```

The resulting feedback loop is coherent:

1. Goals define intent.
2. Planning generates executable strategies.
3. Skills execute steps.
4. Effects change the world.
5. Beliefs are revised.
6. Updated beliefs influence future planning and goal evaluation.

This creates a deterministic, replayable cognitive execution cycle consistent with RC-500 (Cognitive Runtime) and RC-700 (Cognitive Virtual Machine).

## Recommendation

After incorporating the recommended additions, I recommend:

**RFC-0005 — Planning Semantics v1.1**

**Status:** **Ratified**

At that point, the core cognitive semantics would cover:

- ✓ RFC-0001 — Cognitive Type System
- ✓ RFC-0002 — Effect Ordering Model
- ✓ RFC-0003 — Belief Revision System
- ✓ RFC-0004 — Goal Lifecycle and Satisfaction Model
- ✓ RFC-0005 — Planning Semantics

The next logical specification would then be **RFC-0006 — Capability Model**, defining the security and authority framework that governs execution across the compiler, runtime, CVM, and Cognitive Operating System.
