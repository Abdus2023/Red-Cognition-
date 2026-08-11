# Components

> Provenance: Corpus message #2, sub-messages [4], [6], [8], [14]. Diagrams verbatim; snippet IDs link to [Code Snippets](Code-Snippets.md). All content is proposed design, not implemented artifacts.

## Cognitive Virtual Machine (CVM) (sub-message [14])

If Red/Cognition becomes a first-class language, the next logical step is to redesign the runtime itself. Instead of executing instructions like a conventional virtual machine, it executes **cognitive operations**. The VM becomes a reasoning engine rather than merely an execution engine.

Today, most VMs execute opcodes such as (**SN-086**): LOAD, STORE, CALL, RETURN, JUMP, ADD, SUB. A **Cognitive Virtual Machine (CVM)** would execute semantic opcodes:

**SN-087**

```text
OBSERVE
RECALL
INFER
PLAN
SELECT
EXECUTE
VERIFY
REFLECT
LEARN
```

(Instruction set details: Cognitive ISA — see [APIs](APIs.md).)

## The Cognitive Kernel (sub-message [8])

The Cognitive Kernel continuously cycles through perception and action. Unlike a traditional scheduler, this loop never truly ends.

**SN-040**

```text
              External World
                     │
                     ▼
              Observe Events
                     │
                     ▼
          Update Working Memory
                     │
                     ▼
            Detect Opportunities
                     │
                     ▼
             Prioritise Goals
                     │
                     ▼
              Generate Plans
                     │
                     ▼
              Execute Actions
                     │
                     ▼
            Verify Outcomes
                     │
                     ▼
           Learn & Consolidate
                     │
                     └───────────────┐
                                     ▼
                               Observe Again
```

Managed resources of the cognitive kernel: see [Architecture](Architecture.md) (SN-026). Microkernel service decomposition: see [Services](Services.md) (SN-120).

## Cognitive Processes (sub-message [8])

Instead of processes, we might define **Cognitive Processes**. A CogProcess resembles both a Unix process and a notebook session, but with persistent knowledge and reasoning.

**SN-041**

```text
CogProcess
Identity
Goal
Context
Working Memory
Capabilities
Policies
Budget
Execution State
Reflection Log
```

## Goals as Scheduling Units (sub-message [8])

Unix schedules processes. Agent runtimes schedule goals. Execution becomes a graph rather than a linear sequence.

**SN-042**

```text
Goal
 │
 ├── Subgoal A
 │      │
 │      ├── Task 1
 │      ├── Task 2
 │      └── Task 3
 │
 ├── Subgoal B
 │
 └── Subgoal C
```

Goal attributes for the native goal scheduler: see [Data Models](Data-Models.md) (**SN-079**). Native Goal Scheduler: traditional runtimes schedule threads (**SN-078**: Thread A/B/C); a cognitive runtime schedules goals — scheduling becomes a language feature instead of an application concern ([12]).

## Knowledge Graph as the New Filesystem (sub-message [8])

Unix stores bytes. A Cognitive OS stores meaning. Instead of locating a file by path, the runtime retrieves information through semantic relationships.

Traditional hierarchy:

**SN-043**

```text
/
├── home
├── etc
├── usr
└── var
```

**SN-044** — Cognitive hierarchy:

```text
Knowledge
├── Facts
├── Concepts
├── Skills
├── Memories
├── Plans
├── Projects
├── Relationships
└── Evidence
```

## Time Becomes First-Class (sub-message [8])

Unix mainly understands **now**. Agents must understand **time**. Planning requires reasoning across multiple timelines.

**SN-045**

```text
Past
 │
 ▼
Experiences
 │
 ▼
Current Situation
 │
 ▼
Predictions
 │
 ▼
Possible Futures
 │
 ▼
Selected Plan
```

## Uncertainty Becomes a Core Primitive (sub-message [8])

Classical software usually assumes deterministic execution. Agents operate with uncertainty. Every observation, memory, and inference may carry a confidence score.

**SN-046**

```text
Observation
Confidence: 0.42
Need More Evidence?
        │
   Yes──┴──No
Collect Data     Execute
```

### Native Uncertainty (sub-message [14])

Most languages treat values as absolute.

**SN-097**

```red
temperature: 25
```

A cognitive language could treat certainty as intrinsic. Every fact has provenance and reliability.

**SN-098**

```text
temperature
value: 25
confidence: 0.91
source: sensor
```

(Related: the agent system prompt [19] refers to "the BDI-style semantics and four-dimensional uncertainty model defined in the specification" — the specification itself is not present in the corpus; see [Source Traceability](Source-Traceability.md) missing items.)

## Reflection Engine (sub-message [8])

Traditional software rarely evaluates its own decisions. Agents do. Reflection is effectively a feedback controller for intelligence.

**SN-047**

```text
Action
     │
     ▼
Expected Outcome
     │
Compare
     │
Actual Outcome
     │
Difference
     │
Lesson Learned
     │
Memory Update
```

## Skills Replace Commands (sub-message [8])

Unix has commands.

**SN-048**

```text
cp
mv
grep
find
awk
sed
```

Agents have skills. A skill may internally invoke dozens of traditional commands, APIs, or models.

**SN-049**

```text
Search Knowledge
Summarise Document
Write Code
Debug Program
Plan Trip
Analyse Repository
Generate Report
Negotiate Schedule
```

First-class skill syntax proposal: see [Data Models](Data-Models.md) (**SN-059**).

## Attention Management (sub-message [14])

One resource absent from traditional operating systems is **attention**. The scheduler allocates reasoning effort according to attention rather than simple arrival order.

**SN-096**

```text
Incoming Events
        │
        ▼
Importance
        │
Urgency
        │
Novelty
        │
Risk
        │
Attention Score
```

## The Model Layer (sub-message [6])

Modern agent systems introduce another resource unknown to classic operating systems: **AI models**. Model selection becomes analogous to selecting the right processor or accelerator.

**SN-036**

```text
Small Local Model
        │
        ▼
Medium Local Model
        │
        ▼
Large Remote Model
```

The runtime chooses the most appropriate model based on: task complexity, latency requirements, privacy constraints, energy consumption, financial cost.

Multi-model reasoning language surface: see [Data Models](Data-Models.md) (**SN-063**).

## Event Sources (sub-message [4])

Traditional shells react only to keyboard input. An agent reacts to many event streams simultaneously. This shifts the model from **polling** to **event-driven cognition**.

**SN-020**

```text
Filesystem
Network
Calendar
Email
Git
Database
Sensors
User Messages
Timers
Webhooks
          │
          ▼
      Event Queue
          │
          ▼
     Agent Scheduler
```

Event-driven cognition language surface: see [Workflows](Workflows.md) (**SN-064**). Layered placement ("Event Bus & Task Orchestrator"): see [Architecture](Architecture.md) (**SN-039**).

## Memory Architecture (sub-messages [4], [14], [18])

### Memory Hierarchy (sub-message [4])

Human cognition inspired modern AI memory architectures. Unlike a REPL, which only preserves variables for one session, an agent preserves **experiences**, **knowledge**, and **plans** across sessions.

**SN-019**

```
                Long-Term Knowledge
                       ▲
                       │
             Semantic Memory Store
                       ▲
                       │
               Episodic Memory Store
                       ▲
                       │
               Working Memory Graph
                       ▲
                       │
                  Current Context
```

Memory Model from the agent system prompt ([18]) — separate memory into distinct layers: Working Memory; Episodic Memory; Semantic Memory; Procedural Memory; Knowledge Graph; Long-Term Archive. Each layer has different lifetime, retrieval, and optimisation strategies. *(Complementary variant of SN-019 — see [Source Traceability](Source-Traceability.md) duplicate log.)*

### Semantic Memory Addressing (sub-message [14])

Traditional memory is addressed by location.

**SN-092**

```text
0x1000
0x1004
0x1008
```

Cognitive memory is addressed semantically. Retrieval becomes associative rather than positional.

**SN-093**

```text
Project/OpenClaw
Architecture/Runtime
Knowledge/Rust
Experience/GitHub
```

### The Cognitive Heap (sub-message [14])

Instead of allocating anonymous objects:

**SN-094**

```red
make object! [...]
```

the runtime allocates semantic entities:

**SN-095**

```text
Goal Object
Observation Object
Plan Object
Memory Object
Evidence Object
Skill Object
```

Each carries metadata such as: creation time; confidence; provenance; dependencies; verification state.

### Knowledge Provenance (sub-message [14])

One of the largest challenges for AI systems is explaining *why* they know something. Every memory should maintain an evidence chain. Instead of merely remembering a conclusion, the runtime remembers how that conclusion was formed.

**SN-099**

```text
Memory
      │
      ▼
Observation
      │
      ▼
Evidence
      │
      ▼
Source
      │
      ▼
Timestamp
```

(See also Provenance Graph, [Workflows](Workflows.md) **SN-115**.)

### Reflection as Garbage Collection (sub-message [14])

Traditional garbage collection removes unreachable objects.

**SN-100**

```text
Object
↓
Unused
↓
Collected
```

A Cognitive Runtime needs an additional process. Rather than simply freeing memory, it curates knowledge.

**SN-101**

```text
Memory
↓
Useful?
↓
Compress
↓
Summarise
↓
Archive
↓
Forget
```

(Complementary variant: Cognitive Garbage Collection, [Design Decisions](Design-Decisions.md) **SN-117**.)

## Native Multi-Agent Runtime (sub-message [14])

Instead of multiple processes:

**SN-102**

```text
Process A
Process B
Process C
```

the runtime hosts multiple collaborating cognitive entities:

**SN-103**

```text
Planner Agent
Reviewer Agent
Executor Agent
Verifier Agent
Memory Agent
```

Each has: independent working memory; specialised skills; shared semantic knowledge; message passing; policy constraints. This resembles actor systems but with richer cognitive state.

Agent declarations proposal: see [Workflows](Workflows.md) (**SN-081**, message passing **SN-082**).

## A Cognitive Object Model (sub-message [14])

Red's object system could evolve beyond state and methods. Instead of objects modelling *things*, they model *reasoning entities*.

**SN-104**

```red
agent! [
    beliefs
    goals
    memories
    skills
    policies
    capabilities
    reflection
]
```

## Related pages

[Architecture](Architecture.md) · [APIs](APIs.md) · [Data Models](Data-Models.md) · [Workflows](Workflows.md) · [Services](Services.md)

---

## Message #3 additions — Normative definitions (RC-100 v1.1, corpus message #3)

### Four-tier memory topology (RC-100 §7; ADR-0004 sketch [36]; approved [40] §6)

| Tier | Purpose | Characteristics |
|---|---|---|
| Working Memory | Current context | Short-lived, bounded (, fast access [37]) |
| Episodic Memory | Events and experiences | Timestamped, provenance-aware |
| Semantic Memory | Knowledge and concepts | Structured, queryable, persistent |
| Procedural Memory | Skills and capabilities | Compiled, performance-tracked |

"Memory should not be a single vector database" ([36] ADR-0004). Memory ownership and mutation events MUST be observable by owning agents (RC-100 §7). **Collective Memory** (distributed shared knowledge) is a future RC-800 concern ([38] §8, RC-100 v1.1 §7). This is the normative consolidation of earlier variants SN-019 ([4]) and the [18] six-layer Memory Model — see duplicate log D-4.

### Cognitive Runtime API (LICM example, [38] §4)

observe() · remember() · recall() · reason() · plan() · execute() · verify() · checkpoint() · restore() · explain() — complementary variant of earlier primitive lists (D-2).

### CEC-1 execution cycle

Canonical lifecycle: see [Architecture](Architecture.md) Normative Reference Architecture and [Workflows](Workflows.md).

### Static Core + Dynamic Shell (ADR-0003 sketch, [36])

Dynamic Layer: Agent Runtime Shell, Skills, Policies, Plugins, User Extensions. Static Core: Cognitive VM, Runtime Kernel, Memory Engine, Scheduler, Capability System, Event System. Preserves determinism, security, portability, inspectability.

---

## Message #4 additions — Runtime component models (RC-400/RC-500, msg#4 [55]–[58])

### Red Runtime + Cognitive Runtime components (RC-400 §3)

Red Runtime: Core Execution Engine · Memory Manager · Scheduler · Event System. Cognitive Runtime: Cognitive Execution Engine (CEC-1) · Memory Hierarchy Manager · Capability Enforcement · Trace & Checkpoint System · Agent Lifecycle Manager. Runtime Kernel Boundary ([56]): Runtime Kernel → Red Services | Cognitive Services — prevents Cognitive Runtime from directly modifying core runtime behaviour.

### Cognitive Runtime service model (ADR-0006 per [58])

Cognitive Runtime = replaceable services: Execution Service (CEC-1 lifecycle) · Memory Service (Working/Episodic/Semantic/Procedural) · Capability Service (effect authorization) · Trace Service (replay and explainability) · Agent Lifecycle Service (Spawn / Run / Suspend / Restore / Terminate).

### Memory management responsibilities (RC-400 §6; RC-500 §6)

| Tier | Management (RC-400) | Persistence | Ownership (RC-500) |
|---|---|---|---|
| Working Memory | Bounded context storage | Ephemeral | Per agent |
| Episodic Memory | Event and experience storage | Persistent | Per agent |
| Semantic Memory | Knowledge graph storage | Persistent | Shared |
| Procedural Memory | Skill and capability storage | Persistent | Shared |

Ownership tracking and observable mutation events MUST be supported for all tiers.

### Compiler component model (RC-300 v1.1 §4)

Compiler Kernel → Frontend / Analysis / Backend (replaceable subsystems, LICM interfaces). Frontend/Analysis detail per [52]: Parser, AST, Dialect Lowering | Type System, Effects, Capability Verification | Red/System, C-Backend, Cognitive VM, Future Targets.

### Cognitive Runtime API (proposed, [58])

`CognitiveRuntimeAPI { execute-cycle(), store-memory(), retrieve-memory(), request-capability(), emit-trace(), create-checkpoint(), restore-checkpoint() }` — mechanism implementation-defined. Complements msg#2 Cognitive ABI (SN-121) and [38] LICM API example — see duplicate log D-2.

---

## Message #8 additions — CVM & CogOS components (msg#8 [61]–[64])

### CVM (Layer 6) per RC-700

Built on Cognitive Runtime (Layer 4) + RC-400 services; MUST use Cognitive Runtime for memory/capabilities/tracing/agent lifecycle; LICM respected. Execution model: CEC-1 executed via CISA instructions; deterministic instruction sequences; interruption/resumption at instruction boundaries; checkpointing; replay from checkpoints and traces. State (RC-700 §6): instruction pointer, working memory references, active capabilities, execution trace, checkpoint references — serializable and restorable. Capability integration: check capabilities before execution; record usage in trace; prevent execution on violation. Full CISA detail in [Architecture](Architecture.md).

### CogOS (Layer 7) per RC-800

Built on CVM (Layer 6), Cognitive Runtime (Layer 4), RC-400 services. Seven core services: process management, system-wide capability governance, memory system coordination, event/messaging infrastructure, scheduling/resource allocation, security/isolation, checkpoint/recovery coordination. Cognitive Process = fundamental execution unit (ADR-0012 per [64]); isolation model, resource model, scheduler classes S0–S3, memory domains, security domains — see [Architecture](Architecture.md). Multi-agent coordination: shared memory with access control, capability-enforced messaging, system-wide event distribution. Distributed foundation: remote CVM instances, distributed memory/events, cross-node capability enforcement.

---

## Message #14 additions — runtime subsystems & services (msg#14 [125]–[140])

### Cognitive Runtime subsystems (RFC-0016 [125])

**Agent Manager:** creation/initialization/termination of agents; identity & ownership management; lifecycle state coordination; isolation of execution contexts. **Scheduler:** selection/ordering of cognitive processes; fairness/priority/deadline enforcement; queues & blocking states; checkpoint/recovery integration. **CVM Executor:** CISA instruction execution; execution context management; instruction-level capability checks; instruction traces. **Memory Manager:** four-tier memory management; ownership & access control; memory snapshots for checkpointing; deterministic memory operations. **Capability Manager:** granting/revocation/verification; checks before external effects; audit logs; delegation support. **Trace Engine:** instruction/effect/capability/exception/scheduler traces; execution history; deterministic replay; explainable records. **Exception Manager:** exception handling; rollback/compensation coordination; propagation to scheduler/agent manager; exception traces. **Checkpoint Manager:** checkpoint creation/storage; restoration; cross-subsystem coordination; integrity validation. Relationships: built on Red Runtime, CVM, Memory system, Scheduler; MUST NOT bypass/redefine lower-layer semantics; serves Agent Runtime Shell, CogOS, Distributed Agent Network.

### Runtime service interfaces (RFC-0017 [127] §3)

**Agent Service:** CreateAgent(...)→AgentID · InitializeAgent · GetAgentState→AgentState · SuspendAgent · TerminateAgent. **Scheduler Service:** Enqueue(ExecutionContext) · Dequeue()→ExecutionContext · Block(AgentID, Reason) · Unblock · Preempt(CurrentContext)→NextContext. **CVM Executor Service:** Execute(ExecutionContext, InstructionCount?)→ExecutionResult · Yield · GetExecutionContext. **Memory Service:** Read(MemoryTier, Reference)→Value · Write · Append · CreateSnapshot()→MemorySnapshot · RestoreSnapshot. **Capability Service:** RequestCapability(AgentID, CapabilityType, Scope)→CapabilityID · VerifyCapability(CapabilityID, Action)→Boolean · RevokeCapability · GetCapabilityState→CapabilitySet. **Trace Service:** Record(TraceEvent) · GetTrace(TraceID)→Trace · GetAgentTrace(AgentID, Range?). **Exception Service:** Raise(Exception) · Handle(Exception)→RecoveryAction · GetExceptionTrace(ExceptionID)→Trace. **Checkpoint Service:** CreateCheckpoint(AgentID)→CheckpointID · RestoreCheckpoint(CheckpointID)→ExecutionContext · ValidateCheckpoint→Boolean. Event bus types: ScheduleDecision, InstructionExecuted, MemoryMutated, CapabilityVerified, ExceptionRaised, CheckpointCreated — all MUST carry provenance and timestamp. Pluggable providers: memory backends, scheduling policies, trace storage, exception handling strategies.

### CogOS core services (RFC-0019 [131] §3)

Cognitive Process Management (incl. process isolation) · System-Wide Capability Governance (centralized granting/revoking, system-level auditing) · Shared Memory Coordination (shared Semantic/Procedural Memory, access control, consistency) · Event and Messaging Infrastructure (system-wide routing, capability-enforced inter-agent messaging) · Resource Management (allocation/accounting of execution time, memory, capability usage; quotas/limits) · Security and Isolation (process isolation boundaries, system-level policy enforcement) · Checkpoint and Recovery Coordination (system-level management, coordinated multi-agent restoration). Recommended extensions ([132]): CogOS identity { CogOSID, Version, PolicyVersion, SupportedRFCs, ConfigurationHash }; CognitiveDomain { DomainID, Owner, Agents, MemoryNamespaces, PolicySet }; Policy { PolicyID, Scope, Rules, Priority, EnforcementMode } with DENY/ALLOW rules.
