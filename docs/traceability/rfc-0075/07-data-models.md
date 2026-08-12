# Data-model traceability

All fields are shown as required in the RFC pseudostructures, but **types, encoding, optionality syntax, authority, and validation rules are not specified**. Therefore all implementation/test locations are MISSING.

| Model | Fields | Semantic/security/replay role | Source |
|---|---|---|---|
| FederationAgreement | AgreementID; ParticipatingDomains; SharedCapabilities; KnowledgeSharingRules; CollaborationPolicies; TrustRequirements; DisputeResolutionMechanism; TerminationConditions; Version | authorization/policy contract; Version is replay-critical | §4 |
| FederationTrust | DomainID; TrustLevel; TrustEvidence; CertificateChain; RevocationStatus; ValidityPeriod | trust validity/revocation | §9 |
| KnowledgeExchange | ExchangeID; SourceDomain; DestinationDomain; KnowledgeObjects; Classification; ProvenanceReference; AgreementReference; CapabilityContext; IntegrityProof | transfer authorization, provenance, integrity | §10 |
| KnowledgeView | ViewID; VisibleObjects; ClassificationFilter; CapabilityRequirements; ProvenancePolicy | optional governed disclosure | §13 |
| FederationEvent | EventID; AgreementID; Domains; EventType; Subject; Outcome; Provenance; Timestamp | lifecycle/exchange audit and replay observation | §14 |

Machine-readable field inventory is deliberately limited to the exact canonical field lists above; inventing types would be unsupported. GAP-001 and GAP-003 address this.
