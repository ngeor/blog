---
layout: post
title: clang-format as a git filter
date: 2019-01-27
published: true
categories:
  - Code
tags:
  - java
  - clang-format
  - git
---

[clang-format] is a tool that can format source code of C-like languages
(C/C++/Java/JavaScript/Objective-C/Protobuf). It supports various presets but it
is also possible to fine tune its behavior with a configuration file named
`.clang-format`. It has quite a lot [configuration
options](https://clang.llvm.org/docs/ClangFormatStyleOptions.html).

In this post, I'm showing how to use this tool as a git filter in order to
automatically format Java code when committing code to git. The inspiration
comes from [these
examples](https://git-scm.com/book/en/v2/Customizing-Git-Git-Attributes) in the
Git documentation and by tools like [prettier ](https://prettier.io/) from the
JavaScript ecosystem.

First of all, you need to have the `clang-format` program somewhere in your
`PATH`. You can get it [here](http://releases.llvm.org/download.html). For
Windows, there is a
[bundle](http://releases.llvm.org/7.0.1/LLVM-7.0.1-win64.exe) containing various
tools. Just unzip it with 7zip and keep only the `bin/clang-format.exe` file.

Next, you'll need to define your style preferences. Mine currently look like this:

```
BasedOnStyle: LLVM

AccessModifierOffset: -4
AlignConsecutiveAssignments: true
AlignConsecutiveDeclarations: false
AlignOperands: true
AlignTrailingComments: true
AllowAllParametersOfDeclarationOnNextLine: false
AllowShortBlocksOnASingleLine: false
AllowShortCaseLabelsOnASingleLine: false
AllowShortFunctionsOnASingleLine: None
AllowShortIfStatementsOnASingleLine: false
AllowShortLoopsOnASingleLine: false
BinPackArguments: false
BinPackParameters: false
BreakAfterJavaFieldAnnotations: true
BreakBeforeBinaryOperators: NonAssignment
BreakBeforeBraces: Attach
ColumnLimit: 120
ContinuationIndentWidth: 4
IndentCaseLabels: true
IndentWidth: 4
SortIncludes: false
SpaceAfterCStyleCast: true
TabWidth: 4
UseTab: Never
```

You can start with a preset and play with it until it is what you like.

In order to find the style options, clang-format searches for a file called
`.clang-format` at the current directory. When it can't find it, it continues
the search recursively to parent directories. This means that if you keep your
git repositories under a common folder, you can store the `.clang-format` file
at the root. And if a project needs different settings, you can always override.

At this point you can experiment with `clang-format` from the command line to
see how it works. There are also plugins for IDEs that use it.

Now, the fun part. We'll setup a git repository to automatically format Java
files with clang-format. You need a `.gitattributes` file on your repository
(see [documentation](https://git-scm.com/docs/gitattributes)). There, you
specify that java files will go through the `clang-format-java` filter:

```
*.java filter=clang-format-java
```

Note that git doesn't know anything about this, so we need to define what that filter does. Run the following commands:

```sh
git config --global filter.clang-format-java.clean 'clang-format -assume-filename=test.java'
git config --global filter.clang-format-java.smudge cat
```

A filter has two operations, clean and smudge. Clean happens when files are
staged, smudge when files are checked out.

When files are staged, we run `clang-format -assume-filename=test.java`. The
`-assume-filename` parameter helps clang-format to understand we're formatting a
Java file. This is needed because the input is received from the stdin and there
is no filename information available.

The effect is that when we're staging files (e.g. with `git add`) what is staged
goes first through clang-format and gets "cleaned" (hence the name of the clean
operation).

The smudge operation `cat` simply outputs the clean file as-is.

Note that the `.gitattributes` file is part of the git repository, while the
filter definition is part of the git configuration. If someone uses the
repository without having configured the filter, git will not give an error.
It's a good idea to add the commands that setup the filters in a readme or as
comments in the `.gitattributes` file, e.g.:

```
# To enable the custom clang-format-java filter, you need to run:
# git config --global filter.clang-format-java.clean 'clang-format -assume-filename=test.java'
# git config --global filter.clang-format-java.smudge cat
*.java filter=clang-format-java
```

[clang-format]: https://clang.llvm.org/docs/ClangFormat.html
