# Lifecycle traceability

§8 supplies only ordered labels and requires a FederationEvent for each transition. It does **not** define actors, authorization, state objects, preconditions, failure/rollback, persistence transaction, or replay semantics. Those omissions are GAP-002/004.

| Transition | Required event | Defined preconditions/actor/auth/failure/replay | Evidence |
|---|---|---|---|
| Proposal → Negotiation | FederationEvent | Unspecified | E1 §8 |
| Negotiation → Verification | FederationEvent | Unspecified | E1 §8 |
| Verification → Agreement | FederationEvent | Unspecified | E1 §8 |
| Agreement → Activation | FederationEvent | Unspecified | E1 §8 |
| Activation → Operation | FederationEvent | Unspecified | E1 §8 |
| Operation → Suspension | FederationEvent | Unspecified | E1 §8 |
| Suspension → Termination | FederationEvent | Unspecified | E1 §8 |
