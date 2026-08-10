# Red/Cognition Traceability Suite — Index

**Master Archive:** [`../TRACEABILITY-ARCHIVE.md`](../TRACEABILITY-ARCHIVE.md) — 776-line formal auditor's report containing all phases 0–5, appendices, and mandatory provenance per item. **Start there for the complete intellectual history.**

This `docs/traceability/` suite splits the master archive's **Phase 4** ten deliverables into individually citable Markdown files (each retains Origin / Evolution / Final / Status provenance). The suite together with `docs/wiki/` (20 canonical + analysis files, 8177 lines) constitutes the formal engineering traceability archive for the 9-turn Red/Cognition research conversation.

| # | Document | Contents | Status |
|---|----------|----------|--------|
| 0 | [`00-Research-Timeline.md`](00-Research-Timeline.md) | Phase 0.1 full chronological timeline table (23 steps from Red baseline → MSG-09) + terminology evolution | Master §Phase 0 |
| 1 | [`01-Concept-Evolution-Map.md`](01-Concept-Evolution-Map.md) | Phase 1 — 24 concepts tracked Origin→Motivation→Refinement→Final→Status | Master §Phase 1 |
| 2 | [`02-RFC-Origin-Map.md`](02-RFC-Origin-Map.md) | Phase 4.1 — RFC Origin Map (10 RFCs, why created, influencing discussions) | Master §4.1 |
| 3 | [`03-Requirements-Traceability-Matrix.md`](03-Requirements-Traceability-Matrix.md) | Phase 4.2 — RTM (22 requirements REQ-001→022 with verification & dependency) | Master §4.2 |
| 4 | [`04-Architecture-Decision-Records.md`](04-Architecture-Decision-Records.md) | Phase 4.3 — 11 ADRs including rejected alternatives (ADR-001→011) | Master §4.3 |
| 5 | [`05-Formal-Model-Traceability.md`](05-Formal-Model-Traceability.md) | Phase 4.4 — 15 formal models → RFC mappings (BDI, LoT, CoALA, GWT, RHTT, etc.) | Master §4.4 |
| 6 | [`06-Dependency-Graph.md`](06-Dependency-Graph.md) | Phase 4.5 — Conceptual RFC DAG + technical file DAG (Mermaid) | Master §4.5 |
| 7 | [`07-Implementation-Roadmap.md`](07-Implementation-Roadmap.md) | Phase 4.6 — 12-phase roadmap (-1→11) with gates A–D | Master §4.6 |
| 8 | [`08-Open-Problems-Registry.md`](08-Open-Problems-Registry.md) | Phase 4.7 — 13 open problems OP-01→13 with severity & closing RFC | Master §4.7 |
| 9 | [`09-Future-RFC-Roadmap.md`](09-Future-RFC-Roadmap.md) | Phase 4.8 — RFC-011→025 future roadmap, priority & dependencies | Master §4.8 |

**Conventions (all files):** Every item carries **Origin** (MSG-01..09 + Stable ID), **Evolution** (how it changed), **Final Representation** (RFC/Component/REQ), **Status** (`Implemented`/`Proposed`/`Rejected`/`Open Question`). No early discussion is ignored; failed approaches are preserved (see ADR-002, ADR-004, `00-Research-Timeline §0.3`).

**Provenance — Message Index:**

| ID | Stable ID family | Scope |
|----|------------------|-------|
| MSG-01 | `TEXT-INT-001`, `RED-LANG-001`, `AGENT-ANALYSIS-001` | Text interfaces, REPL, Red features, dialect→tool |
| MSG-02 | `AGENT-ENV-001`, `AGENT-ENV-ANALYSIS-001` | ARS triad, pipeline, memory, events, tool invocation |
| MSG-03 | `COGOS-001`, `COGOS-ANALYSIS-001` | CogOS, goal scheduler, kernel primitives |
| MSG-04 | `COGOS-FRAMEWORK-001`, `...-ANALYSIS-001` | Layered stack, goals as DAG, knowledge-graph FS, uncertainty |
| MSG-05 | `RED-COG-001`, `RED-COG-ANALYSIS-001` | Red/Cognition 16 types, contracts, BDI/LoT grounding |
| MSG-06 | `RED-COMPILER-001`, `RED-COMPILER-ANALYSIS-001` | Compiler passes, CIR, DAG plans, Policy-as-Type |
| MSG-07 | `CVM-001`, `CVM-ANALYSIS-001` | CVM, CISA v0.1, heap, attention/GWT, provenance |
| MSG-08 | `RED-20-001`, `RED-20-ANALYSIS-001` | Red 2.0, three compilers, intent contracts |
| MSG-09 | `RED-SPEC-001`, `RED-SPEC-015`, `RED-SPEC-PART-III-001` | Deep technical spec ground truth |

**Branches:** `audio` (9b5b15a baseline) → `arena/019fae00`/`arena/019fae68` (wiki +8197) → `arena/019fec34-red-cognition` (this archive). See `TRACEABILITY-ARCHIVE.md Appendix B`.

*Generated 2026-08-10 on `arena/019fec34-red-cognition` by Full Conversation Traceability Auditor.*
