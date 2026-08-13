# Pipeline Report

**Generated:** 2026-08-13 10:48 UTC
**Pipeline version:** 5.0
**HEAD:** `4b06081ae5b1`

## Executive Summary

| Metric | Value |
|---|---|
| Normative requirements | **1467** |
| RFCs scanned | 75 (19 ratified) |
| Repository modules | 40 (1096 files) |
| Implementation tasks | 4 |
| RFC task coverage | **1.33%** (1/75 RFCs) |
| Structured req→task coverage | **0.0%** |
| Execution frontier | PAUSED |
| Tests | 390 (385 controller + 5 pipeline) |

## Epistemic States (never collapsed)

| State | Count |
|---|---|
| specified | 1467 |
| implemented | 1 |
| executed | 0 |
| tested | 0 |
| validated | 0 |
| evidenced | 0 |
| formally_verified | 0 |

## Stage 1 — Extraction

- **RFCs:** 92 files (75 unique, 19 ratified)
- **Specs:** 52 documents
- **Wiki:** 19 pages
- **Extraction reports:** 35
- **Normative requirements:** 1467 extracted
  - Mandatory (MUST/SHALL): 1192
  - Mandatory-prohibition: 47
  - Recommended (SHOULD): 63
  - Optional (MAY): 165

## Stage 2 — Reconstruction

| Module | Classification | Files |
|---|---|---|
| .appveyor.yml | UNKNOWN | 1 |
| .editorconfig | UNKNOWN | 1 |
| .gitattributes-sample | UNKNOWN | 1 |
| .github | UNKNOWN | 3 |
| .gitignore-sample | UNKNOWN | 1 |
| .travis.yml | UNKNOWN | 1 |
| BSD-3-License.txt | UNKNOWN | 1 |
| BSL-License.txt | UNKNOWN | 1 |
| CODE_OF_CONDUCT.md | UNKNOWN | 1 |
| CONTRIBUTING.md | UNKNOWN | 1 |
| README.md | UNKNOWN | 1 |
| boot.red | UNKNOWN | 1 |
| bridges | SCAFFOLDED | 25 |
| build | SCAFFOLDED | 7 |
| cognition | ABSENT | 1 |
| *...25 more* | | |

**Cognition runtime:** ABSENT

## Stage 3 — Traceability

- Total edges: 24
- Structured coverage: **0.0%**
- Requirements with tasks: 0
- Orphan requirements: 1407
- Informal refs unmatched: 8

## Stage 4 — Planning & Gap Analysis

- Plan valid: True
- Task count: 4
- RFC coverage: **1.33%** (1/75 RFCs)
- Requirements in uncovered RFCs: **1436**

### Tasks

| Task | Status | Blocker |
|---|---|---|
| RED-LEX-001 | BLOCKED | TOOLCHAIN, ARCHITECTURE, PROVISIONING, AUTHORIZATION |
| LIBRED-001 | BLOCKED | DEPENDENCY, TOOLCHAIN |
| HASH-001 | BLOCKED | INCOMPLETE_SPECIFICATION, TOOLCHAIN |
| RFC0075-001 | BLOCKED | SPECIFICATION_CONFLICT, INCOMPLETE_SPECIFICATION |

## Stage 5 — Control

| Metric | Value |
|---|---|
| BLOCKED | 4 |
| DEFERRED | 0 |
| DISCOVERED | 0 |
| FAIL | 0 |
| IN_PROGRESS | 0 |
| PASS | 0 |
| PLANNED | 0 |
| READY | 0 |
| REJECTED | 0 |

**Evidence integrity:** True

## Implementation Gap Summary

```
specified(1467) > implemented(1) > executed(0)
  > tested(0) > validated(0)
  > evidenced(0) > formally_verified(0)
```

- **74** RFCs with **1436** requirements have NO implementation tasks
- **0** requirements are structurally linked to tasks
- **4** tasks exist, all **BLOCKED** (toolchain/spec prerequisites)
- **Cognition runtime: ABSENT**
- **RFC-0075: independently BLOCKED** (specification conflict)

## Constraints Preserved

- No Red/Rebol/RFC-0075/specification/product modification
- Four seed blockers byte-for-byte unchanged
- Never infers semantic relationships
- Never promotes derived state to authority
- EXTRACTED ≠ SPECIFIED ≠ IMPLEMENTED ≠ EXECUTED ≠ VALIDATED ≠ EVIDENCED
