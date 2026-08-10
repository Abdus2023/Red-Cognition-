# RFC Origin Map — Phase 2 (Conversation→RFC Traceability) + Phase 4.1

> Master Source: `docs/TRACEABILITY-ARCHIVE.md` §Phase 2 & §4.1. Every row carries **Origin | Why Created | Influencing Discussions | Final RFC | Component | Requirement | Status**.

## Conversation→RFC→Component→Requirement Mapping

| # | Conversation Idea (Origin) | Design Decision | RFC Specification (Stable ID + proposed #) | Architecture Component | Implementation Requirement | Status |
|---|----------------------------------------------------------|-----------------|-----------------------------------------------------|------------------------|----------------------------|--------|
| R1 | “CLI operates on Stateless Request-Response” (MSG-01) | Distinguish stateless vs stateful | **RFC-TEXT-INT-001** `TEXT-INT-001` — § Lifecycle of CLI Command | Text Interface Layer (CLI/Prompt/REPL) | Preserve REPL `READ→EVAL→PRINT→LOOP` | Implemented |
| R2 | “REPL is continuous, stateful sandbox” (MSG-01) | REPL as precedent for persistence | Same | REPL Engine (`compiler.r` + `runtime/`) | Verify persistent context binding per `RED-SPEC-015` | Implemented |
| R3 | “Homoiconic: plan is data structure” (MSG-01) | Elevate block to executable goal | **RFC-RED-COG-001** `RED-COG-001` § New Primitive Types | Red Language Core → Red/Cognition Types | Implement `goal! plan! belief!` with metadata | Proposed |
| R4 | Dialect IS tool interface (MSG-01) | Eliminate JSON serialization | **RFC-RED-COG-001** § Skills + Capability Execution | Dialect Engine (Parse dialect) | Dialect enforces `capability!` policy checks | Proposed |
| R5 | Ecosystem Problem (MSG-01 Analysis) | Hybrid bridging not isolation | **RFC-RED-COG-ANALYSIS-001** § IX | FFI + MCP Gateway | MCP gateway, DID identity, vector DB connectors | Open Question |
| R6 | ARS triad + loop (MSG-02) | ARS as event-driven OS | **RFC-AGENT-ENV-001** `AGENT-ENV-001` | Agent Runtime Shell (ARS) | Event queue multiplex → Scheduler | Proposed |
| R7 | Unix→Agent table (MSG-02) | Reframe OS primitives | **RFC-AGENT-ENV-001** Table + `AGENT-ENV-ANALYSIS-001` AgenticOS table | Cognitive Runtime Abstraction | Intent ABI instead of POSIX fork/pipe | Proposed |
| R8 | 11-stage pipeline →14 (MSG-02 Analysis) | Add 3 auxiliary gates | **RFC-AGENT-ENV-ANALYSIS-001** § V | Cognitive Pipeline Engine | Promotion/confidence/DID verification | Proposed |
| R9 | Memory hierarchy correction (MSG-02 Analysis) | 4 parallel stores | **RFC-AGENT-ENV-ANALYSIS-001** § II | Memory Manager (4-store) | Hybrid store per CoALA; MemGPT paging | Proposed |
| R10 | Tool invocation + Receipt (MSG-02) | Policy Engine critical | **RFC-COGOS-001** + **RFC-CVM-001** Execution | Capability & Policy Manager | `Goal→Resolver→Policy→Permission→Binding→Receipt(HMAC)` | Proposed |
| R11 | Evolutionary stack (MSG-02) | Discrete phase changes | **RFC-AGENT-ENV-ANALYSIS-001** § VI Table | Historical Reference | Initiative→identity transition | Proposed |
| R12 | CogOS goal scheduler inversion (MSG-03) | Manage attention/budget not CPU | **RFC-COGOS-001** § Kernel | Goal Scheduler | Priority+dependency+budget; cooperative yield | Proposed |
| R13 | New primitives observe→sleep/wake (MSG-03) | First-class runtime ops | **RFC-COGOS-001** → **RFC-CVM-001** CISA | Cognitive Kernel API | Map to CISA opcodes in `runtime/` | Proposed |
| R14 | Cognitive pipes (MSG-03) | Semantic not byte streams | **RFC-COGOS-001** § Pipes | Knowledge Pipeline | Typed pipeline `Observe→Reflect` | Proposed |
| R15 | Knowledge graph as filesystem (MSG-04) | `Knowledge/{Facts...Evidence}` | **RFC-COGOS-FRAMEWORK-001** + Analysis § II hybrid+temporal | Memory Substrate (Graph DB) | Graphiti bi-temporal + hybrid router | Proposed |
| R16 | Time & Uncertainty first-class (MSG-04) | Past→Plan; confidence 0.42 | **RFC-COGOS-FRAMEWORK-001** + Analysis § III 4-dim UQ | Uncertainty Manager | 4-dim UQ + calibration | Proposed |
| R17 | Reflection dual-loop (MSG-04 Analysis) | Self + critic agent | **RFC-COGOS-FRAMEWORK-ANALYSIS-001** § IV | Reflection Engine | Fast self + slow adversarial critique | Proposed |
| R18 | Skills replace commands (MSG-04) | Internal DAG composition | **RFC-COGOS-FRAMEWORK-001** § Skills | Skill Registry | Capability-gated skill with history | Proposed |
| R19 | Universal Runtime 10-layer (MSG-04) | Microkernel analogy | **RFC-COGOS-FRAMEWORK-001** | Layered CogOS Stack | LLM reasoning + runtime execution split | Proposed |
| R20 | 16 cognitive types (MSG-05 Analysis) | Metadata-enforced types | **RFC-RED-COG-001** + **RFC-RED-COG-ANALYSIS-001** § VIII | Red/Cognition Type System | `make belief! [content confidence source]` | Proposed |
| R21 | Inter-layer contracts (MSG-05 Analysis) | Boundary semantics | **RFC-RED-COG-ANALYSIS-001** § IX | Compiler/Runtime Boundary | Metadata shedding/acquisition at boundaries | Proposed |
| R22 | Repository Assistant complete example (MSG-05) | Human+machine+inspectable | **RFC-RED-COG-001** → Analysis § X annotated | Conformance Test | Golden-file parse/verify/execute | Proposed |
| R23 | CIR 6-stage (MSG-06) | Lower to reasoning structures | **RFC-RED-COMPILER-001** CIR | CIR Emitter (4 graphs) | `Goal→Intent→Task→Capability→Execution` | Proposed |
| R24 | DAG plans + parallel 1.8–3.7× (MSG-06 Analysis) | Static parallelisation | **RFC-RED-COMPILER-ANALYSIS-001** § III | Planning Analysis Pass | DAG acyclicity + speedup | Proposed |
| R25 | Intent optimisation 6 passes + PGO (MSG-06) | Multi-objective | **RFC-RED-COMPILER-001** § Optimisation | Intent Optimiser | Goal simplification, plan fusion, speculative | Proposed |
| R26 | Planner as compiler pass (MSG-06) | Macro-expansion analog | **RFC-RED-COMPILER-001** § Planner | Planning Analysis | `goal generate-report` →5-node DAG | Proposed |
| R27 | Policies become types (MSG-06) | Compile-time rejection | **RFC-RED-COMPILER-001** + Policy-as-Type proof | Capability Analysis (RHTT) | Proof obligation for `dangerous` | Proposed |
| R28 | Cognitive effects (MSG-06) | Behavioural envelope | **RFC-RED-COMPILER-001** § Effects | Effect Inference Pass | `effects [observe remember reason]` | Proposed |
| R29 | Goal scheduler + self-modifying plans (MSG-06) | Scheduler as language feature | **RFC-RED-COMPILER-001** | Runtime Scheduler + Memory | Priority tuple + plan rewrite→reflect→store | Proposed |
| R30 | Multi-agent `agent planner/reviewer` (MSG-06) | Objects as agents | **RFC-RED-COMPILER-001** § Multi-Agent | Agent Runtime | `SPAWN/MESSAGE/SYNCHRONISE/MERGE` | Proposed |
| R31 | CISA 5 cat →30 ops (MSG-07) | Semantic ISA | **RFC-CVM-001** → **RFC-CVM-ANALYSIS § IX** | CVM ISA | `OBSERVE/RECALL/PLAN/SELECT/EXECUTE/VERIFY/REFLECT`+ | Proposed |
| R32 | Cognitive registers (MSG-07) | Logical registers | **RFC-CVM-001** § Register File | CVM Register File | Goal/Plan/WM/Attention/... | Proposed |
| R33 | Semantic addressing + heap (MSG-07) | Associative not positional | **RFC-CVM-001** + Analysis § III | Cognitive Heap | Semantic routing allocation | Proposed |
| R34 | Attention GWT spotlight (MSG-07 Analysis) | Anti-stagnation | **RFC-CVM-ANALYSIS-001** § II + IX | Attention Manager | `ATTEND/COMPETE/BROADCAST/SUPPRESS` | Proposed |
| R35 | Provenance + reflection-as-GC (MSG-07) | Evidence chain + curation | **RFC-CVM-001** | Memory Governance | Chain `Sensor→Action` + GC ladder | Proposed |
| R36 | Toolchain `Source→CIR→CVM→OS` + 3 compilers (MSG-07/08) | Intelligence as compilation target | **RFC-CVM-001** → **RFC-RED-20-001** | Red 2.0 Compiler | Unified pipeline `SOURCE→...→CIR→(Red IR/WASM)` | Proposed |
| R37 | Intent contracts (MSG-08) | `purpose/quality/deadline/budget` | **RFC-RED-20-001** § Contracts | Intent Type System | Goal contract facets verification | Proposed |
| R38 | Mnemonic sovereignty (MSG-07 Analysis) | Write-gate + verified deletion | **RFC-CVM-ANALYSIS-001** § IV–V | Memory Security | 9 primitives audit | Proposed |
| R39 | Collective false memory (MSG-07 Analysis) | Belief coherence protocol | **RFC-CVM-ANALYSIS-001** § VIII | Multi-Agent Coherence | `SYNCHRONISE/MERGE` arbitration | Open Question |
| R40 | 40+ datatypes + lexer v2 + hybrid runtime (MSG-09) | Ground truth | **RFC-RED-SPEC-001** + PART-III +015 | Red Core | Verify `compiler.r`/`lexer.r`/dispatch; JIT open | Implemented |

## RFC Origin Map — Per-RFC Summary

| RFC # | Title (proposed) | Stable ID(s) | Origin (Message) | Why Created | Influencing Discussions | Component |
|-------|------------------|--------------|------------------|-------------|-------------------------|-----------|
| **RFC-001** | Text Interfaces & Agent Runtimes | `TEXT-INT-001` | MSG-01 | Spectrum stateless→stateful before agent generalisation | Rebol/Red history, Docker CLI, REPL 4-step | Text Interface Layer |
| **RFC-002** | Red Programming Language Core | `RED-LANG-001`, `RED-SPEC-001/015/PART-III` | MSG-01 + MSG-09 | Baseline datatypes/dialects/Red/System/toolchain | Full-stack philosophy, 1 MB, dispatch table | Red Core |
| **RFC-003** | Agent Operating Environment | `AGENT-ENV-001`, `AGENT-ENV-ANALYSIS-001` | MSG-02 | ARS triad, pipeline, memory, events, evolutionary ladder | CLI→REPL precedent, AgenticOS/CoALA | ARS + Pipeline + Memory |
| **RFC-004** | Cognitive Operating System | `COGOS-001`, `COGOS-ANALYSIS-001`, `COGOS-FRAMEWORK-001/ANALYSIS` | MSG-03/04 | Invert OS to Intelligence; kernel/primitives/pipes/model | Unix/Multics, AIOS kernel, Graphiti, 4-dim UQ | CogOS Stack |
| **RFC-005** | Red/Cognition Language | `RED-COG-001`, `RED-COG-ANALYSIS-001` | MSG-05 | Typed cognitive primitives; declarative vs procedural | BDI/LoT/AgentSpec, GOAL declarative | Red/Cognition Type System |
| **RFC-006** | Cognitive Compiler & CIR | `RED-COMPILER-001`, `RED-COMPILER-ANALYSIS-001` | MSG-06 | Intent as compilation target; CIR + 4 passes | 1.6k-trace failures, PlanCompiler, RHTT, PASTE | Cognitive Compiler + CIR |
| **RFC-007** | Cognitive Virtual Machine | `CVM-001`, `CVM-ANALYSIS-001` | MSG-07 | Semantic ISA; registers/heap/attention/provenance | Soar/ACT-R/LIDA, MemOS, GWT, mnemonic sovereignty | CVM + CISA |
| **RFC-008** | Red 2.0 Architecture | `RED-20-001`, `RED-20-ANALYSIS-001` | MSG-08 | Unify hardware→intelligence | Multi-objective GC, trust assertions, model tiers | Red 2.0 Unified Stack |
| **RFC-009** | Red Deep Technical Specification | `RED-SPEC-001` (1317) + PART-III (1996) +015 (67) | MSG-09 | Encyclopedic ground truth | Red/System specs, lexer FSM, evaluators | Toolchain Spec |
| **RFC-010** | Analysis & Grounding Suite (meta) | All `*-ANALYSIS-001` | MSG-01–08 analyses | Ground each RFC in 2025–26 literature | 30+ papers | Traceability Extension |

*Every entry satisfies mandatory provenance: Origin (Message+Stable ID) → Evolution (why/influences) → Final (RFC+Component) → Status column in master RTM.*
