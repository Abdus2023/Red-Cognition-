# Architecture Decision Records (ADRs) — Phase 4.3

> Master Source: `docs/TRACEABILITY-ARCHIVE.md` §4.3. Every ADR carries **Context | Decision | Alternatives Rejected | Consequences | Evolution | Status** with mandatory Origin provenance.

---

## ADR-001 — Red as Substrate (not Python) for Cognitive Core

- **Origin:** MSG-01 Thoughtful Analysis + MSG-02 Analysis § VII — Python's stringly-typed plans vs Red blocks
- **Context:** Agent frameworks in Python suffer string manipulation gap between reasoning-about-action and taking-action; but Python has vector DB/LLM SDK ecosystem Red lacks.
- **Decision:** Use Red (homoiconic, dialects, 1 MB, Red/System) for cognitive core; bridge ecosystem via MCP gateway + FFI adapter functions rather than reimplement.
- **Alternatives Rejected:** Pure Python (rejected: composability/verifiability loss), pure Red isolation (rejected: cannot reach production memory/governance infra).
- **Consequences:** Specification elegance and compile-time verifiability gained; bridging work imposed. — **Evolution:** MSG-03/05/06 confirm via AIOS native vs non-native adapters; MSG-08 model-layer swap. — **Final:** `RED-COG-001` + `RED-COG-ANALYSIS § I` synthesis table. — **Status:** `Proposed`.

## ADR-002 — Four Parallel Memory Stores (Corrected from Vertical Stack)

- **Origin:** MSG-02 Memory Hierarchy diagram; **Corrected** by `AGENT-ENV-ANALYSIS-001 § II` (CoALA, Tulving).
- **Context:** Vertical depth hierarchy conflates stores with different access patterns (context-window-bounded working vs embedding-indexed episodic vs context-independent semantic vs compiled procedural).
- **Decision:** Replace linear stack with 4 parallel stores; add promotion gate, hybrid router, bi-temporal graph.
- **Alternatives Rejected:** Single stack (deprecated), single vector store (rejected: 36–46% multi-hop loss vs hybrid).
- **Consequences:** More precise retrieval but router + coherence complexity. — **Final:** `AGENT-ENV-001` → corrected `AGENT-ENV-ANALYSIS-001` + `COGOS-FRAMEWORK-ANALYSIS § II`. — **Status:** `Proposed`.

## ADR-003 — Capability-Based Execution with Audit Receipt

- **Origin:** MSG-02 Tool Invocation `Goal→Receipt`; MSG-03 capability pipeline.
- **Context:** Autonomous agents need least-privilege, auditable, replayable execution; classical permission checks insufficient for goal hijacking/tool misuse/identity abuse (OWASP 2025).
- **Decision:** Every action is capability-gated (`Lookup→Policy→Budget→Execution→Receipt(HMAC)`) with dialect-embedded policy types + sandbox.
- **Alternatives Rejected:** Direct syscall/exec (rejected: no audit), external policy bolt-on only (rejected: not composable per AgentSpec analysis).
- **Consequences:** Strong auditability but policy verification complexity (OP-02). — **Final:** `CVM-001` `EXECUTE/VERIFY/COMMIT/SANDBOX` + `RED-COG-ANALYSIS § III`. — **Status:** `Proposed`.

## ADR-004 — Declarative Goals (Achievement) vs Procedural Plans

- **Origin:** MSG-05 `goal analyse-log [...]`; refined by `RED-COG-ANALYSIS § IV` GOAL language.
- **Context:** `goal!` name ambiguity: satisfaction (state true) vs completion (steps executed) require different runtime semantics (verification vs exception).
- **Decision:** Type-distinguish: `achieve [repository: analysed]` (declarative, modal-logic verifiable) vs `plan analyse-log [observe ... verify]` (procedural).
- **Alternatives Rejected:** Single overloaded `goal` (rejected: verification ambiguity), pure procedural (rejected: loses declarative verification).
- **Consequences:** Verification semantics precise but type system wider. — **Final:** 16-type intentional category `goal!` (declarative) / `plan!` (procedural) / `intention!` (committed). — **Status:** `Proposed`.

## ADR-005 — CIR as Typed DAG (not Untyped JSON replay)

- **Origin:** MSG-06 DAG plans + MSG-06 Analysis PlanCompiler & growing-context cost study (3.6× tokens).
- **Context:** Production already emits untyped plans as JSON blobs with no static validation, causing 41.8% specification failures.
- **Decision:** Compile to typed, acyclic, budget-checked DAGs (Intent→Task→Capability→Exec) with topological compilation before any tool call.
- **Alternatives Rejected:** Untyped JSON/Python plans (deprecated for cost/non-determinism), sequential statement list (rejected: misses 1.8–3.7× parallel speedup).
- **Final:** `RED-COMPILER-001` CIR + `RED-COMPILER-ANALYSIS §§ II–III` performance grounding. — **Status:** `Proposed`.

## ADR-006 — Policy-as-Type (Dependent Types, Compile-Time Proof)

- **Origin:** MSG-06 `Policies Become Types`; proven `RED-COMPILER-ANALYSIS § IV` (June 2025 paper, RHTT).
- **Context:** Ad-hoc untyped policies cannot be tested/verified except by observation; access-control correctness unprovable.
- **Decision:** Encode ABAC policies as dependent types; `capability! [policy: dangerous]` requires proof-term discharge (`authorisation token`) before compilation succeeds.
- **Alternatives Rejected:** Runtime-only checks (rejected: late failure), untyped policy files (rejected: drift).
- **Challenges:** Proof granularity ergonomics (OP-02) + effect termination (OP-03) remain open. — **Status:** `Proposed` (theorem proven).

## ADR-007 — CVM Dual Substrates (Memory + Execution parallel, not sequential)

- **Origin:** MSG-07 toolchain; extended `CVM-ANALYSIS § X` correction.
- **Context:** Single OS-effects layer conflates semantic memory operations with OS I/O.
- **Decision:** Split into Memory Substrate (Episodic/Semantic/Procedural/WM) + Execution Substrate (Process/Sandbox/Network/Model/Registry) with simultaneous dispatch per CVM instruction.
- **Alternatives Rejected:** Single sequential layer (rejected: log/audit/binding would be afterthought).
- **Final:** Two-substrate diagram + allocation routing. — **Status:** `Proposed`.

## ADR-008 — GWT Attention as Safety-Critical (not Optimisation)

- **Origin:** MSG-07 Attention Management; grounded `CVM-ANALYSIS § II` via LIDA/GWT + empirical stagnation.
- **Context:** Without competition, multi-agent reasoning collapses into sycophancy/echo chambers/degeneration.
- **Decision:** Formalise attention ISA (`ATTEND/COMPETE/BROADCAST/SUPPRESS/THRESHOLD`) with GWT semantics; safety-critical classification.
- **Alternatives Rejected:** Priority queue only (rejected: no broadcast coherence), no attention primitive (rejected: safety failure).
- **Final:** CISA Attention category + coherence protocol. — **Status:** `Proposed`.

## ADR-009 — Self-Modifying Plans (not Code)

- **Origin:** MSG-06 Self-Modifying Plans.
- **Context:** Homoiconicity invites self-rewrite, but rewriting executable code risks trusted runtime corruption.
- **Decision:** Plans are data (DAG) rewritten via `reflect → improve plan → store improved plan`; runtime remains stable, knowledge evolves.
- **Alternatives Rejected:** Self-modifying code (rejected), frozen plans (rejected: no learning).
- **Final:** `RED-COMPILER-001` § Self-Modifying Plans + `LEARN/UPDATE` CISA. — **Status:** `Proposed`.

## ADR-010 — Three Compilers (Syntax/Semantic/Intent)

- **Origin:** MSG-08 Three Compilers.
- **Context:** Single compiler cannot answer `Is valid? → Does it make sense? → Does it accomplish objective?` jointly.
- **Decision:** Pipeline split: Syntax (`valid Red?`) → Semantic (`makes sense? type/binding`) → Intent (`accomplishes goal? completeness, ambiguity`).
- **Alternatives Rejected:** Single-pass compiler (rejected: verification conflation).
- **Final:** `RED-20-001` + `RED-COMPILER-ANALYSIS § IX` full pipeline. — **Status:** `Proposed`.

## ADR-011 — Mnemonic Sovereignty Write-Gate (not Content Filter only)

- **Origin:** `CVM-ANALYSIS § IV` — no system implements all 9 primitives; poisoning expands to procedural/graph/organisational.
- **Context:** Content filters alone cannot secure expanded poisoning surface; verified deletion missing.
- **Decision:** Pre-consolidation write-gate validation + verified deletion with audit trail (`COMMIT` write-gate, `FORGET` verified).
- **Alternatives Rejected:** Input filter only (rejected), lazy deletion (rejected: sovereignty violation).
- **Final:** `CISA COMMIT/FORGET/ROLLBACK` + mnemonic sovereignty. — **Status:** `Proposed`.

---

*Rejected alternatives preserved per mandatory provenance rule; each rejected option's Origin and Reason for rejection are explicit. See also `00-Research-Timeline.md §0.3` for abandoned ideas table.*
