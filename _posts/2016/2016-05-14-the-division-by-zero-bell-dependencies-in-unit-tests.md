---
layout: post
title: The division by zero bell - Dependencies in unit tests
date: 2016-05-14 08:00:38.000000000 +02:00
published: true
categories:
- Code
series: Unit Tests
tags:
- javascript
- unit tests
---

We left our calculator <a href="/2016/05/what-is-code-coverage/">in the previous post</a> in a decent state, being able to do the four basic mathematical operations. In the special case of division by zero, we want the calculator to make a noise like a bell. Let's see what we can do about this.<!--more-->

Like I mentioned in previous posts, the good thing about <a href="/2016/04/what-is-test-driven-development/">TDD</a> is that it guides you towards code that is better organized and follows good principles. What do I mean? We could start of course by adding the code that connects to the sound system of the calculator directly inside our <code>Calculator</code> class. However, unit testing in that case would be rather difficult. Even worse, it's bad practice because it puts too much responsibilities in the same class. The <a href="https://en.wikipedia.org/wiki/Single_responsibility_principle">single responsibility principle</a> says that the <code>Calculator</code> should keep doing only its maths and leave anything else to other classes.

The unit test for dividing by zero might look like this:

```
describe('Calculator', function() {
    describe('divide', function() {
        it('should ring the bell when dividing by zero', function() {
            // arrange
            var theBellIsCalled = false;
            var bell = function() {
                theBellIsCalled = true;
            };

            var calculator = new Calculator(bell);

            // act
            calculator.divide(4, 0);

            // assert
            expect(theBellIsCalled).to.be.true;
        });
    });
});
```

A couple of things are happening here:
<ul>
<li>the calculator's constructor accepts a parameter, which hasn't happened before in our examples.</li>
<li>the parameter is a simple function that represents the bell. In this naive case, the bell sound system is reduced into a single simple function.</li>
<li>the implementation of the function doesn't do anything, it just sets a flag that we can use to verify that the function was called.</li>
</ul>

Starting with the last bit, this is the essence of how you're supposed to deal with your dependencies. You're supposed to replace all of your dependencies with stubs that comply to the same contract. In this example, the contract isn't even an interface, it's a simple function. When it's called, it's supposed to make a sound like a bell.

We're passing the function as a constructor parameter. This is another good practice that isn't related to TDD but it complies with TDD's principle to write the least amount of code possible. This is about <a href="https://en.wikipedia.org/wiki/Dependency_inversion_principle">dependency inversion</a>. The <code>Calculator</code> class shouldn't try to figure out the bell function it's supposed to call. That is a dependency and it's not the <code>Calculator</code>'s responsibility to resolve dependencies. That will be taken care of by some bootstrapping class that brings all the dependencies together, by some dependency injection framework, by someone else. All the <code>Calculator</code> needs to know is that there will be a bell function provided by someone.

Let's see the implementation for this:

```
function Calculator(bell) {
    // store reference to the bell function
    this.bell = bell;
}

Calculator.prototype.divide = function(x, y) {
    if (y === 0) {
        // make the sound!
        this.bell();
    }

    return x / y;
};
```

We have written zero code related the actual implementation of the bell function that is supposed to connect to the sound card (maybe? who knows? maybe it just plays an mp3?). But our Calculator is ready. Some other developer can go and create the function that actually makes the sound.

This is another reason why TDD is better: it lets you design your contracts, your interfaces, your API, first and from the caller code's point of view. The API of the bell is just a simple function. Lean. Nothing superfluous. Only what is needed.

Consider the following counter example. Let's start implementing the bell feature request without writing the unit test first. Instead, we'll dive head first into implementing it:

```
function Calculator() {
}

Calculator.prototype.divide = function(x, y) {
    if (y === 0) {
        this.bell();
    }

    return x / y;
};

Calculator.prototype.bell = function() {
    var player = require('play-sound')(opts = {});
    player.play('bell.mp3', function(err) {});
};
```

The <a href="https://www.npmjs.com/package/play-sound">play-sound</a> package actually exists, I just found it after a 30'' google search and I copied its hello world example into the <code>bell</code> method.

We have several problems here. Even though this (probably) works, it's not possible to unit test it. We can't write a unit test for the division by zero case, because there's no way to assert programmatically that the computer made a noise. Unless you want to connect a microphone and monitor sound levels that is. After all, where there's a will, there's a way. This is truly the worst case scenario, where testing your code becomes incredibly expensive or even impossible.

In a more real life scenario, your external resource wouldn't be a speaker but a database or a web service. It is possible to run tests against a live database, but it brings additional headaches like initializing the database, making sure it's in the correct state, reading it to verify the results, performance problems because accessing it is slow, and so on. But the biggest problem is the principle. You're not unit testing anymore. You're doing an integration test of the entire system. The calculator's responsibility is to notify the speaker. We take it for granted that the outside world works as expected. We only care about our particular business logic.

Another problem is that our implementation is bound to a specific class. We have a hard dependency that is difficult to remove or replace if needed. What if another class wants to reuse the bell function? You're going to have to refactor it anyway to make it reusable then. TDD gently guides you to make the code small and modular upfront.

Integration tests are definitely useful. But they shouldn't spot problems that unit tests could've spotted. Unit tests are cheap and the more you can do with them, the better. In our topic regarding dependencies, this means that when you're mocking out the dependencies, you have to make sure you're not making a serious contract mistake (e.g. calling the wrong method name). In compiled languages like Java and C#, this isn't likely to be a problem because the compiler will be the first to complain. But in JavaScript, this can very easily go wrong. For example, let's pretend the bell function is supposed to accept a parameter that specifies the duration of the sound in seconds. We're not calling it with any parameters, so it will never make a sound at all. And still, our unit tests are passing. Especially in languages like JavaScript, it's very important that your stubs are complying to the contracts of the external dependencies you're mocking.

In the next post, we'll have a look at sinon, a library that can reduce the boilerplate code we added to setup the bell stub.
