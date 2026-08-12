# Source authority and inspection record

Authority was applied as: ratified normative RFC; candidate RFC; ratification/decision record; draft RFC; formal model; schema; implementation; tests; explanatory docs; inference. RFC-0075 is a candidate and its parent RFC-0074 is Draft, so neither outranks ratified prerequisites. A repository ratification record exists at `docs/specifications/red-deep-technical-spec/RFC-0075-Ratification-Record.md`. It declares “Ratified” effective upon RFC-0074 ratification, while RFC-0074 is described there as Candidate and the target remains Candidate. It also introduces materially divergent normative additions. This is recorded as CONFLICT-0075-004, not silently accepted as a superseding text.

| Source | Version/status observed | Role |
|---|---|---|
| RFC-0075 | 1.1, Candidate | Primary claim source |
| RFC-0075 ratification record | says Ratified conditional on RFC-0074; conflicting | Secondary authority with divergent normative additions; see CONFLICT-004 |
| RFC-0050 | 1.2, candidate text; repository provenance says ratified | Architecture/conformance reference |
| RFC-0053 / RFC-0057 | candidate text; provenance reports ratified decisions | Related prerequisite only where semantics apply |
| RFC-0006 | 1.2 Candidate | Capability prerequisite inferred from capability gating |
| RFC-0018, 0020–25, 0040–41, 0055–56, 0069, 0073–74 | Draft unless noted | Dependencies or semantic context |

All status observations are repository text, not an independent ratification registry. Inferences are labelled in dependency and architecture documents.
