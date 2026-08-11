# XXII. The Compiler CLI — Complete Flag Reference

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│              RED COMPILER CLI — COMPLETE REFERENCE                   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  BASIC USAGE:                                                        │
│    red <script.red>               ; Run in interpreter               │
│    red -c <script.red>            ; Compile to native binary         │
│    red -r <script.red>            ; Compile + run                    │
│                                                                      │
│  COMPILATION FLAGS:                                                  │
│    -c                   ; Compile to native binary                   │
│    -d                   ; Enable development mode (libRedRT)         │
│    -e                   ; Export symbols (for library creation)      │
│    -o <file>            ; Specify output filename                    │
│    -r                   ; Compile and immediately run                │
│    -s                   ; Compile to Red/System source only          │
│                                                                      │
│  CROSS-COMPILATION:                                                  │
│    -t MSDOS              ; 16-bit MS-DOS target                      │
│    -t Windows            ; Windows PE 32-bit                         │
│    -t Linux              ; Linux ELF 32-bit                          │
│    -t Linux-ARM          ; Linux ARM ELF                             │
│    -t Linux-AArch64      ; Linux ARM64 ELF                           │
│    -t RPi                ; Raspberry Pi (Linux ARM)                  │
│    -t Darwin             ; macOS 32-bit Mach-O                       │
│    -t macOS              ; macOS 64-bit (via 32-bit layer)           │
│    -t Android            ; Android ARM                               │
│    -t Android-x86        ; Android x86                               │
│    -t FreeBSD            ; FreeBSD ELF                               │
│                                                                      │
│  VIEW ENGINE SELECTION:                                              │
│    --view native         ; Platform-native GUI (Win32/Cocoa/GTK)     │
│    --view terminal       ; Terminal/console UI                       │
│    --view GTK            ; Force GTK backend                         │
│    --view test           ; Headless test mode                        │
│    --no-view             ; Exclude VIEW entirely                     │
│                                                                      │
│  DEBUG AND VERBOSITY:                                                │
│    -v 1                  ; Red-level warning output                  │
│    -v 2                  ; Red-level info output                     │
│    -v 3                  ; Red-level debug output                    │
│    -v 4                  ; Red/System code generation                │
│    -v 7                  ; Emitter output (machine code)             │
│    -v 11                 ; Maximum: all internal passes              │
│    --show-func-map       ; Output address/name map (debugging)       │
│    --red-only            ; Stop after Red-level compilation          │
│                                                                      │
│  BINARY OPTIONS:                                                     │
│    --no-compress         ; Disable CRUSH compression on Redbin data  │
│    --no-runtime          ; Omit runtime (Red/System only)            │
│    -u, --update-libRedRT ; Rebuild libRedRT before compilation       │
│                                                                      │
│  LIBRARY BUILDING:                                                   │
│    red --build libRed              ; Build libRed (cdecl)            │
│    red --build libRed [stdcall]    ; Build libRed (stdcall/Windows)  │
│                                                                      │
│  CONFIG BLOCK:                                                       │
│    red --config [                                                    │
│        target: 'Windows                                              │
│        output: %myapp.exe                                            │
│        debug: yes                                                    │
│    ] [myapp.red]                                                       │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```