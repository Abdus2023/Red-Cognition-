# RFC-0075 Reconciliation Template — Ratification Patch

**Purpose:** Resolve CONFLICT-0075-002..004 and GAP-0075-001..004 so `validate_rfc_0075_traceability.py` can pass and RFC0075-001 can move from BLOCKED_SPEC_CONFLICT to READY.

**Status:** TEMPLATE — requires governance approval, not implementation via coding.

## Conflicts (per docs/traceability/rfc-0075/16-conflicts.md)

| ID | Authorities | Description | Proposed authoritative choice | Rationale | Approver |
|----|-------------|-------------|-------------------------------|-----------|----------|
| CONFLICT-0075-002 | RFC-0075 §17-18 vs RFC-0054 title/scope | `cog agent register/discover` and "local registration and discovery" profiles appear CADFP discovery content, not CFCKEP federation exchange | Choose: Keep CFCKEP-specific federation trust negotiation in §17-18, move discovery CLI to informative appendix referencing RFC-0054 CADFP, or define mapping: CFCKEP Federation profile MAY use CADFP discovery as underlying transport | Avoids conflating discovery with federation exchange, preserves provider neutrality | <TO_BE_FILLED> |
| CONFLICT-0075-003 | RFC-0075 §2/§§6,11,12 vs §§4,7,14 | Determinism/replay mandatory but canonical types/serialization/input capture absent — internal incompleteness prevents demonstrating claim | Choose: Define canonical encoding (e.g., CBOR or JSON canonical per RFC-8785) + external input capture via FederationEvent Subject/Provenance fields, plus equivalence predicate (deep structural equality excluding Timestamp) | Makes replay verifiable, aligns with determinism principle | <TO_BE_FILLED> |
| CONFLICT-0075-004 | RFC-0075 header/§§4,8,10,13,18 vs docs/specifications/red-deep-technical-spec/RFC-0075-Ratification-Record.md | Candidate calls itself Candidate, parent RFC-0074 CRPDGSMP, 8-stage lifecycle, KnowledgeExchange, 5 profiles Minimal/Developer/Distributed/Enterprise/Federation; Record calls Ratified effective upon RFC-0074 ratification, parent title Cognitive Federation Governance and Trust Framework, 5-stage lifecycle Proposal→Negotiation→Activation→Amendment→Termination, KnowledgeExchangeObject, 3 profiles Minimal/Full/Governance, plus FederationID, Agreement Version Invariant, Trust state machine | Choose ONE canonical lifecycle + object model + profiles and record decision in ratification record. Recommendation (example): Adopt Record's 5-stage lifecycle (includes Amendment, critical for versioning) + KnowledgeExchangeObject as representation-agnostic (per Record's semantics-agnostic clarification) + 3 profiles Minimal/Full/Governance as normative, keep 5-profile table as informative mapping to Full. Require FederationID, Version, RootTrust as mandatory fields in FederationAgreement. Adopt Agreement Version Invariant: replay evaluates exchange against exact agreement version active at original time. | Record contains normative additions (identity, version evolution, trust lifecycle, invariant) that address gaps flagged in review [420]; 8-stage model includes Operation/Suspension which can be mapped to Activation/Amendment states | <TO_BE_FILLED> |

CONFLICT-0075-001 already resolved 2026-08-13: 4 body CADFP occurrences corrected to CFCKEP per review [420]; verbatim archive retains original.

## Gaps (per docs/traceability/rfc-0075/15-gaps.md)

| ID | Requirement | Description | Proposed resolution | Severity |
|----|-------------|-------------|---------------------|----------|
| GAP-0075-001 | 007,020,021,024,025 | No types, optionality, validation, canonical encoding or wire format | Define normative schemas (e.g., JSON Schema / CDDL) for FederationAgreement, FederationTrust, KnowledgeExchangeObject, FederationEvent, KnowledgeView — include optionality, validation rules, canonical encoding (RFC-8785 JSON or CBOR deterministic). Specify wire format mapping to RFC-0072 CRCP. | CRITICAL |
| GAP-0075-002 | 018,019 | Lifecycle has no transition guards, actors, authorization, persistence/failure/rollback semantics | Define state machine with guards: Proposal by Domain, Negotiation requires mutual capability, Verification requires TrustLevel≥Provisional, Activation requires signatures, Amendment produces new Version (immutable after activation per Record), Termination requires DisputeResolution or mutual consent. Specify persistence (event log) and rollback (Amendment, not mutation). | CRITICAL |
| GAP-0075-003 | 008,017,021,025,028 | IntegrityProof, trust/certificates, event protection have no crypto profile | Define cryptographic profile: IntegrityProof = detached signature (e.g., Ed25519) over canonical encoding of KnowledgeExchangeObject + AgreementRef + Provenance; CertificateChain = X.509 or DID; RevocationStatus via OCSP or event-log revocation; FederationEvent integrity-protected via same. Reference RFC-0022, RFC-0072. | CRITICAL |
| GAP-0075-004 | 002,004,016,023 | Deterministic inputs, external input capture, equivalence, replay boundary undefined | Define: deterministic inputs = canonical Agreement + Trust + KnowledgeObjects + CapabilityContext at event time; external input capture via FederationEvent Subject/Provenance extended chain; equivalence = observable state equality excluding Timestamp/Transport; replay boundary = from Proposal to Termination inclusive of all FederationEvents for that FederationID. | CRITICAL |
| GAP-0075-005..012 | see 15-gaps.md | HIGH/MEDIUM/LOW gaps (conflict taxonomy, trust lifecycle issuance/expiry, metrics, CLI mapping, KnowledgeView authz, governance-to-event ledger) | Address after critical gaps: define conflict taxonomy (capability, classification, sovereignty, version), ordering tie-breaker (lexicographic AgreementID + timestamp), policy-version semantics (bound to Agreement Version), failure semantics (record as FederationEvent Outcome=Failed). Trust lifecycle issuance/validation/expiry authority = FederationRootTrust, propagation via event log. | HIGH/MEDIUM/LOW |

## HASH-GAP-1 (runtime /hash)

- Location: runtime/crypto.reds L256 `print-line "** /hash support not yet implemented; algorithm TBD."`
- Blocked by incomplete spec + toolchain
- Proposed resolution (requires normative spec): choose algorithm (e.g., case-insensitive hash = FNV-1a or Murmur + case folding, or SHA-256 truncated) and define seed(s) per Red spec. Must be ratified in RC-200 or runtime spec.

## Suggested PR structure for RFC-0075 reconciliation

**Title:** `rfcs(RFC-0075): resolve lifecycle/profile/terminology/crypto conflicts (ratification patch)`

**Files:**

- `rfcs/RFC-0075-cfckep-federation-collaboration-knowledge-exchange.md` — update lifecycle to canonical 5-stage, terminology (ensure all CFCKEP), object name to KnowledgeExchangeObject or keep alias with deprecation note, profiles to chosen set (3 vs 5) with mapping table, add FederationID fields, Agreement Version Invariant, trust state machine.
- `docs/specifications/red-deep-technical-spec/RFC-0075-Ratification-Record.md` — update ratification decision, vote record, references, date, approvers.
- `docs/traceability/rfc-0075/16-conflicts.md` — mark resolved conflicts with resolution choice + approver + date.
- `docs/traceability/rfc-0075/15-gaps.md` — close GAP-001..004 with normative schema references + validation rules.
- `docs/traceability/rfc-0075/validation-result.json` — re-run `validate_rfc_0075_traceability.py` must PASS (0 conflicts, 0 critical gaps).

**Approval required:**

- Governance council / RFC editors / listed approvers per RC-000 §8 Repository Governance
- Must not modify RFC without ratification record

**Verification after merge:**

```bash
python3 tools/validate_rfc_0075_traceability.py -v
# expect: Requirements 31 Mapped >0, Critical Gaps 0, Conflicts 0, RESULT PASS
python3 tools/run-implementation-pipeline.py --dry-run | grep RFC0075
# if gaps closed, RFC0075-001 may still be TOOLCHAIN independent but now READY or BLOCKED only by dependency, ready to implement at enforced runtime boundaries
```

## Traceability after reconciliation

```
REQ-0075-001..031
 -> RFC-0075 candidate + ratification record (reconciled, 5-stage, KnowledgeExchangeObject, 3 profiles, FederationID, invariant, trust lifecycle, crypto profile)
 -> Task RFC0075-001 (no longer SPEC_CONFLICT, now INCOMPLETE_SPECIFICATION resolved -> READY if implementation_targets defined)
 -> Source: cognition/ federation module (to be implemented at enforced boundaries, capability-gated, provenanced, event-logged, replay-equivalent)
 -> Validation: python3 tools/validate_rfc_0075_traceability.py PASS
 -> Evidence: EVD-RFC0075-001 with deterministic execution + replay equivalence
```

## Notes

- Do NOT implement CFCKEP until traceability validator PASS (0 conflicts, 0 critical gaps) — per task acceptance criteria RFC0075-AC-1
- Keep implementation at enforced runtime boundaries (capability-gated, provenance chain, event log, determinism, sovereignty invariants)
- Preserve verbatim archive in knowledge-base/sources/ (uncorrected original) for provenance
