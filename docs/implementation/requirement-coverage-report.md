# Requirement Coverage Report (Stage-5, Phase 25)

**Date:** 2026-08-12 · **Controller:** 2.0.0 · **Scope:** infrastructure only.

## 1. Audit

The manifest had no requirement entity — only tasks with `requirement_refs`
(strings). The system could not detect "requirement with no task," "partial
coverage," or distinguish task PASS from requirement satisfied.

## 2. Confirmed gap (backward-compatible fix)

No requirement coverage model. **Fix:** optional top-level `requirements`
section declaring obligation→task bindings; derived `requirement_statuses`
(SATISFIED/PARTIAL/BLOCKED/NO_COVERAGE) + deterministic `coverage_identity` in
the report. TASK PASS ≠ REQUIREMENT SATISFIED — the ledger is derived, never
authoritative. Seed unaffected (no requirements section → empty ledger).

## 3. Fixes
- `model.Requirement` + `CoverageEntry` dataclasses.
- `manifest._parse_requirements` + KNOWN_TOPLEVEL "requirements".
- `provenance.coverage_identity` + `requirement_statuses` (derived ledger).
- `controller._build_report` includes `requirement_ledger` + `coverage_identity`.

## 4. Attack matrix (RC-01..30)
`tests/test_requirement_coverage.py` (13 cases): no-coverage NO_COVERAGE;
single-PASS SATISFIED; PASS+BLOCKED PARTIAL; multi-partial; all-PASS SATISFIED;
one-invalidated PARTIAL; task-PASS-not-other-req; no-PASS BLOCKED;
retry-no-duplicate; reorder-same-identity; mutated-different-identity;
ledger-derived-not-authoritative; real-repo empty-ledger.

## 5–8. Determinism / stability / recovery / real-repo
Coverage identity deterministic (reorder = same; mutation = different). 5×
stability 298/298. Ledger idempotent across retries. Real-repo: PAUSED,
READY=0, BLOCKED=4, empty ledger.

## Terminology
- **PROVEN BY TEST:** requirement-status derivation, coverage_identity,
  ledger-is-derived-not-authoritative.
- **FORMALLY SPECIFIED:** coverage model (this doc).
- **DOCUMENTED LIMITATION:** coverage is opt-in (declared, not inferred);
  requirement↔task semantic correctness is a planner/review responsibility.

## Files changed
```
tools/impl_controller/model.py        (Requirement, CoverageEntry)
tools/impl_controller/manifest.py     (parse requirements)
tools/impl_controller/provenance.py   (coverage_identity, requirement_statuses)
tools/impl_controller/controller.py   (requirement_ledger in report)
tools/impl_controller/tests/test_requirement_coverage.py (new, 13 cases)
docs/implementation/requirement-coverage-model.md / -report.md
docs/implementation/pipeline-status.json (regenerated)
.github/workflows/implementation-pipeline.yml (RC CI)
```

## Product scope
No product implementation performed. Red/RFC-0075/specifications/Rebol unchanged.
