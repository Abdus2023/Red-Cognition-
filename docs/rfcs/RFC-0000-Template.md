# RFC-0000 — Red/Cognition RFC Template & Conventions

**Status:** `Implemented` · **Type:** Meta · **Source:** Auditor-defined (derived from `docs/TRACEABILITY-ARCHIVE.md` Conventions)

This template defines the mandatory structure for all RFCs in `docs/rfcs/`. Every RFC must satisfy the audit's **Provenance Rule**.

---

## Header

```markdown
# RFC-XXXX — Title

**RFC:** RFC-XXXX
**Title:** ...
**Stable ID(s):** `...-001` (maps to docs/wiki filename)
**Origin:** MSG-YY (Conversation location / message reference) — one-line idea where introduced
**Evolution:** How it changed across turns (one paragraph, references to analysis files)
**Final Representation:** This RFC + the architecture component it specifies (e.g., CVM + CISA v0.1)
**Status:** `Draft` | `Implemented` | `Deprecated` | `Open Question`
**Authors:** Conversation author(s) + Analyzer + Auditor
**Verification:** How to verify (test, benchmark, or literature citation)
```

## Body Sections (all required)

1. **Abstract** — one paragraph, what the RFC specifies.
2. **Motivation (Why)** — why created; which failure/limitation it addresses; with Origin citation.
3. **Specification** — normative sections. Verbatim content from `docs/wiki` goes here, reorganised but not silently corrected; any correction (e.g., memory hierarchy) is explicitly marked `**Corrected:** ... (see AGENT-ENV-ANALYSIS-001 §II)`.
4. **Consequences** — decisions, trade-offs, rejected alternatives (table per `docs/traceability/04-Architecture-Decision-Records.md`).
5. **Traceability** — table row(s) from `docs/traceability/02-RFC-Origin-Map.md` + REQ IDs from `03-Requirements-Traceability-Matrix.md` + formal models from `05-Formal-Model-Traceability.md` + OPs from `08-Open-Problems-Registry.md`.
6. **Dependencies** — upstream/downstream RFCs per `06-Dependency-Graph.md`.
7. **Appendix: Wiki Source Mapping** — `docs/wiki` file(s) + line counts that this RFC reorganises.

## Conventions

- `MSG-01..10` numbering is from the reconstructed 10-turn conversation (see `docs/TRACEABILITY-ARCHIVE.md` Message Index). Always cite `Stable ID`.
- `Implemented` means verified against `9b5b15a` baseline or published literature; `Draft` means specified but not yet implemented in `compiler.r`/`runtime/`.
- No early discussion ignored — if an idea was abandoned, list it under *Consequences / Rejected Alternatives* with provenance.
- Use `Open Question` for ADRs where scheduler semantics (preemptive vs cooperative) remains unresolved.

---

*Template version 2026-08-10 v1.1, paired with `docs/TRACEABILITY-ARCHIVE.md` v1.1.*
