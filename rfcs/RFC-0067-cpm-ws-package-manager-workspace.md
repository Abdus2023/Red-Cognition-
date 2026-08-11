<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #29, sub-message [313], 2026-08-11
  Verbatim source: knowledge-base/sources/message-029-original-part4.md
  Status in corpus: RFC-0067 CPM-WS v1.0 (Draft). Title echoes ratified RFC-0047 CPMWS (Cognitive Package Manager and Workspace Specification); [313] §12 cites RFC-0047 as "Previous workspace concepts" — overlap documented in corpus. §1 cites "RFC-0034 (CPRDP)" where RFC-0034 is CPR-TDP — quirk preserved as received. No ratification decision present in corpus. Parent: RFC-0066 CPRDP v1.0 (Draft).
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->



**RFC-0067 — Cognitive Package Manager and Workspace Specification (CPM-WS) v1.0 Draft**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0066 Cognitive Package Registry and Distribution Protocol (CPRDP) v1.0 (Draft)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Package Manager and Workspace Specification (CPM-WS)** for Red/Cognition.

While RFC-0034 (CPRDP) and RFC-0066 define the registry, distribution, and trust mechanisms for cognitive artifacts, CPM-WS specifies the developer-facing tools, workspace organization, dependency resolution, lockfiles, and build reproducibility required to manage cognitive packages in a deterministic and auditable manner.

CPM-WS ensures that cognitive software development remains reproducible, capability-aware, and aligned with the verified supply chain established in RFC-0036 (CBR-SCP).

### 2. Design Principles

CPM-WS follows these principles:

- **Deterministic Resolution** — The same workspace manifest and lockfile must always resolve to the same set of artifacts.

- **Reproducibility** — Builds from the same workspace definition must produce bit-identical CPCPF artifacts when using identical compiler and environment inputs.

- **Capability Awareness** — Package manifests must declare capability requirements, which the package manager must validate before installation.

- **Traceability** — All package operations that affect runtime state must be recorded in the event log (RFC-0018).

- **Provider Neutrality** — The specification must remain independent of specific registry or storage implementations.

### 3. Workspace Model

A workspace is a directory tree containing at minimum:

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

- Workspace identity and version

- Member packages

- Shared dependencies

- Compiler and runtime configuration

- Default deployment targets

- Workspace-level policies (security, capability, resource)

### 4. Package Manifest

Each package **MUST** contain a manifest declaring:

- Package identity (aligned with RFC-0034 and RFC-0066)

- Version (semantic versioning)

- Dependencies (with immutable `PackageID` references including content hash)

- Capability requirements (RFC-0006)

- Resource requirements (RFC-0024)

- Build configuration

- Test configuration

### 5. Dependency Resolution

Dependency resolution **MUST** be deterministic.

Requirements:

- Dependencies **MUST** reference immutable `PackageID` values.

- Version conflicts, duplicate packages, and cyclic dependencies **MUST** be detected and rejected.

- The resolved dependency graph **MUST** be recorded in the lockfile.

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

- Ensuring that the same inputs always produce bit-identical CPCPF artifacts (RFC-0036)

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

A conforming implementation **SHOULD** provide the following commands:

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

### 12. Relationship to Other RFCs

CPM-WS integrates with:

- RFC-0033 — CPCPF

- RFC-0034 / RFC-0066 — Registry and distribution

- RFC-0036 — Build reproducibility

- RFC-0042 — CADP

- RFC-0045 — CTDX

- RFC-0047 — Previous workspace concepts

### 13. Conformance

A conforming CPM-WS implementation **SHOULD** provide:

- Workspace and package manifest parsing

- Deterministic dependency resolution

- Lockfile generation and validation

- Reproducible build support

- Integration with at least one registry implementing RFC-0034 / RFC-0066

If any capability is omitted, the implementation **MUST** document the omission.

### 14. Open Questions

The following areas require future specification:

- Standard workspace layout (non-normative recommendation)

- Cryptographic signing of lockfiles

- Integration with external package registries

- Workspace-level capability and policy inheritance semantics

---

**RFC-0067 — Cognitive Package Manager and Workspace Specification (CPM-WS) v1.0 Draft** is now complete.

This RFC establishes the developer workspace and package management layer required for reproducible, deterministic, and auditable development of cognitive programs. It bridges the gap between the language, compiler, and distribution layers of the Red/Cognition platform.
