<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #21, sub-message [185], 2026-08-11
  Verbatim source: knowledge-base/sources/message-021-original-part*.md
  Status in corpus: RFC-0044 CSL v1.1 (Candidate for Ratification); supersedes v1.0 draft of sub-message [183] (preserved in archive). Review [186]: "Ratification Recommended (with editorial refinements)" - no ratification decision present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->


**RFC-0044 — Cognitive Standard Library (CSL) v1.1**

**Version:** 1.1  

**Status:** Candidate for Ratification  

**Parent:** RFC-0043 Cognitive Language Specification (CLS) v1.0 (Draft)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Standard Library (CSL)** for Red/Cognition.

The CSL provides a canonical set of cognitive types, operations, dialects, modules, and utilities that every conforming Red/Cognition implementation **MUST** or **SHOULD** provide. It serves as the foundational library layer that sits above the language specification (RFC-0043) and below application-level cognitive programs.

The goal of the CSL is to ensure consistency, interoperability, and a high-quality developer experience across different compilers, runtimes, and cognitive operating systems.

### 2. Design Principles

The Cognitive Standard Library follows these principles:

- **Minimality with Completeness** — Provide the smallest set of primitives that enables the construction of complex cognitive systems.

- **Determinism** — Core operations must behave deterministically when required by the declared determinism level.

- **Capability Awareness** — Library operations must declare and respect capability requirements.

- **Provider Neutrality** — The library must not embed assumptions about specific reasoning or planning implementations.

- **Traceability** — All operations that affect state or produce effects must participate in execution traces.

- **Replay Equivalence** — Library operations must support deterministic replay.

### 3. Library Profiles

Not every implementation will provide the full CSL. The following profiles are defined:

| Profile              | Mandatory Modules                                      | Use Case                     |

|----------------------|--------------------------------------------------------|------------------------------|

| **Core**             | `cognition.core`, `goal`, `belief`, `capability`       | Embedded / minimal runtimes  |

| **Runtime**          | Core + `scheduler`, `checkpoint`, `trace`              | Standard cognitive runtimes  |

| **Distributed**      | Runtime + `federation`, `network`, `registry`          | Multi-node / federated systems |

| **Full**             | All standard modules                                   | Complete cognitive platforms |

Implementations **MUST** declare their supported profile(s).

### 4. Module Versioning

Every standard module **MUST** expose semantic version metadata:

```

cognition.goal Version: 1.0.0 Compatibility: RFC-0044

```

Version changes **MUST** follow semantic versioning. Breaking changes require a new major version and a migration path.

### 5. Core Modules (Mandatory)

| Module                    | Purpose                                              | Purity Classification |

|---------------------------|------------------------------------------------------|-----------------------|

| `cognition.core`          | Foundational operations `observe`, `infer`, `remember`, `plan`, `execute`, `reflect`, `checkpoint`) | Mixed |

| `cognition.goal`          | Goal construction, lifecycle, satisfaction           | Declarative           |

| `cognition.belief`        | Belief creation, revision, querying                  | Knowledge             |

| `cognition.capability`    | Capability acquisition, verification, revocation     | Security              |

| `cognition.effect`        | Effect creation, ordering, tracing                   | Event                 |

| `cognition.memory`        | Access to four-tier memory architecture              | Mixed                 |

| `cognition.agent`         | Agent lifecycle and state management                 | Entity                |

### 6. Recommended Modules

| Module                    | Purpose                                              | Purity Classification |

|---------------------------|------------------------------------------------------|-----------------------|

| `cognition.skill`         | Skill registration, invocation, versioning           | Mixed                 |

| `cognition.plan`          | Plan construction, validation, execution             | Procedure             |

| `cognition.scheduler`     | Scheduling primitives and policy interfaces          | Control               |

| `cognition.trace`         | Execution tracing and provenance                     | Observability         |

| `cognition.reflect`       | Reflection and self-model operations                 | Meta-cognitive        |

| `cognition.checkpoint`    | Checkpoint creation and restoration                  | Recovery              |

| `cognition.workflow`      | Structured multi-step processes                      | Procedure             |

| `cognition.policy`        | Declarative security and governance rules            | Governance            |

| `cognition.simulation`    | What-if and scenario modeling                        | Pure / Internal       |

### 7. Separation of Pure and Effectful Operations

The CSL distinguishes operations by their effect class (aligned with RFC-0002 and RFC-0007):

**Pure operations** (no external effects):

- `infer(...)`, `evaluate(...)`, `score(...)`

**Effectful operations** (may produce external effects):

- `observe(...)`, `remember(...)`, `execute(...)`, `checkpoint(...)`

Effectful operations **MUST** declare their `EffectClass` and required capabilities.

### 8. Standard Error Model

The CSL defines the following canonical error types (integrated with RFC-0015):

- `CapabilityDenied`

- `GoalUnsatisfied`

- `MemoryUnavailable`

- `CheckpointInvalid`

- `PolicyViolation`

- `ProofVerificationFailed`

- `ResourceQuotaExceeded`

- `SkillFailure`

- `PlanFailure`

All errors **MUST** carry provenance and participate in execution traces.

### 9. Async and Long-Running Operations

Operations such as `observe`, `plan`, and `execute` **MAY** be long-running.

The CSL supports the following return styles (implementation may choose one or more):

- Immediate value

- Future / Promise

- Task / Continuation

- Streamed result

The chosen style **MUST** be documented and must integrate with the scheduler (RFC-0011).

### 10. Reflection API

The `cognition.reflect` module provides:

- `reflect.trace(agent?)`

- `reflect.goals(agent?)`

- `reflect.effects(agent?)`

- `reflect.capabilities(agent?)`

- `reflect.reasoning(agent?)`

- `reflect.memory(agent?)`

These operations **MUST** respect capability and policy constraints.

### 11. Standard Collections

The CSL provides cognitive-aware collection types:

- `GoalSet`, `BeliefSet`, `PlanSet`, `SkillSet`, `CapabilitySet`

- `EffectGraph`, `GoalGraph`, `PlanGraph`

- `Trace`, `EventDAG`

These collections **MUST** support deterministic iteration and hashing.

### 12. Standard Serialization

All CSL types **MUST** support canonical serialization to:

- CIR (RFC-0028)

- CIR-SER (RFC-0029)

- CPCPF (RFC-0033)

- JSON / CBOR (for interoperability)

Serialization **MUST** be deterministic and versioned.

### 13. Module Hierarchy (Recommended)

```

cognition.core

cognition.types

cognition.goal

cognition.plan

cognition.belief

cognition.capability

cognition.effect

cognition.memory

cognition.agent

cognition.trace

cognition.reflect

cognition.scheduler

cognition.workflow

cognition.policy

cognition.simulation

cognition.checkpoint

cognition.compiler

cognition.proof

cognition.package

cognition.registry

cognition.governance

cognition.federation

cognition.marketplace

```

### 14. Conformance

A conforming CSL implementation **MUST** provide all modules marked **Mandatory** in Section 5.

Modules marked **Recommended** **SHOULD** be provided. If omitted, the implementation **MUST** document the omission and provide a migration or compatibility note.

### 15. Open Questions

The following areas require future specification:

- Formal semantics and resource characteristics of each operation

- Extension mechanism for additional standard modules

- Integration with external cognitive libraries and foreign function interfaces

- Performance and energy characteristics of library operations

---

**RFC-0044 — Cognitive Standard Library (CSL) v1.1** is now ready for **Final Ratification Review**.

This version incorporates library profiles, module versioning, separation of pure and effectful operations, a standard error model, reflection APIs, and standard collections, bringing it in line with the precision of the strongest RFCs in the series.
