# XXXIV. FPU Control in Red/System — Usage Patterns

```red
Red/System [Title: "FPU Control Examples"]

; ── Initialise FPU (required on IA-32 before float ops) ──────────────
system/fpu/init

; ── Trap division by zero ────────────────────────────────────────────
system/fpu/exception/mask/zero-divide: false    ; unmask = enable trap
system/fpu/update

; ── Trap invalid operations (like 0.0 / 0.0 = NaN) ──────────────────
system/fpu/exception/mask/invalid-op: false
system/fpu/update

; ── Set truncation rounding (for integer conversion) ─────────────────
system/fpu/option/rounding: 'truncate
system/fpu/update

x: 3.7
i: as integer! x     ; → 3 (truncated, not rounded)

; ── Restore default rounding ─────────────────────────────────────────
system/fpu/option/rounding: 'nearest
system/fpu/update

; ── Full precision mode (extended 80-bit on IA-32) ───────────────────
system/fpu/option/precision: 'extended
system/fpu/update

; ── Read/write hardware I/O port (requires ring 0 privileges) ────────
; p: declare pointer! [byte!]
; value: system/io/read p    ; read 8-bit hardware port
; system/io/write p 0xFF     ; write to hardware port
```