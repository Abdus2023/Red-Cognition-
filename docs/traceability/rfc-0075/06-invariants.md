# Invariant traceability

These are **specified properties**, not formal proofs. RFC-0075 §12 names rather than defines them; statements below are minimally derived interpretations and marked inference.

| ID | Statement | Source/dependencies | Verification/status |
|---|---|---|---|
| INV-0075-001 | Ownership authority is not transferred except under governed delegation. | §12; RFC-0074; inference | no formal model/test: UNVERIFIED |
| INV-0075-002 | Shared item provenance remains linked through every cross-domain transformation. | §§7,12 | UNVERIFIED |
| INV-0075-003 | Classification constrains receiving-domain handling. | §§5,12; RFC-0074 | UNVERIFIED |
| INV-0075-004 | Delegated action remains bounded by capability context. | §12; RFC-0006 | UNVERIFIED |
| INV-0075-005 | A transfer cannot escape the governing federation agreement boundary. | §12; inference | UNVERIFIED |
| INV-0075-006 | Replay has equivalent observable state. | §§2,12; RFC-0018 | UNVERIFIED |
| INV-0075-007 | Collaborative decisions have reproducible outcomes for captured inputs. | §§2,6; inference | UNVERIFIED |
| INV-0075-008 | Accepted trust assertion is valid, verifiable and not revoked at evaluation time. | §§9,15; inference | UNVERIFIED |
| INV-0075-009 | Event/agreement interpretation uses the referenced agreement version. | §4/§7; inference | UNVERIFIED |

No Lean/formal model, runtime assertion, or conformance test was located.
