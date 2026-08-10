# RFC-0019 — Red JIT Specification

**RFC:** RFC-0019
**Title:** Red JIT Specification — Hybrid Static+Interpreter Middle Tier
**Stable ID(s):** `RED-JIT-001`
**Origin:** OP-10 (JIT Compiler) — `RED-SPEC-001` Overview + `red.r` toolchain: hybrid approach compiles what it can deduce statically, uses embedded interpreter otherwise; JIT for cases in between has not yet been implemented.
**Evolution:** RFC-0002/0009 noted JIT as `Open Question` / `Implemented` baseline gap; RFC-0006 PGO speculative (PASTE) showed intent-pattern JIT would be richer signal. This RFC ties Red-level JIT to cognitive JIT.
**Final Representation:** This RFC + JIT tier (profiling → tier-up) + WASM backend interaction + `runtime/` JIT boundary.
**Status:** `Draft` — P2 (performance, roadmap 0029 in roadmap)
**Verification:** Deducible-static vs dynamic-interpreted vs JIT-triggered dispatch coverage; no regression to `RED-SPEC-015` evaluator semantics.

---

## 1. Specification

### 1.1 JIT Boundary (normative)

```
Fully Deducible (static compile) → JIT Zone (hot interpreted paths, now compiled) → Residual Interpreter (dynamic)
```

- **Trigger:** Hot `word!` context (frequent `DO` of same block shape) or loop count threshold — profiling per `system/utils/profiler.r`.
- **Tier-up:** JIT-compiled Red → Red/System native (same emitter path `system/emitter.r`); JIT cache invalidated on dialect redefinition.

### 1.2 WASM Interaction (informative)

WASM backend (RFC-0006 CIR alternative) reuses JIT cache as ahead-of-time artifact for embedded targets — JIT profile informs `WASM/Native` split.

## 2. Consequences

- Closes the middle-zone performance gap without changing language semantics.
- Trade-off: JIT compile time vs interpreter overhead — only tier-up when profiling justifies.

## 3. Traceability

- **OP:** OP-10 (Medium).
- **REQ:** REQ-022 extension.

