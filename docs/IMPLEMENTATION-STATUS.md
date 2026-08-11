# Implementation Status — Red/Cognition (derived from 07-Implementation-Roadmap.md)

**Branch:** `arena/019fec34-red-cognition` · **PR:** #2 vs `audio` · **Snapshot:** `93b25f4` + `08-Open-Problems` scaffold-closed

| Phase | Title | Planned | Actual (this branch) | Gate | Status |
|-------|-------|---------|----------------------|------|--------|
| **-1** | Baseline Verbatim Preservation | Verify `9b5b15a` | `compiler.r` 125703 / `lexer.r` 26389 / `red.r` 25562 pinned | — | ✅ Implemented |
| **0** | Traceability Archive | Audit 9-turn + synthesis MSG-10 | `docs/TRACEABILITY-ARCHIVE.md` v1.1 (814) + `docs/traceability/` (11) + `docs/wiki/` (21 inc. `Red-and-AI-Agents.md`) + `docs/IMPLEMENTATION-STATUS.md` mirror | — | ✅ Delivered (`a10d401`+`cb429d2`) |
| **RFC scaffolding** | RFC 0000→0025 | 26 RFCs per §4.8 | `docs/rfcs/` 0000→0025 (26 files, ~1960 lines) — all P0/P1/P2 + P3 PCA | — | ✅ Draft (26/26) |
| **1** | Type System MVP | 16 types with metadata + 4-dim UQ | `modules/cognition/types.red` (16 object mocks + UQ + validity bi-temporal) + `prototypes/red-cognition-types.red` (121) | Gate A shape | 🟡 Scaffold |
| **2** | Capability Dialects + Proof | `with-authorisation` tactic | `modules/cognition/dialects.red` + `lint.red` `lint-dangerous` (Tier 1) | Gate A shape | 🟡 Mock (lint prints, not compiler reject) |
| **Lint** | Policy/yield/recursion lints | RFC-0012/13/15 enforcement | `lint.red`: `lint-dangerous` / `lint-yield` (N≥5) / `lint-recursion` (base case) | — | 🟡 Mock |
| **3** | CIR / DAG + Lock | CIR emitter + `cognitive.lock` | `lock.red` `generate-lock`/`check-drift`/`recompile-cir` + schema (RFC-0014) | Gate D 1.8–3.7× | 🟡 Scaffold (no `system/compiler.r` patch yet) |
| **4** | Intent/Effect/Optimisation | 5 passes | Not yet (effect inference fixed-point + widening) | — | ⬜ Not started |
| **5** | Memory Substrate | 4-store + promotion + GC | `memory.red` (4-store CoALA + `allocate→route` + `memory-promote` Mem0 gate + `memory-gc` curation + `invalidate-memory` MESI) + `tests/memory-test.red` + `tests/run.red` | Gate B temporal (bi-temporal validAt) | 🟡 Scaffold (mock stores, mock Graphiti) |
| **6** | CVM Core | CISA 30 ops + dual substrates | CISA v0.1 spec in RFC-0007, no `cvm/` VM yet (EXECUTE→COMMIT HMAC mocked) | — | ⬜ Mock only |
| **OP closure** | OP-01→13 | Scaffold → implemented | `08-Open-Problems-Registry.md` now **13/13 Closed (scaffold)** — OP-14 remains Open | — | 🟡 Scaffold-closed (see that file) |
| **CI** | Gate A scaffold check | — | `docs/ci/cognition.yml` (traceability + RFC 0011→0018 presence) — promote via `mv docs/ci/cognition.yml .github/workflows/` | Gate A mock | ✅ Delivered |

**Verification on this commit:**

```
ls docs/rfcs/RFC-*.md | wc -l          # → 26 (0000→0025)
grep -c "Closed (scaffold)" docs/traceability/08-Open-Problems-Registry.md  # → 13
red prototypes/red-cognition-types.red  # prototype 121 lines
red modules/cognition/tests/run.red     # golden-file single-block agent
red modules/cognition/tests/memory-test.red # Gate B bi-temporal
```

**Next 3 commits recommended (incremental, keep PR reviewable):**
1. `red/cognition/` compiler patch — register `goal! plan! belief!` as real datatypes in `runtime/datatypes` + `lexer.r` (requires `build/build.r` encap update) — promotes Phase 1 from scaffold to implemented
2. `modules/cognition/tests/` — make `execute [delete %temp/]` **fail** without token (RFC-0012 Tier 1) as compiler error not lint print — promotes Phase 2 to implemented
3. `cognitive.lock` generator wired to `build/build.r` (RFC-0014) — `red --recompile-cir` emits lock with real `cir-hash` and adapter versions, `HMAC` receipt verified by `cvm/` — promotes Phase 3 drift check to implemented

*Source of truth remains `docs/traceability/07-Implementation-Roadmap.md`; this file is operational mirror — update that roadmap and regenerate this status via CI (docs/ci/cognition.yml).*
