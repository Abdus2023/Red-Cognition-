<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #18, sub-message [165], 2026-08-10
  Verbatim source: knowledge-base/sources/message-018-original-part*.md
  Status in corpus: RFC-0036 CBR-SCP v1.0 (Draft); review [166] proceeds to RFC-0037. No ratification in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->

**RFC-0036 — Cognitive Build Reproducibility and Supply Chain Protocol (CBR-SCP)**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0035 Cognitive Sandbox and Execution Isolation Model (CSEIM) v1.0 (Draft)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Build Reproducibility and Supply Chain Protocol (CBR-SCP)** for Red/Cognition.

CBR-SCP establishes the mechanisms required to ensure that cognitive programs can be built, verified, and distributed in a fully deterministic, auditable, and tamper-resistant manner. It connects the compiler pipeline (RFC-0027–RFC-0032), the proof-carrying artifact format (RFC-0033), the registry and distribution system (RFC-0034), and the secure execution environment (RFC-0035) into a coherent, end-to-end supply chain.

The goal is to guarantee that any party can independently reproduce a cognitive build from source and verify that the resulting CPCPF artifact has not been altered since compilation.

### 2. Design Principles

CBR-SCP follows these principles:

- **Deterministic Builds** — Identical source, compiler version, and build environment must always produce bit-identical artifacts.
- **Complete Provenance** — Every stage from source to final artifact must be recorded and verifiable.
- **Tamper Resistance** — Any modification to a build artifact or its metadata must be detectable.
- **Replay Equivalence** — Rebuilt artifacts must support identical execution behaviour during replay.
- **Capability and Policy Awareness** — Build processes must respect declared capabilities and security policies.
- **Provider Neutrality** — The protocol must remain independent of specific compilers or hardware.

### 3. Build Reproducibility Requirements

A conforming build system **MUST** guarantee:

- Fixed compiler version and configuration
- Deterministic dependency resolution (via immutable `PackageID` values from RFC-0034)
- Canonical ordering of all inputs (source files, graphs, metadata)
- Reproducible random number generation (when used)
- Fixed timestamps or explicit timestamp normalization
- Bit-identical output for identical inputs

### 4. Build Provenance Chain

Every CPCPF artifact **MUST** carry a complete, verifiable provenance chain:

```
Source Code
   ↓ (deterministic hash)
Compiler Invocation
   ↓ (compiler identity + version + flags)
CIR Generation
   ↓ (CIR hash)
Optimization Passes (COIL + COVF)
   ↓ (transformation certificates + proofs)
CISA Generation
   ↓ (CISA binary hash)
CPCPF Packaging
   ↓ (final artifact hash + signature)
```

Each step **MUST** be recorded in a machine-verifiable format.

### 5. Supply Chain Security

CBR-SCP integrates with:

- RFC-0022 — Identity and Trust Framework (signing and attestation)
- RFC-0025 — Security Policy Language (build-time policy enforcement)
- RFC-0033 — CPCPF (artifact integrity)
- RFC-0034 — CPR-TDP (registry trust)

Requirements:

- All build artifacts **MUST** be signed by the producing compiler or trusted authority.
- Registries **MUST** verify signatures and proof certificates before accepting packages.
- Runtimes **MUST** re-verify artifact integrity before execution.

### 6. Build Environment Attestation

When hardware attestation is available (RFC-0022, RFC-0026), the build process **SHOULD** record:

- Compiler runtime environment
- Hardware security measurements
- Build container or sandbox identity
- Dependency resolution environment

This enables policy enforcement such as “only accept builds from attested compilers.”

### 7. Relationship to Other RFCs

CBR-SCP integrates with RFC-0027–0033 (compiler and artifact layers) and RFC-0022, RFC-0024, RFC-0025 (governance and security).

### 8. Open Questions

The following areas require future specification:

- Concrete build manifest and lockfile formats
- Standardized build container specifications
- Cryptographic signing and attestation formats for build environments
- Automated reproducibility verification tools

---

**RFC-0036 — Cognitive Build Reproducibility and Supply Chain Protocol (CBR-SCP) v1.0 Draft** is now complete.

This RFC establishes the mechanisms required to guarantee that cognitive programs can be built and distributed in a fully deterministic, auditable, and tamper-resistant manner, completing the end-to-end chain from source to verified execution.
