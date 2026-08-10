# RFC-0003 — Agent Operating Environment

**RFC:** RFC-0003
**Title:** Agent Operating Environment — Agent Runtime Shell, Cognitive Pipeline, Memory Hierarchy, Event Queue, Tool Invocation, and Evolutionary Ladder
**Stable ID(s):** `AGENT-ENV-001`, `AGENT-ENV-ANALYSIS-001`, `AGENT-ANALYSIS-001`
**Origin:** MSG-02 (The Missing Layer: Agent Operating Environment) — REPL “designed for a human at a keyboard; an autonomous agent requires a persistent operating environment managing cognition, memory, tools, safety, execution” + `AGENT-ENV-ANALYSIS-001` grounding and extension.
**Evolution:** ARS triad `Cognitive Engine | Memory System | Tool System` → Cognitive Kernel resources in MSG-03/04; 11-stage pipeline extended with three missing stages; vertical memory stack **corrected** to CoALA 4 parallel stores (`AGENT-ENV-ANALYSIS-001 §II`) via Tulving/Baddeley/Squire + CoALA Princeton 2023; tool pipeline validated against Microsoft Agent Governance Toolkit + OWASP Top 10; evolutionary ladder refined with discrete phase changes (Analysis §VI).
**Final Representation:** This RFC + Agent Runtime Shell (ARS) + Cognitive Pipeline Engine + Memory Manager (4-store) + Event Bus & Task Orchestrator + Tool Invocation Pipeline as layered in `COGOS-FRAMEWORK-001`.
**Status:** `Draft` (validated against AgenticOS June 2026 / AgentOS Mar 2026 / CoALA / MemGPT / Generative Agents literature; not yet implemented in Red runtime)
**Authors:** Conversation MSG-02 + Analyzer MSG-02 + Auditor
**Verification:** AgenticOS intent-filter table match, CoALA store-type-vs-access-pattern check, event-queue wake-on-event integration test (proposed).

---

## 1. Abstract

Defines the missing layer between the language runtime and the agent: an event-driven, persistent operating environment that manages cognition (Observe→Reflect→Learn), memory (working/episodic/semantic/procedural), and tool execution (Goal→Receipt) — the substrate that CogOS (RFC-0004) later kernelizes.

## 2. Motivation

The REPL was built for a human at a keyboard (polling, single-session variables). Production agents fail at specification (41.8%) and coordination (36.9%) because they lack this environment: they conflate the four memory stores (“goldfish” complaints), lack a policy engine, and replay growing-context at 3.6× tokens. This RFC names and structures the missing layer.

## 3. Specification

### 3.1 Agent Runtime Shell (ARS) — triad (normative)

```
Human / Agent
      │
      ▼
Agent Runtime Shell (ARS)
      ├───────┼───────┐
      ▼       ▼       ▼
Cognitive Engine  Memory System  Tool System
      │       │       │
      ▼       ▼       ▼
Observe → Reason → Plan → Act → Reflect → Learn → Loop
```

Unlike a traditional shell, the ARS is **event-driven**, not just input-driven.

### 3.2 Process Runtime → Cognitive Runtime inversion (normative table)

| Unix Runtime | Agent Runtime |
|---|---|
| Process | **Task** |
| PID | Goal ID |
| File | **Knowledge** |
| Environment Variables | **Working Memory** |
| Process Tree | **Reasoning Tree** |
| Scheduler | **Planner** |
| Signals | **Events** |
| Exit Code | **Confidence / Verification** |

Validated verbatim by `AGENT-ENV-ANALYSIS-001 §I` against AgenticOS (June 2026) “intent filter” and AgentOS (Mar 2026) `System Calls / POSIX → MCP / Semantic API` kernel table — independent convergence, not speculation.

### 3.3 Agent Lifecycle (normative, daemon-like)

`Start → Load Identity → Load Memory → Synchronise Environment → Observe World → Reason → Generate Plan → Request Permissions → Execute → Verify → Store Experience → Sleep → Wake on Event` — more OS daemon than CLI program.

### 3.4 Cognitive Pipeline (normative, 14-stage after correction)

Canonical 11-stage `Observation → Perception → Understanding → Goal Matching → Planning → Scheduling → Execution → Validation → Reflection → Memory Consolidation` **plus three inserted stages** per Analysis §V:

- **Memory Promotion Gate** (between Reflection and Memory Consolidation) — routes `Reflection→(Episodic | Semantic | Procedural | Discard)` per Mem0 hierarchy.
- **Confidence Scoring** (between Validation and Reflection) — calibrated belief about result reliability in multi-tool chains.
- **Identity Verification** (before Observation) — DID-based identity + behavioural trust scoring.

Many stages have **no classical REPL equivalent**.

### 3.5 Memory Hierarchy — **Corrected** (normative)

**Original (deprecated):**

```
Long-Term Knowledge → Semantic → Episodic → Working Memory Graph → Current Context
```

**Corrected (per AGENT-ENV-ANALYSIS-001 §II, CoALA Princeton 2023 + Tulving 1972 / Squire 1987 / Baddeley 1974):**

```
┌──────────────────────────────────────────────────────┐
│                    AGENT MEMORY SYSTEM               │
├────────────────┬───────────────┬───────────────┬──────┤
│ WORKING        │ EPISODIC      │ SEMANTIC      │PROCED│
│ Active context │ Past events   │ Stable facts  │Workfl│
│ Current turn   │ Experiences   │ World model   │Skills│
│ Bounded by     │ Indexed by    │ Context-indep │Compi.│
│ context window │ embedding     │               │      │
└────────────────┴───────────────┴───────────────┴──────┘
```

- Context-window pressure is *fundamental*, not implementation detail (MemGPT page-in/out, Generative Agents importance scoring).
- Degrades asymmetrically without each store; conflation causes most “goldfish” failures.
- Implemented by IBM/MongoDB/LangChain/Letta/Mem0 per Analysis.

### 3.6 Event Sources (normative)

`Filesystem | Network | Calendar | Email | Git | Database | Sensors | User Messages | Timers | Webhooks → Event Queue → Agent Scheduler` — polling → event-driven cognition.

### 3.7 Tool Invocation (normative, 7-stage)

`Goal → Capability Resolver → Policy Engine → Permission Check → Tool Binding → Execution → Receipt`

- The **Policy Engine** is the most critical and least mature (Analysis §III: Microsoft toolkit, OWASP Top 10 mapping goal hijacking→semantic intent classifier, tool misuse→MCP gateway, identity abuse→DID).
- `Receipt` = audit trail, enabling log/verify/replay.

### 3.8 Why Red Is an Interesting Foundation (informative, bridge to RFC-0005)

Blocks represent plans/workflows (`plan: [observe filesystem search "*.log" summarise verify ...]`), homoiconicity enables self-inspection/rewrite (`replace plan ...`), dialects define specialised execution contexts — each maps to a governance requirement. Small standalone binaries suit offline local agents.

### 3.9 Evolutionary Ladder (informative, refined)

`Batch → Shell → CLI → REPL → Notebook → LLM Chat → Agent Runtime → Autonomous OS` with phase changes per `AGENT-ENV-ANALYSIS-001 §VI` (CLI→REPL statefulness, etc.), and toward `Agent Runtime Shell → Agent Operating Environment → Autonomous Digital Operating System` where the shell becomes a cognitive environment managing goals/memory/planning/permissions/tools/learning.

## 4. Consequences

- **Corrected:** Vertical memory stack deprecated; implementers must use 4 parallel stores + context-window eviction.
- **Extended:** Pipeline v2 adds promotion/confidence/identity — omitting them loses governance (Microsoft toolkit) and personalisation/semantic accuracy (Mem0).
- **Red bridging claim:** Dialect = Capability Resolver (hardened in RFC-0005) but ecosystem FFI to Python/Rust remains blocker (OP-01).
- **Rejected:** Single-store memory, poll-based agent loop, receipt-less tool execution.

## 5. Traceability

- **RFC Origin Map rows:** R6–R11 (ARS triad, table, lifecycle, pipeline, memory correction, event queue, tool pipeline, evolutionary ladder).
- **REQ IDs:** REQ-003 (event-driven queue), REQ-004 (4 parallel stores), REQ-005 (7-stage receipt), REQ-009 influence via pipeline stage 10.
- **ADRs:** ADR-002 (4 parallel stores, corrected), ADR-003 (capability-based execution).
- **Formal models:** CoALA 4-store; Tulving/Baddeley/Squire lineage; Generative Agents/MemGPT paging; AgenticOS intent filter; Microsoft Governance Toolkit; OWASP Agentic Top 10.
- **Open problems:** OP-01 (ecosystem FFI blocks Red dialect→tool reach).

## 6. Dependencies

- **Upstream:** RFC-0001 (REPL lifecycle as precedent), RFC-0002 (Red blocks/dialects as primitives).
- **Downstream:** RFC-0004 (CogOS kernelizes ARS triad into Goal Scheduler + Cognitive Kernel), RFC-0005 (types formalise pipeline stages).

## 7. Appendix — Wiki Source Mapping

- `Agent-Operating-Environment.md` (`AGENT-ENV-001`, 263 lines) — §§ triad through agentic shell.
- `Agent-Operating-Environment-Analysis.md` (`AGENT-ENV-ANALYSIS-001`, 163 lines) — §§ I–VII grounding, correction, extensions.
- `Agent-Runtime-Analysis.md` (`AGENT-ANALYSIS-001`, 134 lines) — homoiconicity/dialect→tool scrutiny (strengths + ecosystem gap).
- `TRACEABILITY-ARCHIVE.md` §Phase 0 Steps 5–12, §0.2 Memory/Policy rows.
