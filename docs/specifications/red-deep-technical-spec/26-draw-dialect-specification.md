# XXXIII. The Draw Dialect — Complete Technical Specification

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│              DRAW DIALECT — COMPLETE COMMAND REFERENCE               │
│              Vector 2D graphics for Red/View                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  INVOCATION:                                                         │
│    draw image! [draw-commands]     ; render to image!               │
│    view [base 400x300 draw [...]]  ; render to canvas face           │
│                                                                      │
│  CANVAS STATE:                                                       │
│    pen          color | off        ; stroke colour                   │
│    fill-pen     color | off        ; fill colour                     │
│    line-width   float!             ; stroke width (pixels)           │
│    line-join    miter|round|bevel  ; corner style                    │
│    line-cap     flat|square|round  ; end cap style                   │
│    anti-alias   on | off           ; enable anti-aliasing            │
│    font         font-object        ; text rendering font             │
│    shadow       pair! color [blur [spread]] ; drop shadow            │
│                                                                      │
│  PRIMITIVES:                                                         │
│    line    pair! pair! [pair! ...]     ; polyline                    │
│    box     pair! pair! [radius]        ; rect [with rounded corners] │
│    circle  pair! integer!              ; center radius               │
│    ellipse pair! pair!                 ; center size                 │
│    arc     pair! pair! integer! integer! [sweep] ; arc               │
│    curve   pair! pair! pair! [pair!]   ; bezier curve                │
│    spline  [pair! ...] [closed]        ; catmull-rom spline          │
│    polygon [pair! ...]                 ; filled polygon              │
│    triangle pair! pair! pair!          ; 3-point polygon             │
│                                                                      │
│  TEXT:                                                               │
│    text    pair! string!              ; render string at position    │
│    text    pair! pair! string!        ; render in bounding box       │
│                                                                      │
│  IMAGES:                                                             │
│    image   image!                     ; render at 0x0               │
│    image   image! pair!               ; render at position           │
│    image   image! pair! pair!         ; render with size             │
│    image   image! pair! pair! [key-color [border]] ; keyed          │
│                                                                      │
│  TRANSFORMS:                                                         │
│    translate pair!                    ; move coordinate origin       │
│    scale     float! float!            ; scale x and y               │
│    rotate    float! [pair!]           ; rotate [around center]       │
│    skew      float! [float!]          ; shear x [and y]             │
│    matrix    [6 floats]               ; 2D affine matrix             │
│    reset-matrix                       ; restore identity matrix      │
│    invert-matrix                      ; invert current matrix        │
│                                                                      │
│  GRADIENTS:                                                          │
│    fill-pen linear  pair! pair! [pad|repeat|reflect]                 │
│              [color float! ...]  ; gradient stops                    │
│    fill-pen radial  pair! integer! integer! [pad|repeat|reflect]     │
│              [color float! ...]                                      │
│    fill-pen diamond pair! pair! integer! [pad|repeat|reflect]        │
│              [color float! ...]                                      │
│                                                                      │
│  CLIPPING:                                                           │
│    clip pair! pair!               ; rectangular clip region          │
│    clip [draw-commands]           ; clip to path                     │
│                                                                      │
│  STATE SAVE/RESTORE:                                                 │
│    push [draw-commands]           ; save state, restore after block  │
│                                                                      │
│  POSITION MARKS (Red 0.6.0+):                                        │
│    set-mark word!                 ; save current position to word    │
│    ; word then contains pair! of current canvas position            │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```