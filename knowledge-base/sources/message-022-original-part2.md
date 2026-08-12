# Source Record: Conversation Message #22 — Verbatim Transcript (Part 2 of 5: sub-messages [205]–[208])

- **Message index:** 22 (continued) · **Part 2:** `message-022-original-part1.md` · **Cleanup:** as Part 1.

---

## [205] USER

**RFC-0048 — Cognitive Foreign Function Interface (CFFI) v1.1**

**Version:** 1.1  

**Status:** Candidate for Ratification  

**Parent:** RFC-0047 Cognitive Package Manager and Workspace Specification (CPMWS) v1.2 (Candidate)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Foreign Function Interface (CFFI)** for Red/Cognition.

While RFC-0043 (Cognitive Language Specification) and RFC-0044 (Cognitive Standard Library) define the core language and library, CFFI specifies how Red/Cognition programs interact with foreign code written in other languages (such as Red, Rebol, C, Rust, WebAssembly, Python, and JavaScript) and with external cognitive runtimes.

CFFI ensures that cognitive programs can safely and deterministically call into, and be called from, foreign code while preserving capability enforcement, traceability, and replay equivalence.

### 2. Design Principles

CFFI follows these principles:

- **Determinism** — Foreign calls must produce reproducible results given the same inputs and state.

- **Capability Mediation** — All foreign calls that may produce external effects must be capability-gated.

- **Traceability** — Foreign calls and their results must participate in execution traces.

- **Replay Equivalence** — Replayed executions involving foreign calls must produce equivalent observable behaviour.

- **Provider Neutrality** — The interface must remain independent of specific foreign language implementations or reasoning mechanisms.

- **Safety** — Foreign calls must not bypass the security, isolation, or policy models of the Cognitive Runtime and CogOS.

### 3. Conformance Profiles

CFFI defines the following implementation profiles:

| Profile     | Supported Languages                          | Typical Runtime                  |

|-------------|----------------------------------------------|----------------------------------|

| **Embedded**| Red, C                                     | Embedded systems                 |

| **Standard**| Embedded + Rust + WebAssembly                | Desktop / server runtimes        |

| **Extended**| Standard + Python + JavaScript               | AI development environments      |

| **Full**    | All bindings + remote runtimes               | Distributed CogOS platforms      |

Implementations **MUST** declare their supported profile(s).

### 4. Determinism Classification

Foreign functions **MUST** be classified by determinism level:

| Class             | Description                              | Replay Behaviour                  |

|-------------------|------------------------------------------|-----------------------------------|

| **Pure**          | No observable side effects               | Reproducible                      |

| **Deterministic** | Deterministic given inputs               | Reproducible                      |

| **ReplayRecorded**| Non-deterministic; results must be recorded | Use recorded values during replay |

| **Effectful**     | Produces external effects                | Subject to capability enforcement |

| **External**      | Depends on external state                | Requires recorded input values    |

### 5. Memory Ownership Model

Objects crossing the FFI boundary **MUST** declare an ownership model:

- **Borrowed** — Temporary reference; caller retains ownership.

- **Shared** — Shared ownership with reference counting or garbage collection.

- **Copied** — Value is copied across the boundary.

- **Owned** — Ownership is transferred to the callee.

- **Immutable** — Read-only access.

- **Pinned** — Memory location is stable for the duration of the call.

The chosen model **MUST** be declared in the binding.

### 6. ABI Stability

CFFI supports the following ABI classes:

- Native C ABI

- Stable Rust ABI (via C or component model)

- WASI Component ABI

- Red ABI

- Rebol ABI

Implementations **MUST** declare supported ABIs.

### 7. Async Foreign Calls

Asynchronous foreign calls **MUST** integrate with the scheduler (RFC-0011).

Supported styles include:

- Synchronous

- Future / Promise

- Stream

- Callback

- Continuation

The chosen style **MUST** be documented in the binding.

### 8. Sandboxing Levels

Foreign code execution **MAY** occur at different isolation levels:

| Level       | Isolation                              | Use Case                     |

|-------------|----------------------------------------|------------------------------|

| **Trusted** | Native execution                       | Trusted libraries            |

| **Sandboxed** | Runtime isolation                    | Untrusted native code        |

| **WASM**    | WebAssembly sandbox                    | Portable, safe execution     |

| **Remote**  | Separate runtime or node               | Distributed execution        |

| **Verified**| Proof-carrying module                  | High-assurance execution     |

### 9. Type Mapping

CFFI defines a canonical mapping between cognitive types and foreign types. Examples include:

- `goal!` ↔ Rust `struct Goal`, C `struct`, WASM component, Python class, JavaScript object

- `belief!` ↔ equivalent structures in each language

- `capability!` ↔ opaque handle or token in each language

Bindings **MUST** declare the mapping used.

### 10. Error Translation

Foreign exceptions **MUST** be translated into Red/Cognition exceptions (RFC-0015):

| Foreign Error       | CFFI Exception             |

|---------------------|----------------------------|

| Rust panic          | `ForeignFailure`           |

| Python `Exception`  | `ForeignFailure`           |

| Segmentation fault  | `FatalForeignFailure`      |

| WASM trap           | `ForeignTrap`              |

### 11. Foreign Module Manifest

Every foreign module **MUST** expose metadata:

```

ForeignModule {

    Name,

    Version,

    ABI,

    Language,

    Capabilities,

    Effects,

    Determinism,

    Signature (optional)

}

```

This metadata **MUST** be included when packaging foreign modules as CPCPF artifacts.

### 12. Conformance Requirements

A conforming CFFI implementation **MUST**:

- Validate bindings at load time.

- Enforce capabilities before foreign calls.

- Preserve traceability for all foreign interactions.

- Support deterministic replay (including recorded non-deterministic results).

- Expose binding metadata for static analysis and tooling.

- Document supported language profiles and ABIs.

### 13. Relationship to Other RFCs

CFFI integrates with:

- RFC-0002 — Effect Ordering

- RFC-0006 — Capability Model

- RFC-0015 — Exception Semantics

- RFC-0016 — Cognitive Runtime Architecture

- RFC-0025 — Security Policy Language

- RFC-0035 — CSEIM (sandboxing)

- RFC-0036 — CBR-SCP (supply chain)

- RFC-0037 — CSLEMP (lifecycle)

- RFC-0043 — Cognitive Language Specification

- RFC-0044 — Cognitive Standard Library

### 14. Open Questions

The following areas require future specification:

- Performance and resource characteristics of foreign calls

- Sandboxing and isolation of foreign code

- Asynchronous and streaming foreign call semantics

- Formal verification of foreign function bindings

- Standard foreign module manifest schema

---

**RFC-0048 — Cognitive Foreign Function Interface (CFFI) v1.1** is now ready for **Final Ratification Review**.

This version incorporates conformance profiles, determinism classification, memory ownership models, ABI stability classes, async call support, sandboxing levels, canonical type mappings, error translation, foreign module manifests, and explicit conformance requirements, bringing it in line with the precision of the strongest RFCs in the series.

---

## [206] CHATGPT (gpt-5-5)

RFC-0048 v1.1 is a significant improvement and is comparable in maturity to RFC-0046 v1.2 (CODP) and RFC-0047 v1.2 (CPMWS). I would assess it as **96–98% complete** and suitable for **Candidate for Final Ratification**. It now covers most of the design space expected of a modern, language-independent FFI specification.

### Strengths

The RFC now provides a comprehensive framework:

- **Interoperability model** through language profiles and ABI declarations.

- **Execution semantics** via determinism classes and replay behaviour.

- **Memory safety** through explicit ownership models.

- **Security** through capability enforcement and sandboxing levels.

- **Tooling support** via binding metadata and static analysis requirements.

- **Runtime integration** with scheduler, tracing, replay, and packaging.

- **Cross-language consistency** through canonical type mapping and error translation.

It is well aligned with the surrounding RFCs, particularly RFC-0002, RFC-0006, RFC-0015, RFC-0016, RFC-0035, RFC-0036, RFC-0043, RFC-0044, RFC-0046, and RFC-0047.

## Remaining recommendations

These are refinements rather than architectural gaps.

### 1. Canonical Binding Schema

The RFC describes what bindings contain but not their formal representation. Adding a normative schema would improve interoperability.

For example:

```text

ForeignBinding {

    Name

    Symbol

    Language

    ABI

    Signature

    InputTypes

    OutputTypes

    Ownership

    Determinism

    EffectClass

    RequiredCapabilities

    AsyncStyle

}

```

This becomes the canonical format consumed by the compiler, runtime, debugger, and package manager.

---

### 2. Version Negotiation

Introduce compatibility rules for foreign modules.

Example:

- ABI version

- Interface version

- Minimum runtime version

- Maximum supported runtime version

This avoids silent incompatibilities.

---

### 3. Streaming Semantics

Section 7 identifies streams but does not specify lifecycle.

A future RFC should define:

- opening

- yielding

- cancellation

- completion

- failure

- replay

for foreign streams.

---

### 4. Resource Accounting

Foreign code should integrate with RFC-0024.

Bindings should optionally declare:

- CPU budget

- memory budget

- timeout

- I/O quota

- network quota

This enables scheduler and policy enforcement.

---

### 5. Trust Model

The current sandbox levels are excellent, but module trust could also be classified.

For example:

| Trust | Meaning |

|-------|---------|

| Trusted | Platform module |

| Verified | Cryptographically verified |

| Audited | Third-party audited |

| Community | Registry trust only |

| Untrusted | User supplied |

This integrates naturally with RFC-0034 and RFC-0036.

---

### 6. Remote Runtime Protocol

The "Full" profile references remote runtimes but does not specify invocation semantics.

Eventually this should define:

- transport

- authentication

- serialization

- timeout

- retry

- cancellation

- trace propagation

That could become a dedicated future RFC.

---

### 7. FFI Lifecycle

A normative lifecycle would help implementations converge.

```text

Load

↓

Validate

↓

Verify Signature

↓

Resolve ABI

↓

Capability Check

↓

Execute

↓

Trace

↓

Replay

↓

Unload

```

---

### 8. Observability Integration

RFC-0046 already defines observability.

CFFI should state that every foreign invocation emits standard lifecycle events such as:

- ForeignCallStarted

- ForeignCallCompleted

- ForeignCallFailed

- ForeignReplay

- ForeignModuleLoaded

This avoids ecosystem divergence.

## Ratification assessment

Current maturity across the recent RFCs is approximately:

| RFC | Status | Maturity |

|------|--------|----------:|

| RFC-0043 CLS | Draft | 94% |

| RFC-0044 CSL | Candidate | 98% |

| RFC-0045 CTDX | Candidate | 98% |

| RFC-0046 CODP | Final Candidate | 99% |

| RFC-0047 CPMWS | Final Candidate | 99% |

| RFC-0048 CFFI | Candidate | **97–98%** |

## Overall assessment

RFC-0048 successfully completes another major subsystem of the Red/Cognition platform. Together, RFC-0043 through RFC-0048 now define:

- **CLS** — the language

- **CSL** — the standard library

- **CTDX** — the developer toolchain

- **CODP** — observability and diagnostics

- **CPMWS** — package management and workspaces

- **CFFI** — interoperability with native, managed, and distributed environments

This forms a coherent developer ecosystem built on top of the previously specified runtime, compiler, deployment, governance, and operating system layers.

At this stage, the architecture is naturally shifting from defining core platform components toward standardising higher-level capabilities. Logical next RFCs include areas such as a **Cognitive Macro and Metaprogramming System**, a **Standard Testing and Verification Framework**, a **Remote Agent Invocation Protocol**, or a **Formal Language Specification (EBNF and semantics)** to complete the language standard.

---

## [207] USER

**RFC-0049 — Cognitive Standard Toolchain Specification (CSTS) v1.0 Draft**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0048 Cognitive Foreign Function Interface (CFFI) v1.1 (Candidate)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Standard Toolchain Specification (CSTS)** for Red/Cognition.

While RFC-0045 (Cognitive Tooling and Developer Experience) and RFC-0047 (Cognitive Package Manager and Workspace Specification) describe tooling and package management, CSTS specifies the canonical reference toolchain that every conforming Red/Cognition implementation **SHOULD** provide. This includes the compiler, linker, package manager, debugger, profiler, formatter, linter, documentation generator, and deployment tools, along with their expected interfaces and behaviour.

The goal of CSTS is to ensure a consistent, reproducible, and high-quality developer experience across the Red/Cognition ecosystem.

### 2. Design Principles

CSTS follows these principles:

- **Determinism** — All toolchain components must support deterministic and reproducible operation.

- **Capability Awareness** — Toolchain operations must respect capability and policy constraints.

- **Traceability** — Toolchain actions that affect builds or deployments must be recorded.

- **Provider Neutrality** — The specification must remain independent of specific compiler or runtime implementations.

- **Interoperability** — Toolchain components must interoperate through stable, documented interfaces.

### 3. Reference Toolchain Components

A conforming implementation **SHOULD** provide the following components:

#### 3.1 Compiler

- Support for the Cognitive Language Specification (RFC-0043)

- Generation of Cognitive IR (RFC-0028) and CISA (RFC-0013)

- Integration with COIL (RFC-0031) and COVF (RFC-0032)

- Deterministic and reproducible compilation

#### 3.2 Linker

- Linking of CISA modules and foreign libraries (via CFFI, RFC-0048)

- Production of CPCPF artifacts (RFC-0033)

#### 3.3 Package Manager

- Workspace and dependency management (RFC-0047)

- Registry interaction (RFC-0034)

- Reproducible builds and lockfile support (RFC-0036)

#### 3.4 Debugger

- Support for breakpoints, inspection, and step-through of the Cognitive Execution Cycle

- Integration with checkpoints (RFC-0010) and traces (RFC-0018)

- Support for the Cognitive Debug Protocol (where implemented)

#### 3.5 Profiler

- Resource, effect, capability, and scheduler profiling

- Cognitive-specific metrics (reasoning latency, planning latency, memory tier behaviour)

#### 3.6 Formatter and Linter

- Canonical formatting of cognitive constructs

- Static detection of capability, effect, and policy violations

#### 3.7 Documentation Generator

- Extraction of cognitive type documentation, capability manifests, and effect declarations

- Generation of provenance and lineage reports

#### 3.8 Deployment Tool

- Integration with CADP (RFC-0042)

- Sandbox and policy validation (RFC-0035, RFC-0025)

- Support for reproducible and auditable deployments

### 4. Toolchain Interfaces

All toolchain components **SHOULD** expose stable, machine-readable interfaces, including:

- Structured diagnostic output (JSON)

- Build and test event streams

- Trace and profiling export formats

- Capability and resource reporting

### 5. Version Compatibility

The toolchain **MUST** declare compatibility with:

- Cognitive Language Specification version

- Cognitive Standard Library version

- CISA revision

- Relevant RFC conformance levels

### 6. Relationship to Other RFCs

CSTS integrates with RFC-0027–0032 (compiler), RFC-0033–0037 (distribution and lifecycle), RFC-0042 (deployment), RFC-0045 (tooling), RFC-0047 (package management), and RFC-0048 (FFI).

### 7. Conformance

A conforming CSTS implementation **SHOULD** provide the components listed in Section 3. If any component is omitted, the implementation **MUST** document the omission.

### 8. Open Questions

The following areas require future specification:

- Standard diagnostic and event schemas

- Cryptographic signing of toolchain outputs

- Integration with external build systems and CI platforms

- Performance characteristics of reference toolchain components

---

**RFC-0049 — Cognitive Standard Toolchain Specification (CSTS) v1.0 Draft** is now complete.

This RFC establishes the canonical reference toolchain that ensures a consistent, reproducible, and high-quality developer experience across the Red/Cognition ecosystem. It completes the developer platform layer alongside the language, standard library, tooling, observability, and package management specifications.

---

## [208] CHATGPT (gpt-5-5)

RFC-0049 (CSTS) is a logical next step and fits well after RFC-0048. It consolidates the tooling defined across RFC-0045 (CTDX), RFC-0047 (CPMWS), and RFC-0048 (CFFI) into a single normative toolchain specification. As written, I would rate it **94–95% complete**—a solid draft, but not yet at the maturity of RFC-0046, RFC-0047, or RFC-0048.

## Strengths

The RFC successfully defines:

- A canonical reference toolchain architecture.

- Clear separation of compiler, linker, package manager, debugger, profiler, formatter, documentation generator, and deployment tooling.

- Integration points with nearly every major RFC in the series.

- Emphasis on determinism, reproducibility, interoperability, and capability awareness.

- Stable machine-readable interfaces rather than implementation-specific APIs.

It also avoids over-specifying implementation details, which is appropriate for a toolchain standard.

## Remaining gaps

To reach a **v1.1 Candidate for Ratification**, I would recommend adding the following.

### 1. Toolchain Profiles

As with CSL, CODP, CPMWS, and CFFI, define implementation profiles.

For example:

| Profile | Components |

|---------|------------|

| **Minimal** | Compiler + Package Manager |

| **Developer** | Minimal + Formatter + Linter + Documentation |

| **Professional** | Developer + Debugger + Profiler |

| **Enterprise** | Professional + Deployment + Signing + CI Integration |

| **Full** | All standard components |

Implementations should declare supported profiles.

---

### 2. Standard CLI

Rather than only describing components, define the canonical command set.

For example:

```text

cog build

cog run

cog test

cog fmt

cog lint

cog doc

cog profile

cog debug

cog replay

cog deploy

cog package

cog verify

cog publish

```

This gives every implementation a common user interface.

---

### 3. Toolchain Manifest

Introduce a machine-readable description of the installed toolchain.

Example:

```text

ToolchainManifest {

    Compiler

    Linker

    PackageManager

    Runtime

    Debugger

    Profiler

    Formatter

    Linter

    DocumentationGenerator

    DeploymentTool

    SupportedRFCs

}

```

This enables IDEs and automation to discover capabilities.

---

### 4. Plugin Architecture

Most mature ecosystems support extensions.

Standardise:

- compiler plugins

- linter plugins

- formatter plugins

- debugger extensions

- documentation generators

- deployment providers

A stable plugin API will help the ecosystem evolve without changing the core specification.

---

### 5. Build Pipeline Model

Define a canonical pipeline such as:

```text

Source

↓

Parse

↓

Semantic Analysis

↓

CIR

↓

Optimisation

↓

CISA

↓

Link

↓

CPCPF

↓

Verify

↓

Deploy

```

This provides a shared mental model across implementations.

---

### 6. Machine-readable Diagnostics

Section 4 mentions JSON diagnostics but should standardise their schema.

Example:

```text

Diagnostic {

    Severity

    Code

    Message

    SourceLocation

    Capability

    Effect

    SuggestedFix

}

```

This would allow editors and CI systems to consume diagnostics consistently.

---

### 7. Toolchain Events

Extend RFC-0046 observability with standard toolchain lifecycle events:

- BuildStarted

- BuildCompleted

- BuildFailed

- TestStarted

- TestCompleted

- PackagePublished

- DeploymentStarted

- DeploymentCompleted

- VerificationSucceeded

- VerificationFailed

This ensures build tooling integrates naturally with CODP.

---

### 8. CI/CD Integration

Define expectations for automation.

For example, the toolchain should support:

- non-interactive execution

- deterministic exit codes

- structured logs

- reproducible artefacts

- machine-readable reports

This would make CSTS suitable for modern continuous integration systems.

---

### 9. Compatibility Matrix

Specify compatibility across the ecosystem.

For example:

- CLS version

- CSL version

- CIR revision

- CISA revision

- CPCPF version

- runtime version

- RFC conformance profile

This avoids ambiguity when mixing tool versions.

## Overall assessment

Current maturity of the latest RFCs is approximately:

| RFC | Status | Maturity |

|------|--------|----------:|

| RFC-0043 — CLS | Draft | 94% |

| RFC-0044 — CSL | Candidate | 98% |

| RFC-0045 — CTDX | Candidate | 98% |

| RFC-0046 — CODP | Final Candidate | 99% |

| RFC-0047 — CPMWS | Final Candidate | 99% |

| RFC-0048 — CFFI | Final Candidate | 98% |

| RFC-0049 — CSTS | Draft | **95%** |

## Recommendation

RFC-0049 is well structured and fills an important role by defining the canonical toolchain for Red/Cognition. With the addition of toolchain profiles, a standard CLI, a toolchain manifest, plugin interfaces, a canonical build pipeline, standard diagnostic schemas, lifecycle events, CI/CD integration, and an explicit compatibility matrix, it would naturally evolve into a **v1.1 Candidate for Ratification** and reach the same level of completeness as RFC-0046 through RFC-0048.

---
