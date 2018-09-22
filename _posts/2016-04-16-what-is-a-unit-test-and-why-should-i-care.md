---
layout: post
title: What is a unit test and why should I care?
date: 2016-04-16 08:08:45.000000000 +02:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags:
- unit tests
author: Nikolaos Georgiou
---

So, let's start with some basics. What is a unit test? A unit test is a piece of code that validates the expected behavior of a unit in isolation. I guess the next question is, what is a unit? A unit is the smallest piece of code in a given programming language. Typically that is a function or a class method. Let's see it with an example.

<!--more-->

Let's pick the classic example of the Calculator class. The Calculator performs math operations on numbers and returns the results. I'll use JavaScript for the examples:

```
function Calculator() {}

Calculator.prototype.add = function(x, y) {
    return x + y;
};
```

If this file is called Calculator.js, the unit test lives in a different file (let's say CalculatorTest.js):

```
it('should add 2+2 and give 4', function() {
    var calculator = new Calculator();
    var result = calculator.add(2, 2);
    expect(result).to.equal(4);
});
```

This is a simple unit test. The unit in this example is the add method of the Calculator class. I hope it looks rather simple. We'll go into details about its structure in a next post.

More than often, developers complain that this doesn't add value and resist writing unit tests. <strong>The excuse is</strong> often that the code is too simple, it doesn't have a bug, it can't ever have a bug, "<strong>I know that it works</strong>". I've even worked with developers that were personally offended by this. A different excuse is that "it's too difficult to write the test". We'll see the second one in a moment. Let's start with the first excuse.

It is true that the Calculator class looks rather robust. Adding two numbers should be straightforward. What the developer fails understand is that <strong>we're not testing for the present, we're testing for the future</strong>. People make mistakes. Even in trivial functions, a developer can inadvertently introduce a slightly different behavior the original author didn't wish or expect. Tests are there to guarantee that the behavior of the unit hasn't changed. They are the safety net you need in order to feel confident when deploying to production or when performing a large refactoring. I also like to think of them as a form of documentation: they describe exactly what the unit is supposed to be doing. Finally, once you've found a bug in your unit, you always add a unit test that proves the bug is fixed and stays fixed.

This takes me to the next question: <strong>when should you run unit tests</strong>? The answer is: automatically, on every commit. If you have unit tests but you don't run them at all, they're of no use. You have to run them so that you ensure everything still works as expected. Running them manually is a first step, but Murphy's law suggests you'll probably forget to run them when you actually need them the most. Plus, never send a human do a machine's job! There are a few ways to run unit tests automatically: setup a watch task, so that they run as soon as you save a file on your computer. Setup a pre-commit hook, so that they run just before you commit to git. But the best way for a team is to have a CI server that runs the tests for you for every branch and gives you the results. This is easy and it should be a no-brainer.

I mentioned that the unit test tests the unit in isolation. <strong>What does isolation mean</strong>? It means that every dependency of the unit is replaced by controllable dummy units (mocks). We'll cover this technique in another post. For now it's just important to understand that unit tests focus solely on the unit they test. By dependencies we mean other units, but also external resources such as databases, file system, network, web services, etc. As these external resources are replaced by dummies, the side-effect is that unit tests are blazing fast. You can run thousands of them in a second.

So now we can see the second excuse we left unanswered: "<strong>it's too hard to write the unit test</strong>". This is a sign that the unit may be written with various bad practices. Typically this involves hard-coded dependencies that are difficult to mock. It can also include coding against concrete classes instead of coding against interfaces. Another frequent symptom is that the unit does not have a clear responsibility and it's doing too many things. Yes, that piece of code may be doing its job and doing it well. But these code smells that are now preventing a unit test from being easily written are not specific to the unit test. These code smells will become a problem in the future, when trying to maintain or extend this unit. Units like these are expensive in the long run and become the ugly piece of code that nobody wants to touch. With that in mind, you could say that adding unit tests also forces you to write better code.

In the next post we'll add another method to the Calculator class and have a closer look to the structure of the simple unit test we added.
