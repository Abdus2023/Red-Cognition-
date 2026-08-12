# Extraction Report — Message #35 (directive "Deeply Verification" #8)

- **Processed:** 2026-08-12 · **Source:** user directive "Deeply Verification" — no new corpus content.
- **Documentation sections identified/extracted:** 0 / 0. **Code snippets found/extracted:** 0 / 0.

## Deep audit suite #8 — 68 checks, 8 categories

| # | Category | Checks | Result |
|---|----------|--------|--------|
| 1 | Archive structure | 103 archive files; labels [1]…[420] contiguous (420/420); speaker labels; byte-identity spot checks for identical re-send groups (D-96/97/99/100/104) and re-purposed-number pairs (D-107…D-114, msg#29-vs-#33 and msg#29-vs-#34) verified distinct | 5/5 PASS |
| 2 | Snippet-ledger integrity | SN-001…SN-2460 no gaps; totals line 2460 with single parenthetical; msg#2 ledger 123 rows; 14 breakdown tables (msgs #16/18/21/22/23/25/26/27/29/30/31/32/33/34); archive fenced total 2457 = 2460 − 3 inline; per-message fenced counts (all 21 transcript messages); annex SN sequences complete & ascending; all annex blocks byte-faithful vs archives (msgs 3…34, 2457 blocks) | 22/22 PASS |
| 3 | Scaffolded documents | specs/ = 12; rfcs/ = 92; RFC-0001…0075 exactly once each (75 docs); 17 ratification records; msg#33/#34 renames present & superseded filenames absent; 104/104 provenance headers; 104/104 bodies verbatim from archive | 7/7 PASS |
| 4 | Wiki fidelity & provenance | 2457/2457 archived fenced blocks verbatim in Wiki; ≥17 pages with provenance headers; reports 001…035; 0 broken links | 4/4 PASS |
| 5 | Normative consistency — deep focus on messages #32–#34 | RFC-0072 record publication form [361] (D-101); RFC-0062 scaffold [377] lineage + ratification per [381] reflected; RFC-0061 provenance notes divergent [369] (D-102); RFC-0063 ratified per [385] + D-105; RFC-0064 scaffold [389] + ratified per [391] + D-106; RFC-0065 CPCAVP (C-21/D-107) + RFC-0066 CARTDP (D-108) + RFC-0067 CDLMP (D-109); records [381]/[385]/[391]; msg#34 re-purposing (D-110/111/112) and C-22 retentions (RFC-0071 CRCP body [319], RFC-0072 body [335]); RFC-0073/0074/0075 scaffolds; RFC-Index sections & ratified-set sections after #32/#33/#34; no RATIFIED claims for draft numbers; C-20/C-21/C-22; D-105…D-114; X-145…X-158; Glossary 13/13 terms | 16/16 PASS |
| 6 | RFC parent-chain integrity | all 75 RFC documents carry Parent headers; chain RFC-0034…0075 exact (incl. 0043→0028 detour) | 2/2 PASS |
| 7 | Status & cross-page coherence | README 35 messages + current totals (2460/12/92); no stale counts; ordering #32→#33→#34; table row current; Code-Snippets header current; changelog 1…35 | 6/6 PASS |
| 8 | Traceability bookkeeping | register rows 1…35 contiguous; 21 sub-message indexes; X-01…X-158; D-1…D-114; C-1…C-22; RC-000 §8 directories 9/9 | 6/6 PASS |

**Result: 68/68 checks passed after defect remediation (below).**

## Defects found & corrected (3 — provenance metadata only; no source text altered)

1. **RFC-0062 scaffold provenance stale (the principal finding):** written during message-#32 processing, it still claimed "No USER ratification record present in corpus — RFC-0062 remains Candidate" although message #33's [381] is exactly that record and `rfcs/RFC-0062-ratification-record.md` is scaffolded from it. Provenance updated to "RATIFIED per USER ratification record [381] (msg#33)"; body untouched.
2. **RFC-0061 scaffold provenance incomplete:** did not mention the divergent RFC-0061 v1.0 Draft [369] (msg#32, D-102), which is archive-only. Note added; body untouched.
3. **Suite-construction corrections (check-side, disclosed):** two suite-#8 checks initially referenced the wrong sub-message numbers for the RFC-0063/0064 lineage ([369]/[371] instead of [389]/[391] — the RFC-0064 v1.1+record arc lives in message #33, not #32); corrected and two checks added (RFC-0062 ratification-provenance reflection; RFC-0061 D-102 note).

No source-content fidelity issues found: all 2457 fenced blocks byte-faithful, all 104 scaffold bodies verbatim, 0 broken links, all ledgers contiguous.

## Adjudications & regression notes

1. **Ratified set re-verified (22 documents):** RC-000, RC-100, RC-200, RFC-0001, RFC-0002, RFC-0011, RFC-0042, RFC-0046, RFC-0047, RFC-0049, RFC-0050, RFC-0052, RFC-0053, RFC-0057, RFC-0058, RFC-0059, RFC-0060, RFC-0061, RFC-0062, RFC-0063, RFC-0064, RFC-0072 — each backed by a ratification event; RFC-0072's effect remains conditionally suspended on RFC-0071 per the [361] record.
2. **C-22 retention decisions re-verified:** RFC-0071 CRCP scaffold retained (dependency of ratified RFC-0072), RFC-0072 ratified scaffold retained; CRSEDTP [407] and CRARSH [409] archive-only.
3. **Regression:** message-018 monotonic suite re-run — **25/25 PASS**. Suites #29–#34 are point-in-time snapshots superseded by suite #8 (same treatment as suites 019–028 at earlier directives); not re-scored.

## Verification artifacts

- Reproducible suite: [`message-035-verification-suite.py`](message-035-verification-suite.py) (run from the repository root; final state **68/68 PASS** after the disclosed corrections).
- Prior deep suites: #6 (`message-024-verification-suite.py`), #7 (`message-028-verification-suite.py`); monotonic regression: `message-018-verification-suite.py`.

## Status

Deep verification complete: the knowledge base is consistent, complete, and fully traceable for all 34 processed content messages ([1]–[420], SN-001…SN-2460, 104 scaffolded documents). Three provenance-metadata defects were found and corrected; no source-content fidelity issues remain.
