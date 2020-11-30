---
layout: post
title: Inside rusty basic part 1
tags:
  - rusty basic
---

Time to talk about how rusty-basic is built.

[rusty-basic] is a [QBasic] hobby interpreter I started coding in March 2020.
With this project, I'm primarily learning and practicing [rust]. I'm solving the
problem of writing an interpreter, something I always wanted to do. And I'm
reverse engineering the quirks of QBasic, in order to make rusty-basic faithful
to it, in the happy flow as well as in the edge cases.

An interpreter is supposed to take a program, such as `PRINT "Hello, world"` and
somehow make these words appear on the console. In rusty-basic, this is
accomplished with four main components:

- **Parser**: Reads a program and returns an [abstract syntax tree] (AST).
  Performs very few sanity checks. Supports reading from a file but also from a
  string (useful for the unit tests). The AST retains source code comments and,
  important for reporting errors to the user, the row and column of the parsed
  elements within the program.
- **Linter**: Validates and transforms the AST of the parser into a new one.
  Performs the bulk of the sanity checks and figures out things like is `A(1)` a
  function call or an array element.
- **Instruction generator**: Converts the AST into a flat list of
  [assembly]-like instructions that can be executed by the interpreter (the next
  step). Some example instructions are `LoadIntoA`, which loads a value into the
  register A, `Plus`, which adds registers A and B together storing the result
  into A, and `JumpIfFalse`, which jumps to an "address" if register A holds the
  value zero.
- **Interpreter**: Runs the instructions one by one. It also holds the
  implementation of built-in functions / subs of QBasic, e.g. the `LEN` function
  which calculates the size of a variable, the `ENVIRON$` which gets an
  environment variable, and, naturally, the `PRINT` statement. Built with
  testability in mind, certain parts can be replaced with mocks, e.g. there is a
  stdio component that deals with standard input, standard output, and, because
  this is QBasic and the early 90s,
  [LPT1](https://en.wikipedia.org/wiki/Parallel_port).

Regarding how much time I've spent on it, I stopped spending time on other home
projects and decided to stick with it until it can run a simple program. I think
I coded almost every day for an hour or so, with more time in the weekends. As I
was also studying rust, I didn't look for any external dependency I could use to
save time (the [nom](https://github.com/Geal/nom) library looks like it could
have saved me quite some time).

I was using Visual Studio Code but I've switched recently to IntelliJ IDEA,
which is much faster in autocomplete and has all the productivity refactorings.
I still have Visual Studio Code on the side to debug if needed (IntelliJ IDEA,
at least the community edition, can only run tests, not debug them).

Speaking of tests, I only test the four main components I described above as
black boxes. Testing the final component, the interpreter, is basically testing
the whole thing. I don't add tests for the many smaller parts that comprise
these components, even though I could do that (with very few exceptions). This
has allowed me to rewrite a lot of code I felt was confusing or could be
improved without having to rewrite its accompanying unit tests (and at the same
time I had all the safety from the component tests). The most pronounced case
was when I rewrote the parser implementation to use
[parser combinators](https://en.wikipedia.org/wiki/Parser_combinator).

In the next posts, I'll describe more details about the design and
implementation of rusty-basic.

[rusty-basic]: https://github.com/ngeor/rusty-basic
[qbasic]: https://en.wikipedia.org/wiki/QBasic
[rust]: https://www.rust-lang.org/
[abstract syntax tree]: https://en.wikipedia.org/wiki/Abstract_syntax_tree
[assembly]: https://en.wikipedia.org/wiki/Assembly_language
