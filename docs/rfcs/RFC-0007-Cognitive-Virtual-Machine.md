# RFC-0007 — Cognitive Virtual Machine (CVM)

**RFC:** RFC-0007
**Title:** Cognitive Virtual Machine — Semantic Execution Substrate: CISA, Registers, Semantic Memory, Heap, Attention, Provenance, and Multi-Agent
**Stable ID(s):** `CVM-001`, `CVM-ANALYSIS-001`
**Origin:** MSG-07 (Beyond Red/Cognition: A Cognitive Virtual Machine) — proposes semantic opcodes `OBSERVE RECALL INFER PLAN SELECT EXECUTE VERIFY REFLECT LEARN`, cognitive ISA, registers, semantic addressing, heap, attention, provenance, reflection-as-GC, multi-agent, object model, toolchain `Source→CIR→CVM→OS Effects`.
**Evolution:** Grounded in Analysis §§I–IV via Wray et al. Soar→ReAct missing commitment (=PLAN/SELECT), MemOS MemCube, ACT-R/Soar, GWT attention spotlight + safety, mnemonic sovereignty 9 primitives + heap attack surfaces, belief coherence (MESI-like) and collective false memory; extends to complete **CISA v0.1 (30 ops)** across perception/memory/reasoning/planning/execution/learning/agent + dual memory+execution substrates (§X) and architectural safety table (§XI: Red/System→Red→Red/Cognition→CIR→CVM each adding a safety dimension).
**Final Representation:** This RFC + CVM (CISA execution + Cognitive Register File + Cognitive Heap + Attention Manager + Provenance Subsystem) above dual substrates.
**Status:** `Draft` (MemOS prototype exists at framework level; no Red/Cognition VM implementation yet)
**Authors:** Conversation MSG-07 + Analyzer MSG-07 + Auditor
**Verification:** CISA opcode conformance per category; register file state-vector test; heap allocator route `classify→confidence→provenance→validity→route→register`; GWT attention competition liveness; EXPLAIN provenance chain; MESI-like coherence stress.

---

## 1. Abstract

Redesigns the runtime from an instruction executor into a **reasoning engine**: the VM executes semantic opcodes over semantic memory with verified provenance and safety guarantees, sitting above the CIR and below the OS.

## 2. Motivation

LLMs like GPT-4/Claude are powerful reasoning engines but lack persistent goals, embodied perception, continuous operation, and verifiable provenance. The CVM supplies the fixed architecture (substrate) vs LLMs' content (reasoning) — the “operating system” for cognition, not the content.

## 3. Specification

### 3.1 Cognitive Instruction Set Architecture — CISA v0.1 (normative, complete per Analysis §IX)

```
; PERCEPTION (& Attention — GWT formal, safety-critical)
OBSERVE   src                  ; capture external event into working memory
ATTEND    entity               ; direct spotlight
COMPETE   [entity ...]         ; attention competition across candidates
BROADCAST entity               ; distribute attended content to all modules
SUPPRESS  entity               ; reduce salience
THRESHOLD confidence           ; gate action on minimum

; MEMORY — with write-gate & verified deletion (mnemonic sovereignty)
COMMIT    memory! [...]        ; write-gated store to cognitive heap
RECALL    query                ; multi-signal retrieval (semantic+keyword+entity)
FORGET    memory! [...]        ; verified deletion with audit trail
COMPRESS  episode! [...]       ; summarise with fidelity preservation
PROMOTE   episodic → semantic  ; elevate durable facts
ROLLBACK  checkpoint           ; restore prior belief state
INVALIDATE belief! condition   ; revoke when world-state changes

; REASONING
INFER     [evidence ...]       ; derive new belief from evidence chain
COMPARE   [alternative ...]    ; evaluate options against criteria
CLASSIFY  entity               ; assign category with confidence
EXPLAIN   belief!              ; trace provenance chain
ESTIMATE  [cost | risk | time] ; probabilistic projection
THRESHOLD confidence           ; (also perception-gating)

; PLANNING
PLAN      goal! → plan!        ; expand declarative goal to task DAG
SCHEDULE  plan! [priority ...] ; assign execution order/resources
DELEGATE  task! → agent!       ; assign subtask to specialist
CANCEL    plan!                ; abort with rollback
REPLAN    goal! [changed ...]  ; revise given new constraints

; EXECUTION
EXECUTE   capability! [...]    ; policy-gated action
VERIFY    outcome!             ; compare actual vs expected
ROLLBACK  execution!           ; undo reversible action
COMMIT    result!              ; seal receipt with HMAC (audit)
SANDBOX   capability! [...]    ; isolated context

; LEARNING
REFLECT   [expected actual]    ; compute divergence, derive lesson
LEARN     lesson! → skill!     ; compile experience to reusable skill
UPDATE    belief! [new-evidence] ; revise belief confidence
CONSOLIDATE [episode ...]      ; merge related episodes

; AGENT
SPAWN     agent! [spec]        ; instantiate cognitive actor
MESSAGE   agent! payload       ; typed message
SYNCHRONISE [agent ...]        ; shared memory coherence (MESI-like)
MERGE     [belief ...]         ; arbitrate conflicting beliefs across agents
TERMINATE agent!               ; clean shutdown with persistence
```

### 3.2 Cognitive Register File (normative)

CPU `RAX RBX...` → logical registers `Current Goal, Current Plan, Working Memory, Attention, Context, Confidence, Policy, Capability` continuously updated:

```
Goal Register       ── "Analyse repository"
Confidence Register ── 0.82
Attention Register  ── Architecture module
```

Attention register competes for Global Workspace (GWT) broadcast.

### 3.3 Memory Architecture (normative)

- **Addressing:** `0x1000` positional → `Project/OpenClaw` semantic, associative retrieval.
- **Heap entities:** `Goal Object, Observation Object, Plan Object, Memory Object, Evidence Object, Skill Object` with `creation time / confidence / provenance / dependencies / verification state`.
- **Allocator (normative, Analysis §III):**

```
malloc(size) → address
allocate(entity) → { classify type: episodic|semantic|procedural|working
                     assess confidence: float
                     extract provenance: source chain
                     set validity: datetime|perpetual
                     route to store: graph|vector|in-context|parameter
                     register lifecycle: scheduler callback }
```

`MemCube` (MemOS) is this heap made concrete: plaintext/activation/parameter memory encapsulated with scheduler+lifecycle; adaptive routing + self-organising coherence required.

### 3.4 Attention Management (normative, GWT safety-critical)

```
Incoming Events → Importance/Urgency/Novelty/Risk → Attention Score → Spotlight → Competition → Broadcast
```

Without competition, reasoning stagnates into sycophancy/echo chambers/degeneration — the 5 perception ops are safety, not optimisation.

### 3.5 Provenance & Reflection-as-GC (normative)

- **Evidence chain:** `Memory → Observation → Evidence → Source → Timestamp`; `Sensor→Observation→Reasoning→Decision→Action` lineage per reasoning step; `EXPLAIN belief!` traverses chain.
- **Reflection as GC:** `Working Memory → Still Relevant? → Keep / Compress→Summarise→Archive→Forget` — curates knowledge, not just frees it.

### 3.6 Multi-Agent (normative)

```
Planner Agent | Reviewer Agent | Executor Agent | Verifier Agent | Memory Agent
```

Each with independent WM, specialised skills, shared semantic knowledge, message passing, policy constraints — actor systems with richer cognitive state.

### 3.7 Cognitive Object Model & Toolchain (normative)

```red
agent! [beliefs goals memories skills policies capabilities reflection]
```

Toolchain `Red Source → Cognitive Parser → Intent Graph Builder → Planning Optimiser → Capability Verifier → CIR → CVM → OS Effects` where the CVM sits **above dual substrates** (not single sequential — Analysis §X correction):

```
CVM (CISA + Registers + Attention)
  ├─ Memory Substrate (Episodic | Semantic | Procedural | Working Memory)
  └─ Execution Substrate (OS Process/Sandbox | Network/FS/APIs | Model Engines | Tool Registries)
```

Single CVM instruction `EXECUTE capability! [read-file %data.csv]` dispatches **simultaneously** to both substrates (I/O + episodic log + capability usage + COMMIT write-gate).

## 4. Consequences

- **LLM role repositioned:** LLMs implement `INFER/CLASSIFY/EXPLAIN`; CVM implements `COMMIT/ROLLBACK/VERIFY/SANDBOX` — together, reasoning + safety.
- **Trust per memory:** write-gate enforcement + verified deletion closes 9-primitive sovereignty gaps (OP-09).
- **Collective coherence:** `SYNCHRONISE/MERGE` prevents false memory (OP-08) via MESI-like belief coherence — locally consistent but globally contradictory states are detected before semantic consolidation.
- **Trade-off:** 30-op ISA is larger surface than 6-op toy; conformance suite required per category.

## 5. Traceability

- **RFC Origin Map rows:** R31–R35 (CISA v0.1, registers, semantic memory/heap, attention, provenance/GC).
- **REQ IDs:** REQ-016 (30 ops, dual substrates), REQ-017 (heap routing + MemCube + write-gate), REQ-018 (GWT attention), REQ-019 (evidence chain), REQ-020 (semantic GC), REQ-021 (MESI coherence — Open Question).
- **ADRs:** ADR-007 (dual substrates), ADR-008 (GWT as safety-critical), ADR-011 (write-gate sovereignty).
- **Formal models:** Soar/ACT-R/LIDA/GWT; MemOS/MemCube; mnemonic sovereignty (9 primitives); MESI coherence.
- **Open problems:** OP-08 (collective false memory), OP-09 (mnemonic sovereignty write-gate/deletion), OP-12 (attention liveness), OP-06 (goal coherence co-closed).

## 6. Dependencies

- **Upstream:** RFC-0006 (CIR is the artifact this VM executes), RFC-0004 (CogOS kernel requirements formalised here).
- **Downstream:** RFC-0008 (Red 2.0 unifies CVM into hardware→intelligence narrative).

## 7. Appendix — Wiki Source Mapping

- `Cognitive-Virtual-Machine-CVM.md` (367 lines) — core proposal: ISA categories, registers, memory, heap, toolchain.
- `Cognitive-Virtual-Machine-Analysis.md` (376 `wc -l`, 32k rendered) — §§I–XI MemOS/GWT/sovereignty/coherence, complete CISA v0.1, dual substrates, safety table (each layer adding one guarantee).

