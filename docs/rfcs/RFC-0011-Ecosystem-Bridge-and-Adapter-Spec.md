# RFC-0011 — Ecosystem Bridge & Adapter Specification

**RFC:** RFC-0011
**Title:** Ecosystem Bridge & Adapter Specification — FFI to Python/Rust Agent Infrastructure (MCP, Vector DBs, LLM SDKs)
**Stable ID(s):** `RED-AI-BRIDGE-001` (new, derives from `RED-COG-ANALYSIS-009` / OP-01)
**Origin:** OP-01 (Ecosystem Bridging) — `AGENT-ENV-ANALYSIS-001 §VII` + `COGOS-ANALYSIS-001 §III` + `RED-COG-ANALYSIS-001 §I/IX` — 60%+ of production agent infra (MCP gateways, LangMem/Mem0/Zep, Neo4j, OpenAI/Anthropic/Google SDKs, embedding libraries, OAuth) is Python/Rust; pure Red isolation was **Rejected** in ADR-001.
**Evolution:** Analysis proposes two adapter classes per AIOS: **native** (pre-defined API invoking CVM syscalls) vs **non-native** (adapter functions bridging external resources). Microsoft Agent Framework 1.0 (6 providers, one-line swap) shows provider-swap feasibility; MCP security gateway + DID identity become mandatory for tool misuse / identity abuse threat model.
**Final Representation:** This RFC + `bridges/cognition/` FFI bindings + MCP gateway capability dialect + `libRedRT-exports.r` extension, sitting between Red/Cognition (goal!→capability!) and Execution Substrate (RFC-0007).
**Status:** `Draft` — P0 **Blocking** (gates production readiness per `07-Implementation-Roadmap.md` Phase 11; without it Red/Cognition is `⚠️ Unsolved` per synthesis table)
**Authors:** Auditor (derivation from OP-01) — to be refined by implementer
**Verification:** Adapter conformance suite: dialect-embedded `http-dialect [GET https://… timeout 30 retry 3]` → HMAC receipt via MCP gateway, with DID identity + behavioural trust scoring.

---

## 1. Abstract

Specifies how Red/Cognition's **dialect-is-tool** promise (RFC-0005) reaches the Python/Rust ecosystem it currently cannot: a typed adapter ABI for MCP gateways, vector DB connectors, LLM SDKs, and embedding pipelines that preserves capability-based, audited execution (RFC-0003 tool pipeline) rather than reimplementing the ecosystem.

## 2. Motivation

ADR-001 decided *Red as substrate for the cognitive core* but *bridged, not isolated* — otherwise every `RECALL query` needing a vector DB would HIT `Open Question`. OP-01 is the only **Blocking** severity Open Problem because no amount of CISA completeness matters if the agent cannot call a search engine.

## 3. Specification

### 3.1 Adapter Taxonomy (normative)

```
Non-Native (e.g., LangMem, Mem0, Zep — Python) ── Adapter Function (typed, capability-gated) ── Native CVM syscall (OBSERVE/RECALL/COMMIT)
Native     (e.g., capability dialect, Red-implemented skill) ── Direct CVM syscall
```

Adapters are **typed**: `capability! [tool: vector-store  policy: safe]` + `permission! [scope: read  expiry: 30min]` — the Capability Analysis pass (RFC-0006) type-checks them identically to native capabilities (Policy-as-Type).

### 3.2 MCP Security Gateway (normative)

- Every non-native tool invocation must pass `Capability Lookup → Policy Evaluation (ABAC proof term) → Budget Check → Sandbox → MCP Gateway → External Tool → HMAC Receipt`.
- Gateway enforces **MCP** (Model Context Protocol) envelope: structured intent declaration (AgenticOS `intent filter`) rather than raw `fork/exec` — the OS as intent filter per `AGENT-ENV-ANALYSIS-001 §I`.

### 3.3 Identity & Trust (normative)

- DID-based identity with behavioural trust scoring per `AGENT-ENV-ANALYSIS-001 §VII` + `COGOS-FRAMEWORK-ANALYSIS-001 §VIII`.
- Every object/event/goal carries trust assertion (GTG-1002: 80–90% of intrusion campaign run by AI agent) — the Trust & Identity Layer in RFC-0004 §3.11.

### 3.4 Excluded Scope

This RFC does **not** re-express vector DB query language as a Red dialect beyond the adapter — it specifies the *boundary* (Cognitive Pipe Protocol `goal!→plan!→call+policy`). A future `RFC-0023` (Skill Composition Algebra) will define richer dialect composition for bundled skills.

## 4. Consequences

- **Trade-off:** One-time binding work (Rust/Python FFI via `libRed` / `system/bridges/java/bridge.red` pattern) vs permanent ecosystem reach.
- **Rejected:** Pure reimplementation in Red (rejected: velocity) and pure Python host (rejected: composability loss — see synthesis).
- **Risk:** Adapter drift (external SDK versioning) → mitigated by cognitive lock file (RFC-0014).

## 5. Traceability

- **OP:** OP-01 (Blocking).
- **ADRs:** ADR-001 (Red as substrate, bridged).
- **REQs:** Extends REQ-002/003 (tool/queue reach).
- **Dependencies:** Upstream RFC-0005 (capability types), RFC-0006 (capability analysis), RFC-0007 (EXECUTE/SANDBOX); Downstream RFC-0014 (lock file must snapshot adapter versions).

## 6. Dependencies

- Upstream: RFCs 0005/0006/0007 + `system/utils/libRedRT-exports.r`.
- Downstream: RFCs 0014 (lock file), 0016 (coherence must cover bridged memory).

## 7. Appendix

- `bridges/java/bridge.java` + `bridges/android/build.r` as precedent for host-language bridging in this repo (verified at `9b5b15a`).
