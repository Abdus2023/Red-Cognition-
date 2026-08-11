# II. The Complete Toolchain — Diagram

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│                     RED COMPILER TOOLCHAIN                           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   Source (.red / .reds)                                              │
│          │                                                           │
│          ▼                                                           │
│   ┌─────────────────┐                                                │
│   │  Preprocessor   │  ← #include, #if, #define, macro expansion    │
│   │  (Loader)       │                                                │
│   └────────┬────────┘                                                │
│            │                                                         │
│            ▼                                                         │
│   ┌─────────────────┐                                                │
│   │  Lexer / Scanner│  ← Tokenises source into Red values           │
│   │                 │    (homoiconic: code = data)                   │
│   └────────┬────────┘                                                │
│            │                                                         │
│            ▼                                                         │
│   ┌─────────────────┐                                                │
│   │  Parser /       │  ← Builds block tree (no separate AST:        │
│   │  Loader         │    Red blocks ARE the parse tree)             │
│   └────────┬────────┘                                                │
│            │                                                         │
│    ┌───────┴──────────┐                                              │
│    ▼                  ▼                                              │
│  Interpret         Compile                                           │
│  (Dynamic)         (Static)                                          │
│    │                  │                                              │
│    │          ┌───────▼──────────────┐                              │
│    │          │  Red/System Compiler │                              │
│    │          │  (comp-dialect)      │                              │
│    │          └───────┬──────────────┘                              │
│    │                  │                                              │
│    │          ┌───────▼──────────────┐                              │
│    │          │  Code Emitter        │  ← Direct machine code gen  │
│    │          │  (emitter.r)         │    (no IR currently)         │
│    │          └───────┬──────────────┘                              │
│    │                  │                                              │
│    │          ┌───────▼──────────────┐                              │
│    │          │  Linker              │  ← PE.r / ELF.r / Mach-O    │
│    │          └───────┬──────────────┘                              │
│    │                  │                                              │
│    └────────┬─────────┘                                              │
│             ▼                                                        │
│   ┌─────────────────┐                                                │
│   │  Encapper       │  ← Bundles runtime + code into ~1MB binary    │
│   └─────────────────┘                                                │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```