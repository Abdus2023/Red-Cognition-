# Project Invariants — Red/Cognition

**Document class:** Governance record (non-normative for RFC/specification content)
**Status:** Permanent top-level project invariants
**Established:** 2026-08-13
**Baseline audited:** `4b06081ae5b13eb692968a1467e7a46ce6fd1f7a`
**Source:** [Independent Repository Deep Analysis](audits/RED-COGNITION-DEEP-ANALYSIS-2026-08-13.md)

These invariants separate two facts that the repository had begun to conflate,
and define the two independent gates on project progression.

---

## Invariant 1 — Governance tests are not product validation

```
GOVERNANCE TESTS (390 PASS)   ≠   PRODUCT VALIDATION (0)
```

The 390 passing tests demonstrate that the **governance machinery** (the
fail-closed implementation execution controller and its hardening suite) works.

They demonstrate **nothing** about whether Red/Cognition itself works.

| Property | State |
|---|---:|
| Governance tests passing | 390 / 390 |
| Product requirements specified | 1,467 |
| Product code executed / tested / validated / evidenced | 0 |

**Rule:** a green governance test suite is never treated as a proxy for product
maturity. Product maturity is measured only by the epistemic ladder below.

## Invariant 2 — Epistemic states are never collapsed

```
specified(1467) > implemented(1) > executed(0) > tested(0)
> validated(0) > evidenced(0) > formally_verified(0)
```

The only meaningful project-level proof of progress is moving a **complete
vertical slice** through every state of this ladder — not accumulating
additional specified requirements, generated task stubs, or passing governance
tests.

## Invariant 3 — Two independent gates on progression

```
PROJECT PROGRESSION
        │
  ┌─────┴──────────┐
  │                │
GOVERNANCE GATE  EXECUTION GATE
  │                │
RFC authority    Rebol 2.7.8
reconciliation   (Gate A)
  │                │
  ▼                ▼
SPEC READY      TOOL READY
  │                │
  └─────┬──────────┘
        ▼
   RED-LEX-001
```

- **GOVERNANCE GATE** — the specification corpus must be internally
  authoritative (RFC identity, ratification counts, derived artifacts, and
  documentation all consistent). Gate owner: project governance.
- **EXECUTION GATE (Gate A)** — an executable Rebol 2.7.8 toolchain must be
  observed in the environment. Gate owner: external toolchain provisioner.

The two gates are **independent and never conflated**. Passing one does not
open the other.

## Invariant 4 — Authority before derivatives

```
FROZEN ARCHITECTURE (preserve)
        ↓
INDEPENDENT AUDIT
        ↓
CORRECTION / REGENERATION   ← authority is fixed first
        ↓
RE-AUDIT
        ↓
GATE A + VERTICAL SLICE
```

Derived artifacts (indexes, reports, dashboards, traceability) are regenerated
**only after** the authoritative corpus is corrected. Regenerating against a
drifting authority would produce:

```
correct source → stale generated artifact → incorrect analysis → incorrect task
```

## Invariant 5 — Historical evidence is preserved

The frozen architecture baseline is never rewritten to make a later audit
disappear. The freeze and the independent audit are different facts and remain
separately traceable.

---

## Vertical-slice strategy (endorsed)

The first evidenced pass is worth more than hundreds of additional generated
task stubs:

```
TYPE SYSTEM → SCHEDULER → CVM → CISA INTERPRETER
   → ONE END-TO-END EXECUTION → OBSERVED RESULT → EVIDENCE → PASS
```

## Related

- [Independent Repository Deep Analysis](audits/RED-COGNITION-DEEP-ANALYSIS-2026-08-13.md)
- [Repository Integrity Reconciliation](audits/REPOSITORY-INTEGRITY-RECONCILIATION-2026-08-13.md)
- [Ratification Registry](governance/ratification-registry.md)
- [Gate A protocol](implementation/gate-a-protocol.md)
