# Future RFC Roadmap — Phase 4.8

> Master Source: `docs/TRACEABILITY-ARCHIVE.md` §4.8. Every RFC entry carries **Motivation (which OP it closes) | Depends On | Content | Priority**.

| RFC # | Proposed Title | Motivation (which OP or gap it closes) | Depends On (prior RFC + OP resolution) | Proposed Content Highlights | Priority | Est. Message Equivalent |
|-------|----------------|----------------------------------------|----------------------------------------|----------------------------|----------|-------------------------|
| **RFC-011** | Ecosystem Bridge & Adapter Specification | OP-01; AIOS native vs non-native adapter gap | RFC-005 + OP-01 scoping | FFI to MCP/LangMem/Mem0/Zep/Neo4j; adapter function ABI; DID identity; libRed extensions | **P0 (blocking)** | Would extend MSG-05/06 |
| **RFC-012** | Ergonomic Proof Elaboration Tactics for Capability Types | OP-02; Policy-as-Type adoption risk | RFC-006 + OP-02 | Agda-style elaboration or Rust-borrow ergonomics for `dangerous` proof discharge; examples per ABAC complexity tier | P1 | Would extend MSG-06 Analysis |
| **RFC-013** | Totality & Recursion Constraints for Cognitive Blocks | OP-03 | RFC-006 (Effect Inference) | Totality checker; `no recursive plan without base case` rule; termination proof obligation | P1 | Would extend MSG-06 Analysis |
| **RFC-014** | Cognitive Lock File & Recompile-on-Drift Protocol | OP-04 | RFC-006 (CIR) | Environment snapshot format (skill registry/capabilities/models); lock file schema; recompile trigger policy | P1 | Would extend MSG-06 Analysis |
| **RFC-015** | Cooperative Yield Protocol for Goal Blocks | OP-05 + OP-06 | RFC-004 (Goal Scheduler) + RFC-007 (CVM) | Explicit `yield` syntax in goal! blocks; scheduler checkpoint semantics; yield-required lint pass | P1 | Would extend MSG-04/06 |
| **RFC-016** | Goal Invalidation & Belief Coherence Protocol (MESI for Cognition) | OP-06 + OP-08 | RFC-007 (SYNCHRONISE/MERGE) + CVM Analysis § VIII | `invalidate-goal(trigger: world-state-changed)` semantics; belief coherence states `Modified/Exclusive/Shared/Invalid` adapted; anti-false-memory anchoring | P0 | Would extend MSG-07 Analysis |
| **RFC-017** | Misalignment Detection & Suppression Pre-Execution | OP-07 | RFC-004 (CogOS kernel) | Intent classifier gating; suppression policy before EXECUTE; CLTR corpus as test suite | **P0 (safety)** | New section post-MSG-04 |
| **RFC-018** | Mnemonic Sovereignty Compliance (Write-Gate + Verified Deletion) | OP-09 | RFC-007 (Heap) + CVM Analysis § IV | 9-primitive checklist; write-gate policy dialect; verified `FORGET` with cryptographic attestation | P1 | Would extend MSG-07 Analysis |
| **RFC-019** | Red JIT Compiler Specification | OP-10 | RFC-009 (Red Spec) + runtime/ | JIT tier between static compile and interpreter; profiling→tier-up policy; WASM backend interaction | P2 | Would extend MSG-09 |
| **RFC-020** | Calibrated Confidence & UQ Layer | OP-11 | RFC-004 (Uncertainty) | 4-dim UQ slots per belief!; calibration layer correcting training overconfidence; `THRESHOLD` gating semantics | P1 | Would extend MSG-04 Analysis |
| **RFC-021** | Attention Arbitration & Liveness Guarantees | OP-12 | RFC-007 (Attention) + GWT | `COMPETE/BROADCAST` arbitration protocol; liveness parity guarantee; echo-chamber regression suite | P1 | Would extend MSG-07 Analysis |
| **RFC-022** | Skill Composition Algebra (Semantic Pipes) | OP-13 | RFC-004 (Skills) | DAG composition vs byte pipes; parallel skill dispatch formal semantics; skill effect composition | P2 | Would extend MSG-04 Analysis |
| **RFC-023** | New Lexer v2 & Instrumentation API Finalisation | MSG-09 lexer spec completeness | RFC-009 + `lexer.r` | Character class table, scanning phases, `transcode` event-API final spec; performance benchmark vs Parse dialect | P2 | Would close MSG-09 open item |
| **RFC-024** | Cognitive Object Model (agent!) & Message Passing | MSG-07 § Cognitive Object Model | RFC-007 + Phase 8 roadmap | `agent! [beliefs goals memories skills policies capabilities reflection]` formal spec; message types | P2 | Would formalise MSG-07 |
| **RFC-025** | Proof-Carrying Artifact (Post-RFC-24 extension) — not yet in conversation, logical next | Drift to verified cognition | RFC-006/007 (CIR+CISA) + OP-02/04 | Artifact metadata: provenance + proof terms + HMAC + version history = verifiable cognition package | P3 (future) | Beyond MSG-09 (roadmap-derived) |

## Horizon Note

The conversation ends at MSG-09 with no “future directions” section beyond the Red 2.0 slogan “One language from hardware to intelligence.” Entries RFC-011→024 are **derived as necessary completions** of the open problems the analyses themselves identify (explicitly: OP-01→13). RFC-025 (Proof-Carrying Artifact) is flagged as *roadmap-derived* not conversation-sourced — included because `RED-COMPILER-ANALYSIS § XI` (“artefacts carry provenance/proofs/parallelism/model bindings/history”) already implies it but MSG-06 stops short of naming it.

**Sequencing recommendation:** P0 (RFC-011, 016, 017) before P1; P1 before P2; RFC-025 only after RFC-006+007 stabilise with OP-02/04 resolved.

*All future RFCs trace back to an OP in the registry or a gap explicitly listed in the corresponding `*-ANALYSIS-001` wiki file; none are speculative without provenance.*
