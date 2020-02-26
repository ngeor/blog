---
layout: post
title: Flaky tests
date: 2019-07-29
published: true
categories:
  - tech
tags:
  - javascript
  - typescript
  - angular
  - protractor
  - browser tests
---

A flaky test is a test that can flip from success to failure without any code change.
Such failures can be annoying and difficult to diagnose. In this post, I'll focus on
browser tests, where flaky tests can happen more often.

A senior QA engineer once told me what he used to tell his team:

- Senior QA: Is your test green?
- Junior QA: Yes
- S: How many times did you run it?
- J: Um... once?
- S: Run it a hundred times and then come back to me.

What the junior QA would discover is that the test was green... mostly. Sometimes, it would be red.
This is where we can have a closer look on the test and see why it's unstable.


## Element not visible / clickable etc

This is probably the easiest to understand. The test loads a page, which might take some time. When
you try to interact with an element on the page, it is quite possible that it hasn't been rendered yet.

The best way to deal with this is to wait until the element is visible. The library that controls the browser
should offer such a method in order to efficiently wait until a condition is met. When the page renders fast,
the waiting time will be short.

The bad practice here is to wait for a fixed amount of time instead of waiting for a condition. The amount of
time might not suffice if the page happens to be a bit slower than usual, so we're back to a flaky test. And if
the page happens to be faster than usual, we're waisting time waiting for nothing.

## Asynchronous code bugs

This is specific to JavaScript when writing tests requires using promises or async/await. It is possible to make
a mistake and call a function that returns a promise without awaiting it. This can easily lead to a flaky test.

Careful code reviews help catching these problems. As this pitfall typically leads to an evergreen test,
try to validate your test does what it is supposed to be doing by trying to make it fail. If the test stays
green no matter what, you might be missing an `await` keyword.

## Animations

Animations can be responsible for brittle tests. If an animation takes a bit longer to complete, the animated
element might moving or resizing within the page. A test that tries to interact with that element (e.g. click it)
might fail. A typical error message in this case mentions that "another element would receive the click event".

Please note that this might affect even animations that render very fast on your local computer. Things might
run slower on the CI server (and they most likely will).

The technique I use here is a custom workaround, as I don't know an out of the box way to wait for an element
to stop moving or resizing. I get the location and size of the element that I expect that will be animated.
I wait a few milliseconds (e.g. 50-100). I get the location and size again. If they differ, the element's
animation is still in progress.

## Timeout

This is specific to Angular/Protractor/Jasmine but might apply to other frameworks. It is not possible for these
frameworks to know if your test is slow or stuck. After a certain [timeout](https://github.com/angular/protractor/blob/master/docs/timeouts.md),
the tests fail.

This might be because a test is doing too many things, which on a slower day takes longer to execute. Breaking the
test down to smaller parts might help not only the stability but also the readability of the code.

## Reproducing flaky tests

A common frustration with flaky tests is that they're difficult to reproduce locally. They might fail or pass on the CI server,
but they always pass locally.

Instability might be caused by one test affecting another. This shouldn't happen of course. When you're debugging a test
locally, keep in mind that in order to reproduce the failure you might need to run it together with other tests.

A good test does not interfere with other tests. It can run alone, or with other tests, in any order.

Another reason that tests fail on the CI server but not locally is the better performance of your computer. The CI server
typically will be slower, which will increase the chance of a flaky test. To reproduce that locally, I run the tests inside
a Docker container with throttled CPU.

## Flaky tests should be fixed

It is important to make sure the CI pipeline stays reliable. Fixing flaky tests should therefore be prioritized.
Create a Jira ticket so that the problem is known to everyone and make sure it gets picked up in the current or in the next sprint.

The worst way to deal with flaky tests is to disable them in the code. Based on my experience, if you do that, chances
are you'll never get around to fixing them. The code won't even compile by the time someone has a look at them.

## Happy ending

Flaky tests is nothing but code and logs, and a good developer is like a good detective.
With a little bit of patience, the problem can be found and fixed.
