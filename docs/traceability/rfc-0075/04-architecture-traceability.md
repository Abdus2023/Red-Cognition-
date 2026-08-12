# Architecture traceability

| Component | Responsibility / boundary | Inputs → outputs | Source | Implementation status |
|---|---|---|---|---|
| Actors/domains/CogOS | independent participants; sovereignty boundary | agreement, identity → governed action | RFC-0075 §§1–4 | NOT_FOUND |
| Runtime / transport / storage | execute, exchange, persist | contracts/events → state/event log | §§5,8,14; RFC-0018/0021 | NOT_FOUND |
| Registry / identity / trust | discovery, authentication, assertions/revocation | identity/certificates → trust decision | §§9,15; RFC-0022 | NOT_FOUND |
| Capability / governance | authorize and decide | capability/policy → decision | §§5–6; RFC-0006/0040 | NOT_FOUND |
| Memory / knowledge layer | synchronize classified knowledge | KnowledgeExchange → KnowledgeView | §§5,10,13; RFC-0056/0074 | NOT_FOUND |
| Event log / observability | persistent, replayable observation | FederationEvent → interface/metrics | §§2,4,8,14,16; RFC-0018/0046 | NOT_FOUND |
| Security / verification | integrity, policy and conformance | proofs/assertions → acceptance evidence | §15; RFC-0025/0050 | NOT_FOUND |

Persistence is mandated only generally (agreements/event participation); retention, transactionality, and storage authority are unspecified. Replay boundary and security boundary algorithms are gaps, not architecture facts.
