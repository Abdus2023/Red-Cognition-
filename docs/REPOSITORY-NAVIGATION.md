# Repository Navigation

Start at [Documentation Navigation](README.md). These navigation documents organize the existing extracted corpus without relocating, renaming, merging, or deleting any source material.

- [RFC Index](RFC-INDEX.md) — header-derived RFC number, title, status, version, parent, children, and textual related-RFC references.
- [Wiki Index](WIKI-INDEX.md) — existing wiki pages in their current locations.
- [Architecture Index](ARCHITECTURE-INDEX.md) — explicitly named architecture/runtime documents.
- [File Index](FILE-INDEX.md) — corpus inventory and machine-readable companion.
- [Traceability](traceability/rfc-0075/README.md) — existing RFC-0075 evidence package.

## Preserved locations

- `rfcs/`: existing RFC corpus.
- `knowledge-base/sources/`: verbatim extracted source fragments.
- `knowledge-base/reports/`: extraction/verification reports.
- `knowledge-base/wiki/` and `docs/wiki/`: existing wiki material.
- Existing source and test paths remain unchanged; no code snippets were relocated.

## Validation

Regenerate with `python3 tools/generate_repository_index.py` and verify with `python3 tools/validate_repository_index.py`. The validator writes `docs/repository-index-validation.json`.
