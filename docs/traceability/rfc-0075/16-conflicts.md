# Conflicts and inconsistencies

| ID | Authorities | Conflict / impact |
|---|---|---|
| CONFLICT-0075-001 | RFC-0075 title/§§1–14 vs §§15–19 | Later sections call the protocol **CADFP**, the RFC-0054 acronym. Security, observability, CLI, profiles and relationship claims are ambiguously scoped. |
| CONFLICT-0075-002 | RFC-0075 §17–18 vs RFC-0054 title/scope | `cog agent register/discover` and “local registration and discovery” profiles appear to be CADFP discovery content, not defined CFCKEP federation exchange behavior. |
| CONFLICT-0075-003 | RFC-0075 §2/§§6,11,12 vs §§4,7,14 | Determinism/replay are mandatory but canonical types/serialization/input capture are absent; this is an internal specification incompleteness that prevents demonstrating the claim. |

No resolution is invented. CONFLICT-001 is the highest-priority terminology correction identified in target provenance comments.
| CONFLICT-0075-004 | `rfcs/RFC-0075...` header/§§4,8,10,13,18 vs `docs/specifications/red-deep-technical-spec/RFC-0075-Ratification-Record.md` | The target calls itself Candidate, names parent RFC-0074 CRPDGSMP, shows an 8-stage lifecycle, `KnowledgeExchange`, and five profiles. The record calls it Ratified only effective upon RFC-0074 ratification, changes RFC-0074’s title, gives a different 5-stage lifecycle including Amendment, calls the contract `KnowledgeExchangeObject`, adds agreement identity/trust lifecycle/version invariant, and defines three profiles. Under the supplied hierarchy the Candidate RFC outranks a ratification record; no resolution is implied. |
