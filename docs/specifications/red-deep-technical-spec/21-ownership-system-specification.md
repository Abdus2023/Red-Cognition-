# XXX. The Ownership System — Deep Technical Specification

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│          OBJECT OWNERSHIP SYSTEM — COMPLETE ARCHITECTURE             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  OWNERSHIP ESTABLISHMENT:                                            │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  obj: make object! [                                        │    │
│  │      data: [1 2 3]          ; obj OWNS data series          │    │
│  │      on-deep-change*: func [owner word target action        │    │
│  │                              new index part][               │    │
│  │          ; triggered on ANY change to data or nested series │    │
│  │      ]                                                      │    │
│  │  ]                                                          │    │
│  │                                                             │    │
│  │  Ownership propagation:                                     │    │
│  │    obj/data      → obj owns data                           │    │
│  │    obj/data/sub  → obj owns nested sub-series              │    │
│  │    any level deep                                           │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  on-deep-change* ARGUMENT MAP:                                       │
│  ┌──────────────┬─────────────────────────────────────────────┐     │
│  │  owner       │  The object that owns the modified series   │     │
│  │  word        │  Name of the field in owner that was changed│     │
│  │  target      │  The actual series that was modified        │     │
│  │  action      │  What action caused the change (see list)   │     │
│  │  new         │  New value (for poke/insert actions)        │     │
│  │  index       │  Position of change (-1 = multiple/all)     │     │
│  │  part        │  Number of elements changed                 │     │
│  └──────────────┴─────────────────────────────────────────────┘     │
│                                                                      │
│  ACTION EVENT PAIRS:                                                 │
│  ┌──────────────────┬──────────────────────────────────────────┐    │
│  │  Single-event    │  random insert poke reverse sort         │    │
│  │                  │  swap trim clear                         │    │
│  │  Double-event    │  remove  → removed                       │    │
│  │  (before+after)  │  take    → taken                         │    │
│  │                  │  clear   → cleared                       │    │
│  └──────────────────┴──────────────────────────────────────────┘    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```