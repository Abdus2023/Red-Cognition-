# RFC-0014 — Cognitive Lock File & Recompile-on-Drift Protocol

**RFC:** RFC-0014
**Title:** Cognitive Lock File & Recompile-on-Drift Protocol — Stable Environment Snapshots for CIR
**Stable ID(s):** `RED-LOCKFILE-001`
**Origin:** OP-04 (CIR Version Mismatch) — `RED-COMPILER-ANALYSIS-001 §X.3` — “recompile-on-drift loop” is response when compiled workflow breaks due to world change; skill registry / capability policies / model availability may have drifted since original compilation; no classical lock file equivalent.
**Evolution:** RFC-0006 §3.7 noted lock file analogy to dependency lock files; RFC-0011 (adapter versions) added drift surface. This RFC formalises the file.
**Final Representation:** This RFC + `cognitive.lock` (env snapshot) + drift detector + recompile trigger policy.
**Status:** `Draft` — P1 (correctness)
**Verification:** Compile A, drift skill registry, attempt execute A without recompile → fails with drift diagnostic; recompile with lock update succeeds; lock diff is human-reviewable.

---

## 1. Specification

### 1.1 `cognitive.lock` Schema (normative, illustrative)

```
; auto-generated — do not edit; see RFC-0014
lockfile 1.0 [
  red-version: 0.6.4
  cir-hash: #a1b2c3...
  skills: [summarize: 1.2.0  vector-store: 3.0.1]
  capabilities: [delete: policy dangerous v2  read: policy safe v1]
  models: [small-local: ollama/llama3  large-remote: openai/gpt-5]
  adapters: [mcp-gateway: 0.4.1  graphiti: 1.0.3]
  provenance: [compiled: 2026-08-10T15:18:00Z  by: a10d401  source: RED-AI-SYNTHESIS-001]
]
```

### 1.2 Drift Protocol (normative)

```
Compile (CIR + lock snapshot) → Execute (check lock vs live env before EXECUTE)
  ├─ no drift → execute + HMAC receipt (RFC-0007 COMMIT)
  └─ drift detected → refuse EXECUTE, emit drift receipt, require `red --recompile-cir`
```

Refusing execution on drift is correctness, not convenience — executing stale capability policies against a new skill registry would be audit-non-compliant.

### 2. Consequences

- **Reviewability:** Lock diff is the audit artifact for env drift.
- **Trade-off:** Compile cache invalidation on any adapter version bump — secured vs stale-speedy.

## 3. Traceability

- **OP:** OP-04 (High — correctness).
- **REQ:** REQ-013 (CIR 4 graphs + budget; lock extends budget stability across time).
- **Dependencies:** Upstream RFCs 0006/0007/0011; informs OP-06/08 coherence (env coherence = goal coherence sibling).

