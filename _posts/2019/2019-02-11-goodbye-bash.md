---
layout: post
title: Goodbye bash
date: 2019-02-11
published: true
tags:
  - bash
  - python
  - ruby
  - scripting
---

Having written my fair share of bash scripts last year, I decided to replace it
with something else. This is how I decided to replace it with Python.

The scripts I'm referring to are either running during the build (or deployment)
at the CI server or they're small scripts that I use on my laptop. The primary
factor in choosing bash in the first place was that the builds run inside Docker
containers, which all have one thing in common: bash.

And there's nothing wrong with that, as long as the scripts are small. But, if
they start to become larger and more complex, things become a bit more
challenging. Bash is great for glueing together other commands like lego blocks.
If all it takes is to run a few commands and maybe do some text filtering with
`grep` or replacing with `sed`, it's all fine.

I found bash a bit unsatisfying in the following cases:

- Dealing with structured text files (xml, json, yaml). Coming up with a correct
  regular expression for `sed` in this case is like trying to use a hammer with
  as a screw driver.
- I never remember when to use `[ ]`, `[[ ]]`, `( )` or `(( ))`. Maybe I'm
  forgetting some combination? A [cheatsheet](https://devhints.io/bash) goes a
  long way, but the code is just not readable. You want the basics of a language
  to be intuitive.

So, following the recent internet trend, it's time to apply the
[KonMari](https://en.wikipedia.org/wiki/Marie_Kondo) method. Bash doesn't spark
joy. Thank you bash for all the automatic deployments, but it's time to throw
you away.

But what should I replace it with? I gave this a lot of thought in the past
months and I went back and forth between some options.

First of all, I excluded compiled languages. We're still talking about small
scripts that should fit in a single file. There's no need for the overhead of
having to compile it and run the binary. Just plain old write, run, edit,
repeat.

I considered several options: Python, Ruby, nodeJS with JavaScript or
TypeScript, Groovy, Beanshell.

The last two aren't really as popular as the rest but I thought to give them a
try because at work our stack is mostly Java. I wasn't impressed, it felt like
Java with different shoes and Java can be a bit too verbose.

A side note on popularity: you've probably seen the
[TIOBE Index](https://www.tiobe.com/tiobe-index/) that lists the popularity of
programming languages. I was baffled by it because it lists C and C++ so high,
or VB .net more popular than C#. I found instead GitHub's
[State of the Octoverse](https://octoverse.github.com/projects) to be a bit more
believable (hurray for my confirmation bias).

nodeJS was also rejected. I have enough experience with JavaScript and
TypeScript and JavaScript is the most popular language (with TypeScript climbing
high). However, these scripts would typically have to run commands and deal with
files, which means having to write a lot of `async`-`await` all the time. It's
also an ecosystem that moves a bit too fast for my taste.

This leaves us with Python and Ruby. I was a bit sad to see that Ruby seems to
be constantly falling in popularity. I never used it professionally but I played
with it and I found its language constructs very interesting. I also liked
Python a lot, so in this case I decided to go with the crowd. According to both
TIOBE and GitHub's reports it's quite popular. The days of the Python 2 vs
Python 3 schism are behind us (although you need to be careful you're reading a
recent StackOverflow answer). Visual Studio Code has great support for it (I
have to say it's better than Ruby's support). And it has gained a new wave of
popularity, as it's used by the AI/Machine Learning folks.

I had put together a rather complicated bash script which was generic enough to
handle deployments for all of our projects at work, but it had reached its
limits in terms of maintainability. I managed to rewrite it in Python in a few
hours. It is slightly longer (from 152 to 179 lines) than the bash script, but
it's significantly more readable, robust and generic. But the emphasis here is
that this was possible in a few hours and I'm not exactly a Python guru.
