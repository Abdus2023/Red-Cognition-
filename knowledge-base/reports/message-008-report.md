# Extraction Report — Message #8 (transcript [61]–[80])

- **Processed:** 2026-08-10
- **Source processed:** Conversation message #8 — a 20-part labeled transcript ([61]–[80]; speakers USER, CHATGPT (gpt-5-5-mini), CHATGPT (gpt-5-5)) covering: RC-700 Cognitive VM Specification (draft + review), RC-800 Cognitive OS Specification (draft + review), RC-900 Governance Manual (draft; concludes RC family drafting), family coherence review (doctrines, dependency graph, Phase 0–3 roadmap, RC-1000 proposal), RFC-0001 Cognitive Type System (v1.0→v1.2, **RATIFIED**), RFC-0002 Effect Ordering Model (v1.0→v1.1, **RATIFIED**), RFC-0003 Belief Revision System (v1.0→v1.1, **Accepted for Final Ratification**), and ADR-0005…0012 occurrences with numbering conflicts.
- **Verbatim archive:** `sources/message-008-original-part1..5.md`.

## Counts

| Metric | Value |
|--------|-------|
| Documentation sections identified | **297** heading-delimited sections (all heading levels within sub-message bodies, programmatic count over the archive; reproducible) |
| Documentation sections extracted | **297 / 297** — verbatim in archive; organized per the message #8 sub-message index |
| Wiki pages created | **0** (all content fit existing supported pages) |
| Wiki pages updated | **14** — RFC Index, Architecture, Data Models, Components, Workflows, Design Decisions, Glossary, Specifications, Repository Structure, Code Snippets, Changelog, Source Traceability (+ README index; report file created) |
| Repository files identified | **8** documents with documented placement (RC-000 §8 mandates `specs/` and `rfcs/`) |
| Repository locations assigned | **8** — specs/: RC-700 ([61]), RC-800 ([63]), RC-900 ([65]); rfcs/: RFC-0001 v1.2 ([71]) + record ([72]), RFC-0002 v1.1 ([75]) + record ([76]), RFC-0003 v1.1 ([79]). Extracted programmatically, byte-exact |
| Unresolved repository locations | **109 of 109 code snippets** (no documented paths). Phase-0 skeleton ([66]: `cvm/`, `cogos/`, sub-dirs) recorded as documented proposal, NOT scaffolded (ambiguity vs mandated layout — see Repository Structure) |
| Code snippets found | **109** fenced blocks ([62] 15, [63] 1, [64] 12, [65] 1, [66] 16, [68] 19, [69] 3, [70] 16, [71] 4, [72] 5, [73] 1, [74] 3, [75] 2, [76] 1, [77] 2, [78] 4, [79] 2, [80] 2; [61]/[67] have none) |
| Code snippets extracted | **109 / 109** (SN-319…SN-427; Message #8 Annex, corpus order) |
| Cross references added | **10** (X-41…X-50) |
| RFC relationships added | **9** — parent links RC-700→RC-600, RC-800→RC-700, RC-900→RC-800, RFC-0001/0002/0003→RC-200, RFC-0002/0003→RFC-0001; ratification records [72]→RFC-0001, [76]→RFC-0002; RFC-0002 extends RC-300/400/500/700/800 |
| Duplicate items detected | **4 new groups** (D-31…D-34) + D-21 updated (RC-700 CISA as normative concretization); all preserved |
| Conflicts detected | **2 extended** — C-5 (RFC-0004+ numbering: six documented assignment waves; registered set fixed by ratified records) and C-6 (ADR-0005…0009 multiple documented titles; [66] registry snapshot lists only ADR-0001…0004). No new independent conflicts |
| Traceability status | **Complete** — all 20 sub-messages indexed; every scaffolded document traced to exact origin; every snippet ID'd |
| Verification status | **Passed** — see below |
| Missing items | **10** (see below) |
| Ambiguous items | See below |

## Explicit comparisons

- **Documentation found vs extracted:** 297 / 297 (100%).
- **Code snippets found vs extracted:** 109 / 109 (100%).

## Verification

1–4. Section and snippet counts as above. ✔
5. Snippets: extracted ✔; rendering artifacts only (entity decoding, `<details>` removal) ✔; Unresolved Location (no documented paths) ✔; unchanged from source ✔ (programmatic extraction guarantees byte-exact embeddings).
6. Knowledge items: extracted/categorized/linked/traceable ✔.
7. Discrepancies reported without inference:
   - Phase-0 skeleton naming/structure differs from RC-000 §8 mandated layout — recorded, unresolved.
   - [66] ADR registry snapshot (ADR-0001…0004 only) contradicts ADR-0005+ acceptances in [62]/[64]/[70]/[72]/[76] — recorded as C-6, unresolved.
   - [69]/[71] contain stray `*` after type names (e.g., "`goal!`*:") — preserved as received.
   - [66] Phase-0 tree contains auto-link artifacts (`[RC-000.md](http://RC-000.md)`) — preserved as received.
   - Speaker label shifts from (gpt-5-5-mini) to (gpt-5-5) at [74] — recorded as-is.

## Missing items

1. Red Deep Technical Specification (Parts I–IV); 2. BDI & four-dimensional uncertainty definitions; 3. JIT+IR spec (msg#2 refs).
4. RC-700/800/900 ratified versions and ratification records. 5. RC-300 ratification record (carried). 6. RC-400/500/600 v1.1 revisions (carried).
7. RFC-0003 ratification record. 8. RFC-0004+ documents (titles contested). 9. RFC-0001 "full specification" for lifecycle state machines (§8 reference). 10. RC-1000 Formal Semantics (proposed [66]).

## Ambiguous items

1. Whether Phase-0 skeleton supersedes or complements the mandated layout (not stated).
2. Canonical ADR numbering (no consolidation statement in corpus).
3. Canonical RFC-0004+ titles (six waves; none ratified).
4. RC-900 hierarchy places "RC-100–800 Technical Architecture Specifications" at one frequency tier — RC-900 self-placement ("Moderate") vs its role as governance manual consistent; no conflict recorded.

## Status

All content in message #8 has been extracted, organized, scaffolded (to the extent documented), cross-referenced, verified, and confirmed complete.
