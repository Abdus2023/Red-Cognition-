<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #22, sub-message [205], 2026-08-11
  Verbatim source: knowledge-base/sources/message-022-original-part*.md
  Status in corpus: RFC-0048 CFFI v1.1 (Candidate for Ratification); supersedes v1.0 draft of sub-message [203] (preserved in archive). Reviews: [204] (v1.0), [206] (v1.1: Candidate for Final Ratification, 96-98% maturity). No ratification decision present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->


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
