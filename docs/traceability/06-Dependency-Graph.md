# Dependency Graph — Phase 4.5

> Master Source: `docs/TRACEABILITY-ARCHIVE.md` §4.5. Both conceptual (RFC-level) and technical (file-level) graphs. Arrows read `A → B` = `A depends on B` or `A is upstream of B` where noted.

## 6.1 Conceptual Dependency (RFC-level)

```mermaid
flowchart TD
    RFC002["RFC-002 Red Core<br/>(Implemented)"]
    RFC001["RFC-001 Text Interfaces"]
    RFC003["RFC-003 Agent Operating Environment<br/>(ARS triad)"]
    RFC004["RFC-004 CogOS<br/>(Kernel, Goals, Knowledge FS)"]
    RFC005["RFC-005 Red/Cognition Language<br/>(16 types, contracts)"]
    RFC006["RFC-006 Compiler + CIR<br/>(4 graphs, 4 passes)"]
    RFC007["RFC-007 CVM + CISA v0.1<br/>(30 ops, heap, attention)"]
    RFC008["RFC-008 Red 2.0<br/>(hardware→intelligence)"]
    RFC009["RFC-009 Red Deep Spec<br/>(ground truth)"]
    RFC010["RFC-010 Analysis Suite<br/>(meta, external grounding)"]

    RFC009 -. verifies .-> RFC002

    RFC001 --> RFC002
    RFC003 --> RFC001
    RFC003 --> RFC002
    RFC004 --> RFC003
    RFC005 --> RFC004
    RFC006 --> RFC005
    RFC007 --> RFC006
    RFC008 --> RFC004
    RFC008 --> RFC007
    RFC008 --> RFC005

    RFC010 -. grounds .-> RFC003
    RFC010 -. grounds .-> RFC004
    RFC010 -. grounds .-> RFC005
    RFC010 -. grounds .-> RFC006
    RFC010 -. grounds .-> RFC007

    style RFC002 fill:#c6f6d5,stroke:#22543d
    style RFC009 fill:#c6f6d5,stroke:#22543d
    style RFC010 fill:#fefcbf,stroke:#744210
    style RFC006 fill:#fed7d7,stroke:#742a2a
```

**Cycle analysis:** Acyclic. Centrality: **RFC-005** (Language) — bridges CogOS and Compiler/CVM. **Cut vertex: RFC-006 (Compiler)** — without it, CVM has no CIR to execute; roadmap critical path transits RFC-006. **RFC-010** is meta-grounding, not on critical path.

**Textual edge list (for auditability, same as master):**

```
RFC-002 Red Core (Implemented)
      │
      ├─► RFC-001 Text Interfaces (lifecycle)
      │       │
      │       └─► RFC-003 Agent Operating Environment (ARS triad)
      │               │
      │               ├─► RFC-004 CogOS (kernel, goals, knowledge FS, uncertainty) ──┐
      │               │       │                                                      │
      │               │       └─► RFC-005 Red/Cognition Language (16 types, contracts) │
      │               │               │                                              │
      │               │               └─► RFC-006 Compiler + CIR (4 graphs, 4 passes)  │
      │               │                       │                                    │
      │               │                       └─► RFC-007 CVM + CISA (30 ops, heap, attention) │
      │               │                               │                            │
      │               └───────────────────────────────┴─► RFC-008 Red 2.0 (unified hardware→intelligence)
      │                                                       │
      └───────────────────────────────────────────────────────┘
                                                              │
RFC-009 Red Deep Spec (ground truth, verifies RFC-002) ──────┘

RFC-010 Analysis Suite (meta, grounds RFC-003→007 externally)
```

## 6.2 Technical Artifact Dependency (file/component-level)

```mermaid
flowchart TD
    redR["red.r<br/>toolchain entry, CLI flags"]
    compilerR["compiler.r<br/>125703 B"]
    lexerR["lexer.r<br/>26389 B"]
    sysCompiler["system/compiler.r<br/>comp-dialect, Red/System compiler"]
    emitter["system/emitter.r"]
    formats["system/formats/{PE,ELF,Mach-O}.r"]
    linker["system/linker.r"]
    runtime["runtime/<br/>libRedRT, hybrid"]
    bridges["bridges/<br/>java/android"]
    wiki["docs/wiki/*.md<br/>20 files, 8177 lines"]
    archive["docs/TRACEABILITY-ARCHIVE.md<br/>776 lines"]
    trace["docs/traceability/*<br/>9 split files"]

    redR --> sysCompiler
    compilerR --> sysCompiler
    lexerR --> sysCompiler
    sysCompiler --> emitter
    emitter --> formats
    formats --> linker
    linker --> runtime
    runtime --> bridges

    runtime -. documents .-> wiki
    wiki -. audits .-> archive
    archive -. splits .-> trace

    style runtime fill:#c6f6d5,stroke:#22543d
    style archive fill:#bee3f8,stroke:#2a4365
```

**Cognitive extension dependencies (proposed, no files yet — derived from RFC-005→007):**

```
red/cognition/types/ (goal! plan! belief! ... 16 types) ─┐
red/cognition/dialects/ (reason, plan, observe, remember) ├──► red/cognition/compiler/ (Intent/Effect/Capability/Planning/Optimisation)
red/cognition/contracts/ (Cognitive Pipe, Capability Binding) ─┘         │
                                                                           ▼
                                                                  CIR (cir.r) — Intent Graph → Task DAG → Capability Graph → Exec Graph
                                                                           │
cvm/ (cisa.r, registers.r, heap.r, attention.r, provenance.r) ◄────────────┘
      │
cogos/ (kernel.r, scheduler.r, memory.r, policy.r, model.r) ◄──────────────┘
```

**External ecosystem deps (open, OP-01):** `MCP gateway` · `vector DB` · `LLM provider SDK` · `Graphiti/Zep` · `libRedRT-exports.r`

## 6.3 Dependency Strength & Risk

| Edge | Dependency Strength | Failure If Upstream Missing | Mitigation |
|------|----------------------|-----------------------------|------------|
| RFC-002 → RFC-003..008 (Red Core → all cognitive RFCs) | **Strong / Blocking** | Entire cognitive stack has no substrate | Phases -1/0 already verify Red Core at `9b5b15a` |
| RFC-005 → RFC-006 (Language → Compiler) | Strong | CIR emission undefined without types | Phase 1 type MVP before compiler work |
| RFC-006 → RFC-007 (Compiler → CVM) | **Critical path** | CVM has no verifiable artifact to execute | Gate A: DAG must be valid before CVM work starts |
| RFC-010 → RFC-003..007 (Analyses ground RFCs) | Weak (justification, not implementation) | Architecture ungrounded but implementable | Already captured in docs/wiki analyses |
| Red Core file deps `red.r→compiler.r→system/*→runtime` | Strong | Toolchain broken | CI matrix (`MSDOS`..`Android-x86`) guards |

*Provenance: conceptual edges derived from §02-RFC-Origin-Map conversation→RFC chain; technical edges verified against actual repo `ls`/`compiler.r` size/`system/formats/` inventory.*
