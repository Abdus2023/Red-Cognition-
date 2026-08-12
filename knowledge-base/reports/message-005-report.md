# Extraction Report — Message #5 (transcript [41]–[60])

- **Processed:** 2026-08-10
- **Source processed:** Conversation message #5 — a 20-part labeled transcript ([41]–[60]; speakers USER, CHATGPT (gpt-5-5-mini)) covering: RC-100 ratification ([41]/[42]); RC-200 Language Specification v1.0→v1.1→v1.2 and **ratification as v1.0** ([43]–[50]); RC-300 Compiler Specification v1.0→v1.1 Candidate, **APPROVED FOR RATIFICATION** ([51]–[54]); RC-400 Runtime Specification v1.0 Draft + review ([55]/[56]); RC-500 Cognitive Runtime Specification v1.0 Draft + review ([57]/[58]); RC-600 Agent Runtime Shell Specification v1.0 Draft + review ([59]/[60]); ADR-0002…ADR-0008; RFC registry (RFC-0001…0003 registered; 0004…0008 proposed) with numbering conflicts documented.
- **Verbatim archive:** `sources/message-005-original-part1.md` ([41]–[44]), `…-part2.md` ([45]–[48]), `…-part3.md` ([49]–[52]), `…-part4.md` ([53]–[56]), `…-part5.md` ([57]–[60]).
- **Naming note:** this is corpus message #5 (message #4 was the "Continue" verification directive); archive/report numbered accordingly.

## Counts

| Metric | Value |
|--------|-------|
| Documentation sections identified | **421** heading-delimited sections (all heading levels within sub-message bodies, counted programmatically from the archive; reproducible). Largest: [44] review, [52] review, [56] review, [60] review |
| Documentation sections extracted | **421 / 421** — verbatim in archive; organized into Wiki pages per the message #5 sub-message index in Source Traceability |
| Wiki pages created | **0** (all content fit existing supported pages; no unsupported sections created) |
| Wiki pages updated | **13** — RFC Index, Architecture, Data Models, Components, APIs, Workflows, Security, Design Decisions, Specifications, Glossary, Repository Structure, Code Snippets, Changelog, Source Traceability (+ README index) |
| Repository files identified | **7** specification documents with documented placement (RC-000 §8 mandates `specs/`) |
| Repository locations assigned | **7** — `specs/RC-100-ratification-record.md` ([41]), `specs/RC-200-language-specification.md` ([47]), `specs/RC-200-ratification-record.md` ([49]), `specs/RC-300-compiler-specification.md` ([53]), `specs/RC-400-runtime-specification.md` ([55]), `specs/RC-500-cognitive-runtime-specification.md` ([57]), `specs/RC-600-agent-runtime-shell-specification.md` ([59]) — extracted programmatically, byte-exact from archive |
| Unresolved repository locations | **106 of 106 code snippets** — no snippet carries a documented repository path; all Unresolved Location; `rfcs/` remains empty (RFC-0001…0008 have no document text in corpus — nothing fabricated) |
| Code snippets found | **106** fenced blocks ([41] 1, [42] 11, [43] 1, [44] 24, [45] 1, [46] 6, [47] 0, [48] 6, [49] 0, [50] 4, [51] 1, [52] 10, [53] 4, [54] 5, [55] 3, [56] 11, [57] 1, [58] 7, [59] 1, [60] 9) |
| Code snippets extracted | **106 / 106** (SN-213…SN-318; embedded verbatim in the Code Snippets Message #5 Annex (label corrected during message #7 audit); IDs in corpus order) |
| Cross references added | **9** (X-32…X-40) |
| RFC relationships added | **12** — RC-200→parent RC-100, RC-300→RC-200, RC-400→RC-300, RC-500→RC-400, RC-600→RC-500 (5 parent links); ratification records [41]→RC-100, [49]→RC-200 (2); registered RFC-0001/0002/0003 → RC-200 (3); proposed RFC-0004/0005 → RC-300 review, RFC-0006/0007/0008 → RC-400 review (recorded as proposal links, 2 groups) |
| Duplicate items detected | **9 new groups** (D-22…D-30): cognitive type list evolution (superseded variants → ratified 9-type list), CEC/nine-layer/authority-chain repetitions, type-evolution path, goal-block example variants, runtime component lists, repeated alternatives analyses, runtime API surface variants |
| Conflicts detected | **4 new** (C-5 RFC-0002…0005 title assignments — resolved reference: ratified RC-200 record [49] per documented authority hierarchy; C-6 ADR-0005/0006 dual titles — later acceptance [58] recorded, proposals preserved; C-7 RC-300 approval without ratification record + RC-400 parent-label mismatch; C-8 R0–R3 label collisions across three schemes) |
| Traceability status | **Complete** — all 20 sub-messages indexed; every section in archive; every snippet ID'd; every scaffolded document traced to its exact origin sub-message |
| Verification status | **Passed** — see below |
| Missing items | **7** (see below) |
| Ambiguous items | See below |

## Explicit comparisons

- **Documentation found vs extracted:** 421 found / 421 extracted (100%).
- **Code snippets found vs extracted:** 106 found / 106 extracted (100%).

## Verification

1. Total documentation sections counted: 421 (programmatic heading count). ✔
2. Extracted documentation sections counted: 421. ✔
3. Total code snippets counted: 106. ✔
4. Extracted code snippets counted: 106. ✔
5. Every snippet verified: extracted ✔; cleaned only for rendering artifacts ✔ (entity decoding + `<details>` wrapper removal; no semantic changes); scaffolded = Unresolved Location ✔; unchanged from source ✔ — programmatic extraction from archive guarantees byte-exact embeddings.
6. Every knowledge item verified: extracted ✔ categorized ✔ linked ✔ traceable ✔.
7. Discrepancies reported without inference:
   - C-5…C-8 recorded in Source Traceability; none silently resolved.
   - [44] effect example contains an auto-link rendering artifact `[[filesystem.read](http://filesystem.read)]` — preserved as received in archive; noted in Data Models.
   - RC-300 has no ratification record although approved ([54]); RC-400 cites parent as "RC-300 v1.0 (Candidate)" — recorded as C-7.

## Missing items (referenced in corpus, not provided)

1. Red Deep Technical Specification (Parts I–IV) — referenced by msg#2 [19], msg#3 [21].
2. BDI-style semantics & four-dimensional uncertainty model — referenced by msg#2 [19].
3. JIT + IR infrastructure specification — referenced by msg#2 [19].
4. RC-700 / RC-800 / RC-900 documents — mandated by the RC family, absent.
5. RFC-0001…0008 documents — registrations/proposals/outlines only.
6. RC-300 Ratification Record — expected after [54] approval; absent.
7. RC-400 v1.1 / RC-500 v1.1 / RC-600 v1.1 candidate revisions — recommended by reviews; absent.

## Ambiguous items

1. RC-300 post-approval status (awaiting ratification record; Amendments A–C from [54] not yet incorporated in any corpus document).
2. ADR-0005/0006 canonical titles (two documented variants; later acceptance recorded, no explicit reconciliation in corpus).
3. R0–R3 label reuse across replay/conformance/determinism schemes (documented as-is).
4. Whether RC-400's parent citation "RC-300 v1.0 (Candidate)" anticipates a ratified label (as happened for RC-100/RC-200) — not stated in corpus.

## Status

All content in message #5 has been extracted, organized, scaffolded (to the extent documented), cross-referenced, verified, and confirmed complete.
