# XXI. Redbin — The Binary Serialisation Format

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│              REDBIN FORMAT — BINARY SERIALISATION                    │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  PURPOSE:                                                            │
│    Fast load/save of Red values                                      │
│    Compiled code storage (inside encapped binaries)                 │
│    Cross-process value transmission                                  │
│    Efficient object/block serialisation                              │
│                                                                      │
│  FORMAT STRUCTURE:                                                   │
│  ┌──────────────────────────────────────────────────────┐           │
│  │  Header:                                             │           │
│  │    magic:    4 bytes  "RBIN"                         │           │
│  │    version:  4 bytes  format version                 │           │
│  │    length:   4 bytes  number of values               │           │
│  │                                                      │           │
│  │  Symbol Table:                                       │           │
│  │    count:    integer                                 │           │
│  │    [sym-len: byte  sym-data: UTF-8 bytes]  *count    │           │
│  │                                                      │           │
│  │  Value Array:                                        │           │
│  │    [type: byte  flags: byte  payload: N bytes]*      │           │
│  │                                                      │           │
│  │  Compressed form (default):                          │           │
│  │    Uses CRUSH compression algorithm                  │           │
│  │    Disable with: --no-compress flag                  │           │
│  └──────────────────────────────────────────────────────┘           │
│                                                                      │
│  API:                                                                │
│    save/as %data.rbin 'redbin my-block    ; serialize to file       │
│    data: load %data.rbin                  ; deserialize             │
│    binary-data: to-binary save 'redbin my-block  ; to binary!       │
│                                                                      │
│  COGNITIVE EXTENSION (proposed):                                     │
│    save/as %memory.cogbin 'cogbin agent-memory   ; cognitive state  │
│    ; Includes: belief confidence, timestamps, provenance chains      │
│    ; Enables cross-session memory persistence                        │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```