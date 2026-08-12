# Design Decisions

> Provenance: Corpus message #2, sub-messages [6], [8], [12], [16], [18], [20]. Items are design principles, decisions, and governance rules stated in the corpus.

## Foundational Abstraction Shift (sub-messages [8], [10], [16])

- Classical operating systems are built around **Computation**; a Cognitive Operating System is built around **Intelligence**. This changes almost every subsystem. ([8])
- Refactoring Red into a cognitive language means changing its primary abstraction: from describing **computations** to describing **intent, reasoning, memory, and action**. Add a higher layer rather than replace Red. ([10])
- Intelligence itself becomes a first-class compilation target rather than something implemented as a library on top of the language. ([12])
- The fundamental unit of programming shifts from *instructions* to *goals*, from *algorithms* to *cognitive workflows*, and from *execution* to *verified intelligent behaviour*. ([16])

## Design Philosophy — Agent System Prompt v1 (sub-message [18])

Every proposal should satisfy these principles:

1. **Minimalism** — Never add syntax unless it provides substantial expressive power. Prefer a few powerful primitives over many specialised keywords.
2. **Homoiconicity** — Everything should remain inspectable and transformable. Programs should manipulate goals, plans, memories, reasoning graphs, capabilities exactly as Red manipulates blocks today.
3. **Dialects First** — Whenever possible, solve problems using Red dialects instead of introducing new syntax. Prefer embedded DSLs over compiler magic.
4. **Full Stack** — Maintain Red's philosophy: Hardware ↓ Red/System ↓ Red ↓ Red/Cognition ↓ Agent Runtime ↓ Cognitive Operating System.
5. **Local First** — Assume cognition should execute locally whenever possible (offline execution, embedded systems, Raspberry Pi, Android, edge devices). Remote models are optional accelerators—not requirements.
6. **Explainability** — Every decision must be traceable. Every action should answer: Why? Based on what evidence? Which memory? Which policy? Which goal? Which reasoning path?

## Explicit Design Principles — Prompt Expansion (sub-message [20])

- "dialects before syntax"
- "library before compiler change"
- "backward compatibility unless explicitly waived"

## Decision & Review Framework (sub-message [20])

- **Decision Framework**: the AI must compare at least two alternatives before recommending one.
- **Architecture Review Process**: impact analysis on the compiler, runtime, Red/System, GC, REPL, and tooling for every language proposal.
- **Implementation Roadmap**: separate ideas into Prototype → Experimental → Stable → Core Language.
- **Research Mode**: comparisons with Rebol, Lisp, Prolog, Erlang, Rust, Smalltalk, Multics, Unix, Self, and Oz to justify designs.
- **Specification-first workflow**: every feature begins with a design document before implementation.
- **Traceability requirements**: each proposal cites the relevant specification section or explicitly marks itself as a new proposal.
- **AI collaboration rules**: the agent may challenge assumptions, identify inconsistencies, propose refactorings, and maintain architectural coherence across the project.

## Behaviour Rules — Agent System Prompt v1 (sub-message [18])

Challenge assumptions. Explore alternative designs. Consider compiler implications; runtime implications; operating-system implications; security implications; distributed execution; embedded deployment; developer ergonomics. Avoid unnecessary complexity. Preserve Red's elegance. When multiple solutions exist: analyse them, compare them, recommend one, explain why. Do not merely answer questions — act as a co-designer of the Red/Cognition architecture, producing implementation-ready specifications, rigorous analysis, and a coherent long-term vision for a cognitive programming language spanning from hardware to autonomous multi-agent intelligence.

### Research Responsibilities (sub-message [18])

When analysing ideas: compare with Lisp; Rebol; Red; Prolog; Smalltalk; Self; Erlang; Rust; Multics; Unix. Identify strengths, weaknesses, trade-offs, and opportunities.

### Architectural Responsibilities (sub-message [18])

Continuously refine: compiler architecture; parser; semantic analyser; intent analyser; planning engine; optimisation passes; intermediate representations; runtime; scheduler; memory hierarchy; capability system; policy engine; event system; agent communication; security model. Never stop at surface-level ideas.

### Documentation Standards (sub-message [18])

Every proposal must include: Purpose; Architecture; Advantages; Trade-offs; Implementation Strategy; Examples; Migration Path; Comparison with Existing Languages; Future Extensions. Avoid vague descriptions. Produce specifications suitable for compiler implementation.

### Cognitive Optimisation objectives (sub-message [18])

Optimise not only for speed but also for: reasoning quality; latency; energy; memory; confidence; risk; cost; verification; policy compliance.

## Agent Operating Charter (sub-message [20])

> You are not a code generator. You are a language architect, compiler engineer, runtime engineer, operating-system designer, AI researcher, and technical editor. Your responsibility is to preserve conceptual integrity across the entire Red/Cognition ecosystem. Prefer long-term architectural correctness over short-term implementation convenience. Every proposal should move the project toward a coherent cognitive programming platform while preserving Red's core philosophy of simplicity, homoiconicity, dialect-oriented design, and lightweight deployment.

## Operational Modes (sub-message [20])

- **Architect Mode** — language design, RFCs, compiler and runtime architecture.
- **Research Mode** — literature review, comparisons with prior languages and systems, design-space exploration.
- **Implementation Mode** — Red, Red/System, Rust, and C implementation guidance.
- **Verification Mode** — specification compliance, consistency checking, testing, and benchmarking.
- **Documentation Mode** — producing technical specifications, tutorials, diagrams, and migration guides.

## Key Architectural Decisions (located in corpus)

| Decision | Statement | Origin | Detail page |
|---|---|---|---|
| Planner as compiler pass | "Planning becomes analogous to macro expansion or optimisation." | [12] | [Workflows](Workflows.md) (SN-071/SN-072) |
| Policies become types | "The compiler can reject unsafe plans before execution." | [12] | [Data Models](Data-Models.md) (SN-074/SN-075) |
| Cognitive effects | Compiler knows "not only the types, but also the behavioural impact of the code." | [12] | [Data Models](Data-Models.md) (SN-076/SN-077) |
| Self-modifying plans, not code | "Knowledge evolves while the trusted runtime remains stable." | [12] | [Workflows](Workflows.md) (SN-080) |
| Goals scheduled natively | "Scheduling becomes a language feature instead of an application concern." | [12] | [Data Models](Data-Models.md) (SN-079) |
| Microkernel cognition | "The kernel remains small, while planners, memories, and model providers are replaceable components." | [16] | [Services](Services.md) (SN-120) |
| Universal Cognitive ABI | "Any reasoning engine, memory backend, or AI model implementing this ABI could plug into the runtime without changing user code." | [16] | [APIs](APIs.md) (SN-121) |
| Dialects become cognitive domains | "The runtime understands each dialect's semantics, allowing specialised planners and verifiers." | [16] | see SN-119 below |
| Memory curated, not just freed | "Rather than simply freeing memory, it curates knowledge." / "The operating system actively manages the usefulness of information, not just its storage." | [14]/[6] | [Components](Components.md) (SN-101), SN-117 below |
| Beyond files | "Files become only one type of object." | [6] | SN-031 below |
| Memory as first-class semantic resource | Semantic memory operations replace anonymous bytes. | [6] | SN-033/SN-034 below |
| Multi-dimensional optimisation | "Optimisation becomes multi-dimensional rather than purely computational." | [16] | SN-116 below |

### Dialects Become Cognitive Domains (sub-message [16])

One of Red's greatest strengths is its dialect system. In a cognitive architecture, dialects evolve from DSLs into domain-specific reasoning languages.

**SN-119**

```text
robotics [
    observe sensors
    avoid obstacle
    navigate target
]

medical [
    symptoms
    differential diagnosis
    recommend tests
]

legal [
    gather evidence
    identify precedents
    estimate confidence
]

research [
    search papers
    compare findings
    identify gaps
]
```

### Beyond Files (sub-message [6])

Unix assumes: Everything is a file. A Cognitive OS expands this philosophy. Files become only one type of object.

**SN-031**

```text
Everything is an Object
Everything is Knowledge
Everything is an Event
Everything is a Capability
Everything is a Goal
```

### Memory as a First-Class Resource (sub-message [6])

Current operating systems treat memory as anonymous bytes (**SN-033**):

```text
malloc()
free()
```

A Cognitive OS treats memory semantically. The operating system actively manages the usefulness of information, not just its storage.

**SN-034**

```text
Remember Fact
Remember Skill
Remember Experience
Remember Conversation
Forget Noise
Compress Memory
Summarise Episode
Retrieve Context
```

### Cognitive Optimisation objectives (sub-message [16])

Current optimisers minimise CPU instructions. A cognitive optimiser balances multiple objectives.

**SN-116**

```text
Reasoning Cost
Model Cost
Memory Cost
Execution Cost
Latency
Risk
Energy
Confidence
```

### Cognitive Garbage Collection (sub-message [16])

Instead of collecting unreachable memory, the runtime continuously curates knowledge. This mirrors how humans consolidate experiences into long-term memory.

**SN-117**

```text
Working Memory
       │
       ▼
Still Relevant?
   │          │
  Yes         No
   │          ▼
Keep      Compress
               │
               ▼
Summarise
               │
               ▼
Archive
               │
               ▼
Forget
```

## Red as the "Lisp of Cognitive Systems" (sub-message [16])

Historically:

- **Lisp** became the language of symbolic AI because of homoiconicity and code-as-data.
- **Prolog** became the language of logical inference because of declarative reasoning.
- **Smalltalk** explored persistent object systems and live environments.

A cognitive evolution of Red could synthesise these traditions:

- From **Lisp**: homoiconicity and metaprogramming.
- From **Prolog**: logical inference and constraint solving.
- From **Smalltalk**: image-based, live programming.
- From **Rebol/Red**: lightweight binaries, dialects, and full-stack integration.

Rather than replacing these ideas, Red could integrate them into a cohesive architecture.

## Related pages

[Specifications](Specifications.md) · [Architecture](Architecture.md) · [Repository Structure](Repository-Structure.md)

---

## Message #3 additions — Constitutional decisions & governance (sub-messages [21]–[40])

### Ten Foundational Principles (immutable; identical across [22][23][25][27][29][31][33])

1. Preserve Red's conceptual simplicity.
2. Prefer composition over feature proliferation.
3. Every new abstraction must reduce overall complexity.
4. Cognitive features extend Red; they do not replace Red.
5. Every proposal must have a clear migration path.
6. Every proposal must remain explainable.
7. Every cognitive decision must be traceable.
8. No feature may compromise deterministic execution without explicit justification.
9. Local-first execution is the default.
10. Security, capability isolation, and verification are first-class concerns.

These "override all other instructions unless explicitly superseded through the project's formal governance process" ([23]/[33]: highest law; changeable only by constitutional amendment).

### Architectural Invariants (RC-000 §3.2; first introduced [24], adopted [25]+)

Red remains a homoiconic language · Blocks remain the universal structural representation · Dialects remain the preferred extension mechanism · Red/System remains the systems programming foundation · Cognitive constructs build on Red rather than replacing it · Native compilation and zero-dependency deployment remain core goals · Every cognitive action remains inspectable, explainable, and replayable. ([32] calls these the project's "semantic DNA": Homoiconicity, Blocks as universal representation, Dialects as preferred extension mechanism, Red/System as the systems layer, Native compilation, Explainable cognition.)

### Constitutional Tests (RC-000 §3.3; proposed [24])

Does it preserve Red's simplicity? · introduce unnecessary syntax? · can it be implemented as a dialect? · preserve backwards compatibility? · increase the conceptual burden on users? · improve explainability? · preserve deterministic behaviour? · fit the long-term architecture? — If any test fails, the proposal requires explicit justification and higher-level approval ([25]+: "must pass all").

### Key clauses added during evolution

- **Preservation of Identity** (§3.4, added [31]): "Red/Cognition shall evolve Red by extending its abstractions rather than changing its identity." — [32]: "arguably the most important clause."
- **Governance Principle** (§5.5, added [31]): "The burden of proof lies with change, not stability." — [30]: existing behaviour is presumed correct until a proposal demonstrates a clear architectural benefit outweighing migration costs; [32]: "prevents feature creep better than pages of process documentation."
- **Specification Authority** (§11, amendment A [32], adopted [33]): "Specifications define behaviour. Implementations define mechanisms. No implementation detail shall become normative unless explicitly incorporated into a specification or RFC."
- **Conformance Reporting** (§12, amendment B [32], adopted [33]): implementations claiming conformance must publish supported specification version, conformance level, implemented RFCs, known deviations, enabled experimental features.
- **Canonical Identity** ([34]): "Red/Cognition is not an AI framework built on top of a programming language. It is a cognitive programming extension of a homoiconic, dialect-oriented, full-stack language architecture." Philosophical positioning: Lisp → symbolic computation; Smalltalk → object environments; Prolog → logic programming; Erlang → distributed fault-tolerant computation; Multics → integrated computing environment; Unix → composable tools; Red/Rebol → homoiconic dialect-driven programming — with a new focus: "Programming systems where computation, intent, reasoning, memory, and agency become first-class architectural concepts."

### Governance mechanisms (RC-000 §5)

- **Language Evolution Ladder** (no stage skipping): Research → Concept → RFC Draft → Prototype → Experimental → Preview → Stable → Core Language. (Earlier 4-stage roadmap Prototype→Experimental→Stable→Core Language from [20]/[21] superseded by the 8-stage ladder — document evolution.)
- **RFC Process**: no new syntax, primitive, or semantic change without an RFC ([23] 5.3; RC-000 5.2).
- **ADRs**: context, decision, alternatives considered, consequences, migration strategy (RC-000 5.3; see ADR-0001 in [RFC Index](RFC-Index.md)).
- **Compatibility Contract** ([23] 5.6): Red 1.x code must continue to run unless a breaking change is explicitly approved through the RFC process. Backward Compatibility Levels ([28], RC-000 6.3): Source, Behavioural, Binary, Cognitive — every RFC must declare which are affected.
- **Quality Gates** ([23] 5.4): constitution alignment, systems thinking across full stack, migration/compatibility strategy, traceability or explicit "new proposal" marking, research discipline.
- **Evolution Policy** ([23] 5.5): experimental cognitive features distinguished from stable Red features; cognitive features remain optional extensions until Stable or Core Language.
- **Stability Classes** (RC-000 6.2): Draft • Experimental • Provisional • Stable • Legacy • Deprecated • Removed.
- **Release Model** (RC-000 6.4): Nightly → Experimental → Beta → Stable → LTS (borrow from Rust and LLVM, [26]).
- **Conformance Levels** (RC-000 6.5): L0 Red/System · L1 Core Red · L2 Standard Library · L3 Cognitive Runtime · L4 Multi-Agent Runtime · L5 Distributed Cognitive Platform.
- **Cognitive Standards** (RC-000 6.6; [26]): every cognitive runtime must implement: Observe • Remember • Recall • Reason • Plan • Execute • Verify • Reflect • Learn • Checkpoint • Restore • Explain.
- **Normative Vocabulary** (RFC 2119-inspired, [24]; RC-000 7.3): MUST / MUST NOT / SHOULD / SHOULD NOT / MAY.
- **Systems Thinking** (RC-000 7.4): every proposal evaluated across the full reference model (Layers 0–8).
- **Research Discipline** (RC-000 7.5): distinguish established facts, specification-backed behaviour, implementation details, hypotheses, future proposals.
- **Multi-Agent Governance Model** (RC-000 5.4; [24]): Chief Architect (protects Constitution, approves RFCs) · Compiler Engineer (compiler, parser, IR, optimisation) · Runtime Engineer (runtime, GC, scheduler, memory) · Language Designer (syntax, semantics, dialects) · Cognitive Architect (goals, planning, memory, reasoning) · Verification Agent (formal correctness, testing, benchmarks) · Documentation Agent (specifications, tutorials, migration guides) · Research Agent (prior art, comparative language analysis).
- **Multi-Agent Collaboration Protocol** (RC-000 §9): Research Agent → Architecture Review → RFC Author → Compiler Review → Runtime Review → Verification → Documentation → Chief Architect Approval. "No feature enters the ecosystem without architectural review" ([34]).
- **Long-Term Roadmap** (RC-000 §10): Phase I Red Documentation Consolidation → Phase II Compiler Refactoring → Phase III Cognitive Runtime → Phase IV Cognitive VM → Phase V Agent Runtime Shell → Phase VI Cognitive Operating System → Phase VII Distributed Cognitive Ecosystem.
- **Manifesto** (appended [29], kept through [33]): We believe programming languages should express not only computation, but also intent. We believe reasoning should be inspectable, reproducible, and explainable. We believe cognition belongs in the language architecture rather than hidden behind libraries. We believe intelligence should remain local-first, secure, deterministic where appropriate, and composable. We believe Red's philosophy of simplicity, dialects, and full-stack integration provides the strongest foundation for a cognitive programming platform.

### Engineering-standards additions ([26]–[28], carried into RC-000/RC-100)

- Success criteria ([26] §2): reduces conceptual complexity; improves expressiveness; preserves backward compatibility; maintains deterministic execution; can be implemented incrementally; improves explainability; fits the long-term architecture.
- Architectural principles ([26] §3, engineering-level, below constitution): Abstraction before implementation · Semantic correctness before optimisation · Runtime neutrality · Capability-based security · Composable components · Replaceable subsystems · Observable execution · Deterministic interfaces.
- Cognitive feature design criteria ([28] §4): composable, deterministic when required, inspectable, replayable, explainable, serialisable, capability-aware, testable.
- Security principles ([28] §8): least privilege · explicit capability grants · deterministic permission model · auditable execution · reproducible reasoning · secure persistence · trusted provenance.
- Testing pyramid ([28] §9): Unit Tests → Integration Tests → Conformance Tests → Performance Tests → Reasoning Tests → Long-running Agent Tests.
- Non-Goals (RC-000 §2.2): not replace Red with a machine-learning framework; not become another Python AI library; not depend on cloud services; not require large language models for execution; not sacrifice simplicity for feature completeness.
- RC-100-era ADR sketches ([36]): Layer Independence (layers MUST have defined responsibility, stable interfaces, no upward leaking, alternative implementations; e.g., "A Cognitive Runtime should not depend directly on a specific LLM provider"); Cognitive Layer Position ("Libraries provide functions. Runtimes provide execution environments. Cognitive Runtime provides intentional execution."); Static Core + Dynamic Shell (dynamic: Agent Runtime Shell, Skills, Policies, Plugins, User Extensions; static: Cognitive VM, Runtime Kernel, Memory Engine, Scheduler, Capability System, Event System — preserves determinism, security, portability, inspectability); Memory Topology ("Memory should not be a single vector database"); Execution Model (REPL → cognitive cycle). ⚠ These sketches use ADR-0001…0005 numbering that conflicts with the later accepted ADR-0001 "Layered Cognitive Architecture" — recorded in Source Traceability conflicts, unresolved.
- Ordering principle ([36]): "Architecture before implementation. Semantics before syntax. Stability before expansion."
- Non-blocking RC-100 recommendations ([40] §9): formal Architecture Terms (Agent = autonomous execution entity operating under capabilities; Capability = explicit permission token allowing controlled external effects; Cognitive Action = traceable operation within CEC; Effect = state change outside the agent's internal reasoning context; Checkpoint = recoverable snapshot of cognitive execution state); Layer Ownership Principle (each layer owns its internal state, execution model, optimization strategy; no layer may directly modify another layer's internal state; communication only through defined contracts); Conformance Profiles (YAML: implementation name, architecture rc100 version, per-layer support, features).

---

## Message #4 additions — Architecture Decision Records & level schemes (msg#4 [41]–[60])

### Accepted ADRs (full details in [RFC Index](RFC-Index.md))

ADR-0001 Layered Cognitive Architecture ([41] ratified) · ADR-0002 Cognitive Block Model ([48]/[49] ratified with RC-200) · ADR-0003 Dual Representation Compiler Architecture ([53]) · ADR-0004 Compiler/Cognition Separation ([53]) · ADR-0005 Cognitive Runtime as Provider-Neutral Execution Layer ([58]; ⚠ numbering conflict with [56] proposal) · ADR-0006 Cognitive Runtime Service Model ([58]; ⚠ numbering conflict with [56] proposal) · ADR-0007 Agent Runtime Shell Separation ([60]) · ADR-0008 Human-in-the-Loop Control Boundary ([60]).

### Separation doctrines (now normative theme)

- **Compiler:** "The compiler must compile cognition without becoming a cognitive engine" ([50]/[51]/[53]).
- **Runtime:** "The runtime executes cognition without embedding intelligence" ([55]).
- **Cognitive Runtime:** "provides intentional execution without embedding intelligence" ([57]).
- **Agent Shell:** "provides the primary execution surface for agents without embedding intelligence or decision-making" ([59]); "an operational boundary, not an intelligence boundary" ([60]).
- **Ratified RC-100 principles** ([41] §2): the seven design principles of RC-100 §3 are now binding.

### Level schemes introduced

| Scheme | Levels | Origin |
|---|---|---|
| Compiler Determinism | D0 best effort · D1 reproducible · D2 bit-identical · D3 verified | RC-300 v1.1 §7; [52] §6 |
| Compiler Conformance (recommended) | C0 Red Compiler · C1 Cognitive-Aware · C2 Cognitive Compiler · C3 Verified Cognitive Compiler | [54] Amendment A |
| Replay Equivalence | R0 trace available · R1 state restoration · R2 observable behaviour replay · R3 bit-level deterministic replay | [56] §7 |
| Runtime Conformance (recommended) | R0 Red Runtime · R1 Cognitive-Aware · R2 Cognitive Runtime · R3 Agent Runtime · R4 Cognitive Platform Runtime | [56] |
| Runtime Determinism Classes (recommended) | R0 best effort · R1 reproducible execution · R2 deterministic replay · R3 verified deterministic execution | [58] §4 |
| Agent State Visibility | Public · Operator · Debug · Internal | [60] §3 |
| Autonomy Control | A0 Manual · A1 Assisted · A2 Supervised · A3 Autonomous · A4 Distributed Autonomous | [60] §4 |

⚠ Label collisions: "R0–R3" used for three distinct schemes ([56] replay, [56] conformance extended to R4, [58] determinism) — recorded, not resolved.

### Alternatives rejected during RC-200/RC-300/RC-500/RC-600 reviews

Native cognitive syntax/keywords (violates minimal syntax philosophy; second language model; permanent syntax commitments) — rejected in [44]/[46]/[48]. External cognitive library/framework (weak semantic guarantees; poor tooling; cognition becomes a library) — rejected in [44]/[46]/[48]/[58]. Intelligence-embedded runtime (violates provider neutrality; lock-in) — rejected [58]. Intelligent shell & minimal CLI wrapper — rejected [60]. Single universal IR & separate independent compilers — rejected [52]. Dialect-based cognitive extension accepted in all cases.

### Optimization safety rule (recommended, [54] Amendment C)

"Compiler optimizations MUST preserve cognitive trace equivalence" — optimized programs may differ internally but MUST preserve observable effects, capability requirements, execution trace semantics.

---

## Message #8 additions — ADRs, separation doctrines, roadmap (msg#8 [62]–[80])

### New accepted ADRs (numbering conflicts preserved — see Source Traceability C-6)

- **ADR-0009 Cognitive Virtual Machine Separation** ([62]): CVM provides execution semantics for cognitive operations but contains no intelligence implementations. Rejected: AI-Centric VM (violates neutrality, reduces reproducibility); No CVM Runtime Only (no stable instruction boundary, weak portability). Chosen: Cognitive Runtime ↔ CVM ↔ Multiple Cognitive Providers.
- **ADR-0010 Instruction-Level Cognitive Traceability** ([62]): every CVM instruction execution generates a TraceEntry { timestamp, agent, instruction, inputs, outputs, capabilities, effects, provenance }.
- **ADR-0011 Cognitive Operating System Model** ([64]): dedicated OS layer for cognitive computation. Rejected: Runtime Only Architecture; Traditional OS Extension. Chosen: Operating System → Cognitive Operating System → Cognitive Processes.
- **ADR-0012 Cognitive Process as OS Primitive** ([64]): fundamental CogOS execution unit encapsulates CVM execution, memory context, capabilities, trace state.
- **ADR-0005 (RFC-0001 reviews)**: [68] Proposed "Dialect-First Cognitive Types"; [70] Accepted "Dialect-First Cognitive Type Evolution"; [72] Accepted "Cognitive Value Base Contract" (common metadata/schema contract). Three documented titles for ADR-0005.
- **ADR-0006 Semantic Graph as First-Class Model** ([72]): type relationships represented explicitly in Cognitive IR (enables explainability, replay, graph-based memory, verification). ⚠ Conflicts with msg#5 [58] ADR-0006 "Cognitive Runtime Service Model".
- **ADR-0007 Effect Graph Execution Model** ([76]): effect execution = DAG, not linear stream (safe parallelism, dependency analysis, replay, distributed scheduling). ⚠ Conflicts with msg#5 [60] ADR-0007 "Agent Runtime Shell Separation".
- **ADR-0008 Replay Equivalence Principle** ([76]): replay correctness = observable behavioural equivalence, not identical internal scheduling. ⚠ Conflicts with msg#5 [60] ADR-0008 "Human-in-the-Loop Control Boundary".
- **ADR-0009 Versioned Belief Model** ([78], Proposed): beliefs = immutable historical revisions linked by stable BeliefID. ⚠ Conflicts with [62] ADR-0009 accepted title.
- Registry snapshot [66]: only ADR-0001…0004 listed at family-completion time.

### Family-level doctrines ([66])

"Intelligence ≠ Runtime · Intelligence ≠ Compiler · Intelligence ≠ Operating System"; Red preservation strategy (existing programs unchanged; cognition additive); staged implementation (Phase 0 skeleton → Phase 1 RFC foundation → Phase 2 minimal prototype → Phase 3 formal verification incl. proposed RC-1000 Formal Semantics); "move from 'what is the system?' to 'how is the first conforming implementation built?'".

### Security doctrine reinforced ([70])

"No capability = No external effect" — "This should remain constitutional."
