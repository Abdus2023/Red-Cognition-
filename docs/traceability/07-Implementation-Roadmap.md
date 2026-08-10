# Implementation Roadmap — Phase 4.6

> Master Source: `docs/TRACEABILITY-ARCHIVE.md` §4.6 & Appendix B. Every phase carries **Scope (RFCs) | Deliverables | Depends On | Effort | Status** and traces back to a wiki Stable ID.

| Phase | Title | Scope (RFCs) | Key Deliverables | Depends On | Effort Est. | Status |
|-------|-------|--------------|------------------|------------|-------------|--------|
| **Phase -1** | Baseline Verbatim Preservation | RFC-002/009 | Ensure `9b5b15a` baseline builds; verify `compiler.r` + `lexer.r` + `runtime/` vs RED-SPEC dispatch table; preserve wiki suite at `docs/wiki/` | — | Done (audit confirms `compiler.r` 125703, `lexer.r` 26389) | **Implemented** |
| **Phase 0** | Traceability Archive (this audit) | Meta | `docs/TRACEABILITY-ARCHIVE.md` + `docs/traceability/*` + README sync; git push to `arena/019fec34-red-cognition` | Wiki extraction (`9422679`) | 1 sprint | **This deliverable** |
| **Phase 1** | Red/Cognition Type System & Dialects (Language MVP) | RFC-005 | Define `goal! plan! belief! memory! skill! observation! hypothesis! policy! evidence! event! capability!` (11) → extend to 16 with metadata slots; dialect parsers `reason [...]`, `goal [...]`, `remember [...]`; inter-layer contracts stub | Red core extensions, parse dialect | 2–3 sprints | **Proposed** |
| **Phase 2** | Capability Dialects + Policy-as-Type Prototype | RFC-005/006 (Capability) | Dialect-embedded `capability! [policy: dangerous]` with least-privilege check; authorisation token prototype; HMAC receipt stub; OWASP mapping tests | Phase 1 types + FFI sandbox | 2 sprints | **Proposed** |
| **Phase 3** | CIR Emitter + Planning Analysis (DAG compiler) | RFC-006 | Sequential→DAG expansion, dependency resolution, acyclicity proof, parallelisation detection; emit 4 graphs; PlanCompiler reference integration | Phase 1–2 + compiler pipeline access | 3–4 sprints | **Proposed** |
| **Phase 4** | Intent & Effect & Optimisation Passes | RFC-006 | Intent Analysis (achievement vs procedural completeness, ambiguity detection), Effect Inference (derive `observe!` etc., call-graph propagation with totality constraint), Intent Optimisation (goal simplification, plan fusion, PGO) | Phase 3 CIR | 3 sprints | **Proposed** |
| **Phase 5** | Memory Substrate MVP (4-store + Promotion + GC) | RFC-003/004 | CoALA stores, promotion gate, semantic GC ladder, hybrid vector+graph router with Graphiti temporal edges (or mock) | Phase 1 memory! types | 3 sprints | **Proposed** |
| **Phase 6** | CVM Core (CISA subset + Registers + Heap) | RFC-007 | Implement `OBSERVE/RECALL/COMMIT/FORGET/INFER/PLAN/EXECUTE/VERIFY/REFLECT` subset; cognitive register file; heap allocator route with write-gate | Phase 3 CIR + Phase 5 stores | 4 sprints | **Proposed** |
| **Phase 7** | Attention & Provenance (GWT + Evidence Chain) | RFC-007 | `ATTEND/COMPETE/BROADCAST/SUPPRESS` + MESI-like belief coherence prototype; `EXPLAIN` provenance chain; verified deletion audit | Phase 6 CVM | 3 sprints | **Proposed** |
| **Phase 8** | Multi-Agent & Model Scheduler | RFC-006/007/008 | `SPAWN/MESSAGE/SYNCHRONISE/MERGE`; specialist agents (planner/reviewer/executor/verifier); model-tier utility scheduler (6 providers) | Phase 6–7 | 3 sprints | **Proposed** |
| **Phase 9** | CogOS Integration (Goal Scheduler + Trust Layer) | RFC-004/008 | Goal scheduler tuple `priority/deadline/dependency/confidence/cost/policies` with cooperative yield; DID-based identity; `Everything is Trust Assertion` (GTG-1002) hardening | Phase 5–8 | 4 sprints | **Proposed** |
| **Phase 10** | Red 2.0 Unification & Conformance Suite | RFC-008/009 | Intent contracts `purpose/quality/deadline/budget`; three compilers unified; Repository Assistant golden-file end-to-end; knowledge-flow/provenance verification | All prior | 3 sprints | **Proposed** |
| **Phase 11** | Ecosystem Bridging (FFI hard gate) | RFC-003 Analysis | MCP security gateway, vector DB connectors, LLM SDK bindings via `libRed`/`bridges/`; non-native adapter functions per AIOS | Phase 2 + 8 | Ongoing | **Open Question** |

## Milestone Decision Gates

- **Gate A (after Phase 2):** Can `agent "Repository Assistant"` golden file compile and produce HMAC receipt? → proves type+policy vertical slice.
- **Gate B (after Phase 5):** Hybrid store time-travel query correct? → proves memory substrate (Graphiti bi-temporal).
- **Gate C (after Phase 7):** Multi-agent echo-chamber regression passes? → proves GWT safety.
- **Gate D (after Phase 10):** 1.8–3.7× parallel DAG speedup measured vs sequential? → proves compiler value proposition (PlanCompiler empirical reference).

*Gates are fail-forward: a gate failure triggers RFC iteration, not phase advance. See OP registry for blocking open problems per phase.*

## Critical Path

`Phase 1 (Types)` → `Phase 2 (Policy)` → `Phase 3 (CIR)` → `Phase 6 (CVM)` → `Phase 9 (CogOS)` → `Phase 10 (Red 2.0)`

Cut vertex `Phase 3 / RFC-006`: delay there delays all downstream CVM/CogOS work. Parallelisation possible: Phase 5 (Memory MVP) can proceed concurrently with Phase 3/4 compiler work (separate subsystems; shared dependency only on Phase 1 types).

*Provenance: roadmap phases derived from §4.1 RFC Origin Map ordering + §06-Dependency-Graph critical path; effort estimates are relative sprints, not calendar-committed, per audit requirement to preserve reasoning not speculate delivery dates.*
