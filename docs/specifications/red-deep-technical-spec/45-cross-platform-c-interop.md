# XLVIII. Cross-Platform C Library Interop

```red
Red/System [Title: "Complete C Interop Examples"]

; ── Windows API via stdcall ───────────────────────────────────────────
#if OS = 'Windows [
    #import [
        "kernel32.dll" stdcall [
            GetTickCount: "GetTickCount" [
                return: [integer!]
            ]
            Sleep: "Sleep" [
                ms [integer!]
            ]
            GetLastError: "GetLastError" [
                return: [integer!]
            ]
            CreateFileA: "CreateFileA" [
                path       [c-string!]
                access     [integer!]
                share      [integer!]
                security   [integer!]
                creation   [integer!]
                flags      [integer!]
                template   [integer!]
                return:    [integer!]   ; HANDLE
            ]
        ]
        "user32.dll" stdcall [
            MessageBoxA: "MessageBoxA" [
                hwnd    [integer!]
                text    [c-string!]
                caption [c-string!]
                type    [integer!]
                return: [integer!]
            ]
        ]
    ]

    ; Windows popup dialog
    MessageBoxA 0 "Hello from Red/System!" "Red Alert" 0
]

; ── POSIX via cdecl ───────────────────────────────────────────────────
#if OS <> 'Windows [
    #import [
        "libc.so.6" cdecl [
            clock_gettime: "clock_gettime" [
                clk_id  [integer!]
                tp      [pointer! [integer!]]
                return: [integer!]
            ]
            usleep: "usleep" [
                useconds [integer!]
            ]
            system: "system" [
                cmd     [c-string!]
                return: [integer!]
            ]
        ]
    ]
]

; ── Callback — C calling back into Red/System ─────────────────────────
; Define callback type
compare-fn!: alias function! [
    a  [pointer! [integer!]]
    b  [pointer! [integer!]]
    return: [integer!]
]

#import [
    "libc.so.6" cdecl [
        qsort: "qsort" [
            base    [pointer! [integer!]]
            nmemb   [integer!]
            size    [integer!]
            compar  [compare-fn!]
            return: [integer!]
        ]
    ]
]

; Our comparison callback
int-compare: func [
    a  [pointer! [integer!]]
    b  [pointer! [integer!]]
    return: [integer!]
][
    a/value - b/value
]

; Sort an array using libc qsort
sort-integers: func [
    arr  [pointer! [integer!]]
    n    [integer!]
][
    qsort arr n 4 :int-compare    ; :int-compare → function pointer
]
```