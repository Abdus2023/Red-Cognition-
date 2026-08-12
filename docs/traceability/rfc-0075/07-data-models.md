# Data-model traceability

The RFC presents canonical pseudostructures but declares no grammar for optional fields. Thus each listed field is treated as **listed/required by the shown structure**, while its type, authority, validation and encoding remain `UNSPECIFIED`. Every field has `implementation: MISSING` and `test: MISSING`. The complete machine-readable field register is `traceability.json.models`; stable field IDs are `MODEL-0075-NNN-FieldName`.

| Model ID | Model / source | Fields | Security, provenance and replay role |
|---|---|---|---|
| MODEL-0075-001-* | FederationAgreement, §4 | AgreementID; ParticipatingDomains; SharedCapabilities; KnowledgeSharingRules; CollaborationPolicies; TrustRequirements; DisputeResolutionMechanism; TerminationConditions; Version | contract, policy and agreement-version replay context |
| MODEL-0075-002-* | FederationTrust, §9 | DomainID; TrustLevel; TrustEvidence; CertificateChain; RevocationStatus; ValidityPeriod | trust validity, certificate/revocation context |
| MODEL-0075-003-* | KnowledgeExchange, §10 | ExchangeID; SourceDomain; DestinationDomain; KnowledgeObjects; Classification; ProvenanceReference; AgreementReference; CapabilityContext; IntegrityProof | transfer authorization, integrity and provenance linkage |
| MODEL-0075-004-* | KnowledgeView, §13 | ViewID; VisibleObjects; ClassificationFilter; CapabilityRequirements; ProvenancePolicy | optional governed disclosure/filtering |
| MODEL-0075-005-* | FederationEvent, §14 | EventID; AgreementID; Domains; EventType; Subject; Outcome; Provenance; Timestamp | audit/replay observation |

No types, canonical serialization, validation algorithm, cardinality, identifier uniqueness rule, authority model, or privacy leakage rule is defined. Those omissions are GAP-0075-001, GAP-0075-003, and GAP-0075-011; field presence must not be mistaken for a usable wire schema.
