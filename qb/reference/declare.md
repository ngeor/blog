---
title: DECLARE statement (QBasic)
layout: page
tags:
  - QBasic Reference
---

## DECLARE statement

Declares a `FUNCTION` or `SUB` procedure and invokes argument data type checking.

`DECLARE {FUNCTION | SUB} name [([parameterlist])]`

- `name`: The name of the procedure.
- `parameterlist`: One or more variables that specify parameters to be passed to the procedure when it is called:

  `variable[()] [AS type] [, variable[()] [AS type]]...`
  - `variable`: A Basic variable name.
  - `type`: The data type of the variable (`INTEGER`, `LONG`, `SINGLE`, `DOUBLE`, `STRING`,
    or a user-defined data type). `ANY` allows any data type.

`DECLARE` is required if you call `SUB` procedures without `CALL`.
QBasic automatically generates `DECLARE` statements when you save your program.
