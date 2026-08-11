# XLVI. Event Handling — All Patterns

```red
; ══════════════════════════════════════════════════════════════════
; VIEW EVENT SYSTEM — COMPLETE PATTERN REFERENCE
; ══════════════════════════════════════════════════════════════════

; ── Pattern 1: Inline VID event handlers ────────────────────────────
view [
    f: field 200x25
    on-change [print rejoin ["Field changed: " face/text]]
    on-key    [if event/key = #"^M" [print "Enter pressed"]]
    on-focus  [print "Field focused"]
    on-unfocus [print "Field unfocused"]

    button "Submit"
    on-click    [print rejoin ["Clicked at: " event/offset]]
    on-dbl-click [print "Double clicked!"]
    on-over     [face/color: either event/over [red][gray]]
]

; ── Pattern 2: Actors object ─────────────────────────────────────────
my-actors: make object! [
    on-click: func [face event][
        print rejoin ["Button '" face/text "' clicked"]
    ]
    on-key: func [face event][
        switch event/key [
            #"^[" [quit]    ; Escape to quit
            #"^M" [submit]  ; Enter to submit
        ]
    ]
    on-time: func [face event][
        ; fires at rate: frequency
        update-display face
    ]
]

view [
    rate 10
    b: button "Actors Demo" actors my-actors
]

; ── Pattern 3: Global event handler ─────────────────────────────────
; Intercepts ALL events before face handlers
insert-event-func 'my-global-handler func [face event][
    ; Log all events
    if find [click key] event/type [
        print rejoin ["GLOBAL: " event/type " on " face/type]
    ]
    none    ; return none to continue processing
    ; return 'stop to consume event (prevent face handler)
]

; Remove global handler
remove-event-func 'my-global-handler

; ── Pattern 4: Key detection utilities ──────────────────────────────
key-name: func [event [event!]][
    case [
        event/key = #"^M"  ['enter]
        event/key = #"^["  ['escape]
        event/key = #"^H"  ['backspace]
        event/key = #"^I"  ['tab]
        find event/flags 'shift  ['shift-key event/key]
        find event/flags 'ctrl   ['ctrl-key  event/key]
        find event/flags 'alt    ['alt-key   event/key]
        true [event/key]
    ]
]

; ── Pattern 5: Drag and drop ─────────────────────────────────────────
view [
    source: base 100x100 red
    on-click [
        ; Begin drag
        drag-face: source
    ]

    target: base 100x100 blue
    on-drop [
        ; Handle drop
        print rejoin ["Dropped " event/face/color " onto target"]
        target/color: event/face/color
    ]
]

; ── Pattern 6: Timer-driven animation ───────────────────────────────
angle: 0.0
view [
    title "Rotating Arc"
    rate 60        ; 60 fps
    canvas: base 300x300 black
    draw [
        pen white  line-width 3
        arc 150x150 100x100 0 270
    ]
    on-time [
        angle: mod angle + 2.0 360.0
        canvas/draw: compose [
            fill-pen black
            box 0x0 300x300
            pen white  line-width 3
            pen (to-color reduce [
                to-integer 128 + 127 * sin to-radians angle
                to-integer 128 + 127 * cos to-radians angle
                200
            ])
            arc 150x150 100x100 (to-integer angle) 120
        ]
    ]
]
```