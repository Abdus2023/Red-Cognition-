# RFC-0018 — Mnemonic Sovereignty Compliance

**RFC:** RFC-0018
**Title:** Mnemonic Sovereignty Compliance — Verifiable Governance Over What May Be Written, Read, Updated, and Forgotten
**Stable ID(s):** `RED-SOVEREIGNTY-001`
**Origin:** OP-09 (Mnemonic Sovereignty Gaps) — `CVM-ANALYSIS-001 §IV` — no system implements all 9 primitives; poisoning now targets procedural experience, graph relations, organisational memory (not just factual entries); write-gate enforcement and verified deletion are acutely deficient.
**Evolution:** RFC-0007 §3.1 introduced `COMMIT` (write-gated) / `FORGET` (verified deletion) but left the 9-primitive checklist implicit; RFC-0011 added graph-shaped attack surface via bridged adapters. This RFC makes the checklist normative and the audit cryptographic.
**Final Representation:** This RFC + 9-primitive attestation + policy dialect `with-sovereignty` + `FORGET` cryptographic attestation.
**Status:** `Draft` — P1 (security, ties to OP-09 severity High)
**Verification:** Heap operations without sovereignty attestation fail; `FORGET` without cryptographic attestation fails audit; poisoning graph-relation injection is write-gate-rejected.

---

## 1. Specification

### 1.1 9-Primitive Checklist (normative)

Every cognitive heap operation must attest:

1. **write-gate** enforcement (pre-consolidation validation, not just input content filter — see `CVM-ANALYSIS-001 §IV`)
2. **read-scope** enforcement (permission! scope per RFC-0005)
3. **who may read** (capability + DID)
4. **when updates authorised** (validity window + trigger)
5. **which states may be forgotten** (forget-policy, not arbitrary `FORGET`)
6. **verified deletion** (cryptographic attestation that forgotten state is irrecoverable from working/episodic/semantic/procedural stores + adapters)
7. **provenance** (full `Sensor→Observation→Reasoning→Decision→Action` chain)
8. **recoverability** (prior checkpoint recallable before verification-window expiry)
9. **auditability** (HMAC receipt per operation)

No system today implements all 9 — this RFC requires attestation coverage for each.

### 1.2 Verified `FORGET` (normative)

```
FORGET memory! [id: #a1b2 attest: HMAC(records: zeroed, graph-edges: invalidated, vectors: purged, adapters: confirmed)]
```

Deletion that only zeros local memory but leaves graph edges or bridged vector entries is **not verified** and audit-fails.

### 1.3 Policy Dialect (informative)

```red
with-sovereignty [gate: write  attest: verified] [
    COMMIT memory! [content: lesson  provenance: chain]
]
```

Sugar over the 9-primitive attestation; expands to CISA `COMMIT`/`FORGET` with HMAC.

## 2. Consequences

- **Security:** Moves heap from content-filter security (filter→store) to gate security (validate→store) — required because poisoning targets have expanded.
- **Trade-off:** Verified deletion is expensive (graph invalidation + vector purge + adapter confirmation); policies may retain longer but with tighter read-scope instead.

## 3. Traceability

- **OP:** OP-09 (High — security).
- **REQs:** REQ-017 (heap routing with MemCube) extends to sovereignty; REQ-019/020 (provenance/GC) are prerequisites.
- **Formal model:** Mnemonic sovereignty (2026), 9 primitives.

