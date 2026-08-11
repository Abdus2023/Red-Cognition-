# XXVII. Transcode API — Complete Reference

```red
; ══════════════════════════════════════════════════════════════════
; TRANSCODE — the new lexer's public API
; ══════════════════════════════════════════════════════════════════

; Basic: convert string to block of Red values
transcode "42 hello [1 2 3]"
; → [42 hello [1 2 3]]

; /next — incremental, one token at a time
transcode/next "hello world" 'result
; → result = hello, returns position after token

; /only — return first value only
transcode/only "[1 2 3] rest"
; → [1 2 3]

; /trace — event-driven instrumentation
transcode/trace "42 + hello" func [
    event   [word!]     ; opened closed decoded scanned error
    input   [string! binary!]
    type    [datatype! word!]
    line    [integer!]
    token
][
    print rejoin [event ": " type " = " mold token]
]

; SCAN — identify type without loading value
scan "42"          ; → integer!
scan "hello"       ; → word!
scan "[1 2 3]"     ; → block!
scan "#(a: 1)"     ; → map!
scan "2026-07-29"  ; → date!

; ── Lexer pre-load hook — custom syntax preprocessing ──────────────
; Runs before lexing — can transform source text
system/lexer/pre-load: func [src type][
    ; Example: translate arrow syntax to Red words
    replace/all src "→" "to"
    replace/all src "←" "from"
]
```