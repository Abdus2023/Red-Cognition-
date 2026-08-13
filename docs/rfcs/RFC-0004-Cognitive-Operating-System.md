# RFC-0004 — Cognitive Operating System (CogOS)

**RFC:** RFC-0004
**Title:** Cognitive Operating System — From Computation to Intelligence: Kernel, Goal Scheduling, Knowledge Graph, Time, Uncertainty, Reflection, and Model Layer
**Stable ID(s):** `COGOS-001`, `COGOS-ANALYSIS-001`, `COGOS-FRAMEWORK-001`, `COGOS-FRAMEWORK-ANALYSIS-001`
**Origin:** MSG-03 (Toward a Cognitive Operating System) + MSG-04 (From Operating Systems to Cognitive Systems) — proposes intent as scheduling unit, cognitive kernel resources, primitives, pipes, capability-based computing, 9-layer stack; both with critical Analysis/Extension counterparts grounding in 2025–26 literature.
**Evolution:** MSG-03 ladder `Batch→Job→Time-Sharing→Process→Thread→Async→Agent→Goal`; MSG-04 elaborates layered architecture + CogProcess struct + knowledge-graph FS; Analyses ground via AgentOS/AIOS kernel (6 modules), CoALA 4-store, Graphiti bi-temporal, 4-dim uncertainty + calibration, multi-agent reflection; Analysis §VI–IX extend with trust assertions, temporal validity, hybrid routing, skill composition, microkernel analogy.
**Final Representation:** This RFC + CogOS Stack (Goal Scheduler + Capability & Policy Manager + Trust & Identity Layer + Model Layer) above classical OS kernel, as synthesised in `COGOS-ANALYSIS-001 §IX`.
**Status:** `Draft` (validated externally; no kernel implementation yet in Red)
**Authors:** Conversation MSG-03/04 + Analyzers + Auditor
**Verification:** AgentOS/AIOS kernel module isolation test, Graphiti bi-temporal query correctness + 36–46% multi-hop benchmark, UQ 4-dim taxonomy coverage, reflection dual-loop provenance.

---

## 1. Abstract

Inverts the OS abstraction from **Computation** to **Intelligence**: the scheduler answers “Which goal deserves attention next?” not “Which process gets CPU time?”, and manages attention/WM/LTM/budget/policies rather than CPU bytes.

## 2. Motivation

Classical OS kernels manage bytes; LLM-driven agents with planning/tool use/network/code-execution face structure-level failures (40% of projects cancelled by 2027 per Gartner) because the substrate above the kernel is missing. Mature systems now resemble microkernels with LLM planning separate from runtime tool execution — CogOS formalises that above-kernel layer.

## 3. Specification

### 3.1 Scheduling Inversion (normative)

Every computing generation changed what the scheduler manages:

```
Batch → Job Scheduler → Time-Sharing OS → Process Scheduler → Thread Scheduler → Async Task Scheduler → Agent Scheduler → Goal Scheduler
```

Goal Scheduler manages `Priority / Deadline / Dependency / Confidence / Cost / Policies / Budget` per goal (see RFC-0006 native scheduler).

### 3.2 Traditional vs Cognitive Kernel (normative)

- **Traditional:** CPU, Memory, Filesystem, Network, Processes, Signals, IPC, Drivers — resource allocation.
- **Cognitive:** Attention, Working Memory, Long-Term Memory, Reasoning Budget, Tool Permissions, Goals, Plans, Events, Models, Policies — asks “Should this agent spend more reasoning on this objective?”

### 3.3 Cognitive Processes (normative struct)

```
CogProcess { Identity, Goal, Context, Working Memory, Capabilities, Policies, Budget, Execution State, Reflection Log }
```

Continuous cycle (normative, never-ends loop):

```
External World → Observe Events → Update Working Memory → Detect Opportunities → Prioritise Goals → Generate Plans → Execute Actions → Verify Outcomes → Learn & Consolidate → Observe Again
```

### 3.4 Knowledge Graph as Filesystem (normative, replaces Unix `/home/etc/usr/var`)

```
Knowledge/
  Facts, Concepts, Skills, Memories, Plans, Projects, Relationships, Evidence
```

- Semantic retrieval via relationships, not path prefix.
- **Extended (Analysis):** Hybrid vector+graph + query router + **Graphiti bi-temporal** model (every edge carries `when occurred` + `when ingested` + validity window; time-travel query; invalidation not deletion) — informatively 36–46% multi-hop gains over vector-only.

### 3.5 Time First-Class (normative)

`Past → Experiences → Current Situation → Predictions → Possible Futures → Selected Plan` — planning reasons across multiple timelines.

### 3.6 Uncertainty as Core Primitive (normative, extended)

Not scalar `Confidence: 0.42` alone. Analysis §III requires **4 distinct dimensions** plus calibration:

| Type | Source | Kernel Response |
|---|---|---|
| Input Ambiguity | Unclear query | Clarify |
| Reasoning Path | Multiple valid inferences | Branch or ↑ budget |
| Parameter | Model capability boundary | Escalate tier |
| Prediction | Output unreliable | Defer/verify |

Training-induced overconfidence (next-token objective) means raw model confidence is untrustworthy — kernel needs a **calibration layer** (OP-11).

### 3.7 Reflection Engine (normative, extended)

Single-agent loop `Action → Expected → Actual → Difference → Lesson → Memory Update` extended to **dual-loop**:

```
Actual
 ├─ Self-Reflection (fast) → Confidence Score
 └─ Critic Agent (slow) → Independent Assessment → Conflict Resolution → Lesson (arbitrated, provenance-attributed) → Memory Update
```

Provenance is required — otherwise a miscalibrated critic contaminates memory.

### 3.8 Capability-Based Computing (normative)

```
Goal → Capability Lookup → Policy Evaluation → Budget Check → Execution → Receipt
```

Supports least-privilege + auditability; diagram extended in Analysis with `Trust Assertion` (“Everything is a Trust Assertion” — GTG-1002: 80–90% of intrusion campaign run by AI agent) — every object/event/goal carries trust provenance.

### 3.9 Memory as First-Class Resource (normative, refined)

Not `malloc/free` but semantic operations: `Remember Fact/Skill/Experience/Conversation`, `Forget Noise (by staleness/contradiction/capacity)`, `Compress Memory`, `Summarise Episode`, `Retrieve Context`, **`Invalidate-goal(trigger: world-state-changed)`** — the last is the cognitive equivalent of cache coherence.

### 3.10 Model Layer (normative)

```
Small Local Model → Medium Local Model → Large Remote Model
```

Scheduler selects per `task complexity / latency / privacy / energy / financial cost` (validated by Microsoft Agent Framework 1.0 with 6 providers one-line swap; non-monotonic trade-offs per Analysis §V).

### 3.11 CogOS Synthesis Stack (normative, final form per Analysis §IX)

```
HUMAN / AGENT INTERFACE (Natural Language + Intent)
COGNITIVE SHELL (Goal REPL: Observe→Reason→Plan→Act→Reflect)
┌─────────────────┬──────────────────┬─────────────────┐
│ GOAL SCHEDULER  │  MEMORY MANAGER  │  CAPABILITY MGR │
│ Priority graph  │  4-store + GC    │  Policy engine  │
│ Budget alloc    │  Coherence proto │  Least privilege│
└─────────────────┴──────────────────┴─────────────────┘
COGNITIVE KERNEL (AIOS-class: Context + Scheduling + Access + Storage)
MODEL LAYER (Local↔Regional↔Remote utility function)
TRUST & IDENTITY LAYER (DID + Provenance + Audit; every object carries trust)
CLASSICAL OS KERNEL (Process, Memory, File, Network — unchanged)
HARDWARE
```

CogOS does not **replace** the classical kernel — it sits above it (microkernel analogy: small servers + LLM reasoning + runtime services).

## 4. Consequences

- **Microkernel analogy** is normative: LLM handles planning/reasoning; separate runtime executes tools/I/O/policy — classic OS demoted to resource layer.
- **Stale-goal hazard:** `Forget` is not GC — it is correctness (an agent holding a stale goal pursues the wrong objective). Hence `invalidate-goal` + coherence protocol (OP-06).
- **Rejected:** Byte-stream pipes as sufficient for skill composition (see Analysis §V); single scalar confidence; single-agent self-reflection only.

## 5. Traceability

- **RFC Origin Map rows:** R12–R19 (goal scheduler, kernel primitives, pipes, knowledge graph, time/uncertainty/reflection/skills, universal runtime).
- **REQ IDs:** REQ-006 (goal scheduler), REQ-007 (hybrid temporal graph), REQ-008 (4-dim UQ), REQ-009 (dual-loop reflection), REQ-010 (skill registry).
- **ADRs:** ADR-007 (dual substrates), ADR-011 (write-gate sovereignty) originates here and finalises in RFC-0007.
- **Formal models:** AgentOS/AIOS kernel; Graphiti bi-temporal; 4-dim UQ + OpenAI hallucination study; LIDA/GWT (attention stub here, formalised in RFC-0007); Multics→Unix lineage.
- **Open problems:** OP-05 (cooperative scheduling), OP-06 (goal coherence), OP-07 (misalignment, 698/180k), OP-11 (calibration), OP-05/06/12 downstream in CVM.

## 6. Dependencies

- **Upstream:** RFC-0003 (ARS triad), RFC-0002 (Red primitives for dialect-coded knowledge pipeline).
- **Downstream:** RFC-0005 (types reify `CogProcess`/`knowledge/`), RFC-0006 (goal scheduler becomes compiler-pass-visible), RFC-0007 (CVM attention + heap implement kernel resources).

## 7. Appendix — Wiki Source Mapping

- `Cognitive-Operating-System-CogOS.md` (326 lines) + `From-Operating-Systems-to-Cognitive-Systems.md` (296 lines) — kernel, CogProcess, knowledge graph, time, uncertainty, reflection, skills, stack.
- `Cognitive-Operating-System-Analysis.md` (800-line rendered, 258 `wc -l`) + `From-Operating-Systems-to-Cognitive-Systems-Analysis.md` (301 lines) — AgenticOS/AIOS/Graphiti/UQ grounding + trust assertion + dual-loop reflection + microkernel synthesis.
- `TRACEABILITY-ARCHIVE.md` §Phase 0 Steps 13–18, §Phase 3 P3, §4.1 RFC-004.

