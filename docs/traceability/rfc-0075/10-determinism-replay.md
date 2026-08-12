# Determinism and replay

| Claim | Deterministic input/state defined? | Replay boundary / identical observable state | Finding |
|---|---|---|---|
| REQ-002 (§2) | No | No | GAP-004 |
| REQ-004 (§2) | No | “equivalent observable states” undefined | GAP-004 |
| REQ-016 (§6) | No | decision recording/provenance required, equivalence undefined | GAP-004 |
| REQ-022 (§11) | Workflow labels only; ordering, tie-breakers and policy versions absent | No | GAP-005 |
| REQ-023 (§12) | Replay invariant only named | No | GAP-004 |
| REQ-008/017/025 | agreement version, timestamps/epochs, event fields participate | canonical serialization, clock semantics, external input capture absent | GAP-003/004 |

External nondeterminism (time, network ordering, policy lookup, negotiation choices, trust/revocation state) is neither prohibited nor captured. No result may be called replay-verified.
