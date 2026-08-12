# Data Models

> Provenance: Corpus message #2, sub-messages [10], [12], [14], [16], [18], [19]. Snippet IDs link to [Code Snippets](Code-Snippets.md). All types are proposals from the corpus.

## Current Red Value Types (sub-message [10])

Today, Red has values such as:

**SN-052**

```red
integer!
string!
block!
object!
function!
```

The agent system prompt ([19]) additionally references (against the "Red Deep Technical Specification", not present in corpus): all 50+ datatypes, `vector!`, `map!`, `date!`, `error!`, `routine!`, `port!`, `event!`, `font!`, `para!`.

## New Cognitive Primitive Data Types (sub-message [10])

A cognitive layer could introduce semantic types. These are not merely data—they carry meaning for the runtime.

**SN-053**

```red
goal!
plan!
belief!
memory!
skill!
observation!
hypothesis!
policy!
evidence!
event!
capability!
```

## Cognitive Types — Meaning Instead of Structure (sub-message [16])

Traditional type systems describe structure.

**SN-112**

```text
integer
string
object
block
```

A cognitive type system describes meaning. The compiler understands relationships between these concepts.

**SN-113**

```text
Fact
Observation
Belief
Hypothesis
Prediction
Decision
Evidence
Goal
Constraint
Policy
Capability
```

## Goals Instead of Functions (sub-message [10])

Instead of writing imperative procedures (**SN-054**):

```red
analyse: func [file][
    parse file
    summarize
]
```

You could declare an intent (**SN-055**). The runtime decides *how* to achieve the goal.

```red
goal analyse-log [
    observe %server.log
    extract errors
    summarize
    verify
]
```

## Intent Contracts (sub-message [16])

Today's languages define function contracts (**SN-110**):

```red
func [
    x [integer!]
]
```

A cognitive language defines intent contracts. The runtime now understands expectations.

**SN-111**

```red
goal [
    purpose: "Summarise repository"
    expected-output: report!
    quality >= 95%
    deadline: 5 minutes
    budget: low
]
```

## Goal Attributes — Native Goal Scheduler (sub-message [12])

Traditional runtimes schedule threads.

**SN-078**

```
Thread A
Thread B
Thread C
```

A cognitive runtime schedules goals. Scheduling becomes a language feature instead of an application concern.

**SN-079**

```
Goal
 │
 ├── Priority
 ├── Deadline
 ├── Dependencies
 ├── Confidence
 ├── Cost
 └── Policies
```

## Policies Become Types (sub-message [12])

Today's type systems answer questions like:

**SN-073**

```
integer?
string?
block?
```

A cognitive language extends the type system. The compiler can reject unsafe plans before execution. (See also [Security](Security.md).)

**SN-074**

```
safe?
trusted?
private?
external?
verified?
reversible?
idempotent?
```

**SN-075** — Example:

```red
delete-directory: capability! [
    policy: dangerous
]
```

## Cognitive Effects (sub-message [12])

Functional languages have **effect systems**. A Cognitive Red could introduce semantic effects. The compiler now knows not only the types, but also the behavioural impact of the code.

**SN-076**

```
observe!
remember!
modify!
communicate!
reason!
execute!
learn!
```

**SN-077** — A function signature might become:

```red
analyse: func [
    repo [repository!]
][
    effects [
        observe
        remember
        reason
    ]
]
```

(The agent system prompt [19] lists "effects" among the Red/Cognition cognitive layer items and refers to "the BDI-style semantics and four-dimensional uncertainty model defined in the specification" — specification not present in corpus.)

## Native Reasoning Blocks (sub-message [10])

Blocks are already one of Red's greatest strengths. A cognitive dialect could extend them naturally. The block becomes a structured reasoning graph rather than ordinary control flow.

**SN-056**

```red
reason [
    if confidence < 80% [
        gather-more-evidence
    ]
    compare alternatives
    estimate cost
    choose best-plan
]
```

## Memory as a Language Primitive (sub-message [10])

Instead of manually storing variables:

**SN-057**

```red
cache: make map! []
```

you could express semantic memory directly. The runtime would determine where and how to store and retrieve that information.

**SN-058**

```red
remember [
    user prefers offline execution
]

remember [
    repository contains Rust workspace
]

recall [
    projects about OpenClaw
]
```

## First-Class Skills (sub-message [10])

Today's functions are general-purpose code. A cognitive language could distinguish reusable *skills*. Skills may internally call local code, external tools, or AI models.

**SN-059**

```red
skill summarize
skill search-web
skill inspect-github
skill compile-rust
skill debug-tests
```

## Multi-Model Reasoning (sub-message [10])

The language could allow different reasoning engines. The runtime selects the most appropriate model while presenting a uniform language interface.

**SN-063**

```red
reason using small-model [
    classify message
]

reason using planner [
    build execution graph
]

reason using verifier [
    check consistency
]
```

## Built-in Reflection Syntax (sub-message [10])

Traditional programs rarely analyse themselves. A cognitive language could support reflection explicitly. Reflection becomes part of normal program execution.

**SN-062**

```red
reflect [
    expected success
    actual partial-success
    explain failure
    improve future plan
]
```

## A Complete Agent Example (sub-message [10])

This reads less like a traditional program and more like a specification of autonomous behaviour.

**SN-065**

```red
agent "Repository Assistant" [

    remember [
        project: "OpenClaw"
        language: Rust
    ]

    when github.push [
        observe repository

        reason [
            identify changed modules
            estimate impact
            choose review strategy
        ]

        plan [
            run tests
            inspect architecture
            summarize changes
        ]

        act [
            generate report
        ]

        reflect [
            compare prediction with results
            remember lessons
        ]
    ]
]
```

## Agent Object Model & Agent Ownership (sub-messages [14], [18])

**SN-104** (cognitive object model; objects model *reasoning entities*, not *things*):

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

Agent Principles from the agent system prompt ([18]): agents are persistent cognitive entities. Each agent owns: identity; goals; beliefs; skills; capabilities; policies; working memory; reflection history; execution history. Agents communicate through structured protocols rather than arbitrary text.

## Related pages

[Components](Components.md) (CogProcess SN-041, semantic entities SN-095, provenance SN-099) · [Security](Security.md) · [Workflows](Workflows.md)

---

## Message #4 additions — Ratified language data model (RC-200, msg#4 [43]–[49])

### Cognitive types (ratified, RC-200 §10; subject to RFC-0001)

`goal!` · `belief!` · `plan!` · `skill!` · `memory!` · `capability!` · `effect!` · `agent!` · `checkpoint!`

Evolution path (RC-200 §10.1, ratified): **Dialect → Structured Value → Native Type (optional)**. Types MAY be implemented initially as structured objects or dialects before becoming native datatypes. "Do not immediately make these native Red datatypes" ([44]); rationale: "Every abstraction must reduce complexity." This 9-type list is the ratified consolidation of earlier variants: msg#2 SN-053 (11 types incl. observation!/hypothesis!/policy!/evidence!/event!) and msg#3 [34] (7 types) — see duplicate log.

### Goal / Belief / Plan semantics (RC-200 §7, ratified)

- **Goal** — a desired state or outcome. Declarative by default (what, not how); may contain constraints, priorities, deadlines; may be satisfied through multiple plans.
- **Belief** — a proposition held by an agent with associated confidence and provenance. Must carry confidence value; must carry source/provenance; may carry temporal validity; may be contradicted or updated.
- **Plan** — a sequence of actions intended to achieve a goal. May be declarative or procedural; may contain parallel and dependent steps; must be inspectable and modifiable.

Cognitive block example (ratified spec, SN-225): `goal [ achieve: system-healthy priority: high constraints: [energy-low cost-low] deadline: 2026-12-31 ]`

### Cognitive Block Evaluation Contract (RC-200 §5.1, ratified)

A cognitive block MUST: remain valid Red data at all times; be fully inspectable without execution; require explicit cognitive evaluation to produce external effects; preserve its original source representation. **Evaluation boundary (v1.2 clause):** "A cognitive block SHALL have no external effect unless passed through an approved cognitive evaluation boundary." Evaluation via `evaluate`, `run`, or equivalent cognitive primitives ([45]). Principle: "Data is data until evaluated" ([44]). Semantic model ([44]): `goal [...]` creates Block Value → Cognitive AST → Cognitive Runtime Evaluation; execution requires explicit evaluation.

### Effect System Contract (RC-200 §8.1, ratified)

Every cognitive action MUST declare its effects, MUST identify the required capabilities, MUST produce an execution trace. **Effect** = a state change outside the agent's internal reasoning context. **Effect classes (initial)**: `pure!` · `internal!` · `external!` · `capability!`. Effect ordering deferred to RFC-0002. Effects enable static analysis, security verification, replay, simulation ([44]). Example ([44]): `plan [ step [ action: read-file effect: [filesystem.read] ] ]` (source shows auto-linked `[[filesystem.read](http://filesystem.read)]`).

### Agent type separation ([44] §4.4)

`agent!` should not represent intelligence. An agent is a runtime entity: agent! { identity, capabilities, memory, goals, state }. The intelligence mechanism remains external (symbolic planner / rule engine / neural model / human operator) — preserves Cognitive Neutrality.

### Error and failure semantics (RC-200 §13, ratified)

New failure classes, MUST be first-class and traceable: Goal failure · Belief conflict · Capability denial · Planning failure · Verification failure · Memory inconsistency.

### Agent & Session state models (msg#4 [58], [59], [60])

- **Agent (RC-600 §5):** Agent { Identity, Capabilities, Goals, Beliefs, Plans, Memory References, Execution State, Trace History, Checkpoint State }.
- **Agent State canonical runtime object ([58]):** { Identity, Goals, Beliefs, Plans, Memory References, Capabilities, Execution Trace, Checkpoint State }.
- **Session ([60]):** Session { Identity, Agent Reference, Execution Mode, Interaction History, Active Capabilities, Trace Context, Checkpoint Reference }.
- **Runtime Event ([56]):** Event { id, timestamp, source, capability-context, payload, provenance }.
- **CIR node model (RC-300 v1.1 §6):** Goal/Plan/Belief/Effect structures (see Architecture page).

---

## Message #8 additions — Ratified cognitive value model (RFC-0001 v1.2 RATIFIED; RFC-0002 v1.1 RATIFIED; RFC-0003 v1.1 candidate)

### Cognitive Value Base Contract (RFC-0001 §3, ratified [72])

Every cognitive value MUST conform to: `cognitive-value { cognitive-meta { id: UUID, created: timestamp, modified: timestamp, provenance: source, version: integer }, type: cognitive-type, schema-version: integer }`. "Every cognitive value is therefore: Identity + Metadata + Semantic Type + Versioned Schema."

### Ratified cognitive types (RFC-0001 §4/§7, ratified [72])

| Type | Category | Initial Form | Evolution | Mutation Model | Owner |
|---|---|---|---|---|---|
| `goal!` | Intent | Structured block/object | Native (optional) | Mutable lifecycle (Created → Active → Planning → Executing → Satisfied/Failed → Archived) | Agent |
| `belief!` | Knowledge | Structured block/object | Native (optional) | Append/revision (Created → Confirmed/Updated → Contradicted → Deprecated/Archived; statuses: tentative/confirmed/disputed/deprecated/retracted) | Agent/System |
| `plan!` | Procedure | Structured block/object | Native (optional) | Mutable with history (Draft → Validated → Executable → Running → Completed/Failed) | Agent |
| `skill!` | Procedure | Object/compiled | Native | Versioned immutable | System |
| `memory!` | Knowledge | Object | Native | Reference-controlled | Agent/System |
| `capability!` | Security | Object | Native | Immutable token | System |
| `effect!` | Event | Structured value | Native | Immutable event | System |
| `agent!` | Entity | Object | Native | Persistent entity (runtime lifecycle managed) | Runtime |
| `checkpoint!` | Snapshot | Object/serialized | Native | Immutable snapshot | Runtime |

### Ratified semantic graph + cardinality (RFC-0001 §6, ratified [72])

goal! (1:N) ──satisfied-by──▶ plan! (1:N) ──executes──▶ skill! (1:N) ──produces──▶ effect! (N:M) ──updates──▶ belief!. Implementations MUST NOT remove these relationships; they are part of the Cognitive IR contract. Memory mapping ([70]): belief!→Semantic Memory; effect!→Episodic Memory; skill!→Procedural Memory; goal!/plan!→Working Memory.

### Type identity (RFC-0001 §5)

Every cognitive value MUST support `type-of value` (returns e.g. goal!, belief!). Compiler pipeline (ratified [72]): Red Source → Dialect AST → Cognitive IR → Unified IR → CVM → Cognitive Runtime. Conformance: preserve type identity, metadata/provenance, mutation rules, semantic relationships, deterministic serialization; implementations MAY use blocks/objects/native datatypes.

### Effect model (RFC-0002 v1.1, ratified [76])

**Effect Identity:** globally unique Effect ID, stable through serialization/checkpointing/restoration/distributed propagation/replay. **Classes:** pure! (no side effects; rollback N/A) · internal! (internal state only; rollback yes) · capability! (authorization required; controlled) · external! (direct external change; limited). **Lifecycle (normative state machine):** Created → Validated → Authorized → Scheduled → Executing → Committed → Archived (rollback/compensation transitions where supported). **Metadata contract:** effect { id: EffectID, type: effect-class, provenance: source, capability: capability-reference (optional), timestamp, dependencies: [EffectID], replay-policy: deterministic | best-effort }. **Ordering:** Temporal Order vs Causal Order (independent dimensions; causal order MUST be preserved under parallelization); "The Effect Dependency Graph **MUST** form a **Directed Acyclic Graph (DAG)**" — circular dependencies are invalid and MUST be rejected during analysis or execution; prerequisites execute before dependents; independent branches MAY run concurrently. This graph "becomes the canonical execution model for Cognitive IR and CVM scheduling" ([76] §4). **Conflicts:** Direct / Capability / Temporal / Causal; strategies: rejection, serialization with retry, transactional boundaries, human/agent mediation. **Transactions:** atomic wrt external state; commit all or rollback/compensate; declared or inferred from capability usage. **Rollback/compensation:** pure!/internal! generally rollback-safe; capability!/external! MUST declare support; compensation actions are themselves effects. **Replay contract:** externally observable behaviour equivalent; internal scheduling may differ where permitted. **Parallelism:** allowed when no causal dependency, no resource conflict, capabilities permit; sequential trace semantics MUST be preserved. **Distributed:** causal ordering across nodes; cross-stream conflict detection; consistent checkpointing.

### Belief model (RFC-0003 v1.1, [79]; accepted for final ratification [80])

**Identity/versioning:** stable BeliefID; revisions increment version preserving BeliefID; historical revisions addressable. **Metadata:** belief { cognitive-meta…, proposition, confidence: float 0.0–1.0, source, timestamp, validity-window (optional), contradictions: [BeliefID], revision-cause: observation | inference | external-input | effect | manual, status: tentative | confirmed | disputed | deprecated | retracted }. **Revision graph:** directed graph (review [80] recommends MUST be DAG; cycles rejected; non-initial revisions reference ≥1 parent); alternative paths before reconciliation; deterministic replay of any valid path. **Update rules:** direct update (higher/equal authority, valid confidence bounds, no unresolved contradiction); on contradiction record contradiction + adjust confidence; agent MAY revise/observe/escalate. **Confidence:** all changes recorded in trace with cause/source; contradictory evidence MUST decrease confidence. **Authority policy:** implementations MUST define a deterministic, documented policy. **Effect coupling:** belief-changing effects MUST reference affected beliefs; traceable to originating action and capability. Causal chain ([78]): Action → effect! → belief revision → plan revision → goal evaluation. Recommended editorial additions ([80]): confidence boundary semantics (0.0 no confidence, 1.0 complete, outside invalid); "Replay MUST preserve both belief values and revision topology"; beliefs SHALL normally reside in Semantic Memory (Working Memory MAY hold transient references); extensible revision causes (implementation-defined, documented); authority policy in conformance reports.

---

## Message #10 additions — Goal/Plan/Capability/Skill/Memory models (RFC-0003 v1.2 ratified; RFC-0004 v1.1 ratified; RFC-0005 v1.0; RFC-0006 v1.2 approved; RFC-0007 v1.1; RFC-0008 v1.0)

### Belief model final (RFC-0003 v1.2, RATIFIED [82])

Supersedes v1.1 additions: revision-cause enum extended with `implementation-defined` (extensible, implementations document additions); revision graph MUST be DAG (non-initial revisions reference ≥1 parent; cycles rejected); replay MUST preserve revision topology; Memory Placement section: beliefs SHALL normally reside in Semantic Memory; Working Memory MAY hold transient references; authority policy MUST be included in conformance reports.

### Goal model (RFC-0004 v1.1, RATIFIED [86])

**Identity/versioning:** stable GoalID, constant across revisions and state transitions; every modification increments version; historical versions addressable. **Metadata:** goal { cognitive-meta…, target, priority: float (optional), constraints: [constraint] (optional), deadline: timestamp (optional), required-capabilities: [CapabilityID] (optional), status: pending | active | planning | executing | satisfied | failed | archived, satisfied-by: [EffectID] (optional), supporting-beliefs: [BeliefID] (optional), completion-time: timestamp (optional) }. **Lifecycle:** Created (Pending) → Active → Planning → Executing → Satisfied/Failed → Archived; backward transitions prohibited unless restored from checkpoint; terminal states: Satisfied, Failed, Archived. **Satisfaction:** target condition true under current belief state AND all declared constraints met; evaluated against current belief set; respects constraints and required capabilities; deterministic given same belief state. **Failure:** all viable plans exhausted; hard constraint/deadline violated; unrecoverable contradiction in supporting beliefs; failure recorded with cause(s). **Dependency graph:** goal dependencies MUST form DAG; cycles rejected; goal MUST NOT be satisfied before prerequisites. **Ownership:** Personal / Shared / System goals. **Memory placement:** goals SHALL normally reside in Working Memory while active; MAY be archived into Episodic Memory on completion/failure. **Replay:** equivalent goal states; preserve identity/version and causal chain actions → effects → belief updates → goal state transitions. Review recommendations NOT adopted in v1.1 (preserved in [84]): Unsatisfied-vs-Failed distinction; goal-result metadata name (adopted as satisfied-by/supporting-beliefs/completion-time fields instead).

### Plan model (RFC-0005 v1.0 draft [87]; v1.1 recommended by [88], not yet in corpus)

**Identity/versioning:** stable PlanID; revisions increment version; history addressable. **Metadata:** plan { cognitive-meta…, goal: GoalID, steps: [step], dependencies: [PlanID] (optional), preconditions: [condition] (optional), expected-effects: [EffectID] (optional), required-capabilities: [CapabilityID] (optional), status: draft | validated | executable | running | completed | failed | abandoned }. **Lifecycle:** Draft → Validated → Executable → Running → Completed/Failed/Abandoned. **Goal coupling:** plan MUST associate with exactly one goal; goal MAY have zero or more plans; plan MUST NOT be successful unless its goal is satisfied. **Skills/effects:** each step MUST reference ≥1 skills; execution MUST produce traceable effects; expected effects MUST be consistent with produced effects. **Planning process:** invocation of planning mechanisms (symbolic, rule-based, learned, human); runtime/CVM MUST support invocation without embedding algorithms. **Revision/replanning:** revisions preserve PlanID; replanning triggered by belief changes, effect outcomes, capability revocation; all revisions traced. **Recommended v1.1 additions ([88], not yet normative):** plan dependency DAG; StepID (step {StepID, skill, preconditions, expected-effects, status}); validation criteria (structural correctness, dependency consistency, capability availability, precondition consistency, no cycles); execution states incl. Suspended; ownership (Agent/Shared/System plans); memory placement (active in Working, historical in Episodic); revision DAG with topology-preserving replay; "Goal satisfaction is determined by observed effects and supporting beliefs, not merely by plan completion."

### Capability model (RFC-0006 v1.2, approved for Final Ratification [94])

**Identity:** stable CapabilityID; every modification (incl. revocation, expiration, delegation metadata, administrative updates) MUST increment version preserving CapabilityID. **Metadata:** capability { cognitive-meta…, type: capability-type, scope, owner: AgentID | Runtime | CogOS, granted-to: AgentID, granted-by: authority, delegated-from: CapabilityID (optional), expiration: timestamp (optional), status: active | revoked | expired }. **Scope immutability:** scope MUST be immutable after issuance. **Lifecycle:** Created → Granted → Active → Revoked/Expired; legal transitions table: Created→Granted ✓, Granted→Active ✓, Active→Revoked ✓, Active→Expired ✓, Revoked→Active ✗, Expired→Active ✗. **Graph:** capability inheritance/dependencies MUST form DAG; cycles rejected; dependent capability MUST NOT be granted before prerequisites active. **Resolution order — RFC-0006 v1.2 §6 verbatim (deterministic order):**

1. Capability exists
2. Status == Active
3. Scope is valid
4. Not expired
5. Not revoked
6. Policy allows the action

Evaluation **MUST** terminate at the first failed validation step, and the failure reason **MUST** be recorded in the execution trace. **Effects integration:** grants and revocations MUST themselves be `effect!` values (RFC-0002). **Enforcement:** checks before effect execution; violations produce traceable errors; usage recorded. **Trace contract:** CapabilityTrace { CapabilityID, AgentID, EffectID, Timestamp, Decision: Allow | Deny }. **Delegation:** MAY be delegable; MUST preserve provenance via `delegated-from`. **Memory placement:** active in Working; definitions MAY be Semantic; revoked/expired SHOULD be archived Episodic. **Replay:** same constraints; checks at same causal points; revoked stays revoked; equivalent error behaviour. **Conformance:** preserve CapabilityID; enforce checks; record all grants/revocations/usages; preserve state during replay; reject invalid transitions; include authority policy in conformance reports.

### Skill model (RFC-0007 v1.1 Candidate [97]; v1.2 additions recommended [98])

**Identity:** stable SkillID across versions. **Metadata:** skill { cognitive-meta…, name, specification: [parameter], inputs: [parameter], outputs: [parameter], preconditions: [condition] (optional), postconditions: [condition] (optional), declared-effects: [EffectClass], required-capabilities: [CapabilityID] (optional), performance-metadata: {…} (optional) }. **Lifecycle:** Created → Registered → Active → Deprecated → Archived; transitions: Created→Registered ✓, Registered→Active ✓, Active→Deprecated ✓, Deprecated→Archived ✓, Archived→Active ✗. **Interface contract:** MUST declare inputs, outputs, preconditions, postconditions, declared effects, required capabilities. **Purity:** pure! / internal! / capability! / external! (aligned with RFC-0002 effect classes). **Invocation identity:** SkillInvocationID; SkillInvocation { SkillInvocationID, SkillID, PlanID, GoalID, Timestamp, Inputs, Outputs, Effects, CapabilitiesUsed }. **Failure semantics:** failures MUST produce trace entries; MAY produce compensating effects; MUST be replayable. **Memory placement:** definitions MAY be Semantic; invocations/traces SHALL be Episodic; compiled implementations MAY be Procedural. **Recommended v1.2 additions ([98]):** registered skill definitions SHALL be immutable; invocation uniquely determined by {SkillID, Version, Inputs, Runtime Context, Capability Set, Relevant Belief State}; skill dependency DAG (recursion must be explicitly declared); invocation lifecycle (Created→Validated→Authorized→Executing→Completed/Failed→Archived); SkillTrace {SkillInvocationID, SkillID, PlanID, GoalID, StartTime, EndTime, Status, EffectsProduced, CapabilitiesUsed}; purity enforcement rules; registration validation; belief relations (belief changes only via effect!); memory access rules ("Skills MUST NOT directly mutate Semantic Memory. All memory modifications MUST occur through effects."); extended conformance.

### Memory model (RFC-0008 v1.0 draft [99]; v1.1 additions recommended [100])

**Four tiers (normative table):** Working (current execution context; ephemeral; per agent) · Episodic (events/experiences/traces; persistent; per agent) · Semantic (knowledge/concepts/facts; persistent; shared) · Procedural (skills/compiled procedures/capabilities; persistent; shared). **Access rules:** Working: free read/write, execution-scoped, bounded eviction. Episodic: read own episodes; append via effect!; historical episodes immutable. Semantic: read shared; write controlled by capability/policy; updates create new versions. Procedural: read skills; write via system registration; new versions create new skill! entries. **Ownership/isolation:** every entry MUST have owner; no cross-agent private access without capability; CogOS MAY manage shared memory with access control. **Mutations as effects:** observable memory mutations MUST be effect! values with provenance. **Replay:** reads consistent with original trace; mutations in same causal order; checkpoint restoration replayable. **Type placement:** goals/plans in Working while active; beliefs in Semantic; skills in Procedural; effects appended to Episodic. **Recommended v1.1 additions ([100], 15 items):** MemoryID + versioning; memory lifecycle (Created→Active→Updated→Archived→Deleted(optional), logical deletion); access contract (read/write/append/update/archive/forget with capability/trace/replay per op); MemoryReference/MemoryEntry/MemorySnapshot; Working Memory semantics (agent-local, execution-scoped, reconstructed on replay, never authoritative); Episodic append-only; Semantic versioned retrieval (deterministic policy); Procedural registration validation; memory dependency graph; consistency guarantees (immediate/deterministic/version/append); MemorySnapshot {SnapshotID, Timestamp, WorkingMemory, SemanticVersion, ProceduralVersion, EpisodicPosition}; forgetting rules (preserve provenance, replay correctness, historical traces); capability table per operation; MemoryTrace {MemoryID, Tier, Operation, AgentID, Timestamp, Provenance}; conformance guarantees.

---

## Message #12 additions — Agent/Checkpoint/Scheduler/CVM/CISA models (msg#12 [101]–[120])

### Agent model (RFC-0009 v1.0 draft [101])

**Identity:** stable AgentID, constant throughout lifetime. **Metadata:** agent { cognitive-meta…, name (optional), owner: AgentID | Runtime | CogOS, capabilities: [CapabilityID], status: created | initialized | active | suspended | checkpointed | terminated }. **Lifecycle:** Created → Initialized → Active → Suspended → Checkpointed/Restored → Terminated. **Ownership/isolation:** every agent MUST have owner; MUST NOT access another agent's private memory/state without capability authorization; CogOS MAY manage shared resources with access control. **State:** AgentState { Identity, Goals, Beliefs, Plans, Memory References, Active Capabilities, Execution Context, Trace History, Checkpoint References }. **Type relationships:** MAY own goals/beliefs/plans/capabilities; MUST invoke skills through plans; MUST produce effects when interacting with external world. **Memory placement:** identity/metadata MAY be Semantic; active state SHALL be Working; history/traces SHALL be Episodic. **Recommended v1.1 additions ([102]):** versioning rule; legal transition table (Terminated→Active ✗); agent execution loop (Observe → Update Beliefs → Evaluate Goals → Select Plan → Invoke Skills → Produce Effects → Update Memory); scheduler states orthogonal to lifecycle (Runnable/Waiting/Blocked/Sleeping/Executing); AgentTrace { AgentID, Timestamp, PreviousState, NewState, GoalID, PlanID, EffectID }; coordination graph (shares-goal, delegates; SHOULD be DAG); Mailbox { MessageID, Sender, Receiver, Timestamp } (basis for future Inter-Agent Communication RFC); Resources { WorkingMemory, ActiveGoals, ActivePlans, CapabilitySet, SchedulerQuota }; ownership classes (Runtime/Administrative/Logical/Parent); creation prerequisites (AgentID, initial Working Memory, capability set, execution context, scheduler registration); termination duties (archive traces/goals, release capabilities, flush Working Memory, produce termination effect); checkpoint capture { AgentState, WorkingMemory, ActivePlans, CapabilityState, SchedulerState }; conformance list.

### Checkpoint model (RFC-0010 v1.0 draft [103])

**Identity:** stable CheckpointID. **Metadata:** checkpoint { cognitive-meta…, agent: AgentID, timestamp, captured-state: { working-memory, active-goals, active-plans, capability-state, execution-context }, associated-trace: TraceID (optional) }. **Lifecycle:** Created → Stored → Restored → Archived. **Minimum contents:** agent identity+version; Working Memory state; active goals+versions; active plans+versions; capability state (grants/revocations); execution context (instruction pointer or equivalent); trace position/reference. **Creation:** explicit by agent / automatic at boundaries / by Runtime or CogOS; MUST be deterministic snapshot; MUST be traced. **Restoration:** MUST restore captured condition, resume from recorded context, preserve capability constraints. **Effects/traces:** associated with originating trace; creation/restoration MUST be effects where observable. **Recommended v1.1 additions ([104]):** immutability ("Any modification or re-capture MUST create a new CheckpointID"); legal transitions table (Archived→Stored ✗); completeness contract incl. scheduler/execution state; memory reference strategy (Working by value; Semantic/Procedural by version; Episodic by trace position); consistency boundaries (before plan execution, after effect commitment, after belief revision, after transaction; never during partial transitions); restoration validation (integrity, memory/skill/capability versions, trace consistency; MUST fail if unsatisfied); CheckpointTrace { CheckpointID, AgentID, Timestamp, TracePosition, Action: Create|Restore }; incremental checkpoints MAY (full = reference model); failure outcomes (Success, ValidationFailure, MissingDependency, CorruptedCheckpoint, UnsupportedVersion — each traced); scheduler state preservation (runnable/blocked/waiting/priority); conformance list.

### Scheduler model (RFC-0011 v1.2, RATIFIED [111])

**Identity:** Scheduler { SchedulerID, SchedulerClass, Policy, Version }; SchedulerID stable; policy/metadata changes increment version. **Execution states:** Runnable → Waiting (blocked on resource/capability/dependency) → Executing → Suspended → Terminated. **Legal transitions:** Runnable→Executing ✓, Executing→Waiting ✓, Waiting→Runnable ✓, Executing→Suspended ✓, Suspended→Runnable ✓, Executing→Terminated ✓, Waiting→Terminated ✓, Terminated→Runnable ✗. **Queues:** Ready (Runnable), Waiting (Blocked), Suspended, Completed; each schedulable entity MUST belong to exactly one queue. **ScheduleDecision trace:** { DecisionID, Timestamp, SchedulerID, AgentID, PlanID, RunnableSet, SelectedProcess, Reason }. **Inputs:** Priority, Deadline, Resource requirements, Capability constraints, Current execution state, Fairness metrics. **Deterministic tie-breaking (equal priorities):** 1. Earlier deadline, 2. Older enqueue timestamp, 3. Lower AgentID, 4. Lower PlanID. **Classes:** S0 Cooperative / S1 Priority-based / S2 Deadline-aware / S3 Adaptive Cognitive Scheduling. **WaitingReason model:** Goal | Plan | Effect | Capability | Resource | Timer | ExternalEvent | ImplementationDefined. **Scheduler events as effects:** suspend/resume/preempt/terminate MUST be effect! values. **Checkpoint integration:** MUST preserve runnable queue, waiting queue, current process, scheduler state, pending timers. **Hierarchy:** CogOS Scheduler → Runtime Scheduler → Agent Scheduler. **Conformance:** preserve deterministic order; preserve scheduler state during replay; record decisions; honour declared policy; reject illegal transitions; preserve fairness. Non-blocking editorial suggestions for v1.3 ([110]): PolicyID/PolicyVersion; queue ordering semantics (deterministic); PreviousDecisionID causal links; SchedulerState { ReadyQueue, WaitingQueue, SuspendedQueue, CurrentExecution, PolicyState, TimerState }.

### CVM model (RFC-0012 v1.1, approved [116])

**Identity:** CVM { CVMID, SupportedCISARevision, ExecutionProfile, Version }; CVMID stable; implementation/configuration changes increment version. **ExecutionContext:** { InstructionPointer, OperandStack, RegisterSet, WorkingMemoryReference, CurrentAgent, CurrentPlan, CurrentGoal, CapabilityContext, TraceContext }; MUST be serializable for checkpointing. **Pipeline:** Fetch → Decode → Validate → Capability Check → Execute → Produce Effects → Update Trace → Advance Instruction Pointer. **Transaction model (§5.1):** Begin → Validate → Capability Check → Execute → Generate Effects → Commit → Trace; on failure abort + trace; partial effects MUST NOT be committed. **Instruction classes (§6.1):** pure! / internal! / capability! / external!. **Scheduler contract:** scheduler owns WHEN execution happens; CVM owns HOW; CVM executes until completion/yield/block/preemption/termination; scheduler MUST resume from preserved instruction pointer and context. **Capability enforcement:** check before execution; failures traced; failed instructions MUST NOT produce partial effects. **Memory rules:** Working R/W in context; Semantic read + capability-mediated write; Episodic append-only; Procedural read for skill invocation. **Checkpoint:** MUST preserve IP, operand stack, registers, Working Memory reference, capability context, trace context; restoration resumes exact IP/context. **InstructionTrace:** { TraceID, Timestamp, CVMID, AgentID, InstructionPointer, InstructionID, Opcode, Operands, Result, Effects }. **Recommended v1.1 additions from review [114] that were adopted:** InstructionID, transaction model, purity classes, scheduler/CVM ownership rule. Recommended but NOT in v1.1 (preserved in [114]): ExternalInputRecord { InputID, Source, Timestamp, Value, TraceID } for deterministic sensor replay; register class details; CISA instruction format.

### CISA model (RFC-0013 v1.1 candidate [119]; review [120])

**Instruction format:** Instruction { InstructionID, EncodingVersion, Opcode, OperandCount, OperandTypes: [type], AddressingMode, CapabilityRequirement: CapabilityClass (optional), EffectClass: pure! | internal! | capability! | external! }. **Addressing modes:** Immediate, Register, Memory Reference, Capability Reference, Effect Reference, Belief Reference, Goal Reference, Plan Reference. **Register architecture (v1.1 with mutability):** G-registers (16, general-purpose, Mutable) · M-registers (8, memory references, Reference only) · C-registers (8, capability context, Runtime controlled) · T-registers (8, trace/provenance, Write-only by trace engine) · S-registers (4, scheduler interaction, Scheduler controlled). **Opcode families:** Data Movement (LOAD, STORE, MOVE, SWAP); Belief (BELIEF_ASSERT/RETRACT/QUERY/UPDATE); Goal (GOAL_CREATE/ACTIVATE/SATISFY/FAIL/ARCHIVE); Plan (PLAN_CREATE/VALIDATE/EXECUTE/REVISE/ABORT); Memory (MEM_READ/WRITE/APPEND/CHECKPOINT/RESTORE); Capability (CAP_REQUEST/RELEASE/VERIFY); Effect (EFFECT_EMIT/COMMIT); Control Flow (BRANCH/JUMP/CALL/RETURN/YIELD); Observation & Reflection (OBSERVE/INFER/REFLECT/EXPLAIN). **Transaction model (§6):** every instruction atomic: Begin → Validate → Capability Check → Execute → Generate Effects → Commit → Trace; abort with no partial effects on failure. **Binary representation:** versioned, deterministic, forward/backward compatibility within major version; concrete encoding deferred to RFC-0014. **Review recommendations for v1.2/future ([118]/[120]):** atomic effect boundary (EFFECT_BEGIN → EFFECT_EMIT → EFFECT_VALIDATE → EFFECT_COMMIT → TRACE_APPEND); meta-cognitive mapping (OBSERVE: Environment→Belief; INFER: Beliefs→Knowledge; REFLECT: Execution→Self-model; EXPLAIN: Trace→Human-readable reasoning); CognitiveException { InvalidInstruction, CapabilityDenied, BeliefConflict, GoalViolation, PlanFailure, MemoryFault, ExternalFailure }; full execution pipeline (Fetch Instruction → Decode Opcode → Validate Operands → Check Capability → Execute Semantic Operation → Generate Effects → Commit State → Write Trace → Advance PC); RFC-0014 scope (binary layout incl. Magic Number/Version/Opcode/Flags/Operand Count/Operands/Capability ID/Effect Class; opcode numeric assignments; operand encoding; deterministic serialization via Canonical Encoder → SHA-256 Execution Identity; register ABI; exception ABI; JIT constraints).

---

## Message #14 additions — execution/runtime/distributed data models (msg#14 [121]–[140])

### Instruction binary model (RFC-0014 [121], ratified-grade draft)

CISA binary instruction layout (10 fields, see Architecture); Operand { Type (1 byte), Size (2 bytes), Value (variable) }; operand types: Immediate, Register reference, Memory reference (UUID), Belief/Goal/Plan/Capability/Effect reference. Example opcode assignments: LOAD 0x0001, STORE 0x0002, MOVE 0x0003, BELIEF_ASSERT 0x0010, BELIEF_RETRACT 0x0011, GOAL_CREATE 0x0020, GOAL_SATISFY 0x0021, PLAN_EXECUTE 0x0030, CAP_VERIFY 0x0040, EFFECT_EMIT 0x0050, OBSERVE 0x0060, INFER 0x0061. Proposed future opcode space ([122]): 0000-00FF Core VM, 0100-01FF Memory, 0200-02FF Beliefs, 0300-03FF Goals, 0400-04FF Plans, 0500-05FF Skills, 0600-06FF Capabilities, 0700-07FF Effects, 0800-08FF Agent Operations, 0900-09FF Multi-Agent, 0A00-0AFF Reflection. Proposed CISA Program Container ([122]): CISA Program Header { ProgramID, CISA Version, Required CVM Version, Instruction Count, Entry Point, Metadata Offset } + instructions + metadata + debug info.

### Exception model (RFC-0015 [123])

**Exception hierarchy (8 categories):** ValidationError (instruction/operand validation; recoverable) · CapabilityError (capability missing/revoked; recoverable) · MemoryError (access violation/exhaustion; limited) · SkillError (skill execution failure; recoverable) · PlanError (plan execution failure; recoverable) · GoalError (satisfaction/failure condition; limited) · RuntimeError (internal CVM/runtime failure; not recoverable) · ExternalError (external world failure; limited). **ExceptionTrace:** { TraceID, Timestamp, CVMID, AgentID, InstructionID, ExceptionCategory, ErrorCode, Message, CapabilityContext, RecoveryAction }. **Layer mapping ([124]):** ValidationError→CISA/CVM (RFC-0013/0014), CapabilityError→Security boundary (RFC-0006), MemoryError→Memory (RFC-0008), SkillError→Procedural (RFC-0007), PlanError→Planning (RFC-0005), GoalError→Goals (RFC-0004), ExternalError→Effects (RFC-0002), RuntimeError→CVM/CogOS (RFC-0012). **Trace contract chain:** InstructionTrace → EffectTrace → CapabilityTrace → ExceptionTrace. **Effect recoverability classes ([124]):** reversible / compensatable / irreversible. Recommended additions: ExceptionID { ExceptionID, Category, ErrorCode, SourceInstruction, Timestamp, Version }; failure state machine Detected → Captured → Classified → RecoverySelected → {Retrying | Compensating | Escalated | Terminated}.

### Runtime data models (RFC-0016/0017/0018 drafts + reviews)

**CognitiveRuntime identity ([126] recommended):** { RuntimeID, Version, ConfigurationHash, SupportedRFCVersions, SupportedCISARevision }. **RuntimeEvent (RFC-0018 §3 normative; extended [130]):** { EventID, Timestamp, SourceService: Scheduler|CVM|Memory|Capability|Exception|Checkpoint|Agent, EventType, AgentID, TraceID, CorrelationID (optional), Payload, Provenance } + recommended { ParentEvents: [EventID], SequenceNumber, SchemaVersion, Hash }. **Event ordering:** logical timestamp (Lamport clock or equivalent) + causal dependencies + physical timestamp (observability only); log MUST form DAG. **Event categories:** Scheduling (ScheduleDecision, Preempt, Yield) · Instruction (InstructionExecuted, CapabilityCheck) · Memory (MemoryRead/Write/Append) · Capability (CapabilityGranted/Revoked/Verified) · Exception (ExceptionRaised, RecoveryAction) · Checkpoint (CheckpointCreated/Restored) · Agent (AgentCreated/Suspended/Terminated). **ExternalInputEvent ([130]):** { InputID, Source, Timestamp, Value, Hash } for sensor readings, API responses, human instructions, LLM outputs, network messages. **Event integrity hash chain ([130]):** Hash(A); Hash(B + Hash(A)); Hash(C + Hash(B)). **RuntimeMessage ([128] recommended):** { MessageID, SourceService, TargetService, Timestamp, CorrelationID, AgentID, Payload, TraceID }. **RuntimeService ([128]):** { ServiceID, ServiceType, Version, InterfaceRevision, Capabilities, State }. **Service lifecycle ([128]):** Created → Registered → Initialized → Active → Suspended → Stopped. **ResourceQuota ([126]):** { CPUBudget, MemoryLimit, EffectBudget, CapabilityBudget }. **ResourceAccount ([128]):** { AgentID, CPUTime, MemoryUsed, InstructionCount, CapabilityCalls, ExternalEffects }.

### CogOS & distributed models (RFC-0019…0023 drafts + reviews)

**Cognitive Process (RFC-0019 §4):** { Identity, Agent Reference, CVM Instance, Memory Namespace, Active Capabilities, Resource Quota, Execution State, Trace Context }. **Node (RFC-0020 §3):** { NodeID, Address, Capabilities, SupportedCISARevision, Version }; NodeID stable; config/version changes increment node version. **CNPMessage (RFC-0021 §4):** { MessageID, Timestamp, SourceNodeID, TargetNodeID (or broadcast), MessageType, Payload, CapabilityToken (optional), TraceReference, Signature (optional) }. **CNP message families:** Discovery (NodeAnnouncement/Query/Response) · Execution (RemoteCVMRequest/Response, ExecutionStateTransfer) · Capability (CapabilityDelegation/Revocation/Verification) · Event (EventPropagation/Acknowledgement) · Migration (AgentMigrationRequest/Response, StateTransfer) · Coordination (ConsensusProposal/Vote/Result). **Identity hierarchy (RFC-0022 §3):** NodeID ├── AgentID └── ExecutionContext, ├── CVMID, ├── SchedulerID, ├── CapabilityID, └── CheckpointID. **IdentityVerificationEvent ([138]):** { Identity, Verifier, Capability, Result }. **CapabilityToken ([138] proposed):** { ID, Issuer, Subject, Scope, Constraints, Expiration, Signature }. **ConsensusEvent ([140] proposed):** { ConsensusID, EventSet, Participants, Decision, LogicalTimestamp, Proof }. **Trust domains (RFC-0022 §8):** shared policy & capability authority, common event log visibility, coordinated checkpoint/recovery; cross-domain operations require capability delegation. **Distributed memory (RFC-0020 §7):** Working local per agent; Episodic partitioned/replicated; Semantic/Procedural shared with access control & consistency. **Consensus participation (RFC-0023 §4):** event ordering, checkpoint agreement, conflicting capability resolution, migration outcome coordination — capability-gated; guarantees: eventual causal consistency, deterministic conflict resolution, replay equivalence preserved.

---

## Message #16 additions — governance/hardware/compiler data models (msg#16 [141]–[160])

### Resource models (RFC-0024 [141] + review [142])

**Resource categories (normative table):** Execution Time (CVM cycles/CPU time; Instructions/Time) · Memory (four tiers; Bytes/Entries) · Capability Usage (count per type) · Effect Production (count per class) · Storage (Bytes) · Network/Messaging (Messages/Bytes). **ResourceQuota:** { AgentID, ExecutionBudget, MemoryLimit, CapabilityBudget: {type: count}, EffectBudget: {class: count}, StorageQuota, NetworkQuota } — enforced by CogOS, respected during scheduling/execution. **ResourceState ([142] proposed):** { AgentID, ExecutionUsed, MemoryUsed, CapabilityUsage, EffectUsage, StorageUsed, NetworkUsed, RemainingQuota } — part of checkpoints, replay, auditing, scheduling, consensus. **ResourceEvent ([142]):** { EventID, AgentID, ResourceType, PreviousValue, NewValue, Cause }. **ResourceError hierarchy ([142]):** ExecutionBudgetExceeded, MemoryQuotaExceeded, CapabilityBudgetExceeded, EffectBudgetExceeded, NetworkQuotaExceeded. **CRT (Cognitive Resource Token)** — proposed accounting unit ([142]).

### Policy models (RFC-0025 [143] + review [144])

**Policy:** { PolicyID, Scope: [Agent|Node|Domain|System], Rules: [Rule], Priority, Version }. **Rule:** { Subject, Action, Resource, Condition, Effect: Allow|Deny }. **Policy domains:** Capability, Resource, Trust, Effect, Agent, Domain policies. **Evaluation model:** collect applicable policies → evaluate conditions in priority order → first matching rule wins → record decision; default Deny. **PolicyDecisionTrace:** { TraceID, Timestamp, PolicyID, Subject, Action, Resource, Decision: Allow|Deny, Reason }. **PolicyDecisionEvent ([144]):** { EventID, Subject, Action, Resource, Policy, Decision, Reason }. **PolicyConsensus ([144]):** { PolicyID, Decision, Epoch, Participants }. **PolicyError hierarchy ([144]):** UnauthorizedAction, PolicyConflict, InvalidPolicy, MissingContext, TrustViolation.

### Hardware models (RFC-0026 [145] + review [146])

**Accelerator categories (normative table):** Vector/Matrix (GPU, TPU, NPU) · Symbolic (FPGA graph processors) · Secure Enclave (TPM, SGX, TrustZone) · Energy-Efficient (specialized MCUs, NPUs) · I/O Acceleration (DMA engines, RDMA). **AcceleratorContext ([146]):** { AcceleratorID, Type, CapabilityContext, AttestationState, ExecutionProfile, ResourceBudget }. **HardwareExecutionEvent ([146]):** { EventID, InstructionID, AcceleratorID, ExecutionMode: Hardware, InputHash, OutputHash, Attestation, Timestamp (logical epoch) }. **AcceleratorAccess capability example:** { DeviceClass: NPU, Operations: MatrixMultiply, Budget: 5000 operations, Expiry: Epoch 9000 }. Proposed CISA extensions: VECTOR_EXEC, MATRIX_EXEC, GRAPH_EXEC, SECURE_EXEC, PARALLEL_EXEC; instruction carries Target: Software|Accelerator.

### Compiler models (RFC-0027…0033 drafts + reviews)

**CIRModule (RFC-0028 §3):** { Identity, CognitiveTypes, Graphs: {GoalGraph, PlanGraph, EffectGraph, CapabilityGraph, MemoryAccessGraph}, Operations: [Observe, Infer, Remember, Plan, Execute, Reflect, Checkpoint], Constraints: {CapabilityRequirements, ResourceRequirements, DeterminismRules} }; graphs MUST be DAGs unless cycles explicitly declared/handled. **CIROperation ([150]):** { OperationID, Type, Inputs, Outputs, Preconditions, Postconditions, RequiredCapabilities, Effects, MemoryAccess, ResourceEstimate, Provenance }; ReplayMode: EXACT | DETERMINISTIC | RECORDED_INPUT | NON_REPLAYABLE. **CIR-SER binary structure (RFC-0029 §3):** Magic Number (4 bytes, e.g. 0x43495231 "CIR1") + Format Version (2 bytes) + ModuleID (16 bytes UUID) + Version (2 bytes) + CognitiveTypes + Graphs + Operations + Constraints + Metadata + Signature (optional); little-endian, no padding, canonical ordering, no implicit coercion; graphs serialized as node list (stable IDs) + edge list (source/target) + versions. **CIRModuleArtifact ([152]):** Header { Magic, FormatVersion, ModuleID, ModuleVersion } + SemanticLayer + ExecutionLayer + MetadataLayer { SourceProvenance, CompilerIdentity, BuildInformation, TraceReferences } + IntegrityLayer { Hash, Signature, Attestation }. **OptimizationPass (RFC-0030 [154]):** { InputCIR, Preconditions, Transformation, OutputCIR, SemanticGuarantees, CapabilityImpact, TraceImpact, ReplayGuarantees }; pass categories: Simplification, Capability Minimization, Effect Scheduling, Memory Optimization, Resource Optimization, Determinism Strengthening; legality rules: MUST NOT violate effect ordering / increase capabilities without policy / alter goal satisfaction semantics; MUST preserve replay traces. **COIL operations (RFC-0031 §3):** graph transformations (MergeNodes, SplitNode, ReorderEdges), operation transformations (InlineOperation, HoistCapability, EliminateDeadOperation), constraint transformations (StrengthenConstraint, WeakenConstraint), trace operations (RecordTransformation, AttachProvenance); every operation MUST carry proof obligation preserving effect ordering/goal semantics/capability requirements/determinism. **COILTransform ([156]):** { InputCIRFragment, OperationSequence, Preconditions, VerificationConditions, OutputCIRFragment, Certificate }. **OptimizationCertificate (COC, [156]):** { CertificateID, OriginalCIRHash, OptimizedCIRHash, COILProgram, VerificationResults, CapabilityImpact, EffectImpact, TraceImpact, CompilerVersion }. **OptimizationProof (RFC-0032 §4):** { TransformationID, VerificationConditions, ProofObligations, SolverResults, TrustedComputingBase }; TCB { CIR Validator, COIL Interpreter, Proof Checker, Theorem Kernel }; prover integrations: Lean 4, Coq, Isabelle/HOL, Z3, CVC5. **CPCPF artifact structure (RFC-0033 §3):** Header { Magic Number, Format Version, ArtifactID, Creation Timestamp } + CognitiveProgram { CISA Binary, Entry Point, Metadata } + CIRSection { Serialized CIR, Graph Representations, Operation Definitions } + OptimizationHistory { COIL Transformations, Transformation Certificates, COVF Proofs } + CapabilityManifest { Required Capabilities, Declared Effects, Resource Requirements } + TraceMetadata { Execution Trace References, Replay Information, Checkpoint References } + Integrity { Cryptographic Hash, Digital Signature, Attestation (optional) }. **CapabilityManifest ([160]):** { RequiredCapabilities, AllowedEffects, MemoryAccess, ResourceRequirements }. **ArtifactID identity ([160]):** ArtifactID → CIR Hash + CISA Hash + Proof Hash + Capability Hash.

---

## Message #18 additions — ecosystem data models (msg#18 [161]–[180])

**Package model (RFC-0034 [163]):** CognitivePackage { PackageID, Name, Version, PublisherIdentity, CPCPFArtifact, Dependencies, CapabilityManifest, TrustMetadata, VerificationStatus }. PackageID { Namespace, Name, Version, ContentHash } — ContentHash computed over immutable CPCPF artifact; modification MUST produce new PackageID; example `red.cognition.navigation.path-planner@1.4.0`. PackageManifest { PackageID, Publisher, RequiredCapabilities, DeclaredEffects, ResourceRequirements, Dependencies, MinimumCVMVersion, MinimumCISARevision, VerificationLevel }. Trust levels T0–T5 (Unverified / Signature verified / CPCPF validated / Optimization proofs verified / Formally verified / Hardware-attested). PackageRevoked { PackageID, Reason, Authority, Timestamp }.

**Sandbox model (RFC-0035 [164]):** CognitiveSandbox { SandboxID, AgentID, CVMInstance, MemoryNamespace, CapabilitySet, ResourceQuota, PolicyContext, EffectGateway, TraceContext, SecurityLevel }. CapabilityGrant { CapabilityID, Subject: SandboxID, Scope, Expiration, ResourceLimit }. SandboxQuota { CPUBudget, MemoryLimit, StorageLimit, NetworkLimit, CapabilityUsageLimit, EffectLimit }. Security events: SandboxViolation, CapabilityDenied, QuotaExceeded, UnauthorizedEffectAttempt, IsolationFailure, SandboxTerminated.

**Lifecycle/deployment models (RFC-0037 [166], RFC-0042 [177], proposals [178]):** LifecycleIdentity { PackageID, ArtifactVersion, DeploymentID, RuntimeVersion, CompatibilityProfile, ProvenanceChain }. Deployment { DeploymentID, AgentID, CPCPFArtifact, SandboxID, ResourceQuota, PolicyContext, TrustLevel }. DeploymentManifest { ArtifactID, PackageID, RuntimeRequirements, CapabilityRequirements, ResourceLimits, SecurityPolicies, FederationScope, RollbackPolicy, MonitoringPolicy }. Proposed ([178]): DeploymentPolicy { SecurityPolicy, ResourcePolicy, CapabilityPolicy, UpgradePolicy, RollbackPolicy, FederationPolicy, GovernancePolicy }; DeploymentStrategy { Immediate, Rolling, Canary, BlueGreen, Shadow, Progressive }; health states { Healthy, Degraded, Recovering, Quarantined, Failed, Retired }; DeploymentEvent { EventID, ArtifactID, LifecycleStage, PreviousState, NewState, Timestamp, Actor, Authorization, Reason }; DeploymentContract { SourceDomain, TargetDomain, ArtifactID, AllowedCapabilities, ResourceQuota, Duration, FederationAgreement }.

**Economy model (RFC-0038 [167]):** primitives — Cognitive Artifact, Cognitive Capability, Cognitive Agent, Cognitive Service, Cognitive Credit (system token for computational/cognitive resource value). Marketplace functions: Publishing, Discovery, Licensing, Reputation and Attestation, Incentive Distribution, Dispute Resolution. Economic transactions MUST be event-logged with participants, terms, proofs, settlement conditions. CognitivePackage extended view ([168]): { Identity, Provenance, Proofs, Capabilities, Effects, Resources, Trust Level, Execution Constraints, Economic Rights }.

**Ownership model (RFC-0039 [169], [170]):** primitives — Cognitive Owner, Cognitive Artifact, Derivative Artifact, Capability Lineage, Intellectual Property Token. CognitiveOwnershipRecord ([170]) { ArtifactID, CreatorIdentity, CurrentOwner, OwnershipHistory, Rights, License, ParentArtifacts, ContributionGraph } — "Git history for code / copyright chain for media / package provenance, extended to cognitive systems"; lineage DAG (acyclic); creator attribution immutable; capability inheritance preserves provenance; revocation propagates. Connected graphs form a Cognitive Provenance Graph: Identity Graph / Ownership Graph / Cognitive Artifact Graph / Capability Graph / Event History DAG.

**Governance model (RFC-0040 [171], [172]):** primitives — Cognitive Organization, Governance Proposal, Voting Mechanism, Delegation, Policy Object. CognitiveOrganization { OrganizationID, Members: [AgentID], SharedGoals: [GoalID], SharedCapabilities: [CapabilityID], ActivePolicies: [PolicyObject], OwnershipStructure, GovernanceRules }; hierarchical or federated. Voting models: simple majority, weighted, quadratic, delegated; verifiable records. GovernanceEvent { ProposalID, Participants, Votes, RuleSet, Outcome, Timestamp, Provenance }. Delegation { Grantor, Delegate, Scope, Capability, Expiration, RevocationState }. CognitiveConstitution { IdentityRules, OwnershipRules, CapabilityRules, EconomicRules, GovernanceRules, EvolutionRules } — "a programmable constitution" for organizations.

**Federation model (RFC-0041 [173], [174]):** primitives — Cognitive Domain, Federation Agreement, Cross-Domain Capability, Inter-Domain Event, Trust Negotiation. CognitiveDomain { DomainID, IdentityAuthority, GovernanceModel, SupportedRFCs, SupportedCISA, CapabilityRegistry, PolicySet, TrustLevel }. FederationAgreement { AgreementID, DomainA, DomainB, AllowedCapabilities, TrustRequirements, ResourceRules, MigrationRules, Expiration }. InterDomainEvent { EventID, SourceDomain, TargetDomain, OriginalEvent, FederationAgreement, AuthorizationProof }. Federated Capability { OriginDomain, Owner, DelegationChain, TrustProof, RevocationSource }. MigrationBundle { CPCPF Artifact, Checkpoint State, Memory References, Capability Proofs, Ownership Records, Governance Approval }.

## Message #21 additions — language/library/tooling/observability/package models (msg#21 [181]–[200])

- **CLS language model** ([181]): cognitive types `goal!`, `belief!`, `plan!`, `skill!`, `memory!`, `capability!`, `effect!`, `agent!`, `checkpoint!` (initially structured blocks/objects, promotable to native types via RFC-0001 evolution path); cognitive constructs `goal/plan/belief/skill/capability [ ... ]`, `observe/infer/reflect/checkpoint ...`; grammar core productions (program/module/definition/expression/dialect-block).
- **CSL cognitive type constructors** ([183] §5): goal [target constraints? priority? deadline?] · belief [proposition confidence source timestamp] · plan [goal steps dependencies?] · skill [name spec body effects capabilities?] · capability [type scope granted-to granted-by expiration?] · effect [type target strength timestamp] · agent [identity capabilities goals beliefs] · checkpoint [agent context timestamp].
- **CSL modules** ([183] §3, [185] §5–6): mandatory `cognition.core/goal/belief/capability/effect/memory/agent` (+`plan` in v1.0 mandatory, recommended in v1.1); recommended `cognition.skill/plan/scheduler/trace/reflect/checkpoint/workflow/policy/simulation`; purity classifications per module ([185]); library profiles Core/Runtime/Distributed/Full ([185] §3); module hierarchy 23 modules ([184], [185] §13).
- **CSL standard collections** ([185] §11): GoalSet, BeliefSet, PlanSet, SkillSet, CapabilitySet; EffectGraph, GoalGraph, PlanGraph; Trace, EventDAG — MUST support deterministic iteration and hashing.
- **CSL standard error model** ([185] §8): CapabilityDenied, GoalUnsatisfied, MemoryUnavailable, CheckpointInvalid, PolicyViolation, ProofVerificationFailed, ResourceQuotaExceeded, SkillFailure, PlanFailure — all carry provenance and participate in traces (integrates RFC-0015).
- **OperationDescriptor** (proposed, [186]): { Name, Purity, EffectClass, RequiredCapabilities, SchedulerRequirements, ReplayBehaviour }.
- **ToolCapabilities** (proposed, [190]): { LSP, Debugger, ReplayDebugger, Profiler, Formatter, AICompletion, ProofAssistant } — tool capability discovery for IDEs/agents.
- **ObservabilityEvent** ([191] v1.0; [193]/[195] v1.1/v1.2): v1.0 { EventID, Timestamp, SourceService, EventType, AgentID, TraceID, CorrelationID, Payload, Provenance }; v1.1/v1.2 adds SpanID, ParentSpanID, ExecutionEpoch, DeterminismLevel, CapabilityContext, ReplaySessionID (CorrelationID dropped in v1.1+). Future split proposed: EventHeader/TraceContext/Payload/Provenance ([194]).
- **CODP metric taxonomy** ([193]/[195] §6): `cognition.agent.*`, `cognition.scheduler.*`, `cognition.memory.*`, `cognition.effect.*`, `cognition.runtime.*`, `cognition.compiler.*`.
- **CPMWS workspace model** ([197]/[199]): workspace tree { cog.toml manifest, cog.lock immutable lockfile, packages/, tests/, docs/, examples/, build/ }; workspace profiles Single/Workspace/Enterprise/Federated ([199] §3); lockfile contents incl. workspace hash + optional signature ([199] §7).
- **WorkspaceManifest / PackageManifest** (proposed normative schemas, [200]): WorkspaceManifest { WorkspaceID, Name, Version, Members[], Dependencies[], Policies, CompilerProfile, RuntimeProfile, DeploymentTargets[], Registries[] }; PackageManifest { PackageID, Name, Version, Authors, License, Dependencies[], Capabilities[], Resources, Build, Tests, Metadata }.

## Message #22 additions — package/FFI/toolchain/conformance models (msg#22 [201]–[220])

- **Canonical manifest schemas (CPMWS v1.2 §4, [201]):** WorkspaceManifest { WorkspaceID, Name, Version, Members: [PackageID], Dependencies: [PackageID], Policies: WorkspacePolicies, CompilerProfile, RuntimeProfile, DeploymentTargets: [Target], Registries: [RegistryReference] }; PackageManifest { PackageID, Name, Version, Authors, License, Dependencies: [PackageID], Capabilities: [CapabilityRequirement], Resources: ResourceRequirements, Build: BuildConfiguration, Tests: TestConfiguration, Metadata }.
- **CFFI primitives ([203]/[205]):** Foreign Function, Foreign Module, Cognitive Foreign Binding, Foreign Call Context; ForeignModule manifest { Name, Version, ABI, Language, Capabilities, Effects, Determinism, Signature (optional) } — MUST be included in CPCPF packaging.
- **CFFI classification models ([205]):** determinism classes Pure/Deterministic/ReplayRecorded/Effectful/External with replay behaviour; memory ownership Borrowed/Shared/Copied/Owned/Immutable/Pinned; ABI classes (Native C, Stable Rust, WASI Component, Red, Rebol); sandboxing levels Trusted/Sandboxed/WASM/Remote/Verified; error translation (ForeignFailure, FatalForeignFailure, ForeignTrap).
- **ForeignBinding** (proposed canonical schema, [206]): { Name, Symbol, Language, ABI, Signature, InputTypes, OutputTypes, Ownership, Determinism, EffectClass, RequiredCapabilities, AsyncStyle }.
- **CSTS models ([209]/[211]):** ToolchainManifest { Compiler, Linker, PackageManager, Runtime, Debugger, Profiler, Formatter, Linter, DocumentationGenerator, DeploymentTool, SupportedRFCs }; Capabilities { IncrementalCompilation, CrossCompilation, ReplayDebugging, DistributedBuilds, ProofVerification, WASMBackend }; Diagnostic { Severity, Code, Message, SourceLocation, Capability, Effect, SuggestedFix }; toolchain profiles Minimal/Developer/Professional/Enterprise/Full; backend targets CVM/Native/WebAssembly/LLVM (optional)/Embedded runtime.
- **ToolchainManifest extended schema** (proposed, [212]/[214]): adds Name, Version, Profiles, Capabilities, Components, Backends, Plugins, SupportedRFCs, Compatibility(Matrix), Provenance.
- **ConformanceManifest (RFC-0050 §5, [219]; final schema proposed [220]):** { ImplementationName, Version, Profile, ConformanceLevel, SupportedRFCs, OptionalFeatures, SecurityLevel, ReplayCapability, FederationCapability, RuntimeCapabilities }.
- **FFI lifecycle events** (proposed, [206]): ForeignCallStarted/Completed/Failed, ForeignReplay, ForeignModuleLoaded. **Toolchain lifecycle events** ([209]/[211]): BuildStarted/Completed/Failed, TestStarted/Completed, PackagePublished, DeploymentStarted/Completed, VerificationSucceeded/Failed.

## Message #23 additions — constitution, macro, testing, invocation models (msg#23 [221]–[240])

- **ConformanceManifest (ratified, RFC-0050 §5, [221]/[224]):** { ImplementationName, Version, Profile, ConformanceLevel, SupportedRFCs, OptionalFeatures, SecurityLevel, ReplayCapability, FederationCapability, RuntimeCapabilities } — every implementation MUST expose it; enables Registry → Conformance Scanner → Compatibility Check → Deployment Decision tooling ([222]).
- **Cognitive Epoch (ratified primitive, [221]/[224]):** smallest deterministic execution interval — Observe → Interpret → Retrieve Memory → Reason → Plan → Capability Resolution → Effect Execution → Observation Recording → Checkpoint Creation.
- **MacroExpansionRecord (RFC-0051 §7, [227]; mandatory per [228]):** { MacroName, Version, InputHash, OutputHash, ExpansionTrace, CompilerVersion, CapabilityUsage } — included in CPCPF artifacts and the global event log. Proposed companions: MacroResourceLimits { MaxExpansionDepth, MaxMemory, MaxExecutionTime, MaxGeneratedCodeSize }, MacroPackage { Name, Version, RequiredCompiler, Capabilities, Transformations, VerificationStatus }, IdentifierOrigin { UserDefined, MacroGenerated, CompilerGenerated }, macro trust levels Trusted/Verified/Approved/Restricted ([228]).
- **TestManifest (RFC-0052 §5, [231]→[233]):** { Name, Version, TestProfile, Dependencies, RequiredCapabilities, ReplayRequired, Deterministic, ExpectedEffects } + v1.2 fields RequiredRuntimeVersion, SupportedRFCs. **TestReport (RFC-0052 §6):** { TestName, Status, Duration, ReplayVerified, CapabilityChecks, EffectChecks, Coverage, TraceReference } + v1.2 fields FailureReason, VerificationCertificates.
- **CTVF verification categories:** Functional/Deterministic/Capability/Effect/Performance/Transformation/Policy; cognitive coverage metrics (goal, plan, belief-state, capability, effect, scheduler-path, replay, macro-expansion, transformation); test primitives test-goal/test-plan/test-skill/test-capability/test-replay/test-transformation ([229]).
- **AgentManifest (RFC-0053 §4.1, [238]/[239]):** { AgentID, Version, SupportedMethods, Capabilities, SupportedRFCs, RuntimeVersion, SecurityLevel, Endpoint }.
- **InvocationManifest (RFC-0053 §5, [237]→[239]):** v1.0 { AgentID, ProtocolVersion, Method, Parameters, RequiredCapabilities, ExpectedEffects, Timeout, ReplayPolicy, TraceContext }; v1.1 adds InvocationID, CallerID, Priority, Deadline, AuthenticationContext, VersionConstraints.
- **RemoteError (RFC-0053 §7.1, [238]/[239]):** { Code, Category, Message, Retryable, CapabilityViolation, TraceReference, Cause }. **CRAIP TraceContext** MUST include TraceID, ParentInvocation, Epoch, SpanID, DeterminismLevel, CapabilityContext, ReplaySessionID ([239]). Proposed: RemoteVerificationRecord { InvocationID, ReplayVerified, PolicyVerified, (Verification)Certificates }, InvocationSemantics { AtMostOnce, AtLeastOnce, ExactlyOnce }, Request/Response schemas ([238]/[240]).

## Message #25 additions — federation, coordination, knowledge, and transaction models (msg#25 [241]–[260])

- **CADFP models (RFC-0054 §4–7, [249]):** AgentRegistration { AgentManifest, RegistrationTime, LeaseDuration, HealthEndpoint, DiscoveryScopes, TrustAssertions, FederationAgreements }; DiscoveryQuery { RequiredCapabilities, RequiredRFCs, RuntimeVersion, SecurityLevel, Region, Constraints }; DiscoveryResponse { MatchingAgents: [AgentManifest], TrustAssertions, FederationContext }; FederationManifest { FederationID, Name, Version, Members, TrustDomain, DiscoveryPolicy, RoutingPolicy, SecurityPolicy, SupportedRFCs }. Proposed companions ([248]/[250]): FederationAgreement { AgreementID, FederationID, Participants, TrustLevel, SharedCapabilities, VisibilityRules, ValidFrom, ValidUntil, SignatureSet }; registry state machine Created → Initializing → Serving → Synchronizing → ReadOnly → Retired; discovery resolution pipeline (Capability/Policy/Trust/Version/Health filters → deterministic ranking).
- **CMCWP proposals ([252]):** WorkflowManifest { WorkflowID, Version, Owner, Goals, Tasks, Dependencies, Participants, RequiredCapabilities, CoordinationPolicy, RetryPolicy, TerminationPolicy }; coordination state machine Created → Planned → ParticipantsAssigned → Executing → Synchronizing → Completed (Failed/Cancelled/Suspended); task lifecycle Pending → Accepted → Executing → Completed (Rejected/Failed/Cancelled); CoordinationManifest { CoordinationID, WorkflowID, Participants, Roles, Responsibilities, VotingPolicy, ConsensusPolicy, ConflictPolicy, TimeoutPolicy }; coordination message types (WorkflowCreate/Update, TaskAssign/Accept/Reject/Complete/Fail, ProgressUpdate, CoordinationCancel/Checkpoint); role model Coordinator/Executor/Planner/Observer/Validator/Auditor.
- **CSMKSP proposals ([254]):** SharedKnowledgeObject { KnowledgeID, Namespace, Type, Value, Version, Epoch, Provenance, AccessPolicy, CreatedAt, UpdatedAt }; synchronization state machine Created → Validated → Propagated → Applied → Confirmed (Rejected/Conflicted); SubscriptionManifest { SubscriptionID, SubscriberID, Query, Filters, DeliveryPolicy, OrderingGuarantee, ReplayPolicy, Expiration }; ConflictResolutionRecord { ConflictID, KnowledgeID, CompetingVersions, ResolutionPolicy, WinningVersion, ResolutionEpoch, Resolver }; KnowledgeSnapshot { SnapshotID, Epoch, Objects, ProvenanceRoot, Hash }; consistency profiles Local/Eventual/Causal/Strong/Verified; synchronization message types and knowledge event vocabulary.
- **CDTCP models (RFC-0057 §3–7, [257]/[259]):** TransactionManifest { TransactionID, CoordinatorID, Participants, IsolationLevel, RequiredCapabilities, ExpectedEffects, Timeout, ReplayPolicy, TraceContext, CompensationPlan, VersionConstraints }; protocol messages BeginTransaction/JoinTransaction/Prepare/Prepared/Commit/Committed/Abort/Aborted/Compensate/Compensated/Heartbeat/Status; TransactionLogEntry { TransactionID, ParticipantID, Phase, Timestamp, Epoch, Effects, Decision, TraceReference }; transaction event vocabulary (TransactionCreated…TransactionArchived). Proposed companions ([258]/[260]): VerificationArtifact { TransactionID, ReplayHash, DeterminismResult, IsolationResult, CompensationResult, Coverage }; TransactionError { Code, Category, Retryable, Participant, Phase, Cause, TraceReference }; extended manifest with Priority/Deadline/PolicyContext/RetryPolicy; read-only participant path Prepare → ReadOnly → Archived.

## Message #26 additions — transaction, wire, and security models (msg#26 [261]–[280])

- **CDTCP v1.3 models ([261]/[263]/[265]):** TransactionManifest (14 fields incl. Priority, Deadline, RetryPolicy, VersionConstraints); wire schemas Prepare { TransactionID, Epoch, ParticipantID, ManifestHash }, Prepared { …, Vote: Commit | Abort }, Commit { TransactionID, Epoch, DecisionProof }, Abort { …, Reason }, Compensate { …, CompensationPlan }; TransactionLogEntry; TransactionError { Code, Category, Retryable, Participant, Phase, Cause, TraceReference }; isolation levels Read Uncommitted/Read Committed/Repeatable Read/Snapshot/Serializable; failure matrix; conformance profiles Minimal/Developer/Professional/Enterprise/Verified. Review-proposed companions: CoordinatorElectionPolicy, TransactionVerificationReport { ReplayHash, Coverage, IsolationProof, CompensationProof, ManifestHash }, error code enumeration, commit acknowledgement flow ([262]/[264]/[266]).
- **CTWP v1.2 models ([275]):** CDTPEnvelope { MagicNumber, ProtocolVersion, MessageType, Flags, MessageID, TransactionID, Epoch, SenderID, CoordinatorID, TraceContext, PayloadLength, Payload, IntegrityBlock }; message type registry (0x0001 BeginTransaction … 0x000C Status, 0x00FF Error); flag bit layout; ClientHello { SupportedMajorMin/Max, SupportedMinorMin/Max, SupportedFeatures, SupportedEncodings, NodeID } / ServerHello { SelectedVersion, SelectedEncoding, SelectedSecurityProfile, SessionID }; encoding profiles; MessageSequence { TransactionID, SenderID, Epoch, SequenceNumber }; ReplayProtection { Nonce, SequenceNumber, Epoch, SessionID }; wire error codes 0x0001…0x0009 (InvalidManifest…VersionNegotiationFailed). Review-proposed companions: cryptographic profiles (Minimal CRC32C / Secure SHA-256+Ed25519 / Enterprise SHA-512+PQ), FrameLength vs PayloadLength clarification ([270]/[272]/[274]).
- **CTSTP models ([279]; v1.1 proposal [280]):** v1.0: cryptographic identity requirements, integrity mechanisms, replay protection, trust model, secure channel properties. v1.1 proposal: CognitiveIdentity { IdentityID, IdentityType, PublicKey, AlgorithmProfile, Issuer, ValidFrom, ValidUntil, Capabilities, TrustLevel, AttestationReference }; AuthenticationResult { IdentityID, Status, TrustLevel, Capabilities, SessionID, TraceReference }; IntegrityBlock { Algorithm, Hash, Signature, KeyReference, Timestamp, Nonce }; Signature { Algorithm, SignerID, SignatureValue, KeyID }; AuthorizationDecision { Allowed, Denied, Reason, PolicyReference, CapabilityReference }; TransactionSecurityContext { TransactionID, CoordinatorIdentity, ParticipantIdentities, GrantedCapabilities, SecurityPolicy, TrustLevel, SessionKeys, AuditReference }; ReplayProtection { SessionID, Epoch, SequenceNumber, Nonce, Expiration }; Attestation { SubjectID, Measurement, Evidence, Issuer, Timestamp }; security events vocabulary; security failure matrix; conformance profiles Minimal/Developer/Professional/Enterprise/Verified.

## Message #27 additions — execution, security, and bytecode models (msg#27 [281]–[300])

- **CVM-IESS models (RFC-0060, ratified):** ExecutionContext, ExecutionQuantum { ContextID, StartInstruction, InstructionCount, SchedulerEpoch, Deadline, YieldReason }, YieldState { InstructionPointer, Registers, MemoryReference, TransactionState, TracePosition }, CVMCheckpoint { ContextID, InstructionPointer, RegisterState, MemorySnapshot, TransactionReference, SchedulerEpoch, TraceReference }, InstructionExecuted/ InstructionLifecycleEvent trace events; CVMExecutionState machine (CREATED/READY/RUNNING/BLOCKED/WAITING_TRANSACTION/WAITING_CAPABILITY/COMMITTING/COMPLETED/FAILED/TERMINATED); instruction atomicity levels (PURE/LOCAL/EFFECT/EXTERNAL/IRREVERSIBLE).
- **CISA-RA models (RFC-0061, ratified):** Register { Type, Value, Version, Provenance }; RegisterType { Scalar, Boolean, Integer, Float, Vector, Tensor, Reference, Capability, Effect, BeliefRef, GoalRef, MemoryRef, PlanRef }; CISAInstruction { InstructionID, EncodingVersion, Opcode, Flags, OperandCount, Operands[], EffectClass, CapabilityRequirement, TraceMetadata }; Operand { OperandType, Size, Value } with type IDs 0x01–0x09; OpcodeRegistry { Opcode, Name, Version, InputTypes, OutputTypes, EffectClass, CapabilityRequired }; EffectDescriptor { EffectID, InstructionID, CapabilityRequired, TransactionID, DeterminismClass, CompensationHandler }; VerificationResult { Valid, Errors[], RequiredCapabilities[], EffectSummary }; opcode ranges 0x0000–0xFFFF by family.
- **CTSTP models (RFC-0059, ratified):** IntegrityBlock { Algorithm, Hash, Signature, KeyReference, Timestamp, Nonce }; AuthorizationDecision { Allowed, Denied, Reason, PolicyReference, CapabilityReference }; TransactionSecurityContext { TransactionID, CoordinatorIdentity, ParticipantIdentities, GrantedCapabilities, SecurityPolicy, TrustLevel, SessionKeys, AuditReference }; TrustLevel enumeration (UNKNOWN/BASIC/VERIFIED/ATTESTED/FORMALLY_VERIFIED, proposed [290]); security events vocabulary (IdentityVerified…SecurityPolicyViolation).
- **CVM-BF models (RFC-0062, draft):** CVMBytecodeHeader { Magic, FormatVersion, MinimumRuntimeVersion, ProgramID, ProgramHash, EntryPoint, SectionCount }; instruction binary layout (Opcode 2B, InstructionID 8B, Flags 2B, OperandCount 1B, Operands, EffectInfo); Operand { Type, Length, Value } with type IDs 0x01–0x06; ConstantPool { Strings, Numbers, Symbols, TypeDescriptors, CognitiveObjects }; RegisterMetadata; EffectManifest { EffectID, RequiredCapability, TransactionMode, CompensationHandler }; VerificationMetadata { TypeSafetyHash, CapabilityRequirements, ControlFlowHash, ReplayHash }; DebugInfo; opcode assignments (0x0001 NOP … 0x0803 POLICY_CHECK).

---

## Message #29 additions — formal machine state, bytecode identity, and supply-chain models (msg#29 [301]–[320])

> Provenance: corpus message #29 ([301]–[320]); verbatim archives `sources/message-029-original-part1..5.md`; scaffolds in `rfcs/`.

- **Formal CVM state** (RFC-0063, [305]/[306]): v1.0 CVMState { Registers: Map<RegisterID, Value>, Memory: Map<MemoryReference, Value>, EffectBuffer: List<Effect>, TransactionContext: Option<TransactionID>, CapabilityContext: Set<CapabilityID>, Trace: List<TraceEvent>, InstructionPointer: Address }; v1.1 canonical state { Registers, Memory, OperandStack, InstructionPointer, CallStack, TransactionState, CapabilityState, EffectBuffer, TraceState, SchedulerState } with formal representation State = (RegisterState, MemoryState, ExecutionState, TransactionState, SecurityState, TraceState); transition `step : CVMState × Instruction → Result<CVMState, CVMError>` (total and deterministic for valid instructions); Effect { EffectID, SourceInstruction, CapabilityRequired, TransactionID, DeterminismClass, Compensation }; TransactionState { Active, Effects, CommitStatus, CompensationStack }; TraceEvent { EventID, InstructionID, PreviousStateHash, NewStateHash, EffectHash, Timestamp } forming an immutable execution proof chain (State0→Event0→State1→Event1→State2).
- **Bytecode identity & container models** (RFC-0062 v1.1, [304]): ModuleIdentity { ModuleID, Namespace, Version, CompilerID, SourceHash, BytecodeHash }; SectionHeader { SectionID, Offset, Length, Flags, Hash } with flags 0x01 Required/0x02 Signed/0x04 Immutable/0x08 Debug/0x10 Extension; CVMInstruction v1.1 { Opcode, Flags, InstructionID, EffectClass, CapabilityID, OperandCount, Operands[] } (binary: 16-bit opcode, 16-bit flags, 64-bit ID, 8-bit effect, 32-bit capability, operand count, operands; little endian, no alignment padding); instruction flags bit 0 Pure … bit 6 Experimental (7–15 reserved); Operand v1.1 { OperandType, Flags, Length, Payload }; RegisterMetadata { RegisterID, RegisterClass (G/M/C/T/S), RegisterType, AccessMode (Read/Write/ReadWrite/Immutable) }; CapabilityRequirement { CapabilityID, Permission, SecurityLevel, TransactionRequirement }; EffectDeclaration { EffectID, EffectClass (PURE/LOCAL/TRANSACTIONAL/EXTERNAL/IRREVERSIBLE), DeterminismClass, CompensationRequired, CapabilityRequired }; HashDomain { FormatID, Version, SectionID, Payload }; SignatureBlock { Algorithm, PublicKeyID, Signature, CertificateChain }; ReplayState { BytecodeHash, RegisterState, MemoryState, SchedulerEpoch, TransactionState, SecurityState, EventLogPosition }.
- **CPCPF artifact model** (RFC-0065, [309]): CPCPF { Header { Magic Number, Format Version, ArtifactID, Creation Timestamp }, CognitiveProgram { CISA Binary, Entry Point, Metadata }, CIRSection { Serialized CIR (RFC-0029), Graph Representations, Operation Definitions }, OptimizationHistory { COIL Transformations, Transformation Certificates, COVF Proofs }, CapabilityManifest { Required Capabilities, Declared Effects, Resource Requirements }, TraceMetadata { Execution Trace References, Replay Information, Checkpoint References }, Integrity { Cryptographic Hash, Digital Signature, Attestation (optional) } }; recommended CognitiveArtifactIdentity { ArtifactID, ContentHash, CompilerID, CompilerVersion, SourceHash, CIRHash, BytecodeHash, ProofHash } ([310]).
- **Compiler models** (RFC-0064 recommended v1.1, [308]): CompilerState { SourceArtifact, CurrentIR, PassHistory, TransformationLog, ProofCertificates, CapabilitySummary, EffectSummary, CompilerVersion }; Pass { PassID, InputRepresentation, OutputRepresentation, TransformationRule, Preconditions, Postconditions, Certificate }; CapabilityFlow { Requested, Granted, Consumed, Produced } with proof obligation ProducedCapability ⊆ DeclaredCapability; VerifiedArtifact { Bytecode, CompilerIdentity, CompilerVersion, SourceHash, CIRHash, ProofCertificate, CapabilityManifest, EffectManifest, Signature }.
- **Registry & package models** ([312]/[313]): RegistryState { PackageIndex, ArtifactStore, VerificationDatabase, PublisherIdentityStore, TrustGraph, RevocationRegistry, AuditLedger }; PackageID = Hash(CPCPF Artifact + Dependency Graph + Compiler Version + Proof Set); CognitivePackageManifest { package_id, name, version, artifact_hash, required_capabilities, declared_effects, resource_profile, minimum_cvm_version, proof_level, publisher_identity }; lockfile `cognitive.lock` with content-hash dependency entries and verification level.
- **Build models** (RFC-0068, [314]): BuildGraph { Nodes: Package/Module/Resource/Test; Edges: Dependency/Capability/BuildOrder } (DAG, deterministic traversal, serializable); BuildProfile { Name, OptimizationLevel, VerificationLevel, TargetCVMVersion, TargetCISARevision, SecurityProfile, ReproducibilityMode }; CacheEntry { InputHash, CompilerHash, EnvironmentHash, OutputArtifactHash, VerificationStatus }; BuildMetadata { BuildID, SourceHash, LockfileHash, CompilerVersion, CompilerHash, EnvironmentHash, Timestamp, BuilderIdentity }; BuilderNode { Identity, Capabilities, TrustLevel, HardwareProfile, VerificationSupport }; BuildReceipt { BuildID, WorkspaceHash, ArtifactHash, CompilerHash, VerificationHash, BuilderIdentity, CompletionEvent }.
- **Deployment models** (RFC-0069, [315]/[316]): DeploymentManifest { ArtifactID, PackageID, RuntimeRequirements, CapabilityRequirements, ResourceLimits, SecurityPolicies, FederationScope, RollbackPolicy, MonitoringPolicy }; recommended CognitiveDeploymentUnit { DeploymentID, ArtifactID, AgentID, RuntimeInstanceID, CVMVersion, CapabilityProfile, ResourceProfile, LifecycleState, CheckpointReference, ProvenanceChain }; LifecycleState enum CREATED…RETIRED; RuntimeHealth { ExecutionHealth, MemoryHealth, CapabilityHealth, SecurityHealth, TransactionHealth, ReplayHealth }; MigrationContract { SourceVersion, TargetVersion, StateMapping, ValidationRules, RollbackCheckpoint }; Deployment Security Context { Identity, Attestation, CapabilitySet, PolicySet, SandboxProfile, TrustLevel }.
- **Coordination models** (RFC-0071, [319]/[320]): CRCP primitives Runtime Node / Orchestration Message / Lease / Heartbeat / Topology Update / Coordination Decision; message families per section 5; recommended CRCPMessage { Version, MessageType, MessageID, SenderNode, ReceiverNode, Epoch, LogicalClock, CapabilityToken, Payload, Signature } and error codes CRCP-0001 UnknownNode … CRCP-0006 ReplayViolation ([320]).

---

## Message #30 additions — CRCP wire models (msg#30 [321]–[340])

> Provenance: corpus message #30 ([321]–[340]); verbatim archives `sources/message-030-original-part1..5.md`; scaffolds in `rfcs/`.

- **Unified wire frame / envelope** (RFC-0072 v1.6, [335] §3): Magic Number (0x43524350 "CRCP", 4 bytes) · Protocol Version (uint8 major, uint8 minor) · Message Length (uint32 — number of bytes following this field through the end of IntegrityBlock) · Message Type (uint16) · Flags (uint16) · MessageID (16 bytes UUIDv7) · SourceNodeID (UUID128) · TargetNodeID (UUID128) · Epoch (uint64) · SequenceNumber (uint64) · TraceContext (variable, see below) · Payload (variable) · IntegrityBlock (variable). Little-endian, no padding, canonical ordering, explicit length prefixes.
- **CRCPEnvelope** ([323] §4): logical envelope { MagicNumber, ProtocolVersion, MessageType, Flags, MessageID, SourceNodeID, TargetNodeID, Epoch, SequenceNumber, TraceContext, PayloadLength, Payload, IntegrityBlock } — unified with the frame from v1.5.
- **Message type registry** ([321] §4 / [335] §4): RuntimeAnnouncement 0x0001, RuntimeQuery 0x0002, RuntimeResponse 0x0003, OrchestrationRequest/Response/Decision 0x0010–0x0012, LeaseRequest/Grant/Revoke/Renewal 0x0020–0x0023, Heartbeat/HeartbeatResponse 0x0030–0x0031, TopologyUpdate/Acknowledgement 0x0040–0x0041, FailureNotification/RecoveryRequest/RecoveryResponse 0x0050–0x0052, Error 0x00FF; reserved 0x8000–0x8FFF Experimental, 0x9000–0xFFFF Private/Vendor-specific. Payload schemas for each type remain an open item ([336]/[338]).
- **Handshake models** ([333]/[335] §6): ClientHello { SupportedMajorMin/Max (uint8), SupportedMinorMin/Max (uint8), SupportedFeatures (uint32 bitmap), SupportedEncodings (uint32 bitmap), NodeID (UUID128) }; ServerHello { SelectedVersion (uint16), SelectedEncoding (uint32), SelectedSecurityProfile (uint32), SessionID (UUID128) }.
- **TraceContext** ([333]/[335] §8): { TraceID (UUID128), SpanID (uint64), ParentSpanID (uint64), ReplaySessionID (UUID128), CorrelationID (UUID128) }.
- **IntegrityBlock** ([333]/[335] §9): { AlgorithmID (uint16), HashLength (uint16), Hash (variable), SignatureAlgorithm (uint16), SignatureLength (uint16), Signature (variable) }.
- **MessageSequence / ReplayProtection** ([323]/[335] §12–13): MessageSequence { SourceNodeID (UUID128), TargetNodeID (UUID128), Epoch (uint64), SequenceNumber (uint64) }; ReplayProtection { Nonce (uint64), SequenceNumber (uint64), Epoch (uint64), SessionID (UUID128) }.
- **ErrorMessage** ([333]/[335] §14): { ErrorCode (uint16), Severity (uint8), Message (UTF-8 string), RelatedMessageID (UUID128), Retryable (bool) }; codes 0x0001 UnknownNode, 0x0002 CapabilityDenied, 0x0003 LeaseExpired, 0x0004 InvalidEpoch, 0x0005 TopologyConflict, 0x0006 ReplayViolation, 0x0007 VersionNegotiationFailed.

---

## Message #32 additions — CISA-RA divergent machine model; CVM-BF v1.2/v1.3 wire models (msg#32 [361]–[380])

> Provenance: corpus message #32 ([361]–[380]); verbatim archives `sources/message-032-original-part1..5.md`; scaffolds in `rfcs/`.

- **CVM machine model (archived RFC-0061 v1.0 variant [369], D-102):** CVM { Register File, Operand Stack, Local Memory, Shared Memory Interface, Effect Buffer, Transaction Context, Security Context, Trace Context }; R0–R31 general-purpose registers, each Register { Type, Value, Version, Provenance }; special registers PC/SP/FP (CVM), TX/CAP (Runtime), TRACE (Trace Engine), EPOCH (Scheduler), FLAGS (CVM); cognitive registers BR0–BR7/GR0–GR7/MR0–MR7; EffectDescriptor { EffectID, InstructionID, CapabilityRequired, TransactionID, DeterminismClass, CompensationHandler } buffered until transaction commit; memory spaces Local (no tx) / Working (optional) / Shared (required); verification pipeline Decode→Opcode Validation→Operand Validation→Capability Check→Transaction Check→Execute with `InstructionVerificationFailed`; `cog cvm inspect/registers/trace/disassemble/replay` introspection. The ratified RFC-0061 remains v1.2 per [299]/[301].
- **CVM-BF v1.2/v1.3 wire models ([375]/[377]; scaffolded from [377]):** CVMHeader { MagicNumber (4 bytes), FormatVersion (2 bytes), MinimumRuntimeVersion (2 bytes), ModuleID (16 bytes UUID128), Flags (4 bytes), SectionCount (2 bytes), EntryPoint (8 bytes), IntegrityHash (32 bytes SHA-256) }; SectionEntry { SectionID (2 bytes), Offset (8 bytes), Length (4 bytes), Flags (2 bytes), Hash (32 bytes SHA-256) } — sorted by SectionID ascending (v1.3); instruction encoding with typed fields (uint16 Opcode/Flags, uint64 InstructionID, uint8 EffectClass/OperandCount, optional uint32 CapabilityID); magic 0x43564D58 "CVMX".
- **[380] final-review amendments (accepted pending incorporation):** FormatVersion { Major:uint8, Minor:uint8 } with compatibility rules; SectionDirectory { SectionCount, SectionEntry[] } (unique IDs, no overlap, unknown-critical rejection); byte-packed instructions without alignment; Operand { Type:uint8, Length:uint16, Value }; Constant { Type:uint8, Length:uint32, Value } with canonical encodings; IntegrityBlock { AlgorithmID, ContainerHash, SignatureType, Signature, CertificateReference } (SHA-256 minimum); ReplayState { BytecodeHash, RegisterState, MemoryState, SchedulerEpoch, TransactionContext, SecurityContext }; 11-step loader validation pipeline.

---

## Message #33 additions — formal semantics variants; verified-compilation & supply-chain models (msg#33 [381]–[400])

> Provenance: corpus message #33 ([381]–[400]); verbatim archives `sources/message-033-original-part1..5.md`; scaffolds in `rfcs/`.

- **CVM-FOS divergent v1.0 model ([384], D-105; archived):** execution ⟨S,I⟩→⟨S',E⟩; CVMState { Registers, Stack, Memory, ProgramCounter, TransactionContext, CapabilityContext, SchedulerContext, TraceContext, EffectBuffer, SecurityContext }; S = (R,M,PC,TX,CAP,SCH,TRACE,EFF,SEC); register map R : RegisterID→Value with update R' = R[r↦v]; fetch I = Memory[PC], PC' = PC + sizeof(I); memory domains Local/Working/Shared (Shared writes MUST generate transaction metadata); Effect { ID, Instruction, Capability, Transaction, DeterminismClass }; replay equivalence on (BytecodeHash, InitialState, SchedulerHistory, TransactionHistory) → (FinalState, EffectLog). The ratified model remains v1.1 per [306]/[385].
- **CCC-VTP ratified model ([389]/[391]):** pipeline CLS→Parser→CIR→COIL→COVF→CISA→Binary Encoding→CPCPF packaging; theorems: semantics(stage(program)) = semantics(program); required_capabilities(compile(P)) ⊆ required_capabilities(P); observable_effects(compile(P)) = observable_effects(P); deterministic(P) ⇒ deterministic(compile(P)); Trusted Computing Base (trusted kernel vs untrusted optimizer/frontend/codegen/sources); TransformationCertificate per pass.
- **CPCAVP artifact model ([395]; refinements [396]):** CPCA container: Artifact Magic/Version/Identity, Source Manifest, CIR Section, Proof Certificate Section, CISA Section, CVM Bytecode Section, Capability Manifest, Effect Manifest, Security Attestation, Replay Metadata, Integrity Block; ArtifactIdentity { ArtifactID (UUID128), ContentHash/SourceHash/CIRHash/BytecodeHash/ProofHash (SHA-256), CompilerID, CompilerVersion }; ProofCertificate { SemanticProof, TypeSafetyProof, CapabilityProof, EffectProof, DeterminismProof, VerificationKernelID }; SecurityAttestation { SignerIdentity, Signature, TrustChain, PolicyProfile, CapabilityApproval }; ReplayMetadata { InitialStateHash, SchedulerProfile, RuntimeVersion, TransactionModel, DeterministicSeed }; verification pipeline Integrity→Proof→Capability→Effect→Replay→CVM Load (failing artifacts MUST NOT execute in Verified profiles); proposed: ArtifactSectionEntry, ProofGraph, VerificationProfile, Provenance.
- **CARTDP registry model ([397]; refinements [398]):** registry = Artifact Index + Artifact Storage + Verification Service + Trust Database + Audit Ledger (RFC-0018); ArtifactID = SHA256(CPCAVP Content); lockfile CognitiveLock { RootArtifact, DependencyGraph, ArtifactIDs[], CapabilityResolution, TrustDecisions, RegistrySnapshotHash }; proposed ArtifactRecord, operations REGISTER/PUBLISH/QUERY/FETCH/VERIFY/INSTALL/REVOKE/MIRROR/SYNC, TrustDomain { DomainID, RootAuthority, AllowedCapabilities, VerificationPolicy, FederationRules }, RegistryEvent { EventID, Timestamp, Actor, Operation, ArtifactID, Result, PreviousStateHash }.
- **CDLMP deployment model ([399]; refinements [400]):** DeploymentManifest { ArtifactID, PackageID, RuntimeRequirements, CapabilityRequirements, ResourceLimits, SecurityPolicies, FederationScope, RollbackPolicy, MonitoringPolicy }; lifecycle event per transition; migrations checkpointed and executed within RFC-0057 transaction boundaries; proposed DeploymentState machine, AdmissionCertificate { ArtifactHash, RuntimeHash, PolicyEvaluation, CapabilityApproval, ResourceReservation, SchedulerApproval }, DeploymentGroup { GroupID, Nodes[], ConsistencyMode, SynchronizationPolicy, FailureStrategy }, LifecycleAuthority { OwnerID, DeploymentAuthority, UpgradeAuthority, RetirementAuthority }, LifecycleEvent { EventID, ArtifactID, PreviousState, NewState, Actor, Timestamp, PolicyContext, Result }.

---

## Message #34 additions — governance, evolution, resilience, sovereignty, federation models (msg#34 [401]–[420])

> Provenance: corpus message #34 ([401]–[420]); verbatim archives `sources/message-034-original-part1..5.md`; scaffolds in `rfcs/`.

- **Governance models ([401]/[402]):** GovernanceDecision { DecisionID, DecisionType, Subject, Action, PolicyReference, CapabilityContext, Timestamp, Provenance } (immutable, event-logged, replayable); proposed GovernanceState (Evaluating…Completed), PolicyEvaluation, GovernanceAuthority, GovernanceMode (Autonomous/Supervised/Restricted/Emergency), SafetyConstraint.
- **Decision ledger models ([403]/[404]):** GovernanceDecisionRecord { DecisionID, Timestamp, DecisionType, Subject, Action, PolicyReference, CapabilityContext, ResourceContext, Provenance, TraceReference }; ledger tiers Operational/Policy/Resource/Audit; LedgerQuery determinism (Query(Ledger, Request) = Same Result Set); proposed LedgerEntry, LedgerIntegrity { PreviousHash, EntryHash, MerkleRoot, VerificationProof }, DecisionExplanation, LedgerLifecycle.
- **Evolution models ([405]/[406]):** OptimizationProposal { ProposalID, TargetComponent, CurrentVersion, ProposedChange, ExpectedBenefit, RiskAssessment, EvidenceReference, RequiredCapabilities, RollbackPlan }; ImprovementEvidence { EvidenceID, Metrics, BaselineState, ExperimentalState, ReplayResults, ConfidenceLevel, VerificationReference }; evolution state Proposed→…→Accepted/Rolled Back; RollbackPlan { PreviousVersion, CheckpointReference, StateHash, CompensationEffects, RecoveryProcedure }; proposed EvolutionArtifact.
- **Simulation models ([407]/[408], archived):** DigitalTwin { RuntimeVersion, CVMModel, SchedulerModel, MemoryModel, CapabilityModel, EventModel, InitialState, DeterministicSeed }; SimulationScenario { ScenarioID, InitialStateHash, InputEvents, WorkloadProfile, PolicyVersion, CapabilityContext, ExpectedProperties }; EvaluationResult { PerformanceDelta, ResourceDelta, SafetyImpact, CapabilityImpact, ReplayDifference, ConfidenceScore }; fidelity levels L0–L4; SimulationAttestation; PromotionDecision.
- **Recovery models ([409]/[410], archived):** failure taxonomy (instruction/transaction/scheduler/agent/system); FailureDetectionEvent { FailureID, FailureClass, Component, ExecutionContext, StateHash, TraceReference, Severity }; DiagnosisRecord (root cause, contributing events, recommended actions, ConfidenceScore); RecoveryAction { RecoveryID, Preconditions, Operations, RequiredCapabilities, TargetStateHash, VerificationMethod }; FailedState + RecoveryAction = VerifiedState; RecoveryAssessment confidence profiles (High automatic / Medium simulated-first / Low escalation).
- **Security models ([411]–[414]):** SecurityEvent { EventID, ThreatCategory, SourceComponent, CapabilityContext, PolicyReference, Severity, EvidenceHash, TraceReference }; DefenseAction (canonical per [414]: ActionID, TriggerEvent, ThreatCategory, Preconditions, RequiredCapabilities, TargetComponents, ExpectedEffects, RollbackPlan, VerificationResult); IncidentRecord { IncidentID, DetectionTimestamp, ThreatIndicators, AffectedComponents, DefenseActionsTaken, ResolutionStatus, Provenance }; ThreatCategory taxonomy (UnauthorizedCapabilityUse, PolicyViolation, IdentityCompromise, ArtifactTampering, ReplayAttack, ResourceExhaustion, BehaviorAnomaly, SupplyChainViolation); response levels S0–S5; security invariants (authorization, capability confinement, provenance, event-log integrity, replay consistency, artifact integrity).
- **Sovereignty models ([415]/[416]):** classifications Public/Internal/Confidential/Restricted/Sovereign (immutable unless governed); DataOwnershipRecord (proposed: ObjectID, Creator, Owner, Custodian, GoverningAuthority, DelegatedRights); governed memory classes (Working/Episodic/Semantic/Procedural/Governance); AccessDecision { DecisionID, ObjectID, Subject, RequestedOperation, CapabilityContext, Classification, Decision, PolicyReference, Provenance }; information lifecycle Create→…→Retire; retention Active→Archived→Retained→Cryptographically Erased; synchronization modes Local-only/Owner-approved/Domain/Federated/Public.
- **Federation models ([417]/[419]):** FederationAgreement { AgreementID, ParticipatingDomains, SharedCapabilities, KnowledgeSharingRules, CollaborationPolicies, TrustRequirements, DisputeResolutionMechanism, TerminationConditions, Version }; lifecycle Proposal→Negotiation→Verification→Agreement→Activation→Operation→Suspension→Termination; FederationTrust { DomainID, TrustLevel, TrustEvidence, CertificateChain, RevocationStatus, ValidityPeriod }; KnowledgeExchange { ExchangeID, SourceDomain, DestinationDomain, KnowledgeObjects, Classification, ProvenanceReference, AgreementReference, CapabilityContext, IntegrityProof }; KnowledgeView; FederationEvent { EventID, AgreementID, Domains, EventType, Subject, Outcome, Provenance, Timestamp }; sovereignty invariants (ownership/provenance/classification/delegation/federation-boundary/replay).
