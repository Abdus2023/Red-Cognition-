# RFC-0002 — Red Programming Language Core

**RFC:** RFC-0002
**Title:** Red Programming Language Core — Full-Stack Language, Toolchain, and Runtime Invariants
**Stable ID(s):** `RED-LANG-001`, `RED-SPEC-001`, `RED-SPEC-015`, `RED-SPEC-PART-III-001`
**Origin:** MSG-01 (Red introduction/features: homoiconic, 1 MB toolchain, Red/System) + MSG-09 (Comprehensive Red architecture reference, Parts I–IV + new lexer + interpreter internals) — baseline at `9b5b15a` (Red 0.6.4, 2021-09-17).
**Evolution:** MSG-01 mapped features to agent primitives (homoiconicity→`plan!`, dialects→tools); MSG-09 expanded into 3313-line canonical spec (full-stack diagram, toolchain with encapper/compiler/linker, Red/System overview, datatype taxonomy, lexer v2, evaluator dispatch); analysis `RED-2.0-ANALYSIS` situates core as `Implemented` substrate for cognitive layers.
**Final Representation:** This RFC + Red Core (`compiler.r` 125703 B, `lexer.r` 26389 B, `red.r` 25562 B, `runtime/`, `system/`, `bridges/`, `environment/`, `modules/`) as verified at `9b5b15a`.
**Status:** `Implemented` (JIT planned → `Open Question`, lexer v2 Red/System rewrite → `Partially Implemented`)
**Authors:** Red community (Nenad Rakočević et al.) + Conversation MSG-01/09 + Auditor
**Verification:** Binary size (`1 MB`), cross-target matrix (`-t MSDOS`..`Android-x86`), `tests/source/units/*-test.red` suite, `red-system-quick-test.txt`, `compiler.r` size assertions in audit.

---

## 1. Abstract

Codifies the Red language and toolchain that the entire Red/Cognition lineage builds upon: a Rebol-inspired homoiconic full-stack language with a self-contained native-code toolchain, 40+ datatypes, parse dialect, reactive GUI, and hybrid static+interpreter runtime written in Red/System.

## 2. Motivation

Without a frozen `Implemented` baseline, every cognitive RFC would be speculative. This RFC freezes the 2021-09-17 baseline (verified artifacts) and the evaluator/lexer invariants that cognitive types (RFC-0005) and the CIR (RFC-0006) extend.

## 3. Specification

### 3.1 Full-Stack Philosophy (normative)

```
Human / Application Layer (Scripts · GUI Apps · Data Processing · Domain Tools)
          │
          ▼
Red Language (High Level) — Interpreter+Compiler · Dialects · 40+ types · Objects · Parse
          │
          ▼
Red/System (Low Level DSL) — C-level · Pointers · Structs · Native Code · OS Calls · ARM/IA-32
          │
          ▼
Machine Code — PE/COFF (Windows) · ELF (Linux) · Mach-O (macOS)
          │
          ▼
Hardware — IA-32 · ARM · x86-64 (via 32-bit)
```

Slogan extension (informative, from Red-2.0): “One language from system programming to scripting” → “One language from hardware to intelligence” (see RFC-0008).

### 3.2 Toolchain (normative, verified)

```
Source (.red/.reds) → Preprocessor (Loader: #include/#if/#define) → Lexer/Scanner (transcode) → Parser/Loader (block tree; blocks ARE the parse tree)
        ├→ Interpret (Dynamic, embedded interpreter)
        └→ Compile → Red/System Compiler (comp-dialect) → Emitter (direct machine code, no IR currently) → Linker (PE.r/ELF.r/Mach-O) → Executable
```

- Single 1 MB executable (compiler+linker+interpreter+runtime); zero install.
- Self-hosted bootstrap currently requires Rebol2 interpreter (alpha).
- Flags: `-c` compile (dev, libRedRT), `-r` release, `-dlib` shared lib, `-e` encap, `-d` STABS, `-t ID` cross-compile; see `README.md` table (MSDOS..Android-x86).
- Runtime library written in Red/System, hybrid; JIT for the middle zone planned, not yet implemented (`Open Question`).

### 3.3 Language Invariants (normative)

- **Evaluated dispatch** (`RED-SPEC-015`, fixed table):

| Value Type | Evaluation Rule |
|---|---|
| `integer!`/`float!`/`string!`/`logic!`/`none!`/`char!`/`binary!` | Self-evaluating |
| `block!` | Self-evaluating — NOT executed (use `DO`) |
| `paren!` | Immediately evaluated |
| `word!` | Context lookup → evaluate |
| `set-word!` | Evaluate RHS → bind |
| `get-word!` | Fetch without evaluating |
| `lit-word!` | Return `word!` quoted |
| `path!` | Navigate series/object |

Violations of this table are toolchain regressions.

- **Datatypes:** 40+ (`integer!`..`vector!`, `object!`, `function!`, date/time, pair, tuple, binary, string, block/paren, map, bitset, etc. — see `conversion-matrix.xlsx`, `math-ops-matrix.xlsx`, docs/wiki/Red-Deep…).
- **Dialects/Parse:** `Parse` is the metaprogramming core (`docs/wiki/Red-Deep…`); dialects are DSLs with custom semantics sharing the block substrate.

### 3.4 Build & Test (normative)

- `build/build.r`, `build/precap.r`, `build/includes.r` — encapper paths.
- `quick-test/quick-test.r` + `tests/source/units/*-test.red` (~50 suites) + `tests/libRed/` as regression gate.

## 4. Consequences

- **Implemented:** All cognitive RFCs may assume evaluator/dialect invariants without re-proving them.
- **Reserved:** `goal!`/`plan!`/… are *not* core datatypes — they are Red/Cognition extension (RFC-0005) and must not collide with core parse keywords (reserved via `RED-SPEC-PART-III` word-type taxonomy).
- **Open:** JIT (`RHTT`-level effects) and lexer v2 instrumentation API finalisation (see RFC-0009 / `lexer.r` 26389 vs Parse-dialect performance gap) remain `Open Question`.

## 5. Traceability

- **RFC Origin Map rows:** R1–R2 + R40 (MSG-09 ground truth) → RFC-001+RFC-002.
- **REQ IDs:** REQ-022 (1 MB, cross-compile, hybrid, lexer v2) — **Implemented**; REQ-001 homoiconicity prerequisite — **Implemented** at core, `Proposed` for `plan!` typing (RFC-0005).
- **ADRs:** ADR-001 (Red as substrate) depends on this RFC being `Implemented`.
- **Formal models:** Rebol lineage; Red/System spec as language-level IR.
- **Open problems:** OP-10 (JIT), partially OP-01 (ecosystem FFI depends on `bridges/`).

## 6. Dependencies

- **Upstream:** `red/red` `9b5b15a`; `docs/wiki/Red-Deep…` + `Red-Technical-Specification-Part-III` as spec sources.
- **Downstream:** All RFCs 0001, 0003→0008 depend on this RFC; RFC-0009 is this RFC's detailed specification companion.

## 7. Appendix — Wiki Source Mapping

- `Red-Programming-Language.md` (107 lines) — § Core Features.
- `Red-Deep-Technical-Specification.md` (1318 lines) — full-stack diagram, toolchain stages.
- `Red-Technical-Specification-Part-III.md` (1997 lines) — datatype/system internals.
- `Red-Interpreter-Internals.md` (67 lines) — § XV dispatch table.
- `README.md`, `compiler.r`, `lexer.r`, `red.r`, `runtime/`, `system/`, `build/`, `tests/` — verified artifacts.

