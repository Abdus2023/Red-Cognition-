# XXIX. Red/System Atomic Intrinsics — The Complete Specification

```ascii
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