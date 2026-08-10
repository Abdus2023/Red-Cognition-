# Concept Evolution Map — Phase 1

> Master Source: `docs/TRACEABILITY-ARCHIVE.md` §Phase 1 (authoritative). Each concept satisfies mandatory provenance: **Origin | Motivation | Refinement(s) | Final Representation | Status**.

## 1.01 Homoiconicity as First-Class Agent Primitive

- **Origin:** MSG-01 Thoughtful Analysis § Homoiconicity + `RED-LANG-001` core feature. Example: `plan: [parse-logs summarize archive]`, `replace plan 'summarize 'deep-summarize`, `do plan`.
- **Motivation:** Collapse `reasoning about action` vs `taking action` gap; avoid string kludges of LangChain/Python; plan is inspectable data.
- **Evolution:** MSG-05 elevated from pattern to **type system**: `plan!`/`goal!`/`belief!` as native types carrying confidence/provenance; MSG-06 validated via PlanCompiler contrast (typed Red blocks vs. untyped JSON); MSG-07 made execution unit = reasoning structure under LoT hypothesis (`RED-COG-ANALYSIS § II`).
- **Final:** Red homoiconic block = CogOS goal + CIR Task DAG node + CISA `PLAN` operand. One structure, three roles (human-readable, machine-executable, runtime-inspectable). — **RFCs:** `RED-COG-001`, `CVM-001`, `RED-COMPILER-ANALYSIS § XI` — **Status:** `Implemented` (language) / `Proposed` (cognitive types).

## 1.02 Dialect → Tool Mapping (Dialect as Capability Boundary)

- **Origin:** MSG-01 `filesystem [find %/logs/ where ...]` removes JSON schema/parser/dispatch layers.
- **Motivation:** Tool-calling pipeline in Python is 6-stage serialization overhead; dialect is parser+API+executor unified plus sandbox scope.
- **Evolution:** MSG-02 capability resolver + MSG-03 capability lookup pipeline; MSG-05 Analysis § III AgentSpec external vs dialect-embedded composability claim; MSG-06 `POLICY-AS-TYPE` theorem (policies are types, June 2025) makes dialect type checker = policy enforcer.
- **Final:** Dialect = Capability Resolver + Policy enforcement point. `Cognitive Pipe Protocol` contract: downward `goal!→plan!→function + policy check`, upward `result+confidence+provenance`. — **RFCs:** `RED-COMPILER-001 § Policies Become Types`, `RED-COG-ANALYSIS § III` — **Status:** `Proposed`.

## 1.03 Red Full-Stack Philosophy (Red + Red/System + Red/Cognition)

- **Origin:** `README.md` + `compiler.r` + `boot.red` — “strongly inspired by Rebol, broader field via native-code compiler, Red/System low-level dialect”.
- **Motivation:** Single toolchain from hardware to scripting (`red.r` CLI flags `-c -r -t` cross-compile, `-dlib`).
- **Evolution:** MSG-05 proposed upward extension (mirror of Red/System downward): `Hardware←Red/System←Red←Red/Cognition←Autonomous Multi-Agent`; MSG-06 complete vision triangle; MSG-07 extending trajectory `Machine Code→Assembly→...→Intent→Goal Programming→Cognitive Systems`; MSG-08 slogan extended “One language from hardware to intelligence”; MSG-07 synthesis table adds per-layer safety guarantee.
- **Final:** Three-layer vision table + synthesis ladder with safety dimension per layer. — **RFCs:** `RED-COG-001`, `RED-COMPILER-001`, `CVM-ANALYSIS § XI` — **Status:** `Implemented` (Red/System, Red core) / `Proposed` (Red/Cognition).

## 1.04 Ultra-Lightweight Toolchain (1 MB, Zero-Install, Cross-Compile)

- **Origin:** MSG-01 + `RED-LANG-001` “entire compiler, linker, interpreter, runtime into single 1 MB executable”.
- **Motivation:** Deployable offline local agents.
- **Evolution:** MSG-09 detailed: encapper, native compiler, linker (`PE.r/ELF.r/Mach-O.r`), preprocessor (`Loader`), lexer/scanner, Red/System compiler (`comp-dialect`), emitter (direct machine code, no IR currently), self-hosting roadmap, JIT planned but not yet implemented.
- **Final:** Implemented toolchain as described in `RED-SPEC-001 § II` diagram. — **Status:** `Implemented` (JIT `Open Question`).

## 1.05 REPL Lifecycle vs Cognitive Runtime (Event-Driven Cognition)

- **Origin:** MSG-01 `[READ]→[EVAL]→[PRINT]→LOOP` with persistent environment RAM.
- **Motivation:** REPL designed for human at keyboard, not autonomous persistence.
- **Evolution:** MSG-02 event-driven ARS: event queue (Filesystem/Network/Calendar/Git/DB/Sensors/Webhooks) → scheduler; MSG-03/04 cognitive kernel never-ends loop `Observe→Update WM→Detect→Prioritise→Plan→Execute→Verify→Learn→Observe`.
- **Final:** CogOS never-ends loop + cooperative scheduler + wake-on-event daemon model. — **RFCs:** `AGENT-ENV-001`, `COGOS-001` — **Status:** `Proposed`.

## 1.06 Scheduling Evolution (Process→Goal)

- **Origin:** MSG-02 Unix vs Agent runtime table, `Scheduler→Planner`.
- **Motivation:** “Which process gets CPU?” → “Which goal deserves attention?”.
- **Evolution:** MSG-03 ladder `Batch→Job→Time-Sharing→Process→Thread→Async→Agent→Goal`; MSG-06 `Native Goal Scheduler` with tuple `Priority/Deadline/Dependency/Confidence/Cost/Policies` + cooperative yield open problem.
- **Final:** Goal Scheduler as language feature with utility-function per task. — **RFCs:** `COGOS-001 § Evolution of Scheduling`, `RED-COMPILER-001 § Native Goal Scheduler` — **Status:** `Proposed`.

## 1.07 Four-Store Memory Model

- **Origin:** MSG-02 vertical stack (simplified).
- **Motivation:** REPL only preserves one-session variables; agent needs cross-session experiences.
- **Evolution:** **Correction MSG-02 Analysis § II** CoALA + Tulving/Baddeley/Squire + Generative Agents/MemGPT; MSG-03 MemOS MemCube; MSG-04 hybrid vector+graph + Graphiti bi-temporal; MSG-07 cognitive heap + semantic GC.
- **Final:** 4 parallel stores (Working/Episodic/Semantic/Procedural) + hybrid backend + router + bi-temporal validity. — **Status:** `Proposed` (production validation at framework level).

## 1.08 Memory Promotion Gate

- **Origin:** MSG-02 Analysis § V.5a.
- **Motivation:** Not all reflections equal; avoid over-personalisation.
- **Evolution:** MSG-03/07 `REMEMBER/COMPRESS/PROMOTE` ops; MSG-04 `invalidate-goal`; MSG-07 allocator route `classify type → assess confidence → extract provenance → set validity → route store → register lifecycle`.
- **Final:** Gate diagram `Reflection→Promotion→(Episodic/Semantic/Procedural/Discard)` + `PROMOTE` CISA instruction. — **Status:** `Proposed`.

## 1.09 Tool Invocation Pipeline (Goal→Receipt)

- **Origin:** MSG-02 7-stage.
- **Motivation:** Every action loggable/verifiable/replayable → auditability.
- **Evolution:** MSG-02 Analysis governance gap + OWASP + Microsoft toolkit; MSG-03 `Capability Lookup→Policy→Budget→Execution→Receipt`; MSG-07 `EXECUTE/SANDBOX/COMMIT with HMAC`.
- **Final:** CISA Execution instructions + Capability Verifier pass + audit HMAC receipt. — **Status:** `Proposed`.

## 1.10 Cognitive Pipeline (11-stage)

- **Origin:** MSG-02 `Observation→Perception→Understanding→Goal Matching→Planning→Scheduling→Execution→Validation→Reflection→Consolidation`.
- **Motivation:** Many stages have no REPL equivalent.
- **Evolution:** +3 inserted (Identity Verification, Confidence Scoring, Memory Promotion) + 4-dim uncertainty extension.
- **Final:** 14-stage with auxiliary gates. — **Status:** `Proposed`.

## 1.11 Capability-Based Execution

- **Origin:** MSG-05 `execute [delete %temp/]` checked permissions/policy/risk/sandbox/audit.
- **Motivation:** Least-privilege + auditability.
- **Evolution:** MSG-06 least-privilege validation + proof obligation; MSG-07 `COMMIT` write-gated, `SANDBOX` isolated, mnemonic sovereignty write-gate.
- **Final:** Policy-as-type + least-privilege compile-time check + runtime sandbox + HMAC commit. — **Status:** `Proposed`.

## 1.12 Cognitive Types (16-type System)

- **Origin:** MSG-05 11 new types `goal! plan! belief! ...`.
- **Motivation:** Not merely data — carry meaning; declarative vs imperative.
- **Evolution:** MSG-05 Analysis extended to 16: epistemic (`belief! hypothesis! evidence! observation!`), intentional (`goal! plan! intention! capability!`), temporal (`memory! skill! episode!`), normative (`policy! permission! event!`); each carries cognitive metadata.
- **Final:** Annotated Repository Assistant example with explicit `make belief! [content confidence source]`; inter-layer contracts. — **RFC:** `RED-COG-ANALYSIS § VIII–IX` — **Status:** `Proposed`.

## 1.13 Inter-Layer Contracts

- **Origin:** MSG-05 three-layer table.
- **Motivation:** Preserve philosophy per-layer abstraction.
- **Evolution:** MSG-05 Analysis specified `Cognitive Pipe Protocol` and `Capability Binding`.
- **Final:** Contract diagram in `RED-COG-ANALYSIS § IX`. — **Status:** `Proposed`.

## 1.14 Cognitive Intermediate Representation (CIR)

- **Origin:** MSG-06 `Goal→Intent→Task→Capability→Execution→Machine Code`.
- **Motivation:** Lower first to reasoning structures before instructions; enable optimisation before spending tokens.
- **Evolution:** MSG-06 Analysis grounded in IR theory + DAG Plan-and-Execute + parallel speedup 1.8–3.7×; MSG-06 full emission diagram with 4 IR layers.
- **Final:** CIR v0.1 with 4 graphs, static validation, cycle detection, parallelisation. — **Status:** `Proposed`.

## 1.15 Intent Optimisation & Planning as Compiler Pass

- **Origin:** MSG-06 6 passes `Goal Simplification→...→Scheduling`.
- **Motivation:** Optimise quality/latency/resources, not just cycles.
- **Evolution:** MSG-06 Analysis PGO speculative tool execution (PASTE) pre-warms predicted sequences analogous to LLVM PGO/JIT.
- **Final:** 6-pass optimisation + speculative pre-binding with rollback. — **Status:** `Proposed`.

## 1.16 Cognitive Effects System

- **Origin:** MSG-06 `observe! remember! modify! communicate! reason! execute! learn!` effects.
- **Motivation:** Compiler knows behavioural impact + static permission checking.
- **Evolution:** MSG-06 Analysis Effect Inference pass: derive & propagate signatures; Open Problem: termination with recursive plans.
- **Final:** Function signature extended with `effects [observe remember reason]`. — **Status:** `Proposed`.

## 1.17 Multi-Agent Runtime

- **Origin:** MSG-06 `agent planner/reviewer/...`, message passing `Proposal→Reviewer→Executor→Receipt`; MSG-07 `Planner/Reviewer/Executor/Verifier/Memory` actors.
- **Motivation:** Specialist roles > monolith; richer cognitive state than actor model.
- **Evolution:** MSG-07 Analysis multi-agent guarantees: liveness parity, capability contention arbitration, collective false memory prevention (MESI-like).
- **Final:** CISA Agent instructions `SPAWN MESSAGE SYNCHRONISE MERGE TERMINATE`. — **Status:** `Proposed`.

## 1.18 Cognitive Virtual Machine & CISA

- **Origin:** MSG-07 semantic opcodes vs arithmetic; 5 categories; registers; semantic addressing; heap.
- **Motivation:** VM becomes reasoning engine.
- **Evolution:** MSG-07 Analysis grounds via Soar/ACT-R, MemOS, GWT; complete CISA v0.1 (30 ops) + Attention ISA missing-category addition + memory security.
- **Final:** Full CISA v0.1 listing (see `CVM-001` + `CVM-ANALYSIS § IX`) + register file + dual substrates. — **Status:** `Proposed`.

## 1.19 Cognitive Heap / MemCube

- **Origin:** MSG-07 allocation `Goal Object/Observation/Plan/Memory/Evidence/Skill` with metadata.
- **Motivation:** Semantic entities with lifecycle.
- **Evolution:** MSG-07 Analysis MemCube encapsulates plaintext/activation/parameter with scheduler+lifecycle; adaptive routing + self-organising consistency; mnemonic sovereignty 9 primitives.
- **Final:** `allocate(entity)→{classify, assess, provenance, validity, route, register}` + write-gate + verified deletion. — **Status:** `Proposed`.

## 1.20 Attention Management (Global Workspace Theory)

- **Origin:** MSG-07 scoring `Importance/Urgency/Novelty/Risk→Attention Score`.
- **Motivation:** Classical OS has no attention resource.
- **Evolution:** MSG-07 Analysis formalises via LIDA/GWT spotlight + competition/broadcast, empirical cognitive stagnation; adds 5 Attention ISA ops.
- **Final:** `ATTEND COMPETE BROADCAST SUPPRESS THRESHOLD`. — **Status:** `Proposed`.

## 1.21 Provenance & Reflection-as-GC

- **Origin:** MSG-07 evidence chain + reflection `Memory→Useful?→Compress→Summarise→Archive→Forget`.
- **Motivation:** Explainability + audit + long-term coherence.
- **Evolution:** MSG-07 Analysis extends to trust & audit trail, semantic GC; MSG-04 multi-agent reflection dual-loop.
- **Final:** Per-memory evidence chain + reflection as curation GC with provenance-preserved lessons. — **Status:** `Proposed`.

## 1.22 Native Multi-Model Reasoning

- **Origin:** MSG-05 `reason using small-model/planner/verifier`.
- **Motivation:** Task-complexity/latency/privacy/cost routing with uniform interface.
- **Evolution:** MSG-03/04 model layer utility-function scheduler; MSG-06 Skill Selection; MSG-07 model engines as Execution Substrate.
- **Final:** Runtime selects tier per subtask; 6-provider swap validated (MS Agent Framework 1.0). — **Status:** `Proposed` (provider swap at framework).

## 1.23 New Lexer (Red/System, Instrumented)

- **Origin:** MSG-09 § XXVII spec: Parse-dialect lexer → Red/System for near-instant loading, scanning without loading, event-oriented instrumentation.
- **Evolution:** Documented as implemented in `lexer.r` (26389 bytes) plus Red/System rewrite trajectory.
- **Final:** Lexer v2 architecture (UTF-8→classification→scanning phases) + `transcode` native. — **Status:** `Implemented` / `Partially Implemented` (rewrite).

## 1.24 Interpreter Internals (Evaluator Dispatch)

- **Origin:** MSG-09 § XV `RED-SPEC-015` dispatch table.
- **Motivation:** Hybrid static compile + interpreter; JIT roadmap.
- **Final:** Table as spec; `runtime/` libRedRT. — **Status:** `Implemented` (interpreter) / `Open Question` (JIT).
