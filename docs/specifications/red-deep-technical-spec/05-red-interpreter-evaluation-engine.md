# XV. The Red Interpreter — Internal Evaluation Architecture

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│           RED INTERPRETER — EVALUATION ENGINE                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  INPUT: any Red block or expression                                  │
│                                                                      │
│  ┌───────────────────────────────────────────────────────────┐      │
│  │              EVALUATOR DISPATCH TABLE                      │      │
│  │                                                            │      │
│  │  Value Type         │  Evaluation Rule                    │      │
│  │  ─────────────────  │  ──────────────────────────────     │      │
│  │  integer!           │  Self-evaluating → return as-is     │      │
│  │  float!             │  Self-evaluating → return as-is     │      │
│  │  string!            │  Self-evaluating → return as-is     │      │
│  │  logic!             │  Self-evaluating → return as-is     │      │
│  │  none!              │  Self-evaluating → return as-is     │      │
│  │  char!              │  Self-evaluating → return as-is     │      │
│  │  binary!            │  Self-evaluating → return as-is     │      │
│  │  block!             │  Self-evaluating → NOT executed     │      │
│  │                     │  (use DO to evaluate)               │      │
│  │  paren!             │  IMMEDIATELY evaluated              │      │
│  │  word!              │  Lookup in context → evaluate       │      │
│  │  set-word!          │  Evaluate RHS → bind in context     │      │
│  │  get-word!          │  Fetch value WITHOUT evaluating     │      │
│  │  lit-word!          │  Return word! itself (quoted)       │      │
│  │  path!              │  Navigate series/object path        │      │
│  │  set-path!          │  Navigate path → set target         │      │
│  │  get-path!          │  Navigate path → get without call   │      │
│  │  function!          │  Call with next N arguments         │      │
│  │  native!            │  Built-in call (C-level)            │      │
│  │  op!                │  Infix: evaluate left, then right   │      │
│  └───────────────────────────────────────────────────────────┘      │
│                                                                      │
│  ┌───────────────────────────────────────────────────────────┐      │
│  │              EVALUATION SEQUENCE RULES                     │      │
│  │                                                            │      │
│  │  1. Read next value from current block position            │      │
│  │  2. Dispatch on value type (table above)                   │      │
│  │  3. If function!/native!/action!:                          │      │
│  │       a. Collect N arguments (recursively evaluate each)   │      │
│  │       b. Check refinements                                 │      │
│  │       c. Bind arguments to function spec context           │      │
│  │       d. Evaluate function body                            │      │
│  │       e. Return result                                     │      │
│  │  4. If op! (infix):                                        │      │
│  │       a. Left operand = last evaluated result              │      │
│  │       b. Right operand = next evaluation                   │      │
│  │  5. Advance block position                                 │      │
│  │  6. Repeat until block end                                 │      │
│  └───────────────────────────────────────────────────────────┘      │
│                                                                      │
│  KEY PROPERTY: No operator precedence.                               │
│  Evaluation is strictly LEFT-TO-RIGHT.                               │
│                                                                      │
│    2 + 3  *4  → (2 + 3)*  4 → 20    ; NOT 14                       │
│                                                                      │
│  Use parentheses (paren!) for explicit grouping:                     │
│    2 + (3  *4) → 14                                                  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```