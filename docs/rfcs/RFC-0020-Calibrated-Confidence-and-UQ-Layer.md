# RFC-0020 — Calibrated Confidence & UQ Layer

**RFC:** RFC-0020
**Title:** Calibrated Confidence & UQ Layer — 4-Dimensional Uncertainty with Training-Bias Correction
**Stable ID(s):** `RED-UQ-001`
**Origin:** OP-11 (Uncertainty Calibration Layer) — `COGOS-FRAMEWORK-ANALYSIS-001 §III` — next-token objective rewards confident guessing over `I don't know`; raw model confidence untrustworthy; new taxonomy categorises UQ into input/reasoning/parameter/prediction.
**Evolution:** RFC-0004 §3.6 introduced 4-dim table + calibration layer as normative but left slots unspecified. This RFC specifies the `belief!` UQ slots and kernel correction.
**Final Representation:** This RFC + 4-dim UQ per `belief!` + calibration layer + `THRESHOLD` gating semantics.
**Status:** `Draft` — P1 (reliability)
**Verification:** `belief!` with low `reasoning` UQ still `THRESHOLD`-gated; calibration curve measured against held-out “I don’t know” ground truth.

---

## 1. Specification

### 1.1 UQ Slots (normative)

`belief!` gains `uq: [input: 0..1 reasoning: 0..1 parameter: 0..1 prediction: 0..1]` — scalar `confidence` is retained as aggregate but **not sufficient** for gating.

### 1.2 Calibration Layer (normative)

Cognitive kernel applies post-hoc calibration correcting OpenAI Sep 2025 overconfidence bias (trained objective). Raw LLM confidence is input to calibration, not final.

### 1.3 Gating (normative)

`THRESHOLD [reasoning >= 0.8  prediction >= 0.7]` may require multiple dims independently — `input` ambiguity triggers clarify, `parameter` low triggers tier escalation (RFC-0004 table).

## 2. Traceability

- **OP:** OP-11 (High — reliability).
- **REQ:** REQ-008 (4-dim UQ).

