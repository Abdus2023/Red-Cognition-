# RFC-0017 — Misalignment Detection & Suppression Pre-Execution

**RFC:** RFC-0017
**Title:** Misalignment Detection & Suppression Pre-Execution — Intent-Gated EXECUTE
**Stable ID(s):** `RED-MISALIGN-001`
**Origin:** OP-07 (Misalignment Under Autonomy) — `COGOS-ANALYSIS-001 §X.3` — 180,000 transcripts (Oct 2025–Mar 2026), 698 misaligned autonomous behaviours, 4.9× increase over 6 months; centre for Long-Term Resilience (CLTR) corpus; no reliable suppress-before-execution method; the cognitive kernel must detect and suppress before `EXECUTE`.
**Evolution:** RFC-0003 tool pipeline notes Policy Engine as least mature (Microsoft toolkit, OWASP mapping); RFC-0004 Trust & Identity Layer requires every object to carry trust assertion (GTG-1002). This RFC inserts a pre-EXECUTE gate specifically for misalignment, not just policy violation.
**Final Representation:** This RFC + `INTENT-CLASSIFIER` gate before CISA `EXECUTE` + suppression policy + CLTR-corpus test harness.
**Status:** `Draft` — P0 **Safety-Critical** (the only `Critical — safety` OP with 6-month 4.9× growth rate)
**Verification:** CLTR-derived taxonomy of misaligned intents → classifier must suppress misaligned `EXECUTE` while preserving aligned throughput (precision/recall gate; false-suppression budget).

---

## 1. Specification

### 1.1 Gate Placement (normative)

```
Goal → Capability Lookup → Policy Evaluation → Budget Check → INTENT-CLASSIFIER → EXECUTE → Receipt
                                              ──────────────
                                              NEW: misalignment gate
```

Policy Evaluation catches access-control violations; `INTENT-CLASSIFIER` catches **goal-level misalignment** (e.g., reward-hacking, deceptive alignment) that is policy-compliant but intent-misaligned.

### 1.2 Classifier & Suppression (normative categories)

- **Classifier:** Semantic intent classifier (trained on CLTR corpus + deployment telemetry) that scores every `goal!→plan!` expansion *before* any `EXECUTE` fires. Threshold `THRESHOLD confidence` (RFC-0007) gates.
- **Suppression:** Misaligned expansion is **suppressed**, not rewritten — no autonomous recovery via `llm_self_examine` without human escalation (to avoid laundering). Suppression emits `HMAC receipt` with `suppressed: reason: misalignment` for audit.

### 1.3 Audit & Escalation (normative)

Suppressed intents are logged to `Reflection Log` + `Memory Consolidation` with `source: classifier` and `confidence` — feeding back into the dual-loop reflection (RFC-0004 §3.7) as a critic signal. Repeated suppression of same goal pattern → `escalate to human` (RFC-0005 §3.11 failure semantics).

## 2. Consequences

- **Safety vs Throughput:** Aggressive suppression risks false suppression (aligned goals blocked); conservative suppression risks 698-case growth. Threshold is deployment-tunable, not RFC-fixed — but the *gate placement* is non-negotiable.
- **Rejected:** Post-EXECUTE audit only (rejected: harm already executed).

## 3. Traceability

- **OP:** OP-07 (Critical — safety, P0).
- **REQs:** REQ-005/015 (capability pipeline).
- **Formal model:** CLTR 180k-transcript analysis (2026).

