---
title: Math functions (QBasic)
layout: page
tags:
  - QBasic Reference
---

## ABS

`ABS` calculates the absolute value of the given number.

### Example

```bas
PRINT ABS(3)  ' Output is 3
PRINT ABS(-4) ' Output is 4
```

## ATN

`ATN` returns the arctangent of the given numeric expression.

The `ATN` function returns an angle in radians. To convert from
degrees to radians, multiply degrees by (PI / 180).

### Example

```bas
CONST PI=3.141592654
PRINT ATN(TAN(PI/4.0)), PI/4.0
' Output is: .7853981635 .7853981635
```

## SGN

`SGN` returns a value indicating the sign of a numeric expression:

- 1 if the the argument is positive
- 0 if the argument is zero
- -1 if the argument is negative

### Example

```bas
PRINT SGN(3)    ' Output is 1
PRINT SGN(0)    ' Output is 0
PRINT SGN(-2.1) ' Output is -1
```
