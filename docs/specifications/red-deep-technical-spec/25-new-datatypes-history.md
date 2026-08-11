# XXXII. New Datatypes — Complete History Through 0.6.6

```ascii
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