# Red Programming Language — Deep Technical Specification

**Source Message:** Ninth (final) user message — Comprehensive Red architecture reference

**Stable ID:** RED-SPEC-001

## Overview

This document provides a comprehensive architecture reference drawn from official documentation, the Red/Red GitHub repository, the Red/System compiler overview, and the official language specification.

## I. The Full-Stack Architecture — "One Language from Hardware to Human"

Red is a next-generation programming language strongly inspired by Rebol, with a broader field of usage thanks to its native-code compiler — from system programming to high-level scripting and cross-platform reactive GUI, while providing modern support for concurrency. Red tackles software complexity using a DSL-oriented approach, calling them **dialects**.

```
┌──────────────────────────────────────────────────────────────────────┐
│                   RED FULL-STACK ARCHITECTURE                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │              Human / Application Layer                       │   │
│   │    Scripts · GUI Apps · Data Processing · Domain Tools      │   │
│   └──────────────────────────┬──────────────────────────────────┘   │
│                              │                                       │
│   ┌──────────────────────────▼──────────────────────────────────┐   │
│   │               Red Language (High Level)                      │   │
│   │  Interpreter + Compiler · Dialects · Reactive GUI           │   │
│   │  40+ Datatypes · Objects · Functions · Metaprogramming      │   │
│   └──────────────────────────┬──────────────────────────────────┘   │
│                              │                                       │
│   ┌──────────────────────────▼──────────────────────────────────┐   │
│   │              Red/System (Low Level DSL)                      │   │
│   │   C-level · Pointers · Structs · Native Code · OS Calls     │   │
│   │   Memory Management · ARM/IA-32 Targets                     │   │
│   └──────────────────────────┬──────────────────────────────────┘   │
│                              │                                       │
│   ┌──────────────────────────▼──────────────────────────────────┐   │
│   │                  Machine Code                                │   │
│   │      PE/COFF (Windows) · ELF (Linux/Unix) · Mach-O (macOS) │   │
│   └──────────────────────────┬──────────────────────────────────┘   │
│                              │                                       │
│   ┌──────────────────────────▼──────────────────────────────────┐   │
│   │                    Hardware                                  │   │
│   │         IA-32 · ARM · x86-64 (via 32-bit)                   │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## II. The Complete Toolchain

Red has its own complete cross-platform toolchain, featuring an **encapper**, a **native compiler**, an **interpreter**, and a **linker**, not depending on any third-party library, except for a Rebol2 interpreter, required during the alpha stage.

Red's runtime library is written in Red/System, and uses a **hybrid approach**: it compiles what it can deduce statically and uses an embedded interpreter otherwise.

Red seeks to remain independent of any other toolchain; it does its own code generation. It is therefore possible to **cross-compile** Red programs from any platform it supports to any other, via a command-line switch.

```
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

## III. The Red/System Compiler — Internal Source Map

The Red/System compiler source is organised as follows:

```
red-system/
  %compiler.r    ; Main compiler code, loads everything else
  %emitter.r     ; Target code emitter abstract layer
  %linker.r      ; Format files loader
  %rsc.r         ; Compiler's front-end for standalone usage
  formats/
    %PE.r        ; Windows PE/COFF file format emitter
    %ELF.r       ; UNIX ELF file format emitter
  library/       ; Third-party libraries
  runtime/
    %common.reds ; Cross-platform definitions
    %win32.r     ; Windows-specific bindings
    %linux.r     ; Linux-specific bindings
  targets/
    %target-class.r ; Base utility class for emitters
    %IA32.r         ; Intel IA32 code emitter
  tests/           ; Unit tests
```

The **objects hierarchy** in memory after loading:

```
system/words/          ; global REBOL context
system-dialect/        ; main object
  loader/              ; preprocessor object
    process            ; preprocessor entry point function
  compiler/            ; compiler object
    compile            ; compiler entry point function
  emitter/             ; code emitter object
```

### Code Generation Model

All the `compiler/comp-*` functions are used to recursively analyse the source code, each one matching a specific semantic rule from the Red/System language specification. The **production of native code is direct** — there is no intermediary representation; machine code is generated as soon as a language statement or expression is matched. This is the simplest approach, but code cannot be efficiently optimised without a proper IR. When Red/System is rewritten in Red, a simple IR will be introduced to enable the full range of possible code optimisations.

This is the key architectural limitation and roadmap item:

```
CURRENT ARCHITECTURE (Direct Emission):
  Source Statement → comp-* function → Machine Code bytes

PLANNED ARCHITECTURE (IR-based):
  Source Statement → comp-* function → IR node → Optimiser → Machine Code
```

## IV. Red/System Language — Complete Specification Layers

Expressions are the basic building blocks of a Red/System program. The grammar rules are specified in **BNF format**.

### BNF Grammar Core (Red/System)

```bnf
; ═══════════════════════════════════════════════
; RED/SYSTEM CORE BNF GRAMMAR
; ═══════════════════════════════════════════════

<program>     ::= <declaration>*

<declaration> ::= <func-decl>
                | <var-decl>
                | <struct-decl>
                | <import-decl>
                | <statement>

<func-decl>   ::= <word> ":" "func" "[" <spec> "]" "[" <body> "]"

<spec>        ::= <param>* [return: [<type>]]
<param>       ::= <word> "[" <type> "]"

<type>        ::= integer! | float! | float32! | byte! | logic!
                | pointer! "[" <type> "]"
                | struct! "[" <member>+ "]"
                | c-string!
                | <word>   ; aliased type

<statement>   ::= <assignment>
                | <if-stmt>
                | <either-stmt>
                | <while-stmt>
                | <until-stmt>
                | <loop-stmt>
                | <func-call>
                | <return-stmt>

<literal>     ::= ... any valid Red/System literal value ...
<variable>    ::= ... any valid Red/System variable name ...
<logic-call>  ::= ... function call returning logic! ...
<func-call>   ::= ... function call returning a value ...
```

### Type System

```
┌─────────────────────────────────────────────────────────────┐
│              RED/SYSTEM TYPE HIERARCHY                       │
├────────────────────┬────────────────────────────────────────┤
│  SCALAR TYPES      │  integer!   (32-bit signed)            │
│                    │  float!     (64-bit IEEE 754)          │
│                    │  float32!   (32-bit IEEE 754)          │
│                    │  byte!      (8-bit unsigned)           │
│                    │  logic!     (true/false)               │
├────────────────────┼────────────────────────────────────────┤
│  POINTER TYPES     │  pointer! [integer!]                   │
│                    │  pointer! [byte!]                      │
│                    │  pointer! [struct! [...]]              │
├────────────────────┼────────────────────────────────────────┤
│  COMPOSITE TYPES   │  struct! [field [type] ...]            │
│                    │  c-string!  (null-terminated UTF-8)    │
├────────────────────┼────────────────────────────────────────┤
│  ALIAS             │  alias struct! [...]  → new type name  │
└────────────────────┴────────────────────────────────────────┘
```

### Library Import Directive

Red/System is able to load external shared libraries at the time a Red/System executable is loaded by the OS. This requires that the programmer gives instructions to the compiler about which library to load and how to map library functions and variables to the Red/System context. This feature is called **library import** and is supported by the `#import` compiler directive.

```red
; Red/System library import syntax
#import [
    "libc.so.6" cdecl [
        malloc: "malloc" [
            size    [integer!]
            return: [pointer! [byte!]]
        ]
        free: "free" [
            ptr     [pointer! [byte!]]
        ]
        printf: "printf" [
            fmt     [c-string!]
            ...
            return: [integer!]
        ]
    ]
]
```

### Red/System Code Example — Complete System Program

```red
Red/System []

; ── Struct definition ──────────────────────────────────────────
point: alias struct! [
    x   [integer!]
    y   [integer!]
]

; ── Function with pointer manipulation ─────────────────────────
distance-sq: func [
    a   [point]
    b   [point]
    return: [integer!]
    /local dx dy
][
    dx: a/x - b/x
    dy: a/y - b/y
    (dx * dx) + (dy * dy)
]

; ── Native memory allocation ────────────────────────────────────
make-point: func [
    x   [integer!]
    y   [integer!]
    return: [point]
    /local p
][
    p: as point allocate size? point
    p/x: x
    p/y: y
    p
]

; ── Main entry ─────────────────────────────────────────────────
main: func [
    /local p1 p2 d
][
    p1: make-point 0 0
    p2: make-point 3 4
    d: distance-sq p1 p2    ; → 25
    free as byte-ptr! p1
    free as byte-ptr! p2
]
```

## V. Red Memory Model — Complete Internal Architecture

Here is a simplified overview of the Red memory model. **All Red values are stored in series.** Some Red values require one or more buffers to hold their content. Values can never reference a buffer directly, but only through a **node reference**, to enable relocation when expanding the series buffer or when moving it around during compaction by the GC.

```
┌──────────────────────────────────────────────────────────────────────┐
│                    RED MEMORY MODEL                                  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    NODE FRAMES                               │    │
│  │                                                              │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │    │
│  │  │ Node     │  │ Node     │  │ Node     │  │ Node     │   │    │
│  │  │ Frame 1  │  │ Frame 2  │  │ Frame 3  │  │ Frame N  │   │    │
│  │  │          │  │          │  │          │  │          │   │    │
│  │  │[node ref]│  │[node ref]│  │[node ref]│  │[node ref]│   │    │
│  │  │[node ref]│  │[node ref]│  │[node ref]│  │[node ref]│   │    │
│  │  │[node ref]│  │[node ref]│  │   ...    │  │   ...    │   │    │
│  │  └────┬─────┘  └────┬─────┘  └──────────┘  └──────────┘   │    │
│  │       │             │                                        │    │
│  └───────┼─────────────┼────────────────────────────────────── ┘    │
│          │             │                                             │
│          ▼             ▼                                             │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                  SERIES BUFFERS (Heap)                       │    │
│  │                                                              │    │
│  │  ┌────────────────────────────────────────────┐             │    │
│  │  │  Series Buffer                             │             │    │
│  │  │  ┌──────┬──────┬──────┬──────┬──────────┐ │             │    │
│  │  │  │ HDR  │ val0 │ val1 │ val2 │  ...     │ │             │    │
│  │  │  └──────┴──────┴──────┴──────┴──────────┘ │             │    │
│  │  │  head ptr ──►                              │             │    │
│  │  │  tail ptr ──────────────────────►          │             │    │
│  │  └────────────────────────────────────────────┘             │    │
│  │                                                              │    │
│  │  Buffer Header (HDR):                                        │    │
│  │    size     : allocated slots                                │    │
│  │    offset   : current head offset                           │    │
│  │    type     : series type ID                                 │    │
│  │    flags    : GC mark bit, lock bit, etc.                   │    │
│  │    node-ref : back-pointer to owning node                   │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │              VALUE REPRESENTATION (16 bytes each)            │    │
│  │                                                              │    │
│  │  Bytes 0-3:  Type ID (datatype!  number)                    │    │
│  │  Bytes 4-7:  Flags / extra type info                        │    │
│  │  Bytes 8-15: Value payload (varies by type)                 │    │
│  │                                                              │    │
│  │  integer!  → [type][flags][value int32][padding]            │    │
│  │  float!    → [type][flags][value float64       ]            │    │
│  │  block!    → [type][flags][node-ref ][head-idx ]            │    │
│  │  string!   → [type][flags][node-ref ][head-idx ]            │    │
│  │  object!   → [type][flags][node-ref ][ctx-idx  ]            │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Garbage Collector — The "Simple GC"

As of version 0.6.4, Red includes a garbage collector — "the **Simple GC**".

This milestone brings many low-level improvements to Red's memory management and garbage collecting. Most of those are long-planned additions needed to complete the internal memory model and make it robust enough for the future stable Red v1.0.

All Red values are stored in series. Some Red values require one or more buffers to hold their content. Values can never reference a buffer directly, but only through a node reference, to enable relocation when expanding the series buffer or when moving it around during compaction by the GC.

```
┌──────────────────────────────────────────────────────────────┐
│               RED GC CYCLE — MARK & COMPACT                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Phase 1 — MARK                                              │
│  ┌──────────────────────────────────────────┐               │
│  │  Walk all root references:               │               │
│  │    → Global context words                │               │
│  │    → Stack frames                        │               │
│  │    → Red/View face! objects              │               │
│  │    → font! objects (OS-linked)           │               │
│  │  Set MARK bit in each reachable          │               │
│  │  series buffer header                    │               │
│  └──────────────────────────────────────────┘               │
│                                                              │
│  Phase 2 — SWEEP + COMPACT                                   │
│  ┌──────────────────────────────────────────┐               │
│  │  Walk all series buffers:                │               │
│  │    if MARK bit set → keep, clear bit     │               │
│  │    if MARK bit clear → free buffer       │               │
│  │  Compact remaining buffers               │               │
│  │  Update all node references              │               │
│  │  (nodes act as stable indirection)       │               │
│  └──────────────────────────────────────────┘               │
│                                                              │
│  Debug Output (0.6.6+):                                      │
│    memory usage before/after GC cycle                        │
│    GC cycle timing measurement                               │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## VI. The Complete Datatype System — 50+ Types

Red's documentation covers the full datatype system, including typesets, the GUI system, the View Engine, VID Dialect, Draw Dialect, Rich-Text Dialect, Parse, Lexer, Reactive Programming, and LibRed API.

```
┌──────────────────────────────────────────────────────────────────────┐
│                RED DATATYPE TAXONOMY (50+ types)                     │
├─────────────────────┬────────────────────────────────────────────────┤
│  SCALAR TYPES       │  integer!  float!  percent!  money!            │
│                     │  char!     logic!  none!     unset!            │
│                     │  pair!     time!   date!     tuple!            │
├─────────────────────┼────────────────────────────────────────────────┤
│  SERIES TYPES       │  string!   block!  paren!    path!             │
│  (positional        │  binary!   vector! hash!     map!              │
│   head/tail)        │  file!     url!    tag!      email!            │
│                     │  ref!      issue!                              │
├─────────────────────┼────────────────────────────────────────────────┤
│  WORD TYPES         │  word!     set-word!   get-word!  lit-word!    │
│  (symbolic          │  refinement!                                   │
│   references)       │  path!     set-path!   get-path!  lit-path!   │
├─────────────────────┼────────────────────────────────────────────────┤
│  FUNCTION TYPES     │  function!  native!  action!  op!              │
│                     │  routine!  (R/S bridge)                        │
├─────────────────────┼────────────────────────────────────────────────┤
│  OBJECT/CONTEXT     │  object!   error!   port!                      │
│  TYPES              │  face!     (GUI widget)                        │
│                     │  event!    (input event)                       │
├─────────────────────┼────────────────────────────────────────────────┤
│  SYSTEM TYPES       │  datatype!  typeset!  handle!                  │
│                     │  image!     bitset!                            │
└─────────────────────┴────────────────────────────────────────────────┘
```

### Every Type has a Corresponding Action Set

```red
; Actions are polymorphic operations on all datatypes
; Each type implements the relevant subset:

make        ; construct a new value
to          ; convert between types
form        ; convert to human-readable string
mold        ; convert to Red source representation
bind        ; bind words to a context
reflect     ; introspect internal structure

; Series actions (for series types only):
append  insert  remove  clear
head    tail    next    back
index?  length? at      pick
poke    copy    sort    reverse
find    select  skip
```

## VII. The Built-in Dialect System

Red tackles software building complexity using a **DSL-oriented approach** (called dialects). The built-in dialects include Red/System — a C-level system programming language compiled to native code.

Built-in dialects include: **Parse** (a powerful PEG parser), **VID** (a simple GUI layout creation dialect), **Draw** (a vector 2D drawing dialect), and **Rich-text** (a rich-text description dialect).

```
┌──────────────────────────────────────────────────────────────────────┐
│                  RED DIALECT ECOSYSTEM                               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  DIALECT 1: Red/System                                       │    │
│  │  Purpose: C-level systems programming                        │    │
│  │  Target:  Direct machine code (IA-32, ARM)                  │    │
│  │  Features: pointers, structs, OS calls, no GC               │    │
│  │                                                              │    │
│  │  Red/System [origin: 'Red]                                  │    │
│  │  n: 0  while [n < 10][print n  n: n + 1]                   │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  DIALECT 2: Parse                                            │    │
│  │  Purpose: PEG-based pattern matching and transformation      │    │
│  │  Target:  string! or block! series input                    │    │
│  │  Grammar: TDPL (Top-Down Parsing Language) family           │    │
│  │                                                              │    │
│  │  parse "hello world" [                                      │    │
│  │      copy word: to space  skip                              │    │
│  │      copy rest: to end                                      │    │
│  │  ]                                                          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  DIALECT 3: VID (Visual Interface Dialect)                   │    │
│  │  Purpose: Declarative native GUI layout                      │    │
│  │  Target:  face! objects + View engine                       │    │
│  │                                                              │    │
│  │  view [                                                      │    │
│  │      title "My App"                                         │    │
│  │      text  "Hello!"                                         │    │
│  │      field 200                                              │    │
│  │      button "OK" [print face/text]                          │    │
│  │  ]                                                          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  DIALECT 4: Draw                                             │    │
│  │  Purpose: 2D vector graphics                                 │    │
│  │  Target:  image! surface or canvas face                     │    │
│  │                                                              │    │
│  │  draw my-image [                                            │    │
│  │      pen blue  fill-pen red                                 │    │
│  │      circle 100x100 50                                      │    │
│  │      line  10x10 200x200                                    │    │
│  │      box   20x20 180x180                                    │    │
│  │  ]                                                          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  DIALECT 5: Rich-Text                                        │    │
│  │  Purpose: Formatted text with inline styles                  │    │
│  │  Target:  text-list and rich-text faces                     │    │
│  │                                                              │    │
│  │  rich-text [                                                │    │
│  │      bold "Title" nl                                        │    │
│  │      color red "Warning: " color black "message"           │    │
│  │  ]                                                          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## VIII. The Parse Dialect — Deep Specification

The Parse dialect is an embedded DSL for parsing input series using grammar rules. It is an **enhanced member of the TDPL family**. Parse's common usages are for checking, validating, extracting, modifying input data or even implementing embedded and external DSLs.

The core principles mention two modes for parsing. This is necessary in Red because of the two basic series datatypes: `string!` and `block!`.

```
┌──────────────────────────────────────────────────────────────────────┐
│             PARSE DIALECT — COMPLETE KEYWORD REFERENCE               │
├────────────────────────────────────────────────────────────────────  ┤
│                                                                      │
│  CALL SYNTAX:                                                        │
│    parse <input> <rules>                                             │
│    <input> : any series (string!, block!, binary!, ...)              │
│    <rules> : block! of parse rules                                   │
│                                                                      │
│  MATCHING RULES:                                                     │
│    <literal>          match exact value                              │
│    <datatype>         match any value of that type                   │
│    <word>             match via word reference                       │
│    <bitset>           match char in set (string mode only)          │
│                                                                      │
│  QUANTIFIERS:                                                        │
│    <n> <rule>         match exactly n times                          │
│    <n> <m> <rule>     match n to m times                             │
│    opt  <rule>        match 0 or 1 times                             │
│    any  <rule>        match 0 or more times (greedy)                │
│    some <rule>        match 1 or more times                          │
│                                                                      │
│  NAVIGATION:                                                         │
│    to   <rule>        advance TO the match point                     │
│    thru <rule>        advance THROUGH the match point                │
│    skip               advance one position unconditionally           │
│    end                match only at series end                       │
│                                                                      │
│  EXTRACTION:                                                         │
│    copy <word> <rule> copy matched input to word                     │
│    set  <word> <rule> set word to matched value                      │
│    keep <rule>        collect match into result block                │
│    collect [<rules>]  create result block from keep rules            │
│                                                                      │
│  CONTROL FLOW:                                                       │
│    |                  alternation (OR)                               │
│    [<rules>]          grouping (sequence)                            │
│    (<expr>)           escape: evaluate Red expression in place       │
│    if (<expr>)        conditional match                              │
│    not <rule>         negative lookahead                             │
│    ahead <rule>       positive lookahead (no consumption)           │
│                                                                      │
│  MUTATION:                                                           │
│    insert <value>     insert value at current position               │
│    remove <rule>      remove matched portion                         │
│    change <rule> <v>  replace matched portion with value             │
│                                                                      │
│  MARKS & POSITIONS:                                                  │
│    mark <word>        save current position                          │
│    seek <word>        restore saved position                         │
│                                                                      │
│  EXAMPLE — Parsing a simple expression grammar:                      │
│                                                                      │
│    digit: charset "0123456789"                                       │
│    alpha: charset [#"a" - #"z" #"A" - #"Z"]                         │
│    number: [some digit]                                              │
│    ident:  [alpha any [alpha | digit]]                               │
│                                                                      │
│    expr-parser: [                                                    │
│        collect [                                                     │
│            some [                                                    │
│                keep copy tok: [number | ident]                       │
│                (print ["token:" tok])                                │
│                | skip                                                │
│            ]                                                         │
│        ]                                                             │
│    ]                                                                 │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## IX. The GUI System — View Engine Architecture

Red 0.6.0 celebrated a major step forward with the addition of a brand new **GUI system entirely written in Red itself**.

The Red/View engine backends rely on external resources provided by the OS. Among those resources, some are linked to `face!` or `font!` objects and require special care when those objects are not reachable anymore.

```
┌──────────────────────────────────────────────────────────────────────┐
│                RED VIEW ENGINE ARCHITECTURE                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                  VID Dialect (User Layer)                    │    │
│  │   view [title "App"  field  button "OK" [action]]           │    │
│  └──────────────────────────┬──────────────────────────────────┘    │
│                             │ VID → face! tree construction          │
│                             ▼                                        │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │               Face! Object Tree (Data Model)                 │    │
│  │                                                              │    │
│  │   face! [                                                   │    │
│  │     type:    word!      ; window/button/field/text/...      │    │
│  │     offset:  pair!      ; position in parent                │    │
│  │     size:    pair!      ; width x height                    │    │
│  │     text:    string!    ; display text                      │    │
│  │     color:   tuple!     ; R.G.B or R.G.B.A                  │    │
│  │     image:   image!     ; background image                  │    │
│  │     data:    any        ; widget-specific data              │    │
│  │     enable?: logic!     ; interaction enabled               │    │
│  │     visible?:logic!     ; visibility                        │    │
│  │     selected: integer!  ; selection index                   │    │
│  │     flags:   block!     ; platform flags                    │    │
│  │     draw:    block!     ; Draw dialect block                │    │
│  │     font:    object!    ; font! object                      │    │
│  │     para:    object!    ; para! layout object               │    │
│  │     actors: object!     ; event handler object              │    │
│  │     extra:  any         ; user-defined data                 │    │
│  │     pane:   block!      ; child faces                       │    │
│  │     parent: face!       ; parent face reference             │    │
│  │     state:  block!      ; internal platform state           │    │
│  │   ]                                                         │    │
│  └──────────────────────────┬──────────────────────────────────┘    │
│                             │ Reactive dataflow sync                 │
│                             ▼                                        │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │           Reactive Dataflow Engine                           │    │
│  │   ON-CHANGE events on face/font/para property writes        │    │
│  │   react [face1/color: face2/color]  ; live binding          │    │
│  │   Deep reactive paths support                               │    │
│  └──────────────────────────┬──────────────────────────────────┘    │
│                             │ Platform calls                         │
│                             ▼                                        │
│  ┌──────────────────────────────────────────────────────────── ┐    │
│  │              Platform Backend (OS-specific)                  │    │
│  │                                                              │    │
│  │   Windows  → Win32 API  (GDI/Direct2D)                      │    │
│  │   macOS    → Cocoa      (NSWindow / CoreGraphics)           │    │
│  │   Linux    → GTK+       (Cairo)                             │    │
│  │   Android  → Android SDK                                    │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Reactive Programming Model

Reactions are created using the `react` keyword, directly from Red code or from the VID dialect. The syntax is `react [<body>]` where `<body>` is regular Red code. This creates a new reactor from the body block.

Compound scalar datatypes (`pair!`, `date!`, `time!`, and `tuple!`) will now emit **ON-CHANGE events** when one of their components is changed using an access path (both in compiled and interpreted code).

```red
; ── Reactive GUI Example ───────────────────────────────────────────
view [
    title "Reactive Demo"

    ; Slider drives text display — live reactive binding
    sl: slider 200x20
    text 200x20 react [face/text: form to-integer sl/data * 100]

    ; Reactive color change
    b: base 100x100 red
    react [b/color: either sl/data < 0.5 [red][green]]

    ; Event-driven button
    button "Reset" [sl/data: 0.0]
]
```

## X. Homoiconicity — Code as Data Architecture

Red is a **homoiconic language**, which is capable of metaprogramming with Rebol-like semantics.

This is Red's most architecturally significant property: the same block structure that holds data also holds and represents executable code.

```
┌──────────────────────────────────────────────────────────────────────┐
│              HOMOICONICITY — CODE IS DATA                            │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  In Red, a BLOCK is the universal container:                         │
│                                                                      │
│  DATA block:                                                         │
│    config: [host "localhost"  port 8080  debug true]                 │
│                                                                      │
│  CODE block (same structure, different evaluation context):          │
│    [print "hello"  x: 42  if x > 0 [print "positive"]]              │
│                                                                      │
│  DIALECT block (interpreted by a custom evaluator):                  │
│    [circle 100x100 50  line 10x10 200x200]   ; Draw dialect          │
│    [some digit opt [#"." some digit]]         ; Parse dialect        │
│                                                                      │
│  Since code IS data, you can:                                        │
│                                                                      │
│  ; Inspect a function's body as a block                              │
│  source: body-of :some-function                                      │
│                                                                      │
│  ; Construct code at runtime                                         │
│  my-code: compose [print (some-variable)]                            │
│  do my-code                                                          │
│                                                                      │
│  ; Build a dialect evaluator                                         │
│  my-dialect: func [block [block!]] [                                 │
│      parse block [                                                   │
│          some [                                                       │
│              'go    (move-robot)                                     │
│            | 'turn  (turn-robot)                                     │
│            | 'stop  (stop-robot)                                     │
│          ]                                                           │
│      ]                                                               │
│  ]                                                                   │
│  my-dialect [go go turn go stop]    ; execute custom DSL             │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## XI. Platform Targets & Cross-Compilation Matrix

Integer division handling at low-level has notorious shortcomings with different handling for each edge case depending on the hardware platform. Intel IA-32 tends to handle those cases in a slightly safer way, while ARM architecture produces erroneous results silently. To reduce this gap, the R/S compiler now generates extra code to detect those cases for ARM targets and raise a runtime exception.

```
┌──────────────────────────────────────────────────────────────────────┐
│            RED CROSS-COMPILATION MATRIX                              │
├─────────────────┬──────────────────────────────────────────────────  ┤
│  HOST OS        │  Windows · Linux · macOS                           │
├─────────────────┼────────────────────────────────────────────────────┤
│  TARGET OS      │  Windows (Win32 PE/COFF)                           │
│                 │  Linux   (ELF 32-bit)                              │
│                 │  macOS   (Mach-O)                                  │
│                 │  Android (ARM ELF)                                 │
│                 │  FreeBSD (ELF)                                     │
│                 │  Raspberry Pi (ARM ELF)                            │
├─────────────────┼────────────────────────────────────────────────────┤
│  CPU TARGETS    │  IA-32   (Intel/AMD 32-bit)                        │
│                 │  ARM     (ARMv4–ARMv7, armhf)                      │
│                 │  x86-64  (via 32-bit compatibility)                │
├─────────────────┼────────────────────────────────────────────────────┤
│  OUTPUT FORMATS │  %PE.r   → .exe / .dll  (Windows)                 │
│                 │  %ELF.r  → ELF binary   (Linux/Android)           │
│                 │  Mach-O  → macOS binary                            │
├─────────────────┼────────────────────────────────────────────────────┤
│  USAGE SYNTAX   │  red -t Windows %myapp.red                         │
│                 │  red -t Linux   %myapp.red                         │
│                 │  red -t Android %myapp.red                         │
│                 │  red -t RPi     %myapp.red                         │
└─────────────────┴────────────────────────────────────────────────────┘
```

## XII. Red Roadmap — Official Architecture Evolution

The roadmap includes: static linking support; for Red/C3, a WASM backend to support the Ethereum EVM; version 1.4 bringing a proper web runtime environment to the WASM backend including GUI support; and **version 2.0 focused on bringing a proper JIT-compiler** to the Red runtime, which should radically improve code execution of critical parts without having to drop to Red/System.

The memory improvements are needed for completing work on the async IO branch. Another version bump will follow with the deprecation of the high-level Red compiler and the addition of a **new powerful layer** to the Red tower of languages. All these changes are pre-requirements to start work on 64-bit support.

```
┌──────────────────────────────────────────────────────────────────────┐
│                   RED OFFICIAL ROADMAP                               │
├──────────────┬───────────────────────────────────────────────────────┤
│  v0.6.6 ✅   │  Memory management & GC improvements                 │
│  (Current)   │  Async IO foundation                                  │
│              │  Reactive system enhancements                         │
│              │  ARM + Raspberry Pi support                           │
│              │  Static linking support                               │
├──────────────┼───────────────────────────────────────────────────────┤
│  v1.0        │  Self-hosted (Red compiled by Red)                    │
│  (Next major)│  Robust memory model complete                         │
│              │  IR introduced for optimisation                       │
│              │  Async IO complete                                    │
│              │  Stable ABI                                           │
├──────────────┼───────────────────────────────────────────────────────┤
│  v1.1        │  View engine architecture improvements                │
│              │  GUI backend enhancements                             │
├──────────────┼───────────────────────────────────────────────────────┤
│  v1.4        │  WASM backend complete                                │
│              │  Web runtime with GUI support                         │
│              │  Ethereum EVM support (Red/C3)                        │
├──────────────┼───────────────────────────────────────────────────────┤
│  v2.0        │  JIT compiler in Red runtime                          │
│  (Future)    │  Radical performance improvement                      │
│              │  64-bit support                                       │
│              │  New cognitive/agent layer (proposed)                 │
├──────────────┼───────────────────────────────────────────────────────┤
│  v3.0        │  Unannounced (post 1.0 reveal)                        │
└──────────────┴───────────────────────────────────────────────────────┘
```

## XIII. Complete Red Program — All Systems Demonstrated

```red
Red [
    Title:   "Red Architecture Demonstration"
    Purpose: "Shows all major subsystems in one program"
    Author:  "Red/Cognition Prototype"
    Version: 0.1.0
]

; ══════════════════════════════════════════════════════════════════
; SECTION 1: DATATYPES — All major categories
; ══════════════════════════════════════════════════════════════════

; Scalar types
i: 42                       ; integer!
f: 3.14159                  ; float!
p: 128.0.0.1                ; tuple!  (also IP addresses)
d: 2026-07-29               ; date!
t: 14:30:00                 ; time!
c: #"R"                     ; char!
coord: 100x200              ; pair!   (x/y coordinate)
pct: 85%                    ; percent!

; Series types
s: "Hello, Red!"            ; string!
b: [1 2 3 "four" 5.0]       ; block!   — the universal container
u: http://red-lang.org      ; url!
e: user@example.com         ; email!
f: %data/config.txt         ; file!

; Word types demonstrating symbolic system
my-word:    'symbol         ; word!   — unevaluated symbol
set-it:     42              ; set-word! (the : creates binding)
:get-it                     ; get-word!  (get without evaluate)

; ══════════════════════════════════════════════════════════════════
; SECTION 2: FUNCTIONS — All definition styles
; ══════════════════════════════════════════════════════════════════

; Standard function
add: func [
    a [integer!]
    b [integer!]
    return: [integer!]
][
    a + b
]

; Function with refinements (Red's named parameter groups)
greet: func [
    name    [string!]
    /formal                 ; refinement — optional parameter group
    /local msg              ; /local — private variables
][
    msg: either formal [
        rejoin ["Good day, " name "."]
    ][
        rejoin ["Hey, " name "!"]
    ]
    print msg
]

; Higher-order function
apply-twice: func [
    f   [function!]
    x   [integer!]
    return: [integer!]
][
    f f x
]

double: func [x [integer!]][x * 2]
print apply-twice :double 3   ; → 12

; ══════════════════════════════════════════════════════════════════
; SECTION 3: OBJECTS — Prototype-based OOP
; ══════════════════════════════════════════════════════════════════

; Base prototype
Animal: make object! [
    name:    "Unknown"
    sound:   "..."
    speak:   does [print rejoin [name " says: " sound]]
    describe: func [/local desc][
        desc: rejoin ["I am " name]
        print desc
    ]
]

; Derived object via prototype inheritance
Dog: make Animal [
    name:  "Rex"
    sound: "Woof!"
    fetch: does [print rejoin [name " fetches the ball!"]]
]

Dog/speak      ; → Rex says: Woof!
Dog/fetch      ; → Rex fetches the ball!

; ══════════════════════════════════════════════════════════════════
; SECTION 4: PARSE DIALECT — PEG Grammar
; ══════════════════════════════════════════════════════════════════

; Define character classes
digit: charset "0123456789"
alpha: charset [#"a" - #"z" #"A" - #"Z"]
space: charset " ^/^-"
ident-char: charset [#"a" - #"z" #"A" - #"Z" #"0" - #"9" #"-" #"_"]

; A simple tokeniser using Parse
tokenise: func [
    input [string!]
    return: [block!]
    /local tokens token
][
    tokens: copy []
    parse input [
        any [
            ; Skip whitespace
            some space
            |
            ; Match number
            copy token some digit (
                append tokens make map! [type: 'number value: to-integer token]
            )
            |
            ; Match identifier
            copy token [alpha any ident-char] (
                append tokens make map! [type: 'ident value: to-word token]
            )
            |
            ; Match operator
            copy token [#"+" | #"-" | #"*" | #"/"] (
                append tokens make map! [type: 'op value: token]
            )
            |
            ; Skip unknown
            skip
        ]
    ]
    tokens
]

result: tokenise "foo 42 + bar 100"
foreach tok result [
    print rejoin ["  " tok/type ": " tok/value]
]

; ══════════════════════════════════════════════════════════════════
; SECTION 5: METAPROGRAMMING — Homoiconic code manipulation
; ══════════════════════════════════════════════════════════════════

; Build a function dynamically from a spec
make-adder: func [n [integer!]] [
    func [x [integer!]] compose [x + (n)]
]
add5:  make-adder 5
add10: make-adder 10
print add5 3    ; → 8
print add10 3   ; → 13

; Inspect and modify a block (code as data)
code-block: [x: 10  y: 20  z: x + y]
print length? code-block    ; → 9 (tokens, not statements)

; Macro-style code generation
gen-setters: func [
    obj    [object!]
    fields [block!]
][
    foreach field fields [
        set in obj rejoin ["set-" field] func [v] compose [
            (to-set-word field) v
        ]
    ]
]

; ══════════════════════════════════════════════════════════════════
; SECTION 6: GUI — VID + Draw + Reactive System
; ══════════════════════════════════════════════════════════════════

; Counter application with reactive bindings
counter-value: 0

view [
    title "Red Architecture Demo"
    size 400x300

    ; Reactive text display — auto-updates when counter-value changes
    counter-display: text 200x30 "Count: 0" font-size 16

    ; Canvas with Draw dialect
    canvas: base 380x150 white draw [
        pen black  line-width 2
        circle 190x75 60
        pen blue   fill-pen sky
        circle 190x75 40
    ]

    ; Interactive controls
    across
    button "Increment" [
        counter-value: counter-value + 1
        counter-display/text: rejoin ["Count: " counter-value]
        ; Animate canvas reactively
        canvas/draw: compose [
            pen black  line-width 2
            circle 190x75 60
            pen blue   fill-pen sky
            circle (to-pair reduce [190 + counter-value 75]) 40
        ]
    ]
    button "Reset" [
        counter-value: 0
        counter-display/text: "Count: 0"
    ]
    button "Quit" [quit]
]
```

## XIV. Red/Cognition — Proposed Extension Layer

Based on the entire architectural analysis developed across this conversation, here is what the **Red/Cognition extension** would look like as a concrete Red implementation, built using Red's own dialect system — no new parser required, only new dialect evaluators:

```red
Red [
    Title: "Red/Cognition Prototype"
    Purpose: "Cognitive layer implemented as Red dialects"
]

; ══════════════════════════════════════════════════════════════════
; COGNITIVE TYPE EXTENSIONS
; Using Red's existing object! as the foundation
; ══════════════════════════════════════════════════════════════════

; Belief — an epistemic value with confidence and provenance
make-belief: func [
    content     [any-type!]
    confidence  [float!]    ; 0.0 to 1.0
    source      [word!]
][
    make object! [
        type:       'belief!
        content:    content
        confidence: confidence
        source:     source
        timestamp:  now
        valid?:     true
    ]
]

; Goal — declarative intent with quality contract
make-goal: func [
    purpose     [string!]
    spec        [block!]
][
    make object! [
        type:       'goal!
        purpose:    purpose
        spec:       spec
        status:     'pending
        created:    now
        confidence: 0.0
    ]
]

; ══════════════════════════════════════════════════════════════════
; MEMORY DIALECT
; ══════════════════════════════════════════════════════════════════

cognitive-memory: make object! [
    semantic:  make map! []
    episodic:  copy []
    working:   copy []
]

remember: func [block [block!] /with confidence c][
    c: any [c 1.0]
    parse block [
        set subj word! set pred word! set obj skip (
            entry: make-belief reduce [subj pred obj] c 'user
            put cognitive-memory/semantic
                rejoin [form subj "-" form pred]
                entry
        )
        | set fact skip (
            append cognitive-memory/episodic
                make-belief fact c 'observation
        )
    ]
]

recall: func [query [block! word! string!]][
    ; Semantic lookup
    case [
        word? query [
            collect [
                foreach [k v] cognitive-memory/semantic [
                    if find k form query [keep v]
                ]
            ]
        ]
        block? query [
            ; Pattern match against episodic memory
            collect [
                foreach ep cognitive-memory/episodic [
                    if ep/confidence > 0.5 [keep ep]
                ]
            ]
        ]
        true [cognitive-memory/semantic]
    ]
]

; ══════════════════════════════════════════════════════════════════
; GOAL DIALECT
; ══════════════════════════════════════════════════════════════════

; Goal dialect evaluator
eval-goal: func [
    goal-block [block!]
    /local step results
][
    results: copy []
    parse goal-block [
        any [
            'observe set target skip (
                print rejoin ["[OBSERVE] " target]
                append results reduce ['observed target]
            )
            | 'reason set spec block! (
                print "[REASON] Evaluating reasoning block"
                append results reduce ['reasoning do spec]
            )
            | 'plan set steps block! (
                print rejoin ["[PLAN] " length? steps " steps"]
                append results reduce ['plan steps]
            )
            | 'act set actions block! (
                print "[ACT] Executing actions"
                do actions
                append results 'acted
            )
            | 'reflect set reflection block! (
                print "[REFLECT] Processing reflection"
                append results reduce ['reflection do reflection]
            )
            | 'verify (
                print "[VERIFY] Checking outcomes"
                append results 'verified
            )
            | skip
        ]
    ]
    results
]

; ══════════════════════════════════════════════════════════════════
; AGENT DIALECT — The Complete Cognitive Loop
; ══════════════════════════════════════════════════════════════════

make-agent: func [
    name    [string!]
    spec    [block!]
][
    agent: make object! [
        agent-name:     name
        beliefs:        make map! []
        goals:          copy []
        memories:       cognitive-memory
        skills:         make map! []
        event-handlers: make map! []
        running:        false

        ; The core cognitive loop
        run-cycle: does [
            foreach [event handler] event-handlers [
                if triggered? event [
                    result: eval-goal handler
                    consolidate result
                ]
            ]
        ]

        triggered?: func [event [word!]][false]  ; override per agent
        consolidate: func [result [block!]][
            append memories/episodic
                make-belief result 0.8 agent-name
        ]
    ]

    ; Evaluate agent spec to configure the agent
    parse spec [
        any [
            'remember set mem block! (
                remember/with mem 1.0
            )
            | 'when set evt word! set handler block! (
                put agent/event-handlers evt handler
            )
            | 'skill set sk word! set impl block! (
                put agent/skills sk impl
            )
            | skip
        ]
    ]
    agent
]

; ══════════════════════════════════════════════════════════════════
; USAGE — Repository Assistant Agent
; ══════════════════════════════════════════════════════════════════

repo-assistant: make-agent "Repository Assistant" [

    remember [
        project "OpenClaw"
        language Rust
    ]

    skill summarize [
        func [content][
            print rejoin ["Summary of: " content]
        ]
    ]

    when push-event [
        observe repository
        reason [
            identify-changes
            estimate-impact
        ]
        plan [
            run-tests
            inspect-architecture
            summarize-changes
        ]
        act [
            generate-report
        ]
        reflect [
            compare-predictions
            remember lessons
        ]
    ]
]

; Demonstrate belief system
remember [server-host "localhost"]
remember/with [api-key "secret"] 0.9

beliefs: recall 'server
foreach b beliefs [
    print rejoin [
        "Belief: " b/content
        "  confidence: " b/confidence
        "  source: " b/source
    ]
]
```

## Summary — Red Architecture At a Glance

```
┌────────────────────────────────────────────────────────────────────┐
│             RED 2.0 COMPLETE ARCHITECTURE SUMMARY                  │
├─────────────────────────────┬──────────────────────────────────────┤
│  FOUNDATION                 │  Rebol-inspired, homoiconic          │
│                             │  Code = Data = Dialect               │
├─────────────────────────────┼──────────────────────────────────────┤
│  TOOLCHAIN                  │  Lexer → Parser → Compiler           │
│                             │  → Emitter → Linker → Encapper       │
│                             │  All in ~1MB self-contained binary   │
├─────────────────────────────┼──────────────────────────────────────┤
│  MEMORY MODEL               │  Series + Node-reference indirection │
│                             │  Mark-and-compact Simple GC          │
│                             │  16-byte tagged value representation │
├─────────────────────────────┼──────────────────────────────────────┤
│  TYPE SYSTEM                │  50+ native datatypes                │
│                             │  Typesets for polymorphic dispatch   │
│                             │  Action protocol on all types        │
├─────────────────────────────┼──────────────────────────────────────┤
│  DIALECTS (Built-in)        │  Red/System · Parse · VID            │
│                             │  Draw · Rich-text                    │
├─────────────────────────────┼──────────────────────────────────────┤
│  GUI SYSTEM                 │  face! tree + Reactive dataflow      │
│                             │  Cross-platform OS backends          │
├─────────────────────────────┼──────────────────────────────────────┤
│  TARGETS                    │  Windows/Linux/macOS/Android/ARM     │
│                             │  IA-32 · ARMv4-v7 · WASM (planned)  │
├─────────────────────────────┼──────────────────────────────────────┤
│  ROADMAP                    │  v1.0: Self-hosted + IR              │
│                             │  v2.0: JIT + 64-bit + Red/Cognition  │
├─────────────────────────────┼──────────────────────────────────────┤
│  COGNITIVE EXTENSION        │  goal! belief! plan! memory! skill!  │
│  (Proposed Red/Cognition)   │  Intent compiler + CIR + CVM        │
│                             │  Three-compiler pipeline             │
└─────────────────────────────┴──────────────────────────────────────┘
```

The architecture of Red is uniquely positioned for the cognitive computing trajectory developed throughout this conversation: its homoiconic block structure, zero-dependency toolchain, dialect-first design philosophy, and planned JIT and IR infrastructure in v2.0 provide exactly the substrate that a Red/Cognition cognitive layer requires. The `do` / `parse` / `compose` / `bind` primitives that make Red's dialect system work today are the same primitives that would power goal evaluation, plan manipulation, and intent compilation tomorrow — no architectural revolution required, only evolutionary extension upward.

---

**Traceability:** All content extracted verbatim from the ninth (final) user message. Every section, diagram, BNF grammar, code example, roadmap item, and architectural description has been preserved exactly as provided. No information added or inferred.