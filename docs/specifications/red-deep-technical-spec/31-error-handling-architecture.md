# XLI. The Error Handling Architecture — Complete Specification

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│              RED ERROR SYSTEM — COMPLETE ARCHITECTURE                │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ERROR! OBJECT SCHEMA:                                               │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  error! extends object!                                     │    │
│  │    type:     word!     ; error category                     │    │
│  │    id:       word!     ; specific error identifier          │    │
│  │    message:  string! | block!  ; human-readable description │    │
│  │    near:     string!   ; source location of error           │    │
│  │    where:    word!     ; function/native that threw         │    │
│  │    stack:    block!    ; call stack at time of error        │    │
│  │    arg1:     any-type! ; error-specific argument 1         │    │
│  │    arg2:     any-type! ; error-specific argument 2         │    │
│  │    arg3:     any-type! ; error-specific argument 3         │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ERROR CATEGORY TAXONOMY:                                            │
│  ┌─────────────────────┬──────────────────────────────────────┐     │
│  │  Category           │  Example IDs                         │     │
│  ├─────────────────────┼──────────────────────────────────────┤     │
│  │  syntax             │  invalid invalid-char malformed      │     │
│  │  script             │  no-value not-defined bad-path       │     │
│  │                     │  bad-arg bad-type no-op              │     │
│  │  math               │  zero-divide overflow positive       │     │
│  │                     │  not-related out-of-range            │     │
│  │  access             │  cannot-open not-connected           │     │
│  │                     │  no-script read-only                 │     │
│  │  internal           │  bad-sys-func stack-overflow         │     │
│  │                     │  no-memory                           │     │
│  │  user               │  message (user-defined errors)       │     │
│  └─────────────────────┴──────────────────────────────────────┘     │
│                                                                      │
│  ERROR HANDLING MECHANISMS:                                          │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                                                             │    │
│  │  1. TRY — catch any error                                   │    │
│  │     result: try [risky-code]                                │    │
│  │     if error? result [handle result]                        │    │
│  │                                                             │    │
│  │  2. TRY/with — catch and handle immediately                 │    │
│  │     try/with [risky-code] func [e][                         │    │
│  │         print ["Error:" e/id]                               │    │
│  │     ]                                                       │    │
│  │                                                             │    │
│  │  3. ATTEMPT — return none on error (silent)                 │    │
│  │     result: attempt [risky-code]   ; none if error         │    │
│  │                                                             │    │
│  │  4. ERROR? — test if value is error                         │    │
│  │     if error? x [handle x]                                  │    │
│  │                                                             │    │
│  │  5. MAKE ERROR! — create custom error                       │    │
│  │     e: make error! [                                        │    │
│  │         type: 'user                                         │    │
│  │         id:   'message                                      │    │
│  │         message: "Custom error message"                     │    │
│  │     ]                                                       │    │
│  │     do e    ; throw it                                      │    │
│  │                                                             │    │
│  │  6. CAUSE-ERROR — throw with category and id               │    │
│  │     cause-error 'user 'message ["Specific message"]         │    │
│  │                                                             │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```