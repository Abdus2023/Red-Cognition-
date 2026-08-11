# XVI. The Word and Context System — Binding Architecture

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│           RED CONTEXT AND WORD BINDING SYSTEM                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  CONTEXT STRUCTURE:                                                  │
│  ┌──────────────────────────────────────────────────────┐           │
│  │  context! (internal)                                 │           │
│  │    symbols:  [word1 word2 word3 ...]  ; symbol table │           │
│  │    values:   [val1  val2  val3  ...]  ; value array  │           │
│  │    parent:   context! | none          ; scope chain  │           │
│  └──────────────────────────────────────────────────────┘           │
│                                                                      │
│  CONTEXT HIERARCHY:                                                  │
│                                                                      │
│  system/words   ← GLOBAL context (all built-ins live here)          │
│       │                                                              │
│       ▼                                                              │
│  object context  ← created by make object! [...] or context [...]   │
│       │                                                              │
│       ▼                                                              │
│  function context ← created per function call (locals + args)       │
│                                                                      │
│  WORD BINDING STATES:                                                │
│  ┌──────────────────────────────────────────────────────┐           │
│  │  UNBOUND word   → symbol exists but has no context   │           │
│  │  BOUND word     → symbol points to a specific        │           │
│  │                   context slot                       │           │
│  │  UNSET word     → bound to context but value is      │           │
│  │                   unset! (not none!)                 │           │
│  └──────────────────────────────────────────────────────┘           │
│                                                                      │
│  BINDING OPERATIONS:                                                 │
│                                                                      │
│  bind block context      ; bind all words in block to context        │
│  bind/new block context  ; bind + create new words in context        │
│  bind/only block context ; bind only words already in context        │
│  unbind word             ; remove context binding                    │
│  in obj 'word            ; check if word is in object                │
│  context? word           ; get context word is bound to              │
│                                                                      │
│  BINDING EXAMPLE:                                                    │
│                                                                      │
│  x: 10                    ; x bound in global context               │
│                                                                      │
│  obj: make object! [                                                 │
│      x: 20                ; x bound in obj's context                │
│      get-x: does [x]      ; closure over obj context                │
│  ]                                                                   │
│                                                                      │
│  x              ; → 10  (global)                                     │
│  obj/x          ; → 20  (obj context, path access)                  │
│  obj/get-x      ; → 20  (function reads obj's x)                    │
│                                                                      │
│  ; Explicit binding for meta-programming:                            │
│  code: [print x]          ; x is unbound in this block              │
│  bind code obj            ; bind x to obj's context                 │
│  do code                  ; → prints 20                             │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```