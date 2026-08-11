# XLV. Console Customisation and Startup File

```red
; ── ~/.red/user.r — console startup file ────────────────────────────

; Custom prompt
system/console/prompt: "cog> "

; Define console shortcuts
cls: does [prin "^[[2J^[[H"]    ; ANSI clear screen

; Pretty-print helper
pp: func [v][probe v  ()]

; Timing shorthand (already built-in as DT but useful alias)
time-it: func [code [block!]][
    start: now/precise
    result: do code
    elapsed: now/precise - start
    print rejoin ["Elapsed: " elapsed]
    result
]

; Quick documentation lookup
??: func [word [any-word!]][
    help word
]

; Context browser
ls: func [obj [object!]][
    foreach w words-of obj [
        v: get in obj w
        print rejoin ["  " pad form w 20 " : " type? v]
    ]
]

; Load common utilities on startup
; load %my-utils.red
```