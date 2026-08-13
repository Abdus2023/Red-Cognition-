# RFC-0023 — New Lexer v2 & Instrumentation API Finalisation

**RFC:** RFC-0023
**Title:** New Lexer v2 & Instrumentation API Finalisation — Red/System High-Performance Lexer
**Stable ID(s):** `RED-LEXER-V2-001`
**Origin:** MSG-09 §XXVII `Red-Technical-Specification-Part-III.md` — Parse-dialect lexer → Red/System rewrite for near-instant loading of huge quantities of Red values, scanning without loading, event-oriented instrumentation; `lexer.r` 26389 B vs Red/System speculative path.
**Evolution:** RFC-0002/0009 noted `Implemented` (Parse) / `Partially Implemented` (Red/System) split; this RFC finalises the v2 spec.
**Final Representation:** This RFC + `transcode` event-API + character class table + scanning phases + benchmark vs Parse.
**Status:** `Draft` — P2 (performance, closes MSG-09 open item)
**Verification:** `transcode` instrumentation API covers phase coverage; v2 loads huge Red value fixture faster than Parse baseline beyond threshold; no regression to `RED-SPEC-015` dispatch.

---

## 1. Specification

Per `Red-Technical-Specification-Part-III.md` §§XXVII–XXXIX (normative source):

- **Character class table:** `byte → class (DIGIT ALPHA SPECIAL SPACE NEWLINE STRING-START BINARY-START BLOCK-START …)`.
- **Scanning phases:** classification → value identification → datatype tagging without full load (for `load` vs `scan`).
- **Instrumentation API:** event-oriented (`on-token`, `on-type`, `on-error`) customisation of behaviour.

## 2. Traceability

- **OP:** MSG-09 open item (Performance).
- **REQs:** REQ-022 extension.

