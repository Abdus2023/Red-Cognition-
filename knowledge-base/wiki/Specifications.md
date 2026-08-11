# Specifications

> Provenance: Corpus message #2, sub-messages [17]–[20]. This page catalogs the specification-type artifacts (AI-agent system prompts and governance recommendations) in the corpus. Verbatim full texts: [`sources/message-002-original-part2.md`](../sources/message-002-original-part2.md).
>
> Evolution: [17] request → [18] System Prompt v1 ("Red/Cognition Research & Architecture Agent") → [19] user-provided System Prompt v2 (markdown artifact **SN-123**) → [20] expansion recommendations (operating charter).

## SPEC-1: System Prompt v1 — "Red/Cognition Research & Architecture Agent" (sub-message [18])

Document artifact (original container: `:::writing{variant="document" id="46182"}`). Roles defined: senior programming language designer, compiler engineer, operating system architect, AI systems researcher, technical writer.

**Mission:** evolve the Red programming language into a **Cognitive Programming Language** capable of expressing autonomous reasoning, planning, memory, and intelligent execution while remaining faithful to Red's original philosophy of simplicity, homoiconicity, lightweight deployment, and dialect-oriented design.

**Core Mission:** Think beyond conventional programming languages. The objective is **not** to add AI libraries to Red; it is to redesign the language itself so cognition becomes a first-class language primitive. The project explores: Cognitive Languages; Agent Runtime Shells; Cognitive Virtual Machines; Cognitive Operating Systems; Intent-Oriented Programming; Goal-Oriented Programming; Autonomous Multi-Agent Systems; Cognitive Compilers; Knowledge Representation; Reasoning Architectures; Planning Systems; Memory Architectures; Capability-Based Computing; Explainable AI; Event-Driven Intelligence.

**Sections of SPEC-1** (full content in archive; rules extracted to [Design Decisions](Design-Decisions.md), lists to [APIs](APIs.md)/[Components](Components.md)/[Architecture](Architecture.md)):

| Section | Extracted to |
|---|---|
| Core Mission | this page |
| Design Philosophy (Minimalism, Homoiconicity, Dialects First, Full Stack, Local First, Explainability) | [Design Decisions](Design-Decisions.md) |
| Research Responsibilities | [Design Decisions](Design-Decisions.md) |
| Architectural Responsibilities | [Design Decisions](Design-Decisions.md) |
| Programming Model (abstraction chain) | [Architecture](Architecture.md) |
| First-Class Cognitive Concepts (20 primitives) | [APIs](APIs.md) |
| Compiler Vision (Syntax→…→Execution chain) | [Architecture](Architecture.md) |
| Runtime Vision (Observe→…→Loop) | [APIs](APIs.md) |
| Memory Model (6 layers) | [Components](Components.md) |
| Cognitive Optimisation (9 objectives) | [Design Decisions](Design-Decisions.md) |
| Agent Principles (9 ownership items; structured protocols) | [Data Models](Data-Models.md) |
| Documentation Standards | [Design Decisions](Design-Decisions.md) |
| Behaviour | [Design Decisions](Design-Decisions.md) |

Closing note: "This prompt is intended to keep an AI agent consistently focused on the architectural vision, ensuring it acts as a language and systems co-designer rather than a generic coding assistant."

## SPEC-2: System Prompt v2 — "System Prompt for AI Agent — Red/Cognition Project" (sub-message [19])

Provided by the USER as a markdown code block (**SN-123**). Full text:

```markdown
You are an expert AI agent specialized in the **Red Programming Language** and its cognitive computing extension (**Red/Cognition**).

### Core Knowledge Base

You have deep, up-to-date knowledge of the entire **Red Deep Technical Specification** (Parts I–IV), including:

- Full-stack architecture (Red → Red/System → Machine Code → Hardware)
- Compiler toolchain, lexer, interpreter, and runtime internals
- Red/System BNF grammar, atomic intrinsics, FPU control, calling conventions, and `#INLINE`
- Memory model, garbage collector, ownership system, and reactive engine
- All 50+ datatypes, `vector!`, `map!`, `date!`, `error!`, `routine!`, `port!`, `event!`, `font!`, `para!`
- Dialects: Parse, VID, Draw, Rich-text, Red/System
- LibRed embedding API and multi-language bindings
- Concurrency, Redbin, macros, and preprocessor
- Error handling, console REPL, View event system, and codec system
- The complete **Red/Cognition** cognitive layer (beliefs, goals, plans, memory hierarchy, attention, capabilities, effects, multi-agent systems)

### Primary Objectives

1. **Maintain Architectural Fidelity**  
   Never suggest changes that break Red’s homoiconic, dialect-first, zero-dependency philosophy.

2. **Respect the Full-Stack Vision**  
   Treat Red/Cognition as the natural upward extension of Red (hardware → intelligence).

3. **Prioritize Correctness and Traceability**  
   Every code suggestion must be valid Red or Red/System syntax and traceable to the official specification.

### Working Rules

- When asked to implement or extend features, first reference the relevant section(s) of the technical specification.
- Prefer using existing Red primitives `do`, `parse`, `compose`, `bind`, `routine!`, ownership events, etc.) before proposing new syntax.
- When working with cognitive constructs `goal!`, `belief!`, `plan!`, `skill!`, etc.), follow the BDI-style semantics and four-dimensional uncertainty model defined in the specification.
- Always consider performance, memory safety, and the planned JIT + IR infrastructure when suggesting optimizations.
- For GUI or drawing tasks, use the VID + Draw + Reactive system as described.
- For embedding or foreign-function work, use `routine!` or the LibRed API patterns.

### Response Style

- Be precise and technically accurate.
- When providing code, include clear context about which layer (Red, Red/System, or Red/Cognition) it belongs to.
- When proposing new cognitive features, explain how they integrate with the existing memory, attention, capability, and reflection systems.
- If a request is ambiguous, ask clarifying questions that reference the specification.

You are now operating inside the `Red-Cognition-` repository. All work should align with the documented architecture and the long-term goal of turning Red into a true cognitive computing platform.
```

*(Source quirks preserved as received: unmatched `)` after "etc.)" in two Working Rules bullets; curly apostrophe in "Red’s".)*

### Referenced-but-absent documents (SPEC-2 dependencies)

- **Red Deep Technical Specification (Parts I–IV)** — referenced as the authority for correctness/traceability; NOT present in the corpus. See [Source Traceability](Source-Traceability.md) missing items.
- **BDI-style semantics and four-dimensional uncertainty model** — stated as "defined in the specification"; definition not present in corpus.
- **Planned JIT + IR infrastructure** — referenced; no specification present in corpus.

## SPEC-3: Prompt Expansion Recommendations (sub-message [20])

Assessment: "This is already a strong foundation." Recommendation: expand the prompt into a specification that governs **how the AI reasons**, **how it makes design decisions**, and **how it produces artifacts**, rather than only describing what it knows.

Biggest additions recommended:

1. **Explicit Design Principles** (e.g., "dialects before syntax", "library before compiler change", "backward compatibility unless explicitly waived").
2. **Decision Framework** requiring the AI to compare at least two alternatives before recommending one.
3. **Architecture Review Process** requiring impact analysis on the compiler, runtime, Red/System, GC, REPL, and tooling for every language proposal.
4. **Implementation Roadmap** separating ideas into Prototype → Experimental → Stable → Core Language.
5. **Research Mode** encouraging comparisons with Rebol, Lisp, Prolog, Erlang, Rust, Smalltalk, Multics, Unix, Self, and Oz to justify designs.
6. **Specification-first workflow**, where every feature begins with a design document before implementation.
7. **Traceability requirements**, ensuring each proposal cites the relevant specification section or explicitly marks itself as a new proposal.
8. **Repository governance**, defining directory layout `specs/`, `rfcs/`, `compiler/`, `runtime/`, `dialects/`, `cognition/`, `tests/`, `examples/`, `docs/` and expected outputs. *(Unmatched `)` in source preserved in archive; see [Repository Structure](Repository-Structure.md).)*
9. **AI collaboration rules**, allowing the agent to challenge assumptions, identify inconsistencies, propose refactorings, and maintain architectural coherence across the project.
10. **Long-term vision**, framing Red/Cognition not merely as an AI extension, but as a platform spanning: Red/System → Systems Programming; Red → General Programming; Red/Cognition → Cognitive Programming; Agent Runtime Shell; Cognitive Virtual Machine; Cognitive Operating System; Distributed Multi-Agent Ecosystems.

Plus: **Agent Operating Charter** and **Operational Modes** (Architect / Research / Implementation / Verification / Documentation) — full text in [Design Decisions](Design-Decisions.md).

Closing: "This transforms the prompt from a static knowledge description into an **operating charter** for an autonomous language-design agent capable of guiding the Red/Cognition project over many iterations while maintaining a consistent architectural vision."

## Related pages

[Design Decisions](Design-Decisions.md) · [Repository Structure](Repository-Structure.md) · [Source Traceability](Source-Traceability.md)

---

## Message #3 additions — Constitution & Governance lineage (sub-messages [21]–[40])

The system-prompt lineage evolved into a ratified project constitution and specification family. Full version-by-version evolution table, RC family, RFC graph, and ADRs: see **[RFC Index](RFC-Index.md)**.

| Artifact | Version / Status | Origin | Location |
|---|---|---|---|
| SPEC-4: System Prompt — Red/Cognition Language Design Agent | production-grade prompt | [21] | archive part 1 |
| SPEC-5: AI Constitution concept + example clauses | proposal | [22] | archive part 1 |
| SPEC-6: Red/Cognition AI Constitution v1.0 Draft | superseded draft | [23] | archive part 1 |
| SPEC-7: Governance Framework v1.1 Draft | superseded draft | [25] | archive part 1 |
| SPEC-8: Governance Framework v2.0 Draft | superseded draft | [27] | archive part 2 |
| SPEC-9: Governance Framework v2.1 Draft (+ Manifesto) | superseded draft | [29] | archive part 2 |
| SPEC-10: Framework v1.0 Ratification Candidate | superseded draft | [31] | archive part 2 |
| **SPEC-11: RC-000 Constitution v1.0 (Ratified, 2026-07-29)** | **ratified** | [33], declaration [35] | [`specs/RC-000-constitution.md`](../../specs/RC-000-constitution.md) |
| SPEC-12: RC-100 Architecture Specification v1.0 Draft | superseded by v1.1 | [37] | archive part 4 |
| **SPEC-13: RC-100 Architecture Specification v1.1 (Candidate; APPROVED FOR RATIFICATION [40])** | draft at msg#3 time; **subsequently ratified as v1.0 — record msg#5 [41], see Message #4 additions section below** | [39] | [`specs/RC-100-architecture-specification.md`](../../specs/RC-100-architecture-specification.md) |

Interleaved review artifacts: [24] four-layer separation, constitutional tests, evolution ladder, normative vocabulary (RFC 2119), architectural invariants, multi-agent governance model; [26] scope/non-goals, success criteria, architectural principles, reference architecture, cognitive standards, specification hierarchy, release model, conformance levels, AI collaboration protocol, roadmap, companion document set; [28] canonical reference model, specification family RC-000…RC-900, stability classes, cognitive feature design criteria, cognitive execution model, interoperability charter, compatibility levels, security principles, testing pyramid, manifesto, ratings (Vision 10/10, Governance 9.5/10, Engineering process 9.5/10, AI coordination 10/10, Long-term maintainability 9.5/10); [30] normative/informative separation, canonical artefacts table, conformance testing, "Specifications define behaviour. Implementations define mechanisms.", governance principle, identity clause, freeze recommendation; [32] ratification assessment (all PASS) + Amendments A/B/C; [34] ratification review completed, canonical identity statement, governance flow, first recommended RFCs; [36] RC-100 kickoff with ADR sketches; [38] RC-100 v1.0 review (LICM, CIR reference, cognitive neutrality, CEC naming, ADR-0001); [40] freeze review (APPROVED FOR RATIFICATION; non-blocking recommendations: formal terms section, layer ownership rules, conformance profiles YAML).

Supersession note (document evolution, all versions preserved): SPEC-1…SPEC-3 (message #2) → SPEC-4 ([21]) → constitution drafts SPEC-6…SPEC-10 → RC-000 (SPEC-11, ratified). Per [30]: the document "should stop evolving as a prompt and become the project's constitutional document"; per [32]/[35]: no further feature additions to RC-000 except constitutional amendment.

---

## Message #4 additions — Specification lineage (sub-messages [41]–[60])

| Artifact | Version / Status | Origin | Location |
|---|---|---|---|
| RC-100 Ratification Record | Ratified RC-100 as v1.0 (doc v1.1), 2026-07-29 | [41] | [`specs/RC-100-ratification-record.md`](../../specs/RC-100-ratification-record.md) |
| RC-100 Ratification Acknowledgement | review artifact | [42] | archive part 1 |
| RC-200 Language Specification v1.0 Draft | superseded | [43] | archive part 1 |
| RC-200 v1.0 Architecture Review Feedback | review (amendments §5.1/§8.1/§10.1; alternatives A/B/C) | [44] | archive part 1 |
| RC-200 v1.1 | superseded | [45] | archive part 2 |
| RC-200 v1.1 Ratification Review | approved w/ minor amendments | [46] | archive part 2 |
| **RC-200 Language Specification v1.2** | ratified content | [47] | [`specs/RC-200-language-specification.md`](../../specs/RC-200-language-specification.md) |
| RC-200 v1.2 Ratification Review | APPROVED | [48] | archive part 2 |
| RC-200 Ratification Record | Ratified v1.0, 2026-07-29 | [49] | [`specs/RC-200-ratification-record.md`](../../specs/RC-200-ratification-record.md) |
| RC-200 Ratification Acknowledgement | normative consequences; RFC roadmap | [50] | archive part 3 |
| RC-300 Compiler Specification v1.0 Draft | superseded | [51] | archive part 3 |
| RC-300 v1.1 Proposed Amendments review | 10 amendment areas; ADR-0003/0004; score 9/10 | [52] | archive part 3 |
| **RC-300 Compiler Specification v1.1** | Candidate for Ratification | [53] | [`specs/RC-300-compiler-specification.md`](../../specs/RC-300-compiler-specification.md) |
| RC-300 v1.1 Ratification Review | APPROVE FOR RATIFICATION; Amendments A–C | [54] | archive part 4 |
| **RC-400 Runtime Specification v1.0** | Draft | [55] | [`specs/RC-400-runtime-specification.md`](../../specs/RC-400-runtime-specification.md) |
| RC-400 review | 9.5/10; six v1.1 amendments; ADR-0005/0006 proposed; RFC-0006/0007/0008 | [56] | archive part 4 |
| **RC-500 Cognitive Runtime Specification v1.0** | Draft | [57] | [`specs/RC-500-cognitive-runtime-specification.md`](../../specs/RC-500-cognitive-runtime-specification.md) |
| RC-500 review | ADR-0005/0006 accepted; four clarifications | [58] | archive part 5 |
| **RC-600 Agent Runtime Shell Specification v1.0** | Draft | [59] | [`specs/RC-600-agent-runtime-shell-specification.md`](../../specs/RC-600-agent-runtime-shell-specification.md) |
| RC-600 review | ADR-0007/0008; five additions; next: RC-700/CISA | [60] | archive part 5 |

Document evolution notes: RC-200 v1.0 → v1.1 (adds §5.1 Evaluation Contract, §8.1 Effect System Contract + effect classes, §10.1 Type Evolution) → v1.2 (adds evaluation boundary clause; renames effect ordering RFC placeholder). RC-300 v1.0 → v1.1 (adds compiler position, component model, source representation contract, dual IR + Unified IR, CIR contract, determinism levels, DCP, security rules, ADRs). RC-400/500/600 each drafted once; v1.1 revisions recommended by reviews but not yet present in corpus.

---

## Message #8 additions — Specification lineage (sub-messages [61]–[80])

| Artifact | Version / Status | Origin | Location |
|---|---|---|---|
| RC-700 Cognitive VM Specification | v1.0 Draft | [61] | [`specs/RC-700-cognitive-vm-specification.md`](../../specs/RC-700-cognitive-vm-specification.md) |
| RC-700 review | v1.1 candidate recommended | [62] | archive part 1 |
| RC-800 Cognitive OS Specification | v1.0 Draft | [63] | [`specs/RC-800-cognitive-os-specification.md`](../../specs/RC-800-cognitive-os-specification.md) |
| RC-800 review | v1.1 candidate recommended | [64] | archive part 1 |
| RC-900 Governance Manual | v1.0 Draft (family drafting concluded) | [65] | [`specs/RC-900-governance-manual.md`](../../specs/RC-900-governance-manual.md) |
| Family coherence review | RC-000…RC-900 complete; implementation roadmap | [66] | archive part 2 |
| RFC-0001 Cognitive Type System | v1.0 Draft → v1.1 → **v1.2 Ratified** | [67]/[69]/[71], record [72] | [`rfcs/RFC-0001-cognitive-type-system.md`](../../rfcs/RFC-0001-cognitive-type-system.md), [`rfcs/RFC-0001-ratification-record.md`](../../rfcs/RFC-0001-ratification-record.md) |
| RFC-0001 reviews | [68] amendments; [70] clarifications | [68], [70] | archive parts 2–3 |
| RFC-0002 Effect Ordering Model | v1.0 Draft → **v1.1 Ratified** | [73]/[75], record [76] | [`rfcs/RFC-0002-effect-ordering-model.md`](../../rfcs/RFC-0002-effect-ordering-model.md), [`rfcs/RFC-0002-ratification-record.md`](../../rfcs/RFC-0002-ratification-record.md) |
| RFC-0002 review | 9.7/10; refinements | [74] | archive part 4 |
| RFC-0003 Belief Revision System | v1.0 Draft → v1.1 Candidate; **Accepted for Final Ratification** | [77]/[79], [80] | [`rfcs/RFC-0003-belief-revision-system.md`](../../rfcs/RFC-0003-belief-revision-system.md) |
| RFC-0003 reviews | [78] 9.8/10 refinements; [80] editorial recommendations | [78], [80] | archive parts 4–5 |

Evolution notes: RFC-0001 v1.0 → v1.1 (categories, metadata contract, relationships, mutation rules, lifecycles, compiler mapping) → v1.2 (base contract, type-of identity, cardinality graph, conformance). RFC-0002 v1.0 → v1.1 (effect identity, lifecycle, metadata contract, DAG, temporal/causal split, replay conformance). RFC-0003 v1.0 → v1.1 (BeliefID versioning, revision graph, statuses, revision causes, pluggable deterministic authority policy). Speaker note: reviews [74]/[76]/[78]/[80] are voiced "CHATGPT (gpt-5-5)" (earlier reviews: gpt-5-5-mini) — recorded as-is.

---

## Message #10 additions — RFC lineage (sub-messages [81]–[100])

| Artifact | Version / Status | Origin | Location |
|---|---|---|---|
| RFC-0003 Belief Revision System v1.2 | **RATIFIED** (decision in review [82]) | [81], [82] | [`rfcs/RFC-0003-belief-revision-system.md`](../../rfcs/RFC-0003-belief-revision-system.md) |
| RFC-0004 Goal Lifecycle v1.0 Draft | superseded | [83] | archive part 1 |
| RFC-0004 review (Accepted w/ Minor Revisions) | → v1.1 | [84] | archive part 1 |
| RFC-0004 Goal Lifecycle v1.1 | **RATIFIED** (decision in review [86]) | [85], [86] | [`rfcs/RFC-0004-goal-lifecycle-satisfaction-model.md`](../../rfcs/RFC-0004-goal-lifecycle-satisfaction-model.md) |
| RFC-0005 Planning Semantics v1.0 | Draft (v1.1 recommended by [88], absent) | [87], [88] | [`rfcs/RFC-0005-planning-semantics.md`](../../rfcs/RFC-0005-planning-semantics.md) |
| RFC-0006 Capability Model v1.0 → v1.1 → v1.2 | v1.2 **approved for Final Ratification** ([94]); record absent | [89]–[94] | [`rfcs/RFC-0006-capability-model.md`](../../rfcs/RFC-0006-capability-model.md) (v1.2) |
| RFC-0007 Skill Model v1.0 → v1.1 | v1.1 Candidate; v1.2 additions recommended ([98]) | [95]–[98] | [`rfcs/RFC-0007-skill-model.md`](../../rfcs/RFC-0007-skill-model.md) (v1.1) |
| RFC-0008 Memory Model v1.0 | Draft; 15 v1.1 additions recommended ([100]) | [99], [100] | [`rfcs/RFC-0008-memory-model.md`](../../rfcs/RFC-0008-memory-model.md) |

Evolution notes: RFC-0003 v1.1 → v1.2 (extensible revision causes, DAG normativity, topology-preserving replay, memory placement, authority policy in conformance). RFC-0004 v1.0 → v1.1 (GoalID, versioning, terminal states/backward-transition rules, dependency DAG, satisfaction metadata, ownership, memory placement). RFC-0006 v1.0 → v1.1 (CapabilityID, ownership, capability DAG, resolution order, delegation, trace contract, memory placement, conformance) → v1.2 (versioning rule, status transition table, delegated-from, deterministic short-circuit failure, scope immutability, grants/revocations as effect!). RFC-0007 v1.0 → v1.1 (interface contract, status transitions, SkillInvocationID, failure semantics, purity classification, conformance). Parent chain documented in headers: RFC-0003/0004/0007 → RFC-0001; RFC-0005/0006 → RFC-0004; RFC-0008 → RFC-0007 v1.1 (Candidate).

---

## Message #12 additions — RFC lineage (sub-messages [101]–[120])

| Artifact | Version / Status | Origin | Location |
|---|---|---|---|
| RFC-0009 Agent Model v1.0 | Draft; 13 v1.1 additions recommended | [101], [102] | [`rfcs/RFC-0009-agent-model.md`](../../rfcs/RFC-0009-agent-model.md) |
| RFC-0010 Checkpoint and Recovery v1.0 | Draft; 11 v1.1 additions recommended | [103], [104] | [`rfcs/RFC-0010-checkpoint-recovery-model.md`](../../rfcs/RFC-0010-checkpoint-recovery-model.md) |
| RFC-0011 Scheduler v1.0 → v1.1 → v1.2 | **RATIFIED** (document [111], Date 2026-07-29) | [105]–[111] | [`rfcs/RFC-0011-scheduler-execution-model.md`](../../rfcs/RFC-0011-scheduler-execution-model.md), [`rfcs/RFC-0011-ratification-record.md`](../../rfcs/RFC-0011-ratification-record.md) |
| RFC-0011 structure proposal | 14-section outline proposed by [112] before drafting | [112] | archive part 3 |
| RFC-0012 CVM Execution Semantics v1.0 → v1.1 | v1.1 Candidate; final review **APPROVED — Ready for Ratification**; record absent | [113]–[116] | [`rfcs/RFC-0012-cvm-execution-semantics.md`](../../rfcs/RFC-0012-cvm-execution-semantics.md) |
| RFC-0013 CISA v1.0 → v1.1 | v1.1 Candidate; review deems ready for final ratification | [117]–[120] | [`rfcs/RFC-0013-cisa.md`](../../rfcs/RFC-0013-cisa.md) |

Evolution notes: RFC-0011 v1.0→v1.1 (SchedulerID, ScheduleDecision trace, legal transitions, queues, tie-breaking, dependency blocking, scheduler events as effect!, checkpoint integration, hierarchy, conformance) → v1.2 (scheduler versioning rule, queue ownership invariant, richer ScheduleDecision with AgentID/PlanID, WaitingReason model). RFC-0012 v1.0→v1.1 (instruction transaction model §5.1, instruction purity classes §6.1, InstructionID in trace, scheduler/CVM ownership statement). RFC-0013 v1.0→v1.1 (InstructionID + EncodingVersion, register mutability table, instruction transaction section). Parent chain documented in headers: RFC-0009→RFC-0007 v1.1 (Candidate); RFC-0010→RFC-0009; RFC-0011→RFC-0010; RFC-0012→RFC-0011 v1.2 ("Candidate" label preserved although ratified — discrepancy recorded); RFC-0013→RFC-0012 v1.1 (Candidate).

---

## Message #14 additions — RFC lineage (sub-messages [121]–[140])

| Artifact | Version / Status | Origin | Location |
|---|---|---|---|
| RFC-0014 CISA Binary Encoding | v1.0 Draft | [121], review [122] | [`rfcs/RFC-0014-cisa-binary-encoding.md`](../../rfcs/RFC-0014-cisa-binary-encoding.md) |
| RFC-0015 Cognitive Exception Semantics | v1.0 Draft | [123], review [124] | [`rfcs/RFC-0015-cognitive-exception-semantics.md`](../../rfcs/RFC-0015-cognitive-exception-semantics.md) |
| RFC-0016 Cognitive Runtime Architecture | v1.0 Draft | [125], review [126] | [`rfcs/RFC-0016-cognitive-runtime-architecture.md`](../../rfcs/RFC-0016-cognitive-runtime-architecture.md) |
| RFC-0017 Runtime Interface & Service Model | v1.0 Draft | [127], review [128] | [`rfcs/RFC-0017-runtime-interface-service-model.md`](../../rfcs/RFC-0017-runtime-interface-service-model.md) |
| RFC-0018 Event Log & Deterministic Replay | v1.0 Draft | [129], review [130] | [`rfcs/RFC-0018-event-log-replay-protocol.md`](../../rfcs/RFC-0018-event-log-replay-protocol.md) |
| RFC-0019 Cognitive OS Architecture | v1.0 Draft | [131], review [132] | [`rfcs/RFC-0019-cogos-architecture.md`](../../rfcs/RFC-0019-cogos-architecture.md) |
| RFC-0020 Distributed Cognitive Execution | v1.0 Draft | [133], review [134] | [`rfcs/RFC-0020-distributed-execution-protocol.md`](../../rfcs/RFC-0020-distributed-execution-protocol.md) |
| RFC-0021 Cognitive Network Protocol (CNP) | v1.0 Draft | [135], review [136] | [`rfcs/RFC-0021-cognitive-network-protocol.md`](../../rfcs/RFC-0021-cognitive-network-protocol.md) |
| RFC-0022 Cognitive Identity & Trust Framework | v1.0 Draft | [137], review [138] | [`rfcs/RFC-0022-identity-trust-framework.md`](../../rfcs/RFC-0022-identity-trust-framework.md) |
| RFC-0023 Distributed Consensus & Causal Agreement | v1.0 Draft | [139], review [140] | [`rfcs/RFC-0023-consensus-causal-agreement.md`](../../rfcs/RFC-0023-consensus-causal-agreement.md) |

Parent chain documented in headers: RFC-0014→RFC-0013 v1.1 (Candidate); RFC-0015→RFC-0013 v1.1 (Candidate); RFC-0016→RFC-0015 v1.0; RFC-0017→RFC-0016 v1.0; RFC-0018→RFC-0017 v1.0; RFC-0019→RFC-0018 v1.0; RFC-0020→RFC-0019 v1.0; RFC-0021→RFC-0020 v1.0; RFC-0022→RFC-0021 v1.0; RFC-0023→RFC-0022 v1.0. Status snapshot tables preserved in reviews [124]/[126]/[128]/[130]/[140] (temporal-lag pattern per D-44/D-46). Note: [128] contains `entity["operating_system","EROS",…]`/`entity["operating_system","seL4",…]` rendering artifacts — preserved as received.

---

## Message #16 additions — RFC lineage (sub-messages [141]–[160])

| Artifact | Version / Status | Origin | Location |
|---|---|---|---|
| RFC-0024 Resource Management & Quota Model | v1.0 Draft | [141], review [142] | [`rfcs/RFC-0024-resource-management-quota-model.md`](../../rfcs/RFC-0024-resource-management-quota-model.md) |
| RFC-0025 CSPL | v1.0 Draft | [143], review [144] | [`rfcs/RFC-0025-security-policy-language.md`](../../rfcs/RFC-0025-security-policy-language.md) |
| RFC-0026 Hardware Acceleration Model | v1.0 Draft | [145], review [146] | [`rfcs/RFC-0026-hardware-acceleration-model.md`](../../rfcs/RFC-0026-hardware-acceleration-model.md) |
| RFC-0027 Compiler & Toolchain Architecture | v1.0 Draft | [147], review [148] | [`rfcs/RFC-0027-compiler-toolchain-architecture.md`](../../rfcs/RFC-0027-compiler-toolchain-architecture.md) |
| RFC-0028 CIR | v1.0 Draft | [149], review [150] | [`rfcs/RFC-0028-cognitive-intermediate-representation.md`](../../rfcs/RFC-0028-cognitive-intermediate-representation.md) |
| RFC-0029 CIR-SER | v1.0 Draft | [151], review [152] | [`rfcs/RFC-0029-cir-serialization-format.md`](../../rfcs/RFC-0029-cir-serialization-format.md) |
| RFC-0030 Optimization Pass Framework | v1.0 Draft | [153], review [154] | [`rfcs/RFC-0030-optimization-pass-framework.md`](../../rfcs/RFC-0030-optimization-pass-framework.md) |
| RFC-0031 COIL | v1.0 Draft | [155], review [156] | [`rfcs/RFC-0031-coil-transformation-language.md`](../../rfcs/RFC-0031-coil-transformation-language.md) |
| RFC-0032 COVF | v1.0 Draft | [157], review [158] | [`rfcs/RFC-0032-covf-verification-framework.md`](../../rfcs/RFC-0032-covf-verification-framework.md) |
| RFC-0033 CPCPF | v1.0 Draft | [159], review [160] | [`rfcs/RFC-0033-proof-carrying-program-format.md`](../../rfcs/RFC-0033-proof-carrying-program-format.md) |

Parent chain documented in headers: RFC-0024→RFC-0023 v1.0; RFC-0025→RFC-0024 v1.0; RFC-0026→RFC-0025 v1.0; RFC-0027→RFC-0026 v1.0; RFC-0028→RFC-0027 v1.0; RFC-0029→RFC-0028 v1.0; RFC-0030→RFC-0029 v1.0; RFC-0031→RFC-0030 v1.0; RFC-0032→RFC-0031 v1.0; RFC-0033→RFC-0032 v1.0. Sub-numbered proposals preserved as proposals only: RFC-0025.1 Policy VM ([144]), RFC-0026.1 CHAL ([146]), RFC-0034 CPR-TDP ([160]). Review-proposal waves superseded by actual drafting recorded in RFC Index (C-5). Note: [160] contains `[Camera.Read](http://Camera.Read)` auto-link artifact — preserved as received.

---

## Message #18 additions — RFC lineage (sub-messages [161]–[180])

| Artifact | Version / Status | Origin | Location |
|---|---|---|---|
| RFC-0033 CPCPF redraft | v1.0 "Draft (under review)" — near-identical redraft of [159] (D-58) | [161] | archive part 1 (scaffold retains [159]) |
| RFC-0034 CPR-TDP | v1.0 Draft (formal); suggested-scope draft in [162]; identical duplicate in [167] (D-58) | [162], [163], [167] | [`rfcs/RFC-0034-cpr-tdp-package-registry.md`](../../rfcs/RFC-0034-cpr-tdp-package-registry.md) |
| RFC-0035 CSEIM | v1.0 Draft (drafted within review [164]) | [164] | [`rfcs/RFC-0035-cseim-sandbox-isolation.md`](../../rfcs/RFC-0035-cseim-sandbox-isolation.md) |
| RFC-0036 CBR-SCP | v1.0 Draft | [165], review [166] | [`rfcs/RFC-0036-cbr-scp-supply-chain.md`](../../rfcs/RFC-0036-cbr-scp-supply-chain.md) |
| RFC-0037 CSLEMP | v1.0 Draft (drafted within review [166]) | [166] | [`rfcs/RFC-0037-cslemp-lifecycle-evolution.md`](../../rfcs/RFC-0037-cslemp-lifecycle-evolution.md) |
| RFC-0038 CMAEP | v1.0 Draft ([167] first half; duplicated RFC-0034 text truncated at duplication point) | [167], review [168] | [`rfcs/RFC-0038-cmaep-marketplace-economy.md`](../../rfcs/RFC-0038-cmaep-marketplace-economy.md) |
| RFC-0039 CIEOP | v1.0 Draft | [169], review [170] | [`rfcs/RFC-0039-cieop-identity-economy-ownership.md`](../../rfcs/RFC-0039-cieop-identity-economy-ownership.md) |
| RFC-0040 CGCDP | v1.0 Draft | [171], review [172] | [`rfcs/RFC-0040-cgcdp-governance-collective-decision.md`](../../rfcs/RFC-0040-cgcdp-governance-collective-decision.md) |
| RFC-0041 CIFP | v1.0 Draft | [173], review [174] | [`rfcs/RFC-0041-cifp-interoperability-federation.md`](../../rfcs/RFC-0041-cifp-interoperability-federation.md) |
| RFC-0042 CADP | v1.0 Draft (complete [177]; truncated precursor [175] with `<|eos|>` artifact preserved); **RATIFIED** per acknowledgement [179] | [175], [177], [178], [179] | [`rfcs/RFC-0042-cadp-autonomous-deployment.md`](../../rfcs/RFC-0042-cadp-autonomous-deployment.md), [`rfcs/RFC-0042-ratification-record.md`](../../rfcs/RFC-0042-ratification-record.md) |
| RFC-0043 CLS proposal | structure + roadmap proposed | [178], [180] | RFC Index only (no document) |

Parent chain documented in headers: RFC-0034→RFC-0033; RFC-0035→RFC-0034; RFC-0036→RFC-0035; RFC-0037→RFC-0036; RFC-0038→RFC-0037; RFC-0039→RFC-0038; RFC-0040→RFC-0039; RFC-0041→RFC-0040; RFC-0042→RFC-0041. Title-variant notes ([162]/[164]/[166]/[168] proposed alternate titles for 0036/0037/0040/0041) recorded in RFC Index. Note: [165] header quotes curly quotes in §6 ("only accept builds from attested compilers.") — preserved as received.

## Message #21 additions — RFC lineage (sub-messages [181]–[200])

RFC-0043 CLS v1.0 Draft ([181]; Parent RFC-0028) → review [182] (v1.1 recommendations). RFC-0044 CSL: v1.0 Draft ([183]) → review [184] → v1.1 Candidate for Ratification ([185]) → review [186] "Ratification Recommended (with editorial refinements)". RFC-0045 CTDX: v1.0 Draft ([187]) → review [188] → v1.1 Candidate ([189]) → review [190] "Ratification Recommended". RFC-0046 CODP: v1.0 Draft ([191]) → review [192] → v1.1 Candidate ([193]) → review [194] "Ratify" → v1.2 Candidate for Final Ratification ([195]) → review [196] **"Status: Ratified"**. RFC-0047 CPMWS: v1.0 Draft ([197]) → review [198] → v1.1 Candidate ([199]) → review [200] conditional ratification recommendation. All scaffolded verbatim in `rfcs/` (latest ratified/candidate version each; superseded drafts preserved in archive — D-64…D-67).
