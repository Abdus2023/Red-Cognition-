# XLV. The Red Console — REPL Architecture

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│              RED CONSOLE — REPL ARCHITECTURE                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  COMPONENTS:                                                         │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  Input Engine                                               │    │
│  │    Multi-line input detection (unmatched brackets)         │    │
│  │    History navigation (↑↓ arrow keys)                      │    │
│  │    Persistent history file (~/.red/history.r)               │    │
│  │    Copy/paste support                                       │    │
│  │                                                             │    │
│  │  Syntax Highlighter                                         │    │
│  │    Real-time token colouring as user types                  │    │
│  │    Colour map:                                              │    │
│  │      set-word!  → blue                                      │    │
│  │      word!      → black                                     │    │
│  │      string!    → green                                     │    │
│  │      integer!   → red                                       │    │
│  │      float!     → red                                       │    │
│  │      comment    → grey                                      │    │
│  │      native!    → dark blue                                 │    │
│  │      bracket    → purple (matched highlighting)             │    │
│  │                                                             │    │
│  │  Auto-Completion                                            │    │
│  │    Tab → complete current word from global context         │    │
│  │    Double-tab → show all completions                        │    │
│  │    Path completion → obj/ shows available fields            │    │
│  │                                                             │    │
│  │  Output Renderer                                            │    │
│  │    mold for value display                                   │    │
│  │    Truncation for large series                              │    │
│  │    Colour-coded output by type                              │    │
│  │    Error display with near/where context                   │    │
│  │                                                             │    │
│  │  Session Management                                         │    │
│  │    Persistent global context across expressions             │    │
│  │    do <file> to load scripts                                │    │
│  │    clear-history to reset command history                   │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  CONSOLE LIFECYCLE:                                                  │
│                                                                      │
│  startup                                                             │
│    │                                                                 │
│    ▼                                                                 │
│  load ~/.red/user.r  ← user initialisation                          │
│    │                                                                 │
│    ▼                                                                 │
│  ┌─── READ ────────────────────────────────────────────────────┐    │
│  │  render prompt (green >>>)                                  │    │
│  │  accept user input                                          │    │
│  │  detect multi-line (unbalanced brackets)                   │    │
│  │  wait for complete expression                               │    │
│  └──────────────┬──────────────────────────────────────────────┘    │
│                 │                                                    │
│  ┌─── EVAL ────▼───────────────────────────────────────────────┐    │
│  │  try [do/next input position]                               │    │
│  │  catch errors cleanly                                       │    │
│  └──────────────┬──────────────────────────────────────────────┘    │
│                 │                                                    │
│  ┌─── PRINT ───▼───────────────────────────────────────────────┐    │
│  │  unless unset? result [print mold/limit result 2000]        │    │
│  │  display errors with type/id/near                           │    │
│  └──────────────┬──────────────────────────────────────────────┘    │
│                 │                                                    │
│  ┌─── LOOP ────▼───────────────────────────────────────────────┐    │
│  │  append history input                                       │    │
│  │  save history to file                                       │    │
│  │  go back to READ                                            │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```