# XLII. Vector Operations — Complete Usage

```red
; ── Construction ─────────────────────────────────────────────────────
v-int:   make vector! [integer! 32 [10 20 30 40 50]]
v-float: make vector! [float!   64 [1.0 2.0 3.0 4.0 5.0]]
v-byte:  make vector! [integer! 8  256]   ; 256 zero bytes

; ── Element-wise arithmetic (in-place) ──────────────────────────────
v1: make vector! [integer! 32 [1 2 3 4 5]]
v2: make vector! [integer! 32 [10 20 30 40 50]]

add v1 v2          ; v1 = [11 22 33 44 55] (in-place)
multiply v1 2      ; v1 = [22 44 66 88 110]
subtract v1 v2     ; v1 = [12 24 36 48 60]
divide v1 3        ; v1 = [4 8 12 16 20]

; ── Scalar arithmetic (returns new vector) ───────────────────────────
v3: v-float + 1.0    ; each element + 1.0
v4: v-float * 2.0    ; each element * 2.0
v5: v-float - v3     ; element-wise subtraction

; ── Aggregate functions ──────────────────────────────────────────────
print sum    v-int   ; → 150
print average v-int  ; → 30.0
print maximum v-int  ; → 50
print minimum v-int  ; → 10

; ── Direct memory access via routine! ───────────────────────────────
; Vectors expose raw data pointer for C interop
simd-dot-product: routine [
    "SSE2 dot product — requires vector! float32"
    a   [vector!]
    b   [vector!]
    n   [integer!]
    return: [float!]
    /local sum pa pb i
][
    sum: 0.0
    pa: as pointer! [float32!] (as series! a)/offset
    pb: as pointer! [float32!] (as series! b)/offset
    i: 0
    loop n [
        sum: sum + as float! (pa/i * pb/i)
        i: i + 1
    ]
    sum
]

; ── Image processing example ─────────────────────────────────────────
; Image pixels as integer!8 RGBA vector
w: 256  h: 256
pixels: make vector! reduce ['integer! 8  w * h * 4]

; Fill with gradient
repeat y h [
    repeat x w [
        idx: ((y - 1) * w + (x - 1)) * 4 + 1
        poke pixels idx           x                  ; R
        poke pixels idx + 1       y                  ; G
        poke pixels idx + 2       (256 - x)          ; B
        poke pixels idx + 3       255                ; A
    ]
]

; Wrap as image for display
img: make image! reduce [as-pair w h pixels]
view [image img]

; ── Cognitive embedding vector ───────────────────────────────────────
; Store 768-dimensional semantic embedding as float32 vector
make-embedding: func [dimensions [integer!]][
    make vector! reduce ['float! 32 dimensions]
]

embedding-a: make-embedding 768
embedding-b: make-embedding 768

; cosine-similarity routine from Section XXVIII would operate here
```