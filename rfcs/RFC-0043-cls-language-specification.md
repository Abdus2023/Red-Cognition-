<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #21, sub-message [181], 2026-08-11
  Verbatim source: knowledge-base/sources/message-021-original-part*.md
  Status in corpus: RFC-0043 CLS v1.0 (Draft). Review [182] recommends normative additions for a future v1.1 (module system, name resolution, evaluation model, determinism levels, pattern matching, contracts, effect/capability annotations, standard dialect interfaces); no v1.1 and no ratification present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->


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
