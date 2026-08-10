# Requirements Traceability Matrix (RTM) — Phase 4.2

> Master Source: `docs/TRACEABILITY-ARCHIVE.md` §4.2. Every REQ carries **Origin | Evolution | Component | Verification | Depends On | Status**.

| REQ ID | Requirement (shall) | Origin (Message+RFC) | Derived Architecture Component | Verification Method | Depends On | Status |
|--------|---------------------|----------------------|-------------------------------|---------------------|------------|--------|
| REQ-001 | Language shall be homoiconic: plans as data inspectable/rewritable/executable via same block | MSG-01 → RFC-002/005 | Red block! + plan! type | Parser test: `do plan` after `replace` | RED-SPEC-015 dispatch | Implemented (core) / Proposed (plan! typing) |
| REQ-002 | Tool invocation shall bypass serialization, via dialect-as-capability-boundary | MSG-01 → RFC-005/006 | Dialect Engine + Capability Verifier | Dialect parse → policy check → HMAC receipt audit | Dialect compilation (compiler.r) | Proposed |
| REQ-003 | Runtime shall be event-driven with multiplexed queue (Filesystem/Network/Calendar/Git/DB/Sensors/Timers/Webhooks) | MSG-02 → RFC-003 | Event Bus & Task Orchestrator | Event injection test → scheduler dispatch → verify wake-on-event | CogOS kernel loop | Proposed |
| REQ-004 | Memory shall implement 4 parallel stores (Working/Episodic/Semantic/Procedural) with context-window paging | MSG-02 correction → RFC-003/004 | Memory Manager + Substrate | Store-routing test per CoALA classification; context eviction correctness | Working memory graph, embedding index | Proposed |
| REQ-005 | Every action shall produce verifiable Receipt (audit HMAC) via 7-stage pipeline | MSG-02 → RFC-003/007 | Capability Manager + CISA COMMIT | Execute→VERIFY→COMMIT HMAC chain; replay audit | Policy engine + provenance | Proposed |
| REQ-006 | Scheduler shall manage goals by utility (priority/deadline/dependency/confidence/cost/policies), cooperative yield | MSG-03/04/06 → RFC-004/006 | Goal Scheduler | Scheduling simulation with cooperative yield points; deadline miss rate | Cognitive kernel | Proposed |
| REQ-007 | Knowledge store shall be hybrid vector+graph with temporal validity & provenance (bi-temporal edges) | MSG-04 → RFC-004 | Knowledge Graph FS + Router | Hybrid query routing benchmark vs vector-only (36–46% multi-hop) + time-travel query | Graph DB (Graphiti) integration | Proposed |
| REQ-008 | Every observation/belief shall carry confidence with 4-dim UQ plus calibration layer | MSG-04 Analysis → RFC-004 | Uncertainty Manager | Calibrate overconfidence bias; gate action via THRESHOLD | Model provider | Proposed |
| REQ-009 | Reflection shall be dual-loop (fast self + slow critic agent) with conflict resolution & provenance | MSG-04 → RFC-004 | Reflection Engine | Divergence >0.2 triggers critic; lesson provenance checked | Multi-agent runtime | Proposed |
| REQ-010 | Skill shall be capability-gated reusable procedure with performance history | MSG-04 → RFC-004 | Skill Registry | Skill invocation → policy check + performance update | Capability analysis | Proposed |
| REQ-011 | Language shall provide 16 cognitive types with metadata (confidence, validity, source, scope) | MSG-05 → RFC-005 | Red/Cognition Type System | Typecheck `make belief! [content confidence source]` + validity interval enforcement | Red type system extension | Proposed |
| REQ-012 | Inter-layer contracts shall enforce metadata shedding/acquisition at Red/Cognition↔Red↔Red/System boundaries | MSG-05 Analysis → RFC-005 | Cognitive Pipe + Capability Binding | Compile test: cross-boundary value carries provenance before/after | Compiler pipeline | Proposed |
| REQ-013 | Compiler shall emit CIR with 4 graphs (Intent→Task→Capability→Exec) and verify acyclicity/completeness/budget | MSG-06 → RFC-006 | CIR Emitter | Topological compile test + DAG cycle detection + budget check | Planning Analysis pass | Proposed |
| REQ-014 | Compiler shall perform Intent→Effect→Capability→Planning→Optimisation passes with parallelisation detection | MSG-06 → RFC-006 | 5-pass Cognitive Compiler | Sequential→DAG speedup 1.8–3.7× measured; PGO speculative hit rate | Effect inference totality | Proposed |
| REQ-015 | Policies shall be types: dangerous capability requires compile-time proof obligation discharge | MSG-06 → RFC-006 | Capability Analysis (RHTT) | Compile fails without authorisation token for `policy: dangerous` | Dependent-type elaboration | Proposed |
| REQ-016 | CVM shall execute CISA v0.1 30 ops atomically with dual memory+execution substrates | MSG-07 → RFC-007 | CVM + CISA | Opcode conformance suite per category (Perception/Memory/Reasoning/Planning/Execution/Learning/Agent) | CIR emission | Proposed |
| REQ-017 | Heap shall allocate via semantic routing (`classify→confidence→provenance→validity→route→register`) with MemCube + write-gate + verified deletion | MSG-07 Analysis → RFC-007 | Cognitive Heap + Mnemonic Sovereignty | Allocation routing test + write-gate enforcement + deletion audit | Episodic/semantic/procedural stores | Proposed |
| REQ-018 | Attention shall compete via GWT spotlight with BROADCAST coherence to prevent stagnation | MSG-07 Analysis → RFC-007 | Attention Manager | Multi-agent sycophancy/echo-chamber regression; liveness parity | Register file (Attention) | Proposed |
| REQ-019 | Every memory shall have evidence chain `Sensor→Observation→Reasoning→Decision→Action` explainable via EXPLAIN | MSG-07 → RFC-007 | Provenance Subsystem | `EXPLAIN belief!` traces full chain + timestamp | RECALL routing | Proposed |
| REQ-020 | Curate memory via semantic GC `Relevance?→Compress→Summarise→Archive→Forget` not just free | MSG-07/08 → RFC-007/008 | Semantic GC | GC policy test: stale goal invalidation trigger | Memory manager | Proposed |
| REQ-021 | Multi-agent beliefs shall achieve MESI-like coherence, preventing collective false memory | MSG-07 Analysis → RFC-007 | SYNCHRONISE/MERGE protocol | Coherence stress: contradictory beliefs → merged consistency | Agent instructions | Open Question |
| REQ-022 | Red toolchain shall remain 1 MB, cross-compile via `-t`, hybrid static+interpreter, new lexer v2 instrumented | MSG-09 → RFC-009 | Red Core Compiler Toolchain | Binary size + target matrix test (`MSDOS`..`Android-x86`); lexer phase coverage | Red/System backend | Implemented |

## Verification Trace

**Implemented baseline (must not regress):**

- `compiler.r` (125703 B), `lexer.r` (26389 B), `red.r` (25562 B), `runtime/` libRedRT — verified against `RED-SPEC-001` §II + `RED-SPEC-015` dispatch table at `9b5b15a`.
- UTF-8 → classification → scanning lexer phases; 40+ datatype taxonomy; evaluator rule `block!` self-evaluating (use `DO`), `paren!` immediate, `word!` context lookup — golden file tests required before any cognitive change.

**Proposed — verification before promotion to Implemented requires:**

- Golden file: `agent "Repository Assistant"` (RFC-005 § Complete Example) compiles, emits CIR DAG, passes Capability Verifier, executes under CVM simulation, produces HMAC receipt (Gate A).
- Performance gate: DAG parallel dispatch achieves 1.8–3.7× wall-clock speedup vs sequential baseline (PlanCompiler empirical reference).
- Audit gates: every `EXECUTE` → `COMMIT(HMAC)` is replayable; `FORGET` verified deletion auditable per mnemonic sovereignty.

*All requirements traceable back to conversation idea → RFC → component per §02-RFC-Origin-Map.*
