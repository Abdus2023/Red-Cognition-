<!--
  KB-Scaffold Provenance (knowledge-base traceability):
  Origin: corpus message #25, sub-message [249], 2026-08-11
  Verbatim source: knowledge-base/sources/message-025-original-part*.md
  Status in corpus: RFC-0054 CADFP v1.0 (Draft). Scope proposed in [248] (control plane vs CRAIP data plane; FederationManifest/AgentRegistration/DiscoveryQuery schemas). Review [250] recommends seven v1.1 additions (discovery resolution algorithm, registry state machine, FederationAgreement schema, consistency model, lease renewal, registry replication, capability negotiation); no v1.1 or ratification present in corpus.
  Placement rationale: RC-000 section 8 "Repository Governance" mandates rfcs/.
  Content below is the document text exactly as provided (no edits).
-->


**RFC-0054 — Cognitive Agent Discovery and Federation Protocol (CADFP) v1.0 Draft**

**Version:** 1.0  

**Status:** Draft  

**Parent:** RFC-0053 Cognitive Remote Agent Invocation Protocol (CRAIP) v1.2 (Ratified)  

**Date:** 2026-07-29

---

### 1. Introduction

This RFC defines the **Cognitive Agent Discovery and Federation Protocol (CADFP)** for Red/Cognition.

While CRAIP (RFC-0053) specifies the mechanisms for invoking remote cognitive agents, CADFP defines the control-plane mechanisms for discovering, registering, authenticating, organizing, and monitoring agents across distributed Cognitive Operating Systems (CogOS instances) and trust domains.

CADFP enables the formation of federated cognitive ecosystems in which independent domains can discover and collaborate with agents while preserving determinism, traceability, capability enforcement, and replay equivalence.

### 2. Design Principles

CADFP follows these principles:

- **Control Plane Separation** — Discovery and federation are distinct from invocation (CRAIP).

- **Deterministic Discovery** — Agent discovery and resolution must produce reproducible results.

- **Capability Awareness** — All discovery and federation operations must be capability-gated.

- **Traceability** — All discovery, registration, and federation events must participate in the unified event log (RFC-0018).

- **Provider Neutrality** — The protocol must remain independent of specific reasoning or planning mechanisms.

- **Federation without Centralization** — Domains may cooperate while retaining independent governance.

### 3. Federation Architecture

A **Cognitive Federation** is a set of cooperating Cognitive Domains (RFC-0041) that share discovery, identity, and capability information under defined trust and policy agreements.

CADFP defines three primary roles:

- **Registry Node** — Maintains agent directories and supports discovery queries.

- **Agent Node** — Hosts cognitive agents and participates in discovery and federation.

- **Federation Gateway** — Mediates cross-domain discovery and trust negotiation.

### 4. Agent Registration

Every agent that wishes to be discoverable **MUST** register with at least one registry node.

#### 4.1 Agent Registration Record

```

AgentRegistration {

    AgentManifest,

    RegistrationTime,

    LeaseDuration,

    HealthEndpoint,

    DiscoveryScopes,

    TrustAssertions,

    FederationAgreements

}

```

Requirements:

- Registration **MUST** include a valid `AgentManifest` (RFC-0053).

- Registration **MUST** be capability-gated.

- Registrations **MUST** be time-bounded via `LeaseDuration` unless explicitly marked as permanent.

### 5. Agent Discovery

CADFP defines a query-based discovery model.

#### 5.1 Discovery Query

```

DiscoveryQuery {

    RequiredCapabilities,

    RequiredRFCs,

    RuntimeVersion,

    SecurityLevel,

    Region,

    Constraints

}

```

#### 5.2 Discovery Response

```

DiscoveryResponse {

    MatchingAgents: [AgentManifest],

    TrustAssertions,

    FederationContext

}

```

Discovery responses **MUST** be deterministic given the same query and registry state.

### 6. Capability Advertisement

Agents **MUST** advertise their capabilities during registration and discovery.

Requirements:

- Advertised capabilities **MUST** match the agent’s current grants (RFC-0006).

- Capability advertisements **MUST** include version and scope information.

- Revocation of a capability **MUST** trigger an immediate update to the agent’s discovery record.

### 7. Federation Topology

CADFP supports multiple federation topologies, including:

- Hierarchical (parent/child domains)

- Peer-to-peer

- Hub-and-spoke

- Mesh

Topology information **MUST** be expressed in a `FederationManifest`:

```

FederationManifest {

    FederationID,

    Name,

    Version,

    Members,

    TrustDomain,

    DiscoveryPolicy,

    RoutingPolicy,

    SecurityPolicy,

    SupportedRFCs

}

```

### 8. Trust Domains

CADFP supports the definition of **Trust Domains** (RFC-0041) that scope identity, capability, and policy visibility.

Cross-domain operations **MUST** be explicitly authorized via federation agreements.

### 9. Membership Lifecycle

Agent and domain membership in a federation follows this lifecycle:

```

Registered

   ↓

Active

   ↓

Suspended

   ↓

Expired / Revoked

   ↓

Deregistered

```

All membership transitions **MUST** generate federation events.

### 10. Health Monitoring

Agents **SHOULD** expose a health endpoint.

The registry **MUST** support health-based discovery filters (e.g., only return healthy agents).

Health status changes **MUST** be propagated as federation events.

### 11. Directory Synchronization

Registries **MAY** synchronize agent directories across federation boundaries.

Synchronization **MUST** preserve:

- Agent identity and versioning

- Capability state

- Trust assertions

- Provenance

### 12. Federation Policies

Federations **MAY** define policies governing:

- Who may register

- What capabilities may be advertised

- Cross-domain access rules

- Health and liveness requirements

Policies **MUST** be expressed using the Cognitive Security Policy Language (RFC-0025).

### 13. Federation Events

CADFP defines the following federation event types (integrated with RFC-0018):

- `AgentRegistered`

- `AgentDeregistered`

- `CapabilityAdvertised`

- `CapabilityRevoked`

- `FederationJoined`

- `FederationLeft`

- `HealthStatusChanged`

- `DirectorySynchronized`

### 14. Security Model

CADFP integrates with RFC-0022 (Identity and Trust) and RFC-0025 (Security Policy).

Requirements:

- All registration and discovery operations **MUST** be authenticated.

- Cross-domain operations **MUST** carry verifiable trust assertions.

- Federation events **MUST** be integrity-protected.

### 15. Observability

CADFP integrates with RFC-0046 (Observability).

Requirements:

- Federation events **MUST** be observable via the standard observability interfaces.

- Discovery and registration metrics **SHOULD** be exposed under the `cognition.federation.*` namespace.

### 16. Standard CLI

A conforming implementation **SHOULD** provide the following commands:

```

cog federation join

cog federation leave

cog agent register

cog agent deregister

cog agent discover

cog agent health

cog federation list

cog federation policy

```

### 17. Conformance Profiles

CADFP defines the following conformance profiles:

| Profile       | Capabilities                                      |

|---------------|---------------------------------------------------|

| **Minimal**   | Local registration and discovery                  |

| **Developer** | Minimal + health monitoring                       |

| **Distributed** | Developer + cross-node discovery                |

| **Enterprise**| Distributed + policy enforcement + audit          |

| **Federation**| Enterprise + cross-domain trust negotiation       |

### 18. Relationship to Other RFCs

CADFP integrates with RFC-0020, RFC-0021, RFC-0022, RFC-0041, RFC-0050, and RFC-0053.

### 19. Open Questions

The following areas require future specification:

- Formal federation agreement language

- Cross-federation routing and service discovery

- Privacy-preserving discovery mechanisms

- Automated federation membership management

---

**RFC-0054 — Cognitive Agent Discovery and Federation Protocol (CADFP) v1.0 Draft** is now complete.

This RFC establishes the control-plane mechanisms for discovering, registering, and federating cognitive agents across distributed Cognitive Operating Systems, complementing the invocation-focused CRAIP (RFC-0053) and completing the distributed systems foundation of the Red/Cognition platform.
