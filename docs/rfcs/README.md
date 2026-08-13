# Red/Cognition RFC Series — Index

This directory formalises the `docs/wiki` canonical draft RFCs (20 files, 8177 lines) into numbered, reviewable RFC documents per `docs/TRACEABILITY-ARCHIVE.md` §4.1 / §4.8.

All RFCs satisfy the mandatory provenance rule **Origin / Evolution / Final Representation / Status** inherited from the audit.

| RFC | Title | Stable ID(s) | Origin | Status | Wiki Source |
|-----|-------|--------------|--------|--------|-------------|
| [0000](RFC-0000-Template.md) | RFC Template & Conventions | — | Meta | `Implemented` | — |
| [0001](RFC-0001-Text-Interfaces-and-Agent-Runtimes.md) | Text Interfaces & Agent Runtimes | `TEXT-INT-001` | MSG-01 | `Draft` | `Text-Interfaces-and-Agent-Runtimes.md` |
| [0002](RFC-0002-Red-Programming-Language-Core.md) | Red Programming Language Core | `RED-LANG-001`, `RED-SPEC-001/015/PART-III` | MSG-01+09 | `Implemented` | `Red-Programming-Language.md` + `Red-Deep-Technical-Specification.md` + `Red-Technical-Specification-Part-III.md` + `Red-Interpreter-Internals.md` |
| [0003](RFC-0003-Agent-Operating-Environment.md) | Agent Operating Environment | `AGENT-ENV-001`, `AGENT-ENV-ANALYSIS-001` | MSG-02 | `Draft` | `Agent-Operating-Environment.md` + `Agent-Operating-Environment-Analysis.md` + `Agent-Runtime-Analysis.md` |
| [0004](RFC-0004-Cognitive-Operating-System.md) | Cognitive Operating System (CogOS) | `COGOS-001`, `COGOS-ANALYSIS-001`, `COGOS-FRAMEWORK-001/ANALYSIS` | MSG-03/04 | `Draft` | `Cognitive-Operating-System-CogOS.md` + `From-Operating-Systems-to-Cognitive-Systems.md` + both Analyses |
| [0005](RFC-0005-Red-Cognition-Language.md) | Red/Cognition Language | `RED-COG-001`, `RED-COG-ANALYSIS-001` | MSG-05 | `Draft` | `Red-Cognition-Language.md` + `Red-Cognition-Analysis.md` |
| [0006](RFC-0006-Cognitive-Compiler-and-CIR.md) | Cognitive Compiler & CIR | `RED-COMPILER-001`, `RED-COMPILER-ANALYSIS-001` | MSG-06 | `Draft` | `Red-Compiler-Refactoring.md` + `Red-Compiler-Analysis.md` |
| [0007](RFC-0007-Cognitive-Virtual-Machine.md) | Cognitive Virtual Machine (CVM) | `CVM-001`, `CVM-ANALYSIS-001` | MSG-07 | `Draft` | `Cognitive-Virtual-Machine-CVM.md` + `Cognitive-Virtual-Machine-Analysis.md` |
| [0008](RFC-0008-Red-2.0-Architecture.md) | Red 2.0 Cognitive Computing Architecture | `RED-20-001`, `RED-20-ANALYSIS-001` | MSG-08 | `Draft` | `Red-2.0-Cognitive-Computing-Architecture.md` + `Red-2.0-Analysis.md` |
| [0009](RFC-0009-Red-Deep-Technical-Specification.md) | Red Deep Technical Specification (Parts I–IV) | `RED-SPEC-001`, `RED-SPEC-015`, `RED-SPEC-PART-III-001` | MSG-09 | `Implemented` | `Red-Deep-Technical-Specification.md` + `Red-Technical-Specification-Part-III.md` + `Red-Interpreter-Internals.md` |
| [0010](RFC-0010-Analysis-and-Grounding-Suite.md) | Analysis & Grounding Suite (Meta-RFC) | All `*-ANALYSIS-001` | MSG-01–08 | `Implemented` | All `*-Analysis.md` (8 files) |
| Synthesis | [Red and AI Agents](../../docs/wiki/Red-and-AI-Agents.md) | `RED-AI-SYNTHESIS-001` | MSG-10 | `Draft` | `Red-and-AI-Agents.md` (canon synthesis of 0001–0009) |

Future RFCs `0011→0025` — **all now drafted** (see commits `ce65dd5` for 0011→0014, this commit for 0015→0025):

| RFC | OP Closed | Priority | Title |
|-----|-----------|----------|-------|
| 0011 | OP-01 | P0 Blocking | Ecosystem Bridge |
| 0012 | OP-02 | P1 | Ergonomic Proof |
| 0013 | OP-03 | P1 | Totality |
| 0014 | OP-04 | P1 | Cognitive Lock File |
| 0015 | OP-05 | P1 | Cooperative Yield |
| 0016 | OP-06+08 | P0 | MESI Coherence |
| 0017 | OP-07 | P0 Safety | Misalignment Gate |
| 0018 | OP-09 | P1 | Mnemonic Sovereignty |
| 0019 | OP-10 | P2 | Red JIT |
| 0020 | OP-11 | P1 | Calibrated Confidence |
| 0021 | OP-12 | P1 | Attention Liveness |
| 0022 | OP-13 | P2 | Skill Algebra |
| 0023 | MSG-09 open | P2 | Lexer v2 |
| 0024 | MSG-07 object | P2 | Cognitive Object Model |
| 0025 | Roadmap-derived | P3 Future | Proof-Carrying Artifact (only roadmap-derived RFC per horizon note) |

Process per `docs/TRACEABILITY-ARCHIVE.md` §4.8: each closes its `OP-xx`, updates `08-Open-Problems-Registry.md` to `Closed (RFC-00yy)` on merge.

**How to review an RFC:** Each file carries a *Provenance* header table (Origin / Evolution / Final / Status) plus the canonical content verbatim from `docs/wiki`, reorganised into IETF-style sections (Abstract, Motivation, Specification, Consequences, Traceability). Changes vs `docs/wiki` are diff-marked; no early discussion is omitted.
