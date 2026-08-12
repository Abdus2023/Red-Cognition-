# Documentation Navigation

This directory retains the existing documentation hierarchy. The links below are generated or organizational navigation only; they do not replace the underlying extracted corpus.

## Repository-level navigation

- [Repository Navigation](REPOSITORY-NAVIGATION.md)
- [Repository Reconstruction Report](REPOSITORY-RECONSTRUCTION-REPORT.md)
- [File Index](FILE-INDEX.md) and [machine-readable inventory](repository-file-index.json)
- [Repository Index Validation](repository-index-validation.json)

## Documentation collections

- [RFC corpus index](RFC-INDEX.md) → [`../rfcs/`](../rfcs/)
- [Architecture index](ARCHITECTURE-INDEX.md)
- [Source and test index](SOURCE-INDEX.md)
- [Explicit dependency map](DEPENDENCY-MAP.md)
- [RFC artifact groups](RFC-ARTIFACT-GROUPS.md)
- [Wiki index](WIKI-INDEX.md)
- [`specifications/`](specifications/) — existing technical specifications
- [`traceability/`](traceability/) — existing traceability packages
- [`wiki/`](wiki/) — existing documentation wiki pages

## Regeneration

```sh
python3 tools/generate_repository_index.py
python3 tools/validate_repository_index.py
```
