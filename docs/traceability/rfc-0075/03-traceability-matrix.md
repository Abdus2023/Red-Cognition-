# Bidirectional traceability matrix

All entries have E1 specification evidence only. `—` means no repository mapping found after source inspection; it is not a claim that no implementation exists anywhere outside this checkout.

| Requirement | Source | Concept | Invariant | Model | RFC dependency | Implementation | Test | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| REQ-0075-001–006 | §2 | Federation collaboration principles | INV-001/006/007 | — | 0006,0018,0074 (semantic) | — | — | EVID-001 (E1) | SPECIFIED_ONLY |
| REQ-0075-007–008 | §4 | Agreement | INV-009 | FederationAgreement | 0018,0074 | — | — | EVID-001 | SPECIFIED_ONLY |
| REQ-0075-009–013 | §5 | Governed exchange | INV-002–006 | KnowledgeExchange, FederationEvent | 0006,0056,0074 | — | — | EVID-001 | SPECIFIED_ONLY |
| REQ-0075-014–016 | §6 | Collaborative decision | INV-006/007 | FederationEvent | 0040,0018 | — | — | EVID-001 | SPECIFIED_ONLY |
| REQ-0075-017 | §7 | Cross-domain provenance | INV-002/005 | provenance chain | 0006,0074 | — | — | EVID-001 | SPECIFIED_ONLY |
| REQ-0075-018–019 | §8 | Lifecycle | INV-009 | FederationEvent | 0018 | — | — | EVID-001 | SPECIFIED_ONLY |
| REQ-0075-020–028 | §9–15 | Trust, contracts, security | INV-001–005/008 | all canonical models | 0022,0025,0074 | — | — | EVID-001 | SPECIFIED_ONLY |
| REQ-0075-029–031 | §16–17 | Observability and CLI | INV-006 | FederationEvent | 0046,0054 (terminology conflict) | — | — | EVID-001 | SPECIFIED_ONLY |

Reverse direction: no CFCKEP implementation symbols or tests were found, hence no implementation-to-requirement chain exists.
