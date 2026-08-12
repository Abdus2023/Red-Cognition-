<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #22, sub-message [201], 2026-08-11
  Verbatim source: knowledge-base/sources/message-022-original-part*.md
  Status in corpus: RFC-0047 CPMWS v1.2; RATIFIED per ratification decision in review [202] ("Status: Ratified"); supersedes v1.0 ([197]) and v1.1 ([199]) drafts (preserved in archive). Note: the status table in ratification record [215] lists RFC-0047 as "Final Candidate" although the ratification event [202] precedes it - contradiction C-12 recorded; ratification events treated as authoritative.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->


**RFC-0047 — Cognitive Package Manager and Workspace Specification (CPMWS) v1.2**

**Version:** 1.2  

**Status:** Candidate for Final Ratification  

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

### 4. Canonical Manifest Schema

#### 4.1 Workspace Manifest

```

WorkspaceManifest {

    WorkspaceID,

    Name,

    Version,

    Members: [PackageID],

    Dependencies: [PackageID],

    Policies: WorkspacePolicies,

    CompilerProfile,

    RuntimeProfile,

    DeploymentTargets: [Target],

    Registries: [RegistryReference]

}

```

#### 4.2 Package Manifest

```

PackageManifest {

    PackageID,

    Name,

    Version,

    Authors,

    License,

    Dependencies: [PackageID],

    Capabilities: [CapabilityRequirement],

    Resources: ResourceRequirements,

    Build: BuildConfiguration,

    Tests: TestConfiguration,

    Metadata

}

```

### 5. Dependency Resolution Algorithm

Dependency resolution **MUST** be deterministic. A conforming implementation **MUST**:

- Resolve dependencies using immutable `PackageID` values.

- Detect and reject version conflicts, duplicate packages, and cyclic dependencies.

- Record the resolved dependency graph in the lockfile.

- Produce identical lockfiles for the same manifest and registry state.

### 6. Lockfile Format

The lockfile **MUST** contain:

- Exact package identities and content hashes

- Resolved dependency graph

- Capability and resource declarations

- Reproducibility metadata (compiler version, build environment hash)

- Workspace hash

- Optional cryptographic signature

### 7. Build Reproducibility

The package manager **MUST** support reproducible builds by:

- Recording the exact compiler version and flags used

- Capturing the hash of the build environment (where attestation is available)

- Ensuring that the same inputs always produce bit-identical CPCPF artifacts

### 8. Workspace Policies

Workspaces **MAY** declare policies that apply to all member packages, including:

- Minimum trust level for dependencies

- Allowed registries

- Capability restrictions

- Compiler profile

- Reproducibility mode

These policies **MUST** be inherited by member packages unless overridden.

### 9. Registry Mirrors and Offline Support

The package manager **SHOULD** support:

- Local mirrors

- Offline registries

- Cache registries

- Air-gapped environments

Mirror configuration **MUST** be recorded in the workspace manifest or lockfile for reproducibility.

### 10. Standard CLI

A conforming implementation **SHOULD** provide a standard command-line interface including at least:

```

cog new

cog init

cog add

cog remove

cog update

cog build

cog test

cog publish

cog install

cog search

cog lock

cog verify

cog tree

cog doctor

cog clean

```

### 11. Package Lifecycle Events

Package lifecycle transitions **SHOULD** emit events in the unified event log (RFC-0018):

```

Created → Built → Verified → Packed → Published → Installed → Updated → Deprecated → Archived

```

### 12. Integration with Other RFCs

CPMWS integrates with:

- RFC-0033 — CPCPF (artifact packaging)

- RFC-0034 — CPR-TDP (registry interaction)

- RFC-0036 — CBR-SCP (build reproducibility)

- RFC-0042 — CADP (deployment manifests)

- RFC-0045 — CTDX (tooling integration)

### 13. Conformance

A conforming CPMWS implementation **SHOULD** provide:

- Workspace and package manifest parsing

- Deterministic dependency resolution

- Lockfile generation and validation

- Reproducible build support

- Integration with at least one registry implementing RFC-0034

If any capability is omitted, the implementation **MUST** document the omission.

### 14. Open Questions

The following areas require future specification:

- Standard workspace layout (non-normative recommendation)

- Cryptographic signing of lockfiles

- Integration with external package registries

- Workspace-level capability and policy inheritance semantics

---

**RFC-0047 — Cognitive Package Manager and Workspace Specification (CPMWS) v1.2** is now ready for **Final Ratification Review**.

This version incorporates workspace profiles, a canonical manifest schema, deterministic dependency resolution, richer lockfile metadata, registry mirror support, standard CLI, package lifecycle events, and workspace policy inheritance, bringing it in line with the precision of the strongest RFCs in the series.
