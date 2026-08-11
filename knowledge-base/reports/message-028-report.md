# Extraction Report — Message #28 (directive "Deeply Verification" #7)

- **Processed:** 2026-08-11 · **Source:** user directive "Deeply Verification" — no new corpus content.
- **Documentation sections identified/extracted:** 0 / 0. **Code snippets found/extracted:** 0 / 0.

## Deep audit suite #7 — 66 checks, 8 categories

| # | Category | Checks | Result |
|---|----------|--------|--------|
| 1 | Archive structure | 73 archive files; labels [1]…[300] contiguous (300/300); speaker labels on every sub-message header | 3/3 PASS |
| 2 | Snippet-ledger integrity | SN-001…SN-1777 no gaps; totals line = 1777 with a single parenthetical breakdown; msg#2 ledger = 123 rows; breakdown tables msg#16 (20 rows, 168) / #18 (20, 100) / #21 (20, 45) / #22 (20, 91) / #23 (20, 119) / #25 (20, 71) / #26 (20, 172) / #27 (20, 186); archive fenced total 1774 = 1777 − 3 inline; per-message fenced counts match breakdown sums for all 15 transcript messages; annex SN sequences complete & ascending (msg#16/18/21/22/23/25/26/27); all 1774 annex blocks byte-faithful vs archives (msgs 3…27) | 16/16 PASS |
| 3 | Scaffolded documents | specs/ = 12; rfcs/ = 75; RFC-0001…0062 exactly once each; ratification records = 0001/0002/0011/0042/0049/0050/0052/0053/0057/0058/0059/0060/0061 (13); all 87 scaffolds carry KB provenance headers and are verbatim from archive | 6/6 PASS |
| 4 | Wiki fidelity & provenance | 1774/1774 archived fenced blocks present in Wiki (byte-exact or trailing-whitespace-normalized); 17 pages with provenance headers; reports message-001…028; 0 broken links | 4/4 PASS |
| 5 | Normative consistency (messages #25–#27 material) | 23 checks: RFC-0053 v1.2 RATIFIED ([244]/[245]/[247], D-81/D-82) + record; RFC-0054/0055/0056 Drafts w/o ratification claims; RFC-0057 v1.3 RATIFIED ([266]/[267], D-85/D-86) + record; RFC-0058 v1.2 RATIFIED ([276]/[277]/[278], C-15) + record; RFC-0059 v1.1 RATIFIED ([281]/[291]/[293]) + record; RFC-0060 v1.1 RATIFIED ([285], D-93) + record; RFC-0061 v1.2 RATIFIED ([300]) + record; RFC-0062 v1.0 Draft (no ratification claim); RFC-Index rows 0053/0057/0058/0059/0060/0061 = RATIFIED; no ratification claims for Draft/Candidate rows (0043/0044/0045/0048/0051/0054/0055/0056/0062); ratified-set sections after msgs #25/#26/#27; D-81…D-93; X-106…X-121; C-15/C-16; Glossary terms 17/17 | 23/23 PASS |
| 6 | RFC parent-chain integrity | all 62 RFC documents carry Parent headers; documented chain RFC-0034…0062 exact (incl. 0043→0028 detour; 0054→0053, 0055→0054, 0056→0055, 0057→0056, 0058→0057, 0059→0058, 0060→0059, 0061→0060, 0062→0061) | 2/2 PASS |
| 7 | Status & cross-page coherence (incl. stale-residue checks) | README 28 messages + current totals (1777/12/75); no stale messages-processed counts; ordering #25→#26→#27→#28 with cumulative totals in order; Code Snippets table row current; Code-Snippets provenance header current; changelog entries messages 1–28 | 6/6 PASS |
| 8 | Traceability bookkeeping | register rows 1…28 contiguous; 15 sub-message indexes; X-01…X-121; D-1…D-93; C-1…C-16; RC-000 §8 mandated directories exist (9/9) | 6/6 PASS |

**Result: 66/66 checks passed after defect remediation (below). No remaining KB defects found. No source content created or altered during this pass.**

## Defects found & corrected (4 — all stale edit residue in bookkeeping/meta text; no verbatim source content touched)

1. **README corpus-status paragraph ordering & stale terminal totals:** during message-#27 processing, the message-#27 sentence had been inserted *before* the message-#26 sentence, ordering the paragraph …#25 → #27 (totals 1777) → #26 (totals 1591/69) and leaving the stale message-#26 totals as the paragraph's final statement. Additionally the message-#25 cumulative totals sentence had been dropped in that edit. Corrected: ordering restored to #25 → #26 → #27, message-#25 totals sentence restored (verbatim from commit 554b941), and "Message #28 = deep verification directive #7." appended. All historical cumulative totals preserved.
2. **Code Snippets corpus-totals line duplicated parenthetical:** the pre-#27 parenthetical breakdown ("(message #2: … message #26: SN-1420…SN-1591, Message #26 Annex at the bottom of this page).") had been left appended after the new #27 breakdown. Removed; the single current breakdown (superset) remains.
3. **README Code Snippets table row stale counter:** "ledger of all 1093 snippets (SN-001…SN-1093)" (stale since message #18) → "ledger of all 1777 snippets (SN-001…SN-1777)".
4. **Code Snippets provenance header stale coverage:** "(messages #2, #3, #5, #8)" / archive list (stale since the bulk commit) → updated to messages #2…#27 with the full archive enumeration (message-002-part1..2 … message-027-part1..5).

Defect class: bookkeeping edit residue — introduced by the message-#27 update (defects 1–2) and long-standing staleness (defects 3–4). Suite #6's substring-based README checks could not detect ordering/terminal-total issues; suite #7 adds explicit ordering, uniqueness, and staleness checks (category 7) that now guard against recurrence.

## Adjudications & regression notes

1. **Ratified set verified:** RC-000, RC-100, RC-200, RFC-0001, RFC-0002, RFC-0011, RFC-0042, RFC-0046, RFC-0047, RFC-0049, RFC-0050, RFC-0052, RFC-0053, RFC-0057 (v1.3), RFC-0058 (v1.2), RFC-0059 (v1.1), RFC-0060 (v1.1), RFC-0061 (v1.2) — each backed by a ratification event in the corpus; RFC-0043/0044/0045/0048/0051/0054/0055/0056/0062 confirmed NOT ratified (Draft/Candidate only).
2. **Conflict log reviewed:** C-1…C-16 coherent; C-13/C-14/C-16 share the ratification-record status-table snapshot pattern (tables preserved verbatim; ratification events authoritative). C-15 (claimed-vs-actual content in [271]/[273] closing paragraphs) remains recorded and resolved-in-place by the [275] second v1.2 iteration.
3. **Regression suites:** message-#18 monotonic regression suite (`message-018-verification-suite.py`) re-executed: **25/25 PASS**, no further patches needed. Message-#27 suite (`message-027-verification-suite.py`) re-executed: **59/59 PASS** after two disclosed monotonicity patches (README messages-processed ≥ 27 instead of == 27; register rows contiguous with max ≥ 27 instead of == 27) — required because message #28 legitimately grew the bookkeeping beyond that suite's point-in-time snapshot; patches alter checks only, no KB content.
4. **Superseded snapshot suites:** `message-019-`, `message-021-`, `message-022-`, `message-023-`, `message-025-`, `message-026-verification-suite.py` encode point-in-time totals (messages/snippets/scaffolds/register ranges) and are superseded by suite #7; they were intentionally not re-scored.

## Verification artifacts

- Reproducible suite: [`message-028-verification-suite.py`](message-028-verification-suite.py) (run from the repository root; final state 66/66 PASS).
- Prior suites: [`message-027-verification-suite.py`](message-027-verification-suite.py) (59/59 after 2 monotonicity patches), [`message-024-verification-suite.py`](message-024-verification-suite.py) (suite #6, 52/52 at message #24), [`message-018-verification-suite.py`](message-018-verification-suite.py) (monotonic regression, 25/25).

## Status

Deep verification complete: the knowledge base is consistent, complete, and fully traceable for all 27 processed content messages ([1]–[300], SN-001…SN-1777, 87 scaffolded documents). Four bookkeeping defects were found and corrected; no source-content fidelity issues remain.
