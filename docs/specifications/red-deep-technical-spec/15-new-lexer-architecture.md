# XXVII. The New Lexer — Architecture and Instrumentation API

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│              RED LEXER v2 — INTERNAL ARCHITECTURE                    │
│              (Rewritten in Red/System for maximum performance)       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  INPUT: UTF-8 encoded string or binary buffer                        │
│                                                                      │
│  SCANNING PHASES:                                                    │
│  ┌───────────────────────────────────────────────────────────┐      │
│  │  Phase 1 — CHARACTER CLASSIFICATION                        │      │
│  │    Lookup table: byte → character class                   │      │
│  │    Classes: DIGIT ALPHA SPECIAL SPACE NEWLINE             │      │
│  │             STRING-START BINARY-START BLOCK-START etc.   │      │
│  └────────────────────────┬──────────────────────────────────┘      │
│                           │                                          │
│  ┌────────────────────────▼──────────────────────────────────┐      │
│  │  Phase 2 — TOKEN RECOGNITION (per-type scanners)           │      │
│  │                                                            │      │
│  │  scan-integer    : [+-]? digit+                            │      │
│  │  scan-float      : integer . digit* [e integer]?           │      │
│  │  scan-word       : alpha (alpha|digit|special-word-char)*  │      │
│  │  scan-string     : {"} chars {"}  OR {^{} chars {^}}      │      │
│  │  scan-binary     : #{hex-pairs}  2#{bits}  64#{b64}       │      │
│  │  scan-file       : % path-chars                            │      │
│  │  scan-url        : word :// rest                           │      │
│  │  scan-date       : DD-MMM-YYYY | YYYY-MM-DD variants       │      │
│  │  scan-time       : HH:MM:SS[.mmm][AM|PM]                  │      │
│  │  scan-pair       : integer x integer                       │      │
│  │  scan-tuple      : integer . integer . integer [...]       │      │
│  │  scan-issue      : # non-space+                            │      │
│  │  scan-char       : #" char "                               │      │
│  │  scan-email      : word @ domain                           │      │
│  │  scan-money      : [$|currency-code] digits [. digits]     │      │
│  │  scan-ref        : @ word                                  │      │
│  └────────────────────────┬──────────────────────────────────┘      │
│                           │                                          │
│  ┌────────────────────────▼──────────────────────────────────┐      │
│  │  Phase 3 — VALUE CONSTRUCTION                              │      │
│  │    Token string → typed Red value in memory               │      │
│  │    Word interning: symbol table lookup/insert             │      │
│  │    Buffer allocation via node system                       │      │
│  └────────────────────────┬──────────────────────────────────┘      │
│                           │                                          │
│  ┌────────────────────────▼──────────────────────────────────┐      │
│  │  INSTRUMENTATION API (Event-Oriented)                      │      │
│  │                                                            │      │
│  │  system/lexer/pre-load    : hook before lexing starts      │      │
│  │  system/lexer/on-token    : hook per token recognised      │      │
│  │  system/lexer/on-error    : hook on lexer error           │      │
│  │                                                            │      │
│  │  transcode/trace src [callback]   ; per-token events       │      │
│  │  scan src type                    ; scan without loading   │      │
│  │  transcode/next src               ; incremental lexing     │      │
│  └────────────────────────────────────────────────────────────┘      │
│                                                                      │
│  SUBROUTINES — intra-function factorisation (new in 0.6.x):         │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  Defined as separate blocks inside function bodies         │     │
│  │  Called like functions but with zero argument passing      │     │
│  │  One stack slot for return address only                    │     │
│  │  Analogous to GOSUB in BASIC                               │     │
│  │                                                            │     │
│  │  parse-digit: [                                            │     │
│  │      ; inlined routine — no function call overhead         │     │
│  │      ...                                                   │     │
│  │  ]                                                         │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```