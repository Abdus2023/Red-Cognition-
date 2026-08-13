# RFC-0001 — Text Interfaces and Agent Runtimes

**RFC:** RFC-0001
**Title:** Text Interfaces and Agent Runtimes — CLI, Interactive Prompt, REPL Lifecycle, and the Agent Evolution Spectrum
**Stable ID(s):** `TEXT-INT-001`
**Origin:** MSG-01 (First user message — CLI architecture, REPL lifecycle, agent evolution) — stateless CLI `User→Shell→Spawn→Process→Exit` vs stateful REPL `READ→EVAL→PRINT→LOOP`; proposed as baseline before generalising to agent runtimes.
**Evolution:** Contrasted in MSG-02 with event-driven ARS (`polling→event queue`); refined in MSG-03 as Goal Scheduler replacing Time-Sharing scheduler; analysis `AGENT-ANALYSIS-001` notes homoiconicity widens the gap — REPL persistence is prerequisite, not sufficient, for cognitive runtime.
**Final Representation:** This RFC + Text Interface Layer (CLI / Prompt / REPL) as defined in `docs/TRACEABILITY-ARCHIVE.md` §Phase 0 Step 1 and RFC Origin Map R1–R2.
**Status:** `Draft` (`Implemented` for underlying Red REPL; `Proposed` for agent-runtime generalisation)
**Authors:** Conversation (MSG-01) + Auditor reconstruction
**Verification:** Red REPL golden-file: `red.r` → `READ→EVAL→PRINT→LOOP` preserves `word!` bindings across turns per `RED-SPEC-015`; CLI lifecycle preserves exit-code contract (`red.r` flags `-c/-r/-t`).

---

## 1. Abstract

Specifies the three primary text-interface layers and the state spectrum from one-shot automation to continuous evaluation environments, establishing why neither CLI nor REPL alone suffices for autonomous agents and how the lineage `Batch→Shell→CLI→REPL→Notebook→LLM Chat→Agent Runtime→Autonomous OS` structures the evolution toward cognition.

## 2. Motivation

- Classical automation is caught between **efficiency** (one-shot scriptable commands) and **flexibility** (stateful live environments). Without naming this trade-off, every agent runtime reinvents REPL persistence poorly.
- The conversation introduced Docker's command anatomy (`binary/subcommand/flag/argument`) to show CLI's request-response statelessness, then the REPL's 4-step loop to show statefulness, to argue that agents require a third point: event-driven persistence.

## 3. Specification

### 3.1 CLI Lifecycle (Stateless Request-Response)

`[User Input] ➔ [Shell Parses Flags/Args] ➔ [OS Spawns Process] ➔ [Process Executes & Out] ➔ [Process Dies/Exit Code]`

Example anatomy (normative):

```
docker container run -d --name web_server -p 80:80 nginx:latest
#   └───┬──┘ └───┬───┘ └─┬┘ └────────┬─────┘ └───┬───┘ └───┬────┘
#     Binary  Subcommand Flag     Arguments     Option   Argument
```

Properties: bridges user / OS shell / filesystem; terminates per invocation; exit code is sole feedback channel.

### 3.2 Interactive Prompt (normative)

A temporary pause within a CLI workflow to gather input, converting a static script into active dialogue. Distinguished from REPL: prompt is **within** a command, REPL is a **continuous engine**.

### 3.3 REPL Lifecycle (Stateful Persistent Environment)

```
┌────────────────────────────────────────────────────────┐
│ [READ] ──► Reads code input string into memory buffers. │
│ [EVAL] ──► Compiles/Interprets code via the engine.    │
│ [PRINT] ─► Formats and dumps evaluation result.         │
│ └─────────────────────────────────────────────────────┘
│ Loop: holds variables/functions/imports in RAM until exit
```

Detailed steps (normative):

1. **Read:** lexical analysis → AST/token set.
2. **Eval:** evaluate within persistent context (bindings survive).
3. **Print:** auto-output even without `print()` / `console.log()`.
4. **Loop:** await next input vector with state intact.

### 3.4 Evolution Spectrum (informative, normative for roadmap)

```
Batch → Shell → CLI → REPL → Notebook → LLM Chat → Agent Runtime → Autonomous OS
```

Refined in `AGENT-ENV-ANALYSIS-001` §VI with discrete phase changes (normative for traceability):

| Transition | Phase Change |
|---|---|
| CLI → REPL | **Statefulness** added |
| REPL → Notebook | **Narrative context** added |
| Notebook → LLM Chat | **Natural language** replaces syntax |
| LLM Chat → Agent Runtime | **Initiative** moves human→system |
| Agent Runtime → Autonomous OS | **Identity & persistence** become OS primitives |

## 4. Consequences

- **Preserved:** Red REPL (`red.r`, `compiler.r`, `runtime/`) remains reference implementation; agent runtimes must not regress to statelessness.
- **Rejected alternative:** “CLI is sufficient for agents” — rejected; agents require cross-session `remember!` and wake-on-event, which CLI cannot provide (see RFC-0003 ARS triad).
- **Trade-off:** REPL statefulness is powerful but unbounded without memory hierarchy (see RFC-0003 correction to CoALA 4-store).

## 5. Traceability

| Mapping | Value |
|---------|-------|
| **RFC Origin Map rows** | R1–R2 (MSG-01 → RFC-001 → Text Interface Layer → preserve REPL statefulness) |
| **REQ IDs** | None directly (prerequisite for REQ-003 event-driven runtime) |
| **ADR** | ADR-001 (Red as substrate) — REPL persistence is necessary but not sufficient |
| **Formal models** | CLI/REPL lifecycle as historical precedent for ARS event loop |
| **Open problems** | None at this layer; OP-01 (ecosystem) is downstream |

## 6. Dependencies

- **Upstream:** RFC-0002 (Red Core implements REPL), RFC-0009 (lexer/evaluator spec).
- **Downstream:** RFC-0003 (ARS triad generalises REPL persistence into agent cognition).

## 7. Appendix — Wiki Source Mapping

- `docs/wiki/Text-Interfaces-and-Agent-Runtimes.md` (`TEXT-INT-001`, 284 lines) — CLI/REPL/evolution sections verbatim.
- `docs/TRACEABILITY-ARCHIVE.md` §Phase 0 Steps 1–2, §0.2 `ARS` row.
