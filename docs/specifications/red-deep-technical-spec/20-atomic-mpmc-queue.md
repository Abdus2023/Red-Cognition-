# XXIX. Lock-Free MPMC Queue — Implementation Pattern

```red
Red/System [Title: "Lock-Free MPMC Queue using Atomic CAS"]

; Queue node structure
node!: alias struct! [
    value [integer!]
    next  [pointer! [integer!]]   ; points to next node!
]

; Queue head and tail (shared between threads)
queue-head: declare pointer! [integer!]   ; consumer pointer
queue-tail: declare pointer! [integer!]   ; producer pointer

; ── Initialise empty queue ─────────────────────────────────────────
init-queue: func [/local sentinel][
    sentinel: as node! allocate size? node!
    sentinel/next: null
    queue-head: as pointer! [integer!] sentinel
    queue-tail: as pointer! [integer!] sentinel
]

; ── Enqueue (Producer) — CAS on tail ──────────────────────────────
enqueue: func [
    val     [integer!]
    return: [logic!]
    /local new-node tail next
][
    new-node: as node! allocate size? node!
    new-node/value: val
    new-node/next: null

    forever [
        tail: as node! system/atomic/load queue-tail
        next: as node! system/atomic/load
            as pointer! [integer!] tail + (offset? node! next)

        ; Tail still consistent?
        if tail = (as node! system/atomic/load queue-tail) [
            either null? next [
                ; Tail at last node — try to link new node
                if system/atomic/cas
                    as pointer! [integer!] tail + (offset? node! next)
                    as integer! null
                    as integer! new-node
                [
                    ; Successfully linked — advance tail (can fail, ok)
                    system/atomic/cas queue-tail
                        as integer! tail
                        as integer! new-node
                    return true
                ]
            ][
                ; Tail not pointing to last — advance it
                system/atomic/cas queue-tail
                    as integer! tail
                    as integer! next
            ]
        ]
    ]
    true
]

; ── Dequeue (Consumer) — CAS on head ──────────────────────────────
dequeue: func [
    result  [pointer! [integer!]]
    return: [logic!]
    /local head tail next
][
    forever [
        head: as node! system/atomic/load queue-head
        tail: as node! system/atomic/load queue-tail
        next: as node! system/atomic/load
            as pointer! [integer!] head + (offset? node! next)

        if head = (as node! system/atomic/load queue-head) [
            either head = tail [
                if null? next [return false]   ; queue empty
                ; Tail falling behind — advance it
                system/atomic/cas queue-tail
                    as integer! tail
                    as integer! next
            ][
                ; Read value before CAS (another thread may free node)
                result/value: (as node! next)/value
                ; Try to swing head to next
                if system/atomic/cas queue-head
                    as integer! head
                    as integer! next
                [
                    free as byte-ptr! head
                    return true
                ]
            ]
        ]
    ]
    false
]
```