# Security

> Provenance: Corpus message #2, sub-messages [4], [6], [10], [12], [18]. Snippet IDs link to [Code Snippets](Code-Snippets.md).

## Capability-Based Execution (sub-message [10])

Rather than invoking commands directly (**SN-060**):

```red
call "rm -rf temp"
```

Execution would pass through capabilities (**SN-061**):

```red
execute [
    delete %temp/
]
```

The runtime checks:

- permissions
- policy
- risk
- sandbox
- audit trail

before performing the action.

## Capability-Based Computing (sub-message [6])

Instead of executing commands directly, every action becomes a capability. This naturally supports least-privilege execution and auditability.

**SN-032**

```text
Goal
   │
   ▼
Capability Lookup
   │
   ▼
Policy Evaluation
   │
   ▼
Budget Check
   │
   ▼
Execution
   │
   ▼
Receipt
```

(Comparison variant with Permission Check and Tool Binding stages: Tool Invocation, [Workflows](Workflows.md) **SN-021** — see duplicate log.)

## Policies Become Types (sub-message [12])

A cognitive language extends the type system with policy predicates; the compiler can reject unsafe plans before execution. Full detail and snippets in [Data Models](Data-Models.md) (**SN-073**, **SN-074**, **SN-075**).

## Security-Related Architecture Placements

- **Capability & Policy Management** is a dedicated layer of the layered cognitive architecture ([8], **SN-039**, [Architecture](Architecture.md)).
- **Capability Analysis** is a new compiler stage before Code Generation ([12], **SN-066**).
- The cognitive toolchain includes a **Capability Verifier** stage ([14], **SN-105**).
- **Tool Permissions** are a managed resource of the cognitive kernel ([6], **SN-026**).
- The **Policy Engine** and **Permission Check** stages gate tool invocation ([4], **SN-021**).
- Policy constraints apply per agent in the multi-agent runtime ([14], see [Components](Components.md)).
- Agent lifecycle includes **Request Permissions** before Execute ([4], **SN-017**).

## Explainability (sub-message [18], agent system prompt)

Every decision must be traceable. Every action should answer:

- Why?
- Based on what evidence?
- Which memory?
- Which policy?
- Which goal?
- Which reasoning path?

## Related pages

[Data Models](Data-Models.md) · [Workflows](Workflows.md) · [Architecture](Architecture.md) · [Design Decisions](Design-Decisions.md)

---

## Message #3 additions — Normative security requirements (RC-000, RC-100)

### Capability Architecture (RC-100 §9; RC-000 §3.1.10)

Capabilities are first-class and explicit:

- Every action that affects external state **MUST** be mediated by a capability.
- Capability grants **MUST** be auditable and revocable.
- The capability model **MUST** support least-privilege execution.

### Security Architecture (RC-100 §11; principles per [28] §8)

Least privilege by default · Explicit capability grants · Deterministic permission evaluation · Full execution auditability · Trusted provenance for all cognitive actions (+ [28]: reproducible reasoning, secure persistence).

### Mediation invariant ([40] §7)

An agent does not directly perform effects. Incorrect: Agent → File System. Correct: Agent → Capability → Permission Check → File System.

### Constitution clause

"Security, capability isolation, and verification are first-class concerns" — Foundational Principle 10 (RC-000 §3.1; identical in all drafts since [22]).

---

## Message #4 additions — Ratified security boundaries (msg#4 [47]–[60])

### Cognitive evaluation boundary (RC-200 §5.1, ratified)

"A cognitive block SHALL have no external effect unless passed through an approved cognitive evaluation boundary." Prevents accidental execution ([46]).

### Runtime capability enforcement (RC-400 §10, RC-500 §7)

All external effects MUST be mediated by capabilities; capability checks MUST occur before effect execution; capability grants MUST be auditable; capability violations MUST produce traceable errors. Enforcement boundary flow ([56]): Agent → Capability Check → Effect Execution → Trace Record. "No external effect bypasses capability verification."

### Compiler security rules (RC-300 v1.1 §9)

Compiler MUST NOT: execute generated plans · access agent capabilities · modify external state · invoke autonomous actions. Compiler MAY: validate capability requirements · simulate static properties · generate verification metadata. Trust boundary ([54]): Untrusted Source → Compiler → Verified Runtime Input → Cognitive Runtime.

### Shell security boundary ([60])

Shell MUST NOT directly modify cognitive state or bypass capability checks. Human intervention implemented through capability requests, approvals, and runtime inspection rather than direct state manipulation (ADR-0008). State Visibility Levels restrict exposure: Public / Operator / Debug / Internal.

---

## Message #10 additions — Capability model ratified-grade detail (RFC-0006 v1.2, [93]; approved [94])

- **Deterministic resolution order** (short-circuit): exists → active → scope valid → not expired → not revoked → policy allows → effect executes; failure reason MUST be recorded in trace.
- **Scope immutability** after issuance; **capability DAG** (inheritance/dependencies acyclic; dependent grants blocked until prerequisites active).
- **Grants/revocations are effect! values** — all externally observable state changes remain within RFC-0002.
- **CapabilityTrace** { CapabilityID, AgentID, EffectID, Timestamp, Decision: Allow|Deny } for every usage.
- **Delegation provenance** via `delegated-from: CapabilityID`.
- **Status transition legality:** Revoked→Active ✗, Expired→Active ✗.
- **Replay:** revoked capabilities remain revoked; checks at same causal points.
- **Memory access control (RFC-0008 [99]/[100]):** no cross-agent private memory access without capability; semantic writes capability/policy-controlled; capability requirements table per memory operation.
- **Skill mediation (RFC-0007):** external-effect-producing skill invocations MUST be capability-verified before execution.

---

## Message #12 additions — execution-layer security (msg#12 [112]–[120])

- **Capability check before execution** is a ratified-grade invariant of the CVM pipeline: failed capability check → instruction aborts, failure traced, no partial effects (RFC-0012 §8/[115]; [116] capability chain: Instruction → Validation → Capability Resolution → Execution → Effect Commit; invalid: Capability Missing → Instruction Abort → Trace Failure → No Effect).
- **Register authority separation (RFC-0013 v1.1/[120]):** C-registers Runtime controlled; T-registers write-only by trace engine; S-registers scheduler controlled; "Cognitive programs should not directly modify security-critical registers" ([118]).
- **Checkpoint security (RFC-0010/[104]):** restoration MUST preserve all capability constraints existing at checkpoint time; capability versions validated before restoration.
- **Scheduler capability awareness (RFC-0011, ratified):** scheduling inputs include capability constraints; scheduler events (suspend/resume/preempt/terminate) are effect! values (auditable).
- **Agent isolation (RFC-0009):** no cross-agent private state access without explicit capability authorization.
- **CISA capability declaration:** every instruction declares CapabilityRequirement + EffectClass; capability!/external! instructions MUST be capability-checked (RFC-0013 §9-§10).

---

## Message #14 additions — runtime security boundaries, identity & trust (msg#14 [126]–[140])

- **Runtime security boundary ([126]/[127]):** allowed path Agent → Skill → Capability → Runtime → External Effect; forbidden path "Agent → OS Resource" must never exist; all external effects produced by the runtime MUST pass through the Capability Service; runtime MUST NOT allow direct access to host OS resources by cognitive processes.
- **Service isolation (RFC-0017):** services MUST NOT directly mutate each other's internal state; all inter-service messages deterministic; state-affecting messages MUST be traced.
- **System-wide capability governance (RFC-0019):** centralized granting/revocation policy across all agents; system-level capability auditing; CogOS elevates capabilities from local runtime checks into system policy.
- **Distributed capability rules (RFC-0020):** capability state MUST be synchronized or delegated across nodes; revocation on any node MUST be respected system-wide; "A capability cannot become weaker when crossing a node boundary" ([134]) — preserve authority, scope, expiration, revocation state, provenance.
- **Authentication & trust (RFC-0021 §6):** all cross-node communication MUST be authenticated; nodes MUST present verifiable identity (certificates or capability tokens); messages MAY be signed; capability tokens MUST be verified before granting remote access.
- **Identity & trust framework (RFC-0022):** capability-based authorization ("Trust is expressed through explicit, revocable capabilities rather than implicit permissions"); NodeID MUST be cryptographically verifiable; AgentID constant across migrations; capabilities bound to AgentID; capability tokens MUST carry provenance linking to issuing authority; attestation (software versions, CISA revision, RFC compliance, hardware security e.g. TPM/secure enclaves) MUST be verifiable and recorded when used for authorization; trust domains with explicit cross-domain delegation; identity/trust operations MUST produce event-log events (identity, verifier, outcome, capability/attestation used); replay MUST reproduce authorization decisions.
- **Trust chain ([138]):** Authority → Capability Issuer → Capability Token → Agent/Node → Effect Execution — every action answers: who requested, who authorized, which capability allowed, which node executed, what trace produced it.
- **Consensus security (RFC-0023):** participation MUST be capability-gated; trust chain for consensus: Identity → Authentication → Capability Check → Consensus Permission → Vote/Agreement.
- **Event integrity ([130]):** hash-chain event log (Hash(B + Hash(A))) for tamper detection — safety auditing, regulated environments, agent accountability.
- **Capability binding model question ([122]):** static binding (compiled into bytecode; stronger determinism) vs dynamic binding (resolved at execution; flexibility) — deferred to future RFC.

---

## Message #16 additions — policy language, hardware attestation, proof-carrying trust (msg#16 [141]–[160])

- **CSPL evaluation guarantees (RFC-0025):** deterministic policy evaluation; all decisions traced (PolicyDecisionTrace); replay produces equivalent decisions; default-deny. CSPL governs capability usage, resource allocation, trust relationships, effect authorization across CogOS.
- **Policy violations as exceptions ([144]):** PolicyError { UnauthorizedAction, PolicyConflict, InvalidPolicy, MissingContext, TrustViolation }; violation flow: EFFECT_EMIT + capability present + policy deny → Abort Transaction → Generate ExceptionTrace → No Effect Commit.
- **Hardware access control (RFC-0026):** hardware acceleration MUST NOT bypass capability system or security policies; accelerator access MUST be capability-authorized; policy engines evaluate accelerator-specific constraints (energy budget, attestation); accelerator capability revocation MUST immediately prevent further use; CVM MUST verify hardware attestation before sensitive instructions; attestation results traced; only verified hardware MAY be used for strong-isolation operations. "A cognitive agent cannot simply 'use a GPU' — it must prove: who it is, what hardware is trusted, what policy permits, what capability grants, what quota allows" ([146]).
- **CPCPF security model ([160]):** an agent must provide "my executable code, its meaning, its transformations, its proofs, its permissions, and its replay history"; CogOS can reject deployment before execution via CapabilityManifest check. Artifact integrity: cryptographic hash + digital signature + optional attestation; ArtifactID = CIR Hash + CISA Hash + Proof Hash + Capability Hash — enables reproducible builds, artifact comparison, trust registries, cognitive package repositories.
- **Optimization trust model (RFC-0031/0032):** compiler MUST reject COIL transformations whose verification conditions cannot be satisfied; certificates validated before accepting optimized CIR (structure, proof obligations, TCB acceptability); "Trust the verifier, not the optimizer" — proof-carrying code / verified compilers / microkernel verification lineage.
- **Future proposals preserved:** Policy VM / RFC-0025.1 CSPL Virtual Machine Semantics ([144]); CHAL / RFC-0026.1 Cognitive Hardware Abstraction Layer ([146]); RFC-0034 CPR-TDP Cognitive Package Registry and Trust Distribution Protocol ([160]: signed repositories, capability compatibility checking, proof verification before installation, version negotiation, reputation/attestation).

---

## Message #18 additions — sandbox, supply chain, federation security (msg#18 [161]–[180])

- **Sandbox isolation (RFC-0035):** isolation applies to memory, capabilities, effects, hardware resources, network access, persistent storage; all access via capability checks (RFC-0006), security policies (RFC-0025), resource quotas (RFC-0024); fault containment — failing process MUST NOT corrupt other agents, shared memory, system services, global event history; Effect Gateway mediates all external effects (Cognitive Program → Effect Gateway → Capability Check → Policy Evaluation → External Effect); hardware acceleration mediated through sandbox controls (capability authorization, checkpointable hardware state, attestation verification, failure containment); quota violations → exception event → policy evaluation → suspend/terminate.
- **Registry trust (RFC-0034):** "Trust by Verification" — registries MUST NOT rely solely on reputation; independent verifiability via CPCPF integrity, signatures, capability manifests, proof certificates, provenance; trust levels T0–T5 enforceable by policy; revocation (vulnerabilities, invalid proofs, compromised keys, capability/policy violations) recorded in RFC-0018 event log and propagated to federated registries; federation preserves identity/immutability, signature validity, provenance chains, trust boundaries.
- **Supply chain (RFC-0036):** deterministic builds (bit-identical output for identical inputs); complete machine-verifiable provenance chain; tamper resistance; all artifacts signed by producing compiler or trusted authority; registries verify signatures + proofs before acceptance; runtimes re-verify before execution; build environment attestation enables "only accept builds from attested compilers".
- **Ownership & lineage integrity (RFC-0039):** ownership transfer capability-gated and event-recorded; creator attribution immutable; lineage graph acyclic; capability inheritance preserves provenance; parent-capability revocation propagates to inherited/delegated capabilities.
- **Governance security (RFC-0040):** governance participation capability-gated; deterministic/replayable voting; decisions cannot bypass capabilities, quotas, policies, proofs, audit logs.
- **Federation security (RFC-0041):** cross-domain operations capability-gated; DomainID globally unique and verifiable; cross-domain capabilities carry delegation chains; receiving domain verifies provenance/validity; revocation propagates to all federated domains; trust negotiation produces auditable events.
- **Deployment security (RFC-0042):** 7-step validation pipeline mandatory; evolution actions follow governance (RFC-0040); quarantine of faulty artifacts; rollback semantics ([178]: restore verified CPCPF + capability bindings + resource allocations + checkpoint state, generate rollback event, preserve audit history).

## Message #21 additions — observability security, workspace policy, package trust (msg#21 [181]–[200])

- **CODP security & privacy** ([193]/[195] §5): access to observability data MUST be capability-gated; sensitive fields MAY be redacted per policy; trace data MAY be encrypted at rest/in transit; retention policies MUST be defined and auditable; all access MUST be logged. Rationale: traces may contain beliefs, goals, plans, memory contents, capability usage.
- **Capability-aware language semantics** ([181] §2/§6): all operations that may produce external effects must be expressible with explicit capability requirements; cognitive operations are subject to capability checks before producing external effects. Effect/capability annotations proposed at source level ([182] §7–8; aligns with RFC-0002).
- **CSL capability discipline** ([185] §7): effectful operations MUST declare their EffectClass and required capabilities; reflection operations MUST respect capability and policy constraints ([185] §10).
- **Workspace policies** ([199] §9): workspaces MAY declare minimum trust level, allowed registries, capability restrictions, compiler profile, reproducibility mode; policies MUST be inherited by member packages unless overridden (builds on RFC-0025).
- **Package trust & verification** (proposed, [200] §3): installation should verify package signature, proof validity, PackageID hash, and registry trust chain before accepting a package (extends CPCPF/CPR-TDP trust).
- **Registry mirrors / offline operation** ([199] §10): local mirrors, offline registries, cache registries, air-gapped environments; mirror configuration MUST be recorded in manifest/lockfile for reproducibility.

## Message #22 additions — FFI security, toolchain provenance, conformance (msg#22 [201]–[220])

- **CFFI security model ([203]/[205]):** foreign calls MUST NOT bypass the security/isolation/policy models of the Cognitive Runtime and CogOS; all effect-producing foreign calls pass through the capability system (RFC-0006) and security policies (RFC-0025); capability violations MUST produce traceable exceptions; sandboxing levels Trusted/Sandboxed/WASM/Remote/Verified (aligns with RFC-0035).
- **FFI determinism safety ([205]):** non-deterministic foreign calls MUST record results in the trace; replays MUST use recorded values (replay equivalence across the FFI boundary).
- **Package supply chain ([201]):** lockfile optional cryptographic signature; registry mirrors recorded for reproducibility; workspace policy inheritance (minimum trust level, allowed registries, capability restrictions) per [199]/[201]. Proposed v2.0 extensions ([202]): dependency classes, feature flags, package signing (algorithm/trust roots/revocation/transparency log/timestamping), registry resolution precedence.
- **Toolchain provenance (CSTS §15, [211]):** emitted artefacts SHOULD carry provenance metadata (compiler/plugin/package-manager versions, build pipeline revision, RFC compatibility profile); complements RFC-0036 reproducibility.
- **Conformance as verifiable artifact (RFC-0050 §5):** implementations MUST declare conformance level and supported RFCs via machine-readable ConformanceManifest ([219], [220]).
