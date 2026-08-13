# 5-Stage Pipeline Architecture

**Version:** 5.0 · **Controller:** v2.0.0 · **Tests:** 390

## Architecture

```
AUTHORITATIVE KNOWLEDGE
        │
        ▼
┌───────────────┐
│   STAGE 1     │  Extraction: RFCs → normative requirements (1467)
│  EXTRACTION   │  tools/stage1_extract_requirements.py
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   STAGE 2     │  Reconstruction: repository → component classification
│ RECONSTRUCTION│  tools/stage2_inventory.py (40 modules, 1096 files)
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   STAGE 3     │  Traceability: bidirectional requirement↔task graph
│ TRACEABILITY  │  tools/stage3_build_traceability.py (0% coverage surfaced)
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   STAGE 4     │  Planning: implementation-plan.json validated
│   PLANNER     │  docs/implementation/implementation-plan.json (4 tasks)
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   STAGE 5     │  Control: contract→execute→observe→evidence→PASS
│  CONTROLLER   │  tools/run-implementation-pipeline.py (385 controller tests)
└───────────────┘
```

## How to run

```bash
# Full pipeline (all 5 stages)
python3 tools/run-full-pipeline.py

# Individual stages
python3 tools/stage1_extract_requirements.py    # → requirements-inventory.json
python3 tools/stage2_inventory.py               # → repository-inventory.json
python3 tools/stage3_build_traceability.py      # → traceability-graph.json
python3 tools/run-implementation-pipeline.py    # Stage 5 controller

# Tests
python3 tools/impl-controller.py --self-test    # 390 tests
```

## Epistemic states (never collapsed)

```
specified(1467) > implemented(1) > executed(0) > tested(0)
> validated(0) > evidenced(0) > formally_verified(0)
```

## Current findings

| Finding | Detail |
|---|---|
| Normative requirements | 1467 (1192 mandatory, 47 prohibition, 63 recommended, 165 optional) |
| Repository components | 40 modules, 1096 files (580 SCAFFOLDED, 320 AUTHORITATIVE, 72 IMPLEMENTED) |
| Traceability coverage | 0% structured (8 informal refs unmatched; 1407 orphan requirements) |
| Implementation tasks | 4 (all BLOCKED: TOOLCHAIN/DEPENDENCY/INCOMPLETE_SPEC/SPEC_CONFLICT) |
| Execution frontier | READY=0 / BLOCKED=4 / PAUSED=true |
| Cognition runtime | ABSENT (empty .gitkeep only) |
| RFC-0075 | Independently BLOCKED (SPECIFICATION_CONFLICT) |

## Controller capabilities (Stage 5)

- Deterministic contract identity (SHA256 over canonicalized inputs)
- Hash-chained, fsynced evidence (tamper-evident)
- Atomic checkpoint (temp→fsync→os.replace)
- Exclusive fcntl.flock serialization
- Per-command idempotency (skip verified PASS)
- Criterion-level attestation (criterion_evidence_id)
- Execution-result integrity (target_hashes observation)
- Cross-task requirement ledger (SATISFIED/PARTIAL/BLOCKED)
- Crash/recovery fixpoint (recover×10 converges)
- State-machine monotonicity (no PASS resurrection)
- Concurrency safety (single-authority execution)
- External-state consistency (HEAD/manifest/target mutation invalidates)

## Constraints preserved

- No Red/Rebol/RFC-0075/specification/product modification
- Four seed blockers byte-for-byte unchanged
- Legacy task grandfathering (opt-in semantic coverage)
- Never infers semantic relationships
- Never promotes derived state to authority
