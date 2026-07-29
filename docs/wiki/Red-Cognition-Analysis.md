# Red/Cognition — Analysis, Grounding, and Critical Extension

**Source Message:** Fifth user message (Red/Cognition — Analysis, Grounding, and Critical Extension section)

**Stable ID:** RED-COG-ANALYSIS-001

## Overview

Your proposal is not a speculative thought experiment. It sits at the intersection of three active research lineages that have been developing in parallel for decades and are now converging under pressure from production AI agent systems. This document grounds each layer of the proposal rigorously, identifies where it extends known work, and specifies the problems it must still solve.

## I. The Proposal Has Deep Intellectual Predecessors — And They Are Being Revived

The most important context for evaluating Red/Cognition is that **you are not the first to propose this idea**. A thirty-year research tradition called Agent-Oriented Programming (AOP) attempted exactly what you describe — and understanding where it succeeded and where it failed is essential for building the next version correctly.

Agent-oriented programming aims to create autonomous digital agents capable of making intelligent decisions on their own. Traditional programming treats software as passive objects waiting for commands; AOP represents a shift toward more intelligent and proactive systems.

In the area of agent-oriented programming languages, AgentSpeak has been one of the most influential abstract languages based on the BDI architecture. The BDI (Beliefs-Desires-Intentions) architecture is one of the best known approaches to the development of cognitive agents.

The BDI model directly anticipates the proposed primitive types. 2APL provides a rich set of programming constructs allowing direct implementation of concepts such as beliefs, declarative goals, actions, plans, events, and reasoning rules. The reasoning rules allow runtime selection and generation of plans based on declarative goals, received events and messages, and failed plans.

The `goal!`, `plan!`, `belief!`, `memory!` and `policy!` types map almost exactly onto the BDI primitive vocabulary. This is not a coincidence — it is independent convergence on what the domain requires. But the prior art reveals something critical: **BDI languages existed for thirty years without achieving mainstream adoption.** Understanding why is more valuable than simply noting the parallel.

Weaknesses in existing BDI approaches can negatively impact their adoption beyond the agent-oriented programming community. Features extending the basic model provided by AgentSpeak/Jason were discussed with the purpose of improving its adoption for programming and software development.

The failures were specific: BDI languages lacked the ecosystem integration, tooling, debugging infrastructure, and compositional guarantees that production software requires. Red/Cognition must solve those same problems — and it now has something the 1990s BDI researchers did not: **production LLM inference as the reasoning engine**.

## II. The Language of Thought — Formal Cognitive Science Grounding

The `reason` block — turning a structured block into a reasoning graph rather than ordinary control flow — connects to a deep and now actively researched thesis in cognitive science.

The modern interpretation of the "Language of Thought" (LoT) hypothesis posits that many aspects of thinking and learning can be modeled as writing and executing code in some general-purpose programming language. In other words, the mind might contain operations like variable manipulation, conditional branching, and recursions, and can leverage appropriate data structures and algorithms in response to task demands.

Programs provide more versatile and flexible representations of knowledge and skills compared to other formalisms like logical formulas and graphical models.

This gives the proposal an unexpected theoretical foundation. If the Language of Thought hypothesis is correct — that reasoning is fundamentally code-like — then a language whose syntax *is* the reasoning structure is not a convenience feature. It is **architecturally aligned with how cognition actually works**. The homoiconic block:

```red
reason [
    if confidence < 80% [gather-more-evidence]
    compare alternatives
    estimate cost
    choose best-plan
]
```

is not just readable code. Under the LoT hypothesis, it is a plausible *representation of a mental act* — which is precisely why it reads more naturally than an equivalent Python implementation.

Language agents have demonstrated the power of programming languages as a general representational device. Most agent frameworks using these techniques can be described by a template where a reasoner (an LLM) generates code and an interpreter is a system that executes the code.

Red/Cognition would collapse this two-component model into one: the block *is* the reasoning representation *and* the execution unit simultaneously, without the translation layer between them.

## III. AgentSpec — Runtime Enforcement Is Already Being Formalised Declaratively

The capability-based execution proposal — routing every action through permissions, policy, risk, sandbox, and audit trail — now has a direct formal parallel in ICSE 2026 research.

AgentSpec is declarative and externalized from the LLM, ensuring consistent behavior across runs, environments, and model versions. This decoupling avoids brittleness from prompt engineering or fine-tuning and enables transparent inspection and auditing of enforced rules.

Enforcement strategies like `llm_self_examine` allow agents to recover from violations by reflecting on their intentions or re-deriving subgoals, enhancing both robustness and task continuity.

Compare the proposed:

```red
execute [
    delete %temp/
]
; Runtime checks: permissions, policy, risk, sandbox, audit trail
```

to AgentSpec's model: a declarative specification, externalized from the reasoning engine, that intercepts every action and enforces policy. The architectural idea is identical. The difference is that the proposal embeds the policy language *into* the host language as a dialect, rather than as a separate specification layer bolted on externally.

This is the key claim for Red/Cognition's dialect system: **a policy dialect is more composable than an external policy specification**, because it can be inspected and modified by the same runtime that uses it.

## IV. The Declarative Goal — A Critical Distinction

The framework uses `goal` as a primitive without distinguishing between two fundamentally different types of goals that the AOP literature spent decades formalising. This distinction is not academic — it determines whether the runtime can verify completion.

In GOAL (Goal Oriented Agent Language), the key concept is that of declarative goals. This contrasts with goals in languages such as AgentSpeak and 3APL. In those languages, a goal is in effect a plan, as it represents the desire of an agent to perform some action. In contrast, a declarative goal represents a desired state to be brought about. The use of declarative goals enables modal logic to specify and verify agent programs.

The `goal analyse-log` example sits between these two categories — it contains procedural steps (observe, extract, summarize) but is named as a declarative intent. A more rigorous Red/Cognition would distinguish them:

```red
; ACHIEVEMENT GOAL — declarative: desired end state
achieve [
    repository: analysed
    report: generated
    errors: documented
]

; PROCEDURAL GOAL — imperative: sequence of steps
plan analyse-log [
    observe %server.log
    extract errors
    summarize
    verify
]
```

Agents may have multiple goals that specify what the agent wants to achieve at some moment in the near or distant future. Declarative goals specify a state of the environment that the agent wants to establish — they do not specify actions or procedures for how to achieve such states.

This distinction matters for the runtime. A declarative goal can be *satisfied* (the runtime checks whether the desired state is true). A procedural goal can only be *completed* (the steps were executed). When a declarative goal is satisfied by a path the programmer did not specify, that is a feature. When a procedural goal is interrupted, the runtime must handle partial completion. These require different semantics in the `goal!` type.

## V. The Production Convergence — Declarative Agents Are Already Mainstream

The proposal is not merely theoretical — it describes a design direction the industry has already independently adopted for agent construction.

In the fully managed (declarative) approach, you write a structured specification of the desired behavior, and a managed-agent platform runs the agent and the production stack around it. You define the *what* in a structured spec and let the managed-agent platform handle the *how*. You describe behavior in natural language; the platform runs the agent and the production stack around it.

You describe the rules, schemas, and goals in a single document. The platform handles orchestration, observability, model routing, deployment, and the lifecycle of the agent itself. Every agent, regardless of how it's built, is assembled from the same fundamental pieces: instructions, a reasoning loop, tools, and guardrails.

Red/Cognition would take this observation seriously at the language level: instead of describing agent behaviour in *natural language inside a Python string* (the current dominant approach), you describe it in *structured, executable Red blocks* that the runtime can inspect, transform, and verify — not just evaluate blindly.

By 2026, most agentic coding systems have converged on a set of common architectural primitives and capabilities. This standardisation allows for more predictable interactions and integrations across different platforms. Agents maintain long-term memory of a project's goals, conventions, and architecture through dedicated files — allowing them to retain context across sessions lasting days or weeks.

The `remember` and `recall` primitives directly address this — but by making them language-level primitives rather than file-based conventions (`AGENTS.md`, `CLAUDE.md`), Red/Cognition would make memory a *typed, queryable, runtime-verified resource* rather than a document convention that is silently ignored when the context window overflows.

## VI. The Multi-Model Reasoning Proposal — Now Confirmed as Standard Architecture

The `reason using small-model`, `reason using planner`, `reason using verifier` syntax describes a routing architecture that has become the production standard.

The Agents SDK provides simple primitives: Agent (an LLM plus instructions and tools that can think and act), Runner (a loop that executes the agent on an input, invoking tools and repeating until termination), and Handoffs (a built-in way for one agent to delegate a conversation to another agent).

The proposal elegantly collapses this multi-component model into unified language syntax. Instead of instantiating three separate agent objects with different model configurations and wiring handoffs between them, Red/Cognition expresses model routing as a first-class language construct:

```red
reason using small-model [    ; fast, cheap, local
    classify message
]
reason using planner [        ; structured, multi-step
    build execution graph
]
reason using verifier [       ; critical, high-confidence
    check consistency
]
```

The significant insight here is that `using` is not just a model selector — it is a **capability declaration**. The runtime knows before execution which model tier is required, which means it can budget, schedule, and gate the operation through the policy layer before the first token is generated. This is architecturally superior to frameworks where model selection is a runtime side-effect of tool calling.

## VII. The Three Critical Problems Red/Cognition Must Solve

Grounding in the prior art now makes the unsolved problems precise. There are three, and they are structurally different from each other.

### Problem 1: The Semantic Type System — What Does `belief!` Mean Formally?

The new primitive types are named but not specified. A `belief!` in BDI theory carries specific formal semantics: beliefs represent the agent's knowledge about the world, itself, and other agents. But a belief can be true, false, outdated, uncertain, or contradicted. A string in Red is just a string — it has no truth value. A `belief!` type must carry:

```
belief! = {
    content:     any value
    confidence:  float [0.0–1.0]
    source:      agent | sensor | inference | memory
    timestamp:   datetime
    valid-until: datetime | none
    contradicts: [belief! ...]
}
```

Without this structure, `believe` is just a renamed map entry, and the runtime cannot reason about its epistemic status. The type system must make the *cognitive properties* of values inspectable — not just their data structure.

### Problem 2: The Plan Selection Problem — How Does the Runtime Choose?

The `goal analyse-log` block specifies *what to do* but not *which plan to use when multiple plans could achieve the same goal*. This is the central unsolved problem of BDI systems. A plan is linked to an agent's goal and will only be considered when the agent holds that goal. To adopt the plan, the plan's guard conditions must be satisfied — these typically represent the agent's beliefs. Once adopted, the actions are executed in sequence. If multiple plans can be adopted, AgentSpeak will select one for execution.

Red/Cognition requires a plan selection semantics. When the runtime encounters:

```red
goal analyse-log [...]
```

and multiple plans exist that could satisfy it, it needs a selection mechanism. Options include:

- **Priority ordering** — first applicable plan wins
- **Utility scoring** — plans are evaluated by expected cost/confidence
- **LLM selection** — the reasoning engine selects the most appropriate plan

Each has different failure modes. Priority ordering is deterministic but brittle. Utility scoring requires a cost model. LLM selection is flexible but non-deterministic and expensive. Red/Cognition needs to specify which mechanism is the default and how the programmer can override it.

### Problem 3: The Failure Handling Gap — What Happens When a Goal Cannot Be Achieved?

The framework describes the happy path beautifully. It does not specify failure semantics. Classical BDI systems found this to be their hardest problem: a key characteristic is the configuration option for what to do when there is no applicable plan for a relevant event. If an event is relevant, it means there are plans in the agent's plan library for handling it. If none of those plans are applicable, this can be a problem as the agent does not know how to handle the situation.

Red/Cognition needs an explicit failure handling model for every cognitive primitive:

```red
goal analyse-log [
    observe %server.log
    extract errors
    summarize
    verify
]
on-failure [
    retry with-model large-remote
    escalate to human
    record-failure in memory
    abandon with-reason "verification-failed"
]
```

Without this, a failed cognitive goal silently propagates incorrect state into memory — which is categorically worse than a classical exception, because incorrect beliefs contaminate all subsequent reasoning built on them.

## VIII. The Complete Red/Cognition Type System — Extended

Drawing together the proposal, the BDI tradition, and current production requirements, a complete `belief!`-anchored type system can be specified:

```
; EPISTEMIC TYPES — carry truth and confidence
belief!      — what the agent holds to be true (with confidence)
hypothesis!  — belief with confidence below threshold for action
evidence!    — observation that updates belief confidence
observation! — raw sensory or API input, not yet interpreted

; INTENTIONAL TYPES — carry goal structure
goal!        — desired end state (declarative)
plan!        — sequence of steps toward a goal (procedural)
intention!   — a plan the agent has committed to executing
capability!  — an action the agent is permitted to take

; TEMPORAL TYPES — carry validity windows
memory!      — past experience with timestamp and validity
skill!       — compiled procedural knowledge with performance history
episode!     — bounded sequence of events forming a narrative unit

; NORMATIVE TYPES — carry policy and constraint
policy!      — a rule governing agent behaviour
permission!  — a granted capability with scope and expiry
event!       — a trigger binding world-state change to response
```

The key property distinguishing these from plain Red values is that **each type carries cognitive metadata** — confidence, validity, source, scope — that the runtime can interrogate before executing any action that depends on it. A plan built on a `belief!` with confidence 0.23 should behave differently from one built on confidence 0.97. That distinction must be enforced by the type system, not left to the programmer to check manually.

## IX. The Full Three-Layer Stack — With Inter-Layer Contracts Specified

The three-layer table is correct but incomplete without specifying what crosses each boundary:

```
┌──────────────────────────────────────────────────────────────────┐
│                    Red/Cognition                                  │
│   goal! plan! belief! memory! skill! observation! hypothesis!    │
│   policy! evidence! event! capability! intention! episode!        │
│                                                                   │
│   Primitives: observe() reason() plan() act() reflect()          │
│               remember() recall() forget() delegate() verify()   │
│                                                                   │
│   Semantics: Declarative goals, BDI mental attitudes,            │
│              Confidence-weighted belief, Temporal validity        │
├──────────────────────────────────────────────────────────────────┤
│           INTER-LAYER CONTRACT: Cognitive Pipe Protocol          │
│   Downward: goal! → plan! → function call + policy check         │
│   Upward:   result + confidence + provenance + reflection        │
├──────────────────────────────────────────────────────────────────┤
│                       Red Language                                │
│   integer! string! block! object! function! dialect!             │
│                                                                   │
│   Homoiconic blocks carry Red/Cognition types transparently      │
│   Dialects implement: reason, plan, observe, remember, execute   │
│   Parse dialect validates cognitive type structure               │
├──────────────────────────────────────────────────────────────────┤
│           INTER-LAYER CONTRACT: Capability Binding               │
│   Downward: Red function → Red/System native call + sandbox      │
│   Upward:   result + exit status + resource consumption          │
├──────────────────────────────────────────────────────────────────┤
│                       Red/System                                  │
│   Memory · Pointers · Native Code · OS calls                     │
│   Provides: execution substrate, I/O, timing, process control    │
└──────────────────────────────────────────────────────────────────┘
```

The inter-layer contracts are the engineering work that makes the philosophy concrete. Every value crossing the boundary from Red/Cognition downward must shed its cognitive metadata and become a typed Red value. Every result crossing upward must acquire confidence, provenance, and validity metadata before the cognitive layer can act on it.

## X. The Complete Example — Annotated Against the Full Architecture

The Repository Assistant example is worth re-examining with the full type system in view:

```red
agent "Repository Assistant" [
    ; IDENTITY — establishes cognitive process scope
    identity [
        name: "Repository Assistant"
        version: 1.0
        permissions: [read-filesystem call-github generate-report]
    ]

    ; WORKING MEMORY — initial beliefs with explicit confidence
    believe [
        project: make belief! [
            content: "OpenClaw"
            confidence: 1.0         ; known with certainty
            source: 'user
        ]
        language: make belief! [
            content: 'Rust
            confidence: 0.95        ; inferred, not verified
            source: 'observation
        ]
    ]

    ; EVENT BINDING — declarative trigger
    when github.push [

        ; OBSERVATION — raw input, not yet interpreted
        observe make observation! [
            source: 'github
            event: 'push
            payload: github.event-data
        ]

        ; REASONING — structured deliberation with model selection
        reason using planner [
            identify changed modules
            estimate impact
            choose review-strategy
        ]

        ; PLANNING — procedural steps derived from declarative goal
        plan [
            run tests
            inspect architecture
            summarize changes
        ]

        ; ACTION — capability-gated execution
        act [
            generate report        ; requires: generate-report capability
        ]

        ; REFLECTION — compares prediction against outcome
        reflect [
            compare prediction with results
            if divergence > 0.2 [
                update beliefs
                record episode
            ]
            remember lessons       ; promotes to semantic memory
        ]
    ]
]
```

What this example demonstrates — that prior BDI languages never achieved — is that **the agent specification is simultaneously human-readable, machine-executable, and runtime-inspectable**. A BDI system in Jason requires the programmer to maintain beliefs, goals, and plans in separate files with separate syntaxes. A Red/Cognition agent carries all three in a single block structure that the runtime can traverse, modify, and verify as a data structure before, during, and after execution.

## XI. The Synthesis: What Red/Cognition Is, Precisely

Pulling the full analysis together, Red/Cognition is precisely definable against the prior art:

| Dimension                  | BDI / AgentSpeak          | Current Python Frameworks | Red/Cognition |
|----------------------------|---------------------------|---------------------------|---------------|
| Cognitive primitive types  | ✅ Formal BDI             | ❌ Python objects         | ✅ Native types |
| Homoiconic plan representation | ❌ Separate syntax     | ❌ Python AST             | ✅ Same block structure |
| Declarative goal semantics | ✅ Formal                 | ⚠️ Natural language       | ✅ Typed with verification |
| Runtime policy enforcement | ⚠️ Limited                | ⚠️ External (AgentSpec)   | ✅ Dialect-embedded |
| Multi-model routing        | ❌ None                   | ✅ Framework-dependent    | ✅ First-class syntax |
| Ecosystem integration      | ❌ Academic only          | ✅ Vast                   | ⚠️ Unsolved |
| Failure handling semantics | ⚠️ Configuration option   | ❌ Exception-only         | 🔲 Needs specification |
| Temporal belief validity   | ❌ None                   | ❌ None                   | 🔲 Needs specification |
| Confidence-weighted types  | ❌ None                   | ❌ None                   | ✅ Proposed, needs formal semantics |

Red/Cognition is the intersection of three things that have never existed simultaneously in one language: the **formal cognitive type system** of BDI languages, the **homoiconic composability** of Red's dialect architecture, and the **production LLM inference capability** that 1990s BDI researchers never had access to.

The prior art failed because reasoning engines were either too weak (rule-based) or too expensive (expert systems). The current Python frameworks succeed on ecosystem but fail on cognitive composability. Red/Cognition's claim is that **composability is not a convenience feature** — it is the architectural property that makes cognitive programs inspectable, verifiable, and safe to run autonomously. That is the claim worth building toward.

---

**Traceability:** All content extracted verbatim from the analysis section of the fifth user message. No information added or inferred.