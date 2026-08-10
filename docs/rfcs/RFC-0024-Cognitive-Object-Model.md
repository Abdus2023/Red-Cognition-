# RFC-0024 — Cognitive Object Model (agent!) & Message Passing

**RFC:** RFC-0024
**Title:** Cognitive Object Model (agent!) & Message Passing — `agent!` Formal Spec
**Stable ID(s):** `RED-AGENT-OBJECT-001`
**Origin:** MSG-07 § Cognitive Object Model — `agent! [beliefs goals memories skills policies capabilities reflection]` — objects modelling reasoning entities, not things; plus MSG-06 `agent planner [...]` as independent agents with `Proposal→Reviewer→Executor→Receipt`.
**Evolution:** RFC-0007 §3.6 introduced `agent!` + toolchain but left `agent!` facets implicit; RFC-0015/0016 added scheduling/coherence that `agent!` must carry. This RFC formalises the object.
**Final Representation:** This RFC + `agent!` spec + message types.
**Status:** `Draft` — P2 (formalisation, Phase 8 roadmap)
**Verification:** `agent!` golden file decomposes into facets with typed slots; message `Proposal` → `Approved` round-trips via `MESSAGE`.

---

## 1. Specification

### 1.1 `agent!` Facets (normative)

```
agent! [
    beliefs: block! [belief!]      ; epistemic (RFC-0005)
    goals: block! [goal!]          ; intentional
    memories: block! [memory!]     ; temporal
    skills: block! [skill!]        ; procedural
    policies: block! [policy!]     ; normative
    capabilities: block! [capability!]
    reflection: block! []          ; lessons + provenance log
]
```

Each facet is the typed block that RFC-0005 introduced — `agent!` is the housing.

### 1.2 Messages (normative)

```
Proposal  → Review  → Approved/Rejected → Receipt(kind: execution, audit: HMAC)
```

Typed payloads per CISA `MESSAGE agent! payload` (RFC-0007 §3.1 agentinstructions).

## 2. Traceability

- **REQs:** REQ-010/021 (skill/message).
- **Dependencies:** RFC-0007 + RFC-0015/0016.

