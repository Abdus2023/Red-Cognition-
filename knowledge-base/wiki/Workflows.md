# Workflows

> Provenance: Corpus message #2, sub-messages [1], [2], [4], [6], [8], [10], [12], [14], [16]. Snippet content preserved verbatim; IDs link to [Code Snippets](Code-Snippets.md).

## Text Interface Layers (sub-message [1])

Text-based computing operates across three primary layers. Each layer balances **automation efficiency** against **human flexibility**. Command-line ecosystems operate across distinct layers of interaction, moving from **one-shot scriptable commands** to **stateful, continuous evaluation environments**. Understanding the differences between a standard CLI, interactive prompts, and REPLs is essential for efficient software development and system administration.

### The Lifecycle of a CLI Command (sub-message [1])

A Command Line Interface operates on a Stateless Request-Response cycle. It is designed to bridge the user, the operating system shell, and the file system.

**SN-002**

`[User Input] ➔ [Shell Parses Flags/Args] ➔ [OS Spawns Process] ➔ [Process Executes & Out] ➔ [Process Dies/Exit Code]`

### 1. Command-Line Interface (CLI) & Commands (sub-message [1])

A CLI is a text-based interface used to operate software and operating systems. It relies on a request-response pattern. You type a command, the shell executes it, prints the output, and terminates the process.

### Anatomy of a CLI Command (sub-message [1])

**SN-003** (language tag as given: `bash`). ⚠ Received flattened; preserved unchanged — see [Code Snippets](Code-Snippets.md).

```
docker container run -d --name web_server -p 80:80 nginx:latest # └───┬──┘ └───┬───┘ └─┬┘ └────────┬─────┘ └───┬───┘ └───┬────┘ #   Binary  Subcommand Flag     Arguments     Option   Argument
```

### 2. CLI Interactive Prompt (sub-message [1])

An Interactive Prompt is a temporary state inside a CLI workflow where execution pauses to gather input from a human user. It transitions a command from a static script to an active dialogue

### 3. CLI REPL (Read-Eval-Print Loop) (sub-message [1])

A REPL is a continuous, stateful interactive programming environment. Instead of executing an external program and exiting, a REPL runs an engine that waits for you to type code snippets, evaluates them on the fly, and keeps the results in system memory.

### The Four-Step Lifecycle Loop (sub-message [1])

**SN-004**

```
┌────────────────────────────────────────────────────────┐
│                                                        │
▼                                                        │
[READ] ──► Reads code input string into memory buffers.  │
   │                                                     │
[EVAL] ──► Compiles/Interprets code via the engine.      │
   │                                                     │
[PRINT] ─► Formats and dumps evaluation result to screen.│
   │                                                     │
   └─────────────────────────────────────────────────────┘
```

### The Lifecycle of a REPL Session (sub-message [1])

A Read-Eval-Print Loop operates on a Stateful, Persistent Environment. It acts as a live runtime sandbox, typically for a specific programming language.

**SN-005**

```
┌────────────────────────────────────────┐
│  ▶ READ: Parse token inputs            │
│  ▼ EVAL: Compute in memory context     │
│  ▶ PRINT: Stringify resulting value    │
│  ▲ LOOP: Await next input vector       │
└────────────────────────────────────────┘
```

1. Read: The environment scans user input, performs lexical analysis, and parses it into an Abstract Syntax Tree (AST) or token set.
2. Eval: The interpreter evaluates the expressions within a persistent context. If you define a variable here, it is bound to the current environment's memory space.
3. Print: The system automatically outputs the evaluated result of the expression, even without an explicit `print()` or `console.log()` command.
4. Loop: The environment loops back to the read phase, holding all declared variables, functions, and imported modules active in RAM until the user explicitly quits the session `exit()`). *(Unmatched parenthesis preserved as received.)*

**SN-006** — Comparison:

```
[Standard CLI] ------------> [Interactive Prompt] -------> [REPL Environment]
  - Fully Automated            - Semi-Automated             - Fully Exploratory
  - One-shot execution         - Step-by-step input         - Stateful memory loop
  - Stateless                  - Scripting roadblock        - Live evaluation
```

That final category—an **agent runtime shell**—extends the REPL concept from **Read → Eval → Print → Loop** to something closer to **Observe → Reason → Plan → Act → Reflect → Loop**, making it a natural interface for autonomous AI systems. ([1])

## Extending REPL into an Agent Loop (sub-message [2])

Traditional REPL (**SN-010**):

```
READ
 ↓
EVAL
 ↓
PRINT
 ↓
LOOP
```

Agent Runtime (**SN-011**):

```
OBSERVE
    ↓
UNDERSTAND
    ↓
REASON
    ↓
PLAN
    ↓
SELECT TOOLS
    ↓
EXECUTE
    ↓
VERIFY
    ↓
LEARN
    ↓
MEMORISE
    ↓
LOOP
```

Notice that **Read** becomes **Observe**, and **Print** becomes **Act** plus **Reflect**.

## Agentic Red REPL (sub-message [2])

A future "Agent REPL" written in Red might look like this. Instead of typing commands manually, the runtime continuously observes its environment and decides the next action.

**SN-012**

```
observe "Directory contains 500 log files"

reason [
    detect-patterns
    estimate-cost
    choose-parser
]

plan [
    parse
    summarize
    archive
]

act [
    parse-logs
    generate-report
]

reflect [
    verify-output
    store-memory
]
```

## Agent Flows in Red Data (sub-messages [2], [4], [6])

**SN-007** — Homoiconicity → Reasoning flow ([2]):

```
Task
  ↓
Generate Red Block
  ↓
Inspect
  ↓
Modify
  ↓
Execute
  ↓
Observe Result
```

**SN-008** — Dialects → AI Skills flow ([2]):

```
Natural Language
        ↓
Planning
        ↓
Generate Dialect
        ↓
Run Specialized Engine
```

**SN-009** — Red/System → Hardware Layer ([2]):

```
Reason
   ↓
Red
   ↓
Red/System
   ↓
Machine Code
   ↓
Hardware
```

**SN-022** — Agent plan as native data ([4]). Because the plan is a data structure, it can be analysed, modified, optimised, or executed by the runtime itself:

```red
plan: [
    observe filesystem
    search "*.log"
    summarise
    verify
    archive
    notify
]
```

**SN-037** — Cognitive workflow in Red ([6]). This is not just executable code—it is also a readable representation of intent. Because Red is homoiconic, the runtime can inspect, transform, optimise, or even synthesise these workflows before executing them:

```red
goal [
    observe filesystem
    search "*.rs"
    analyse architecture
    compare with memory
    generate report
    verify
]
```

## Agent Lifecycle (sub-message [4])

A modern agent rarely starts from a blank slate. This resembles an operating system daemon more than a command-line program.

**SN-017**

```
Start
   │
Load Identity
   │
Load Memory
   │
Synchronise Environment
   │
Observe World
   │
Reason
   │
Generate Plan
   │
Request Permissions
   │
Execute
   │
Verify
   │
Store Experience
   │
Sleep
   │
Wake on Event
```

## Internal Cognitive Pipeline (sub-message [4])

Instead of a single evaluation stage, an agent has multiple specialised stages. Many of these stages have no equivalent in a classical REPL.

**SN-018**

```
Observation
      │
      ▼
Perception
      │
      ▼
Understanding
      │
      ▼
Goal Matching
      │
      ▼
Planning
      │
      ▼
Scheduling
      │
      ▼
Execution
      │
      ▼
Validation
      │
      ▼
Reflection
      │
      ▼
Memory Consolidation
```

## Cognitive Pipes (sub-message [6])

Unix pipelines move bytes (**SN-029**: `cat log.txt | grep error | sort | uniq`). An agent pipeline moves **knowledge**. The data flowing through the pipeline are semantic structures rather than text streams.

**SN-030**

```text
Observe
    │
    ▼
Extract Facts
    │
    ▼
Infer Relationships
    │
    ▼
Generate Plan
    │
    ▼
Execute
    │
    ▼
Reflect
```

## Tool Invocation (sub-message [4])

Instead of executing binaries directly, the runtime resolves capabilities. Every action can be logged, verified, and replayed, enabling auditability. (Security aspects: [Security](Security.md).)

**SN-021**

```
Goal
  │
  ▼
Capability Resolver
  │
  ▼
Policy Engine
  │
  ▼
Permission Check
  │
  ▼
Tool Binding
  │
  ▼
Execution
  │
  ▼
Receipt
```

## Planning as Scheduling (sub-message [6])

Today's schedulers optimise CPU utilisation. An agent scheduler optimises reasoning. A task with higher urgency or greater expected value may be prioritised over one that merely arrived first.

**SN-035**

```text
Incoming Goals
       │
       ▼
Priority Analysis
       │
       ▼
Dependency Resolution
       │
       ▼
Risk Assessment
       │
       ▼
Resource Allocation
       │
       ▼
Execution Queue
```

## The Planner Becomes a Compiler Pass (sub-message [12])

Imagine writing (**SN-071**):

```red
goal generate-report [
    inspect repository
    analyse changes
    write summary
]
```

The planner expands this into an executable graph (**SN-072**). Planning becomes analogous to macro expansion or optimisation.

```
Inspect Repository
        │
        ▼
Find Changed Files
        │
        ▼
Classify Changes
        │
        ▼
Summarise
        │
        ▼
Verify
```

## Self-Modifying Plans (Not Self-Modifying Code) (sub-message [12])

Red's homoiconicity allows programs to manipulate themselves. A cognitive version should avoid rewriting executable code directly. Instead, it rewrites **plans**. Knowledge evolves while the trusted runtime remains stable.

**SN-080**

```
Original Plan
        │
Execute
        │
Reflect
        │
Improve Plan
        │
Store Improved Plan
```

## Native Multi-Agent Support — Message Passing (sub-message [12])

Red objects already represent encapsulated state. A cognitive extension could treat every object as an independent agent. This aligns naturally with distributed agent systems.

**SN-081**

```red
agent planner [...]
agent reviewer [...]
agent executor [...]
agent verifier [...]
```

Communication could resemble message passing (**SN-082**):

```
Planner
   │
Proposal
   ▼
Reviewer
   │
Approved
   ▼
Executor
   │
Receipt
   ▼
Memory
```

(Agent roster variant: [Components](Components.md) **SN-103**.)

## Event-Driven Cognition (sub-message [10])

Instead of only reacting to user input — the runtime continuously responds to events from filesystems, networks, timers, sensors, or other agents.

**SN-064**

```red
when filesystem changes [
    observe
    reason
    update memory
    notify
]
```

## Knowledge Flow Analysis (sub-message [16])

Compilers perform data-flow analysis. A cognitive compiler performs **knowledge-flow analysis**. Every action can be traced back to supporting evidence.

**SN-114**

```text
Observation
      │
      ▼
Evidence
      │
      ▼
Inference
      │
      ▼
Decision
      │
      ▼
Action
```

## Provenance Graph (sub-message [16])

Every cognitive object records its lineage. This enables explainability and auditing.

**SN-115**

```text
Sensor
     │
     ▼
Observation
     │
     ▼
Reasoning Step
     │
     ▼
Decision
     │
     ▼
Action
```

## Native Time Travel (sub-message [16])

Traditional debuggers replay execution. A cognitive runtime replays reasoning. Developers could inspect not only *what* happened but *why* each decision was made.

**SN-118**

```text
Goal
     │
Observation
     │
Inference
     │
Decision
     │
Execution
     │
Reflection
```

## Related pages

[Components](Components.md) (kernel loop SN-040, reflection engine SN-047) · [Security](Security.md) (capability-based execution SN-060/SN-061, capability computing SN-032) · [Design Decisions](Design-Decisions.md) (cognitive GC SN-117)

---

## Message #3 additions — Normative workflows (sub-messages [26]–[40])

### CEC-1 — Cognitive Execution Cycle (canonical; RC-100 §6, named in [38])

Observe → Interpret → Retrieve Memory → Reason → Plan → Act → Verify → Reflect → Checkpoint → Loop. Embedded with full context in [Architecture](Architecture.md) (Normative Reference Architecture). Variants in corpus (complementary, see duplicate log): [28] 12-step lifecycle (adds Schedule/Learn/Persist), [34] RFC-0002 9-step outline, [36] ADR-0005 outline. **CEC does not replace REPL** — the REPL remains part of Layer 5 Agent Runtime Shell ([40] §5).

### Multi-Agent Collaboration Protocol (RC-000 §9; [26] §9; [34] Governance Flow)

Research Agent → Architecture Review → RFC Author → Compiler Review → Runtime Review → Verification (Agent) → Documentation (Agent) → Chief Architect Approval (→ Implementation per [34]).

### Capability mediation invariant ([40] §7)

An agent does not directly perform effects. Incorrect: Agent → File System. Correct: Agent → Capability → Permission Check → File System. Approved capability model: Agent → Capability Request → Policy Engine → External Effect.

### Language Evolution Ladder workflow (RC-000 §5.1)

Research → Concept → RFC Draft → Prototype → Experimental → Preview → Stable → Core Language — no feature may skip stages.

### Release pipeline (RC-000 §6.4)

Nightly → Experimental → Beta → Stable → LTS.

---

## Message #4 additions — Normative & recommended workflows (msg#4 [51]–[60])

### Compilation pipeline flow (RC-300; SN-267 and updated model SN-277)

Source → Lexer/Parser → Red AST → {Normal Red Code → Red IR | Cognitive Blocks → Dialect Lowering → Cognitive IR} → Unified IR → backends (Red/System / Bytecode / Cognitive VM).

### Agent lifecycle (RC-400 §8; extended states [56])

Spawn → Initialize (identity, capabilities, memory) → Run (cognitive execution cycles) → Checkpoint/Restore → Terminate. Normative state set recommended: Created → Initialized → Active → Suspended → Checkpointed → Restored → Terminated.

### Cognitive vs runtime control flows ([56])

Cognitive Control Flow (managed by Cognitive Runtime): Observe → Reasoning Request → Plan Selection → Execution. Runtime Control Flow (managed by runtime): Schedule → Execute → Trace → Checkpoint.

### Shell interaction flow ([60])

Human Command → Shell Parser → Intent Request → Cognitive Runtime → Trace Result. Autonomy levels gate execution: A0 Manual → A1 Assisted → A2 Supervised → A3 Autonomous → A4 Distributed Autonomous.

### Cognitive representation workflow (ratified contract, [50])

Cognitive Concept → Red Block Representation → Cognitive Dialect Interpretation → Cognitive Runtime Execution → Traceable Effects. MUST NOT be bypassed without an approved RFC.

### Cognitive block evaluation workflow ([44])

`goal [...]` → Block Value → Cognitive AST → Cognitive Runtime Evaluation; explicit `evaluate goal-block` / `run goal-block` required.

---

## Message #8 additions — Normative lifecycles & processes (msg#8 [65]–[80])

### RFC lifecycle (RC-900 §4.1, [65])

Research → RFC Draft → Architecture Review → Public Comment → Final Review → Approval / Rejection / Deferral.

### Effect lifecycle (RFC-0002, ratified [76])

Created → Validated → Authorized → Scheduled → Executing → Committed → Archived (rollback/compensation transitions where supported by class and metadata).

### Belief lifecycle + revision (RFC-0003 v1.1 [79]; [80])

Created → Confirmed/Updated → Contradicted → Deprecated/Archived; semantic status separate from lifecycle (tentative/confirmed/disputed/deprecated/retracted); revision graph (branching, reconciliation, replay of any valid path); causal chain Action → effect! → belief revision → plan revision → goal evaluation.

### CVM program example ([62])

`cvm [ OBSERVE sensor-data RECALL maintenance-history PLAN repair-goal EXECUTE repair-action VERIFY result CHECKPOINT ]` — observation/reasoning/planning instructions invoke external providers; EXECUTE is capability-mediated.

### Prototype execution flow (Phase 2, [66])

`goal [achieve: system-healthy priority: high] run goal` → CEC-1 (Observe → Interpret → Retrieve Memory → Reason → Plan → Act → Verify → Reflect → Checkpoint) with trace: Goal Created, Goal Planned, Capability Requested, Action Executed, Result Verified, Checkpoint Stored.

---

## Message #10 additions — Normative lifecycles (msg#10 [81]–[100])

- **Belief lifecycle (ratified RFC-0003 v1.2):** Created → Confirmed/Updated → Contradicted → Deprecated/Archived (+ revision DAG).
- **Goal lifecycle (ratified RFC-0004 v1.1):** Created (Pending) → Active → Planning → Executing → Satisfied/Failed → Archived (backward transitions only via checkpoint restore).
- **Plan lifecycle (RFC-0005 v1.0):** Draft → Validated → Executable → Running → Completed/Failed/Abandoned (recommended additions: Suspended state, revision DAG).
- **Capability lifecycle (RFC-0006 v1.2):** Created → Granted → Active → Revoked/Expired; resolution order Exists → Active → Scope Valid → Not Expired → Not Revoked → Policy → Allow Effect (short-circuit at first failure).
- **Skill lifecycle (RFC-0007 v1.1):** Created → Registered → Active → Deprecated → Archived; invocation recorded via SkillInvocation/SkillTrace (recommended invocation lifecycle: Created→Validated→Authorized→Executing→Completed/Failed→Archived).
- **Memory lifecycle (recommended, [100]):** Created → Active → Updated → Archived → Deleted (optional; logical deletion).
- **Cognitive causal loop ([88]):** Goals define intent → planning generates strategies → skills execute steps → effects change the world → beliefs are revised → updated beliefs influence future planning and goal evaluation.

---

## Message #12 additions — execution workflows (msg#12 [101]–[120])

- **Agent lifecycle (RFC-0009):** Created → Initialized → Active → Suspended → Checkpointed/Restored → Terminated. Recommended agent execution loop ([102]): Observe → Update Beliefs → Evaluate Goals → Select Plan → Invoke Skills → Produce Effects → Update Memory.
- **Checkpoint lifecycle (RFC-0010):** Created → Stored → Restored → Archived; consistency boundaries before/after plan execution, after effect commitment, after belief revision, after transaction completion ([104]).
- **Scheduler state machine (RFC-0011, ratified):** Runnable → Waiting → Executing → Suspended → Terminated with legal-transition table; WaitingReason recorded; decisions traced via ScheduleDecision records.
- **CVM instruction pipeline (RFC-0012):** Fetch → Decode → Validate → Capability Check → Execute → Produce Effects → Update Trace → Advance Instruction Pointer; per-instruction transaction: Begin → Validate → Capability Check → Execute → Generate Effects → Commit → Trace (failure → Abort → Trace → No Partial Effects).
- **CISA full execution pipeline ([118]):** Fetch Instruction → Decode Opcode → Validate Operands → Check Capability → Execute Semantic Operation → Generate Effects → Commit State → Write Trace → Advance PC.
- **Atomic effect boundary (recommended, [118]):** EFFECT_BEGIN → EFFECT_EMIT → EFFECT_VALIDATE → EFFECT_COMMIT → TRACE_APPEND.
- **Deterministic external input replay ([114]):** record ExternalInputRecord at original execution; replay from trace (Original: Sensor → 25°C; Replay: Trace → 25°C — not Sensor → 27°C).
- **Checkpoint restoration failure outcomes ([104]):** Success / ValidationFailure / MissingDependency / CorruptedCheckpoint / UnsupportedVersion — each MUST be recorded in the execution trace.
- **Agent termination duties ([102]):** archive active traces, archive goals, release capabilities, flush Working Memory, produce a termination effect.

---

## Message #14 additions — failure, replay, migration workflows (msg#14 [121]–[140])

- **Exception propagation (RFC-0015 §4):** on exception — 1. instruction transaction aborted; 2. partial effects rolled back (where supported); 3. exception recorded in trace; 4. control transferred to exception handler or scheduler. Path: Instruction → CVM Exception Handler → Cognitive Runtime → Scheduler / Agent Runtime Shell.
- **Failure transaction flow ([124]):** Begin → Validate → Capability Check → FAIL → Abort → Rollback → Generate ExceptionTrace → Recovery.
- **Recovery levels ([124]):** Instruction level (retry) · Skill level (retry/compensate) · Plan level (abort step/replan) · Goal level (fail/create alternative goal) · Agent level (suspend/checkpoint/escalate). Recovery actions MUST be recorded in the execution trace.
- **CVM decoding pipeline ([122]):** Read Magic → Verify Version → Decode InstructionID → Decode Opcode → Decode Operands → Resolve Capability → Execute Transaction → Produce Trace.
- **Deterministic replay pipeline (RFC-0018/[130]):** Event DAG → Replay Engine → Scheduler/CVM/Memory Reconstruction → Equivalent Behaviour; replay modes L0 trace / L1 state / L2 execution; external inputs replayed from recorded values.
- **Runtime tick loop ([126]):** collect runnable → scheduler selects → CVM executes → effects generated → capabilities validated → memory updated → trace appended → checkpoint boundary evaluated → scheduler continues.
- **Event-sourced causal timeline ([128]):** t1 AgentCreated → t2 CapabilityGranted → t3 GoalActivated → t4 PlanScheduled → t5 InstructionExecuted → t6 EffectProduced → t7 CheckpointCreated.
- **Multi-agent communication (RFC-0019/[132]):** Agent → Message → Capability Check → Event Log → Receiver (never shared mutable state).
- **Agent migration (RFC-0020/0021):** Source Node (Checkpoint + Capabilities + Trace Context) → CNP StateTransfer → Target Node (Validate → Restore → Resume); AgentID remains unchanged; migration recorded as system-level effect; target validates capabilities before resuming.
- **Capability federation flow ([134]/[136]):** Agent A → Capability Token → Node A → Delegation Verification → Node B → External Effect; revocation propagation: Capability revoked at Node A → CNP propagation → Node B denies usage.
- **Consensus participation chain ([140]):** Identity → Authentication → Capability Check → Consensus Permission → Vote/Agreement; Remote Execution → Agreement Required → Commit Execution Result.

---

## Message #16 additions — governance & verified-deployment workflows (msg#16 [141]–[160])

- **Resource-gated execution ([142]):** Agent → Request execution → Check quota → Check capability → Schedule → Execute → Account usage → Record event → Update quota state. Scheduler check extension: Select next runnable process → Check {priority, deadline, fairness, capability, resource quota} → Execute. Quota-violation example: EFFECT_EMIT + capability allowed + quota exceeded → ResourceError, no effect committed, trace generated.
- **Authorization decision process (RFC-0025 [143]/[144]):** collect applicable policies → evaluate conditions in priority order → first matching rule (Allow/Deny) → record decision + provenance; default Deny. Full chain: Agent → Identity Verification → Trust Evaluation → Policy Evaluation → Capability Verification → Resource Check → Scheduler Decision → CVM Execution → Trace. Distributed policy agreement: Policy Conflict → Consensus Event → Global Policy State.
- **CPCPF verification lifecycle (RFC-0033 §4):** 1. verify cryptographic hash and signature; 2. validate CIR structure and version; 3. re-verify all attached optimization proofs (via COVF); 4. confirm declared capabilities available; 5. validate resource requirements within quotas; 6. confirm CVM/CISA revision compatibility — execution only begins after verification. Loader flow ([160]): CPCPF Loader → Verify Artifact Identity → Validate CIR Graphs → Validate COIL History → Check COVF Proofs → Verify Capabilities → Verify Resource Limits → Load CISA → Execute CVM.
- **Cognitive package verification ([152]):** 1. Verify Identity → 2. Verify Signature → 3. Verify CIR Hash → 4. Verify Capabilities → 5. Verify Runtime Compatibility → 6. Execute.
- **COVF verification pipeline ([158]):** CIR → COIL Transformation → Verification Condition Generator → {SMT Solver | Theorem Prover} → Optimization Proof → Transformation Certificate → Validated CIR. Verification domains: effect preservation (order per RFC-0002), goal preservation (Satisfied(Goal_before) = Satisfied(Goal_after)), capability preservation, replay equivalence (ObservableBehavior(A) == ObservableBehavior(B)).
- **COIL transformation flow ([156]):** Optimization Pass → COIL Transformation → Verification Conditions → Transformation Certificate → Modified CIR; "Transformation + Proof Obligation + Certificate = Accepted Optimization".
- **Hardware-accelerated execution ([146]):** Input State → CISA Instruction → Accelerated Execution → Result → Trace Verification; replay with missing accelerator → Software Fallback → Equivalent Result.
- **Self-verifying compilation ([158]):** Agent Program → Compile → Optimize → Prove Optimization Correct → Deploy; policy example: "Do not execute optimized code unless optimization proof is valid."

---

## Message #18 additions — ecosystem workflows (msg#18 [161]–[180])

- **Package installation protocol (RFC-0034 §7, 10 steps):** Discover → Resolve Dependencies (deterministic) → Download CPCPF → Verify integrity (hash + signature) → Validate proof certificates (COVF) → Check capabilities → Evaluate security policies (CSPL) → Verify resource quotas → Install only if all checks pass → Register in local event log. Runtime MUST reject packages failing verification.
- **Sandbox lifecycle (RFC-0035 §5):** Create → Verify CPCPF Artifact → Initialize CVM → Attach Capabilities → Allocate Resources → Execute → Checkpoint → Suspend/Resume → Terminate; all transitions generate RFC-0018 events. Execution modes: Verified (T4/T5, max optimization, HW acceleration), Restricted (T2/T3, limited capabilities, strict quotas, mandatory tracing), Experimental (T0/T1, no production effects, simulation-only).
- **Software lifecycle (RFC-0037 §3):** Created → Built → Verified → Published → Deployed → Observed → Updated → Migrated → Retired; each transition generates lifecycle events. Version migration: Checkpoint Current State → Validate Target Version → Transform State → Verify Compatibility → Resume Execution. Update safety: CPCPF verification + CBR-SCP provenance + CPR-TDP trust + CSPL policy + sandbox compatibility; unsafe updates rejected. Rollback requires previous CPCPF artifact, compatible checkpoint, event log position, capability state restoration.
- **Build provenance chain (RFC-0036 §4):** Source Code →(hash)→ Compiler Invocation →(identity+version+flags)→ CIR Generation →(CIR hash)→ Optimization Passes (COIL+COVF) →(certificates+proofs)→ CISA Generation →(binary hash)→ CPCPF Packaging →(final hash+signature). Bit-identical output for identical inputs; fixed compiler version/config; canonical ordering; reproducible RNG; timestamp normalization.
- **Deployment validation pipeline (RFC-0042 §4, 7 steps):** Verify CPCPF integrity → Verify optimization proofs → Verify capabilities → Evaluate security policies → Check resource quotas → Validate federation agreements → Approve governance requirements; deployment only after full success.
- **Deployment state machine (RFC-0042 §5):** Pending → Validating → Approved → Provisioning → Running → Monitoring → Updating/Suspended → Retired → Archived.
- **CADP normative lifecycle stages (RFC-0042 §3):** Created → Compiled & Verified → Packaged (CPCPF) → Registered (CPR-TDP) → Governance Approved (CGCDP) → Federated (CIFP) → Deployed (into Cognitive Sandbox) → Monitored & Observed → Evolved (via CSLEMP) → Retired/Archived.
- **Cross-domain migration (RFC-0041 §8):** Running Agent → Checkpoint → Capability Validation → Federation Agreement Check → Target Domain Approval → Resume Execution. Trust negotiation: Domain A (Identity Proof) → Domain B (Capability Request) → Policy Evaluation → Federation Session Created.
- **Policy evolution loop (RFC-0040/[172]):** Observe → Identify Issue → Create Proposal → Analyze Impact → Vote → Approve → Version Policy → Deploy → Monitor — a self-evolving governance system.
- **Failure recovery (RFC-0042 §9):** checkpoint restoration, rollback to verified versions, sandbox restart, federation failover, quarantine; all recovery actions recorded as lifecycle events.

## Message #21 additions — language, tooling, observability, and package workflows (msg#21 [181]–[200])

- **CLS compilation & evaluation** ([181] §9, [182]): full pipeline Source (CLS) → … → CVM Execution (see Architecture); proposed evaluation phases Parse → Bind → Expand Dialects → Static Analysis → Capability Analysis → CIR Generation → Optimisation → Execution.
- **cog CLI toolchain** ([188]/[189] via RFC-0045): `cog build/test/run/fmt/lint/doc/publish/verify/replay`; package-management extensions proposed: [198] `cog new/init/add/remove/update/build/test/publish/install/verify/tree/doctor/clean`; [200] `cog new/init/add/remove/update/build/test/publish/install/search/lock/verify` (variants preserved — no canonical command set fixed in corpus).
- **Deterministic dependency resolution** ([197]/[199] §6): dependencies MUST reference immutable PackageID values (incl. content hash); version resolution MUST follow a defined deterministic algorithm; results MUST be recorded in the lockfile. Normative conflict/cycle/feature-flag behaviour still open ([200] §2).
- **Reproducible builds** ([197]/[199] §8): record exact compiler version/flags; capture build-environment hash where attestation available; same inputs MUST produce bit-identical CPCPF artifacts.
- **Observability sampling workflow** ([193]/[195] §4): Mandatory Replay Traces (MUST always record) · Optional Diagnostic Traces (MAY sample) · Statistical Telemetry (MAY statistically sample); sampling policy MUST be documented; mandatory traces never dropped.
- **Package lifecycle** (proposed, [200] §6): Created → Built → Verified → Packed → Published → Installed → Updated → Deprecated → Archived; each transition emits an event (integrates RFC-0018, aligns with CADP).
- **Workspace event logging** (proposed, [200] §4): add/remove dependency, update lockfile, publish/install package recorded in event log for replayable workspace history.

## Message #22 additions — package, FFI, and toolchain workflows (msg#22 [201]–[220])

- **CPMWS v1.2 normative flows ([201]):** deterministic dependency resolution algorithm (immutable PackageID; MUST detect/reject version conflicts, duplicate packages, cyclic dependencies; identical lockfiles for same manifest + registry state); standard CLI surface `cog new/init/add/remove/update/build/test/publish/install/search/lock/verify/tree/doctor/clean`; package lifecycle events Created → Built → Verified → Packed → Published → Installed → Updated → Deprecated → Archived (each transition emits an event to RFC-0018 event log).
- **CFFI call flow ([203]/[205]):** bindings validated at load time and enforced at runtime; capability verification before every foreign call; every call generates a trace entry (name/signature, inputs/outputs, capability context, effects, timestamp/provenance); replay uses recorded results for non-deterministic calls. Proposed FFI lifecycle ([206]): Load → Validate → Verify Signature → Resolve ABI → Capability Check → Execute → Trace → Replay → Unload.
- **CSTS canonical build pipeline ([209]/[211] §8):** Source → Parse → Semantic Analysis → CIR Generation → Optimisation → CISA Generation → Link → CPCPF Packaging → Verification → Deploy (implementations MUST support this pipeline or document equivalent behaviour).
- **Cognitive epochs (RFC-0050 §12, [219]):** Observe → Interpret → Retrieve Memory → Reason → Plan → Capability Resolution → Effect Execution → Observation Recording → Checkpoint Creation — the deterministic execution unit of cognitive programs.
- **CI/CD integration (CSTS §13):** non-interactive execution with deterministic exit codes, structured logs/reports, reproducible artefacts, machine-readable output; exit-code semantics (0–5 reserved meanings) proposed in [210]/[214].

## Message #23 additions — macro, verification, and remote-invocation workflows (msg#23 [221]–[240])

- **Macro expansion workflow (RFC-0051 §3, [227]):** Cognitive Source → Macro Expansion Phase → Expanded Cognitive AST → Semantic Analysis → CIR Generation → Optimization + Verification → CISA; every expansion MUST pass Macro Request → Capability Check → Policy Validation → Expansion → Trace Recording; hygienic expansion with compiler-controlled namespaces; CIR-level macros MAY operate directly on CIR (COIL expressible via CIR-level operations).
- **Macro CLI ([226]/[227]):** `cog macro list/expand/trace/verify/inspect`; proposed additions `cog macro debug/explain/provenance` ([228]).
- **Verification pipeline (RFC-0052 §9, ratified, [231]/[233]):** Source → Static Analysis → Unit Tests → Property Tests → Replay Verification → Capability Verification → Transformation Verification → Proof Verification → Deployment. **Testing CLI ([230]/[231]):** `cog test`, `cog test replay/property/capability`, `cog verify`, `cog verify proof/replay/policy/transformation`.
- **Remote invocation workflow (RFC-0053 §6, [239]):** state machine Created → Authenticated → Authorized → Scheduled → Executing → Completed (branches Failed/Cancelled/TimedOut); capability/policy enforcement before execution; deterministic replay uses recorded non-deterministic inputs; causal ordering per RFC-0002/0023.
- **Remote invocation CLI ([236]/[237]/[239]):** `cog invoke`, `cog agent discover`, `cog agent list`, `cog trace remote`, `cog replay remote`, `cog verify remote`.
- **Ratified application lifecycle ([224]):** Source → Package → Verify → Deploy → Execute → Observe → Replay. Full development lifecycle after RFC-0052 ([232]/[234]): Write/Author → Expand → Compile → Verify → Package → Deploy → Execute → Replay (& Validation).
