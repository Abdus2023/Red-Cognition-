# Concurrency Report (Stage-5, Phase 28)

**Date:** 2026-08-12 · **Controller:** 2.0.0 · **Scope:** infrastructure only.

## 1. Audit
The controller uses exclusive fcntl.flock serialization for all non-dry-run operations. The entire run (classify → execute → evidence → checkpoint) is serialized within the lock. No genuine race defects found.

## 2. Genuine race defects: **NONE**

## 3. Test-harness/specification limitations
- Concurrent mutation (manifest/target/HEAD changes between runs) is tested as sequential run→mutate→run, not truly concurrent (external mutation is uncontrollable). This is the correct test approach — the controller's lock prevents concurrent controller runs, but external mutations between runs are correctly handled by contract_id invalidation.
- No thread-level concurrency tested (fcntl is per-process). Documented limitation.

## 4. New tests
`tests/test_concurrency.py` — 20 cases: mutual exclusion (lock held → denied); retry idempotency (no dup); evidence races (serialized); PASS convergence; SIGKILL then recovery; mutation between runs; recovery convergence; derived-state non-authority; stress (10 retries, 10 recoveries, execute+recover); subprocess contention; sequential consistency; seed regression.

## 5. Full regression: **364/364 PASS** (344 prior + 20 concurrency)
## 6. Five-run stability: **5/5 × 364/364 PASS**
## 7. Convergence: sequential and recovery runs converge to identical normalized state. PROVEN BY TEST.
## 8. Mutation-race: mutation between runs invalidates old evidence. PROVEN BY TEST.
## 9. Real frontier: `READY=0 / BLOCKED=4 / PAUSED=true`
## 10. Seed: byte-for-byte unchanged
## 11. Validators: repo-index PASS; RFC-0075 FAIL (blocked)
## 12. Scope: clean
## 13. Commit: (below)

## Files changed
```
tools/impl_controller/tests/test_concurrency.py (new, 20 cases)
docs/implementation/concurrency-model.md / -report.md
docs/implementation/pipeline-status.json (regenerated)
.github/workflows/implementation-pipeline.yml (concurrency CI)
```

## Product scope
No product implementation performed. Red/RFC-0075/specifications/Rebol unchanged.
