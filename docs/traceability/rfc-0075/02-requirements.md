# Normative requirements

Extraction is from the authoritative candidate text. Lower-case “must” in §2 is retained because it expresses mandatory design principles; no RFC 2119 boilerplate is supplied. Container REQ-0075-009 is retained separately from its four child rules.

| ID | Source | Keyword | Statement | Classification | Status |
|---|---|---|---|---|---|
| REQ-0075-001 | RFC-0075 §2 | MUST | Cross-domain collaboration must be based on explicit agreements, capabilities, and provenance chains. | Architecture, Capability, Provenance, Sovereignty | SPECIFIED_ONLY |
| REQ-0075-002 | RFC-0075 §2 | MUST | Collaborative decisions and knowledge exchanges must produce reproducible outcomes. | Determinism, Replay | SPECIFIED_ONLY |
| REQ-0075-003 | RFC-0075 §2 | MUST | Federation, collaboration, and knowledge exchange events must participate in the unified event log. | Observability, Replay | SPECIFIED_ONLY |
| REQ-0075-004 | RFC-0075 §2 | MUST | Replayed collaborative executions must produce equivalent observable states. | Replay, Determinism | SPECIFIED_ONLY |
| REQ-0075-005 | RFC-0075 §2 | MUST | Knowledge exchange and collaboration actions must be capability-gated. | Capability, Security | SPECIFIED_ONLY |
| REQ-0075-006 | RFC-0075 §2 | MUST | The protocol must remain independent of specific reasoning or planning implementations. | Architecture, Interoperability | SPECIFIED_ONLY |
| REQ-0075-007 | RFC-0075 §4 | MUST | A FederationAgreement MUST include AgreementID, ParticipatingDomains, SharedCapabilities, KnowledgeSharingRules, CollaborationPolicies, TrustRequirements, DisputeResolutionMechanism, TerminationConditions, and Version. | Data Model, Protocol | SPECIFIED_ONLY |
| REQ-0075-008 | RFC-0075 §4 | MUST | Agreements must be versioned and recorded in the event log. | Data Model, Observability, Replay | SPECIFIED_ONLY |
| REQ-0075-009 | RFC-0075 §5 | MUST | Knowledge exchange between domains must follow the stated exchange rules. | Protocol | SPECIFIED_ONLY |
| REQ-0075-010 | RFC-0075 §5 | MUST | Exchange must be capability-gated. | Capability, Security | SPECIFIED_ONLY |
| REQ-0075-011 | RFC-0075 §5 | MUST | The receiving domain must respect provenance and classification of shared knowledge. | Provenance, Privacy, Sovereignty | SPECIFIED_ONLY |
| REQ-0075-012 | RFC-0075 §5 | MUST | Knowledge updates must follow synchronization rules in RFC-0056. | Protocol, Distributed Execution | SPECIFIED_ONLY |
| REQ-0075-013 | RFC-0075 §5 | MUST | All exchanges must generate federation events. | Observability | SPECIFIED_ONLY |
| REQ-0075-014 | RFC-0075 §6 | MUST | The decision process must follow the governance model in RFC-0040. | Governance | SPECIFIED_ONLY |
| REQ-0075-015 | RFC-0075 §6 | MUST | A collaborative decision must be recorded with cross-domain provenance. | Governance, Provenance, Observability | SPECIFIED_ONLY |
| REQ-0075-016 | RFC-0075 §6 | MUST | A collaborative decision must be deterministic and replayable. | Determinism, Replay | SPECIFIED_ONLY |
| REQ-0075-017 | RFC-0075 §7 | MUST | Each shared knowledge item crossing a domain boundary must carry original domain and creator, intermediate domains and transformations, capability context at each transfer, timestamps and logical epochs, and federation agreement references. | Provenance, Sovereignty, Replay | SPECIFIED_ONLY |
| REQ-0075-018 | RFC-0075 §8 | MUST | Federations must follow Proposal, Negotiation, Verification, Agreement, Activation, Operation, Suspension, and Termination lifecycle. | Lifecycle | SPECIFIED_ONLY |
| REQ-0075-019 | RFC-0075 §8 | MUST | Each federation lifecycle transition must generate a FederationEvent. | Lifecycle, Observability | SPECIFIED_ONLY |
| REQ-0075-020 | RFC-0075 §9 | MUST | Trust must be represented explicitly as FederationTrust with DomainID, TrustLevel, TrustEvidence, CertificateChain, RevocationStatus, and ValidityPeriod. | Trust, Identity, Data Model | SPECIFIED_ONLY |
| REQ-0075-021 | RFC-0075 §10 | MUST | Knowledge exchange must be represented as canonical KnowledgeExchange with ExchangeID, SourceDomain, DestinationDomain, KnowledgeObjects, Classification, ProvenanceReference, AgreementReference, CapabilityContext, and IntegrityProof. | Protocol, Data Model, Integrity | SPECIFIED_ONLY |
| REQ-0075-022 | RFC-0075 §11 | MUST | Federations must define the deterministic conflict-resolution workflow Detect, Classify, Evaluate Policies, Negotiate, Resolve, Record Decision. | Governance, Determinism, Lifecycle | SPECIFIED_ONLY |
| REQ-0075-023 | RFC-0075 §12 | MUST | Ownership, provenance, classification, delegation, federation-boundary, and replay invariants must be preserved. | Sovereignty, Provenance, Security, Replay | SPECIFIED_ONLY |
| REQ-0075-024 | RFC-0075 §13 | MAY | Domains may expose governed KnowledgeView objects. | Data Model, Privacy, Sovereignty | SPECIFIED_ONLY |
| REQ-0075-025 | RFC-0075 §14 | MUST | Federation events must follow canonical FederationEvent structure: EventID, AgreementID, Domains, EventType, Subject, Outcome, Provenance, Timestamp. | Data Model, Observability | SPECIFIED_ONLY |
| REQ-0075-026 | RFC-0075 §15 | MUST | All registration and discovery operations must be authenticated. | Identity, Security | SPECIFIED_ONLY |
| REQ-0075-027 | RFC-0075 §15 | MUST | Cross-domain operations must carry verifiable trust assertions. | Trust, Security | SPECIFIED_ONLY |
| REQ-0075-028 | RFC-0075 §15 | MUST | Federation events must be integrity-protected. | Security, Integrity, Observability | SPECIFIED_ONLY |
| REQ-0075-029 | RFC-0075 §16 | MUST | Federation events must be observable via standard observability interfaces. | Observability | SPECIFIED_ONLY |
| REQ-0075-030 | RFC-0075 §16 | SHOULD | Discovery and registration metrics should be exposed under cognition.federation.* namespace. | Observability | SPECIFIED_ONLY |
| REQ-0075-031 | RFC-0075 §17 | SHOULD | A conforming implementation should provide the listed cog federation and cog agent commands. | CLI / Tooling, Conformance | SPECIFIED_ONLY |
