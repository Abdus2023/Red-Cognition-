# Conflicts and inconsistencies

| ID | Authorities | Conflict / impact |
|---|---|---|
| CONFLICT-0075-001 | RFC-0075 title/§§1–14 vs §§15–19 | Later sections call the protocol **CADFP**, the RFC-0054 acronym. Security, observability, CLI, profiles and relationship claims are ambiguously scoped. |
| CONFLICT-0075-002 | RFC-0075 §17–18 vs RFC-0054 title/scope | `cog agent register/discover` and “local registration and discovery” profiles appear to be CADFP discovery content, not defined CFCKEP federation exchange behavior. |
| CONFLICT-0075-003 | RFC-0075 §2/§§6,11,12 vs §§4,7,14 | Determinism/replay are mandatory but canonical types/serialization/input capture are absent; this is an internal specification incompleteness that prevents demonstrating the claim. |

No resolution is invented. CONFLICT-001 is the highest-priority terminology correction identified in target provenance comments.
