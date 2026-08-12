# Gap register

| ID | Requirement(s) | Description / action | Severity | Missing layer | Blocks ratification |
|---|---|---|---|---|---|
| GAP-0075-001 | 007,020,021,024,025 | No types, optionality, validation, canonical encoding or wire format. Define normative schemas. | CRITICAL | specification | true |
| GAP-0075-002 | 018,019 | Lifecycle has no transition guards, actors, authorization, persistence/failure/rollback semantics. Define state machine. | CRITICAL | specification | true |
| GAP-0075-003 | 008,017,021,025,028 | IntegrityProof, trust/certificates and event protection have no cryptographic profile/key/revocation semantics. Define algorithms and verification. | CRITICAL | specification | true |
| GAP-0075-004 | 002,004,016,023 | Deterministic inputs, external input capture, equivalence and replay boundary undefined. Define and test replay model. | CRITICAL | specification | true |
| GAP-0075-005 | 022 | Conflict workflow has no conflict taxonomy, ordering/tie-breaker, policy-version or failure semantics. | HIGH | specification | true |
| GAP-0075-006 | all | No CFCKEP implementation found. Implement at enforced runtime boundaries. | HIGH | implementation | true |
| GAP-0075-007 | all | No CFCKEP tests/conformance suite found. Add unit, integration, replay and security tests. | HIGH | testing | true |
| GAP-0075-008 | 020,027 | Trust lifecycle lacks issuance, validation, expiry/revocation authority and propagation. | HIGH | specification | true |
| GAP-0075-009 | 029,030 | Standard interface/metric schemas and correlations unspecified. | MEDIUM | specification | false |
| GAP-0075-010 | 031 | CLI names are CADFP-oriented and commands lack behavior/profile mapping. | MEDIUM | specification | false |
| GAP-0075-011 | 024 | KnowledgeView authorization/filter evaluation and leakage controls unspecified. | MEDIUM | specification | false |
| GAP-0075-012 | 014,015 | Governance-to-event/ledger transaction and cross-domain decision authority unspecified. | LOW | specification | false |
