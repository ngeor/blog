---
layout: post
title: Learning QBasic part 1
date: 2020-08-08 07:20:58 +02:00
tags:
  - qbasic
  - rusty basic
---

I've been writing an interpreter for QBasic for quite some time now, since March
28th to be precise. This was something I always wanted to do. In the process, I
am learning Rust, which I like a lot. But, as I implement feature after feature,
I am learning QBasic as well, especially things a developer normally never has
to worry about.

## Dynamic Typing? Nope

The first misconception I had was that QBasic is a dynamic typed language. In
Ruby, you can do the following:

```ruby
i = 42
puts i
i = "is the answer"
puts i
```

The variable `i` gets first the numeric value 42 and then the string value "is
the answer".

In QBasic, that doesn't work. You can't re-assign a variable to a different
type. In fact, it goes a bit beyond that. The name of the variable dictates the
type of values it can hold.

```basic
A = 42      ' works
A = "oops"  ' does not work
```

In my interpreter, [rusty basic](https://github.com/ngeor/rusty-basic), I refer
to these variable names as **bare**. They consist of just letters and optionally
numbers, e.g. `A`, `B`, `Age`, `MysteriousVariable42`.

Side note: I figured out variable names in QBasic can also contain dots for
crying out loud, which I haven't supported yet.

By default, _bare_ names hold float values of single precision. So the
assignment `A = 42` is actually creating a single value. To create a different
variable, we need to use what I call in rusty basic a **qualified** name: a
variable name followed by a **type qualifier**. There are five such characters:

- `%` declares an integer
- `&` declares a long
- `!` declares a single (which is the default)
- `#` declares a double
- `$` declares a string

Some examples:

```basic
A% = 42
B& = 5653376574648
C! = 3.14
D# = 45644564.3353
E$ = "hello world"
```

When coding the interpreter, I often worry about edge cases. Things that a
developer wouldn't normally do, but out of curiosity I dive into. An example is,
what would happen if I define the same variable name with different type
qualifiers:

```basic
A% = 42
A$ = "the answer"
PRINT A%, A$
```

Will the above program work? Turns out it works just fine, as far as QBasic is
concerned, `A%` and `A$` are two different variables.

## Default type resolution

I mentioned that a bare variable holds a single float value by default. Consider
the following program:

```basic
A = 41
A! = A! + 1
PRINT A
```

It prints 42. As the `A` variable is a single, it is resolved to `A!`. `A` and
`A!` are the same variable.

It is possible to change the default type to one of the other 4 types with the
keywords `DEFINT` (for integers), `DEFLNG` (for longs), `DEFDBL` (for doubles)
and `DEFSTR` (for strings). There's also of course `DEFSNG` for singles. In
fact, in the games that came with QBasic, Gorillas and Nibbles, the first
statement in the game is:

```basic
' Set default data type to integer for faster game play
DEFINT A-Z
```

The above statement says that any variable that starts with a letter between A
and Z (so all variables) is an integer. I don't know why integers aren't the
default to begin with, might be some backwards compatibility issue with an even
older BASIC flavor.

If we use this statement in the above program:

```basic
DEFINT A-Z
A = 41
A! = A! + 1
PRINT A
```

It will print 41 instead. Now we have two variables `A` (which is now an
integer, so `A%`) and `A!`.

In rusty-basic, I have a layer called "linting" which sits between getting the
parse tree and generating instructions. Among other things, the linter makes
sure that all bare names are resolved to qualified names and that there are no
mismatch types or duplicate definitions.

## Making it more complicated: DIM A AS STRING

I'm currently in the process of implementing the `DIM` statement. With `DIM`,
you can declare a variable without an assignment. It's even possible to declare
arrays and user defined types, but I haven't gone that far in implementation.

There's two ways you can declare a variable with `DIM`. The one is exactly the
same as seen so far:

```basic
DIM A
DIM A$
A = 42
PRINT A!
A$ = "the answer"
PRINT A$
```

The program works fine. The variable `A` is a bare variable resolved to a single
(so it's the same as `A!`) and `A$` is a different variable.

It gets complicated when using the second way of declaring a variable:

```basic
DIM A AS INTEGER
A = 42
PRINT A
```

The keywords that match the five data types are `INTEGER`, `LONG`, `SINGLE`,
`DOUBLE` and `STRING`.

For the lack of a better name, I call this an **extended** variable (naming
things is hard) while I call the variables seen earlier as **compact**. It's
important to flag this as something special in the interpreter because it
follows different naming resolution rules.

An extended variable cannot coexist with other variables of the same bare name.
The following throw a _duplicate definition_ error:

Trying to use the same extended variable with different type (this one makes
sense):

```basic
DIM A AS INTEGER
DIM A AS STRING
```

Trying to use an extended integer with a bare compact (which should be single):

```basic
DIM A AS INTEGER
DIM A
```

Trying to use an extended integer with a compact string:

```basic
DIM A AS INTEGER
DIM A$
```

Trying to use an extended integer with an implicit compact string on assignment:

```basic
DIM A AS INTEGER
A$ = "hello"
```

Side note: every such edge case discovery has become a unit test in rusty basic.

You could argue at least the latter might be something the interpreter should
allow, given it allows it for compact style variables, but it doesn't.

The next difference is that `A` now is resolved to `A%` (as it declared as an
integer), bypassing the default type resolution rules:

```basic
DIM A AS INTEGER
A% = 42
PRINT A
```

So it's still possible to use a type qualifier, as long as it matches the type
declared at the `DIM` statement.

Again, these are all probably things that a developer wouldn't do. It would be
also tempting on my side to just say "a variable must be unique, throw an error
otherwise" and call it a day. But I'm curious to discover how it is supposed to
work.
