# Extraction Report — Message #26 (transcript [261]–[280])

- **Processed:** 2026-08-11
- **Source processed:** Conversation message #26 — a 20-part labeled transcript ([261]–[280]; speakers USER, CHATGPT (gpt-5-5), CHATGPT (gpt-5-5-mini)): RFC-0057 CDTCP v1.3 in three successive same-label iterations ([261] → [263] adds §7.1 Wire Message Schemas → [265] adds Prepared vote schema) → reviews ([262] 9.6/10; [264] 9.3/10; [266] "Ready for Ratification", 9.5/10) → ratification record ([267]) — **RATIFIED**; RFC-0058 CTWP: v1.0 ([269]) → v1.1 ([271]) → v1.2 first iteration ([273]) (normative bodies byte-identical — D-87; closing paragraphs claim additions absent from bodies — C-15, flagged by [272]) → CHATGPT-authored v1.1 candidate improvements embedded in review ([270]) → v1.2 second iteration ([275], substantive additions — D-88) → reviews ([274] "APPROVED WITH MINOR AMENDMENTS"; [276] "Decision: APPROVED FOR RATIFICATION") → ratification record ([277]) + confirmation ([278]) — **RATIFIED**; RFC-0059 CTSTP: v1.0 Draft ([279]) + CHATGPT-authored v1.1 Candidate proposal embedded in review ([280]).
- **Verbatim archive:** `sources/message-026-original-part1..5.md` ([261]–[264], [265]–[268], [269]–[272], [273]–[276], [277]–[280]).

## Counts

| Metric | Value |
|--------|-------|
| Documentation sections identified | **306** heading-delimited sections (all heading levels within sub-message bodies, programmatic count over the archive; same reproducible metric validated against message #16's 224) |
| Documentation sections extracted | **306 / 306** — verbatim in archive; organized per the message #26 sub-message index |
| Wiki pages created | **0** |
| Wiki pages updated | **12** — RFC Index, Architecture, Data Models, Workflows, Security, Glossary (+12 terms, CDTCP entry updated), Specifications, Repository Structure, Code Snippets, Changelog, Source Traceability (+ README index) |
| Repository files identified | **5** documents with documented placement (RC-000 §8 mandates `rfcs/`): RFC-0057 update (v1.3), RFC-0057 ratification record, RFC-0058, RFC-0058 ratification record, RFC-0059 |
| Repository locations assigned | **5** — RFC-0057 ([265], scaffold updated), RFC-0057 ratification record ([267]), RFC-0058 ([275], second v1.2 iteration), RFC-0058 ratification record ([277]), RFC-0059 ([279] v1.0; CHATGPT v1.1 proposal [280] archived, not scaffolded) — programmatic, byte-exact; superseded versions preserved in archive only |
| Unresolved repository locations | **172 of 172 code snippets** (no documented paths) |
| Code snippets found | **172** fenced blocks ([261] 6, [262] 5, [263] 7, [264] 15, [265] 7, [266] 11, [267] 0, [268] 0, [269] 2, [270] 18, [271] 2, [272] 20, [273] 2, [274] 21, [275] 6, [276] 16, [277] 0, [278] 10, [279] 0, [280] 24) |
| Code snippets extracted | **172 / 172** (SN-1420…SN-1591; Message #26 Annex, corpus order; repeated CDTCP fences across [261]/[263]/[265] and identical CTWP fences across [269]/[271]/[273] preserved) |
| Cross references added | **5** (X-112…X-116) |
| RFC relationships added | **4** — 2 parent links (0058→0057, 0059→0058) + 2 ratification links (RFC-0057 ← [266]/[267], RFC-0058 ← [276]/[277]/[278]) |
| Duplicate items detected | **6 new** (D-85 CDTCP v1.2→v1.3; D-86 CDTCP v1.3 same-label iterations; D-87 CTWP [269]≡[271]≡[273] bodies; D-88 CTWP second v1.2 [275] supersedes; D-89 CTSTP v1.0 vs CHATGPT v1.1 proposal; D-90 ratified-foundation snapshots) |
| Conflicts detected | **2 new** — C-14 ([267]/[277] status tables omit RFC-0049…0052 and list RFC-0046/0047 as "Final Candidate" despite ratification events [196]/[202]; C-9/C-12/C-13 pattern; events authoritative, tables preserved); C-15 ([271]/[273] closing paragraphs claim additions absent from their byte-identical v1.0 bodies; flagged by [272]; additions first appear in [275]; bodies authoritative) |
| Traceability status | **Complete** — all 20 sub-messages indexed; scaffolded documents traced; all snippets ID'd |
| Verification status | **Passed** — see below |
| Missing items | cumulative list extended (see Source Traceability; new: RFC-0054/0055/0056 v1.1 revisions absent ([250]/[252]/[254] additions not incorporated in corpus); RFC-0059 v1.1 exists only as a CHATGPT-authored proposal ([280]) — no user-submitted v1.1; RFC-0060 transport binding / RFC-0061 persistence engine proposed-but-absent ([270]/[276]); CDTCP fields DecisionProof/ManifestHash/Epoch/RetryPolicy remain semantically undefined ([262]/[264]/[266]); CTWP cryptographic algorithm profiles deferred to RFC-0059 ([276])) |
| Ambiguous items | See below |

## Explicit comparisons

- **Documentation found vs extracted:** 306 / 306 (100%).
- **Code snippets found vs extracted:** 172 / 172 (100%).

## Verification

1–4. Counts as above. ✔
5. Snippets: extracted ✔; rendering artifacts only ✔ (entities decoded incl. encoded blockquote markers and arrows inside fences; `<details>` wrappers removed; no other changes); Unresolved Location ✔; unchanged from source ✔ (programmatic byte-exact extraction; all 172 archived fenced blocks embedded in the Wiki annex; version-iteration identities verified programmatically: [269]≡[271]≡[273] normative bodies, [261]→[263]→[265] deltas as described).
6. Knowledge items: extracted/categorized/linked/traceable ✔.
7. Discrepancies reported without inference:
   - C-14: [267]/[277] status tables vs ratification events — events authoritative; tables preserved verbatim.
   - C-15: [271]/[273] closing claims vs actual bodies — bodies authoritative; claims recorded as erroneous; [275] carries the first actual incorporation.
   - Three successive documents share the "v1.3" label ([261]/[263]/[265]) and two share "v1.2" ([273]/[275]) — preserved as received; distinguished by sub-message in all traceability records.
   - Source quirks preserved: stray closing parentheses in [277] ratified-components list and [279] §3; [262] parenthetical quirk — no corrected versions exist in corpus.
   - D-85…D-90 recorded; nothing silently discarded.
   - Ratification nuance: RFC-0057 ratified via review assessment [266] + user record [267]; RFC-0058 ratified via review decision [276] + user record [277] + confirmation [278]; RFC-0059 NOT ratified — v1.0 Draft only, v1.1 is a CHATGPT-authored proposal.

## Ambiguous items

1. Whether a user-submitted RFC-0059 v1.1 will appear (only the CHATGPT-authored proposal [280] exists) — corpus silent.
2. Roadmap numbering for RFC-0059…0061 diverges across [262] (0059 verification & proofs, 0060 advanced transactions), [270] (0059 CCISCP, 0060 QUIC binding, 0061 persistence), and [276]/[277] (0059 CTSTP ✓ drafted, 0060 transport binding, 0061 persistence engine) — drafting followed [276]/[277] for 0059; C-11 lineage; corpus silent on the rest.
3. Whether [262]/[264]/[266] remaining gaps (coordinator election, transition tables, DecisionProof/ManifestHash/Epoch/RetryPolicy semantics, nested transactions, isolation guarantees) will be addressed in a v1.4/errata — corpus silent.

## Status

All content in message #26 has been extracted, organized, scaffolded (to the extent documented), cross-referenced, verified, and confirmed complete.
