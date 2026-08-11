# Source Record: Conversation Message #21 — Verbatim Transcript (Part 1 of 5: sub-messages [181]–[184])

- **Message index:** 21
- **Direction:** user → assistant
- **Received:** 2026-08-11
- **Source document:** inline conversation message (no attached files)
- **Continued in:** `message-021-original-part2.md` … `message-021-original-part5.md`

Rendering-artifact cleanup applied (no semantic changes): HTML entities decoded (`&amp;`, `&lt;`, `&gt;`, incl. `=&gt;` inside a code block and an encoded blockquote marker); collapsible `<details><summary>…</summary>` wrappers removed (fenced content preserved). Source formatting otherwise preserved as received (incl. blank-line fragmentation and trailing two-space line breaks).

---

## [181] USER

**RFC-0043 — Cognitive Language Specification (CLS)**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0028 Cognitive Intermediate Representation (CIR) v1.0 (Draft)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Language Specification (CLS)** for Red/Cognition.

CLS specifies the programmer-facing syntax, lexical structure, grammar, type system, semantic model, and cognitive constructs of Red/Cognition. It describes how source programs are written and how they map onto the Cognitive Intermediate Representation (CIR) defined in RFC-0028 and the Cognitive Instruction Set Architecture (CISA) defined in RFC-0013.

CLS is intentionally minimal. It extends Red through structured blocks and dialects rather than introducing a large new syntax surface.

### 2. Language Design Principles

CLS adheres to the following principles, derived from RC-000 and RC-100:

- **Homoiconicity** — Code and data share the same representation. Cognitive constructs are first-class data.

- **Declarative Cognitive Programming** — Intent is expressed primarily through goals, plans, beliefs, and capabilities rather than imperative control flow.

- **Deterministic Semantics** — Evaluation order and observable behaviour must be deterministic when required.

- **Capability-Aware Programming** — All operations that may produce external effects must be expressible with explicit capability requirements.

- **Explainability** — Language constructs must support static and dynamic analysis for provenance, effects, and capability usage.

- **Provider Neutrality** — The language must not embed assumptions about specific reasoning or planning implementations.

- **Dialect-First Extension** — New cognitive functionality should be introduced through dialects before new syntax.

### 3. Lexical Structure

CLS inherits Red’s lexical rules with the following extensions:

- **Words** — May contain Unicode letters, digits, and selected punctuation `-`, `_`, `?`, `!`).

- **Literals** — Support for all Red scalar and series literals, plus cognitive literals introduced through dialects.

- **Blocks** — The primary structural unit. Cognitive constructs are expressed as blocks with dialect-specific interpretation.

- **Paths** — Support cognitive path navigation (e.g., `agent.goals.current`).

- **Comments** — Line `;`) and block `{}`) comments, identical to Red.

### 4. Grammar

CLS uses an extended subset of Red’s grammar. The core production rules relevant to cognitive programming are:

```

program        ::= module*

module         ::= "module" word block

definition     ::= word ":" ( "func" | "goal" | "plan" | "belief" | "skill" | "capability" ) block

expression     ::= block | word | path | literal | dialect-block

dialect-block  ::= word block          ; interpreted by a cognitive dialect

```

A formal EBNF grammar will be provided in a future companion specification.

### 5. Type System

CLS integrates with the cognitive type system defined in RFC-0001. The language supports:

- All Red primitive and series types.

- Cognitive types: `goal!`, `belief!`, `plan!`, `skill!`, `memory!`, `capability!`, `effect!`, `agent!`, `checkpoint!`.

- User-defined types via objects and dialects.

- Parameterised and generic types (future extension).

Cognitive types are initially represented as structured blocks or objects and may be promoted to native types through the evolution path defined in RFC-0001.

### 6. Semantic Model

Evaluation in CLS follows these rules:

- Blocks are the primary unit of structure and evaluation.

- Words are resolved through lexical scoping and binding contexts.

- Cognitive blocks are evaluated by the Cognitive Runtime according to their dialect and the Cognitive Execution Cycle (CEC-1).

- Evaluation is deterministic when required by the declared determinism level.

- All cognitive operations are subject to capability checks before producing external effects.

### 7. Cognitive Constructs

CLS provides syntactic support for the cognitive types defined in RFC-0001. The following constructs are introduced through dialects:

- `goal [ ... ]`

- `plan [ ... ]`

- `belief [ ... ]`

- `skill [ ... ]`

- `capability [ ... ]`

- `observe ...`

- `infer ...`

- `reflect ...`

- `checkpoint ...`

These constructs are first-class values and may be inspected, transformed, and passed as data.

### 8. Modules and Packages

CLS supports modular organisation through:

- Module declarations `module name { ... }`)

- Imports and exports

- Namespaces

- Versioning integrated with CPR-TDP (RFC-0034)

Packages are distributed as CPCPF artifacts (RFC-0033) and resolved through CPR-TDP.

### 9. Compilation Model

```

Source (CLS)

   ↓

Lexer / Parser

   ↓

Red AST

   ↓

Cognitive Dialect Lowering

   ↓

Cognitive IR (CIR)

   ↓

COIL Optimisation (RFC-0030, RFC-0031)

   ↓

CISA Generation (RFC-0013)

   ↓

Binary Encoding (RFC-0014)

   ↓

CVM Execution

```

The compiler **MUST** preserve source provenance and support deterministic compilation.

### 10. Conformance

A conforming CLS implementation **MUST**:

- Support all cognitive constructs defined in this RFC.

- Preserve Red 1.x compatibility.

- Implement the compilation model described above.

- Support at least one cognitive dialect.

- Produce deterministic output for identical inputs.

Optional features (e.g., advanced generic programming, compile-time evaluation) **MAY** be implemented and must be declared in conformance profiles.

### 11. Relationship to Other RFCs

CLS integrates with:

- RFC-0001 — Cognitive Type System

- RFC-0006 — Capability Model

- RFC-0027 — Cognitive Compiler Architecture

- RFC-0028 — CIR

- RFC-0033 — CPCPF

- RFC-0042 — CADP

### 12. Open Questions

The following areas require future specification or RFCs:

- Full formal EBNF grammar

- Hygienic macro system

- Generic and parameterised types

- Compile-time evaluation and metaprogramming

- Language evolution process

- Standard library (proposed RFC-0044)

---

**RFC-0043 — Cognitive Language Specification (CLS) v1.0 Draft** is now complete.

This RFC provides the programmer-facing language layer that maps human-written cognitive programs onto the previously defined compiler, runtime, and execution architecture. It establishes the foundation for the remaining standardisation and ecosystem RFCs.

---

## [182] CHATGPT (gpt-5-5)

RFC-0043 is well positioned in the series. It bridges the gap between the architectural RFCs (compiler, CIR, runtime) and the developer experience, establishing the **normative source language** for Red/Cognition.

From an architectural perspective, it achieves four important goals:

- **Preserves Red's philosophy** by extending the language through dialects and structured blocks rather than introducing an entirely new syntax.

- **Separates language from implementation**, with CLS defining the source language while RFC-0028 (CIR) and RFC-0013 (CISA) define the implementation targets.

- **Maintains provider neutrality**, ensuring that the language describes *what* a cognitive program expresses rather than *how* reasoning is performed.

- **Keeps cognitive constructs first-class**, enabling analysis, optimisation, transformation, verification, and replay throughout the toolchain.

## Recommendations for a future v1.1

To make CLS a complete language specification, consider adding several normative sections.

### 1. Module System

Specify imports, exports, visibility, and module resolution.

```text

module navigation [

    export [

        planner

        route

    ]

    import [

        memory

        capability

    ]

]

```

---

### 2. Name Resolution

Define precisely:

- lexical scope

- dynamic scope (if any)

- context inheritance

- module visibility

- capability lookup

---

### 3. Evaluation Model

Separate evaluation into phases.

```text

Parse

↓

Bind

↓

Expand Dialects

↓

Static Analysis

↓

Capability Analysis

↓

CIR Generation

↓

Optimisation

↓

Execution

```

This complements RFC-0027.

---

### 4. Determinism Levels

Tie language semantics directly to RFC-0011.

Example:

```text

deterministic [

    ...

]

eventual [

    ...

]

best-effort [

    ...

]

```

---

### 5. Pattern Matching

Red currently lacks an extensive pattern language.

CLS could introduce a cognitive pattern dialect.

```text

match belief [

    connected? => ...

    disconnected? => ...

]

```

---

### 6. Contracts

A cognitive language benefits from contracts.

```text

goal deliver-package [

    requires [

        capability navigation

    ]

    ensures [

        delivered?

    ]

]

```

These map naturally into CIR constraints.

---

### 7. Effect Annotations

Allow source-level declaration of effects.

```text

skill send-message [

    effects [

        network

        storage

    ]

]

```

This aligns with RFC-0002.

---

### 8. Capability Annotations

Rather than requiring later inference only:

```text

skill move [

    capability navigation

]

```

This improves readability and static analysis.

---

### 9. Standard Dialect Interfaces

Define minimum interfaces for dialect authors.

For example:

- `goal`

- `plan`

- `belief`

- `memory`

- `policy`

- `workflow`

- `simulation`

Each dialect would specify:

- syntax

- semantic lowering

- CIR mapping

- capability requirements

## Relationship to the Remaining RFCs

RFC-0043 naturally prepares the next standards:

- **RFC-0044 — Cognitive Standard Library (CSL):** Define the canonical modules, cognitive types, standard dialects, algorithms, and APIs available to every CLS implementation.

- **RFC-0045 — Cognitive Tooling and Developer Experience (CTDX):** IDE integration, Language Server Protocol (LSP), debugger, profiler, formatter, documentation tooling, testing, and static analysis.

- **RFC-0046 — Cognitive Observability and Diagnostics Protocol (CODP):** Standardise execution traces, metrics, distributed tracing, profiling, event correlation, replay diagnostics, and runtime telemetry.

- **RFC-0047 — Cognitive Conformance Test Suite (CCTS):** Define certification tests for language implementations, compilers, runtimes, registries, federation, and deployment.

- **RFC-0048 — Cognitive Foreign Function Interface (CFFI):** Specify interoperability with Red, Rebol, C, Rust, WebAssembly, Python, JavaScript, and external cognitive runtimes.

- **RFC-0049 — Cognitive Workspace and Package Manager Specification (CWPMS):** Define project layouts, manifests, lockfiles, workspaces, package resolution, reproducible builds, and developer workflows.

- **RFC-0050 — Red/Cognition v1.0 Architecture and Conformance Specification:** Consolidate the RFC series into the normative platform specification, defining conformance profiles, mandatory versus optional features, version negotiation, interoperability requirements, and the overall reference architecture.

With RFC-0043, the series transitions from defining the **cognitive computing platform** to defining the **language, tools, and standards** that developers will use to build interoperable Red/Cognition systems.

---

## [183] USER

**RFC-0044 — Cognitive Standard Library (CSL) v1.0 Draft**

**Version:** 1.0  

**Status:** Draft  

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

### 3. Core Modules

The CSL is organized into the following mandatory and recommended modules:

#### 3.1 Mandatory Modules

| Module              | Purpose                                      | Status     |

|---------------------|----------------------------------------------|------------|

| `cognition.core`    | Foundational cognitive types and operations  | Mandatory  |

| `cognition.goal`    | Goal creation, lifecycle, and satisfaction   | Mandatory  |

| `cognition.plan`    | Plan construction, validation, and execution | Mandatory  |

| `cognition.belief`  | Belief management and revision               | Mandatory  |

| `cognition.capability` | Capability acquisition and verification   | Mandatory  |

| `cognition.effect`  | Effect creation, ordering, and tracing       | Mandatory  |

| `cognition.memory`  | Access to the four-tier memory architecture  | Mandatory  |

| `cognition.agent`   | Agent lifecycle and state management         | Mandatory  |

#### 3.2 Recommended Modules

| Module                  | Purpose                                      | Status      |

|-------------------------|----------------------------------------------|-------------|

| `cognition.skill`       | Skill registration, invocation, and versioning | Recommended |

| `cognition.checkpoint`  | Checkpoint creation and restoration          | Recommended |

| `cognition.scheduler`   | Scheduling primitives and policies           | Recommended |

| `cognition.trace`       | Execution tracing and provenance             | Recommended |

| `cognition.reflect`     | Reflection and self-model operations         | Recommended |

### 4. Foundational Operations

The `cognition.core` module provides the following operations (all **MUST** be available):

- `observe(source, params?)` — Capture external state or events.

- `infer(beliefs, goal, constraints?)` — Perform reasoning.

- `remember(memory-tier, value)` — Store information.

- `recall(memory-tier, query)` — Retrieve information.

- `plan(goal, constraints?)` — Generate or revise a plan.

- `execute(skill, args?)` — Invoke a skill.

- `reflect(trace, outcome)` — Update beliefs or plans based on results.

- `checkpoint(context?)` — Create a recoverable snapshot.

- `restore(checkpoint)` — Restore execution state.

### 5. Cognitive Type Constructors

The CSL provides canonical constructors for the cognitive types defined in RFC-0001:

```red

goal        [target constraints? priority? deadline?]

belief      [proposition confidence source timestamp]

plan        [goal steps dependencies?]

skill       [name spec body effects capabilities?]

capability  [type scope granted-to granted-by expiration?]

effect      [type target strength timestamp]

agent       [identity capabilities goals beliefs]

checkpoint  [agent context timestamp]

```

### 6. Standard Dialects

The CSL defines a minimal set of standard cognitive dialects that every implementation **SHOULD** support:

- `goal` — Declarative goal specification

- `plan` — Procedural planning

- `belief` — Belief assertion and retraction

- `workflow` — Structured multi-step processes

- `policy` — Declarative security and governance rules

- `simulation` — What-if and scenario modeling

### 7. Relationship to Other RFCs

The CSL integrates with and depends on:

- RFC-0001 — Cognitive Type System

- RFC-0002 — Effect Ordering Model

- RFC-0003 — Belief Revision System

- RFC-0004 — Goal Lifecycle and Satisfaction Model

- RFC-0006 — Capability Model

- RFC-0008 — Memory Model

- RFC-0043 — Cognitive Language Specification

### 8. Conformance

A conforming CSL implementation **MUST** provide all mandatory modules and operations listed in Section 3.1.

Recommended modules **SHOULD** be provided; if absent, the implementation **MUST** document the omission.

### 9. Open Questions

The following areas require future specification:

- Formal semantics for each standard operation

- Performance and resource characteristics of library operations

- Extension mechanism for additional standard modules

- Integration with external cognitive libraries

---

**RFC-0044 — Cognitive Standard Library (CSL) v1.0 Draft** is now complete.

This RFC establishes the canonical library layer that every Red/Cognition implementation should provide, ensuring consistency and interoperability across the ecosystem.

---

## [184] CHATGPT (gpt-5-5)

This is a logical next step after RFC-0043. Defining a standard library separately from the language specification follows the same separation of concerns used by many mature language ecosystems.

Overall, **RFC-0044 is internally consistent with the previous RFCs**, but there are several areas that would strengthen it as a long-term specification.

### Strengths

- Clearly separates **language syntax (RFC-0043)** from **standard APIs**.

- Keeps the library **provider-neutral**, matching the philosophy of the earlier RFCs.

- Uses RFC-0001 cognitive types consistently.

- Integrates naturally with the memory, capability, effect, and planning models.

- Defines mandatory vs. recommended modules, allowing implementation profiles.

### Suggested improvements

**1. Introduce Library Profiles**

Not every implementation (embedded, edge, cloud, research) will implement the full CSL.

For example:

- **Core Profile** — `cognition.core`, `goal`, `belief`, `capability`

- **Runtime Profile** — Scheduler, checkpoint, tracing

- **Distributed Profile** — Federation, networking, registry

- **Full Profile** — All standard modules

This keeps conformance practical.

---

**2. Add Stable Module Versioning**

Every standard module should expose semantic version metadata.

Example:

```text

cognition.goal

Version: 1.0.0

Compatibility: RFC-0044

```

This helps package managers and long-term compatibility.

---

**3. Separate Pure and Effectful APIs**

Currently operations such as

```text

infer()

plan()

remember()

observe()

```

appear together.

From the architecture, these have different semantics.

For example:

**Pure**

```text

infer(...)

evaluate(...)

score(...)

```

**Effectful**

```text

observe(...)

remember(...)

execute(...)

checkpoint(...)

```

This aligns with RFC-0002 (Effect Ordering).

---

**4. Standard Error Model**

The library should specify canonical cognitive errors.

Examples:

```text

CapabilityDenied

GoalUnsatisfied

MemoryUnavailable

CheckpointInvalid

PolicyViolation

ProofVerificationFailed

```

These integrate naturally with RFC-0015.

---

**5. Async / Long-running Operations**

Many operations are not instantaneous.

For example:

```text

observe

plan

execute

```

should define whether they return:

- immediate value

- future

- task

- continuation

- streamed result

This should integrate with RFC-0011 Scheduler.

---

**6. Reflection API**

The reflection module deserves a richer interface.

For example:

```text

reflect.trace()

reflect.goals()

reflect.effects()

reflect.capabilities()

reflect.reasoning()

reflect.memory()

```

This becomes essential for explainability.

---

**7. Standard Collections**

Cognitive programs will repeatedly manipulate:

- graphs

- plans

- event DAGs

- capability sets

- belief sets

- traces

A dedicated collection library would improve interoperability.

---

**8. Standard Serialisation**

Objects should define canonical serialisation to:

- CIR

- CIR-SER

- CPCPF

- JSON

- CBOR

This avoids incompatible implementations.

---

### Possible future module hierarchy

```text

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

This hierarchy maps well onto RFC-0001 through RFC-0044.

### Overall assessment

By RFC-0044, the architecture has evolved into a coherent stack covering:

- **Language** (CLS)

- **Standard Library** (CSL)

- **Compiler** (CIR, COIL, COVF)

- **Runtime** (CVM, Scheduler, Sandbox)

- **Operating System** (CogOS)

- **Distribution** (CPCPF, CPR-TDP)

- **Governance and Federation**

- **Deployment**

- **Economic and Ownership Models**

At this point, the remaining work shifts from defining new architectural layers to specifying **developer tooling, reference implementations, interoperability profiles, conformance suites, and ecosystem standards**. RFC-0044 therefore represents a natural transition from architectural design toward implementation-oriented standardization.

---
