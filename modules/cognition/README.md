# Red/Cognition — Module Scaffold (Phase 1→2 Implementation Start)

This directory bootstraps **RFC-0005** (16 cognitive types) + **RFC-0012** (ergonomic proof) + **RFC-0024** (agent! object model) as real Red modules, derived from `prototypes/red-cognition-types.red` and the traceability archive's **07-Implementation-Roadmap.md**.

**Phase mapping:**

| File | RFC | REQ | Status |
|------|-----|-----|--------|
| `types.red` | RFC-0005 §3.2 + RFC-0020 (UQ slots) | REQ-011 | Scaffold (`Draft` — objects mocking `!` types) |
| `dialects.red` | RFC-0005 §3.4–3.8 + RFC-0012 (with-authorisation) | REQ-002/015 | Scaffold (dialect stubs) |
| `contracts.red` | RFC-0005 §3.10 (Cognitive Pipe + Capability Binding) | REQ-012 | Scaffold |
| `agent.red` | RFC-0024 (agent! facets) + RFC-0005 §3.9 golden-file | REQ-010/021 | Scaffold |

**How to run the scaffold (no compiler patch required yet — prototypes level):**

```bash
red prototypes/red-cognition-types.red        # original 121-line prototype
red modules/cognition/tests/run.red           # scaffold test (mock verification)
```

**Next steps per `docs/rfcs/RFC-0011`→`0014` (OP-01→04 closed):**
- Replace object-mock types with real datatype registrations in `runtime/` (requires `lexer.r` + `system/compiler.r` patch — see RFC-0009).
- Implement `with-authorisation` elaboration as a `Parse` dialect tactic (RFC-0012) rather than `do body` mock.
- Add `cognitive.lock` generation to `build/build.r` (RFC-0014).

**Traceability:** Every symbol carries an RFC anchor comment (`; RFC-0005 §…`).

*Branch `arena/019fec34-red-cognition`, scaffold commit — Gate A not yet passing (mock HMAC only).*
