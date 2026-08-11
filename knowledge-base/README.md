# Knowledge Base Index

Traceable, incrementally maintained knowledge base built from the conversation corpus.

**Corpus status:** 26 messages processed (2026-08-11). Message #1 = governing extraction specification. Message #2 = 20-part transcript on Red and the Red/Cognition vision. Message #3 = [21]–[40]: ratified **RC-000 Constitution**, RC-100 Architecture Specification. Message #4 = "Continue" verification directive. Message #5 = [41]–[60]: RC-100/RC-200 ratified; RC-300 approved-pending-record; RC-400/500/600 drafts. Messages #6–#7 = verification directives. Message #8 = [61]–[80]: RC-700/RC-800/RC-900 drafts complete the RC family; RFC-0001/0002 ratified. Message #9 = verification directive. Message #10 = [81]–[100]: RFC-0003 & RFC-0004 ratified; RFC-0006 v1.2 approved. Message #11 = deep verification directive. Message #12 = [101]–[120]: RFC-0011 Scheduler ratified; RFC-0012 CVM approved; RFC-0013 CISA candidate. Message #13 = deep verification directive #2. Message #14 = [121]–[140]: RFC-0014…RFC-0023 drafted. Message #15 = deep verification directive #3. Message #16 = [141]–[160]: RFC-0024…RFC-0033 drafted — governance/hardware/verified-compiler planes (resource quotas, CSPL, hardware acceleration, compiler & toolchain, CIR, CIR-SER, optimization pass framework, COIL, COVF, CPCPF); sub-numbered proposals RFC-0025.1 Policy VM / RFC-0026.1 CHAL; RFC-0034 title proposed (CPR-TDP). Message #17 = deep verification directive #4. Message #18 = [161]–[180]: **RFC-0033 CPCPF redraft; RFC-0034…RFC-0042 drafted; RFC-0042 RATIFIED** — ecosystem planes: package registry (CPR-TDP), sandbox (CSEIM), supply chain (CBR-SCP), lifecycle (CSLEMP), marketplace (CMAEP), ownership (CIEOP), governance (CGCDP), federation (CIFP), autonomous deployment (CADP); RFC-0043…0050 roadmap proposed. Message #19 = deep verification directive #5. Message #20 = re-sent governing extraction specification (identical duplicate of message #1; D-63). Message #21 = [181]–[200]: **RFC-0043 CLS; RFC-0044 CSL; RFC-0045 CTDX; RFC-0046 CODP (v1.2 RATIFIED per [196]); RFC-0047 CPMWS** — Language & Developer Platform layer; roadmaps [182]/[196]. Message #22 = [201]–[220]: **RFC-0047 CPMWS RATIFIED ([202]); RFC-0048 CFFI; RFC-0049 CSTS RATIFIED ([215]); RFC-0050 Architecture & Conformance capstone (v1.1 Candidate)** — toolchain layer complete. Message #23 = [221]–[240]: **RFC-0050 RATIFIED (constitutional architecture, [224]/[225]); RFC-0051 CMMS; RFC-0052 CTVF RATIFIED ([235]); RFC-0053 CRAIP** — platform constitution frozen; ecosystem expansion underway. Message #24 = deep verification directive #6. Message #25 = [241]–[260]: **RFC-0053 CRAIP RATIFIED ([244]/[247]); RFC-0054 CADFP; RFC-0055 CMCWP; RFC-0056 CSMKSP; RFC-0057 CDTCP** — distributed cognition planes (invocation/control/coordination/knowledge/transaction). Totals: **1419 code snippets** (SN-001…SN-1419), **12 scaffolded documents in `specs/`**, **65 files in `rfcs/`**. Message #26 = [261]–[280]: **RFC-0057 CDTCP RATIFIED ([266]/[267]); RFC-0058 CTWP RATIFIED ([276]/[277]/[278]); RFC-0059 CTSTP** — transaction subsystem complete (semantics/wire/security planes). Totals: **1591 code snippets** (SN-001…SN-1591), **12 scaffolded documents in `specs/`**, **69 files in `rfcs/`**.

## Governing rules (Message #1)

- Verbatim source: [`sources/message-001-original.md`](sources/message-001-original.md)
- Treat the entire conversation as a single evolving corpus; integrate incrementally without losing provenance.
- Never fabricate, infer, modify, summarize, or omit information unless explicitly instructed.
- Code snippets are extracted verbatim (rendering-artifact cleanup only); repository scaffolding uses only documented layout — undocumented placement is marked **Unresolved Location**.
- Wiki pages are created only when supported by source material. Cross-references and RFC relationships are recorded only when they exist in the source.
- Every item carries full traceability (message, document, file, heading, section, filename, path, version, RFC id, parent document).
- Duplicates are classified (identical / updated / superseded / conflicting / complementary) and never silently discarded.
- An extraction report with verification counts is produced after every message: [`reports/`](reports/).

## Structure

| Path | Purpose |
|------|---------|
| `sources/` | Verbatim original messages and documents (provenance archive) |
| `wiki/` | Structured Wiki pages (only supported pages exist) |
| `reports/` | Per-message extraction & verification reports |

## Wiki pages

| Page | Status |
|------|--------|
| [Overview](wiki/Overview.md) | Active — Red language overview, core features, three-layer vision, positioning |
| [Architecture](wiki/Architecture.md) | Active — stacks, layered cognitive architecture, CogOS, compiler architecture |
| [Components](wiki/Components.md) | Active — CVM, kernel, CogProcess, memory, attention, multi-agent runtime |
| [Services](wiki/Services.md) | Active — cognitive microkernel services |
| [Modules](wiki/Modules.md) | Active — cognitive standard library |
| [APIs](wiki/APIs.md) | Active — primitives, Cognitive ABI, CISA, register file |
| [Data Models](wiki/Data-Models.md) | Active — cognitive datatypes, intent contracts, effects, agent model |
| [Workflows](wiki/Workflows.md) | Active — CLI/REPL/agent lifecycles, pipelines, planning, provenance |
| [Security](wiki/Security.md) | Active — capability-based execution, policy types, explainability |
| [Deployment](wiki/Deployment.md) | Active — 1 MB toolchain, cross-compilation, local-first |
| [Design Decisions](wiki/Design-Decisions.md) | Active — philosophy, charter, modes, key decisions |
| [Specifications](wiki/Specifications.md) | Active — SPEC-1/SPEC-2/SPEC-3 system-prompt artifacts |
| [Repository Structure](wiki/Repository-Structure.md) | Active — documented governance layout vs. actual repo |
| [Code Snippets](wiki/Code-Snippets.md) | Active — ledger of all 1093 snippets (SN-001…SN-1093) |
| [RFC Index](wiki/RFC-Index.md) | Active — RC-000…RC-900 family, RFC-0001…0004 outlines, ADRs, constitution evolution |
| [Glossary](wiki/Glossary.md) | Active — terms defined in corpus |
| [References](wiki/References.md) | Active — cited URLs + missing referenced documents |
| [Changelog](wiki/Changelog.md) | Active — knowledge-base evolution log |
| [Source Traceability](wiki/Source-Traceability.md) | Active — message register, items ledger, cross-references, RFC graph, duplicate log |

Candidate pages not yet created (no supporting source material yet): Database, Configuration, Infrastructure, Authentication, Build System, Dependencies, File References.
