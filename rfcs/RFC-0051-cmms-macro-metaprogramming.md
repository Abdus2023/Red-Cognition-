<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #23, sub-message [227], 2026-08-11
  Verbatim source: knowledge-base/sources/message-023-original-part*.md
  Status in corpus: RFC-0051 CMMS v1.0 (Draft). Review [228]: "Draft → Candidate for Ratification Recommended" / "APPROVED FOR RATIFICATION PATH" with four additions (macro resource limits, trust model, package metadata, debugging/provenance tooling); no v1.1 or ratification present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->


**RFC-0051 — Cognitive Macro and Metaprogramming System (CMMS) v1.0 Draft**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0050 Red/Cognition v1.0 Architecture and Conformance Specification v1.2 (Candidate)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Macro and Metaprogramming System (CMMS)** for Red/Cognition.

While the Cognitive Language Specification (RFC-0043) and the Cognitive Standard Library (RFC-0044) define the core language and its APIs, CMMS specifies a powerful, hygienic, and capability-aware macro system that enables safe compile-time computation, AST/CIR transformation, cognitive dialect extension, and verified program generation.

CMMS is not a traditional syntactic macro system. It is a **cognitive-aware program transformation framework** that integrates with the Cognitive Intermediate Representation (CIR), the Cognitive Instruction Set Architecture (CISA), and the verification infrastructure of the platform.

### 2. Design Principles

CMMS follows these principles:

- **Hygienic Expansion** — Macros must prevent accidental capture and ensure predictable scoping.

- **Typed Transformation** — Macros operate on typed cognitive structures, not raw syntax.

- **Capability Control** — Compile-time execution is subject to explicit capability restrictions.

- **Deterministic Expansion** — Macro expansion must be reproducible given the same inputs and environment.

- **Traceable Expansion** — Every macro expansion must produce provenance records.

- **Verified Transformations** — Complex macros may produce optimization certificates (RFC-0032).

- **Provider Neutrality** — The macro system must not embed assumptions about specific reasoning mechanisms.

### 3. Macro Execution Model

Cognitive macros execute in a restricted compile-time environment. The expansion pipeline is:

```

Cognitive Source Code

   ↓

Macro Expansion Phase

   ↓

Expanded Cognitive AST

   ↓

Semantic Analysis

   ↓

CIR Generation

   ↓

Optimization + Verification

   ↓

CISA

```

Macro execution **MUST** follow:

```

Macro Request

   ↓

Capability Check

   ↓

Policy Validation

   ↓

Expansion

   ↓

Trace Recording

```

### 4. Hygienic Expansion System

Macros **MUST** be hygienic. The compiler **MUST** manage identifier namespaces during expansion to prevent accidental capture.

Generated identifiers **MUST** use compiler-controlled namespaces that are invisible to user code unless explicitly exported.

### 5. Cognitive Macro Types

CMMS defines three classes of macros:

#### 5.1 Syntax Macros

Extend the language surface through new syntactic forms.

Example:

```red

define-goal improve-model [

    objective: accuracy

    constraint: latency < 50ms

]

```

#### 5.2 Semantic Macros

Operate on typed cognitive structures to generate or transform goals, plans, beliefs, or capabilities.

Example:

```red

optimize-agent-training goal

```

#### 5.3 Cognitive Macros

Specialized macros for high-level cognitive constructs (goals, agents, workflows, policies, simulations).

Example:

```red

agent "researcher" [

    goal "summarize papers"

    memory semantic

    capability web-search

]

```

### 6. Compile-Time Capability Model

Compile-time macro execution **MUST** be capability-gated.

A macro **MUST NOT**:

- Access the filesystem without explicit capability

- Perform network operations without explicit capability

- Execute arbitrary external code

- Modify external state

All capability usage during macro expansion **MUST** be recorded in the expansion trace.

### 7. Macro Provenance and Traceability

Every macro expansion **MUST** produce a `MacroExpansionRecord`:

```

MacroExpansionRecord {

    MacroName,

    Version,

    InputHash,

    OutputHash,

    ExpansionTrace,

    CompilerVersion,

    CapabilityUsage

}

```

This record **MUST** be included in CPCPF artifacts (RFC-0033) and participate in the global event log (RFC-0018).

### 8. CIR-Level Transformations

Advanced macros **MAY** operate directly on the Cognitive Intermediate Representation (CIR) defined in RFC-0028.

COIL transformations (RFC-0031) **MUST** be expressible using CIR-level operations when operating below the AST layer.

### 9. Verification Requirements

Complex macros that perform significant transformations **SHOULD** produce optimization certificates (RFC-0032) demonstrating that the transformation preserves:

- Effect ordering

- Goal satisfaction semantics

- Capability requirements

- Determinism and replay equivalence

### 10. Toolchain Integration

The macro system **MUST** integrate with the standard toolchain (RFC-0049). The following commands **SHOULD** be supported:

```

cog macro list

cog macro expand

cog macro trace

cog macro verify

cog macro inspect

```

### 11. Conformance Profiles

CMMS defines the following macro capability profiles:

| Profile     | Capabilities                                      |

|-------------|---------------------------------------------------|

| **Basic**   | Syntax macros                                     |

| **Developer** | Typed semantic macros                           |

| **Cognitive** | Goal, belief, plan, agent, skill macros         |

| **Verified**  | Proof-producing transformations                 |

### 12. Relationship to Existing RFCs

CMMS integrates with:

- RFC-0001 — Cognitive Type System

- RFC-0002 — Effect Ordering Model

- RFC-0006 — Capability Model

- RFC-0028 — Cognitive Intermediate Representation

- RFC-0030 — Optimization Pass Framework

- RFC-0031 — COIL

- RFC-0032 — COVF

- RFC-0043 — Cognitive Language Specification

### 13. Open Questions

The following areas require future specification:

- Full formal hygiene rules and capture prevention algorithm

- Compile-time evaluation limits and resource accounting

- Generic programming and compile-time type computation

- Language evolution process for new macro primitives

- Integration with just-in-time macro expansion at runtime

---

**RFC-0051 — Cognitive Macro and Metaprogramming System (CMMS) v1.0 Draft** is now complete.

This RFC establishes the metaprogramming foundation that enables safe, hygienic, capability-controlled, and verifiable program transformation in Red/Cognition. It bridges the gap between the language, the compiler, and the verified execution model.
