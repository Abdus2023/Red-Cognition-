<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #18, sub-message [163], 2026-08-10
  Verbatim source: knowledge-base/sources/message-018-original-part*.md
  Status in corpus: RFC-0034 CPR-TDP v1.0 (Draft); formal draft. Near-identical suggested-scope draft in review [162]; identical duplicate text embedded in [167] (logged as D-58). No review/ratification in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0034 — Cognitive Package Registry and Trust Distribution Protocol (CPR-TDP)**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0033 Cognitive Proof-Carrying Program Format (CPCPF) v1.0 (Draft)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Package Registry and Trust Distribution Protocol (CPR-TDP)** for Red/Cognition.

CPR-TDP provides the ecosystem infrastructure for publishing, discovering, distributing, verifying, versioning, revoking, and managing Cognitive Proof-Carrying Program Format (CPCPF) artifacts across a distributed network of registries and runtimes.

While CPCPF (RFC-0033) defines the structure of an individual verified cognitive artifact, CPR-TDP defines the registry, discovery, trust, lifecycle, and federation mechanisms required for a global cognitive software distribution system.

### 2. Design Principles

CPR-TDP follows these principles:

- **Trust by Verification** — Registries must not rely solely on reputation. Every package must be independently verifiable through CPCPF integrity, signatures, capability manifests, proof certificates, and provenance metadata.
- **Deterministic Distribution** — Package resolution must be deterministic. The same package identifier, version constraints, and registry state must resolve to the same artifact.
- **Provenance Preservation** — Every package must preserve original author identity, compiler version, optimization history, verification environment, and dependency chain.
- **Capability Awareness** — Package installation must evaluate required capabilities, declared effects, resource requirements, and trust requirements before deployment.
- **Federation** — Multiple registries may cooperate while preserving independent trust domains.

### 3. Cognitive Package Model

A package is defined as:

```
CognitivePackage {
    PackageID,
    Name,
    Version,
    PublisherIdentity,
    CPCPFArtifact,
    Dependencies,
    CapabilityManifest,
    TrustMetadata,
    VerificationStatus
}
```

### 4. Package Identity

Every package **MUST** have a globally unique identifier:

```
PackageID {
    Namespace,
    Name,
    Version,
    ContentHash
}
```

Example: `red.cognition.navigation.path-planner@1.4.0`

The `ContentHash` **MUST** be computed over the immutable CPCPF artifact. Any modification to the artifact **MUST** produce a new `PackageID`.

### 5. Registry Architecture

A CPR-TDP registry consists of:

- **Package Index** — Search, version resolution, dependency discovery.
- **Artifact Storage** — CPCPF binaries, CIR representations, proof certificates, metadata.
- **Verification Service** — Signature verification, proof validation, capability analysis.
- **Trust Database** — Publisher identities, revocations, attestations, reputation metadata.
- **Audit Event Log** — Immutable record of all registry operations (integrated with RFC-0018).

### 6. Package Manifest

Every package **MUST** contain:

```
PackageManifest {
    PackageID,
    Publisher,
    RequiredCapabilities,
    DeclaredEffects,
    ResourceRequirements,
    Dependencies,
    MinimumCVMVersion,
    MinimumCISARevision,
    VerificationLevel
}
```

### 7. Package Installation Protocol

Before installation, a runtime **MUST**:

1. Discover the package via the registry.
2. Resolve dependencies deterministically.
3. Download the CPCPF artifact.
4. Verify integrity (hash and signature).
5. Validate proof certificates (via COVF, RFC-0032).
6. Check required capabilities against available grants (RFC-0006).
7. Evaluate against local security policies (RFC-0025).
8. Verify resource requirements against quotas (RFC-0024).
9. Install only if all checks pass.
10. Register the installation in the local event log.

### 8. Dependency Management

Dependencies **MUST** reference immutable `PackageID` values (including `ContentHash`).

Dependency resolution **MUST** be deterministic and respect:

- Version constraints
- Capability compatibility
- Trust level requirements
- Resource constraints

### 9. Trust Levels

CPR-TDP defines the following trust levels:

| Level | Meaning                              | Verification Required                  |
|-------|--------------------------------------|----------------------------------------|
| T0    | Unverified package                   | None                                   |
| T1    | Signature verified                   | Publisher signature                    |
| T2    | CPCPF validated                      | Integrity + capability manifest        |
| T3    | Optimization proofs verified         | COVF certificates (RFC-0032)           |
| T4    | Formally verified package            | Full proof verification                |
| T5    | Hardware-attested package            | Attestation (RFC-0022, RFC-0026)       |

Runtimes **MAY** enforce minimum trust levels via policy.

### 10. Package Revocation

Packages **MAY** be revoked due to:

- Security vulnerabilities
- Invalid or revoked proofs
- Compromised signing keys
- Capability or policy violations

Revocation events **MUST** be recorded in the Cognitive Event Log (RFC-0018) and propagated to federated registries.

### 11. Registry Federation

Multiple registries **MAY** synchronize via CPR-TDP while preserving independent trust domains.

Federation **MUST** preserve:

- Package identity and immutability
- Signature validity
- Provenance chains
- Trust boundaries between domains

### 12. Security Model

CPR-TDP integrates with:

- RFC-0021 — Cognitive Network Protocol (message transport)
- RFC-0022 — Identity and Trust Framework (publisher verification)
- RFC-0025 — Security Policy Language (installation policies)
- RFC-0033 — CPCPF (artifact verification)

Package execution **MUST NOT** bypass capability checks, resource quotas, policy evaluation, or event logging.

### 13. Relationship to Other RFCs

CPR-TDP integrates with RFC-0018, RFC-0021, RFC-0022, RFC-0024, RFC-0025, RFC-0029, RFC-0032, and RFC-0033.

### 14. Open Questions

Future specifications may address:

- Distributed registry consensus model
- Package economics, licensing, and reputation systems
- Privacy-preserving package discovery
- Zero-knowledge proof integration for package verification
- Cognitive package sandboxing
- AI-generated package certification

---

**RFC-0034 — Cognitive Package Registry and Trust Distribution Protocol (CPR-TDP) v1.0 Draft** is now complete.

This RFC establishes the distribution, discovery, verification, and trust infrastructure required for a secure cognitive software ecosystem, enabling verified, traceable, and reproducible deployment of cognitive programs across the Red/Cognition network.
