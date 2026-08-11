# XLI. Complete Error Handling Patterns

```red
; ══════════════════════════════════════════════════════════════════
; RED ERROR HANDLING — ALL PATTERNS
; ══════════════════════════════════════════════════════════════════

; ── Pattern 1: Basic try/error? ──────────────────────────────────────
safe-divide: func [a [number!] b [number!]][
    result: try [a / b]
    either error? result [
        print rejoin ["Division error: " result/id]
        none
    ][
        result
    ]
]

print safe-divide 10 2      ; → 5
print safe-divide 10 0      ; → Division error: zero-divide

; ── Pattern 2: try/with — inline handler ────────────────────────────
load-config: func [path [file!]][
    try/with [
        data: load path
        unless block? data [cause-error 'user 'message ["Not a block"]]
        data
    ] func [err][
        print rejoin ["Config error [" err/type "/" err/id "]: "
            err/message]
        ; Return default config
        [host: "localhost" port: 8080]
    ]
]

; ── Pattern 3: attempt for optional operations ─────────────────────
; Returns none silently on any error
img: attempt [load %missing-image.png]   ; none if file missing
if img [display img]

; ── Pattern 4: Nested error handling with re-throw ──────────────────
process-file: func [path [file!]][
    outer: try [
        inner: try [read path]
        if error? inner [
            ; Wrap with more context
            cause-error 'access 'cannot-open path
        ]
        parse-content inner
    ]
    if error? outer [
        ; Log and propagate
        log-error outer
        do outer     ; re-throw
    ]
]

; ── Pattern 5: Custom error type ────────────────────────────────────
; Define custom error category
system/error/cognitive: make object! [
    type:    'cognitive
    budget-exceeded: ["Reasoning budget exceeded: $" :arg1]
    belief-conflict: ["Conflicting beliefs about:" :arg1]
    goal-failed:     ["Goal failed after" :arg1 "retries"]
]

; Throw custom cognitive error
throw-cognitive-error: func [id [word!] arg [any-type!]][
    e: make error! [
        type: 'cognitive
        id:   id
        arg1: arg
    ]
    do e
]

; ── Pattern 6: Comprehensive error wrapper ──────────────────────────
with-error-handling: func [
    "Execute body with full error classification and logging"
    body    [block!]
    /log    log-fn [function!]
    /default def-val [any-type!]
][
    result: try body
    either error? result [
        msg: rejoin [
            "[" result/type "/" result/id "] "
            either string? result/message [result/message]["unknown"]
            either result/near [rejoin [" near: " result/near]][""] 
        ]
        if log [log-fn msg]
        either default [def-val][none]
    ][
        result
    ]
]

; ── Pattern 7: Stack trace inspection ───────────────────────────────
debug-error: func [err [error!]][
    print "=== Error Report ==="
    print rejoin ["Type:    " err/type]
    print rejoin ["ID:      " err/id]
    print rejoin ["Message: " err/message]
    print rejoin ["Near:    " err/near]
    print rejoin ["Where:   " err/where]
    if block? err/stack [
        print "Stack:"
        foreach frame err/stack [
            print rejoin ["  -> " frame]
        ]
    ]
    print "==================="
]
```