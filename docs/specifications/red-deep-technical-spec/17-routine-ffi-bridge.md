# XXVIII. The `routine!` Datatype — Red/System FFI Bridge

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│              ROUTINE! — THE RED/RED SYSTEM BRIDGE                    │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  PURPOSE: Embed compiled Red/System code inside Red programs         │
│  Use case: performance-critical sections, direct OS access,          │
│            hardware manipulation from high-level code                │
│                                                                      │
│  DECLARATION SYNTAX:                                                 │
│                                                                      │
│    routine-name: routine [                                           │
│        arg1  [red-type!]                                             │
│        arg2  [red-type!]                                             │
│        return: [red-type!]     ; optional                            │
│    ][                                                                │
│        ; Red/System code body                                        │
│        ; native types available: integer! float! logic! byte!        │
│        ; Red values auto-converted via type-map                      │
│    ]                                                                 │
│                                                                      │
│  TYPE CONVERSION TABLE (Red → Red/System):                          │
│  ┌────────────────────┬─────────────────────────────────────┐       │
│  │  Red type          │  Red/System type                    │       │
│  ├────────────────────┼─────────────────────────────────────┤       │
│  │  integer!          │  integer!   (32-bit signed)         │       │
│  │  float!            │  float!     (64-bit double)         │       │
│  │  float32!          │  float32!   (32-bit float)          │       │
│  │  char!             │  byte!      (8-bit unsigned)        │       │
│  │  logic!            │  logic!     (bool)                  │       │
│  │  string!           │  c-string!  (pointer to UTF-8)      │       │
│  │  block!            │  pointer! [red-value!]              │       │
│  │  any-type!         │  red-value! (generic value ptr)     │       │
│  └────────────────────┴─────────────────────────────────────┘       │
│                                                                      │
│  COMPILATION: Routines are compiled when the containing              │
│  Red source is compiled. The R/S body is compiled inline             │
│  and a trampoline wrapper handles type conversion.                   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```