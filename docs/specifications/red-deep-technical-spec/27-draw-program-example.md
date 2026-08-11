# XXXIII. Complete Draw Program — All Features Demonstrated

```red
Red [Title: "Draw Dialect Complete Demonstration"]

; ── Create target image ──────────────────────────────────────────────
canvas: make image! 800x600

draw canvas [

    ; ── BACKGROUND ─────────────────────────────────────────────────
    fill-pen linear 0x0 800x0 pad [
        255.200.50 0.0    ; gold at left
        255.100.0  0.5    ; orange at centre
        200.50.255 1.0    ; purple at right
    ]
    pen off
    box 0x0 800x600

    ; ── COORDINATE TRANSFORM DEMONSTRATION ─────────────────────────
    push [
        translate 100x100
        rotate 45.0 200x200
        pen white  line-width 2  fill-pen 0.100.255.200
        box 0x0 200x200 10        ; rounded rect, 10px radius
    ]

    ; ── BEZIER CURVE ────────────────────────────────────────────────
    pen yellow  line-width 3  fill-pen off
    curve 50x400  150x300  250x500  350x350

    ; ── SPLINE ──────────────────────────────────────────────────────
    pen cyan  line-width 2
    spline [
        400x500  450x400  500x480
        550x380  600x460  650x350
        700x430  750x380
    ]

    ; ── SHADOW AND CIRCLE ───────────────────────────────────────────
    shadow 5x5 black 8    ; 8px blur
    fill-pen radial 600x150 0 80 pad [
        white    0.0
        255.50.50 0.5
        red      1.0
    ]
    pen off
    circle 600x150 80

    ; ── RESET SHADOW ────────────────────────────────────────────────
    shadow off

    ; ── TEXT RENDERING ──────────────────────────────────────────────
    push [
        font make font! [
            name: "Arial"  size: 24
            color: white   style: 'bold
        ]
        pen off  fill-pen white
        text 50x50 "Red Draw Dialect"
    ]

    ; ── CLIP DEMONSTRATION ──────────────────────────────────────────
    push [
        clip 300x200 550x400      ; circular clip region
        fill-pen 50.200.50
        circle 425x300 120
        pen white  line-width 1
        line 300x200 550x400
        line 300x400 550x200
    ]

    ; ── POLYGON ─────────────────────────────────────────────────────
    fill-pen 255.200.0.180     ; semi-transparent gold
    pen white  line-width 2
    polygon [
        400x100  430x190  520x190
        460x245  480x340  400x290
        320x340  340x245  280x190
        370x190
    ]

    ; ── POSITION MARKS ──────────────────────────────────────────────
    translate 650x450
    pen blue  fill-pen sky
    set-mark p1
    circle 0x0 40
    set-mark p2
    line 0x0 p1        ; line from current back to saved mark
]

; Display result
view [
    title "Draw Demo"
    image canvas
    button "Save" [save %draw-output.png canvas]
]
```