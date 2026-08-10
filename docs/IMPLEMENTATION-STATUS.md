# Implementation Status — Red/Cognition (derived from 07-Implementation-Roadmap.md)

**Branch:** `arena/019fec34-red-cognition` · **PR:** #2 vs `audio` · **Snapshot:** `471db90` + `gate` workflow

| Phase | Title | Planned | Actual (this branch) | Gate | Status |
|-------|-------|---------|----------------------|------|--------|
| **-1** | Baseline Verbatim Preservation | Verify `9b5b15a` | `compiler.r` 125703 / `lexer.r` 26389 / `red.r` 25562 pinned | — | ✅ Implemented |
| **0** | Traceability Archive | Audit 9-turn + synthesis | `docs/TRACEABILITY-ARCHIVE.md` v1.1 (814 lines) + `docs/traceability/` (11) + `docs/wiki/` (21) | — | ✅ Delivered (`a10d401` + `cb429d2`) |
| **RFC scaffolding** | RFC 0000→0025 | 26 RFCs per §4.8 | `docs/rfcs/` 0000→0025 (26 files, 1960 lines) | — | ✅ Draft (all 25 normative + template) |
| **1** | Type System MVP | 16 types with metadata | `modules/cognition/types.red` (16 object mocks + UQ + validity) + `prototypes/red-cognition-types.red` | Gate A shape | 🟡 Scaffold (objects, not registered datatypes) |
| **2** | Capability Dialects + Proof | `with-authorisation` tactic | `modules/cognition/dialects.red` (reason/execute/yield/when) | Gate A shape | 🟡 Mock (`do body` not proof term) |
| **3** | CIR / DAG | CIR emitter | Not yet (requires `system/compiler.r` patch) | Gate D 1.8–3.7× | ⬜ Not started |
| **4** | Intent/Effect/Optimisation | 5 passes | Not yet (OP-02/03 lint TBD) | — | ⬜ Not started |
| **5** | Memory Substrate | 4-store + Gate | Not yet (needs Graphiti mock) | Gate B temporal | ⬜ Not started |
| **6** | CVM Core | CISA 30 ops | Not yet (dual substrates) | — | ⬜ Mock only |
| **CI** | Gate A scaffold check | — | `.github/workflows/cognition.yml` — verifies traceability + RFC 0011→0018 presence | Gate A mock | ✅ Delivered |

**How to run Gate A mock today:**

```bash
red prototypes/red-cognition-types.red   # 121-line prototype
red modules/cognition/tests/run.red      # scaffold golden-file (single-block agent)
```

**Next 3 commits recommended (keep PR incremental):**
1. `red/cognition/` compiler patch — register `goal! plan! belief!` as real types in `runtime/datatypes` + `lexer.r` (requires `build/build.r` encap update)
2. `modules/cognition/tests/` — negative test `execute [delete %temp/]` without token must **fail** (RFC-0012 Tier 1) — currently only prints, not rejects
3. `cognitive.lock` generator in `build/build.r` (RFC-0014) — `red --recompile-cir` emits `cognitive.lock` and `HMAC receipt`

*This file is an operational mirror of `docs/traceability/07-Implementation-Roadmap.md`; do not duplicate roadmap logic here — update that file as source of truth and regenerate this status via CI.*
