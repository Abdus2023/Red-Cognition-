# XXVIII. Routine Examples — All Major Patterns

```red
Red [Title: "Routine! Examples"]

; ── Pattern 1: Pure computation — integer arithmetic ───────────────
fast-pow: routine [
    "Compute base^exp using Red/System (compiled native)"
    base [integer!]
    exp  [integer!]
    return: [integer!]
][
    result: 1
    loop exp [result: result * base]
    result
]

print fast-pow 2 10   ; → 1024  (compiled, not interpreted)

; ── Pattern 2: Byte-level string processing ──────────────────────
count-bytes: routine [
    "Count occurrences of byte in string using direct memory scan"
    str   [string!]
    byte  [char!]       ; char! maps to byte! in R/S
    return: [integer!]
    /local count ptr
][
    count: 0
    ptr: as c-string! str
    while [ptr/1 <> #"^(00)"] [    ; until null terminator
        if ptr/1 = byte [count: count + 1]
        ptr: ptr + 1
    ]
    count
]

print count-bytes "hello world" #"l"  ; → 3

; ── Pattern 3: OS system call ─────────────────────────────────────
#import [
    "libc.so.6" cdecl [
        c-getpid: "getpid" [return: [integer!]]
    ]
]

get-pid: routine [
    "Get current process ID via OS syscall"
    return: [integer!]
][
    c-getpid
]

print get-pid   ; → current PID

; ── Pattern 4: struct manipulation ───────────────────────────────
point3d!: alias struct! [
    x [float!]
    y [float!]
    z [float!]
]

dot-product: routine [
    "3D dot product — returns float"
    ax [float!]  ay [float!]  az [float!]
    bx [float!]  by [float!]  bz [float!]
    return: [float!]
][
    (ax * bx) + (ay * by) + (az * bz)
]

print dot-product 1.0 0.0 0.0  0.0 1.0 0.0  ; → 0.0

; ── Pattern 5: LibRed callback — C calls Red ─────────────────────
; From C side:
; redRoutine(redWord("add-from-c"),
;            "[a [integer!] b [integer!] return: [integer!]]",
;            (void*)&my_c_add);
```