# XVIII. LibRed — The Embedding API

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│                   LibRed ARCHITECTURE                                │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  BUILD VARIANTS:                                                     │
│    red --build libRed          → cdecl ABI  (Linux/macOS)           │
│    red --build libRed [stdcall]→ stdcall ABI (Windows/COM)          │
│                                                                      │
│  OUTPUT:                                                             │
│    libRed.dll   (Windows)                                            │
│    libRed.so    (Linux)                                              │
│    libRed.dylib (macOS)                                              │
│    + libRed/libRed.h           C header                             │
│    + libRed/libRed.lib         Import library (Windows)             │
│                                                                      │
│  MEMORY MODEL — Short-lived references:                              │
│  ┌──────────────────────────────────────────────────────┐           │
│  │  API functions return RedValue references            │           │
│  │  These are valid for ~50 API calls only              │           │
│  │  After that, the internal reference manager          │           │
│  │  may reuse the slot                                  │           │
│  │                                                      │           │
│  │  SAFE pattern:                                       │           │
│  │    long sym = redSymbol("myword");                   │           │
│  │    redSet(sym, redInteger(42));   ← use immediately  │           │
│  │                                                      │           │
│  │  UNSAFE pattern:                                     │           │
│  │    long ref = redInteger(42);                        │           │
│  │    for(i=0; i<100; i++) {                            │           │
│  │        redAppend(blk, ref);  ← ref may be stale!    │           │
│  │    }                                                 │           │
│  └──────────────────────────────────────────────────────┘           │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```