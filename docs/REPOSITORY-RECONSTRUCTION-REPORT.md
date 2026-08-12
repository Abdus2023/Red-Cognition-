# Repository Reconstruction Report

## Scope
Organization-only pass over the existing extracted corpus. No RFC, source fragment, report, wiki page, code, or test was moved, renamed, merged, or deleted.

## Summary
- Directories created: none. Existing `docs/` was used for generated navigation artifacts.
- RFC files indexed: 92 in `rfcs/`.
- Same-number RFC artifact groups preserved: 17 (see `RFC-ARTIFACT-GROUPS.md`).
- Specifications indexed: 52 in `docs/specifications/`.
- Extracted source fragments indexed: 103.
- Extraction reports indexed: 52.
- Wiki pages indexed: 39.
- Specifications organized: retained in their existing `rfcs/` and `docs/specifications/` paths; RFC navigation links to the RFC corpus.
- Code snippets organized: none relocated. Existing code remains at documented repository paths; no unresolved snippet was identified or created.
- Unresolved repository locations: none introduced. The corpus has no standalone, destinationless snippet artifact in the indexed locations.
- Duplicate/conflicting documents: no documents were merged. RFC status/title conflicts remain preserved, notably the RFC-0075 traceability conflict register.
- Traceability preserved: original paths and contents are unchanged; generated indexes cite repository paths and the RFC-0075 package retains provenance/evidence.

## Consistency check
- Every indexed corpus file has an existing repository path: PASS.
- Every `rfcs/RFC-*.md` file is represented in `RFC-INDEX.md`: PASS.
- Every existing wiki markdown page in `knowledge-base/wiki/` and `docs/wiki/` is represented in `WIKI-INDEX.md`: PASS.
- No code or documentation relocation was performed, so no unsupported destination was guessed: PASS.

Regenerate with `python3 tools/generate_repository_index.py`.
