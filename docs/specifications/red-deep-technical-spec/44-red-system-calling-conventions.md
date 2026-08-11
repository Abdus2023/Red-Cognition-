# XLVIII. Red/System Calling Conventions — Complete Specification

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│         RED/SYSTEM CALLING CONVENTIONS — COMPLETE SPECIFICATION      │
│         (From static.red-lang.org/red-system-specs.html)             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  SUPPORTED CALLING CONVENTIONS:                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  cdecl     — C default (Linux/macOS/MinGW standard)          │   │
│  │  stdcall   — Windows API standard (__stdcall)                │   │
│  │  fastcall  — Optimised: first args in registers (x86)        │   │
│  │  unix64    — System V AMD64 ABI (Linux/macOS 64-bit)         │   │
│  │  win64     — Microsoft x64 ABI (Windows 64-bit)              │   │
│  │  fallback  — Portable, always-correct (no optimisation)      │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  CDECL (Default):                                                    │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Stack-based parameter passing                               │   │
│  │  Arguments pushed RIGHT to LEFT                              │   │
│  │  CALLER cleans up the stack (not the callee)                 │   │
│  │  Return value in EAX (integer/pointer) or FPU ST(0) (float) │   │
│  │  Preserved registers: EBX ESI EDI EBP                        │   │
│  │  Scratch registers:   EAX ECX EDX                            │   │
│  │                                                              │   │
│  │  Stack frame layout (IA-32 cdecl):                          │   │
│  │                                                              │   │
│  │    [ESP+N]   last arg                                        │   │
│  │    ...                                                       │   │
│  │    [ESP+8]   arg2                                            │   │
│  │    [ESP+4]   arg1                                            │   │
│  │    [ESP+0]   return address       ← ESP after CALL           │   │
│  │    [EBP-4]   local var 1          ← after PUSH EBP / MOV    │   │
│  │    [EBP-8]   local var 2                                     │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  STDCALL (Windows API):                                              │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Arguments pushed RIGHT to LEFT (same as cdecl)             │   │
│  │  CALLEE cleans up the stack (RET N instruction)              │   │
│  │  Required for: Win32 API, COM interfaces, callbacks          │   │
│  │  Decorated names: *FunctionName@ArgBytes                     │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ARM CALLING CONVENTION (AAPCS):                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  First 4 args in registers: R0 R1 R2 R3                      │   │
│  │  Additional args: stack                                      │   │
│  │  Return: R0 (integer/pointer)  or  D0 (float)               │   │
│  │  Preserved: R4-R11 R13(SP) R14(LR)                           │   │
│  │  Scratch:   R0-R3 R12 R14                                    │   │
│  │                                                              │   │
│  │  Integer division: ARM raises exception on div-by-zero       │   │
│  │  BUT some ARM chips silently return 0                        │   │
│  │  R/S compiler generates extra detection code on ARM targets  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  DECLARATION SYNTAX:                                                 │
│                                                                      │
│    my-func: func [cdecl] [x [integer!] return: [integer!]][]        │
│    ; OR in #import:                                                  │
│    #import ["libc.so.6" cdecl [malloc: "malloc" [...]]]             │
│    #import ["kernel32.dll" stdcall [CreateFile: "CreateFileA" [...]]]│
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```