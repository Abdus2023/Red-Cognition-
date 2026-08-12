# Security traceability

| Control | Requirement | Enforcement boundary claimed | Evidence/status |
|---|---|---|---|
| Authentication | REQ-026 | specification-level; runtime mechanism absent | E1 / SPECIFIED_ONLY |
| Trust assertions / certificates / revocation | REQ-020,027 | specification-level; cryptographic profile absent | E1 / SPECIFIED_ONLY |
| Capability authorization | REQ-005,010 | specification-level; RFC-0006 semantic dependency | E1 / SPECIFIED_ONLY |
| Integrity protection | REQ-021,028 | specification-level; algorithm/key/coverage absent | E1 / SPECIFIED_ONLY |
| Policy / sovereignty / provenance | REQ-001,011,014,017,023 | governance/specification level | E1 / SPECIFIED_ONLY |
| Audit / replay protection | REQ-003,004,008,013,019,025,029 | event-log boundary; anti-replay semantics absent | E1 / SPECIFIED_ONLY |

No runtime, registry, federation, or cryptographic control was found in the checkout. “IntegrityProof” does not define a cryptographic control by itself.
