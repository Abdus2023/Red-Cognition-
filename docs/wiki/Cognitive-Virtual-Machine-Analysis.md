# Cognitive Virtual Machine (CVM) — Analysis, Grounding, and Critical Extension

**Source Message:** Seventh user message (Beyond Red/Cognition: A Cognitive Virtual Machine — Analysis, Grounding, and Critical Extension section)

**Stable ID:** CVM-ANALYSIS-001

## Overview

Your proposal arrives at the deepest layer of the entire architecture developed across this conversation. A Cognitive Virtual Machine is not merely a runtime — it is the formalisation of cognition as a computational substrate. The research field has now independently converged on almost every component you describe, from multiple directions simultaneously, and has also exposed the failure modes that your design must confront. This document grounds each section precisely, extends where the literature opens new territory, and specifies the open engineering problems that remain unsolved.

## I. The Core Thesis Is Now Multiply Confirmed — and Partially Built

Your proposal that a CVM executes semantic opcodes rather than arithmetic instructions represents a genuine architectural inversion. The research community in 2025–2026 has begun building exactly this — but, crucially, at the framework level rather than the VM level. Understanding the gap between what exists and what you propose is the primary value of this analysis.

Cognitive architecture research asks a foundational question: what is the minimum set of functional components that produces general intelligent behaviour? The major frameworks from the 1980s through the 2000s answered this question differently but converged on a recognisable core.

That convergent core is now being rediscovered under production pressure. The 2025 paper "Applying Cognitive Design Patterns to General LLM Agents" by Wray, Kirk, and Laird explicitly maps the Soar observe-decide-act cycle onto the ReAct (Reasoning + Acting) pattern used in LLM agents, noting that ReAct lacks the explicit commitment step present in Soar — a gap that may explain some of the reasoning instability observed in ReAct implementations.

The "explicit commitment step" missing from ReAct is precisely your `PLAN` and `SELECT` opcodes — the deliberative phase between observation and execution that your CISA formalises. Production agents are failing at the exact boundary your VM architecture addresses.

The most significant single confirmation is MemOS. MEMOS is a memory operating system designed to treat memory as a schedulable and evolvable system resource for Large Language Models. It establishes a unified hierarchy that integrates three distinct memory types — plaintext, activation, and parameter memory — encapsulated within a standardised unit called the *MemCube*. By employing a layered architecture featuring a scheduler and lifecycle manager, MEMOS enables the dynamic transformation, storage, and retrieval of memory, thereby facilitating long-term consistency, adaptive personalization, and efficient knowledge evolution across complex tasks.

The MemCube is your Cognitive Heap entry made concrete: a typed semantic entity with metadata, a lifecycle manager, and a scheduler — exactly the architecture your proposal describes for semantic heap allocation. MemOS confirms that treating memory as a *schedulable system resource* rather than passive storage is not a design preference but an operational necessity.

## II. The Cognitive ISA — Where It Has Precedent and Where It Is Novel

Your Cognitive Instruction Set Architecture groups semantic operations into five categories: Memory, Reasoning, Planning, Execution, and Learning instructions. This grouping has deep intellectual precedent that clarifies both its strengths and its gaps.

### The Predecessor Architectures

Modern LLM agent architectures connect to classical cognitive architectures like ACT-R and SOAR, demonstrating that the episodic-semantic-procedural memory taxonomy has deep roots in cognitive science.

ACT-R (Adaptive Control of Thought — Rational) and Soar each implement a restricted instruction set for cognition, but at the symbolic level. Your CISA advances beyond them in one critical dimension: **it treats the LLM as the execution engine for reasoning instructions**, rather than requiring symbolic rule compilation. This is the architectural discontinuity that makes your proposal genuinely new rather than a restatement of 1980s work.

### The Missing Instruction Category: Attention

Your CISA is complete in four of five dimensions. The missing category is the one your "Attention Management" section discusses but does not formalise as instructions: **attention allocation**.

LIDA is introduced through Global Workspace Theory, treating consciousness as an attention spotlight that broadcasts a small set of relevant information to specialised systems so they can coordinate. It runs in cognitive cycles: perception → attention competition → broadcast → action selection → loop, with multi-level learning noted.

Global Workspace Theory provides the formal model for your attention register. The "attention spotlight" is not merely a priority queue — it is the mechanism by which the CVM decides what enters working memory for the current cognitive cycle. The core structural claim of GWT is that human cognitive architecture consists of a number of relatively autonomous modules which process information specific to particular tasks, together with a single global workspace with which all of these modules interface.

This gives your Attention register a formal semantics. The global workspace is the Current Context register in your cognitive register file — and the competition for access to it is the attention management system. The full attention instruction set that GWT implies:

```
; Attention ISA — derived from Global Workspace Theory

ATTEND     ; direct spotlight to entity/event
COMPETE    ; evaluate multiple candidates for attention
BROADCAST  ; distribute attended content to all modules
SUPPRESS   ; reduce salience of attended item
THRESHOLD  ; set minimum salience for attention capture
```

Without this instruction category, the CVM has no formal mechanism for handling the case where multiple events simultaneously demand cognitive resources — which is precisely the multi-agent coordination failure mode the research identifies.

### The Attention Competition Problem in Practice

Empirical observation reveals that systems without proper attention management rapidly descend into a state of cognitive stagnation. Recent studies on multi-agent interactions characterise this stagnation through phenomena such as sycophancy, echo chambers, and the degeneration of thought.

This failure mode — cognitive stagnation through unmediated attention loops — is exactly what the GWT attention competition mechanism prevents. The CVM's attention register is not an optimisation feature. It is a **safety-critical component** that prevents runaway reasoning loops.

## III. The Cognitive Heap — Extended to the MemCube Standard

Your Cognitive Heap introduces semantic entities with metadata (creation time, confidence, provenance, dependencies, verification state). The research has now formalised this into a specific standard that extends your model materially.

MemoryBank and MIRIX separate events, user profiles, and world knowledge; MemOS distinguishes explicit and implicit memory; and xMemory builds a topic-event hierarchy.

The goal is not simply neat taxonomy, but more precise retrieval under complex task conditions. The architectures above still rely heavily on human-designed heuristics. Adaptive memory systems go further by making modules, routing decisions, or retrieval strategies responsive to experience.

Beyond static taxonomy, your heap requires **adaptive routing** — the allocator must decide which memory store receives a new entity based on its cognitive type, not just its data type. This is the heap allocator generalised to semantic space:

```
; Classical heap allocation
malloc(size) → address

; Cognitive heap allocation
allocate(entity) → {
    classify type: episodic | semantic | procedural | working
    assess confidence: float
    extract provenance: source chain
    set validity: datetime | perpetual
    route to store: graph | vector | in-context | parameter
    register lifecycle: scheduler callback
}
```

The lifecycle registration is the key addition. Nemori draws upon cognitive science to introduce a self-organising memory policy: the agent internalises rules for maintaining consistency and organisation (such as periodically reconciling new information with old) without external supervision, thereby gradually improving memory coherence.

Self-organising memory coherence is the cognitive equivalent of a garbage collector with defragmentation — but operating on semantic validity rather than pointer reachability.

## IV. Memory Security — The Heap Has Attack Surfaces

Your Cognitive Heap proposal does not address security. The research has now formalised why this is a critical gap.

Mnemonic sovereignty encompasses verifiable, recoverable governance over what may be written, who may read, when updates are authorised, and which states may be forgotten — arguing future secure agents will be differentiated not only by recall capacity, but by memory governance quality.

No system implements all nine necessary primitives for mnemonic sovereignty; deficiencies are particularly acute around write-gate enforcement and verified deletion.

This maps to a specific vulnerability in your heap architecture. A classical heap has one attack surface: the allocator can be exploited to write to arbitrary addresses. The Cognitive Heap has a richer attack surface: Poisoning targets have expanded from factual knowledge to procedural experience, from single entries to graph relations, and from individual agents to shared organisational memory. The defensive corollary is that write-path security cannot rely on input-level content filters alone. It requires pre-consolidation validation — a gate that treats every memory write as a privileged state transition, verifying provenance, checking consistency with existing memory, and enforcing authorisation boundaries before content is committed to long-term storage.

The pre-consolidation validation gate maps to a new heap operation that your proposal does not yet name:

```
; Classical heap: no write validation
heap[addr] = value

; Cognitive heap: provenance-gated write
COMMIT memory! [
    content: value
    provenance: source
    validate: consistency-check
    authorise: policy-check
    timestamp: now
    integrity: hmac-sign
]
```

The `COMMIT` opcode is the write-gate for the Cognitive Heap. Without it, the heap is writable by any process — including adversarial ones. A cognitive collusion attack allows colluding agents to steer victim beliefs using only truthful evidence fragments distributed through public channels without covert communication. This attack works precisely by bypassing write-gate validation — each individual memory write is locally consistent, but the aggregate produces a false belief. The `COMMIT` opcode must validate not just the individual write but its relationship to the existing belief graph.

## V. The Cognitive Register File — Formally Grounded

Your cognitive registers (Current Goal, Current Plan, Working Memory, Attention, Context, Confidence, Policy, Capability) map precisely onto a formal model from the academic literature.

Rethinking Memory Mechanisms of Foundation Agents surveys foundation agent memory organised by substrate (internal/external), cognitive mechanism (episodic, semantic, working, procedural), and subject (agent- vs user-centric).

The substrate dimension of this taxonomy is what distinguishes your register file from a mere variable set. Each register is not just a named value — it is a **substrate-typed slot** with specific access semantics:

```
┌─────────────────────────────────────────────────────────────┐
│              COGNITIVE REGISTER FILE                         │
├──────────────────┬──────────────────────┬───────────────────┤
│ Register         │ Substrate            │ Access Semantics  │
├──────────────────┼──────────────────────┼───────────────────┤
│ Current Goal     │ Intentional          │ Write-once/cycle  │
│ Current Plan     │ Procedural           │ Mutable, typed    │
│ Working Memory   │ In-context           │ Bounded, evictable│
│ Attention        │ Broadcast channel    │ Competition-gated │
│ Context          │ Session              │ Append-only       │
│ Confidence       │ Calibrated float     │ Monotone decay    │
│ Policy           │ Normative            │ Immutable/versioned│
│ Capability       │ Permission-scoped    │ Grant/revoke      │
└──────────────────┴──────────────────────┴───────────────────┘
```

The `Confidence` register deserves special attention. Your proposal treats it as a scalar value updated by the runtime. The research reveals it must be **substrate-aware**: confidence in an episodic memory decays differently from confidence in a semantic fact, which decays differently from confidence in a procedural skill. The two largest gains in Mem0's new algorithm are on temporal queries (+29.6 points over the old algorithm) and multi-hop reasoning (+23.1 points) — the two categories that most directly reflect how agents handle real user histories, in which facts accumulate, change, and relate to one another over time.

Temporal query accuracy improves 29.6 points with proper temporal confidence modelling — meaning a flat confidence scalar loses nearly 30 points of retrieval accuracy compared to a temporally-aware confidence model. The Confidence register is not a single float. It is a **confidence tensor** with dimensions for type, recency, source reliability, and contradiction history.

## VI. Reflection as Garbage Collection — Extended to a Full Memory Lifecycle

Your reflection-as-GC model correctly identifies that cognitive memory requires active curation rather than passive reclamation. The research has extended this to a full lifecycle with specific phase semantics.

Learning How to Remember proposes treating memory abstraction as a learnable cognitive skill, training a memory copilot via DPO to determine how memories should be structured, abstracted, and reused across tasks.

This means the `REFLECT` and `LEARN` opcodes in your CISA must produce not just memory updates but **structural transformations** of the memory graph itself. A memory copilot that reorganises memory topology is categorically different from a GC that frees unreachable nodes.

The full memory lifecycle that the research now maps:

```
WRITE    → Pre-consolidation validation gate
STORE    → Substrate routing (episodic/semantic/procedural)
COMPRESS → Summarisation with fidelity preservation
RETRIEVE → Multi-signal fusion (semantic + keyword + entity)
REFLECT  → Coherence reconciliation + importance scoring
PROMOTE  → Episode → Semantic elevation
FORGET   → Verified deletion with audit trail
ROLLBACK → State recovery to prior checkpoint
```

A larger context window can reduce pressure on write-time compression by permitting more raw text to be rehearsed without distillation, but it does not remove the need for any of provenance tagging, principal-scoped retrieval, rollbackable state, or verified forgetting — those arise whenever content outlives a single session or crosses a principal boundary.

The `ROLLBACK` opcode is the most technically demanding item in this set. It has no classical GC equivalent because classical GC does not require reversibility — freed memory is gone. The Cognitive Heap must support rollback because incorrect beliefs, once consolidated, corrupt all reasoning that builds on them. The rollback target is not a memory address but a **belief state checkpoint** — requiring the VM to maintain a transaction log of all COMMIT operations.

## VII. Native Uncertainty — The Four-Dimensional Extension

Your native uncertainty proposal — attaching confidence and source to every value — is correct and necessary. The research has now expanded it to four dimensions that require separate VM handling.

Beyond Dialogue Time introduces a temporal semantic memory framework that organises memories by actual occurrence time rather than dialogue time and consolidates temporally continuous information into durative memory.

This confirms that time is not just metadata on a value — it is a primary retrieval dimension. But the full uncertainty model requires four orthogonal axes:

```
; Classical value
temperature: 25

; CVM value — four-dimensional uncertainty
temperature: make uncertain! [
    value:      25
    confidence: 0.91          ; epistemic: how sure are we?
    source:     'sensor-7     ; provenance: where from?
    valid-from: 2026-07-29T14:00:00
    valid-until: 2026-07-29T14:15:00  ; temporal: still true?
    precision:  ± 0.5         ; aleatoric: measurement noise
]
```

The four dimensions — epistemic confidence, provenance, temporal validity, and aleatoric precision — each require different VM handling:

- **Epistemic confidence** is updated by the `INFER` and `LEARN` opcodes
- **Provenance** is written once by `COMMIT` and is immutable
- **Temporal validity** is evaluated at `RECALL` time against the current clock
- **Aleatoric precision** is intrinsic to the measurement and does not change with reasoning

Conflating these into a single scalar produces the failure mode that the literature identifies as the dominant source of memory errors: Claude Code v2.1.59+ implements six memory subsystems with a 4-type taxonomy. No supersession, no temporal validity, no structured facts — despite being the most widely deployed AI memory system.

The most deployed memory system in the world lacks temporal validity and provenance tracking. Your CVM's native uncertainty model addresses the precise gap that the most widely used production system currently leaves open.

## VIII. The Native Multi-Agent Runtime — Actor Model Extended to Cognitive Actors

Your multi-agent runtime — treating each agent as an independent cognitive entity with working memory, skills, shared knowledge, message passing, and policy constraints — has a formal model in the Actor calculus, but requires significant extension for cognitive correctness.

The classical Actor model guarantees: message delivery ordering, no shared mutable state, and location transparency. Your cognitive actor extension requires three additional guarantees that the Actor model does not provide:

### Guarantee 1: Belief Isolation with Selective Sharing

Actors share no state. Cognitive agents *must* share semantic memory (otherwise they cannot collaborate), but must isolate working memory (otherwise one agent's in-progress reasoning contaminates another's). This requires a **principal-scoped retrieval** model:

```
; Classical actor: no shared state
agent-a.state ≠ agent-b.state  ; always

; Cognitive actor: scoped sharing
agent-a.working-memory ≠ agent-b.working-memory  ; isolated
agent-a.semantic-memory = agent-b.semantic-memory  ; shared
agent-a.episodic-memory ≠ agent-b.episodic-memory  ; isolated
```

A cognitive collusion attack allows colluding agents to steer victim beliefs using only truthful evidence fragments distributed through public channels without covert communication. Shared semantic memory without write-gate enforcement is the attack surface. Each write to shared semantic memory must pass through the COMMIT opcode's provenance validation, even when the writer is another trusted agent.

### Guarantee 2: Attention Arbitration Across Agents

When multiple agents compete for the same capability — a database lock, an API rate limit, a human's attention — the CVM requires an attention arbitration protocol. Global Workspace Theory proposed that specialised processors compete for access to a shared workspace, with the winning signal broadcast globally. The multi-agent CVM is a distributed implementation of this competition — and the BROADCAST opcode is the mechanism by which the winning signal reaches all agents simultaneously.

### Guarantee 3: Collective False Memory Prevention

When Agents "Misremember" Collectively explores how collective false memories form in LLM-based multi-agent systems and proposes defences including cognitive anchoring and alignment-based approaches.

Collective false memory is the multi-agent version of cache incoherence: each agent's local belief is internally consistent, but the global belief state is contradictory. The CVM requires a **belief coherence protocol** — analogous to MESI in CPU cache coherence — that detects and resolves contradictions across agent belief stores before they consolidate into shared semantic memory.

## IX. The Complete CISA — Specified in Full

Drawing together your proposal, the GWT attention model, the mnemonic sovereignty requirements, and the multi-agent extensions, the complete Cognitive ISA can be specified:

```
; ══════════════════════════════════════════════════════════════
; COGNITIVE INSTRUCTION SET ARCHITECTURE (CISA) v0.1
; ══════════════════════════════════════════════════════════════

; PERCEPTION INSTRUCTIONS
OBSERVE   src                  ; capture external event into working memory
ATTEND    entity               ; direct attention spotlight to entity
COMPETE   [entity ...]         ; attention competition across candidates
BROADCAST entity               ; distribute attended content to all modules
SUPPRESS  entity               ; reduce salience of attended entity

; MEMORY INSTRUCTIONS
COMMIT    memory! [...]        ; write-gated store to cognitive heap
RECALL    query                ; multi-signal retrieval (semantic+keyword+entity)
FORGET    memory! [...]        ; verified deletion with audit trail
COMPRESS  episode! [...]       ; summarise with fidelity preservation
PROMOTE   episodic → semantic  ; elevate durable facts
ROLLBACK  checkpoint           ; restore prior belief state
INVALIDATE belief! condition   ; revoke belief when world-state changes

; REASONING INSTRUCTIONS
INFER     [evidence ...]       ; derive new belief from evidence chain
COMPARE   [alternative ...]    ; evaluate options against criteria
CLASSIFY  entity               ; assign category with confidence
EXPLAIN   belief!              ; trace provenance chain of belief
ESTIMATE  [cost | risk | time] ; probabilistic projection
THRESHOLD confidence           ; gate action on minimum confidence

; PLANNING INSTRUCTIONS
PLAN      goal! → plan!        ; expand declarative goal to task DAG
SCHEDULE  plan! [priority ...]  ; assign execution order and resources
DELEGATE  task! → agent!       ; assign subtask to specialist agent
CANCEL    plan!                ; abort plan with rollback
REPLAN    goal! [changed ...]   ; revise plan given new constraints

; EXECUTION INSTRUCTIONS
EXECUTE   capability! [...]    ; policy-gated action execution
VERIFY    outcome!             ; compare actual vs. expected state
ROLLBACK  execution!           ; undo reversible action
COMMIT    result!              ; seal execution receipt with HMAC
SANDBOX   capability! [...]    ; execute in isolated context

; LEARNING INSTRUCTIONS
REFLECT   [expected actual]    ; compute divergence, derive lesson
LEARN     lesson! → skill!     ; compile experience to reusable skill
UPDATE    belief! [new-evidence] ; revise belief confidence
CONSOLIDATE [episode ...]      ; merge related episodes

; AGENT INSTRUCTIONS
SPAWN     agent! [spec]        ; instantiate new cognitive actor
MESSAGE   agent! payload       ; send typed message to agent
SYNCHRONISE [agent ...]        ; coordinate shared memory coherence
MERGE     [belief ...]         ; arbitrate conflicting beliefs across agents
TERMINATE agent!               ; clean shutdown with memory persistence
```

The key additions to your original CISA are:

1. **Perception layer** — ATTEND, COMPETE, BROADCAST, SUPPRESS, grounded in GWT
2. **Memory security** — COMMIT with write-gate, ROLLBACK, INVALIDATE
3. **Agent coordination** — SYNCHRONISE, MERGE, for belief coherence
4. **Execution safety** — SANDBOX, COMMIT with HMAC for audit trail

## X. The Toolchain — Extended to Include the CVM Position

Your complete toolchain diagram:

```
Red Source → Cognitive Parser → Intent Graph Builder →
Planning Optimiser → Capability Verifier → CIR → CVM → OS Effects
```

is correct and now positions correctly against the research landscape. One addition is required: the CVM must sit above a **Memory Substrate Layer** that is distinct from the OS Effects layer.

```
┌──────────────────────────────────────────────────────────────────┐
│                         Red Source                               │
├──────────────────────────────────────────────────────────────────┤
│   Cognitive Parser + Intent Graph Builder                        │
│   (Declarative goal extraction, BDI type classification)         │
├──────────────────────────────────────────────────────────────────┤
│   Planning Optimiser                                             │
│   (DAG expansion, parallelisation, profile-guided speculation)   │
├──────────────────────────────────────────────────────────────────┤
│   Capability Verifier                                            │
│   (Policy-as-type checking, proof obligation discharge)          │
├──────────────────────────────────────────────────────────────────┤
│   Cognitive IR (CIR)                                             │
│   (Intent Graph → Task DAG → Capability Graph → Exec Graph)      │
├──────────────────────────────────────────────────────────────────┤
│   Cognitive Virtual Machine (CVM)                                │
│   (CISA execution, Cognitive Register File, Attention Manager)   │
├────────────────────────┬─────────────────────────────────────────┤
│   Memory Substrate     │   Execution Substrate                   │
│   Episodic Store       │   OS Process / Capability Sandbox       │
│   Semantic Store       │   Network / Filesystem / APIs           │
│   Procedural Store     │   Model Inference Engines               │
│   Working Memory       │   Tool Registries                       │
└────────────────────────┴─────────────────────────────────────────┘
```

The Memory Substrate and Execution Substrate are parallel, not sequential. A single CVM instruction like `EXECUTE capability! [read-file %data.csv]` dispatches simultaneously to the Execution Substrate (OS file I/O) and the Memory Substrate (logs the action as an episodic event, updates the capability usage register, triggers the COMMIT write-gate for the resulting observation).

## XI. The Deepest Claim — Intelligence as a Computational Substrate

Your conclusion — that Red would "compile intent into verified cognitive execution" — is the precise statement of what separates a CVM from a conventional runtime. The research now frames this in terms of what the scheduler actually manages at each architectural level.

A cognitive architecture is a framework that specifies the fixed structures and mechanisms underlying intelligent behaviour — including how perception, attention, memory, reasoning, learning, and action are organised and interact. It describes the mind's "operating system," not its content.

This distinction — architecture vs. content — is the CVM's central design principle. The CVM is the fixed structure. The goals, beliefs, plans, and memories are the content. The CVM makes no assumptions about what the agent wants to do; it provides the computational substrate for doing it with verifiability, provenance, and safety guarantees.

Large language models like GPT-4 and Claude are powerful but are not full cognitive architectures — they lack persistent goals, embodied perception, and continuous operation across time.

This is the gap that the CVM fills. An LLM is a reasoning engine — powerful, flexible, but stateless. A CVM is a cognitive substrate — persistent, structured, and governed. Together, the LLM provides the `INFER`, `CLASSIFY`, and `EXPLAIN` instruction implementations; the CVM provides the `COMMIT`, `ROLLBACK`, `VERIFY`, and `SANDBOX` operations that make the LLM's outputs safe to act on.

The full progression from Red to CVM can now be stated precisely:

| Layer            | Primary Abstraction          | Safety Guarantee                     |
|------------------|------------------------------|--------------------------------------|
| Red/System       | Machine resource             | Type-safe memory operations          |
| Red              | Computation                  | Type-safe code composition           |
| Red/Cognition    | Intent and reasoning         | Policy-checked capabilities          |
| CIR              | Verified cognitive plan      | Acyclicity, completeness, budget     |
| **CVM**          | **Semantic execution**       | **Provenance, rollback, coherence**  |

Each layer adds one safety dimension that the layer below cannot provide. The CVM is not the top of this stack — it is the runtime that makes all the layers above it trustworthy. Intelligence, as you have framed it across this entire architecture, is not a feature added to computation. It is a new substrate, with its own instruction set, its own memory model, its own safety properties — and its own compiler.

That is the complete argument. The CVM is the point at which Red's original "full-stack" vision — hardware to human — extends through one more abstraction boundary into cognition itself.

---

**Traceability:** All content extracted verbatim from the analysis section of the seventh user message. No information added or inferred.