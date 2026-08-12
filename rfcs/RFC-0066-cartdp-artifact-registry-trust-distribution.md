<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #33, sub-message [397], 2026-08-12
  Verbatim source: knowledge-base/sources/message-033-original-part5.md
  Status in corpus: RFC-0066 CARTDP (Cognitive Artifact Registry and Trust Distribution Protocol) v1.0 (Draft). Dual-lineage numbering divergence (C-21; D-108): the msg#29 scaffold for RFC-0066 was "CPRDP — Cognitive Package Registry and Distribution Protocol" v1.0 [311] (review [312]); msg#33 re-purposes RFC-0066 as CARTDP (artifact index/storage/verification service/trust database/audit ledger; publication, discovery, deterministic dependency resolution on ArtifactID, trust & verification, versioning, revocation, federation). The msg#29 CPRDP form is preserved in archive; scaffold follows the latest lineage. Source quirks preserved as received: §11 lists "RFC-0033 — CPCAVP" and "RFC-0034 — CPRDP" although RFC-0033 is CPCPF and RFC-0034 is CPR-TDP in the earlier corpus. No ratification decision. Review/refinements: [398] (ArtifactRecord schema, registry operations, TrustDomain, RegistryEvent, CognitiveLock).
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->



**RFC-0066 — Cognitive Artifact Registry and Trust Distribution Protocol (CARTDP) v1.0 Draft**

**Version:** 1.0  
**Status:** Draft  
**Parent:** RFC-0065 — Cognitive Proof-Carrying Artifact Format and Verification Protocol (CPCAVP) v1.0 (Draft)  
**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Artifact Registry and Trust Distribution Protocol (CARTDP)** for Red/Cognition.

While RFC-0065 establishes the proof-carrying artifact format (CPCAVP), this specification defines the ecosystem infrastructure for publishing, discovering, distributing, verifying, versioning, revoking, and managing these artifacts across a federated network of registries and Cognitive Operating Systems.

CARTDP completes the distribution and trust layer by specifying the operational mechanisms that enable a global, deterministic, and verifiable cognitive software supply chain.

### 2. Design Principles

CARTDP follows these principles:

- **Trust by Verification** — Artifact acceptance must be based on verifiable proofs, signatures, attestations, and provenance rather than reputation.
- **Deterministic Distribution** — Package resolution must always produce the same artifact given the same query and registry state.
- **Provenance Preservation** — Every artifact must carry its complete compilation, optimization, verification, and ownership history.
- **Capability Awareness** — Distribution and retrieval must respect declared capabilities and security policies.
- **Replay Equivalence** — Distributed artifacts must support deterministic replay across nodes.
- **Provider Neutrality** — The protocol must remain independent of specific reasoning or planning implementations.

### 3. Cognitive Artifact Registry Model

A CARTDP registry consists of:

- **Artifact Index** — Searchable catalog of CPCAVP artifacts with identity, version, capability, and provenance metadata.
- **Artifact Storage** — Immutable storage for CPCAVP containers, CIR representations, and proof certificates.
- **Verification Service** — Performs integrity checks, proof validation, capability analysis, and policy compliance.
- **Trust Database** — Maintains publisher identities, attestations, revocation lists, and trust domains.
- **Audit Ledger** — Immutable record of all registry operations, integrated with the unified event log (RFC-0018).

### 4. Artifact Publication

To publish an artifact, a publisher **MUST**:

1. Submit a valid CPCAVP container (RFC-0065).
2. Provide cryptographic proof of ownership or authorization.
3. Declare required capabilities, effects, and resource requirements.
4. Undergo automated verification by the registry.
5. Receive a signed publication receipt.

### 5. Artifact Discovery

Discovery queries **MUST** support:

- Capability-based search
- Trust level filtering
- Version constraints
- Provenance requirements
- Resource compatibility

Discovery results **MUST** be deterministic given the same query and registry state.

### 6. Dependency Resolution

Dependencies **MUST** reference immutable `ArtifactID` values (including content hashes).

Requirements:

- Resolution **MUST** be deterministic.
- Conflicts (version, capability, resource) **MUST** be reported and resolved according to declared policies.
- The resolved dependency graph **MUST** be recorded in a machine-verifiable lockfile.

### 7. Trust and Verification

Before accepting an artifact, the registry **MUST** verify:

- Cryptographic integrity of the CPCAVP container
- Validity of optimization and correctness proofs (RFC-0032)
- Consistency of the capability manifest (RFC-0006)
- Compliance with registry trust policies (RFC-0025)

Only artifacts that pass verification **MAY** be published.

### 8. Versioning and Evolution

Artifacts **MUST** follow semantic versioning.

Requirements:

- Major version changes **MUST** indicate breaking changes.
- Minor and patch versions **MUST** be backward compatible within the declared conformance level.
- Version transitions **MUST** be recorded in the artifact’s provenance chain.

### 9. Revocation and Retirement

Artifacts **MAY** be revoked or retired by their publisher or by the registry under defined policies.

Revocation **MUST**:

- Invalidate future installations
- Be recorded as a registry event
- Propagate to federated registries where applicable

### 10. Federation

Multiple registries **MAY** federate under defined agreements.

Federation **MUST** preserve:

- Artifact identity and immutability
- Verification status
- Provenance chains
- Trust boundaries between domains

### 11. Relationship to Other RFCs

CARTDP integrates with:

- RFC-0033 — CPCAVP
- RFC-0034 — CPRDP
- RFC-0036 — CBR-SCP
- RFC-0042 — CADP
- RFC-0050 — Architecture and Conformance
- RFC-0059 — CTSTP

### 12. Open Questions

Future specifications may address:

- Concrete wire protocol and API for registry interaction
- Cryptographic signing and attestation profiles for publishers
- Privacy-preserving discovery mechanisms
- Economic and incentive models for registry participation

---

**RFC-0066 — Cognitive Artifact Registry and Trust Distribution Protocol (CARTDP) v1.0 Draft** is now complete.

This RFC establishes the registry and distribution mechanisms required to support a global, deterministic, and verifiable cognitive software supply chain. It completes the distribution layer of the Red/Cognition platform and enables trusted discovery and deployment of verified cognitive artifacts.
