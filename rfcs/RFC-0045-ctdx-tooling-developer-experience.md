<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #21, sub-message [189], 2026-08-11
  Verbatim source: knowledge-base/sources/message-021-original-part*.md
  Status in corpus: RFC-0045 CTDX v1.1 (Candidate for Ratification); supersedes v1.0 draft of sub-message [187] (preserved in archive). Review [190]: "Ratification Recommended" - no ratification decision present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->


**RFC-0045 — Cognitive Tooling and Developer Experience (CTDX) v1.1**

**Version:** 1.1  

**Status:** Candidate for Ratification  

**Parent:** RFC-0044 Cognitive Standard Library (CSL) v1.1 (Candidate)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Tooling and Developer Experience (CTDX)** requirements for Red/Cognition.

While RFC-0043 (Cognitive Language Specification) and RFC-0044 (Cognitive Standard Library) define the language and its APIs, CTDX specifies the tooling, editors, debuggers, profilers, formatters, language servers, testing frameworks, and documentation systems that developers and cognitive agents will use to build, debug, test, and maintain Red/Cognition programs.

The goal of CTDX is to ensure that the developer experience remains first-class, consistent, and aligned with the determinism, traceability, capability awareness, and replay requirements established throughout the Red/Cognition architecture.

### 2. Design Principles

CTDX follows these principles:

- **First-Class Tooling** — Tooling must be treated as a core part of the language ecosystem.

- **Determinism Support** — All tooling must support deterministic builds, execution, and replay.

- **Capability Awareness** — Editors and debuggers must understand and surface capability requirements.

- **Provider Neutrality** — Tooling must not embed assumptions about specific reasoning or planning implementations.

- **Traceability** — All tooling must preserve and expose provenance, effects, and execution traces.

- **Accessibility** — Tooling must support both human developers and autonomous cognitive agents.

### 3. Core Tooling Components

Every conforming Red/Cognition implementation **SHOULD** provide or support the following components:

#### 3.1 Language Server Protocol (LSP) Implementation

- Semantic highlighting for cognitive constructs

- Go-to-definition, find-references, and rename support

- Hover documentation for cognitive types and operations

- Inline diagnostics for capability, effect, and resource violations

#### 3.2 Debugger

- Breakpoints on cognitive constructs

- Inspection of `ExecutionContext`, `AgentState`, and memory tiers

- Step-through of the Cognitive Execution Cycle (CEC-1)

- Trace exploration and causal graph visualization

- Checkpoint creation, inspection, and restoration

#### 3.3 Profiler

- Per-instruction and per-skill resource accounting

- Effect production profiling

- Capability usage heatmaps

- Memory tier access patterns

- Scheduler decision visualization

- Cognitive-specific metrics (reasoning latency, planning latency, capability lookup cost, memory tier hit rates, scheduler utilisation, replay divergence detection)

#### 3.4 Formatter and Linter

- Canonical formatting for cognitive blocks and dialects

- Enforcement of naming conventions

- Static detection of capability and effect violations

#### 3.5 Testing Framework

- Deterministic unit and integration testing

- Replay-based regression testing

- Capability and policy violation testing

- Goal satisfaction and plan coverage metrics

- Property-based testing for cognitive invariants

#### 3.6 Documentation Generator

- Automatic extraction of cognitive type documentation

- Generation of capability manifests and effect declarations

- Visualization of goal/plan graphs and effect dependencies

- Integration with CPCPF metadata (RFC-0033)

### 4. Build System and Package Tooling

A conforming implementation **SHOULD** provide a standard command-line toolchain with at least the following commands:

```

cog build

cog test

cog run

cog fmt

cog lint

cog doc

cog publish

cog verify

cog replay

```

### 5. Workspace Model

A standard **Workspace** specification **SHOULD** be provided that defines:

- Multiple packages within a single project

- Shared dependencies

- Compiler and testing configuration

- Deployment targets

- Reproducible lockfiles

### 6. Debugger Protocol

In addition to LSP, a **Cognitive Debug Protocol (CDP)** **MAY** be implemented. It **SHOULD** support:

- Breakpoint management

- Execution control (step, continue, pause)

- Event streaming

- Checkpoint inspection

- Distributed debugging

- Replay debugging

### 7. Visualisation Standards

Tooling **SHOULD** support standard visualisations for:

- Goal graphs

- Plan graphs

- Belief dependency graphs

- Effect graphs

- Event DAGs

- Capability delegation graphs

- Federation topology

### 8. AI-Assisted Development

Tooling **SHOULD** expose interfaces for AI assistance, including:

- Code completion

- Proof assistance

- Optimisation suggestions

- Capability analysis

- Automatic documentation

- Test generation

- Replay analysis

### 9. Conformance Test Suite

A standard conformance test suite **SHOULD** be provided covering:

- Formatter stability and determinism

- LSP behaviour

- Debugger protocol compliance

- Replay correctness

- Profiler accuracy

- Documentation generation

### 10. Reference Toolchain (Non-Normative)

A recommended reference toolchain stack is:

```

Compiler

   ↓

Language Server

   ↓

Formatter + Linter

   ↓

Debugger + Profiler

   ↓

Documentation Generator

   ↓

Package Manager

   ↓

Deployment Tool

```

### 11. Conformance

A conforming CTDX implementation **SHOULD** provide the components listed in Sections 3–9. If any component is omitted, the implementation **MUST** document the omission.

### 12. Open Questions

The following areas require future specification:

- Standardised debugger protocol beyond LSP

- Cognitive-specific IDE plugin APIs

- Performance characteristics of tooling components

- Integration with external cognitive development environments

---

**RFC-0045 — Cognitive Tooling and Developer Experience (CTDX) v1.1** is now ready for **Final Ratification Review**.

This version incorporates build system tooling, workspace model, debugger protocol, visualisation standards, AI-assisted development interfaces, conformance testing, and performance diagnostics, bringing it in line with mature language ecosystems while remaining aligned with the Red/Cognition architecture.
