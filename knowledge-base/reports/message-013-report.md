# Extraction Report — Message #13 (directive "Deeply Verification" #2)

- **Processed:** 2026-08-10 · **Source:** user directive "Deeply Verification" — no new corpus content.
- **Documentation sections identified/extracted:** 0 / 0. **Code snippets found/extracted:** 0 / 0.

## Deep audit suite #2 — 50 checks, 7 categories

| # | Category | Checks | Result |
|---|----------|--------|--------|
| 1 | Archive structure | [1]…[120] contiguous (120/120); speaker labels consistent | 2/2 PASS |
| 2 | Snippet annex integrity | SN-001…SN-640 no gaps; 85 groups contiguous; 637 fenced = per-message sum; 640 = 637 + 3 inline | 4/4 PASS |
| 3 | Scaffolded documents | 28/28 byte-exact vs archive; provenance + origin refs correct; counts match (specs=12, rfcs=16) | 3/3 PASS |
| 4 | Wiki fidelity & provenance | 637/637 blocks verbatim in Wiki; 19 pages with provenance; reports for messages 1–12; 9 mandated dirs; 0 broken links | 5/5 PASS |
| 5 | Normative consistency (message-#12 docs) | 25 checks across RFC-0009/0010/0011(+record)/0012/0013 essentials (metadata, lifecycles, tie-breaking, WaitingReason, queue invariant, transaction semantics, ExecutionContext, InstructionTrace, register mutability, opcode families, addressing modes) | 25/25 PASS |
| 6 | Status-claim coherence | ratified set consistent; approved-vs-ratified distinction preserved; RFC-0005 gap recorded; 1 programmatic flag adjudicated false positive (verbatim annex snippets from [114]/[116] status-transition diagrams + window overlap referring to RFC-0011) | 5/5 PASS (after adjudication) |
| 7 | Traceability bookkeeping | register 1…13; 6 sub-message indexes; X-01…X-64; D-1…D-45; C-1…C-8; changelog complete | 6/6 PASS |

## Duplicates/Conflicts

None new. Logs unchanged: D-1…D-45, C-1…C-8.

## Verification status

**Passed — 50/50 checks.** Knowledge base state: 13 corpus messages processed (sub-messages [1]–[120] fully archived), 640 snippets tracked (637 fenced + 3 inline), 28 scaffolded documents, 19 wiki pages, 13 reports, full traceability. No unresolved defects; no content created or altered during this verification pass.
