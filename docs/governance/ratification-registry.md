# Ratification Registry — Single Authoritative Source of Truth

**Document class:** Normative governance record
**Status:** Authoritative for all ratification-status questions
**As of:** 2026-08-13
**Baseline audited:** `4b06081ae5b13eb692968a1467e7a46ce6fd1f7a`
**Machine-readable:** [`ratification-registry.json`](ratification-registry.json)

## Purpose

This registry is the **single authoritative source of truth** for which
documents are ratified in the Red/Cognition corpus. Every generated report,
index, dashboard, and traceability artifact that displays a "ratified" count
**MUST read this registry** and must not independently recompute its own count.

Derivation chain (fixed):

```
corpus ratification events + rfcs/*-ratification-record.md scaffolds
                          ↓
                 THIS registry (authoritative)
                          ↓
        generated reports · indexes · dashboards · traceability
```

## Authoritative count

| Measure | Count |
|---|---:|
| RC documents ratified | **3** |
| RFCs ratified | **19** |
| RFCs with scaffolded ratification-record file | 17 |
| RFCs ratified but record file not scaffolded | 2 (RFC-0046, RFC-0047) |
| RFCs conditionally effective | 1 (RFC-0072, on RFC-0071) |
| **Total ratified documents** | **22** |

## Ratified documents

| ID | Title | Record file | Evidence |
|---|---|---|:---|
| RC-000 | Constitution | — | message #3 |
| RC-100 | Architecture Specification | `specs/RC-100-ratification-record.md` | message #3 |
| RC-200 | Language Specification | `specs/RC-200-ratification-record.md` | message #5 |
| RFC-0001 | Cognitive Type System v1.2 | `rfcs/RFC-0001-ratification-record.md` | [72] (msg #8) |
| RFC-0002 | Effect Ordering Model v1.1 | `rfcs/RFC-0002-ratification-record.md` | [76] (msg #8) |
| RFC-0011 | Scheduler and Execution Model v1.2 | `rfcs/RFC-0011-ratification-record.md` | msg #12 |
| RFC-0042 | Cognitive Autonomous Deployment Protocol (CADP) | `rfcs/RFC-0042-ratification-record.md` | msg #18 |
| RFC-0046 | Cognitive Observability and Diagnostics Protocol (CODP) v1.2 | **none scaffolded** | [196] (msg #21) |
| RFC-0047 | Cognitive Package Manager and Workspace Specification (CPMWS) | **none scaffolded** | [202] (msg #22) |
| RFC-0049 | Cognitive Standard Toolchain Specification (CSTS) v1.2 | `rfcs/RFC-0049-ratification-record.md` | [215] (msg #22) |
| RFC-0050 | Red/Cognition v1.0 Architecture and Conformance Specification v1.2 | `rfcs/RFC-0050-ratification-record.md` | [224]/[225] (msg #23) |
| RFC-0052 | Cognitive Testing and Verification Framework (CTVF) | `rfcs/RFC-0052-ratification-record.md` | [235] (msg #23) |
| RFC-0053 | Cognitive Remote Agent Invocation Protocol (CRAIP) | `rfcs/RFC-0053-ratification-record.md` | [244]/[247] (msg #25) |
| RFC-0057 | Cognitive Distributed Transaction and Consistency Protocol (CDTCP) | `rfcs/RFC-0057-ratification-record.md` | [266]/[267] (msg #26) |
| RFC-0058 | Cognitive Transaction Wire Protocol and Message Encoding (CTWP) | `rfcs/RFC-0058-ratification-record.md` | [276]/[277]/[278] (msg #26) |
| RFC-0059 | Cognitive Transaction Security and Trust Profile (CTSTP) | `rfcs/RFC-0059-ratification-record.md` | msg #27 |
| RFC-0060 | Cognitive Virtual Machine Instruction Execution and Scheduling Semantics (CVM-IESS) | `rfcs/RFC-0060-ratification-record.md` | msg #27 |
| RFC-0061 | CVM Instruction Set and Register Architecture (CISA-RA) v1.2 | `rfcs/RFC-0061-ratification-record.md` | msg #27; [301] (msg #29) |
| RFC-0062 | CVM Bytecode Format and Encoding (CVM-BF) v1.3 | `rfcs/RFC-0062-ratification-record.md` | [381] (msg #33) |
| RFC-0063 | CVM Formal Operational Semantics (CVM-FOS) v1.1 | `rfcs/RFC-0063-ratification-record.md` | [385] (msg #33) |
| RFC-0064 | Compiler Correctness and Verified Translation Pipeline (CCC-VTP) v1.1 | `rfcs/RFC-0064-ratification-record.md` | [391] (msg #33) |
| RFC-0072 | CRCP Wire Format and Binary Message Encoding v1.6 | `rfcs/RFC-0072-ratification-record.md` | [339] (msg #30); **conditional** on RFC-0071 |

## Special cases and exclusions

- **RFC-0046, RFC-0047** are ratified per corpus events but their
  ratification-record files were never scaffolded. Ratification status is not
  in doubt; the scaffold gap is recorded, not silently filled.
- **RFC-0072** is ratified effective upon ratification of **RFC-0071**; RFC-0071
  is not ratified, so RFC-0072 is provisionally effective only.
- **RFC-0075** is **not** ratified. It is a Candidate in `rfcs/`. A divergent
  record exists at `docs/specifications/red-deep-technical-spec/RFC-0075-Ratification-Record.md`
  (see CONFLICT-0075-004) and is **not adopted** by this registry.
- The legacy substring heuristic (`status contains "Ratified"`) produced **16**
  and missed RFC-0001 ("Approved for Ratification"), RFC-0046, and RFC-0047.
  That heuristic is retired in favor of this registry.

## Superseded counts

| Location | Stale value | Authoritative value |
|---|---|---|
| `docs/implementation/freeze-baseline.md` (frozen; not edited) | 16 ratified | 19 (registry) |
| `docs/implementation/pipeline-report.md` (regenerated) | 16 ratified | 19 (registry) |
| `docs/implementation/full-pipeline-status.json` (regenerated) | ratified: 16 | ratified: 19 |
