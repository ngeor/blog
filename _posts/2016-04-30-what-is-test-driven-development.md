---
layout: post
title: What is Test Driven Development?
date: 2016-04-30 09:09:00.000000000 +02:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags:
- tdd
- test driven development
- unit tests
author: Nikolaos Georgiou
---

Let's continue building up our calculator with more mathematic operations. So far <a href="/2016/04/a-closer-look-to-a-basic-unit-test/">we have addition and subtraction</a>, so multiplication comes up next.  In this post, we'll have a look at test driven development. Even though the examples are a bit trivial, I hope they'll outline the important points.<!--more-->

So, what is test driven development? Test driven development is a different way of developing in which you write the unit tests first, before you've even written any line of code. If you've never done it before, it seems counterintuitive. How can you write a test for something that doesn't even exist? Well let's try it then!

We find our test and we add a new <code>describe</code> scope to correspond to the new method:

```
describe('Calculator', function() {
    describe('add', function() { /* the add unit tests */ });
    describe('subtract', function() { /* the subtract unit tests */ });
    describe('multiply', function() {
        it('should multiply 2 times 2 and give 4', function() {
            var calculator = new Calculator();
            var result = calculator.multiply(2, 2);
            expect(result).to.equal(4);
        });
    });
});
```

Since we don't have such a method in the <code>Calculator</code> class, the test will fail. If you're using a compiled language like Java, the code won't even compile. Let's add an implementation in our class:

```
Calculator.prototype.multiply = function(x, y) {
    // TODO: learn how to multiply
};
```

I am adding on purpose an empty implementation because this is what I would've done if this was Java or C#. I would have added an implementation that makes the code compile but throws a <code>NotImplementedException</code> at runtime. In test driven development, it's important to start with a red test.

The test will still turn red, but now with a different error. We have to fix the implementation:

```
Calculator.prototype.multiply = function(x, y) {
    return x * y;
};
```

We should be good now and the test is passing. That's the second step in test driven development: writing just enough code to make the test green.

The third step, often forgotten, is refactoring. Test driven development is an iterative cycle: <strong>red - green - refactor.</strong> A lot of times people forget about the refactoring part. In our trivial example, there's not much room for refactoring left, but it's important to remember it.

To get the most out of TDD, you need to focus on its iterative aspect. If you write too much code while you're in the green phase, you drift away from TDD and you start adding more untested functionality. Write <strong>just enough code</strong> to make the test green and leave the green phase.

That's all there is to it really. It's not rocket science but it can change the way you write code. Let's see some benefits of working with test driven development.

First of all, starting with the unit test means that <strong>you treat the test as something important</strong>. It has priority, you start with it, so you don't forget about it later. You're already shifting your mindset about the importance of unit tests by prioritizing them first.

Writing tests first means that you also write in code (the unit test code) the <strong>specifications</strong> of what you intend to build. Having a lot of these small unit tests is a valuable source of documentation about what your module is supposed to be doing. Again, this becomes more effective if you keep the TDD cycles short. If you get carried away while coding, you'll end up writing more code than what you're actually testing for. You need to break out of the green phase. If you manage it, in the ideal situation, you've got <strong>full test coverage</strong> for everything you implement.

Starting with a red test is important because it avoids a common pitfall: <strong>the evergreen test</strong>. When you write tests after the implementation is done, you risk writing a test that is written in a wrong way and that it's green but can't ever turn red. The developer finishes his work, he's happy he added the unit tests and they're green, but there's no real quality added because the test has a problem that causes it to stay green for ever. That test offers no value. Test driven development prevents this common problem from the beginning.

TDD can also improve the <strong>quality of your code</strong>. When you're developing a new module, you often forget about the user of your module. Starting with the test, you're already using your module. You're forced to think about the design of your classes and methods so that they're user friendly. The calling code is written first, so this drives you into making it <strong>friendly for the caller</strong>, which in our case is the unit test.

Another way the quality improves is that you end up writing <strong>leaner units</strong>. Smaller methods, smaller classes, bits and pieces that have a specific purpose and responsibility, <strong>instead of huge messy monoliths</strong>. When practicing TDD, you see that it helps to think about the purpose of your classes and draw boundaries between them. You make interfaces and you avoid hard dependency coupling. Overall, TDD forces you to follow best practices and patterns.

A small final note here: TDD won't magically turn you into an experienced developer that masters class design and OOP principles and whatnot. You still need a senior developer / architect to help out with the design and do some pair programming with the junior / medior developer. Then again, that is something you need regardless of TDD.

Next time, let's start dividing numbers with our calculator and discuss a bit about what code coverage is.
