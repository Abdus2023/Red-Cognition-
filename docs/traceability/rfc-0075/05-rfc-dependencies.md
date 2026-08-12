# RFC dependency traceability

“Direct” means named by RFC-0075; “semantic” means needed to give a target requirement meaning. No dependency is treated as ratified merely because it is named.

| RFC | Exists/title | Relationship | Why / discrepancy |
|---|---|---|---|
| 0006 | Yes, Capability Model | Semantic prerequisite | capability gates (§2/5); not explicitly cited |
| 0018 | Yes, Event Log and Deterministic Replay | Semantic prerequisite | event/replay claims; not explicitly cited |
| 0020 | Yes, Distributed Cognitive Execution | Direct (§19) | no particular interface stated |
| 0021 | Yes, Cognitive Network Protocol | Direct (§19) | transport is unnamed |
| 0022 | Yes, Identity and Trust | Direct (§15,19) | supports assertions/authentication |
| 0023 | Yes, Distributed Consensus and Causal Agreement | Indirect | potentially relevant to agreement, not cited |
| 0025 | Yes, Security Policy Language | Direct (§15) | policy enforcement unspecified |
| 0040 | Yes, Governance and Collective Decision | Direct (§6) | required decision model |
| 0041 | Yes, Interoperability and Federation | Direct (§1,19) | federation context |
| 0050 | Yes, Architecture/Conformance | Direct (§19) | conformance relation unstated |
| 0053 | Yes, Remote Agent Invocation | Direct (§19) | invocation relation unstated |
| 0055 | Yes, Multi-Agent Coordination | Direct (§1) | coordination context |
| 0056 | Yes, Shared Memory/Knowledge Sync | Direct (§1,5) | update rules required |
| 0057 | Yes, Distributed Transaction | Indirect | plausible atomic exchange prerequisite, not cited |
| 0069 | Yes, Decision Ledger/Memory | Indirect | plausible decision recording, not cited |
| 0073 | Yes, Security Monitoring/Defense | Indirect/parent-chain | security context, not cited |
| 0074 | Yes, Privacy/Data Governance/Sovereign Memory | Parent/direct (§1) | sovereignty/provenance foundation |

Dependency graph: RFC-0075 → {0041,0055,0056,0074,0040,0022,0025,0046,0020,0021,0050,0053}; semantic additions → {0006,0018}; potential only → {0023,0057,0069,0073}. RFC-0046 is named but was outside the requested list and exists as observability RFC.
