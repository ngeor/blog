---
title: String functions (QBasic)
layout: page
tags:
  - QBasic Reference
---

## ASC

`ASC` returns the ASCII code for the first character in a string expression.

`ASC(stringexpression$)`

### Example

```bas
PRINT ASC("Q") ' Output is 81
```

## CHR$

`CHR$` returns the character corresponding to a specified ASCII code.

`CHR$(ascii-code%)`

### Example

```bas
PRINT CHR$(65) ' Output is A
```
