# Conditional ratification-record reconciliation

This document preserves the separation between the target candidate RFC and the later repository artifact `docs/specifications/red-deep-technical-spec/RFC-0075-Ratification-Record.md` (record). It is a reconciliation analysis, **not** an erratum and not an authority to merge incompatible rules. The declared authority hierarchy places a Candidate-for-Ratification RFC above a ratification record; the target remains the source of REQ-0075-001–031.

## Record claims requiring disposition

| Record location | Claim | Candidate counterpart | Disposition |
|---|---|---|---|
| header, lines 1–8 | title is “Cognitive Federation Coordination…”, status Ratified effective on RFC-0074 ratification, parent title differs | target lines 14–18 calls itself Collaboration protocol, Candidate, parent CRPDGSMP Draft | CONFLICT-004; conditional status is internally unresolved |
| lines 17–20 | all conforming implementations MUST follow record-listed controls | target does not adopt this record as an update mechanism | do not map as target requirement |
| lines 25–32 | lifecycle is Proposal → Negotiation → Activation → Amendment → Termination | target lines 100–120 has eight states including Verification, Agreement, Operation, Suspension | incompatible lifecycle |
| lines 34–37 | agreement adds FederationID, FederationName, FederationVersion, FederationRootTrust | target lines 56–65 has different agreement fields | incompatible schema addition |
| lines 39–43 | immutability/amendment and exact-version exchange binding | target requires Version but has no amendment semantics | candidate gap; not silently imported |
| lines 45–51 | deterministic trust state machine | target lists trust fields only | candidate trust-lifecycle gap; not silently imported |
| lines 53–55 | `KnowledgeExchangeObject`, expanded KnowledgeObjects scope | target uses `KnowledgeExchange` | naming/schema conflict |
| lines 57–59 | Agreement Version Invariant | target names six invariants only | additional normative property outside target |
| lines 61–68 | candidate conformance MUST controls / Minimal Interoperable profile | target lines 250–256 defines five different CADFP-labelled profiles | profile conflict |
| lines 70–79 | registry governance and protocol evolution rules | no target analogue | additional record-only controls |
| lines 93–108 | protocol reference/encoding profile expectations | target has no wire-format choice | reinforces GAP-001; does not solve it |

## Required resolution path

1. Establish whether the record is a valid ratification decision and whether RFC-0074’s prerequisite has been met.
2. Publish either a corrected RFC-0075 revision or a scoped erratum that identifies which record additions supersede which target sections.
3. Reconcile title, acronym, parent, lifecycle, object names, schemas, profiles, and normative references.
4. Re-run requirement extraction with new stable IDs only for genuinely new requirements; preserve existing IDs for unchanged claims.
5. Do not claim conforming implementation until the reconciled schema, cryptographic profile, replay rules, implementation, and tests are evidenced.
