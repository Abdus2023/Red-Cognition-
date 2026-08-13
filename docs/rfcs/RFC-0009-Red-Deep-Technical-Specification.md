# RFC-0009 — Red Deep Technical Specification (Parts I–IV)

**RFC:** RFC-0009
**Title:** Red Deep Technical Specification — Canonical Ground Truth (Parts I–IV, New Lexer, Interpreter Internals)
**Stable ID(s):** `RED-SPEC-001`, `RED-SPEC-015`, `RED-SPEC-PART-III-001`
**Origin:** MSG-09 (Ninth/final user message — Comprehensive Red architecture reference) — the 3313-line encyclopedic reference that phrases spec language.
**Evolution:** No divergent evolution in conversation; serves as the `Implemented` ground truth that corrects earlier informal summaries (MSG-01 Red features) and anchors RFC-0002's invariants with full detail (lexer FSM, compiler stages, Red/System overview, format encoders, evaluator dispatch).
**Final Representation:** This RFC + canonical toolchain spec + lexer v2 instrumentation API + evaluator dispatch table + 40+ datatype taxonomy, as implemented at `9b5b15a` (with JIT and lexer rewrite as noted open items).
**Status:** `Implemented` (lexer rewrite in Red/System `Partially Implemented`, JIT `Open Question`; all else verified)
**Authors:** Red core team / Official Red language specification + Conversation MSG-09 + Auditor
**Verification:** `compiler.r` 125703 / `lexer.r` 26389 / `red.r` 25562 size invariants + `tests/source/units/*-test.red` + `red-system-quick-test.txt` + `transcode` instrumentation API.

---

## 1. Abstract

The 3313-line canonical reference (1317 + 1996 + 67) that records Red as it is: full-stack diagram, toolchain (encapper/compiler/interpreter/linker, Rebol2 bootstrap, cross-targets), Red/System low-level dialect, lexer architecture, interpreter dispatch, and datatype/object/parse system.

## 2. Motivation

Without a verbatim ground truth, cognitive extensions would silently redefine core semantics (e.g., treating `block!` as executed). This RFC freezes the spec that every `Proposed` RFC extends without breaking.

## 3. Specification

### 3.1 Red System and the Full-Stack Diagram (normative)

See `Red-Deep-Technical-Specification.md` §§ I–III for the full 5-layer diagram (`Human/Application → Red High Level (40+ datatypes, objects, functions, dialects, reactive GUI) → Red/System (C-level, pointers, ARM/IA-32) → Machine Code (PE/ELF/Mach-O) → Hardware`) and the “One Language from Hardware to Human” narrative. Normative behavior: Red/System is the low-level DSL; Red compiles to it; direct machine code generation (no IR currently) via `system/emitter.r`; linker via `system/formats/{PE,ELF,Mach-O}.r`.

### 3.2 Toolchain Detail (normative)

`red.r` flags verified: `-c/--compile`, `-r/--release`, `-dlib/--dynamic-lib`, `-e/--encap`, `-d/--debug`, `-t/--target` (ID table `MSDOS/Windows/Linux/…/Android-x86`), `-o`, `-v`, `--cli/--no-view/--red-only` etc. (see `README.md` + `usage.txt` + `system/config.r`). Build via `build/build.r` + `build/precap.r`.

### 3.3 Lexer v2 — Architecture and Instrumentation API (normative, partially implemented)

`transcode` converts UTF-8 string/binary → structured Red values. Until this spec, lexer was Parse dialect (maintainable, not performant). Spec mandates **Red/System rewrite** for near-instant loading of huge Red values / scanning without loading, with phases:

```
Phase 1 — CHARACTER CLASSIFICATION (byte → class: DIGIT ALPHA SPECIAL SPACE NEWLINE STRING-START BINARY-START BLOCK-START …)
```

Instrumentation: event-oriented API allowing customisation of lexer's behaviour at will (see `docs/old/*`, `utils/generate-lexer-table.red`).

Status split (normative): Parse-dialect lexer `Implemented` at 26389 B; Red/System lexer `Partially Implemented` (spec defines performance goal, not yet the sole path).

### 3.4 Interpreter Internals — Evaluator Dispatch (normative)

From `Red-Interpreter-Internals.md` §XV (verbatim table, binding contract):

| Value Type | Evaluation Rule |
|---|---|
| `integer!`/`float!`/`string!`/`logic!`/`none!`/`char!`/`binary!` | Self-evaluating |
| `block!` | Self-evaluating — NOT executed (use `DO`) |
| `paren!` | IMMEDIATELY evaluated |
| `word!` | Context lookup → evaluate |
| `set-word!` | Evaluate RHS → bind |
| `get-word!` | Fetch without evaluating |
| `lit-word!` | Return `word!` itself |
| `path!` | Navigate series/object |

Implemented in `runtime/` (hybrid static+interpreter; JIT for “cases in between” not yet implemented — `Open Question`).

### 3.5 Datatype and System Spec (normative, summary)

40+ datatypes, objects, reactivity (`VID`/`View`), `system/compiler.r` stages, `system/targets/{ARM,IA-32}.r`, `environment/*.red`, `quick-test/`. For full matrix, see `Red-Technical-Specification-Part-III.md` (1996 lines, §§XXVII–XXXIX + Summary) — verbatim therein, not re-copied here to avoid drift; this RFC normatively references that file for lexical states, evaluator phases, and Red/System specs.

## 4. Consequences

- **Freezes invariants** that RFC-0005→0007 extend: `block!` non-evaluation, word binding, `transcode` contract, format encoders.
- **Open items:** JIT and lexer rewrite completion are explicitly `Open Question` / `Partially Implemented` — cognitive layers may not assume they are available.

## 5. Traceability

- **RFC Origin Map rows:** R40 (MSG-09 ground truth).
- **REQ IDs:** REQ-022 (`Implemented`); underpins REQ-001 (homoiconicity) and RFC-0002 evaluator invariants.
- **ADRs:** None new; supports ADR-001 substrate decision.
- **Formal models:** Red/System compiler overview, official language specification (MSG-09 sources).
- **Open problems:** OP-10 (JIT) directly; lexer instrumentation finalisation deferred to RFC-023 in future roadmap.

## 6. Dependencies

- **Upstream:** `red/red` `9b5b15a` + official Red/System specs.
- **Downstream:** RFC-0002 (normatively references this RFC for detail); all cognitive RFCs depend transitively.

## 7. Appendix — Wiki Source Mapping

- `Red-Deep-Technical-Specification.md` (`RED-SPEC-001`, 1318 lines) — §§ I–III full-stack + toolchain overview.
- `Red-Technical-Specification-Part-III.md` (`RED-SPEC-PART-III-001`, 1996 lines) — §§XXVII–XXXIX lexer v2 phases, scanning, instrumentation, Summary.
- `Red-Interpreter-Internals.md` (`RED-SPEC-015`, 67 lines) — §XV dispatch table verbatim.

