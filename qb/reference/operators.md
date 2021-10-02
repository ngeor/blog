---
title: Operators (QBasic)
layout: page
tags:
  - QBasic Reference
---

## Boolean operators

- `NOT`: bit-wise complement
- `AND`: conjunction
- `OR`: disjunction (inclusive "or")
- `XOR`: exclusive "or"
- `EQV`: equivalence
- `IMP`: implication

| Left expression | Right expression | `NOT` | `AND` | `OR` | `XOR` | `EQV` | `IMP` |
|-----------------|------------------|:-----:|:-----:|:----:|:-----:|:-----:|:-----:|
| T               | T                | F     | T     | T    | F     | T     | T     |
| T               | F                | F     | F     | T    | T     | F     | F     |
| F               | T                | T     | F     | T    | T     | F     | T     |
| F               | F                | T     | F     | F    | F     | T     | T     |

- Boolean operators are performed after arithmetic and relational operations in order of precedence.
- Expressions are converted to integers or long integers before a Boolean operation is performed.
- If the expressions evaluate to 0 or -1, a Boolean operation returns 0 or -1 as the result.
  Because Boolean operators do bit-wise calculations, using values other than 0 for false and
  -1 for true may produce unexpected results.
