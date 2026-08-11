# XIX. The Macro and Preprocessor System

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│            RED PREPROCESSOR DIRECTIVE SYSTEM                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  COMPILATION DIRECTIVES (processed before evaluation):               │
│                                                                      │
│  #include %file.red              ; inline another file's content     │
│  #include %relative/path.red                                         │
│                                                                      │
│  #if <condition> [<code>]        ; conditional compilation           │
│  #either <cond> [<yes>] [<no>]   ; if-either at compile time        │
│  #switch <val> [<case> [<code>] ...] ; switch at compile time       │
│                                                                      │
│  #define WORD value              ; constant substitution             │
│  #define WORD [block]            ; block substitution                │
│                                                                      │
│  ── MACRO SYSTEM ─────────────────────────────────────────────      │
│                                                                      │
│  Red-level macros (transform code at load time):                     │
│                                                                      │
│  #macro 'unless func [s e][     ; 'unless' macro                    │
│      change s 'if                                                    │
│      insert next s 'not                                              │
│      s                                                               │
│  ]                                                                   │
│                                                                      │
│  ; Now 'unless' works as a conditional:                              │
│  unless x > 0 [print "non-positive"]                                 │
│  ; Expands to: if not x > 0 [print "non-positive"]                  │
│                                                                      │
│  #macro [integer! '+  integer!] func [s e][   ; pattern macro       │
│      ; match pattern: integer + integer                              │
│      ; can fold constants at load time                               │
│      change/part s (s/1 + s/3) 3                                    │
│      s                                                               │
│  ]                                                                   │
│                                                                      │
│  ── pre-load HOOK ─────────────────────────────────────────────     │
│                                                                      │
│  ; Plug into the lexer's pre-processing pipeline:                    │
│  system/lexer/pre-load: func [src type][                             │
│      ; transform src string before lexing                            │
│      ; enables custom syntax extensions                              │
│      replace/all src "→" "->"                                        │
│  ]                                                                   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```