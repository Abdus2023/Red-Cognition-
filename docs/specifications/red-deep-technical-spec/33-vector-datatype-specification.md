# XLII. The `vector!` Datatype — Complete Specification

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│              VECTOR! DATATYPE — COMPLETE SPECIFICATION               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  PURPOSE: Typed, compact numeric arrays for performance-critical     │
│  applications. Unlike block! which stores heterogeneous Red values,  │
│  vector! stores a single type contiguously in memory.               │
│                                                                      │
│  SUPPORTED ELEMENT TYPES:                                            │
│  ┌───────────────┬──────────────────────────────────────────┐       │
│  │  Type         │  Width   │  Range                        │       │
│  ├───────────────┼──────────────────────────────────────────┤       │
│  │  integer! 8   │  8-bit   │  0 to 255 (unsigned)          │       │
│  │  integer! 16  │  16-bit  │  0 to 65535                   │       │
│  │  integer! 32  │  32-bit  │  ±2 billion                   │       │
│  │  integer! 64  │  64-bit  │  ±9.2 × 10^18                 │       │
│  │  float!   32  │  32-bit  │  IEEE 754 single              │       │
│  │  float!   64  │  64-bit  │  IEEE 754 double              │       │
│  │  char!        │  32-bit  │  Unicode code points          │       │
│  └───────────────┴──────────────────────────────────────────┘       │
│                                                                      │
│  CONSTRUCTION SYNTAX:                                                │
│                                                                      │
│  make vector! [integer! 32 1000]    ; 1000-element int32 vector     │
│  make vector! [float! 64 500]       ; 500-element float64 vector    │
│  make vector! [integer! 8 [1 2 3 4]]; from literal block            │
│                                                                      │
│  Shorthand factory:                                                  │
│  random/only make vector! [integer! 32 N]  ; random fill            │
│                                                                      │
│  MEMORY LAYOUT:                                                      │
│  ┌───────────────────────────────────────────────────────────┐      │
│  │  Series header (standard Red series HDR)                  │      │
│  │  type-bits: 2   (element type encoding)                   │      │
│  │  unit:      1|2|4|8  (bytes per element)                  │      │
│  │  ┌──┬──┬──┬──┬──┬──┬──┬──┬──┐                            │      │
│  │  │e0│e1│e2│e3│e4│e5│e6│e7│..│  contiguous element data   │      │
│  │  └──┴──┴──┴──┴──┴──┴──┴──┴──┘                            │      │
│  │  No boxing — raw binary values                            │      │
│  │  Cache-friendly sequential access                         │      │
│  └───────────────────────────────────────────────────────────┘      │
│                                                                      │
│  OPERATIONS — subset of series operations:                           │
│    append  insert  remove  clear  copy                               │
│    length? head tail next back  at  pick  poke                       │
│    sort  reverse  find  skip                                         │
│    +  -    */  (element-wise arithmetic)                            │
│    add  subtract  multiply  divide  (in-place variants)              │
│    sum  average  maximum  minimum  (aggregate ops)                   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```