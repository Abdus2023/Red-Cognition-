# XVII. The Reactive Programming Engine — Source Architecture

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│         RED REACTIVE SYSTEM — INTERNAL ARCHITECTURE                  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  RELATIONS TABLE (global flat block):                                │
│  Format: [reactor field reaction target  reactor field ...]          │
│          [obj1    x     [block]  field1   obj2    y    ...]          │
│                                                                      │
│  ┌───────────────────────────────────────────────────────────┐      │
│  │  REACTION TYPES                                            │      │
│  │                                                            │      │
│  │  STATIC REACTION:                                          │      │
│  │    react [face/color: obj/value]                          │      │
│  │    • Sources detected at CREATE time by Parse scan        │      │
│  │    • Faster: no re-scanning on each trigger               │      │
│  │    • Sources must be object paths (obj/field)             │      │
│  │                                                            │      │
│  │  DYNAMIC REACTION:                                         │      │
│  │    react/later [face/color: obj/value]                    │      │
│  │    • Sources detected at EXECUTION time                   │      │
│  │    • More flexible: sources can be computed               │      │
│  │    • /later = don't execute immediately on creation       │      │
│  └───────────────────────────────────────────────────────────┘      │
│                                                                      │
│  EXECUTION FLOW:                                                     │
│                                                                      │
│  Object field SET                                                    │
│       │                                                              │
│       ▼                                                              │
│  ON-CHANGE* event fires     ← intercepted by object system          │
│       │                                                              │
│       ▼                                                              │
│  lookup relations table     ← find [obj field] in table             │
│       │                                                              │
│       ▼                                                              │
│  for each matching reaction:                                         │
│    → eval reaction block    ← executes in reactor's context         │
│    → update target field    ← triggers further ON-CHANGE events     │
│    → propagate downstream   ← follows the dependency graph          │
│                                                                      │
│  ANTI-CYCLE PROTECTION:                                              │
│    • Execution depth counter                                         │
│    • Same-reaction re-entry guard                                    │
│    • Prevents infinite propagation loops                             │
│                                                                      │
│  DEEP PATH SUPPORT (0.6.6):                                          │
│  ┌──────────────────────────────────────────────────────┐           │
│  │  Compound scalar types now emit ON-CHANGE events     │           │
│  │  when components change via path access:             │           │
│  │                                                      │           │
│  │  pos: make object! [loc: 10x20]                      │           │
│  │  react [target/offset: pos/loc]                      │           │
│  │  pos/loc/x: 50    ; ← triggers reaction              │           │
│  └──────────────────────────────────────────────────────┘           │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```