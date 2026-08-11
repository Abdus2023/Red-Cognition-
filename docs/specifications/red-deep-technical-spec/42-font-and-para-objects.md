# XLVII. The `font!` and `para!` Objects — Complete Specification

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│           FONT! AND PARA! OBJECTS — COMPLETE SPECIFICATION           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  FONT! SCHEMA:                                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  font! object                                               │    │
│  │    name:    string! | none  ; font family name              │    │
│  │    style:   word! | block! | none                           │    │
│  │             ; bold italic underline strike                  │    │
│  │    size:    integer! | none  ; points                       │    │
│  │    color:   tuple! | none    ; RGBA or RGB                  │    │
│  │    angle:   integer! | none  ; rotation in tenths of degree │    │
│  │    bold:    logic!            ; shorthand for style 'bold   │    │
│  │    italic:  logic!            ; shorthand for style 'italic │    │
│  │    underline: logic!          ; shorthand                   │    │
│  │    shadow:  pair! | none      ; drop shadow offset          │    │
│  │    state:   block!            ; internal OS handle storage  │    │
│  │    parent:  face!  | none     ; owning face                 │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  PARA! SCHEMA:                                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  para! object                                               │    │
│  │    origin:  pair! | none   ; text origin padding (x y)     │    │
│  │    padding: pair! | none   ; outer padding (x y)           │    │
│  │    scroll:  pair! | none   ; scroll position for text-list │    │
│  │    align:   word! | none   ; left right center             │    │
│  │    v-align: word! | none   ; top middle bottom             │    │
│  │    wrap?:   logic!          ; word-wrap long text          │    │
│  │    parent:  face! | none    ; owning face                  │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  GC INTEGRATION:                                                     │
│  font! and para! objects hold OS-level resources (HFONT on Windows, │
│  NSFont on macOS, PangoFontDescription on Linux). These are tracked  │
│  by the GC and released when the font/para object becomes            │
│  unreachable. The GC has explicit knowledge of face! and font!       │
│  types during the mark phase.                                        │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```