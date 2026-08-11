<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #22, sub-message [211], 2026-08-11
  Verbatim source: knowledge-base/sources/message-022-original-part*.md
  Status in corpus: RFC-0049 CSTS v1.2; RATIFIED per user ratification record [215]; supersedes v1.0 ([207]) and v1.1 ([209]) drafts (preserved in archive); [213] is an identical re-send of [211] (D-72). Reviews: [208], [210], [212], [214].
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->


**RFC-0049 — Cognitive Standard Toolchain Specification (CSTS) v1.2**

**Version:** 1.2  

**Status:** Candidate for Final Ratification  

**Parent:** RFC-0048 Cognitive Foreign Function Interface (CFFI) v1.1 (Candidate)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Standard Toolchain Specification (CSTS)** for Red/Cognition.

CSTS specifies the canonical reference toolchain that every conforming Red/Cognition implementation **SHOULD** provide. This includes the compiler, linker, package manager, debugger, profiler, formatter, linter, documentation generator, and deployment tools, along with their expected interfaces and behaviour.

The goal of CSTS is to ensure a consistent, reproducible, and high-quality developer experience across the Red/Cognition ecosystem.

### 2. Design Principles

CSTS follows these principles:

- **Determinism** — All toolchain components must support deterministic and reproducible operation.

- **Capability Awareness** — Toolchain operations must respect capability and policy constraints.

- **Traceability** — Toolchain actions that affect builds or deployments must be recorded.

- **Provider Neutrality** — The specification must remain independent of specific compiler or runtime implementations.

- **Interoperability** — Toolchain components must interoperate through stable, documented interfaces.

### 3. Toolchain Profiles

CSTS defines the following implementation profiles:

| Profile       | Components                                      | Typical Use Case                  |

|---------------|--------------------------------------------------|-----------------------------------|

| **Minimal**   | Compiler + Package Manager                       | Embedded or minimal environments  |

| **Developer** | Minimal + Formatter + Linter + Documentation     | Everyday development              |

| **Professional** | Developer + Debugger + Profiler               | Professional development          |

| **Enterprise**| Professional + Deployment + Signing + CI         | Regulated or large-scale environments |

| **Full**      | All standard components                          | Complete cognitive platforms      |

Implementations **MUST** declare their supported profile(s).

### 4. Toolchain Capability Declaration

The `ToolchainManifest` **SHOULD** advertise supported capabilities, for example:

```

Capabilities {

    IncrementalCompilation,

    CrossCompilation,

    ReplayDebugging,

    DistributedBuilds,

    ProofVerification,

    WASMBackend

}

```

This allows IDEs and automation to negotiate available functionality dynamically.

### 5. Standard CLI

A conforming implementation **SHOULD** provide a standard command-line interface, including at least:

```

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

### 6. Toolchain Manifest

A conforming implementation **SHOULD** expose a machine-readable `ToolchainManifest` describing the installed components and their capabilities.

### 7. Plugin Architecture

CSTS **SHOULD** define stable plugin interfaces for:

- Compiler plugins

- Linter and formatter plugins

- Debugger extensions

- Documentation generators

- Deployment providers

Plugins **MUST** be discoverable and versioned.

### 8. Canonical Build Pipeline

CSTS defines the following normative build pipeline:

```

Source

   ↓

Parse

   ↓

Semantic Analysis

   ↓

CIR Generation

   ↓

Optimisation

   ↓

CISA Generation

   ↓

Link

   ↓

CPCPF Packaging

   ↓

Verification

   ↓

Deploy

```

Implementations **MUST** support this pipeline or document equivalent behaviour.

### 9. Compiler Backend Enumeration

The toolchain **SHOULD** support at minimum the following standard backend targets:

- CVM

- Native

- WebAssembly

- LLVM (optional)

- Embedded runtime

The command `cog build --target` **SHOULD** accept these targets.

### 10. Incremental Build Model

The toolchain **SHOULD** support incremental compilation, including:

- Incremental parsing

- Incremental semantic analysis

- Cached optimisation results

- Cached proof certificates

- Distributed compilation (where applicable)

### 11. Machine-Readable Diagnostics

Toolchain components **SHOULD** emit structured diagnostics in a standard schema:

```

Diagnostic {

    Severity,

    Code,

    Message,

    SourceLocation,

    Capability,

    Effect,

    SuggestedFix

}

```

### 12. Toolchain Lifecycle Events

Toolchain operations **SHOULD** emit standard lifecycle events (integrated with RFC-0046):

- `BuildStarted`, `BuildCompleted`, `BuildFailed`

- `TestStarted`, `TestCompleted`

- `PackagePublished`

- `DeploymentStarted`, `DeploymentCompleted`

- `VerificationSucceeded`, `VerificationFailed`

### 13. CI/CD Integration

The toolchain **MUST** support non-interactive execution with:

- Deterministic exit codes

- Structured logs and reports

- Reproducible artefacts

- Machine-readable output

### 14. Compatibility Matrix

The toolchain **MUST** declare compatibility with:

- Cognitive Language Specification version

- Cognitive Standard Library version

- CIR revision

- CISA revision

- CPCPF version

- Runtime version

- Relevant RFC conformance profiles

### 15. Toolchain Provenance

Emitted artefacts **SHOULD** carry provenance metadata linking:

- Compiler version

- Plugin versions

- Package manager version

- Build pipeline revision

- RFC compatibility profile

### 16. Relationship to Other RFCs

CSTS integrates with RFC-0027–0032 (compiler), RFC-0033–0037 (distribution), RFC-0042 (deployment), RFC-0045 (tooling), RFC-0047 (package management), and RFC-0048 (FFI).

### 17. Conformance

A conforming CSTS implementation **SHOULD** provide the components listed in Section 3. If any component is omitted, the implementation **MUST** document the omission.

### 18. Open Questions

The following areas require future specification:

- Standard diagnostic and event schemas

- Cryptographic signing of toolchain outputs

- Integration with external build systems and CI platforms

- Performance characteristics of reference toolchain components

---

**RFC-0049 — Cognitive Standard Toolchain Specification (CSTS) v1.2** is now ready for **Final Ratification Review**.

This version incorporates toolchain profiles, capability declaration, standard CLI, toolchain manifest, plugin architecture, canonical build pipeline, compiler backend enumeration, incremental build model, machine-readable diagnostics, lifecycle events, CI/CD integration, compatibility matrix, and toolchain provenance, bringing it in line with the precision of the strongest RFCs in the series.
