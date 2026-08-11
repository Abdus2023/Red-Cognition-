# XXXI. Custom Scheme Implementation

```red
; ── Custom Scheme: in-memory key-value store ─────────────────────────
make-scheme [
    name:   'memstore
    title:  "In-Memory Key-Value Store"

    ; Shared store across all ports of this scheme
    store: make map! []

    actor: make object! [

        open: func [port [port!]][
            ; Initialise port state
            port/state: make object! [
                key: none
                value: none
            ]
            port
        ]

        read: func [port [port!]][
            ; Return value for current key
            key: port/spec/path
            select port/scheme/store key
        ]

        write: func [port [port!] data [any-type!]][
            ; Store value at key
            key: port/spec/path
            put port/scheme/store key data
            data
        ]

        query: func [port [port!]][
            ; Return all keys
            keys-of port/scheme/store
        ]

        delete: func [port [port!]][
            key: port/spec/path
            remove/key port/scheme/store key
        ]

        close: func [port [port!]][
            port/state: none
            port
        ]
    ]
]

; Usage
p: open memstore://mykey
write p "Hello from port system!"
print read p                          ; → Hello from port system!
print query p                         ; → all stored keys
close p

; ── GPIO Dialect for Raspberry Pi ───────────────────────────────────
; gpio:// scheme provides a domain-specific dialect for pin control
gpio-port: open gpio://

; GPIO dialect block
do-gpio: func [pins [block!]][
    parse pins [
        any [
            'pin set n integer! 'output (
                write gpio-port reduce ['pin n 'mode 'output]
            )
            | 'pin set n integer! 'high (
                write gpio-port reduce ['pin n 'state 'high]
            )
            | 'pin set n integer! 'low (
                write gpio-port reduce ['pin n 'state 'low]
            )
            | 'read 'pin set n integer! (
                read gpio-port
            )
            | 'wait set ms integer! 'ms (
                wait ms / 1000.0
            )
        ]
    ]
]

; Blink LED on pin 17
do-gpio [
    pin 17 output
    pin 17 high  wait 500 ms
    pin 17 low   wait 500 ms
]

close gpio-port
```