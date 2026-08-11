<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #21, sub-message [199], 2026-08-11
  Verbatim source: knowledge-base/sources/message-021-original-part*.md
  Status in corpus: RFC-0047 CPMWS v1.1 (Candidate for Ratification); supersedes v1.0 draft of sub-message [197] (preserved in archive). Review [200]: "Candidate for Ratification (recommended, with a few final refinements)" - conditional ratification recommendation; no ratification decision present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->


**RFC-0047 — Cognitive Package Manager and Workspace Specification (CPMWS) v1.1**

**Version:** 1.1  

**Status:** Candidate for Ratification  

**Parent:** RFC-0046 Cognitive Observability and Diagnostics Protocol (CODP) v1.2 (Candidate)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Package Manager and Workspace Specification (CPMWS)** for Red/Cognition.

While RFC-0034 (CPR-TDP) defines the registry and distribution protocol, and RFC-0033 (CPCPF) defines the verified artifact format, CPMWS specifies the developer-facing package management, workspace layout, dependency resolution, lockfiles, and build reproducibility mechanisms required for practical, large-scale development of cognitive programs.

CPMWS ensures that cognitive packages and workspaces can be managed in a deterministic, reproducible, and auditable manner, consistent with the build reproducibility requirements established in RFC-0036.

### 2. Design Principles

CPMWS follows these principles:

- **Deterministic Resolution** — The same workspace manifest and lockfile must always resolve to the same set of artifacts.

- **Reproducibility** — Builds performed from the same workspace definition must be bit-identical when using the same compiler and environment.

- **Capability Awareness** — Package manifests must declare capability requirements, which the package manager must validate before installation.

- **Traceability** — All package operations must be recorded in the event log where they affect runtime state.

- **Provider Neutrality** — The specification must remain independent of specific package registry implementations.

### 3. Workspace Profiles

Not every development scenario requires the same workspace complexity. CPMWS defines the following standard profiles:

| Profile       | Purpose                                      | Characteristics                              |

|---------------|----------------------------------------------|----------------------------------------------|

| **Single**    | One package                                  | Minimal configuration                        |

| **Workspace** | Multiple packages                            | Shared dependencies, common build configuration |

| **Enterprise**| Large-scale or regulated development         | Policy enforcement, shared caches, audit requirements |

| **Federated** | Cross-domain development                     | Integration with multiple registries and trust domains (RFC-0041) |

Implementations **MUST** document which profiles they support.

### 4. Workspace Model

A workspace is defined as a directory tree containing at minimum:

```

workspace/

├── cog.toml                 # Workspace manifest

├── cog.lock                 # Lockfile (immutable)

├── packages/                # Local packages

├── tests/

├── docs/

├── examples/

└── build/                 # Build artifacts and caches

```

The workspace manifest **MUST** declare:

- Workspace name and version

- Member packages

- Shared dependencies

- Compiler and runtime configuration

- Default deployment targets

- Workspace-level policies (security, capability, resource)

### 5. Package Manifest

Each package **MUST** contain a manifest declaring:

- Package identity (aligned with RFC-0034)

- Version

- Dependencies (with immutable `PackageID` references)

- Capability requirements

- Resource requirements

- Build configuration

- Test configuration

### 6. Dependency Resolution

Dependency resolution **MUST** be deterministic.

Requirements:

- Dependencies **MUST** reference immutable `PackageID` values (including content hash).

- Version resolution **MUST** follow a defined, deterministic algorithm.

- The resulting set of artifacts **MUST** be recorded in the lockfile.

### 7. Lockfile Format

The lockfile **MUST** be machine-readable and human-auditable. It **MUST** contain:

- Exact package identities and content hashes

- Resolved dependency graph

- Capability and resource declarations

- Reproducibility metadata (compiler version, build environment hash)

- Workspace hash

- Optional cryptographic signature

### 8. Build Reproducibility

The package manager **MUST** support reproducible builds by:

- Recording the exact compiler version and flags used

- Capturing the hash of the build environment (where attestation is available)

- Ensuring that the same inputs always produce bit-identical CPCPF artifacts

### 9. Workspace Policies

Workspaces **MAY** declare policies that apply to all member packages, including:

- Minimum trust level for dependencies

- Allowed registries

- Capability restrictions

- Compiler profile

- Reproducibility mode

These policies **MUST** be inherited by member packages unless overridden.

### 10. Registry Mirrors and Offline Support

The package manager **SHOULD** support:

- Local mirrors

- Offline registries

- Cache registries

- Air-gapped environments

Mirror configuration **MUST** be recorded in the workspace manifest or lockfile for reproducibility.

### 11. Integration with Other RFCs

CPMWS integrates with:

- RFC-0033 — CPCPF (artifact packaging)

- RFC-0034 — CPR-TDP (registry interaction)

- RFC-0036 — CBR-SCP (build reproducibility)

- RFC-0042 — CADP (deployment manifests)

- RFC-0045 — CTDX (tooling integration)

### 12. Conformance

A conforming CPMWS implementation **SHOULD** provide:

- Workspace and package manifest parsing

- Deterministic dependency resolution

- Lockfile generation and validation

- Reproducible build support

- Integration with at least one registry implementing RFC-0034

If any capability is omitted, the implementation **MUST** document the omission.

### 13. Open Questions

The following areas require future specification:

- Standard workspace layout (non-normative recommendation)

- Cryptographic signing of lockfiles

- Integration with external package registries

- Workspace-level capability and policy inheritance semantics

---

**RFC-0047 — Cognitive Package Manager and Workspace Specification (CPMWS) v1.1** is now ready for **Final Ratification Review**.

This version incorporates workspace profiles, a canonical manifest schema, standard CLI commands, richer lockfile metadata, registry mirror support, and workspace policy inheritance, bringing it in line with the precision of the strongest RFCs in the series.
