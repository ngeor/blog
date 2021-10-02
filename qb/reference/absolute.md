---
title: CALL ABSOLUTE Statement (QBasic)
layout: page
tags:
  - QBasic Reference
---

## CALL ABSOLUTE

Transfers control to a machine-language procedure.

`CALL ABSOLUTE ([argumentlist,] offset%)`

- `argumentlist`: Arguments passed to a machine-language procedure
  as offsets from the current data segment.
- `offset%`: The offset from the current code segment, set by `DEF SEG`,
  to the starting location of the procedure.

Example:

```bas
' Calls routine for printing the screen to a local printer.
DIM a%(2)
DEF SEG = VARSEG(a%(0))
FOR i% = 0 TO 2
  READ d%
  POKE VARPTR(a%(0)) + i%, d%
NEXT i%
DATA 205, 5, 203 : ' int 5 retf ' Machine-language code
                                ' for printing screen.
CALL ABSOLUTE(VARPTR(a%(0)))
DEF SEG
```
