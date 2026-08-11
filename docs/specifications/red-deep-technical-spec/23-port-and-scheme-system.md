# XXXI. The Port! System and Scheme Architecture

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│              PORT! SYSTEM — ARCHITECTURE AND SCHEME MODEL            │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  CONCEPT:                                                            │
│  A port! is a streaming I/O abstraction. Every I/O operation        │
│  in Red routes through the port system. Schemes define how          │
│  URLs map to I/O behaviours. A new scheme = a new protocol.         │
│                                                                      │
│  PORT! STRUCTURE:                                                    │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  port! object                                              │     │
│  │    scheme:    word!      ; which scheme handles this port  │     │
│  │    actor:     object!    ; scheme actor (handler object)   │     │
│  │    awake:     function!  ; async event callback            │     │
│  │    state:     any-type!  ; scheme-specific state           │     │
│  │    data:      any-type!  ; port data buffer                │     │
│  │    locals:    object!    ; scheme local variables          │     │
│  │    spec:      object!    ; port spec (url, host, port, ..) │     │
│  │    extra:     any-type!  ; user-defined data               │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
│  SCHEME REGISTRY (system/schemes):                                   │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  file://    → local filesystem access                      │     │
│  │  http://    → HTTP/1.1 client                              │     │
│  │  https://   → HTTPS (TLS)                                  │     │
│  │  tcp://     → raw TCP socket                               │     │
│  │  udp://     → raw UDP socket                               │     │
│  │  dns://     → DNS resolution                               │     │
│  │  gpio://    → Raspberry Pi GPIO pins                       │     │
│  │  event://   → OS event loop port                           │     │
│  │  clipboard://→ system clipboard                            │     │
│  │  [custom]   → user-defined schemes                         │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
│  SCHEME ACTOR PROTOCOL:                                              │
│  Every scheme implements a subset of these actor functions:          │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  open    [port]         ; establish connection             │     │
│  │  open?   [port]         ; test if open                     │     │
│  │  close   [port]         ; close connection                 │     │
│  │  read    [port]         ; read data                        │     │
│  │  write   [port data]    ; write data                       │     │
│  │  query   [port]         ; get metadata                     │     │
│  │  update  [port]         ; flush/sync                       │     │
│  │  rename  [port to]      ; rename resource                  │     │
│  │  delete  [port]         ; remove resource                  │     │
│  │  create  [port]         ; create new resource              │     │
│  │  awake   [event]        ; async event dispatch             │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```