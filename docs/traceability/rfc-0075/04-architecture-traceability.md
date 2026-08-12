# Architecture traceability

The machine inventory (`traceability.json.architectural_concepts`) assigns stable `ARCH-0075-*` identifiers. All statuses reflect this checkout, not a claim about external products.

| ID / component | Responsibility / boundary | Inputs → outputs | Specification source / dependencies | Persistence, replay, implementation |
|---|---|---|---|---|
| ARCH-001 Agreement | versioned collaboration contract; federation/trust boundary | terms, domains → agreement reference | §4; RFC-0074 | event-log recording required; replay version semantics undefined; NOT_FOUND |
| ARCH-002 Exchange layer | governed cross-domain transfer; sovereignty boundary | capability, knowledge → KnowledgeExchange/event | §§5,10; RFC-0006/0056/0074 | persistence undefined; NOT_FOUND |
| ARCH-003 Decision layer | cross-domain governance | policy, participants → recorded decision | §6; RFC-0040 | provenance required; deterministic inputs absent; NOT_FOUND |
| ARCH-004 Provenance | transfer lineage | origin/transforms → provenance chain | §7; RFC-0074 | immutable claim, storage/hash model absent; NOT_FOUND |
| ARCH-005 Lifecycle manager | state transitions | lifecycle state → FederationEvent | §8 | event required; state/persistence/rollback absent; NOT_FOUND |
| ARCH-006 Trust layer | assertion and validity | identity/certificates → trust decision | §§9,15; RFC-0022 | revocation listed only; NOT_FOUND |
| ARCH-007 Conflict layer | deterministic resolution | conflict/policy → decision | §11; RFC-0040 | workflow only; no tie-breaker/version capture; NOT_FOUND |
| ARCH-008 Knowledge views | optional governed disclosure | filters/capability → visible objects | §13; RFC-0074 | persistence/replay unspecified; NOT_FOUND |
| ARCH-009 Event/observability | record and expose events | federation action → FederationEvent/interface | §§8,14,16; RFC-0018/0046 | event participation required; endpoint/schema absent; NOT_FOUND |
| ARCH-010 CLI/conformance | operator commands/profiles | commands → operations | §§17–18 | CADFP conflict; implementation absent; UNVERIFIED |

CogOS/runtime, registry, identity, capability, governance, memory, transport, storage, security and verification layers are architectural roles derived from these components and named dependency RFCs; RFC-0075 does not allocate interfaces to them. Such allocation would be inference, not a mapping.
