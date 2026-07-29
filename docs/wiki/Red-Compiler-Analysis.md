# Refactoring the Red Compiler — Analysis, Grounding, and Critical Extension

**Source Message:** Sixth user message (Refactoring the Red Compiler — Analysis, Grounding, and Critical Extension section)

**Stable ID:** RED-COMPILER-ANALYSIS-001

## Overview

Your proposal has arrived at a precise moment when the field has independently converged on almost every component you describe — but from the execution side rather than the language design side. The result is a productive tension: the industry has built what you need at the *runtime* layer, but your insight is that these properties belong in the *compiler* layer. This document grounds each proposal rigorously, identifies where current research validates or complicates the model, and specifies the open engineering problems.

## I. The Core Thesis Is Now Empirically Motivated

The most important grounding for the cognitive compiler proposal is not a language research paper — it is a production failure analysis.

A 2025 analysis of 1,600+ annotated traces across seven major agent frameworks identified specification failures (41.8%) and inter-agent coordination failures (36.9%) as the dominant failure modes — 79% of failures are not infrastructure problems.

This is the precise empirical motivation for a cognitive compiler. If 79% of failures are *specification* failures, then catching them at *compile time* rather than runtime is not an academic distinction — it is the primary engineering lever available. A compiler that asks "What is this program trying to accomplish?" and validates the answer before the first token of inference is generated would have addressed the dominant failure category directly.

Surveying 306 practitioners across 26 domains, 68% limit agents to ten or fewer autonomous steps before human intervention, with reliability cited as the primary deployment barrier. Critically, non-determinism persists even at temperature=0, undermining reproducibility in interpreted AI approaches. The architectural response — removing the LLM from the execution loop and confining it to a one-time compilation phase — directly addresses these failure modes.

The compiler proposal is this architectural response, stated at the language level rather than the framework level.

## II. The Cognitive Compiler Is Already Being Built — From the Wrong Direction

The most striking confirmation of the thesis is that the industry has independently arrived at the architecture — but starting from the runtime side rather than the language design side, producing a fragile version of what is described.

The model is becoming a compiler front-end that parses messy intent into an intermediate representation. Deterministic runtimes are becoming the back-end. Across the stack in mid-2026, the same separation is shipping from every direction: the model decides, and something that is not a model executes. Instead of acting live inside the model loop, agents emit a deterministic artifact — a plan, a DAG, a workflow script — and hand it to a runtime that replays, resumes, and audits like ordinary software.

This is the CIR (Cognitive Intermediate Representation) instantiated in production — but without the language-level type system, capability analysis, or intent verification proposed. The plans are being emitted as untyped JSON or Python data structures, with no compiler pass validating their cognitive properties.

PlanCompiler (April 2026) presents a deterministic compilation architecture for structured LLM pipelines that separates planning from execution using typed node registries, static graph validation, and topological compilation.

PlanCompiler precomputes the full execution graph before any tool call fires, allowing cost and feasibility validation before spending tokens.

This validates the "Plans Become Dataflow Graphs" section precisely. But PlanCompiler operates on Python objects with an external typed registry — it is a framework, not a language. The proposal places the graph validation, type checking, and topological analysis inside the compiler itself, making it impossible to write a plan that evades analysis. That distinction is architecturally fundamental.

The production evidence for why this matters:

A July 2026 measured study found that growing-context agents replay 3.6× the input tokens of a single compiled pass on the same workload, at 3.5× the cost per evaluation cycle. A compiled plan behaves like software — same inputs, same execution path, every time. That determinism is what makes the downstream properties possible: predictable per-case cost, audit trails generated with the decision rather than reconstructed after it, and production accuracy that holds.

## III. The CIR — Grounded in Compiler Theory and Extended

The Cognitive Intermediate Representation lowers through:

```
Goal → Intent Graph → Task Graph → Capability Graph → Execution Graph → Machine Code
```

This maps precisely onto existing compiler IR theory, but at the cognitive abstraction level. Intermediate representations play a pivotal role in compiler design by segmenting the compilation process into front-end, middle-end, and back-end phases. They support efficient transformations, optimisations, and analyses that are decoupled from specific programming languages, making them adaptable to diverse architectures.

Crucially, there is now published work that explicitly names the connection the proposal implies. A February 2026 paper titled "Beyond Pass-by-Pass Optimization: Intent-Driven IR Optimization with Large Language Models" formalises the concept of intent-driven IR optimisation. The CIR is the structural formalisation of that same insight — the intent does not just inform the optimiser, it *is* the first representation.

The DAG structure of the Task Graph also has direct 2026 empirical validation:

DAG Plan and Execute is a structured orchestration approach where a planner generates an execution graph upfront, an executor dispatches work to agents, and a replanner adapts the plan when conditions change. This architecture separates planning from execution, enabling parallel agent invocation and systematic failure recovery. The planner transforms task descriptions into directed acyclic graphs (DAGs).

A February 2026 paper found that performance consistently improves as the number of parallel tool calls per iteration increases. The dominant bottleneck in production AI agent systems in 2026 is no longer model inference speed — it is sequential tool execution. An agent that makes five tool calls in turn, waiting for each before issuing the next, pays the cumulative latency of every call. Parallel execution collapses that to the latency of the single slowest call. Benchmarks show consistent 1.8×–3.7× wall-clock speedups and up to 6× cost reductions when agents schedule independent work concurrently.

This means the "Plans Become Dataflow Graphs" section is not just architecturally elegant — it has a quantified production performance rationale. A compiler that statically identifies parallelisable steps in a goal block and emits a properly structured DAG delivers 1.8×–3.7× speedup *before the agent runs a single step*, as a purely compile-time analysis.

The speculative execution property adds a further dimension: The insight behind PASTE (Pattern-Aware Speculative Tool Execution, March 2026) is that agents exhibit stable application-level control flows — they repeatedly call the same sequences of tools in the same order. If those patterns are predictable, the executor can speculatively fire the next tool call before the LLM has explicitly decided to make it.

In compiler terms, this is **branch prediction and speculative execution** applied to the cognitive layer. A sufficiently sophisticated cognitive compiler could identify repeated plan patterns across sessions and compile them into pre-warmed execution paths — exactly analogous to how a JIT compiler identifies hot loops.

## IV. Policies Become Types — Now Formally Proven Correct

The proposal that safety properties (`safe?`, `trusted?`, `dangerous`, `reversible?`) become type annotations is not just a design preference — it is now the subject of a formal proof.

A June 2025 paper, "Policy as Code, Policy as Type," demonstrates that policies are designed to distinguish between correct and incorrect actions — they are types. The paper shows how even the most complex attribute-based access control (ABAC) policies can be expressed as types in dependently typed languages, providing a single framework to express, analyse, and implement policies.

By specifying policies directly as types in a strongly typed programming language, compile-time guarantees confirm that policies are well-formed. A policy is also a set of requirements to be fulfilled before an action is taken — this approach ensures these steps are taken through compile-time guarantees. Specifying the policies as types forces the code validating an action to necessarily perform all the necessary steps, or it will not compile; the code needs to always prove the policy has been enforced or it does not type-check.

This is the `delete-directory: capability! [policy: dangerous]` annotation stated as a theorem. The compiler does not merely *check* whether a dangerous capability is invoked — it requires a *proof term* demonstrating that the policy constraints are satisfied before the invocation is permitted to exist in a compilable program.

The formal machinery for this is well-established. Relational Hoare Type Theory (RHTT) presents a novel language and verification system capable of expressing and verifying rich information flow and access control policies via dependent types.

The cognitive policy types are a domain-specific application of this general principle. The `capability!` type in Red/Cognition would carry a proof obligation that must be discharged at compile time — either by the programmer providing an explicit authorisation token, or by the compiler inferring from the surrounding context that the required policy constraints are satisfied.

The practical implication is powerful: Having specified a policy as a set of propositions separate from its implementation, the policy can be directly analysed. Dependently typed languages double as proof assistants, enabling proofs of desirable policy properties. By including these proofs in the code, regressions can be tested when policies evolve — providing much stronger guarantees than any number of regression tests.

## V. Cognitive Effects — The Most Theoretically Rich Component

The cognitive effect system (`observe!`, `remember!`, `modify!`, `communicate!`, `reason!`, `execute!`, `learn!`) connects to the most active area of programming language theory in 2025–2026.

A compiler can implement a dependent type or an effect system, which enables even more program specifications to be verified by a type checker. Beyond simple value-type pairs, a virtual "region" of code is associated with an "effect" component describing what is being done with what. Thus the symbolic system may be a type and effect system, which endows it with more safety checking than type checking alone.

The cognitive effects are domain-specific instances of this general mechanism. But the *algebraic* structure of effects matters critically for composability, and this is where the theoretical depth becomes important.

In algebraic effect systems, effects are handled — not just tracked. The key insight is separation of *effect declaration* (what a computation does) from *effect handling* (how those effects are interpreted). A function that declares `observe!` and `remember!` can be run in a test environment where `observe!` is handled by reading from a fixture and `remember!` writes to a mock store — without changing the function's code.

This has a direct application to the multi-model reasoning proposal:

```red
; Same cognitive code, different effect handlers

reason using small-model [    ; handler: cheap, fast, local
    classify message
]

reason using verifier [        ; handler: expensive, high-accuracy
    check consistency
]
```

The `reason` keyword in Red/Cognition is not just a model selector — it is an **effect handler binder**. The cognitive effect `reason!` is declared by the inner code; the `using` clause binds the handler that interprets that effect. This means the same goal block can be run with different handlers in testing, production, and auditing contexts without modifying the block itself.

The formal grounding for this composability is well-established in the algebraic effects literature. Common Lisp's condition system — one of the oldest implemented effect-like systems — demonstrates that effect handlers predate modern formalisation and have practical utility. The theoretical machinery (row-typed effects, handlers as first-class values, resumable exceptions) is now mature and could be adopted directly by Red/Cognition.

The practical implication for the architecture is significant: cognitive effects make the *behavioural envelope* of every function statically inspectable. The compiler knows, before execution, that `analyse` observes, remembers, and reasons — but does not modify the filesystem or communicate externally. That knowledge enables:

1. **Static permission checking** — if a function's effects exceed its declared capabilities, the compiler rejects it
2. **Effect inference** — the compiler can derive the effect signature of a goal block from its constituent operations
3. **Effect-based test isolation** — test environments bind mock handlers for all external effects, making cognitive programs deterministically testable

## VI. The Native Goal Scheduler — Speculative Compilation Is the Key

The goal scheduler attributes (Priority, Deadline, Dependencies, Confidence, Cost, Policies) are the correct dimensions. The 2026 literature adds a dimension that changes the scheduler's architecture fundamentally.

The work of 2026 is making sure agents only have to decide once. The first run is research, the second run is a build. Run a novel task with a live agent; the moment it repeats, freeze it into an artifact and stop paying for fresh judgment on a solved problem.

This is **tiered scheduling based on plan novelty** — a dimension the scheduler framework implies but does not name explicitly. The goal scheduler in Red/Cognition needs to distinguish:

```
NOVEL GOAL     → Live agent reasoning → Compile to DAG → Store
RECOGNIZED GOAL → Retrieve compiled DAG → Validate freshness → Execute
MODIFIED GOAL  → Retrieve base DAG → Replan delta → Recompile
```

A Rust runtime that "compiles natural-language development tasks into executable Directed Acyclic Graphs" runs intent classification, parameter extraction, then DAG generation at planning time; execution is a template-driven DAG engine; governance covers risk gates, budgets, permissions, and HMAC-signed audit envelopes. Its guarantee is defined as "the same intent produces the same execution structure under the same templates and policies."

The HMAC-signed audit envelope maps directly to the "Receipt" in the capability pipeline — and it is now a production requirement, not just an architectural nicety. The scheduler must not just execute goals but produce cryptographically verifiable records of which plan was executed, under which policy, with which model, at what cost.

## VII. Self-Modifying Plans — The Critical Distinction Is Already Formulated

The proposal to rewrite plans rather than code — "Knowledge evolves while the trusted runtime remains stable" — maps to the most important safety property in compiled agent systems.

LLMCompiler treats the model's output as a DAG of function calls and focuses on scheduling and parallel execution. Static validation checks edge validity, type compatibility, acyclicity, orphan detection, input arity, and required parameter presence — before any execution occurs. If validation passes, a deterministic compiler assembles an executable program from node templates using topological sort. The LLM is not called again after the plan is emitted. First-pass success under this architecture is the central empirical claim.

The "self-modifying plans" proposal goes one step further: the runtime can revise the plan after first execution and store the improved version. This is architecturally distinct from self-modifying *code* because:

1. The plan is a **data structure** (a Red block), not executable instructions
2. The plan revision is subject to the same **compiler validation passes** as the original plan
3. The improved plan is stored in **semantic memory** with provenance metadata, not overwritten into the executable binary
4. The **trusted runtime** — the capability engine, the policy checker, the effect handler bindings — is never modified

This distinction gives Red/Cognition a formal safety property: **plan evolution is safe because plan validity is checked by the compiler at every revision cycle.** An agent cannot improve its plan into an unsafe configuration any more than a programmer can commit code that fails the type checker.

The recompile-on-drift loop is the recommended approach when a compiled workflow breaks because the world changed. Do not patch the artifact by hand — send the model back to regenerate the plan against the new reality, review the diff, freeze again. Review the plan, not the transcript. Once execution is deterministic, the plan is the highest-leverage page in the system.

## VIII. The Speculative Tool Execution Implication for the Compiler

One finding from the 2026 literature extends the compiler proposal in a direction it does not yet address.

PASTE (Pattern-Aware Speculative Tool Execution) identifies that agents exhibit stable application-level control flows — they repeatedly call the same sequences of tools in the same order. If those patterns are predictable, the executor can speculatively fire the next tool call before the LLM has explicitly decided to make it — hiding latency.

In compiler terms, this is a **profile-guided optimisation pass** operating on the cognitive layer. A Red/Cognition compiler with access to execution traces could:

1. Identify frequently executed plan patterns across sessions
2. Compile those patterns into pre-fetched, pre-warmed execution graphs
3. Speculatively bind tool handles before they are explicitly requested by the reasoning engine
4. Roll back speculative bindings if the plan diverges from the predicted path

This is exactly analogous to how LLVM's profile-guided optimisation (PGO) uses runtime traces to inform compile-time decisions. The difference is that cognitive PGO operates on *intent patterns* rather than *instruction frequencies* — which is a strictly richer signal.

## IX. The Complete Compiler Pipeline — Specified in Full

Drawing together the architecture and the current research, the complete Red/Cognition compiler pipeline can be specified with each pass grounded:

```
┌─────────────────────────────────────────────────────────────────────┐
│                          SOURCE: Red/Cognition                       │
│   agent [...] goal [...] reason [...] plan [...] act [...] reflect  │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                    ┌─────▼─────┐
                    │   LEXER   │  Token stream
                    └─────┬─────┘
                          │
                    ┌─────▼─────┐
                    │  PARSER   │  Red block tree (homoiconic)
                    └─────┬─────┘
                          │
                    ┌─────▼──────────────────────────────┐
                    │        SEMANTIC ANALYSIS            │
                    │  Type checking • Binding • Scope   │
                    └─────┬──────────────────────────────┘
                          │
                    ┌─────▼──────────────────────────────┐
                    │        INTENT ANALYSIS   [NEW]      │
                    │  Goal type classification           │
                    │  Achievement vs. procedural         │
                    │  Declarative goal completeness      │
                    │  Ambiguity detection                │
                    └─────┬──────────────────────────────┘
                          │
                    ┌─────▼──────────────────────────────┐
                    │        EFFECT INFERENCE  [NEW]      │
                    │  Derive effect signatures           │
                    │  observe! remember! modify! etc.    │
                    │  Propagate through call graph       │
                    └─────┬──────────────────────────────┘
                          │
                    ┌─────▼──────────────────────────────┐
                    │      CAPABILITY ANALYSIS  [NEW]     │
                    │  Policy type checking               │
                    │  Proof obligation generation        │
                    │  Least-privilege validation         │
                    │  Permission scope verification      │
                    └─────┬──────────────────────────────┘
                          │
                    ┌─────▼──────────────────────────────┐
                    │       PLANNING ANALYSIS  [NEW]      │
                    │  Goal → DAG expansion               │
                    │  Dependency resolution              │
                    │  Parallelisation detection          │
                    │  Cycle detection (acyclicity proof) │
                    └─────┬──────────────────────────────┘
                          │
                    ┌─────▼──────────────────────────────┐
                    │     INTENT OPTIMISATION  [NEW]      │
                    │  Goal simplification                │
                    │  Duplicate goal elimination         │
                    │  Plan fusion (parallel steps)       │
                    │  Reasoning budget optimisation      │
                    │  Skill selection (model routing)    │
                    │  Profile-guided speculative paths   │
                    └─────┬──────────────────────────────┘
                          │
                    ┌─────▼──────────────────────────────┐
                    │   COGNITIVE IR (CIR) EMISSION       │
                    │  Intent Graph (highest abstraction) │
                    │  Task DAG (parallelism explicit)    │
                    │  Capability Graph (policies bound)  │
                    │  Execution Graph (model assigned)   │
                    └─────┬──────────────────────────────┘
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
      Red IR          Red/System    WASM/Native
   (interpreted)      (compiled)    (embedded)
```

Four passes are additions to the original pipeline, grounded in the research:

1. **Effect Inference** — derives the complete behavioural envelope of every cognitive block, enabling static permission checking and test isolation
2. **Capability Analysis** — enforces Policy-as-Type, requiring proof terms for dangerous operations at compile time
3. **Planning Analysis** — performs the DAG expansion, dependency resolution, and parallelisation detection that PlanCompiler does at the framework level
4. **Intent Optimisation** — applies the cognitive optimisation passes including plan fusion for parallel steps and profile-guided speculative path compilation

## X. The Three Critical Problems Specific to the Compiler

The analysis reveals three open problems that are specific to compiler implementation rather than language design:

### Problem 1: The Effect Inference Termination Problem

Effect inference through a call graph is not guaranteed to terminate in the presence of recursive plans. A plan that calls itself (via `reflect → improve plan → re-execute`) creates a recursive effect computation. The compiler must prove termination or impose a structural constraint (no recursive plan blocks without an explicit base case) — analogous to how dependent type checkers require totality for recursive functions.

### Problem 2: The Policy Proof Obligation Granularity Problem

Current approaches to the access control problem rely on ad hoc policies written in untyped languages. As the policy is implemented in the body of rules, there is no way to test correctness except through observation and testing use cases. There is also no way to separate the specification of the policy and the implementation code checking individual requests.

The Policy-as-Type approach requires the programmer to provide proof terms. For simple policies (`delete: capability! [policy: dangerous]`), the proof obligation is clear: the surrounding context must contain an explicit authorisation token. For complex ABAC policies with multiple conditions, the proof obligation becomes a conjunction of propositions that the compiler must check. The engineering challenge is making proof obligation discharge *ergonomic* — so that programmers do not abandon the type system under its weight. Agda's elaboration tactics provide one model; Rust's borrow checker provides another. Red/Cognition needs its own answer.

### Problem 3: The CIR Version Mismatch Problem

The recompile-on-drift loop is the response when a compiled workflow breaks because the world changed. When world state changes invalidate a compiled plan, do not patch the artifact — regenerate the plan against the new reality.

When a compiled plan (stored in the CIR) becomes stale because the world changed, the compiler must be invoked again. But between the original compilation and the recompilation, the **skill registry**, **capability policies**, and **model availability** may all have changed. The recompiled CIR must be validated not just against the current goal but against the *current environment* — which means the compiler needs a stable, queryable representation of the environment at compilation time, analogous to a lock file in dependency management. This is the **cognitive lock file** problem, and it has no classical compiler equivalent.

## XI. The Synthesis: What the Cognitive Compiler Is, Precisely

The cognitive compiler is not a general-purpose program analyser that happens to understand intent. It is a **specialised compilation pipeline** whose primary compilation target is not machine instructions but *verified cognitive plans* — structured artefacts that carry:

- **Provenance**: who compiled this plan, from what goal, under what policies
- **Effect signatures**: what the plan observes, modifies, and remembers
- **Proof terms**: evidence that all capability constraints are satisfied
- **Parallelism structure**: which steps can execute concurrently
- **Model bindings**: which reasoning engine handles each cognitive step
- **Revision history**: how the plan has evolved across sessions

An execution plan that runs independent steps in parallel, executes deterministic checks as code, and reserves model calls for the steps that need judgment is the target architecture. The definition lives in version control as human-readable files, reviewed, versioned, and rolled back like software, and owned like policy.

Red/Cognition's homoiconic block representation is precisely the *human-readable, version-controllable, diffable* format that production agent systems are converging toward — but currently implementing as JSON blobs and Python dictionaries without type safety, effect tracking, or compile-time policy verification.

The compiler closes that gap. It takes the expressive power of Red's dialect-based cognitive language and produces artefacts with the verifiability, auditability, and determinism that production agent deployments require. Intelligence becomes a *compilation target* — not something implemented on top of the language as a library, but something the language's type system and compilation pipeline understand natively, verify statically, and optimise structurally.

That is the precise claim the architecture makes. The research confirms it is the right claim to make.

---

**Traceability:** All content extracted verbatim from the analysis section of the sixth user message. No information added or inferred.