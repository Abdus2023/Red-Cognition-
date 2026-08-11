# XLVI. The View Event System — Complete Architecture

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│              RED VIEW EVENT SYSTEM — COMPLETE ARCHITECTURE           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  EVENT OBJECT SCHEMA:                                                │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  event! object                                              │    │
│  │    type:    word!    ; event type identifier                │    │
│  │    face:    face!    ; face that received the event         │    │
│  │    window:  face!    ; top-level window face               │    │
│  │    offset:  pair!    ; mouse position (relative to face)   │    │
│  │    key:     char!    ; key pressed (for key events)        │    │
│  │    flags:   block!   ; modifier keys [shift ctrl alt]      │    │
│  │    picked:  integer! ; scroll delta / list selection       │    │
│  │    data:    any-type!; event-specific additional data      │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  COMPLETE EVENT TYPE TAXONOMY:                                       │
│  ┌─────────────────────┬──────────────────────────────────────┐     │
│  │  Mouse Events       │  click dbl-click alt-click           │     │
│  │                     │  over (enter/leave) down up          │     │
│  │                     │  wheel mid-down mid-up               │     │
│  ├─────────────────────┼──────────────────────────────────────┤     │
│  │  Keyboard Events    │  key key-down key-up                 │     │
│  ├─────────────────────┼──────────────────────────────────────┤     │
│  │  Focus Events       │  focus unfocus                       │     │
│  ├─────────────────────┼──────────────────────────────────────┤     │
│  │  Selection Events   │  select  (list/combobox)             │     │
│  ├─────────────────────┼──────────────────────────────────────┤     │
│  │  Change Events      │  change  (field/area content)        │     │
│  ├─────────────────────┼──────────────────────────────────────┤     │
│  │  Window Events      │  move resize close  (window ops)     │     │
│  ├─────────────────────┼──────────────────────────────────────┤     │
│  │  Timer Events       │  time  (requires rate: in view spec) │     │
│  ├─────────────────────┼──────────────────────────────────────┤     │
│  │  Drag Events        │  drop  drag-start drag-over drag-end │     │
│  ├─────────────────────┼──────────────────────────────────────┤     │
│  │  Menu Events        │  menu  (system menu selection)       │     │
│  └─────────────────────┴──────────────────────────────────────┘     │
│                                                                      │
│  EVENT DISPATCH PIPELINE:                                            │
│                                                                      │
│  OS generates native event                                           │
│       │                                                              │
│       ▼                                                              │
│  Platform backend translates to Red event!                           │
│       │                                                              │
│       ▼                                                              │
│  system/view/event-port receives event                               │
│       │                                                              │
│       ▼                                                              │
│  Global event handlers checked (system/view/handlers)               │
│       │                                                              │
│       ▼                                                              │
│  Face actors checked (face/actors/on-<event>)                        │
│       │                                                              │
│       ▼                                                              │
│  Inline event handler in VID spec                                    │
│       │                                                              │
│       ▼                                                              │
│  Reactive graph updated if face properties changed                   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```