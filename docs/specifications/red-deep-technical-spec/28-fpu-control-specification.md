# XXXIV. Red/System FPU Control — Complete Technical Reference

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│         RED/SYSTEM FPU CONTROL — COMPLETE SPECIFICATION              │
│         (From static.red-lang.org/red-system-specs.html)             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  FPU EXCEPTION MASK BITS:                                            │
│  ┌──────┬───┬───┬───┬───┬───┬───┐                                   │
│  │  Bit │ID │ IX│ UF│ OF│ DZ│ IO│                                   │
│  ├──────┼───┼───┼───┼───┼───┼───┤                                   │
│  │  Name│ID │IX │UF │OF │DZ │IO │                                   │
│  ├──────┼───┼───┼───┼───┼───┼───┤                                   │
│  │Meaning│Inp│Pre│Und│Ove│Div│Inv│                                   │
│  │      │Den│cis│erf│erf│/0 │Op │                                   │
│  └──────┴───┴───┴───┴───┴───┴───┘                                   │
│                                                                      │
│  FPU CONTROL OPERATIONS:                                             │
│                                                                      │
│  system/fpu/update                                                   │
│    ; Apply all pending FPU option changes                            │
│    ; On ARM: changes are immediate, this is a no-op                  │
│    ; On IA-32: required to flush pending changes to hardware         │
│                                                                      │
│  system/fpu/init                                                     │
│    ; Initialise FPU to known state                                   │
│    ; Required on IA-32 before floating-point ops                     │
│    ; On ARM: no-op                                                   │
│                                                                      │
│  system/fpu/control-word                                             │
│    ; Get or set full FPU control register (integer!)                 │
│    ; WARNING: ARM side-effects (shared with status flags)           │
│                                                                      │
│  FPU EXCEPTION FLAGS:                                                │
│    system/fpu/exception/mask/precision:        logic!                │
│    system/fpu/exception/mask/underflow:        logic!                │
│    system/fpu/exception/mask/overflow:         logic!                │
│    system/fpu/exception/mask/zero-divide:      logic!                │
│    system/fpu/exception/mask/invalid-op:       logic!                │
│    system/fpu/exception/mask/denormal:         logic!                │
│                                                                      │
│  ROUNDING MODES:                                                     │
│    system/fpu/option/rounding                                        │
│      nearest   ; round to nearest even (default, IEEE-754)          │
│      down      ; round toward -∞                                     │
│      up        ; round toward +∞                                     │
│      truncate  ; round toward zero                                   │
│                                                                      │
│  PRECISION MODES (IA-32 only):                                       │
│    system/fpu/option/precision                                       │
│      single    ; 32-bit precision                                    │
│      double    ; 64-bit precision (default)                          │
│      extended  ; 80-bit extended precision                           │
│                                                                      │
│  IO PORT ACCESS (low-level hardware):                                │
│    system/io/read  <port-address>    ; read from HW I/O port        │
│    system/io/write <port-address> <value>  ; write to HW I/O port   │
│    The returned/written value type depends on pointer type used.     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```