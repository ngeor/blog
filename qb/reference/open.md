---
title: OPEN statement (QBasic)
layout: page
tags:
  - QBasic Reference
---

Opens a file.

## OPEN statement ACCESS clause

`ACCESS { READ | WRITE | READ WRITE }`

- `READ`: Opens a file for reading only.
- `WRITE`: Opens a file for writing only.
- `READ WRITE`: Opens a file for both reading and writing.
  `READ WRITE` mode is valid only for random access and binary mode files,
  and files opened for `APPEND` (sequential access).

## OPEN statement file modes

- `APPEND`: specifies that the file is to be opened for
  sequential output and sets the file pointer to the end of the file.
- `BINARY`: specifies a binary file mode. In binary mode, you can read
  or write information to any byte position in the file using `GET` or `PUT`
  statements.
- `INPUT`: specifies that the file is opened for sequential input.
- `OUTPUT`: specifies that the file is opened for sequential output.
- `RANDOM`: specifies that the file is opened for random access file mode.
  `RANDOM` is the default file mode.
