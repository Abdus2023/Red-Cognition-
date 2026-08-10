# RFC-0005 — Red/Cognition Language

**RFC:** RFC-0005
**Title:** Refactoring Red into a Cognitive Language — Types, Reasoning Blocks, Memory Primitives, Capabilities, and Inter-Layer Contracts
**Stable ID(s):** `RED-COG-001`, `RED-COG-ANALYSIS-001`
**Origin:** MSG-05 (Refactoring Red into a Cognitive Language) — proposed `goal! plan! belief! memory! skill! observation! hypothesis! policy! evidence! event! capability!` (11 types) and three-layer stack `Human Goals→Red/Cognition→Red→Red/System→Hardware`; with Analysis grounding in BDI/AgentSpeak, LoT, AgentSpec, GOAL declarative semantics.
**Evolution:** 11→16 types (Analysis §VIII adds `intention!`, `episode!`, `permission!`, `hypothesis!` split + epistemic/intentional/temporal/normative taxonomy); LoT hypothesis elevates `reason [...]` from convenience to cognitive alignment; AgentSpec contrast shows dialect-embedded vs external policy; GOAL distinction splits `goal!` (achievement) vs `plan!` (procedural); inter-layer contracts diagram added (§IX); failure semantics `on-failure` added (§VII); synthesis table vs BDI/Python frameworks (§XI).
**Final Representation:** This RFC + Red/Cognition Type System (16 types with cognitive metadata), Three-Layer Stack with Cognitive Pipe + Capability Binding contracts, and Repository Assistant conformance test.
**Status:** `Draft` (language extension; no compiler implementation yet)
**Authors:** Conversation MSG-05 + Analyzer MSG-05 + Auditor
**Verification:** `make belief! [content confidence source]` typecheck; `red/cognition` parse of golden file `agent "Repository Assistant"` (single block, inspectable); inter-layer metadata shedding/acquisition compile test.

---

## 1. Abstract

Extends Red upward (mirroring Red/System downward) into a cognitive layer whose primary abstractions are intent, memory, reasoning, and autonomous behaviour — expressed as typed, inspectable blocks that are simultaneously human-readable, machine-executable, and runtime-inspectable.

## 2. Motivation

Red today describes **computations**; agents require declarations of **intent, reasoning, memory, and action** that survive across sessions and are verifiable before execution. Prior BDI languages had the vocabulary but lacked the runtime (weak reasoners, no ecosystem, separated syntax); Python frameworks have the ecosystem but lack composable typed verification. This RFC closes both gaps.

## 3. Specification

### 3.1 Three-Layer Stack (normative)

| Layer | Purpose | Primary Abstraction |
|---|---|---|
| **Red/System** | Hardware / systems programming | Machine resources |
| **Red** | General programming & DSLs | Computation (integer!/string!/block!/object!/function!/dialect!) |
| **Red/Cognition** | Autonomous agents & AI | Intent, memory, reasoning, goals (`goal!`…`capability!`) |

Informative diagram:

```
Human Goals → Red/Cognition (Goals•Plans•Memory•Skills) → Red (Functions•Objects•Blocks•Dialects) → Red/System (Memory•Pointers•Native)→ Hardware
```

### 3.2 New Primitive Data Types (normative, 16)

**Epistemic — carry truth & confidence:**

`belief!` (holds-to-be-true + confidence), `hypothesis!` (below threshold), `evidence!` (updates confidence), `observation!` (raw input, not yet interpreted)

**Intentional — carry goal structure:**

`goal!` (desired end state, declarative), `plan!` (steps toward goal, procedural), `intention!` (committed plan), `capability!` (permitted action)

**Temporal — carry validity windows:**

`memory!` (past experience + timestamp/validity), `skill!` (compiled procedural + performance history), `episode!` (bounded narrative unit)

**Normative — carry policy & constraint:**

`policy!` (rule governing behaviour), `permission!` (granted capability + scope/expiry), `event!` (trigger binding world-state change to response)

Distinguishing property (normative): **each type carries cognitive metadata** — `confidence`, `validity`, `source`, `scope` — interrogatable by runtime before dependent actions. A plan built on `belief! 0.23` behaves differently from `0.97` by type system, not manual check.

### 3.3 Goals Instead of Functions (normative)

Imperative:

```red
analyse: func [file][ parse file  summarize ]
```

Declarative (runtime decides *how*):

```red
goal analyse-log [
    observe %server.log
    extract errors
    summarize
    verify
]
```

Achievement vs procedural goals (normative per Analysis §IV, GOAL language):

```red
achieve [repository: analysed  report: generated]   ; declarative: desired state, verifiable via modal logic
plan analyse-log [observe %server.log  extract errors  summarize  verify] ; procedural: steps, completable
```

### 3.4 Native Reasoning Blocks (normative)

```red
reason [
    if confidence < 80% [gather-more-evidence]
    compare alternatives
    estimate cost
    choose best-plan
]
```

Block becomes a **structured reasoning graph**, not control flow; grounded via Language-of-Thought hypothesis (Analysis §II: mind's operations are code-like).

### 3.5 Memory as Primitive (normative)

```red
remember [user prefers offline execution]
recall   [projects about OpenClaw]
forget   [noise, no long-term value]  ; via policy, not raw memory free
```

Runtime determines storage/retrieval (vector vs graph per RFC-0003/0004 hybrid router).

### 3.6 First-Class Skills & Capability-Based Execution (normative)

```red
skill summarize
execute [delete %temp/]  ; runtime checks permissions/policy/risk/sandbox/audit trail before action
```

Skill vs function: skill carries `performance-history` and is capability-gated; internally may invoke local code / external tools / AI models. Policy types per RFC-0006: `delete-directory: capability! [policy: dangerous]`.

### 3.7 Multi-Model Reasoning (normative)

```red
reason using small-model [classify message]
reason using planner     [build execution graph]
reason using verifier    [check consistency]
```

Uniform language interface; runtime selects most appropriate model (validated by RFC-0004 model tier).

### 3.8 Event-Driven Cognition (normative)

```red
when filesystem changes [observe  reason  update memory  notify]
when github.push [ ... ]  ; see complete example §3.9
```

### 3.9 Complete Example — Golden File (normative)

```red
agent "Repository Assistant" [
    identity [name: "Repository Assistant" version: 1.0 permissions: [read-filesystem call-github generate-report]]
    believe [
        project: make belief! [content: "OpenClaw" confidence: 1.0 source: 'user]
        language: make belief! [content: 'Rust confidence: 0.95 source: 'observation]
    ]
    when github.push [
        observe make observation! [source: 'github event: 'push payload: github.event-data]
        reason using planner [identify changed modules  estimate impact  choose review-strategy]
        plan [run tests  inspect architecture  summarize changes]
        act  [generate report]  ; requires generate-report capability
        reflect [
            compare prediction with results
            if divergence > 0.2 [update beliefs  record episode]
            remember lessons  ; promotes to semantic per promotion gate
        ]
    ]
]
```

This is the conformance test: the block must be simultaneously human-readable, machine-executable, and runtime-inspectable (single traversal, no separated belief/goal/plan files as in Jason).

### 3.10 Inter-Layer Contracts (normative, Analysis §IX diagram)

```
Red/Cognition (goal!..capability! + observe()/remember()/... + BDI + confidence-weighted)
  ── Cognitive Pipe Protocol ──
  Downward: goal! → plan! → function call + policy check
  Upward:   result + confidence + provenance + reflection
Red Language (integer!..dialect!, blocks carry cognitive types transparently, dialects implement reason/plan/observe/remember)
  ── Capability Binding ──
  Downward: Red function → Red/System native call + sandbox
  Upward:   result + exit status + resource consumption
Red/System (Memory·Pointers·Native·OS)
```

Every value crossing downward sheds cognitive metadata to typed Red value; every result crossing upward acquires confidence/provenance/validity before cognitive layer acts.

### 3.11 Failure Semantics (normative, Analysis §VII)

```red
goal analyse-log [observe %server.log extract errors summarize verify]
on-failure [
    retry with-model large-remote
    escalate to human
    record-failure in memory
    abandon with-reason "verification-failed"
]
```

Silent incorrect-state propagation into memory is categorically worse than classical exception (contaminates subsequent reasoning) — hence explicit `on-failure`.

## 4. Consequences

- **Unified block** replaces BDI's separated syntaxes — inspectable/verifiable diffable.
- **Composability as safety:** type-enforced confidence/validity makes cognitive programs inspectable/verifiable for autonomous execution (synthesis table §XI: Red/Cognition matches BDI's formal types + Python's ecosystem reach, adding homoiconic composability).
- **Blocked**: without FFI bridging (OP-01) ecosystem reach remains `⚠️ Unsolved` per synthesis table.

## 5. Traceability

- **RFC Origin Map rows:** R20–R22 (16-type system, contracts, golden file).
- **REQ IDs:** REQ-011 (16 types), REQ-012 (contracts), REQ-022 golden-file conformance implied.
- **ADR:** ADR-004 (declarative vs procedural).
- **Formal models:** BDI/2APL/AgentSpeak/GOAL (§I, IV), LoT (§II), AgentSpec (§III), production declarative agents (§V).
- **Open problems:** OP-01 (ecosystem bridging, synthesis table), unlocks OP-02/03 (policy proof / effect inference handled in RFC-0006).

## 6. Dependencies

- **Upstream:** RFC-0003/0004 (ARS/CogOS provide the `observe/remember/plan` execution substrates that types reify).
- **Downstream:** RFC-0006 (compiler verifies types via 4 new passes), RFC-0007 (CVM registers/heap hold typed entities).

## 7. Appendix — Wiki Source Mapping

- `Red-Cognition-Language.md` (257 lines) — §§ core proposal through three-layer vision.
- `Red-Cognition-Analysis.md` (361 lines + 25k rendered with tables) — §§ I–XI BDI/LoT/AgentSpec/GOAL + type system + contracts + annotated golden file + synthesis table.

