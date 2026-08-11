# XXX. Ownership in Practice — Observable Data Model

```red
; ── Observable list — notifies on all mutations ─────────────────────
make-observable-list: func [
    "Create a list that fires callbacks on change"
    /local obs
][
    obs: make object! [
        items:      copy []
        listeners:  copy []

        on-deep-change*: func [
            owner word target action new index part
        ][
            ; Notify all registered listeners
            foreach cb listeners [
                cb owner word action new index part
            ]
        ]

        ; Public API
        add: func [item][append items item]
        remove-at: func [idx][remove at items idx]
        clear-all: does [clear items]

        on-change: func [callback [function!]][
            append listeners callback
        ]
    ]
    obs
]

; Usage
my-list: make-observable-list

; Register a listener
my-list/on-change func [owner word action new index part][
    print rejoin [
        "LIST CHANGED: action=" action
        " at index=" index
        " value=" mold new
    ]
]

my-list/add "apple"      ; → LIST CHANGED: action=insert at index=1
my-list/add "banana"     ; → LIST CHANGED: action=insert at index=2
my-list/remove-at 1      ; → LIST CHANGED: action=remove at index=1
;                            → LIST CHANGED: action=removed at index=1

; ── View-model binding using ownership ──────────────────────────────
view-model: make object! [
    name:   ""
    age:    0
    errors: copy []

    on-deep-change*: func [owner word target action new index part][
        ; Validate on change
        switch word [
            age [
                if any [new < 0  new > 150] [
                    append errors rejoin ["Invalid age: " new]
                ]
            ]
            name [
                if empty? new [
                    append errors "Name cannot be empty"
                ]
            ]
        ]
        ; Trigger UI refresh
        do-react view-model 'name
    ]
]
```