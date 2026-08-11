# Glossary

> Provenance: terms defined in the corpus (messages #2, #3, #5, #8). Each section below names its origin sub-messages. Definitions preserve source wording; terms not defined in the corpus are not listed.

> Terms as defined in corpus message #2. Definitions preserved from source wording; origin sub-message noted. Terms not defined in the corpus are not listed.

| Term | Definition (as stated in corpus) | Origin |
|---|---|---|
| **Red** | A next-generation, multi-paradigm programming language strongly inspired by Rebol; uniquely designed to be a "full-stack" language, handling everything from high-level scripting down to low-level systems programming. | [1] |
| **Homoiconic / homoiconicity** | Red treats code as data and data as code, which makes advanced metaprogramming very easy. | [1] |
| **Red/System** | A C-level, low-level system programming layer (dialect of Red); abstracts machine resources. | [1], [12] |
| **Parse** | A powerful Parsing Expression Grammar (PEG) engine (Red dialect). | [1] |
| **VID & Draw** | Dialects for rapid native GUI layout and 2D vector drawing. | [1] |
| **CLI (Command-Line Interface)** | A text-based interface used to operate software and operating systems; relies on a request-response pattern: you type a command, the shell executes it, prints the output, and terminates the process. Operates on a Stateless Request-Response cycle. | [1] |
| **Interactive Prompt** | A temporary state inside a CLI workflow where execution pauses to gather input from a human user; transitions a command from a static script to an active dialogue. | [1] |
| **REPL (Read-Eval-Print Loop)** | A continuous, stateful interactive programming environment. Instead of executing an external program and exiting, a REPL runs an engine that waits for you to type code snippets, evaluates them on the fly, and keeps the results in system memory. Operates on a Stateful, Persistent Environment; a live runtime sandbox, typically for a specific programming language. | [1] |
| **Agent runtime shell** | Extends the REPL concept from Read → Eval → Print → Loop to something closer to Observe → Reason → Plan → Act → Reflect → Loop; a natural interface for autonomous AI systems. Not a replacement for the CLI or REPL—its evolutionary successor. | [1], [2] |
| **ARS (Agent Runtime Shell)** | Persistent operating environment that manages cognition, memory, tools, safety, and execution; event-driven, not just input-driven. | [4] |
| **CogProcess (Cognitive Process)** | Resembles both a Unix process and a notebook session, but with persistent knowledge and reasoning. Fields: Identity, Goal, Context, Working Memory, Capabilities, Policies, Budget, Execution State, Reflection Log. | [8] |
| **CogOS (Cognitive Operating System)** | An operating system whose primary scheduling unit is **intent** rather than **process**; built around the abstraction **Intelligence** (vs Computation). Answers: "Which goal deserves attention next?" | [6], [8] |
| **CIR (Cognitive Intermediate Representation)** | IR of a Cognitive Red compiler; instead of lowering directly to instructions, the compiler first lowers to reasoning structures (Goal → Intent Graph → Task Graph → Capability Graph → Execution Graph → Machine Code). | [12] |
| **CVM (Cognitive Virtual Machine)** | Runtime that executes cognitive operations/semantic opcodes rather than conventional instructions; a reasoning engine rather than merely an execution engine. | [14] |
| **CISA (Cognitive Instruction Set Architecture)** | Architecture-independent semantic operations (Memory/Reasoning/Planning/Execution/Learning instruction groups) that different runtimes could implement; analogous to a CPU ISA. | [14] |
| **Cognitive ABI** | Common interfaces (Observe, Reason, Plan, Execute, Verify, Reflect, Learn, Checkpoint, Restore) exposed by every component; any reasoning engine, memory backend, or AI model implementing it could plug into the runtime without changing user code. Analogous to an OS ABI. | [16] |
| **Red/Cognition** | Proposed new higher layer extending Red upward toward autonomous intelligence; abstracts goals, reasoning, memory, planning, capabilities, and autonomous behaviour. Not simply an AI library or a new syntax — a proposal to elevate intent, knowledge, reasoning, and autonomous behaviour to first-class status. | [10], [12], [16] |
| **Intent contract** | Cognitive-language contract stating purpose, expected-output, quality threshold, deadline, budget; the runtime understands expectations. | [16] |
| **Cognitive effects** | Semantic effect system (observe!, remember!, modify!, communicate!, reason!, execute!, learn!) telling the compiler the behavioural impact of code. | [12] |
| **Policy types** | Type-system extension (safe?, trusted?, private?, external?, verified?, reversible?, idempotent?) letting the compiler reject unsafe plans before execution. | [12] |
| **Skill** | Reusable capability that may internally invoke dozens of traditional commands, APIs, or models (or call local code, external tools, or AI models). | [8], [10] |
| **Knowledge-flow analysis** | Cognitive analogue of data-flow analysis; every action can be traced back to supporting evidence. | [16] |
| **Provenance graph** | Lineage record of every cognitive object (Sensor → Observation → Reasoning Step → Decision → Action); enables explainability and auditing. | [16], [14] |
| **Attention (management)** | Resource absent from traditional operating systems; scheduler allocates reasoning effort according to attention (Importance, Urgency, Novelty, Risk → Attention Score) rather than simple arrival order. | [14] |
| **Cognitive garbage collection** | Runtime process that curates knowledge (compress, summarise, archive, forget) rather than simply freeing memory; mirrors human consolidation of experiences into long-term memory. | [14], [16] |
| **Native time travel** | Cognitive runtime replays reasoning (not just execution), so developers can inspect not only what happened but why each decision was made. | [16] |
| **Cognitive microkernel** | Design borrowing from microkernel OSes: most intelligence moved into modular replaceable services; kernel remains small. | [16] |
| **BDI-style semantics** | Semantics for cognitive constructs referenced by the agent system prompt as defined in the (absent) Red Deep Technical Specification; not defined within the corpus. | [19] |
| **Four-dimensional uncertainty model** | Uncertainty model referenced by the agent system prompt as defined in the (absent) Red Deep Technical Specification; not defined within the corpus. | [19] |
| **LibRed** | Red embedding API (with multi-language bindings), referenced in the agent system prompt knowledge base. | [19] |
| **Redbin** | Referenced in the agent system prompt knowledge base (concurrency/serialization context); not defined within the corpus. | [19] |

## Related pages

[Overview](Overview.md) · [Architecture](Architecture.md) · [References](References.md)

## Message #3 additions (sub-messages [21]–[40])

| Term | Definition (as stated in corpus) | Origin |
|---|---|---|
| **RC-000 Constitution** | The ratified (v1.0, 2026-07-29) governing framework of the Red/Cognition project: immutable principles, governance processes, structural requirements. Highest-law document; changeable only via constitutional amendment. | [33], [35] |
| **RC-100 Architecture Specification** | Normative specification (child of RC-000) defining the canonical nine-layer architecture, layer responsibilities, contracts, CEC-1, memory topology, capability model. History: v1.0 Draft ([37]) → v1.1 Candidate ([39]) → APPROVED FOR RATIFICATION ([40]) → **Ratified as Version 1.0** (record msg#5 [41], Date 2026-07-29). | [37], [39], [40], msg#5 [41] |
| **RC-200 Language Specification** | Normative language-level semantics of Red/Cognition (cognitive blocks/dialects, Goal/Belief/Plan semantics, effect system, capability-aware programming, type evolution, macros, migration). History: v1.0 Draft (msg#5 [43]) → v1.1 ([45]) → v1.2 ([47]) → **Ratified as Version 1.0** (record [49], Date 2026-07-29). | msg#5 [43]–[49] |
| **RC-300 Compiler Specification** | Normative compiler architecture: "compile cognition without becoming a cognitive engine"; dual IR pipeline (Red IR + Cognitive IR → Unified IR), CIR contract, DCP, determinism levels D0–D3, compilation security rules. v1.0 Draft ([51]) → v1.1 Candidate ([53]) → APPROVE FOR RATIFICATION ([54]); ratification record not yet in corpus. | msg#5 [51]–[54] |
| **RC-400 Runtime Specification** | Normative runtime architecture: "the runtime executes cognition without embedding intelligence"; Red Runtime + Cognitive Runtime components, scheduler, agent lifecycle, checkpoint/replay, capability enforcement, event system. v1.0 Draft; v1.1 amendments recommended ([56]). | msg#5 [55], [56] |
| **RC-500 Cognitive Runtime Specification** | Normative Layer-4 services: "intentional execution without embedding intelligence"; CEC-1 engine, memory hierarchy manager, capability enforcement, trace/checkpoint, agent lifecycle; provider-neutral. v1.0 Draft; v1.1 clarifications recommended ([58]). | msg#5 [57], [58] |
| **RC-600 Agent Runtime Shell Specification** | Normative Layer-5 surface: "primary execution surface for agents without embedding intelligence or decision-making"; interactive + autonomous modes, human-in-the-loop, observability. v1.0 Draft; v1.1 additions recommended ([60]). | msg#5 [59], [60] |
| **RC-200…RC-900** | The remaining specification family: Language, Compiler, Runtime, Cognitive Runtime, Agent Runtime Shell, Cognitive VM, CogOS, Governance Manual. Not yet drafted in corpus. | [28], [30], [35] |
| **Reference Model (nine layers)** | Layer 0 Hardware · 1 Operating System · 2 Red/System · 3 Red Runtime · 4 Cognitive Runtime · 5 Agent Runtime Shell · 6 Cognitive Virtual Machine · 7 Cognitive Operating System · 8 Distributed Agent Network. Dependency direction flows upward only. | [28] §1, [29] §5, RC-000 §4, RC-100 §4 |
| **CEC (Cognitive Execution Cycle)** | Canonical execution lifecycle. CEC-1: Observe → Interpret → Retrieve Memory → Reason → Plan → Act → Verify → Reflect → Checkpoint → Loop. Does not replace REPL; CEC-2/CEC-3 reserved. | [38] §9, RC-100 §6 |
| **LICM (Layer Interface Contract Model)** | Every layer MUST define Public Interface, Events, Data Types, Error Model, Security Boundary, Version Contract; any layer replaceable without modifying adjacent layers. | [38] Amendment A, RC-100 v1.1 §15 |
| **Cognitive Neutrality Principle** | "The Cognitive Runtime MUST NOT depend on any single intelligence provider." | [38] §7, RC-100 v1.1 §16 |
| **Constitutional Tests** | Eight questions every proposal must pass before advancing (simplicity, syntax, dialect, compatibility, conceptual burden, explainability, determinism, architecture fit). | [24], RC-000 §3.3 |
| **Architectural Invariants** | Seven never-violated properties (homoiconicity, blocks, dialects, Red/System foundation, extension-not-replacement, native compilation & zero-dependency, inspectable/explainable/replayable cognition). | [24], RC-000 §3.2 |
| **Language Evolution Ladder** | Research → Concept → RFC Draft → Prototype → Experimental → Preview → Stable → Core Language; no feature may skip stages. | [24], RC-000 §5.1 |
| **ADR (Architecture Decision Record)** | Record of a significant design choice containing context, decision, alternatives considered, consequences, migration strategy. | [22], RC-000 §5.3 |
| **Stability Classes** | Draft • Experimental • Provisional • Stable • Legacy • Deprecated • Removed — every feature must carry one. | [28] §3, RC-000 §6.2 |
| **Conformance Levels** | L0 Red/System … L5 Distributed Cognitive Platform; enables lightweight embedded implementations within a common standard. | [26] §8, RC-000 §6.5 |
| **Release Model** | Nightly → Experimental → Beta → Stable → LTS. | [26] §7, RC-000 §6.4 |
| **Compatibility Levels** | Source, Behavioural, Binary, Cognitive — every RFC must declare which are affected. | [28] §7, RC-000 §6.3 |
| **Governance Principle** | "The burden of proof lies with change, not stability." | [30], RC-000 §5.5 |
| **Specification Authority** | "Specifications define behaviour. Implementations define mechanisms." No implementation detail becomes normative unless incorporated into a specification or RFC. | [30], RC-000 §11 |
| **Preservation of Identity** | "Red/Cognition shall evolve Red by extending its abstractions rather than changing its identity." | [30], RC-000 §3.4 |
| **Manifesto** | Five "We believe" statements closing the Constitution (intent, inspectable reasoning, cognition in the architecture, local-first intelligence, Red's philosophy as foundation). | [29], [31], [33] |
| **Multi-Agent Governance Model** | Eight specialised agent roles (Chief Architect, Compiler Engineer, Runtime Engineer, Language Designer, Cognitive Architect, Verification Agent, Documentation Agent, Research Agent). | [24], RC-000 §5.4 |
| **Normative Vocabulary** | MUST / MUST NOT / SHOULD / SHOULD NOT / MAY (RFC 2119-inspired). | [24], RC-000 §7.3 |
| **Canonical Identity statement** | "Red/Cognition is not an AI framework built on top of a programming language. It is a cognitive programming extension of a homoiconic, dialect-oriented, full-stack language architecture." | [34] |
| **CIR (Cognitive Intermediate Representation)** | Future RC-300/RC-700 dependency: Red Source → Red AST → Semantic IR → Cognitive IR → Execution Backend; nodes for Intent, Goal, Belief, Plan, Action, Effect, Capability, Memory Access. | [38] §6 (extends CIR concept from msg #2 [12]) |

## Message #4 additions (sub-messages [41]–[60])

| Term | Definition (as stated in corpus) | Origin |
|---|---|---|
| **CEC / CEC-1** | Cognitive Execution Cycle — canonical: Observe → Interpret → Retrieve Memory → Reason → Plan → Act → Verify → Reflect → Checkpoint → Loop; ratified as architectural component. | [41], RC-100 |
| **Cognitive Block Evaluation Contract** | Cognitive block MUST remain valid Red data, be inspectable without execution, require explicit cognitive evaluation, preserve source representation; SHALL have no external effect outside an approved evaluation boundary. | RC-200 §5.1 ([47]) |
| **Effect Classes** | pure! · internal! · external! · capability! (initial). | RC-200 §8.1 ([45]+) |
| **Cognitive Type Evolution** | Dialect → Structured Value → Native Type (optional). | RC-200 §10.1 |
| **DCP (Dialect Compiler Protocol)** | Parser, Validator, Lowering Rules, Type Rules, Effect Rules, Metadata Generator per cognitive dialect. | RC-300 v1.1 §8 |
| **Unified IR** | Representation connecting Red IR and Cognitive IR to backends; represents interactions between computation, cognitive operations, effects, capabilities, checkpoints without merging language semantics. | [52] §4, RC-300 v1.1 §6 |
| **Compiler determinism levels** | D0–D3 (best effort / reproducible / bit-identical / verified). | RC-300 v1.1 §7 |
| **Replay equivalence levels** | R0 trace available / R1 state restoration / R2 observable behaviour replay / R3 bit-level deterministic replay. | [56] |
| **Autonomy levels** | A0 Manual / A1 Assisted / A2 Supervised / A3 Autonomous / A4 Distributed Autonomous. | [60] |
| **State visibility levels** | Public / Operator / Debug / Internal. | [60] |
| **Agent Session** | Interaction context between operator/event source/scheduler and an agent (Session {Identity, Agent Reference, Execution Mode, Interaction History, Active Capabilities, Trace Context, Checkpoint Reference}). | [60] |
| **CognitiveRuntimeAPI** | execute-cycle(), store-memory(), retrieve-memory(), request-capability(), emit-trace(), create-checkpoint(), restore-checkpoint(). | [58] |
| **Runtime Event Contract** | Event {id, timestamp, source, capability-context, payload, provenance}. | [56] |
| **Agent State Model** | Agent State = {Identity, Goals, Beliefs, Plans, Memory References, Capabilities, Execution Trace, Checkpoint State}. | [58] |

## Message #8 additions (sub-messages [61]–[80])

| Term | Definition (as stated in corpus) | Origin |
|---|---|---|
| **CISA (concrete)** | Cognitive Instruction Set Architecture of RC-700: OBSERVE, RECALL, INFER, PLAN, EXECUTE, VERIFY, REFLECT, CHECKPOINT, RESTORE, EXPLAIN; versioned (CISA-1.0 core + optional + experimental). | [61], [62] |
| **Cognitive Process** | CogOS execution context {Identity, Agent Reference, CVM Instance, Goals, Memory Context, Active Capabilities, Execution State, Trace Context}; fundamental CogOS unit (ADR-0012). | [63], [64] |
| **Cognitive Value Base Contract** | cognitive-value {cognitive-meta{id,created,modified,provenance,version}, type, schema-version} — ratified for all cognitive values. | [71], [72] |
| **Effect ID** | Globally unique, stable-through-serialization/replay/checkpoint/distributed-propagation identifier for effect!. | [74], [75] |
| **Effect Dependency Graph** | DAG of effect precedence; cycles rejected; canonical execution model for Cognitive IR and CVM scheduling. | [75], [76] |
| **Temporal vs Causal Order** | Temporal = chronological occurrence; Causal = dependency relation; independent dimensions; causal preserved under parallelization. | [74], [75], [76] |
| **Replay Equivalence Principle** | Replay correctness = observable behavioural equivalence, not identical internal scheduling (ADR-0008 per [76]). | [76] |
| **BeliefID** | Stable identity of a belief across revisions; versions increment, history addressable. | [78], [79] |
| **Belief Revision Graph** | Directed graph of belief revisions; alternative paths before reconciliation; deterministic replay of any valid path. | [79], [80] |
| **revision-cause** | observation / inference / external-input / effect / manual (extensible via documented implementation-defined causes). | [78], [79], [80] |
| **Scheduler Classes** | S0 Cooperative / S1 Priority Based / S2 Deadline Aware / S3 Adaptive Cognitive Scheduling. | [64] |
| **Memory/Security Domains** | Memory: Private/Shared/System. Security: Kernel/Agent/Capability/Network. | [64] |
| **RC-1000 Formal Semantics** | Proposed future spec: cognitive state transition system, effect calculus, capability safety proofs, replay equivalence, deterministic execution guarantees. | [66] |

## Message #10 additions (sub-messages [81]–[100])

| Term | Definition (as stated in corpus) | Origin |
|---|---|---|
| **GoalID** | Stable identifier of a goal; constant across revisions and state transitions; versions increment preserving it. | [84], [85] |
| **PlanID** | Stable identifier of a plan; constant across revisions; historical versions addressable. | [87] |
| **CapabilityID** | Stable identifier of a capability; constant across lifecycle incl. serialization/checkpointing/restoration/replay. | [90], [91], [93] |
| **SkillID / SkillInvocationID** | Stable skill definition identity (versioned) vs per-execution invocation identity. | [95], [96], [97] |
| **CapabilityTrace** | {CapabilityID, AgentID, EffectID, Timestamp, Decision: Allow\|Deny} — trace entry per capability usage. | [90], [91], [93] |
| **SkillInvocation** | {SkillInvocationID, SkillID, PlanID, GoalID, Timestamp, Inputs, Outputs, Effects, CapabilitiesUsed}. | [97] |
| **goal-result fields** | satisfied-by: [EffectID], supporting-beliefs: [BeliefID], completion-time — why satisfaction occurred. | [84], [85] |
| **MemorySnapshot** | {SnapshotID, Timestamp, WorkingMemory, SemanticVersion, ProceduralVersion, EpisodicPosition} — bridge to checkpoint RFC (recommended). | [100] |
| **MemoryTrace** | {MemoryID, Tier, Operation, AgentID, Timestamp, Provenance} (recommended). | [100] |
| **SkillTrace** | {SkillInvocationID, SkillID, PlanID, GoalID, StartTime, EndTime, Status, EffectsProduced, CapabilitiesUsed} (recommended v1.2). | [98] |
| **Skill purity classes** | pure! / internal! / capability! / external! — aligned with RFC-0002 effect classes. | [96], [97] |
| **Goal ownership classes** | Personal / Shared / System goals. | [84], [85] |
| **Capability type registry** | Example standard types (filesystem.read, filesystem.write, network.connect, …) — implementation-defined for now. | [94] |

## Message #12 additions (sub-messages [101]–[120])

| Term | Definition (as stated in corpus) | Origin |
|---|---|---|
| **AgentID** | Stable identity of an agent; constant throughout the agent's lifetime. | [101] |
| **AgentState** | { Identity, Goals, Beliefs, Plans, Memory References, Active Capabilities, Execution Context, Trace History, Checkpoint References }. | [101] |
| **AgentTrace** | { AgentID, Timestamp, PreviousState, NewState, GoalID, PlanID, EffectID } (recommended). | [102] |
| **Mailbox** | { MessageID, Sender, Receiver, Timestamp } — basis for future Inter-Agent Communication RFC (recommended). | [102] |
| **CheckpointID** | Stable identity of a checkpoint; immutable snapshot semantics recommended ("Any modification or re-capture MUST create a new CheckpointID"). | [103], [104] |
| **CheckpointTrace** | { CheckpointID, AgentID, Timestamp, TracePosition, Action: Create\|Restore } (recommended). | [104] |
| **SchedulerID** | Stable scheduler identity; policy/metadata changes increment version preserving it. | [107], [109], [110] |
| **ScheduleDecision** | First-class scheduling trace record { DecisionID, Timestamp, SchedulerID, AgentID, PlanID, RunnableSet, SelectedProcess, Reason }. | [109] |
| **WaitingReason** | Goal \| Plan \| Effect \| Capability \| Resource \| Timer \| ExternalEvent \| ImplementationDefined. | [108], [109] |
| **Deterministic Tie-Breaking** | Equal priorities resolved by: earlier deadline → older enqueue timestamp → lower AgentID → lower PlanID. | [109] |
| **CVMID** | Stable identity of a CVM instance; implementation/configuration changes increment version. | [113], [115] |
| **ExecutionContext** | { InstructionPointer, OperandStack, RegisterSet, WorkingMemoryReference, CurrentAgent, CurrentPlan, CurrentGoal, CapabilityContext, TraceContext } — serializable, checkpointable cognitive process state. | [112], [113], [115] |
| **Instruction Transaction** | Begin → Validate → Capability Check → Execute → Generate Effects → Commit → Trace; no partial effects escape a failed instruction. | [114], [115], [120] |
| **InstructionTrace** | { TraceID, Timestamp, CVMID, AgentID, InstructionPointer, InstructionID, Opcode, Operands, Result, Effects }. | [115] |
| **InstructionID / EncodingVersion** | Stable per-instruction identity and CISA revision marker enabling cross-version compatibility and replay. | [114], [118], [119] |
| **CISA register classes** | G (16, general, mutable) · M (8, memory refs, reference-only) · C (8, capability context, runtime-controlled) · T (8, trace, write-only by trace engine) · S (4, scheduler-controlled). | [119], [120] |
| **ExternalInputRecord** | { InputID, Source, Timestamp, Value, TraceID } — deterministic replay of external inputs (recommended). | [114] |
| **CognitiveException** | InvalidInstruction, CapabilityDenied, BeliefConflict, GoalViolation, PlanFailure, MemoryFault, ExternalFailure (recommended future model). | [118] |
| **Scheduler/CVM ownership rule** | Scheduler owns WHEN execution happens; CVM owns HOW; CVM MUST NOT independently schedule cognitive processes. | [114], [115], [116] |

## Message #14 additions (sub-messages [121]–[140])

| Term | Definition (as stated in corpus) | Origin |
|---|---|---|
| **CISA binary format** | Deterministic versioned binary encoding of CISA instructions: Magic ("CISA1") + Encoding Version + InstructionID + Opcode + Flags + Operand Count + Operand Types + Operands + Capability ID + Effect Class; little-endian, no padding, canonical ordering, no implicit coercion. | [121] |
| **CISA Program Container** | Proposed program-level wrapper: Program Header { ProgramID, CISA Version, Required CVM Version, Instruction Count, Entry Point, Metadata Offset } + instructions + metadata + debug info. | [122] |
| **CognitiveException** | Eight-category exception hierarchy: ValidationError, CapabilityError, MemoryError, SkillError, PlanError, GoalError, RuntimeError, ExternalError. | [123] |
| **ExceptionTrace** | { TraceID, Timestamp, CVMID, AgentID, InstructionID, ExceptionCategory, ErrorCode, Message, CapabilityContext, RecoveryAction }. | [123] |
| **Cognitive Runtime (CRT)** | Central execution environment integrating CVM, scheduler, memory, capability enforcement, trace engine, exception handling, agent lifecycle into a cohesive runtime substrate; deterministic substrate, not an intelligence engine. | [125] |
| **Runtime tick** | Main runtime cycle: collect runnable → schedule → execute CISA → effects → capability validation → memory update → trace append → checkpoint boundary → continue. | [126] |
| **RuntimeEvent** | Unified runtime event schema { EventID, Timestamp, SourceService, EventType, AgentID, TraceID, CorrelationID, Payload, Provenance } (+ recommended ParentEvents, SequenceNumber, SchemaVersion, Hash). | [129], [130] |
| **Cognitive Flight Recorder** | The RFC-0018 event log conceived as an aircraft-black-box analog: answers "What happened, why did it happen, and can we reproduce it?". | [130] |
| **Replay modes** | L0 Trace Replay (inspect events) · L1 State Replay (Checkpoint + Events = Runtime State) · L2 Execution Replay (CISA + Scheduler Decisions + External Inputs = Same Effects). | [130] |
| **CogOS** | Cognitive Operating System: system-level layer managing multiple cognitive processes/agents, system-wide policies, shared resources, distributed foundation; "governance and execution environment", not an AI engine. | [131], [132] |
| **NodeID** | Stable distributed location identity of a participating node; Node { NodeID, Address, Capabilities, SupportedCISARevision, Version }; completes identity continuity. | [133], [134] |
| **CNP (Cognitive Network Protocol)** | Communication/discovery/authentication/routing layer for distributed cognitive execution; "cognitive equivalent of TCP/IP"; messages are causal execution artifacts. | [135], [136] |
| **CNPMessage** | { MessageID, Timestamp, SourceNodeID, TargetNodeID, MessageType, Payload, CapabilityToken, TraceReference, Signature }. | [135] |
| **Capability federation** | Cross-node capability enforcement: delegation, revocation propagation, scope verification; "a capability cannot become weaker when crossing a node boundary". | [133], [134] |
| **Agent migration** | Agent movement between nodes preserving AgentID, state, capabilities, execution context; recorded as system-level effect; "AgentID remains unchanged; only execution location changes". | [133], [136] |
| **Trust domain** | Organizational boundary with shared policy & capability authority, common event log visibility, coordinated checkpoint/recovery; cross-domain operations require capability delegation. | [137] |
| **Attestation** | Verifiable proofs presented by nodes/agents (software versions, CISA revision, RFC compliance, hardware security e.g. TPM/secure enclaves); recorded in event log when used for authorization. | [137] |
| **Local Truth vs Distributed Agreement** | State known by one runtime vs state accepted by the cognitive network through consensus; prevents divergent cognitive realities. | [140] |
| **ConsensusEvent** | Proposed agreement primitive { ConsensusID, EventSet, Participants, Decision, LogicalTimestamp, Proof }. | [140] |

## Message #16 additions (sub-messages [141]–[160])

| Term | Definition (as stated in corpus) | Origin |
|---|---|---|
| **ResourceQuota** | { AgentID, ExecutionBudget, MemoryLimit, CapabilityBudget, EffectBudget, StorageQuota, NetworkQuota }; enforced by CogOS, respected during scheduling and execution. | [141] |
| **ResourceError** | Exception hierarchy: ExecutionBudgetExceeded, MemoryQuotaExceeded, CapabilityBudgetExceeded, EffectBudgetExceeded, NetworkQuotaExceeded. | [142] |
| **CRT (Cognitive Resource Token)** | Proposed resource accounting unit for instruction execution, memory operations, capability actions, distributed computation. | [142] |
| **CSPL** | Cognitive Security Policy Language: declarative, deterministic language for rules governing capability usage, resource allocation, trust relationships, effect authorization; Policy { PolicyID, Scope, Rules, Priority, Version }; Rule { Subject, Action, Resource, Condition, Effect: Allow\|Deny }; default Deny. | [143] |
| **PolicyError** | UnauthorizedAction, PolicyConflict, InvalidPolicy, MissingContext, TrustViolation. | [144] |
| **Cognitive reference monitor** | The RFC-0024/0025 security chain (Identity → Trust → Policy → Capability → Resource Limits → Execution) characterized as "closer to a cognitive reference monitor than traditional application security". | [144] |
| **AcceleratorContext** | { AcceleratorID, Type, CapabilityContext, AttestationState, ExecutionProfile, ResourceBudget } — accelerators as managed cognitive resources. | [146] |
| **HardwareExecutionEvent** | { EventID, InstructionID, AcceleratorID, ExecutionMode, InputHash, OutputHash, Attestation, Timestamp } — hardware provenance in the event log. | [146] |
| **CHAL** | Cognitive Hardware Abstraction Layer — proposed RFC-0026.1: accelerator discovery, device drivers, instruction mapping, memory transfer, secure execution, performance counters. | [146] |
| **CIR** | Cognitive Intermediate Representation: central, implementation-independent compiler representation; CIRModule with Identity, CognitiveTypes, five graphs (DAGs), operations, constraints; "semantic bridge between cognitive intent and executable cognition". | [149], [150] |
| **CIROperation** | { OperationID, Type, Inputs, Outputs, Preconditions, Postconditions, RequiredCapabilities, Effects, MemoryAccess, ResourceEstimate, Provenance }. | [150] |
| **CIR-SER** | Cognitive IR Serialization Format: deterministic, versioned, portable representation of CIR; Magic "CIR1"; "cognitive equivalent of ELF/WASM/object serialization formats". | [151], [152] |
| **CIRModuleArtifact** | Header + SemanticLayer + ExecutionLayer + MetadataLayer + IntegrityLayer — serialized cognitive module. | [152] |
| **OptimizationPass** | { InputCIR, Preconditions, Transformation, OutputCIR, SemanticGuarantees, CapabilityImpact, TraceImpact, ReplayGuarantees }; six categories; legality rules preserve effect ordering/goal semantics/capabilities/replay. | [153], [154] |
| **COIL** | Cognitive Optimization Intermediate Language: dedicated transformation language (MergeNodes, SplitNode, ReorderEdges, InlineOperation, HoistCapability, EliminateDeadOperation, StrengthenConstraint, WeakenConstraint, RecordTransformation, AttachProvenance) with proof obligations; "compiler proof layer". | [155], [156] |
| **COC (Cognitive Optimization Certificate)** | { CertificateID, OriginalCIRHash, OptimizedCIRHash, COILProgram, VerificationResults, CapabilityImpact, EffectImpact, TraceImpact, CompilerVersion }. | [156] |
| **COVF** | Cognitive Optimization Verification Framework: verification condition generation, proof representation (OptimizationProof), certificate validation, theorem prover integration (Lean 4, Coq, Isabelle/HOL, Z3, CVC5). | [157] |
| **TCB (Trusted Computing Base)** | { CIR Validator, COIL Interpreter, Proof Checker, Theorem Kernel }; "Trust the verifier, not the optimizer." | [158] |
| **CPCPF** | Cognitive Proof-Carrying Program Format: deployable artifact bundling CISA binary + CIR + optimization history + proofs + capability manifest + trace metadata + integrity; "proof-carrying cognitive software". | [159], [160] |
| **CapabilityManifest** | { RequiredCapabilities, AllowedEffects, MemoryAccess, ResourceRequirements } — declared by CPCPF artifacts; CogOS can reject deployment before execution. | [160] |
| **CPR-TDP** | Proposed RFC-0034 Cognitive Package Registry and Trust Distribution Protocol: publishing, discovery, verification, distribution of CPCPF artifacts. | [160] |

## Message #18 additions (sub-messages [161]–[180])

| Term | Definition (as stated in corpus) | Origin |
|---|---|---|
| **CPR-TDP** | Cognitive Package Registry and Trust Distribution Protocol: ecosystem infrastructure for publishing, discovering, distributing, verifying, versioning, revoking, managing CPCPF artifacts; "trust by verification". | [162], [163] |
| **CSEIM** | Cognitive Sandbox and Execution Isolation Model: isolation architecture, sandbox semantics, resource boundaries, effect mediation, capability enforcement, deterministic execution guarantees. | [164] |
| **CBR-SCP** | Cognitive Build Reproducibility and Supply Chain Protocol: deterministic, auditable, tamper-resistant builds; end-to-end supply chain source→verified execution. | [165] |
| **CSLEMP** | Cognitive Software Lifecycle and Evolution Management Protocol: deployment, monitoring, updating, migration, version evolution, compatibility, retirement. | [166] |
| **CMAEP** | Cognitive Marketplace and Agent Economy Protocol: discovery, publishing, licensing, reputation, incentives, economic coordination. | [167] |
| **Cognitive Credit** | A system token representing computational or cognitive resource value (CMAEP primitive). | [167] |
| **CIEOP** | Cognitive Identity Economy and Ownership Protocol: ownership, creator attribution, derivative lineage, capability inheritance, IP lineage. | [169] |
| **CGCDP** | Cognitive Governance and Collective Decision Protocol: multi-agent organizations, voting, delegation, autonomous governance, collective policy evolution. | [171] |
| **CIFP** | Cognitive Interoperability and Federation Protocol: communication, capability exchange, trust negotiation, coordinated execution across CogOS instances/domains. | [173] |
| **CADP** | Cognitive Autonomous Deployment Protocol: end-to-end operational lifecycle from creation to retirement; ratified per [179]. | [177], [179] |
| **Trust levels T0–T5** | T0 Unverified · T1 Signature verified · T2 CPCPF validated · T3 Optimization proofs verified · T4 Formally verified · T5 Hardware-attested. | [162], [163] |
| **Cognitive Domain** | An independent trust and governance boundary (CogOS instance or organization) with stable DomainID. | [173] |
| **Federation Agreement** | Formal versioned contract defining interaction rules between domains (allowed interactions, trust requirements, resource rules, dispute resolution, termination). | [173] |
| **Cognitive Constitution** | Organization-level programmable constitution { IdentityRules, OwnershipRules, CapabilityRules, EconomicRules, GovernanceRules, EvolutionRules } (RFC-0040 concept). | [172] |
| **Effect Gateway** | Sandbox component through which all external effects MUST pass (capability check + policy evaluation). | [164] |
| **CLS (RFC-0043)** | Cognitive Language Specification — programmer-facing syntax, lexical structure, grammar, type system, semantic model, and cognitive constructs; extends Red through structured blocks and dialects; maps onto CIR (RFC-0028) and CISA (RFC-0013). Proposed in [178]/[180]; **drafted v1.0** in [181] (Parent: RFC-0028). | [178], [180], [181] |
| **CSL (RFC-0044)** | Cognitive Standard Library — canonical cognitive types, operations, dialects, modules, and utilities every conforming implementation MUST/SHOULD provide; mandatory `cognition.*` modules; library profiles Core/Runtime/Distributed/Full. v1.0 [183] → v1.1 Candidate [185]. | [183], [185] |
| **CTDX (RFC-0045)** | Cognitive Tooling and Developer Experience — LSP, debugger, profiler, formatter/linter, testing framework, documentation generator, cog CLI, workspace model, CDP, visualisation standards, AI-assisted development, conformance test suite. v1.0 [187] → v1.1 Candidate [189]. | [187], [189] |
| **CODP (RFC-0046)** | Cognitive Observability and Diagnostics Protocol — runtime tracing, metrics, distributed diagnostics, deterministic replay infrastructure; conformance levels Basic/Standard/Full/Forensic; sampling policy; security & privacy; metric taxonomy; ObservabilityEvent. v1.0 [191] → v1.1 [193] → v1.2 [195]; **Ratified** per [196]. | [191], [193], [195], [196] |
| **CPMWS (RFC-0047)** | Cognitive Package Manager and Workspace Specification — developer-facing package management, workspace layout, deterministic dependency resolution, lockfiles, build reproducibility. v1.0 [197] → v1.1 Candidate [199]. | [197], [199] |
| **cog** | Standard command-line developer toolchain (RFC-0045 §4): `cog build/test/run/fmt/lint/doc/publish/verify/replay`; package-management extensions proposed in [198]/[200]. | [189], [198], [200] |
| **Workspace (CPMWS)** | Directory tree with cog.toml manifest, immutable cog.lock lockfile, packages/, tests/, docs/, examples/, build/; profiles Single/Workspace/Enterprise/Federated. | [197], [199] |
| **Lockfile (cog.lock)** | Immutable, machine-readable, human-auditable record of exact package identities/content hashes, resolved dependency graph, capability/resource declarations, reproducibility metadata, workspace hash, optional signature. | [197], [199] |
| **Library Profiles (CSL)** | Core (`cognition.core`, goal, belief, capability) · Runtime (+scheduler, checkpoint, trace) · Distributed (+federation, network, registry) · Full (all standard modules); implementations MUST declare supported profile(s). | [185] |
| **Observability Conformance Levels** | Basic (metrics only) · Standard (metrics + traces) · Full (+ replay + distributed diagnostics) · Forensic (complete deterministic event capture); implementations MUST declare supported level(s). | [193], [195] |
| **Mandatory Replay Traces** | Events required for deterministic replay (instruction execution, effect commitment, capability decisions, checkpoint creation) — MUST always be recorded; never dropped. | [193], [195] |
| **Standard Metric Taxonomy** | Canonical CODP namespaces: cognition.agent.*, cognition.scheduler.*, cognition.memory.*, cognition.effect.*, cognition.runtime.*, cognition.compiler.* | [193], [195] |
| **CDP (proposed)** | Cognitive Debug Protocol — breakpoint management, execution control, event streaming, checkpoint inspection, distributed debugging, replay debugging; proposed as future RFC alongside/beyond LSP. | [188], [189], [196] |
| **CCTS (proposed)** | Cognitive Conformance Test Suite — certification tests for language implementations, compilers, runtimes, registries, federation, deployment; assigned RFC-0047 in [182] roadmap but RFC-0048 in [196] roadmap (conflict C-11). | [182], [196] |
| **CFFI (proposed)** | Cognitive Foreign Function Interface — interoperability with Red, Rebol, C, Rust, WebAssembly, Python, JavaScript, external cognitive runtimes ([182] roadmap; RFC-0048). | [182] |
| **CTEF (proposed)** | Cognitive Trace Exchange Format — proposed RFC-0050 per [196] roadmap (trace export/interchange). | [196] |
| **OperationDescriptor (proposed)** | CSL operation metadata { Name, Purity, EffectClass, RequiredCapabilities, SchedulerRequirements, ReplayBehaviour } ([186] recommendation). | [186] |
| **ToolCapabilities (proposed)** | Tool capability discovery structure { LSP, Debugger, ReplayDebugger, Profiler, Formatter, AICompletion, ProofAssistant } ([190] recommendation). | [190] |
| **WorkspaceManifest / PackageManifest (proposed)** | Normative manifest schemas proposed in [200]: WorkspaceManifest { WorkspaceID, Name, Version, Members[], Dependencies[], Policies, CompilerProfile, RuntimeProfile, DeploymentTargets[], Registries[] }; PackageManifest { PackageID, Name, Version, Authors, License, Dependencies[], Capabilities[], Resources, Build, Tests, Metadata }. | [200] |
| **Package Lifecycle (proposed)** | Created → Built → Verified → Packed → Published → Installed → Updated → Deprecated → Archived; each transition emits an event ([200] recommendation). | [200] |
| **CFFI (RFC-0048)** | Cognitive Foreign Function Interface — safe, deterministic, traceable interoperability with foreign code (Red, Rebol, C, Rust, WASM, Python, JavaScript) and external cognitive runtimes; capability-mediated, replay-equivalent. v1.0 [203] → v1.1 Candidate [205]. | [203], [205] |
| **CSTS (RFC-0049)** | Cognitive Standard Toolchain Specification — canonical reference toolchain (compiler, linker, package manager, debugger, profiler, formatter, linter, docs generator, deployment tool); profiles Minimal/Developer/Professional/Enterprise/Full. v1.2 **Ratified** per [215]. | [207], [211], [215] |
| **RFC-0050 (capstone)** | Red/Cognition v1.0 Architecture and Conformance Specification — freezes the first-generation architecture; conformance model, implementation profiles, cognitive epochs; "architectural constitution" of v1.x. v1.0 [217] → v1.1 Candidate [219]. | [216], [217], [219] |
| **Foreign Module** | A library or module written in a foreign language; exposes ForeignModule manifest { Name, Version, ABI, Language, Capabilities, Effects, Determinism, Signature } packaged into CPCPF. | [203], [205] |
| **Cognitive Foreign Binding** | Typed interface declaration mapping cognitive types to foreign types; declares signature, types, effects, capabilities, determinism; validated at load time, enforced at runtime. | [203], [205] |
| **FFI Determinism Classes** | Pure · Deterministic · ReplayRecorded · Effectful · External — foreign functions MUST be classified; ReplayRecorded results are recorded and reused during replay. | [205] |
| **Memory Ownership Models (FFI)** | Borrowed · Shared · Copied · Owned · Immutable · Pinned — objects crossing the FFI boundary MUST declare an ownership model. | [205] |
| **FFI Sandboxing Levels** | Trusted · Sandboxed · WASM · Remote · Verified (proof-carrying module) — isolation levels for foreign code execution (aligns with RFC-0035). | [204], [205] |
| **ToolchainManifest** | Machine-readable description of the installed toolchain (components + capabilities) enabling IDE/automation discovery (CSTS §5–6); extended schema proposed in [212]/[214]. | [209], [211], [212] |
| **Diagnostic (CSTS)** | Structured toolchain diagnostic { Severity, Code, Message, SourceLocation, Capability, Effect, SuggestedFix } emitted in a standard machine-readable schema. | [208], [209] |
| **Canonical Build Pipeline** | CSTS normative pipeline: Source → Parse → Semantic Analysis → CIR Generation → Optimisation → CISA Generation → Link → CPCPF Packaging → Verification → Deploy. | [209], [211] |
| **ConformanceManifest** | Machine-readable declaration of an implementation's conformance level and supported RFCs (RFC-0050 §5; final schema proposed [220]). | [219], [220] |
| **Cognitive Epoch** | The deterministic execution interval of a cognitive program: Observe → Interpret → Retrieve Memory → Reason → Plan → Capability Resolution → Effect Execution → Observation Recording → Checkpoint Creation (RFC-0050 §12; definition proposed [220]). | [219], [220] |
| **Implementation Profiles (RFC-0050)** | Embedded Cognitive Runtime · Developer Platform · Server Cognitive Node · Distributed Cognitive Federation · Full CogOS Platform. | [216], [217], [219] |
| **Conformance Levels (RFC-0050)** | Core (language/type system/capabilities/scheduler/basic toolchain) · Extended (+distributed execution, federation, proof verification, autonomous deployment) · Full (+complete CogOS, hardware acceleration, governance, marketplace). | [216], [217], [219] |
| **CILSP (proposed)** | Cognitive IDE & Language Server Protocol Extensions — proposed RFC-0050 in [202] roadmap; number reassigned to the capstone spec per [215]/[216] (conflict C-11). | [202] |
| **CTVF (proposed)** | Cognitive Testing & Verification Framework — proposed RFC-0051 in [202] roadmap; [215] roadmap assigns 0052 to Testing and Verification (C-11). | [202], [215] |
| **CMMS (RFC-0051)** | Cognitive Macro and Metaprogramming System — hygienic, typed, capability-controlled, verifiable program transformation (syntax/semantic/cognitive macros, CIR-level macros, MacroExpansionRecord provenance). v1.0 Draft [227]. | [226], [227] |
| **CTVF (RFC-0052)** | Cognitive Testing and Verification Framework — unit/integration, property-based, replay-based, transformation, and security/policy verification; cognitive coverage; profiles Basic/Developer/Professional/Verified/Full. v1.2 **Ratified** per [235]. | [229], [233], [235] |
| **CRAIP (RFC-0053)** | Cognitive Remote Agent Invocation Protocol — deterministic, capability-aware remote agent invocation across process/machine/organization boundaries; invocation state machine; transport-independent; version negotiation + streaming semantics in v1.2. v1.2 **Ratified** per [244]/[245]/[247]. | [236], [241], [244], [247] |
| **Cognitive Epoch (ratified)** | Smallest deterministic execution interval: Observe → Interpret → Retrieve Memory → Reason → Plan → Capability Resolution → Effect Execution → Observation Recording → Checkpoint Creation (RFC-0050 §12; ratified primitive [224]). | [221], [224] |
| **Cognitive Application (ratified)** | A deployable CPCPF artifact containing cognitive programs, capabilities, policies, dependencies, and runtime requirements (RFC-0050 §16). | [221], [224] |
| **Architecture Governance Rule** | RFC-0050 §17 (ratified): future RFCs MUST NOT violate the architectural principles, security boundaries, execution model, or conformance model; v1.x architecture frozen at constitutional level. | [221], [224] |
| **MacroExpansionRecord** | Macro expansion provenance { MacroName, Version, InputHash, OutputHash, ExpansionTrace, CompilerVersion, CapabilityUsage }; included in CPCPF artifacts and the event log (RFC-0051 §7). | [227] |
| **Macro classes** | Syntax macros (language surface), Semantic macros (typed cognitive structures), Cognitive macros (goals/agents/workflows/policies/simulations) — RFC-0051 §5. | [226], [227] |
| **TestManifest / TestReport** | CTVF machine-readable test package manifest and per-execution structured report (RFC-0052 §5–6; v1.2 fields RequiredRuntimeVersion, SupportedRFCs, FailureReason, VerificationCertificates). | [231], [233] |
| **Cognitive coverage** | CTVF metrics: goal, plan, belief-state, capability, effect, scheduler-path, replay, macro-expansion, transformation coverage (RFC-0052 §8). | [230], [231] |
| **InvocationManifest** | CRAIP invocation contract { InvocationID, AgentID, CallerID, ProtocolVersion, Method, Parameters, RequiredCapabilities, ExpectedEffects, Timeout, Priority, Deadline, ReplayPolicy, TraceContext, AuthenticationContext, VersionConstraints } (v1.1). | [238], [239] |
| **AgentManifest** | CRAIP discovery metadata { AgentID, Version, SupportedMethods, Capabilities, SupportedRFCs, RuntimeVersion, SecurityLevel, Endpoint }. | [238], [239] |
| **RemoteError** | CRAIP structured error { Code, Category, Message, Retryable, CapabilityViolation, TraceReference, Cause }. | [238], [239] |
| **CADFP (RFC-0054)** | Cognitive Agent Discovery and Federation Protocol — control-plane mechanisms for discovering, registering, authenticating, organizing, and monitoring agents across CogOS instances and trust domains; complements CRAIP (data plane). v1.0 Draft [249]. | [248], [249] |
| **CMCWP (RFC-0055)** | Cognitive Multi-Agent Coordination and Workflow Protocol — coordination plane: shared goals, workflows, task delegation, coordination agreements, collective state. v1.0 Draft [251]. | [250], [251] |
| **CSMKSP (RFC-0056)** | Cognitive Shared Memory and Knowledge Synchronization Protocol — knowledge plane: shared knowledge objects, capability-gated subscriptions, causal update propagation, deterministic conflict resolution, provenance chains. v1.0 Draft [253]. | [252], [253] |
| **CDTCP (RFC-0057)** | Cognitive Distributed Transaction and Consistency Protocol — transaction plane: atomic commit-or-compensate multi-agent transactions, isolation levels, commit rules, idempotency, failure matrix, wire schemas. v1.3 **Ratified** per [266]/[267] (three same-label iterations [261]/[263]/[265]). | [265], [267] |
| **Cognitive Federation** | A set of cooperating Cognitive Domains (RFC-0041) sharing discovery, identity, and capability information under defined trust and policy agreements (CADFP §3). | [249] |
| **Federation roles** | Registry Node (directories/discovery), Agent Node (hosts agents), Federation Gateway (cross-domain mediation) — CADFP §3. | [249] |
| **AgentRegistration** | CADFP registration record { AgentManifest, RegistrationTime, LeaseDuration, HealthEndpoint, DiscoveryScopes, TrustAssertions, FederationAgreements }; capability-gated, lease-bounded. | [249] |
| **DiscoveryQuery / DiscoveryResponse** | CADFP query-based discovery contract; responses MUST be deterministic given the same query and registry state. | [249] |
| **FederationManifest** | CADFP topology expression { FederationID, Name, Version, Members, TrustDomain, DiscoveryPolicy, RoutingPolicy, SecurityPolicy, SupportedRFCs }. | [248], [249] |
| **Shared Goal / Task Delegation** | CMCWP primitives: a goal jointly pursued by multiple agents with declared roles; capability-gated transfer of responsibility with retained visibility and event logging. | [251] |
| **Coordination Agreement** | CMCWP formal versioned contract defining collaboration rules (shared goals, responsibilities, capability sharing, conflict resolution, termination); recorded in the event log. | [251] |
| **Collective State** | CMCWP shared progress view in shared Semantic Memory; updates as effects (RFC-0002); consensus-observed (RFC-0023). | [251] |
| **Shared Knowledge Object** | CSMKSP belief/fact/derived conclusion in shared Semantic Memory carrying a provenance chain; synchronization via capability-gated subscriptions in causal order. | [253] |
| **TransactionManifest** | CDTCP immutable transaction contract { TransactionID, CoordinatorID, Participants, IsolationLevel, RequiredCapabilities, ExpectedEffects, Timeout, ReplayPolicy, TraceContext, CompensationPlan, VersionConstraints }. | [257], [259] |
| **Compensation Action** | CDTCP defined effect that reverses or mitigates a committed transaction step; first-class alternative to rollback. | [255], [259] |
| **CDTCP isolation levels** | Read Uncommitted · Read Committed · Repeatable Read · Snapshot · Serializable (CDTCP §9, [259]). | [255], [259] |
| **CTWP (RFC-0058)** | Cognitive Transaction Wire Protocol and Message Encoding — CDTP framing, canonical envelope, message type registry, flag registry, handshake, encoding profiles, stream multiplexing, sequence ordering, replay protection, error codes for CDTCP messages. v1.2 **Ratified** per [276]/[277]/[278]. | [275], [277] |
| **CTSTP (RFC-0059)** | Cognitive Transaction Security and Trust Profile — security plane for the transaction subsystem: cryptographic identity, integrity, replay protection, trust model, secure channels. v1.0 Draft [279]; v1.1 Candidate proposal [280]. | [279], [280] |
| **CDTPEnvelope** | Ratified canonical wire envelope { MagicNumber, ProtocolVersion, MessageType, Flags, MessageID, TransactionID, Epoch, SenderID, CoordinatorID, TraceContext, PayloadLength, Payload, IntegrityBlock } (RFC-0058 §4). | [275], [276] |
| **Message Type Registry** | Stable numeric CDTCP message IDs 0x0001 BeginTransaction … 0x000C Status, 0x00FF Error; experimental 0x8000–0x8FFF, vendor 0x9000–0xFFFF (RFC-0058 §5). | [275] |
| **ClientHello / ServerHello** | CTWP version-negotiation handshake exchanged before any transaction messages; negotiates version, encoding profile, security profile, session identity (RFC-0058 §7). | [275], [276] |
| **Encoding Profiles** | 0x01 Canonical Binary Encoding (default, MUST-support), 0x02 CBOR, 0x03 deterministic MessagePack, 0x04 canonical JSON (RFC-0058 §9). | [275], [276] |
| **ReplayProtection (CTWP/CTSTP)** | { Nonce, SequenceNumber, Epoch, SessionID } — MUST for distributed deployments; duplicates rejected, expired sessions invalid, sequence rollback triggers security failure. | [275], [280] |
| **CDTCP wire schemas** | Prepare (ManifestHash), Prepared (Vote: Commit | Abort), Commit (DecisionProof), Abort (Reason), Compensate (CompensationPlan) — normative in RFC-0057 v1.3 §7.1 ([263]/[265]). | [263], [265] |
| **CognitiveIdentity** | CTSTP v1.1 identity object { IdentityID, IdentityType, PublicKey, AlgorithmProfile, Issuer, ValidFrom, ValidUntil, Capabilities, TrustLevel, AttestationReference } ([280] proposal). | [280] |
| **TransactionSecurityContext** | CTSTP v1.1 per-transaction security state { TransactionID, CoordinatorIdentity, ParticipantIdentities, GrantedCapabilities, SecurityPolicy, TrustLevel, SessionKeys, AuditReference } ([280] proposal). | [280] |
| **IntegrityBlock** | CTSTP v1.1 message integrity structure { Algorithm, Hash, Signature, KeyReference, Timestamp, Nonce } ([280] proposal). | [280] |
| **Trust Chain (CTSTP)** | Hierarchical trust Root Trust Authority → Domain Trust Authority → Cognitive Runtime → Agent Identity → Transaction Participant; explicit and auditable ([280] proposal). | [280] |
| **CILSP/CRAIP numbering note** | [202] proposed RFC-0050=CILSP; capstone took 0050 instead; remote invocation drafted as RFC-0053 CRAIP per [215]/[235] sequence (conflict C-11 lineage). | [202], [235] |
