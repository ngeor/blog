---
layout: post
title: Learning QBasic part 2
date: 2020-11-30 08:50:25 +02:00
tags:
  - qbasic
  - rusty basic
use_mermaid: true
---

This is the 2nd part of learning QBasic, still figuring out how QBasic works in
order to write an interpreter for it.

Quick-ish summary of what was covered in the [previous post]:

- **5 types**. There are 5 built-in types: integer, long, single, double, string
  (so 4 numeric types and one type for strings).
- **Implicit & explicit variables**. A variable can be explicitly declared with
  the `DIM` statement, but it can also be implicitly declared simply by using it
  (e.g. `A = 42`).
- **Compact and extended DIM**. A variable declaration can specify the type with
  the `AS type` clause, in which case I call it _extended_. Example:
  `DIM A AS STRING`. If it's without the `AS type` clause, I call it _compact_.
  Example: `DIM A`, `DIM A$`. Implicit variables are by definition compact.
- **Bare and qualified variables**. A variable name can be optionally followed
  by a _type qualifier_ to indicate its type. The qualifiers are `%` for
  integer, `&` for long, `!` for single, `#` for double, and `$` for string.
  Example: `Msg$ = "Hello, world!"`.
- **Resolving type**. The type of a bare compact variable is determined by its
  name (in all other cases the type is known). The default type is single. The
  `DEFxxx` statements can change the default, based on the first letter of the
  variable name (e.g. a common idiom is `DEFINT A-Z` to make all bare compact
  variables integers).

You can read the [previous post] for a bit more context on how all these behave
on edge cases.

## More on the numeric types

The `LEN` built-in function can be used to measure the size of a variable. For
the built-in numeric types, it shows how many bytes they use. For the string
type, it shows the length of the string. Let's use it to see how big the
built-in types are:

```vb
PRINT "Size of integer is:", LEN(A%)
PRINT "Size of long is:", LEN(B&)
PRINT "Size of single is:", LEN(C!)
PRINT "Size of double is:", LEN(D#)
```

This will print out 2 for integer (16 bits), 4 for long (32 bits), 4 for single
and 8 for double (64 bits). For the two integer types, the minimum and maximum
represented values are:

| Type    |            Min |           Max |
| ------- | -------------: | ------------: |
| Integer |        -32,768 |        32,767 |
| Long    | -2,147,483,648 | 2,147,483,647 |

Side note: In the current implementation of rusty basic, I use 32 and 64 bit
types internally ([i32](https://doc.rust-lang.org/std/primitive.i32.html) and
[i64](https://doc.rust-lang.org/std/primitive.i64.html)) and the min-max limits
for each type is enforced programmatically. This might change in the future.

### Literal types

Given the min-max values described above, consider the following program:

```vb
PRINT 32767     ' max int
PRINT 32768
PRINT 32767 + 1 ' oops!
PRINT 32768 + 1
```

The program gives an overflow error on the third line. This might be
counterintuitive. If it can print the value 32,768 on the second line, why can't
it print 32,767 + 1? It's discoveries like these that shed some light on how
QBasic evaluates expressions under the hood (and help me with re-implementing
them in rusty basic). What (probably) happens is that QBasic tries to use the
**smaller type that can hold the literal expression**. On the first line, it
sees 32,767 and it stores it in a integer as it fits. On the second line, it
uses a long type. On the third line, there are two values which both fit in the
integer type on their own. Then, at runtime, it tries to add two integer values
together, leading to an overflow as the result doesn't fit anymore.

It is possible to qualify a number with a type qualifier to be explicit about
its intended type (I haven't fully implemented this in rusty basic yet):

```vb
'PRINT 32767 + 1 ' overflow error!
PRINT 32767& + 1 ' works
```

## Constants

QBasic supports constants with the `CONST` statement, e.g. `CONST Answer = 42`.
What we've discussed so far regarding variable names and types goes a bit
different for constants.

### Type comes from the right side

For bare constants, i.e. where the name isn't followed by a type qualifier, it
is the constant value that determines the type of the constant. In the statement
`CONST A = 42`, the type of A will be an integer, despite the fact that we
haven't added `DEFINT A-Z` in the program. We can even do `CONST A = "hello"`.
It is the type of the right hand expression that determines the type of the
constant.

Let's see this with an example:

```vb
DEFINT A-Z      ' bare variables are integers
A = 32768       ' overflow!
CONST B = 32768 ' allowed, B is long
```

In the variable `A`, the type is derived from the name. We have a `DEFINT A-Z`
statement, which means any unqualified variable starting with a letter A-Z (so
all variables) is an integer. Since A is an integer, assigning the value 32768
to it results to an overflow error, as it doesn't fit the integer type. For `B`
however, the type is determined by the const value. The smallest type that can
accommodate 32768 is long, so B becomes a long constant.

### Constants always follow extended naming rules

We saw in the [previous post] that it's possible to do this with compact style
variables:

```vb
DIM A$
DIM A%
A$ = "The answer is"
A% = 42
PRINT A$, A%
```

but not with extended style variables:

```vb
DIM A AS STRING
DIM A% ' duplicate definition!
```

Constants behave always like extended style variables in this case, even though
they can only be declared in the compact style (there is no such thing as
`CONST A AS STRING = "hello"`).

So if we have a constant with `CONST Msg = "Hello"` (or even
`CONST Msg$ = "Hello"`):

- `Msg` and `Msg$` are both valid ways to reference that constant
- It is not possible to reference `Msg` with any other qualifier, e.g. `Msg%`
  gives a _duplicate definition_ error
- It is not possible to declare a variable named `Msg` (with or without
  qualifier)
- Within the same sub-program, it is not possible to declare another constant
  named `Msg` (with or without qualifier). It is possible however to re-define a
  constant within a sub-program (because why not):

  ```vb
  CONST Msg = "hi"
  PRINT Msg ' prints hi
  Greetings ' prints 42

  SUB Greetings
    ' shadow global constant with a local constant
    CONST Msg = 42
    PRINT Msg
  END SUB

  SUB Oops
    ' error: cannot shadow global constant with a variable
    DIM Msg$
  END SUB
  ```

## Wrap up

While writing rusty basic, one of the most challenging things was to identify
what a name is, and do it in the same way QBasic does. This is what we have so far:

### Defining a constant

- Type determined by value, not from name
- Cannot co-exist with constant or variable of the same name, qualified or unqualified
- Can shadow global constant inside subprogram (`FUNCTION` or `SUB`)

<div class="mermaid">
graph TD
A[CONST A = 42] --> B{constant exists in scope?}
B --> |Yes| DD[Duplicate definition]
B --> |No| C{variable exists in scope?}
C --> |Yes| DD
C --> |No| S[Success]
</div>

### Defining an extended variable

- Type provided by `AS type` clause
- Cannot co-exist with constant of the same name, qualified or unqualified, local or global
- Cannot co-exist with variable of the same name, qualified or unqualified

<div class="mermaid">
graph TD
A[DIM A AS STRING] --> B{const exists in *any* scope?}
B --> |Yes| DD[Duplicate definition]
B --> |No| C{variable exists in scope?}
C --> |Yes| DD
C --> |No| S[Success]
</div>

### Defining a compact variable

- Type provided by qualifier if qualified, resolved by name if bare (affected by `DEFxxx` statements)
- Cannot co-exist with constant of the same name, qualified or unqualified, local or global
- Cannot co-exist with extended variable of the same name
- Can co-exist with compact variables of the same name and different type

<div class="mermaid">
graph TD
A[DIM A$] --> B{const exists in *any* scope?}
B --> |Yes| DD[Duplicate definition]
B --> |No| C{extended variable exists in scope?}
C --> |Yes| DD
C --> |No| E{compact variable A$ exists in scope?}
E --> |Yes| DD
E --> |No| S[Success]
</div>


[previous post]: {% post_url 2020/2020-08-08-learning-qbasic %}
