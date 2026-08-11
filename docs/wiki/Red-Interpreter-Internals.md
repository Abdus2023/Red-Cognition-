# Red Interpreter — Internal Evaluation Architecture

**Source Message:** Ninth user message — Section XV

**Stable ID:** RED-SPEC-015

## Overview

Red's runtime library is written in Red/System, and uses a hybrid approach: it compiles what it can deduce statically and uses an embedded interpreter otherwise. The project roadmap includes a just-in-time compiler for cases in between, but this has not yet been implemented.

The interpreter is the dynamic evaluation path. Understanding it precisely requires examining the evaluation rules, word types, and context binding system in sequence.

## Evaluator Dispatch Table

| Value Type     | Evaluation Rule                                      |
|----------------|------------------------------------------------------|
| integer!       | Self-evaluating → return as-is                       |
| float!         | Self-evaluating → return as-is                       |
| string!        | Self-evaluating → return as-is                       |
| logic!         | Self-evaluating → return as-is                       |
| none!          | Self-evaluating → return as-is                       |
| char!          | Self-evaluating → return as-is                       |
| binary!        | Self-evaluating → return as-is                       |
| block!         | Self-evaluating → NOT executed (use DO to evaluate)  |
| paren!         | IMMEDIATELY evaluated                                |
| word!          | Lookup in context → evaluate                         |
| set-word!      | Evaluate RHS → bind in context                       |
| get-word!      | Fetch value WITHOUT evaluating                       |
| lit-word!      | Return word! itself (quoted)                         |
| path!          | Navigate series/object path                          |
| set-path!      | Navigate path → set target                           |
| get-path!      | Navigate path → get without call                     |
| function!      | Call with next N arguments                           |
| native!        | Built-in call (C-level)                              |
| op!            | Infix: evaluate left, then right                     |

## Evaluation Sequence Rules

1. Read next value from current block position
2. Dispatch on value type (table above)
3. If function!/native!/action!:
   - Collect N arguments (recursively evaluate each)
   - Check refinements
   - Bind arguments to function spec context
   - Evaluate function body
   - Return result
4. If op! (infix):
   - Left operand = last evaluated result
   - Right operand = next evaluation
5. Advance block position
6. Repeat until block end

**KEY PROPERTY:** No operator precedence. Evaluation is strictly LEFT-TO-RIGHT.

```
2 + 3 * 4  → (2 + 3) * 4 → 20    ; NOT 14
```

Use parentheses (paren!) for explicit grouping:

```
2 + (3 * 4) → 14
```

---

**Traceability:** All content extracted verbatim from Section XV of the ninth user message. No information added or inferred.