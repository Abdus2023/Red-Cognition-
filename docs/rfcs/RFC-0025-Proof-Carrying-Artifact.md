# RFC-0025 — Proof-Carrying Artifact (Post-RFC-24 Extension)

**RFC:** RFC-0025
**Title:** Proof-Carrying Artifact — Verifiable Cognition Package with Provenance + Proof Terms + HMAC + Version History
**Stable ID(s):** `RED-PCA-001`
**Origin:** Roadmap-derived (beyond MSG-09) — implied by `RED-COMPILER-ANALYSIS-001 §XI`: artefacts carry `provenance / proof terms / parallelism structure / model bindings / revision history` + `TRACEABILITY-ARCHIVE.md` Forward horizon note: not yet in conversation, logical next after durable verified plans.
**Evolution:** RFCs 0006 (CIR) + 0007 (CISA/COMMIT) + 0014 (cognitive lock) together imply an artifact that is the *output* of the compiler and the *input* of the CVM and the *unit* of the lock file. This RFC names that unit.
**Final Representation:** This RFC + proof-carrying artifact (PCA) format.
**Status:** `Draft` — P3 (future, roadmap-derived, correctly flagged as beyond current conversation)
**Verification:** Same CIR inputs → same artifact hash; verifier can check proof terms without re-executing reasoning; drift detection compares lock vs artifact provenance.

---

## 1. Specification

### 1.1 Artifact Envelope (normative, future)

```
proof-carrying-artifact [
    provenance: [who compiled, from what goal, under what policies, when, on what Red version]
    effect-signatures: [observe! remember! modify! …]
    proof-terms: [capability dangerous: token #… ]
    parallelism: [DAG with parallel groups]
    model-bindings: [reason: large-remote  classify: small-local]
    revision-history: [v1: 2026-08-10T…  v2: …]
    hmac: #…   ; audit receipt (RFC-0007 COMMIT)
]
```

The artifact is **the production analogue** of the 2025–26 industry pattern “model decides, something that is not a model executes” — but typed, provenance-carrying, and drift-aware vs untyped JSON blobs.

## 2. Consequences

- **Verifiable cognition:** Intelligence becomes a compilation target whose output is checkable, not just runnable.
- **Roadmap-derived flag:** Correctly marked P3 — not traceable to a user turn, but implied by combined prior RFCs; the archive's only roadmap-derived RFC (see `09-Future-RFC-Roadmap.md` horizon note).

## 3. Traceability

- **OPs:** Closes OP-02/04 ergonomic+lock aspects at artifact granularity.
- **Dependencies:** RFCs 0006/0007/0014 + `07-Implementation-Roadmap.md` Gate A artifact.

