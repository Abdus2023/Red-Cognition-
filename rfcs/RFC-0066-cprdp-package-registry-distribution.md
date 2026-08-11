<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #29, sub-message [311], 2026-08-11
  Verbatim source: knowledge-base/sources/message-029-original-part3.md
  Status in corpus: RFC-0066 CPRDP v1.0 (Draft). CPRDP parallels RFC-0034 CPR-TDP (registry/trust distribution mechanisms; [311] §1 acknowledges RFC-0034). Review/expansion [312] (PackageID, RegistryState, lifecycle, trust graph, federation). No ratification decision present in corpus. Parent: RFC-0065 CPCPF v1.0 (Draft).
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->



**RFC-0066 — Cognitive Package Registry and Distribution Protocol (CPRDP) v1.0 Draft**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0065 Cognitive Proof-Carrying Artifact Format (CPCPF) v1.0 (Draft)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Package Registry and Distribution Protocol (CPRDP)** for Red/Cognition.

While RFC-0033 introduces the CPCPF artifact format and RFC-0034 defines the registry and trust distribution mechanisms, this specification provides the detailed protocol for how registries operate, how artifacts are published, discovered, versioned, verified, and distributed, and how trust is established and maintained across the ecosystem.

CPRDP completes the distribution layer by specifying the operational rules that enable a global, deterministic, and verifiable cognitive software supply chain.

### 2. Design Principles

CPRDP follows these principles:

- **Deterministic Distribution** — Package resolution must always produce the same result given the same inputs and registry state.

- **Trust by Verification** — Acceptance of artifacts must be based on verifiable proofs, signatures, and attestations rather than reputation alone.

- **Provenance Preservation** — Every artifact must carry its complete compilation, optimization, and verification history.

- **Capability Awareness** — Distribution and installation must respect declared capabilities and policy constraints.

- **Replay Equivalence** — Distributed artifacts must support deterministic replay across nodes.

- **Provider Neutrality** — The protocol must remain independent of specific reasoning or planning implementations.

### 3. Registry Architecture

A CPRDP registry consists of the following components:

- **Package Index** — Searchable catalog of available artifacts with version and dependency information.

- **Artifact Storage** — Immutable storage for CPCPF binaries, CIR representations, and proof certificates.

- **Verification Service** — Performs integrity checks, proof validation, and capability analysis.

- **Trust Database** — Maintains publisher identities, attestations, and revocation lists.

- **Audit Log** — Immutable record of all registry operations, integrated with the unified event log (RFC-0018).

### 4. Package Publication

To publish an artifact, a publisher **MUST**:

1. Submit a valid CPCPF artifact (RFC-0065).

2. Provide cryptographic proof of ownership or authorization.

3. Declare required capabilities, effects, and resource requirements.

4. Undergo automated verification by the registry’s Verification Service.

5. Receive a signed publication receipt upon successful registration.

### 5. Package Discovery

Discovery queries **MUST** support:

- Capability-based search

- Trust level filtering

- Version constraints

- Provenance requirements

- Resource compatibility

Discovery results **MUST** be deterministic given the same query and registry state.

### 6. Dependency Resolution

Dependencies **MUST** be resolved using immutable `PackageID` values that include content hashes.

Requirements:

- Resolution **MUST** be deterministic.

- Conflicts (e.g., version, capability, resource) **MUST** be reported and resolved according to declared policies.

- The resolved dependency graph **MUST** be recorded in a machine-verifiable lockfile.

### 7. Trust and Verification

Before accepting an artifact, the registry **MUST** verify:

- Cryptographic integrity of the CPCPF container

- Validity of optimization and correctness proofs (RFC-0032)

- Consistency of the capability manifest (RFC-0006)

- Compliance with registry trust policies (RFC-0025)

Only artifacts that pass verification **MAY** be published.

### 8. Versioning and Evolution

Packages **MUST** follow semantic versioning.

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

CPRDP integrates with:

- RFC-0033 — CPCPF

- RFC-0034 — CPR-TDP

- RFC-0036 — CBR-SCP

- RFC-0042 — CADP

- RFC-0050 — Architecture and Conformance

### 12. Open Questions

Future specifications may address:

- Concrete wire protocol and API for registry interaction

- Cryptographic signing and attestation profiles for publishers

- Privacy-preserving discovery mechanisms

- Economic and incentive models for registry participation

---

**RFC-0066 — Cognitive Package Registry and Distribution Protocol (CPRDP) v1.0 Draft** is now complete.

This RFC establishes the operational registry and distribution mechanisms required to support a global, deterministic, and verifiable cognitive software supply chain. It completes the distribution layer of the Red/Cognition platform and enables trusted discovery and deployment of verified cognitive artifacts.
