# Red Programming Language — Deep Technical Specification (Part III)

**Source Message:** Ninth user message — Sections XXVII through XXXIX + Summary

**Stable ID:** RED-SPEC-PART-III-001

## XXVII. The New Lexer — Architecture and Instrumentation API

A programming language lexer is the part in charge of converting textual code representation into a structured memory representation. In Red, it is accomplished by the `transcode` native.

Until now, Red was relying on a lexer entirely written using the Parse dialect. Though, the parsing rules were constructed to be easily maintained and not for performance. Rewriting those rules to speed them up could have been possible, but rewriting the lexer entirely in Red/System would give the ultimate performance.

It might not matter for most user scripts, but given that Red is also a data format, we need a solution for fast (near-instant) loading of huge quantities of Red values stored in files or transferred through the network. New scanning features allow identifying values and their datatypes without loading them. Instrumentation allows customisation of the lexer's behaviour at will using an event-oriented API.

```
┌──────────────────────────────────────────────────────────────────────┐
│              RED LEXER v2 — INTERNAL ARCHITECTURE                    │
│              (Rewritten in Red/System for maximum performance)       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  INPUT: UTF-8 encoded string or binary buffer                        │
│                                                                      │
│  SCANNING PHASES:                                                    │
│  ┌───────────────────────────────────────────────────────────┐      │
│  │  Phase 1 — CHARACTER CLASSIFICATION                        │      │
│  │    Lookup table: byte → character class                   │      │
│  │    Classes: DIGIT ALPHA SPECIAL SPACE NEWLINE             │      │
│  │             STRING-START BINARY-START BLOCK-START etc.   │      │
│  └────────────────────────┬──────────────────────────────────┘      │
│                           │                                          │
│  ┌────────────────────────▼──────────────────────────────────┐      │
│  │  Phase 2 — TOKEN RECOGNITION (per-type scanners)           │      │
│  │                                                            │      │
│  │  scan-integer    : [+-]? digit+                            │      │
│  │  scan-float      : integer . digit* [e integer]?           │      │
│  │  scan-word       : alpha (alpha|digit|special-word-char)*  │      │
│  │  scan-string     : {"} chars {"}  OR {^{} chars {^}}      │      │
│  │  scan-binary     : #{hex-pairs}  2#{bits}  64#{b64}       │      │
│  │  scan-file       : % path-chars                            │      │
│  │  scan-url        : word :// rest                           │      │
│  │  scan-date       : DD-MMM-YYYY | YYYY-MM-DD variants       │      │
│  │  scan-time       : HH:MM:SS[.mmm][AM|PM]                  │      │
│  │  scan-pair       : integer x integer                       │      │
│  │  scan-tuple      : integer . integer . integer [...]       │      │
│  │  scan-issue      : # non-space+                            │      │
│  │  scan-char       : #" char "                               │      │
│  │  scan-email      : word @ domain                           │      │
│  │  scan-money      : [$|currency-code] digits [. digits]     │      │
│  │  scan-ref        : @ word                                  │      │
│  └────────────────────────┬──────────────────────────────────┘      │
│                           │                                          │
│  ┌────────────────────────▼──────────────────────────────────┐      │
│  │  Phase 3 — VALUE CONSTRUCTION                              │      │
│  │    Token string → typed Red value in memory               │      │
│  │    Word interning: symbol table lookup/insert             │      │
│  │    Buffer allocation via node system                       │      │
│  └────────────────────────┬──────────────────────────────────┘      │
│                           │                                          │
│  ┌────────────────────────▼──────────────────────────────────┐      │
│  │  INSTRUMENTATION API (Event-Oriented)                      │      │
│  │                                                            │      │
│  │  system/lexer/pre-load    : hook before lexing starts      │      │
│  │  system/lexer/on-token    : hook per token recognised      │      │
│  │  system/lexer/on-error    : hook on lexer error           │      │
│  │                                                            │      │
│  │  transcode/trace src [callback]   ; per-token events       │      │
│  │  scan src type                    ; scan without loading   │      │
│  │  transcode/next src               ; incremental lexing     │      │
│  └────────────────────────────────────────────────────────────┘      │
│                                                                      │
│  SUBROUTINES — intra-function factorisation (new in 0.6.x):         │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  Defined as separate blocks inside function bodies         │     │
│  │  Called like functions but with zero argument passing      │     │
│  │  One stack slot for return address only                    │     │
│  │  Analogous to GOSUB in BASIC                               │     │
│  │                                                            │     │
│  │  parse-digit: [                                            │     │
│  │      ; inlined routine — no function call overhead         │     │
│  │      ...                                                   │     │
│  │  ]                                                         │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Transcode API — Complete Reference

```red
; ══════════════════════════════════════════════════════════════════
; TRANSCODE — the new lexer's public API
; ══════════════════════════════════════════════════════════════════

; Basic: convert string to block of Red values
transcode "42 hello [1 2 3]"
; → [42 hello [1 2 3]]

; /next — incremental, one token at a time
transcode/next "hello world" 'result
; → result = hello, returns position after token

; /only — return first value only
transcode/only "[1 2 3] rest"
; → [1 2 3]

; /trace — event-driven instrumentation
transcode/trace "42 + hello" func [
    event   [word!]     ; opened closed decoded scanned error
    input   [string! binary!]
    type    [datatype! word!]
    line    [integer!]
    token
][
    print rejoin [event ": " type " = " mold token]
]

; SCAN — identify type without loading value
scan "42"          ; → integer!
scan "hello"       ; → word!
scan "[1 2 3]"     ; → block!
scan "#(a: 1)"     ; → map!
scan "2026-07-29"  ; → date!

; ── Lexer pre-load hook — custom syntax preprocessing ──────────────
; Runs before lexing — can transform source text
system/lexer/pre-load: func [src type][
    ; Example: translate arrow syntax to Red words
    replace/all src "→" "to"
    replace/all src "←" "from"
]
```

## XXVIII. The `routine!` Datatype — Red/System FFI Bridge

A routine is a Red/System function defined in a Red program. The routine specification takes Red datatypes as arguments and return value, and the routine will automatically convert them to appropriate Red/System types when called.

In order to more easily interface Red and Red/System, a new function datatype has been added: `routine!`.

```
┌──────────────────────────────────────────────────────────────────────┐
│              ROUTINE! — THE RED/RED SYSTEM BRIDGE                    │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  PURPOSE: Embed compiled Red/System code inside Red programs         │
│  Use case: performance-critical sections, direct OS access,          │
│            hardware manipulation from high-level code                │
│                                                                      │
│  DECLARATION SYNTAX:                                                 │
│                                                                      │
│    routine-name: routine [                                           │
│        arg1  [red-type!]                                             │
│        arg2  [red-type!]                                             │
│        return: [red-type!]     ; optional                            │
│    ][                                                                │
│        ; Red/System code body                                        │
│        ; native types available: integer! float! logic! byte!        │
│        ; Red values auto-converted via type-map                      │
│    ]                                                                 │
│                                                                      │
│  TYPE CONVERSION TABLE (Red → Red/System):                          │
│  ┌────────────────────┬─────────────────────────────────────┐       │
│  │  Red type          │  Red/System type                    │       │
│  ├────────────────────┼─────────────────────────────────────┤       │
│  │  integer!          │  integer!   (32-bit signed)         │       │
│  │  float!            │  float!     (64-bit double)         │       │
│  │  float32!          │  float32!   (32-bit float)          │       │
│  │  char!             │  byte!      (8-bit unsigned)        │       │
│  │  logic!            │  logic!     (bool)                  │       │
│  │  string!           │  c-string!  (pointer to UTF-8)      │       │
│  │  block!            │  pointer! [red-value!]              │       │
│  │  any-type!         │  red-value! (generic value ptr)     │       │
│  └────────────────────┴─────────────────────────────────────┘       │
│                                                                      │
│  COMPILATION: Routines are compiled when the containing              │
│  Red source is compiled. The R/S body is compiled inline             │
│  and a trampoline wrapper handles type conversion.                   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Routine Examples — All Major Patterns

```red
Red [Title: "Routine! Examples"]

; ── Pattern 1: Pure computation — integer arithmetic ───────────────
fast-pow: routine [
    "Compute base^exp using Red/System (compiled native)"
    base [integer!]
    exp  [integer!]
    return: [integer!]
][
    result: 1
    loop exp [result: result * base]
    result
]

print fast-pow 2 10   ; → 1024  (compiled, not interpreted)

; ── Pattern 2: Byte-level string processing ──────────────────────
count-bytes: routine [
    "Count occurrences of byte in string using direct memory scan"
    str   [string!]
    byte  [char!]       ; char! maps to byte! in R/S
    return: [integer!]
    /local count ptr
][
    count: 0
    ptr: as c-string! str
    while [ptr/1 <> #"^(00)"] [    ; until null terminator
        if ptr/1 = byte [count: count + 1]
        ptr: ptr + 1
    ]
    count
]

print count-bytes "hello world" #"l"  ; → 3

; ── Pattern 3: OS system call ─────────────────────────────────────
#import [
    "libc.so.6" cdecl [
        c-getpid: "getpid" [return: [integer!]]
    ]
]

get-pid: routine [
    "Get current process ID via OS syscall"
    return: [integer!]
][
    c-getpid
]

print get-pid   ; → current PID

; ── Pattern 4: struct manipulation ───────────────────────────────
point3d!: alias struct! [
    x [float!]
    y [float!]
    z [float!]
]

dot-product: routine [
    "3D dot product — returns float"
    ax [float!]  ay [float!]  az [float!]
    bx [float!]  by [float!]  bz [float!]
    return: [float!]
][
    (ax * bx) + (ay * by) + (az * bz)
]

print dot-product 1.0 0.0 0.0  0.0 1.0 0.0  ; → 0.0

; ── Pattern 5: LibRed callback — C calls Red ─────────────────────
; From C side:
; redRoutine(redWord("add-from-c"),
;            "[a [integer!] b [integer!] return: [integer!]]",
;            (void*)&my_c_add);
```

## XXIX. Red/System Atomic Intrinsics — The Complete Specification

A simple low-level OS threads wrapper API has been added internally to the Red runtime. A set of atomic intrinsics were added to enable the implementation of lock-free and wait-free algorithms.

The atomic intrinsics overview: `system/atomic/fence` generates a read/write data memory barrier. `system/atomic/load` performs a thread-safe atomic read from a given memory location. `system/atomic/store` performs a thread-safe atomic write to a given memory location. `system/atomic/cas` performs a thread-safe atomic compare & swap to a given memory location. `system/atomic/<math-op>` performs thread-safe atomic math or bitwise operations on a given memory location, including add, sub, or, xor, and.

```
┌──────────────────────────────────────────────────────────────────────┐
│         RED/SYSTEM ATOMIC INTRINSICS — COMPLETE SPECIFICATION        │
│         (From static.red-lang.org/red-system-specs.html)             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  MEMORY BARRIER:                                                     │
│    system/atomic/fence                                               │
│    Generates a full read/write memory barrier.                       │
│    Ensures all prior memory operations complete before               │
│    any subsequent operations begin.                                  │
│    Required when coordinating between threads without                │
│    using the other atomic ops.                                       │
│                                                                      │
│  ATOMIC LOAD:                                                        │
│    system/atomic/load <ptr>                                          │
│    <ptr>    : pointer! [integer!]  ← address to read                │
│    return   : integer!                                               │
│    Performs a thread-safe atomic read.                               │
│    Guarantees the full value is read atomically (no torn reads).     │
│                                                                      │
│  ATOMIC STORE:                                                       │
│    system/atomic/store <ptr> <value>                                 │
│    <ptr>    : pointer! [integer!]  ← address to write               │
│    <value>  : integer!             ← value to store                 │
│    Performs a thread-safe atomic write.                              │
│                                                                      │
│  COMPARE AND SWAP (CAS):                                             │
│    system/atomic/cas <ptr> <old> <new>                               │
│    <ptr>    : pointer! [integer!]  ← address to update              │
│    <old>    : integer!             ← expected current value          │
│    <new>    : integer!             ← value to write if match         │
│    return   : logic!               ← true if swap succeeded          │
│                                                                      │
│    CAS Semantics:                                                    │
│      1. Read current value at <ptr>                                  │
│      2. Compare to <old>                                             │
│      3. If equal: write <new>, return true                           │
│      4. If not equal: abort, return false                            │
│    This is the foundation of all lock-free algorithms.               │
│                                                                      │
│  ATOMIC MATH AND BITWISE OPERATIONS:                                 │
│    system/atomic/add <ptr> <value>         ; fetch-and-add          │
│    system/atomic/sub <ptr> <value>         ; fetch-and-subtract      │
│    system/atomic/or  <ptr> <value>         ; fetch-and-or           │
│    system/atomic/xor <ptr> <value>         ; fetch-and-xor          │
│    system/atomic/and <ptr> <value>         ; fetch-and-and           │
│                                                                      │
│    Return: the NEW value (after operation)                           │
│    With /old refinement: return the OLD value (before operation)     │
│    system/atomic/add/old <ptr> <value>                               │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Lock-Free MPMC Queue — Implementation Pattern

```red
Red/System [Title: "Lock-Free MPMC Queue using Atomic CAS"]

; Queue node structure
node!: alias struct! [
    value [integer!]
    next  [pointer! [integer!]]   ; points to next node!
]

; Queue head and tail (shared between threads)
queue-head: declare pointer! [integer!]   ; consumer pointer
queue-tail: declare pointer! [integer!]   ; producer pointer

; ── Initialise empty queue ─────────────────────────────────────────
init-queue: func [/local sentinel][
    sentinel: as node! allocate size? node!
    sentinel/next: null
    queue-head: as pointer! [integer!] sentinel
    queue-tail: as pointer! [integer!] sentinel
]

; ── Enqueue (Producer) — CAS on tail ──────────────────────────────
enqueue: func [
    val     [integer!]
    return: [logic!]
    /local new-node tail next
][
    new-node: as node! allocate size? node!
    new-node/value: val
    new-node/next: null

    forever [
        tail: as node! system/atomic/load queue-tail
        next: as node! system/atomic/load
            as pointer! [integer!] tail + (offset? node! next)

        ; Tail still consistent?
        if tail = (as node! system/atomic/load queue-tail) [
            either null? next [
                ; Tail at last node — try to link new node
                if system/atomic/cas
                    as pointer! [integer!] tail + (offset? node! next)
                    as integer! null
                    as integer! new-node
                [
                    ; Successfully linked — advance tail (can fail, ok)
                    system/atomic/cas queue-tail
                        as integer! tail
                        as integer! new-node
                    return true
                ]
            ][
                ; Tail not pointing to last — advance it
                system/atomic/cas queue-tail
                    as integer! tail
                    as integer! next
            ]
        ]
    ]
    true
]

; ── Dequeue (Consumer) — CAS on head ──────────────────────────────
dequeue: func [
    result  [pointer! [integer!]]
    return: [logic!]
    /local head tail next
][
    forever [
        head: as node! system/atomic/load queue-head
        tail: as node! system/atomic/load queue-tail
        next: as node! system/atomic/load
            as pointer! [integer!] head + (offset? node! next)

        if head = (as node! system/atomic/load queue-head) [
            either head = tail [
                if null? next [return false]   ; queue empty
                ; Tail falling behind — advance it
                system/atomic/cas queue-tail
                    as integer! tail
                    as integer! next
            ][
                ; Read value before CAS (another thread may free node)
                result/value: (as node! next)/value
                ; Try to swing head to next
                if system/atomic/cas queue-head
                    as integer! head
                    as integer! next
                [
                    free as byte-ptr! head
                    return true
                ]
            ]
        ]
    ]
    false
]
```

## XXX. The Ownership System — Deep Technical Specification

Red's objects ownership system is an extension of object's event support. Now, an object can own series it references, even nested ones. When an owned series is changed, the owner object is notified and its `on-deep-change*` function will be called if available, allowing the object to react appropriately to any change.

Ownership is set automatically on object creation if `on-deep-change*` is defined; all referenced series (including nested ones) will then become owned by the object.

The prototype for `on-deep-change*` takes owner, word, target, action, new, index, and part as arguments, where part is the number of elements changed in the series. Action name can be any of: random, clear, cleared, poke, remove, removed, reverse, sort, insert, take, taken, swap, trim. For actions "destroying" values, two events are generated — one before the "destruction", one after. When modifications affect several non-contiguous or all elements, index will be set to -1.

```
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

### Ownership in Practice — Observable Data Model

```red
; ── Observable list — notifies on all mutations ─────────────────────
make-observable-list: func [
    "Create a list that fires callbacks on change"
    /local obs
][
    obs: make object! [
        items:      copy []
        listeners:  copy []

        on-deep-change*: func [
            owner word target action new index part
        ][
            ; Notify all registered listeners
            foreach cb listeners [
                cb owner word action new index part
            ]
        ]

        ; Public API
        add: func [item][append items item]
        remove-at: func [idx][remove at items idx]
        clear-all: does [clear items]

        on-change: func [callback [function!]][
            append listeners callback
        ]
    ]
    obs
]

; Usage
my-list: make-observable-list

; Register a listener
my-list/on-change func [owner word action new index part][
    print rejoin [
        "LIST CHANGED: action=" action
        " at index=" index
        " value=" mold new
    ]
]

my-list/add "apple"      ; → LIST CHANGED: action=insert at index=1
my-list/add "banana"     ; → LIST CHANGED: action=insert at index=2
my-list/remove-at 1      ; → LIST CHANGED: action=remove at index=1
;                            → LIST CHANGED: action=removed at index=1

; ── View-model binding using ownership ──────────────────────────────
view-model: make object! [
    name:   ""
    age:    0
    errors: copy []

    on-deep-change*: func [owner word target action new index part][
        ; Validate on change
        switch word [
            age [
                if any [new < 0  new > 150] [
                    append errors rejoin ["Invalid age: " new]
                ]
            ]
            name [
                if empty? new [
                    append errors "Name cannot be empty"
                ]
            ]
        ]
        ; Trigger UI refresh
        do-react view-model 'name
    ]
]
```

## XXXI. The Port! System and Scheme Architecture

Finished or almost finished features in branches include full IO ports with async support, including new `IPv6!` datatype.

Red will feature a complete networking layer in 0.7.0, including async IO support, through a nice high-level API (similar to Rebol's one).

Adds `gpio://` port with GPIO dialect for Raspberry Pi.

```
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

### Custom Scheme Implementation

```red
; ── Custom Scheme: in-memory key-value store ─────────────────────────
make-scheme [
    name:   'memstore
    title:  "In-Memory Key-Value Store"

    ; Shared store across all ports of this scheme
    store: make map! []

    actor: make object! [

        open: func [port [port!]][
            ; Initialise port state
            port/state: make object! [
                key: none
                value: none
            ]
            port
        ]

        read: func [port [port!]][
            ; Return value for current key
            key: port/spec/path
            select port/scheme/store key
        ]

        write: func [port [port!] data [any-type!]][
            ; Store value at key
            key: port/spec/path
            put port/scheme/store key data
            data
        ]

        query: func [port [port!]][
            ; Return all keys
            keys-of port/scheme/store
        ]

        delete: func [port [port!]][
            key: port/spec/path
            remove/key port/scheme/store key
        ]

        close: func [port [port!]][
            port/state: none
            port
        ]
    ]
]

; Usage
p: open memstore://mykey
write p "Hello from port system!"
print read p                          ; → Hello from port system!
print query p                         ; → all stored keys
close p

; ── GPIO Dialect for Raspberry Pi ───────────────────────────────────
; gpio:// scheme provides a domain-specific dialect for pin control
gpio-port: open gpio://

; GPIO dialect block
do-gpio: func [pins [block!]][
    parse pins [
        any [
            'pin set n integer! 'output (
                write gpio-port reduce ['pin n 'mode 'output]
            )
            | 'pin set n integer! 'high (
                write gpio-port reduce ['pin n 'state 'high]
            )
            | 'pin set n integer! 'low (
                write gpio-port reduce ['pin n 'state 'low]
            )
            | 'read 'pin set n integer! (
                read gpio-port
            )
            | 'wait set ms integer! 'ms (
                wait ms / 1000.0
            )
        ]
    ]
]

; Blink LED on pin 17
do-gpio [
    pin 17 output
    pin 17 high  wait 500 ms
    pin 17 low   wait 500 ms
]

close gpio-port
```

## XXXII. New Datatypes — Complete History Through 0.6.6

New datatypes added in recent versions: `money!`, `ref!`, `point2D!`, `point3D!`.

Hashtables are now used for fast lookups in contexts.

A custom dtoa library implementation was added to load and form float values correctly.

```
┌──────────────────────────────────────────────────────────────────────┐
│           COMPLETE NEW DATATYPES ADDED 0.5.0 → 0.6.6                │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  money!  — Currency-safe decimal arithmetic                          │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  $1.00   €2.50   £10.99   ¥1000                             │    │
│  │                                                              │    │
│  │  Literal syntax:  $1.00  USD$10.50  EUR€5.00               │    │
│  │  Arithmetic: $1.00 + $2.00 → $3.00 (exact decimal)         │    │
│  │  No floating-point rounding errors                          │    │
│  │  Currency code attached to value                            │    │
│  │                                                              │    │
│  │  print $1.00 + $0.10   ; → $1.10  (exact, not $1.0999...)  │    │
│  │  print as-money 1050   ; → $10.50 (from cents)             │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ref!  — Social/document reference identifier                        │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  @username   @organization   @tag                           │    │
│  │                                                              │    │
│  │  Literal syntax: @word  (@ prefix)                         │    │
│  │  Similar to word! but carries reference semantics           │    │
│  │  Useful for: user mentions, object references, IDs          │    │
│  │                                                              │    │
│  │  user: @alice                                               │    │
│  │  notify user "Message"                                      │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  point2D!  — 2D geometric point with float precision                 │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  1.5x2.7   100.0x200.0   0.0x0.0                           │    │
│  │                                                              │    │
│  │  vs pair! (100x200 — integer only):                         │    │
│  │  point2D! stores float x and float y components             │    │
│  │  Designed for graphics and geometry requiring sub-pixel     │    │
│  │  precision                                                  │    │
│  │                                                              │    │
│  │  p: 1.5x2.7                                                 │    │
│  │  p/x  → 1.5                                                 │    │
│  │  p/y  → 2.7                                                 │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  point3D!  — 3D geometric point with float precision                 │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  1.0x2.0x3.0   (x, y, z float components)                  │    │
│  │                                                              │    │
│  │  p: 1.0x2.0x3.0                                            │    │
│  │  p/x → 1.0   p/y → 2.0   p/z → 3.0                        │    │
│  │                                                              │    │
│  │  Used for: 3D graphics, physics, robotics coordinates       │    │
│  │  Directly feeds into Red/Cognition robotics dialect         │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  SPECIAL FLOAT VALUES (full IEEE-754 support, 0.6.5+):              │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │   0.0    → positive zero                                    │    │
│  │  -0.0    → negative zero (sign preserved)                   │    │
│  │  1.#INF  → positive infinity                                │    │
│  │ -1.#INF  → negative infinity                                │    │
│  │  1.#NaN  → Not-a-Number                                     │    │
│  │                                                              │    │
│  │  print 1.0 / 0.0    ; → 1.#INF                             │    │
│  │  print -1.0 / 0.0   ; → -1.#INF                            │    │
│  │  print 0.0 / 0.0    ; → 1.#NaN                             │    │
│  │  print (1.#NaN = 1.#NaN)  ; → false (IEEE semantics)       │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  NEW NATIVES (0.6.x additions):                                      │
│    TRANSCODE  : new high-performance lexer entry point               │
│    SCAN       : identify datatype without loading value              │
│    AS-MONEY   : construct money! from integer cents                  │
│    ENHEX      : URL-encode a string                                  │
│    TRACE      : enable execution tracing                             │
│    CLOCK      : precise timing measurements                          │
│    NO-REACT   : execute block without triggering reactions           │
│    DO-NO-SYNC : execute without reactive synchronisation             │
│    SINGLE?    : true if series has exactly one element               │
│    LAST?      : true if at last element of series                    │
│    DT         : delta-time measurement shorthand                     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## XXXIII. The Draw Dialect — Complete Technical Specification

```
┌──────────────────────────────────────────────────────────────────────┐
│              DRAW DIALECT — COMPLETE COMMAND REFERENCE               │
│              Vector 2D graphics for Red/View                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  INVOCATION:                                                         │
│    draw image! [draw-commands]     ; render to image!               │
│    view [base 400x300 draw [...]]  ; render to canvas face           │
│                                                                      │
│  CANVAS STATE:                                                       │
│    pen          color | off        ; stroke colour                   │
│    fill-pen     color | off        ; fill colour                     │
│    line-width   float!             ; stroke width (pixels)           │
│    line-join    miter|round|bevel  ; corner style                    │
│    line-cap     flat|square|round  ; end cap style                   │
│    anti-alias   on | off           ; enable anti-aliasing            │
│    font         font-object        ; text rendering font             │
│    shadow       pair! color [blur [spread]] ; drop shadow            │
│                                                                      │
│  PRIMITIVES:                                                         │
│    line    pair! pair! [pair! ...]     ; polyline                    │
│    box     pair! pair! [radius]        ; rect [with rounded corners] │
│    circle  pair! integer!              ; center radius               │
│    ellipse pair! pair!                 ; center size                 │
│    arc     pair! pair! integer! integer! [sweep] ; arc               │
│    curve   pair! pair! pair! [pair!]   ; bezier curve                │
│    spline  [pair! ...] [closed]        ; catmull-rom spline          │
│    polygon [pair! ...]                 ; filled polygon              │
│    triangle pair! pair! pair!          ; 3-point polygon             │
│                                                                      │
│  TEXT:                                                               │
│    text    pair! string!              ; render string at position    │
│    text    pair! pair! string!        ; render in bounding box       │
│                                                                      │
│  IMAGES:                                                             │
│    image   image!                     ; render at 0x0               │
│    image   image! pair!               ; render at position           │
│    image   image! pair! pair!         ; render with size             │
│    image   image! pair! pair! [key-color [border]] ; keyed          │
│                                                                      │
│  TRANSFORMS:                                                         │
│    translate pair!                    ; move coordinate origin       │
│    scale     float! float!            ; scale x and y               │
│    rotate    float! [pair!]           ; rotate [around center]       │
│    skew      float! [float!]          ; shear x [and y]             │
│    matrix    [6 floats]               ; 2D affine matrix             │
│    reset-matrix                       ; restore identity matrix      │
│    invert-matrix                      ; invert current matrix        │
│                                                                      │
│  GRADIENTS:                                                          │
│    fill-pen linear  pair! pair! [pad|repeat|reflect]                 │
│              [color float! ...]  ; gradient stops                    │
│    fill-pen radial  pair! integer! integer! [pad|repeat|reflect]     │
│              [color float! ...]                                      │
│    fill-pen diamond pair! pair! integer! [pad|repeat|reflect]        │
│              [color float! ...]                                      │
│                                                                      │
│  CLIPPING:                                                           │
│    clip pair! pair!               ; rectangular clip region          │
│    clip [draw-commands]           ; clip to path                     │
│                                                                      │
│  STATE SAVE/RESTORE:                                                 │
│    push [draw-commands]           ; save state, restore after block  │
│                                                                      │
│  POSITION MARKS (Red 0.6.0+):                                        │
│    set-mark word!                 ; save current position to word    │
│    ; word then contains pair! of current canvas position            │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Complete Draw Program — All Features Demonstrated

```red
Red [Title: "Draw Dialect Complete Demonstration"]

; ── Create target image ──────────────────────────────────────────────
canvas: make image! 800x600

draw canvas [

    ; ── BACKGROUND ─────────────────────────────────────────────────
    fill-pen linear 0x0 800x0 pad [
        255.200.50 0.0    ; gold at left
        255.100.0  0.5    ; orange at centre
        200.50.255 1.0    ; purple at right
    ]
    pen off
    box 0x0 800x600

    ; ── COORDINATE TRANSFORM DEMONSTRATION ─────────────────────────
    push [
        translate 100x100
        rotate 45.0 200x200
        pen white  line-width 2  fill-pen 0.100.255.200
        box 0x0 200x200 10        ; rounded rect, 10px radius
    ]

    ; ── BEZIER CURVE ────────────────────────────────────────────────
    pen yellow  line-width 3  fill-pen off
    curve 50x400  150x300  250x500  350x350

    ; ── SPLINE ──────────────────────────────────────────────────────
    pen cyan  line-width 2
    spline [
        400x500  450x400  500x480
        550x380  600x460  650x350
        700x430  750x380
    ]

    ; ── SHADOW AND CIRCLE ───────────────────────────────────────────
    shadow 5x5 black 8    ; 8px blur
    fill-pen radial 600x150 0 80 pad [
        white    0.0
        255.50.50 0.5
        red      1.0
    ]
    pen off
    circle 600x150 80

    ; ── RESET SHADOW ────────────────────────────────────────────────
    shadow off

    ; ── TEXT RENDERING ──────────────────────────────────────────────
    push [
        font make font! [
            name: "Arial"  size: 24
            color: white   style: 'bold
        ]
        pen off  fill-pen white
        text 50x50 "Red Draw Dialect"
    ]

    ; ── CLIP DEMONSTRATION ──────────────────────────────────────────
    push [
        clip 300x200 550x400      ; circular clip region
        fill-pen 50.200.50
        circle 425x300 120
        pen white  line-width 1
        line 300x200 550x400
        line 300x400 550x200
    ]

    ; ── POLYGON ─────────────────────────────────────────────────────
    fill-pen 255.200.0.180     ; semi-transparent gold
    pen white  line-width 2
    polygon [
        400x100  430x190  520x190
        460x245  480x340  400x290
        320x340  340x245  280x190
        370x190
    ]

    ; ── POSITION MARKS ──────────────────────────────────────────────
    translate 650x450
    pen blue  fill-pen sky
    set-mark p1
    circle 0x0 40
    set-mark p2
    line 0x0 p1        ; line from current back to saved mark
]

; Display result
view [
    title "Draw Demo"
    image canvas
    button "Save" [save %draw-output.png canvas]
]
```

## XXXIV. Red/System FPU Control — Complete Technical Reference

The FPU control includes fields for Input Denormal, Inexact (Precision), Underflow, Overflow, Division by Zero, and Invalid Operation.

Setting the control-word on ARM can have side-effects, as the same register is used for status flags. Not yet fully implemented on all platforms.

```
┌──────────────────────────────────────────────────────────────────────┐
│         RED/SYSTEM FPU CONTROL — COMPLETE SPECIFICATION              │
│         (From static.red-lang.org/red-system-specs.html)             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  FPU EXCEPTION MASK BITS:                                            │
│  ┌──────┬───┬───┬───┬───┬───┬───┐                                   │
│  │  Bit │ID │ IX│ UF│ OF│ DZ│ IO│                                   │
│  ├──────┼───┼───┼───┼───┼───┼───┤                                   │
│  │  Name│ID │IX │UF │OF │DZ │IO │                                   │
│  ├──────┼───┼───┼───┼───┼───┼───┤                                   │
│  │Meaning│Inp│Pre│Und│Ove│Div│Inv│                                   │
│  │      │Den│cis│erf│erf│/0 │Op │                                   │
│  └──────┴───┴───┴───┴───┴───┴───┘                                   │
│                                                                      │
│  FPU CONTROL OPERATIONS:                                             │
│                                                                      │
│  system/fpu/update                                                   │
│    ; Apply all pending FPU option changes                            │
│    ; On ARM: changes are immediate, this is a no-op                  │
│    ; On IA-32: required to flush pending changes to hardware         │
│                                                                      │
│  system/fpu/init                                                     │
│    ; Initialise FPU to known state                                   │
│    ; Required on IA-32 before floating-point ops                     │
│    ; On ARM: no-op                                                   │
│                                                                      │
│  system/fpu/control-word                                             │
│    ; Get or set full FPU control register (integer!)                 │
│    ; WARNING: ARM side-effects (shared with status flags)           │
│                                                                      │
│  FPU EXCEPTION FLAGS:                                                │
│    system/fpu/exception/mask/precision:        logic!                │
│    system/fpu/exception/mask/underflow:        logic!                │
│    system/fpu/exception/mask/overflow:         logic!                │
│    system/fpu/exception/mask/zero-divide:      logic!                │
│    system/fpu/exception/mask/invalid-op:       logic!                │
│    system/fpu/exception/mask/denormal:         logic!                │
│                                                                      │
│  ROUNDING MODES:                                                     │
│    system/fpu/option/rounding                                        │
│      nearest   ; round to nearest even (default, IEEE-754)          │
│      down      ; round toward -∞                                     │
│      up        ; round toward +∞                                     │
│      truncate  ; round toward zero                                   │
│                                                                      │
│  PRECISION MODES (IA-32 only):                                       │
│    system/fpu/option/precision                                       │
│      single    ; 32-bit precision                                    │
│      double    ; 64-bit precision (default)                          │
│      extended  ; 80-bit extended precision                           │
│                                                                      │
│  IO PORT ACCESS (low-level hardware):                                │
│    system/io/read  <port-address>    ; read from HW I/O port        │
│    system/io/write <port-address> <value>  ; write to HW I/O port   │
│    The returned/written value type depends on pointer type used.     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### FPU Control in Red/System — Usage Patterns

```red
Red/System [Title: "FPU Control Examples"]

; ── Initialise FPU (required on IA-32 before float ops) ──────────────
system/fpu/init

; ── Trap division by zero ────────────────────────────────────────────
system/fpu/exception/mask/zero-divide: false    ; unmask = enable trap
system/fpu/update

; ── Trap invalid operations (like 0.0 / 0.0 = NaN) ──────────────────
system/fpu/exception/mask/invalid-op: false
system/fpu/update

; ── Set truncation rounding (for integer conversion) ─────────────────
system/fpu/option/rounding: 'truncate
system/fpu/update

x: 3.7
i: as integer! x     ; → 3 (truncated, not rounded)

; ── Restore default rounding ─────────────────────────────────────────
system/fpu/option/rounding: 'nearest
system/fpu/update

; ── Full precision mode (extended 80-bit on IA-32) ───────────────────
system/fpu/option/precision: 'extended
system/fpu/update

; ── Read/write hardware I/O port (requires ring 0 privileges) ────────
; p: declare pointer! [byte!]
; value: system/io/read p    ; read 8-bit hardware port
; system/io/write p 0xFF     ; write to hardware port
```

## XXXV. Red/System #INLINE Directive — Direct Machine Code Injection

A `#INLINE` directive allows inlining machine code directly into the compiled output.

This adds the `#inline` directive to Red/System for including assembled binary code.

```red
Red/System [Title: "#INLINE Machine Code Examples"]

; ── CPUID instruction — identify processor capabilities ──────────────
get-cpuid: func [
    leaf    [integer!]
    return: [integer!]   ; returns EAX result
    /local result
][
    result: 0

    ; Inline x86 CPUID instruction
    ; CPUID takes EAX=leaf, returns info in EAX,EBX,ECX,EDX
    #INLINE [
        ; mov eax, [leaf-address]
        8Bh 45h 08h              ; MOV EAX, [EBP+8]  ; load leaf arg
        0Fh A2h                  ; CPUID
        89h 45h FCh              ; MOV [EBP-4], EAX  ; store result
    ]
    result
]

; ── RDTSC — Read Time-Stamp Counter (high precision timing) ──────────
rdtsc: func [
    return: [integer!]    ; low 32 bits of TSC
][
    #INLINE [
        0Fh 31h              ; RDTSC — EDX:EAX = timestamp counter
        ; EAX returned automatically as return value
    ]
    0  ; placeholder — return handled by inline
]

; ── NOP sled (for alignment or timing) ───────────────────────────────
align-nop: func [][][
    #INLINE [
        90h 90h 90h 90h      ; 4 x NOP
    ]
]

; ── Privileged instruction example (SSE2 fence) ───────────────────────
memory-fence: func [][][
    #INLINE [
        0Fh AEh F8h          ; SFENCE — store fence
    ]
]
```

## XXXVI. The Red Standard Library — Complete Module Map

```
┌──────────────────────────────────────────────────────────────────────┐
│              RED STANDARD LIBRARY — COMPLETE MODULE MAP              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  CORE RUNTIME (always loaded):                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  actions.red         ; polymorphic action dispatch          │    │
│  │  boot.red            ; bootstrap, system object init        │    │
│  │  context.red         ; context/binding operations           │    │
│  │  control.red         ; if either while until loop foreach   │    │
│  │  error.red           ; error! type and handlers             │    │
│  │  format.red          ; form mold sprint printf              │    │
│  │  functions.red       ; higher-order: map-each collect etc.  │    │
│  │  math.red            ; sin cos tan sqrt log exp ...         │    │
│  │  mezz.red            ; miscellaneous high-level functions   │    │
│  │  natives.red         ; wrappers for C-level natives         │    │
│  │  object.red          ; object model, inheritance            │    │
│  │  paren.red           ; paren! evaluation rules              │    │
│  │  path.red            ; path! access and navigation          │    │
│  │  reactivity.red      ; ~250 LOC reactive framework          │    │
│  │  series.red          ; generic series operations            │    │
│  │  sort.red            ; sort algorithm (introsort)           │    │
│  │  string.red          ; string manipulation                  │    │
│  │  system.red          ; system object definition             │    │
│  │  unicode.red         ; UTF-8/16/32 support                  │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  OPTIONAL MODULES (loaded on demand):                                │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  view/view.red       ; VID dialect + View engine            │    │
│  │  view/draw.red       ; Draw 2D vector dialect               │    │
│  │  view/rich-text.red  ; Rich-text formatting dialect         │    │
│  │  codec/png.red       ; PNG image encode/decode              │    │
│  │  codec/jpeg.red      ; JPEG image encode/decode             │    │
│  │  codec/gif.red       ; GIF image decode                     │    │
│  │  codec/csv.red       ; CSV parse and format                 │    │
│  │  codec/json.red      ; JSON parse and format                │    │
│  │  codec/redbin.red    ; Redbin binary format                 │    │
│  │  network/http.red    ; HTTP client (scheme handler)         │    │
│  │  crypto/hash.red     ; MD5 SHA-1 SHA-256 SHA-512 CRC32      │    │
│  │  compress/gzip.red   ; gzip/zlib/deflate compress           │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  KEY STANDARD FUNCTIONS (selected reference):                        │
│  ┌────────────────┬───────────────────────────────────────────┐     │
│  │  Series        │  append insert remove find select pick     │     │
│  │                │  sort reverse copy skip head tail at       │     │
│  │                │  length? index? empty? single? last?       │     │
│  ├────────────────┼───────────────────────────────────────────┤     │
│  │  String        │  form mold trim split rejoin uppercase     │     │
│  │                │  lowercase trim replace to-string          │     │
│  ├────────────────┼───────────────────────────────────────────┤     │
│  │  Control       │  if either unless case switch             │     │
│  │                │  while until loop repeat foreach           │     │
│  │                │  break continue return exit                │     │
│  ├────────────────┼───────────────────────────────────────────┤     │
│  │  Meta          │  do load save compose reduce               │     │
│  │                │  bind unbind in context? get set           │     │
│  │                │  func function does has routine            │     │
│  │                │  body-of spec-of type-of reflect           │     │
│  ├────────────────┼───────────────────────────────────────────┤     │
│  │  Type check    │  integer? string? block? object? word?     │     │
│  │                │  function? number? series? any-type?       │     │
│  │                │  type? datatype?                           │     │
│  ├────────────────┼───────────────────────────────────────────┤     │
│  │  I/O           │  read write load save print prin           │     │
│  │                │  open close query update                   │     │
│  │                │  list-dir make-dir delete rename           │     │
│  ├────────────────┼───────────────────────────────────────────┤     │
│  │  Math          │  + - */ //* * mod abs max min             │     │
│  │                │  sin cos tan asin acos atan atan2          │     │
│  │                │  sqrt log exp round floor ceil             │     │
│  ├────────────────┼───────────────────────────────────────────┤     │
│  │  Crypto        │  checksum (md5/sha256/sha512/crc32)       │     │
│  ├────────────────┼───────────────────────────────────────────┤     │
│  │  Compress      │  compress uncompress                       │     │
│  │                │  (gzip zlib deflate algorithms)            │     │
│  └────────────────┴───────────────────────────────────────────┘     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## XXXVII. The Instrumented Interpreter — Debug and Trace API

Instrumentation is built-in for the interpreter, lexer, and parser.

Functions now support `[trace]` and `[no-trace]` function attributes.

```red
; ══════════════════════════════════════════════════════════════════
; RED INTERPRETER INSTRUMENTATION — COMPLETE API
; ══════════════════════════════════════════════════════════════════

; ── TRACE — step-by-step evaluation tracing ──────────────────────────
; Enable global tracing
trace on

; Execute with trace
x: 10 + 20    ; prints each evaluation step

trace off

; ── Function-level trace attributes ─────────────────────────────────
my-func: func [
    [trace]          ; this function always traces
    x [integer!]
][
    x * 2
]

no-trace-func: func [
    [no-trace]       ; suppress tracing even when global trace is on
    x [integer!]
][
    x * 3
]

; ── CLOCK — precise timing ────────────────────────────────────────────
; Measure execution time
dt [
    ; code to benchmark
    repeat i 100000 [sqrt to-float i]
]
; → prints elapsed time in milliseconds

; Shorthand: clock function
elapsed: clock [
    sort array: random/only make vector! [integer! 1000] 1000
]
print rejoin ["Sort took: " elapsed " ms"]

; ── Lexer trace via transcode/trace ──────────────────────────────────
transcode/trace "42 hello [1 2 3]" func [
    event   [word!]
    input   [string!]
    type    [datatype! word!]
    line    [integer!]
    token
][
    switch event [
        opened  [print ["OPEN:  " type]]
        closed  [print ["CLOSE: " type]]
        decoded [print ["TOKEN: " type " = " mold token]]
        scanned [print ["SCAN:  " type]]
        error   [print ["ERROR: " mold token " at line " line]]
    ]
]

; ── STATS — runtime statistics ────────────────────────────────────────
stats              ; → memory used (bytes)
stats/show         ; → detailed memory breakdown
;   series buffers:   N bytes
;   nodes:            N bytes
;   context cache:    N bytes
;   total:            N bytes

; ── System internal state access ────────────────────────────────────
system/state/near     ; last evaluation position (for error reporting)
system/state/trace?   ; is tracing active?
system/state/stack    ; call stack snapshot (for debugging)
```

## XXXVIII. Complete Anti-Virus Mitigation Architecture

One known way to reduce false flagging from anti-viruses is to use the `--no-compress` option when compiling Red binaries. That will prevent the internal Redbin data from being compressed using the CRUSH compressor, reducing that file section entropy.

```
┌──────────────────────────────────────────────────────────────────────┐
│        RED BINARY STRUCTURE — AV MITIGATION ARCHITECTURE             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  WHY AV FLAGS RED BINARIES:                                          │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  1. Encapped binary contains compressed Redbin section      │    │
│  │  2. CRUSH compression → high-entropy binary blob            │    │
│  │  3. High entropy = AV heuristic for encrypted malware       │    │
│  │  4. Self-contained ~1MB single file = suspicious to AV      │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  BINARY LAYOUT (Windows PE, typical):                                │
│  ┌──────────────────────────────────────────────────────────── ┐    │
│  │  .text section     : compiled Red/System code (low entropy) │    │
│  │  .data section     : global variables (low entropy)         │    │
│  │  .redbin section   : Redbin bytecode (high entropy if CRUSH)│    │
│  │  .import table     : imported DLL functions                 │    │
│  │  PE header         : standard Windows PE header             │    │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
│  MITIGATION STRATEGIES:                                              │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  1. --no-compress flag                                       │    │
│  │     Disables CRUSH on Redbin section                        │    │
│  │     Reduces entropy → fewer false positives                 │    │
│  │     Trade-off: larger binary size                           │    │
│  │                                                              │    │
│  │  2. Code signing (recommended for distribution)             │    │
│  │     Sign with valid certificate → AV trusts signature       │    │
│  │                                                              │    │
│  │  3. AV vendor whitelist submission                           │    │
│  │     Submit false-positive sample to vendor                  │    │
│  │     Most vendors respond within 24-72 hours                 │    │
│  │                                                              │    │
│  │  4. libRedRT development mode (-d flag)                      │    │
│  │     Split runtime into separate .dll                        │    │
│  │     Smaller main binary = lower suspicion score             │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## XXXIX. The Complete VID Dialect — Full Widget and Layout Reference

```red
; ══════════════════════════════════════════════════════════════════
; VID DIALECT — COMPLETE WIDGET AND LAYOUT REFERENCE
; ══════════════════════════════════════════════════════════════════

; ── LAYOUT KEYWORDS ─────────────────────────────────────────────────
view [

    ; PANEL GEOMETRY
    across              ; horizontal layout (default)
    below               ; vertical layout
    return              ; newline in layout
    pad  10             ; add spacing (integer! or pair!)

    ; WINDOW PROPERTIES
    title   "Window Title"
    size    800x600
    color   white
    rate    30          ; timer rate in Hz (triggers on-time event)
    offset  100x100     ; window position on screen

    ; ── WIDGETS ────────────────────────────────────────────────────

    ; TEXT DISPLAY
    text "Label text"
    text 200x30 "Fixed size label"
    text bold "Bold text"
    text font-size 18 "Large text"
    text font-color red "Coloured text"
    text wrap "Long text that will wrap within the widget bounds..."

    ; TEXT INPUT
    field                           ; single-line text input
    field 300x25 "placeholder"      ; with size and hint
    field password                  ; password (hidden chars)
    field 200 [print face/text]     ; with on-enter action

    area                            ; multi-line text editor
    area 400x200 "initial content"

    ; BUTTONS
    button "Click Me" [print "clicked"]
    button 120x35 "Wide Button" [action]
    toggle "Toggle" [print face/data]       ; on/off state in data
    check  "Checkbox" [print face/data]     ; boolean data
    radio  "Option 1" [print face/data]     ; radio group

    ; MEDIA
    image %logo.png
    image 200x150 %photo.jpg             ; scaled image

    ; SELECTION
    drop-list 200x25 data ["A" "B" "C"]  ; dropdown
    drop-down 200x25 data ["A" "B" "C"]  ; editable dropdown
    text-list 200x150 data ["item1" "item2" "item3"]

    ; NUMERIC INPUT
    slider 200x20                        ; horizontal 0.0-1.0
    slider 20x200                        ; vertical (tall = vertical)
    progress 200x20                      ; progress bar (0.0-1.0 data)
    spinner  ; integer spinner (up/down arrows)

    ; DATE/TIME
    calendar                             ; date picker
    date-field                           ; date input field

    ; DRAWING CANVAS
    base 400x300 draw [                  ; custom draw canvas
        pen red  circle 200x150 100
    ]

    ; CONTAINERS
    panel [                              ; grouped sub-layout
        text "Inside panel"
        button "Panel Button" []
    ]
    group-box "Group Title" [
        text "Inside group"
    ]
    tab-panel ["Tab 1" [...] "Tab 2" [...]]

    ; SCROLLABLE
    scroller 20x200                      ; standalone scrollbar

    ; ── COMMON WIDGET OPTIONS ──────────────────────────────────────
    ; All widgets accept:
    ;   <size>   pair!      ; explicit size
    ;   <offset> pair!      ; explicit position (breaks flow)
    ;   color    tuple!     ; background colour
    ;   font     object!    ; font! object
    ;   bold italic underline ; font style shortcuts
    ;   font-size integer!  ; font size
    ;   font-name string!   ; font family
    ;   font-color tuple!   ; text colour
    ;   visible  logic!     ; initially visible?
    ;   enable   logic!     ; initially enabled?
    ;   data     any        ; widget data
    ;   extra    any        ; user data (not used by View)

    ; ── EVENT HANDLERS ─────────────────────────────────────────────
    ; As options after widget spec:
    ;   on-click    [action]
    ;   on-dbl-click [action]
    ;   on-focus    [action]
    ;   on-unfocus  [action]
    ;   on-enter    [action]
    ;   on-key      [action]
    ;   on-resize   [action]
    ;   on-move     [action]
    ;   on-time     [action]  ; requires rate: in view spec
    ;   on-change   [action]  ; field/slider value changed
    ;   on-select   [action]  ; list selection changed
    ;   on-over     [action]  ; mouse hover (face/over = logic!)

    ; ── ACTORS OBJECT SHORTHAND ────────────────────────────────────
    ; Actors group all event handlers:
    ; actors make object! [
    ;     on-click: func [face event][]
    ;     on-key:   func [face event][]
    ; ]
]
```

## XL. Red/Cognition v0.3 — Extended With All Technical Grounding

This final section presents the most complete possible Red/Cognition prototype, incorporating all technical details confirmed throughout the specification: ownership system for reactive memory, port-based event injection, `routine!` for performance-critical cognitive operations, `transcode/trace` for intent parsing, and the new datatypes.

```red
Red [
    Title:   "Red/Cognition v0.3 — Full Technical Integration"
    Purpose: {
        Cognitive layer exploiting ALL of Red's subsystems:
        - Ownership system for reactive memory monitoring
        - Atomic operations for thread-safe state
        - routine! for compiled cognitive operations
        - port!/scheme for event injection
        - transcode/trace for intent parsing
        - point3D! for spatial cognitive models
        - money! for resource budget tracking
    }
    Version: 0.3.0
]

; ══════════════════════════════════════════════════════════════════
; SECTION 1: PERFORMANCE-CRITICAL COGNITIVE OPS VIA ROUTINE!
; ══════════════════════════════════════════════════════════════════

; Cosine similarity — hot path in semantic retrieval
cosine-similarity: routine [
    "Compute cosine similarity between two float vectors"
    v1  [block!]     ; vector as block of float!
    v2  [block!]     ; vector as block of float!
    len [integer!]   ; vector dimension
    return: [float!]
    /local
        dot  norm1 norm2
        i    a  b
][
    dot:   0.0
    norm1: 0.0
    norm2: 0.0
    i: 1
    loop len [
        a: as float! (as red-value! v1) + i  ; raw element access
        b: as float! (as red-value! v2) + i
        dot:   dot   + (a * b)
        norm1: norm1 + (a * a)
        norm2: norm2 + (b * b)
        i: i + 1
    ]
    either any [norm1 = 0.0  norm2 = 0.0][
        0.0
    ][
        dot / (sqrt norm1 * sqrt norm2)
    ]
]

; Fast string hash for semantic memory key generation
fast-hash: routine [
    "FNV-1a hash — fast key for semantic memory map"
    s   [string!]
    return: [integer!]
    /local h p
][
    h: 2166136261      ; FNV offset basis
    p: as c-string! s
    while [p/1 <> #"^(00)"] [
        h: h xor (as integer! p/1)
        h: h * 16777619  ; FNV prime
        p: p + 1
    ]
    h
]

; ══════════════════════════════════════════════════════════════════
; SECTION 2: REACTIVE MEMORY USING OWNERSHIP SYSTEM
; ══════════════════════════════════════════════════════════════════

; Memory store that automatically propagates changes to listeners
make-reactive-memory: func ["Create an ownership-based reactive memory"][
    mem: make object! [
        ; SEMANTIC MEMORY — owned series triggers on-deep-change
        semantic-store: copy []
        episodic-store: copy []
        working-store:  copy []

        ; Change listeners (by memory type)
        listeners: make map! [
            semantic  copy []
            episodic  copy []
            working   copy []
        ]

        ; OWNERSHIP EVENT HANDLER
        ; Fires on ANY mutation to owned series (append/remove/poke etc.)
        on-deep-change*: func [
            owner   [object!]
            word    [word!]      ; which field changed
            target  [series!]   ; the actual changed series
            action  [word!]     ; insert/remove/poke etc.
            new     [any-type!] ; new value
            index   [integer!]  ; position (-1 = multiple)
            part    [integer!]  ; number of elements
        ][
            ; Route change events to registered listeners
            memory-type: select make map! [
                semantic-store  'semantic
                episodic-store  'episodic
                working-store   'working
            ] word

            if memory-type [
                cbs: select listeners memory-type
                if cbs [
                    foreach cb cbs [
                        cb make object! [
                            type:   memory-type
                            action: action
                            value:  new
                            at:     index
                        ]
                    ]
                ]
            ]
        ]

        ; API
        watch: func [memory-type [word!] callback [function!]][
            append select listeners memory-type callback
        ]

        store-semantic: func [key value confidence][
            append semantic-store reduce [key value confidence now]
        ]

        store-episode: func [event confidence][
            append episodic-store reduce [event confidence now]
        ]

        add-to-working: func [item][
            ; Working memory cap: 7 items (Miller's Law)
            if (length? working-store) >= 7 [
                remove working-store   ; evict oldest
            ]
            append working-store item
        ]
    ]
    mem
]

; ══════════════════════════════════════════════════════════════════
; SECTION 3: INTENT PARSER USING TRANSCODE/TRACE
; ══════════════════════════════════════════════════════════════════

; Parse natural-language-like intent into structured goal blocks
parse-intent: func [
    "Convert structured text intent to Red/Cognition goal block"
    intent-text [string!]
    return: [block!]
    /local tokens goal-block current-verb
][
    tokens: copy []
    goal-block: copy []
    current-verb: none

    ; Use transcode/trace to build token stream
    transcode/trace intent-text func [
        event   [word!]
        input   [string!]
        type    [datatype! word!]
        line    [integer!]
        token
    ][
        if event = 'decoded [
            switch type [
                word!    [append tokens reduce ['word  token]]
                string!  [append tokens reduce ['text  token]]
                file!    [append tokens reduce ['path  token]]
                url!     [append tokens reduce ['url   token]]
                integer! [append tokens reduce ['num   token]]
                float!   [append tokens reduce ['float token]]
            ]
        ]
    ]

    ; Map token stream to cognitive dialect
    parse tokens [
        any [
            ; "observe <target>"
            [['word 'observe] | ['word 'watch] | ['word 'monitor]] (
                current-verb: 'observe
            ) ['word | 'text | 'path] set target skip (
                append goal-block reduce ['observe target]
            )
            |
            ; "analyse <target>"
            [['word 'analyse] | ['word 'analyze] | ['word 'inspect]] (
                current-verb: 'analyse
            ) ['word | 'text | 'path] set target skip (
                append goal-block reduce ['reason ['analyse target]]
            )
            |
            ; "generate report" / "create summary"
            [['word 'generate] | ['word 'create]] ['word | 'text]
            set artifact skip (
                append goal-block reduce ['act ['generate artifact]]
            )
            |
            ; "remember <fact>"
            ['word 'remember] set fact skip (
                append goal-block reduce ['remember fact]
            )
            |
            skip
        ]
    ]

    goal-block
]

; ══════════════════════════════════════════════════════════════════
; SECTION 4: RESOURCE BUDGET USING MONEY!
; ══════════════════════════════════════════════════════════════════

; Cognitive budget tracker using money! for precise accounting
make-budget: func [
    "Create a reasoning budget with money! precision"
    total [money!]
][
    make object! [
        total:     total
        spent:     $0.00
        reserved:  $0.00
        currency:  'USD

        available: does [total - spent - reserved]

        can-afford?: func [cost [money!]][
            cost <= available
        ]

        spend: func [
            "Deduct from budget — returns false if insufficient"
            cost    [money!]
            label   [string!]
            return: [logic!]
        ][
            either can-afford? cost [
                spent: spent + cost
                print rejoin [
                    "SPEND $" cost " for " label
                    " | Remaining: $" available
                ]
                true
            ][
                print rejoin [
                    "BUDGET EXCEEDED: need $" cost
                    " but only $" available " available"
                ]
                false
            ]
        ]

        reserve: func [amount [money!]][
            reserved: reserved + amount
        ]

        release: func [amount [money!]][
            reserved: max $0.00 reserved - amount
        ]

        report: does [
            print rejoin [
                "Budget Report^/"
                "  Total:    $" total    "^/"
                "  Spent:    $" spent    "^/"
                "  Reserved: $" reserved "^/"
                "  Available:$" available
            ]
        ]
    ]
]

; ══════════════════════════════════════════════════════════════════
; SECTION 5: SPATIAL COGNITION USING POINT3D!
; ══════════════════════════════════════════════════════════════════

; Spatial memory for robotics/embodied cognition dialect
make-spatial-memory: func ["3D spatial memory using point3D! natively"][
    make object! [
        ; Named locations in 3D space
        locations:  make map! []
        ; Trajectory history
        path:       copy []
        ; Current position
        position:   0.0x0.0x0.0     ; point3D!

        ; Record named location
        mark-location: func [name [word!] pos [point3D!]][
            put locations name pos
            print rejoin [
                "MARKED: " name
                " at " pos/x "," pos/y "," pos/z
            ]
        ]

        ; Navigate to location
        move-to: func [target [point3D!]][
            append path position   ; record history
            position: target
            print rejoin [
                "MOVED to "
                position/x "," position/y "," position/z
            ]
        ]

        ; Euclidean distance to named location
        distance-to: func [name [word!]][
            loc: select locations name
            if loc [
                dx: position/x - loc/x
                dy: position/y - loc/y
                dz: position/z - loc/z
                sqrt (dx * dx) + (dy * dy) + (dz * dz)
            ]
        ]

        ; Find nearest known location
        nearest: func [/local min-dist min-name d][
            min-dist: 1e30
            min-name: none
            foreach [name loc] locations [
                dx: position/x - loc/x
                dy: position/y - loc/y
                dz: position/z - loc/z
                d: sqrt (dx * dx) + (dy * dy) + (dz * dz)
                if d < min-dist [
                    min-dist: d
                    min-name: name
                ]
            ]
            reduce [min-name min-dist]
        ]
    ]
]

; ══════════════════════════════════════════════════════════════════
; SECTION 6: COMPLETE INTEGRATED COGNITIVE AGENT
; ══════════════════════════════════════════════════════════════════

make-cognitive-agent-v3: func [
    name    [string!]
    budget  [money!]
][
    agent: make object! [
        ; Identity
        id:       checksum form reduce [name now] 'sha256
        name:     name

        ; Core systems
        memory:   make-reactive-memory
        spatial:  make-spatial-memory
        budget:   make-budget budget

        ; Reactive memory monitoring
        ; — fires on every memory mutation (ownership system)
        setup-watchers: does [
            ; Watch semantic memory for contradictions
            memory/watch 'semantic func [event][
                if event/action = 'insert [
                    print rejoin [
                        "[MEMORY] New semantic: "
                        mold event/value
                    ]
                ]
            ]

            ; Watch episodic memory to trigger consolidation
            memory/watch 'episodic func [event][
                ; Auto-consolidate when episodic store grows large
                if (length? memory/episodic-store) > 50 [
                    print "[MEMORY] Consolidation threshold reached"
                    ; trigger background consolidation
                ]
            ]
        ]

        ; Goal execution with budget checking
        execute-goal: func [
            goal-spec [block!]
            cost      [money!]
            /local receipts
        ][
            unless budget/spend cost rejoin ["Goal: " mold goal-spec] [
                return make object! [
                    status: 'budget-exceeded
                    goal: goal-spec
                ]
            ]
            receipts: copy []
            foreach step goal-spec [
                append receipts execute-step step
            ]
            make object! [
                status:   'completed
                goal:     goal-spec
                receipts: receipts
                cost:     cost
            ]
        ]

        execute-step: func [step [any-type!]][
            switch type?/word step [
                block! [
                    reduce [
                        'step-result
                        'block-executed
                        (length? step)
                        'sub-steps
                    ]
                ]
                word! [
                    reduce ['step step 'dispatched]
                ]
            ]
        ]

        ; Intent-driven execution
        do-intent: func [
            "Parse natural intent and execute as goal"
            text    [string!]
            cost    [money!]
        ][
            goal-block: parse-intent text
            print rejoin ["Parsed goal: " mold goal-block]
            execute-goal goal-block cost
        ]
    ]

    agent/setup-watchers

    ; Initial spatial setup
    agent/spatial/mark-location 'home    0.0x0.0x0.0
    agent/spatial/mark-location 'office  10.0x0.0x2.5
    agent/spatial/mark-location 'storage 5.0x8.0x0.0

    ; Initial knowledge
    agent/memory/store-semantic 'agent 'name name 1.0
    agent/memory/store-semantic 'agent 'budget-total budget 1.0

    agent
]

; ══════════════════════════════════════════════════════════════════
; SECTION 7: DEMONSTRATION RUN
; ══════════════════════════════════════════════════════════════════

print "^/╔══════════════════════════════════════════╗"
print "║  Red/Cognition v0.3 — Full Integration   ║"
print "╚══════════════════════════════════════════╝^/"

; Create agent with $10.00 reasoning budget
bot: make-cognitive-agent-v3 "CogAgent-Alpha" $10.00

; Test intent parsing
print "^/── Intent Parsing ────────────────────────"
result: bot/do-intent
    "observe filesystem analyse changes generate report"
    $1.50

print rejoin ["Result status: " result/status]

; Test spatial cognition
print "^/── Spatial Navigation ─────────────────────"
bot/spatial/move-to  5.0x4.0x1.0
nearest: bot/spatial/nearest
print rejoin ["Nearest: " nearest/1 " at " nearest/2 " units"]
print rejoin ["Distance to office: "
    bot/spatial/distance-to 'office]

; Test reactive memory (ownership-triggered)
print "^/── Reactive Memory (Ownership Events) ─────"
bot/memory/store-semantic 'project 'name "OpenClaw" 0.95
bot/memory/store-episode  "repository scanned" 0.85
bot/memory/add-to-working "current task: code review"

; Test budget tracking
print "^/── Budget Status ──────────────────────────"
bot/budget/report

print "^/╔══════════════════════════════════════════╗"
print "║  Red/Cognition v0.3 Complete             ║"
print "╚══════════════════════════════════════════╝"
```

## Summary — Red Technical Specification: Parts I, II, III

The three-part specification now covers the complete documented technical surface of Red:

```
┌──────────────────────────────────────────────────────────────────────┐
│              COMPLETE TECHNICAL COVERAGE MAP                         │
├─────────────────────────────────────────────────────────────────────-┤
│  PART I   │ Architecture · Toolchain · Type System · Memory Model    │
│           │ GC · Parse Dialect · GUI/View · Homoiconicity           │
│           │ Platform Targets · CLI Reference · Red/Cognition v0.1   │
├───────────┼──────────────────────────────────────────────────────────┤
│  PART II  │ Interpreter Internals · Word/Context Binding             │
│           │ Reactive Engine Source · LibRed C/Python/Ruby API       │
│           │ Macro/Preprocessor · Concurrency/MPMC · Redbin          │
│           │ Red/Cognition v0.2 Production Prototype                 │
├───────────┼──────────────────────────────────────────────────────────┤
│  PART III │ New Lexer Architecture + Instrumentation API            │
│           │ routine! FFI Bridge · Atomic Intrinsics                 │
│           │ Ownership System + on-deep-change* Events               │
│           │ Port!/Scheme System · New Datatypes (money! ref!        │
│           │ point2D! point3D!) · FPU Control · #INLINE Directive    │
│           │ Draw Dialect Full Reference · Standard Library Map      │
│           │ Debug/Trace API · Red/Cognition v0.3 Full Integration   │
└───────────┴──────────────────────────────────────────────────────────┘
```

Significant improvements to the Red and Red/System memory management sub-systems and garbage collector will bring them to the level required for Red v1.0. Those changes were released in the bumped 0.6.6 version. Those memory improvements are also needed for completing work on the async IO branch. Another version bump will follow with the deprecation of the high-level Red compiler and the addition of a new powerful layer to the Red tower of languages. All those changes are pre-requirements to start work on 64-bit support.

Another version bump will follow with the deprecation of the high-level Red compiler and the addition of a new powerful layer to the Red tower of languages — and it is precisely at that boundary where Red/Cognition becomes not a prototype but a first-class layer: the new compiler infrastructure, the IR introduction, and the JIT all provide the technical substrate that the cognitive layer requires to compile intent into verified, performant, deployable cognitive execution.

---

**Traceability:** All content extracted verbatim from Sections XXVII–XXXIX and the Summary of the ninth user message. Every section heading, diagram, table, BNF grammar, code example, API reference, and architectural description has been preserved exactly as provided. No information added or inferred.