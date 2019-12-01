---
layout: post
title: Using sinon spies
date: 2016-05-21 08:15:53.000000000 +02:00
published: true
categories:
- testing
series: Unit Tests
tags:
- chai
- JavaScript
- sinon
- unit tests
---

In the <a href="/2016/05/the-division-by-zero-bell-dependencies-in-unit-tests/">previous post</a>, we implemented a new feature for our calculator: it makes a bell sound when you divide by zero. The bell is a simple function that the calculator calls and it is provided as a constructor dependency. We wrote a unit test for this as well, but the code for that is a bit verbose. Let's see how we can use a mocking library like sinon to reduce and standardize the testing code.<!--more-->

So the testing code was a bit too much:

```javascript
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

While this works, it doesn't scale well:
<ul>
<li>the code is not standardized, there are many ways you can implement this custom code. Every developer can come up with a different approach, which will damage readability and maintainability of the tests.</li>
<li>it's too much code for a simple function. And keep in mind that so far we aren't passing (or validating) any parameters to that function and we aren't doing anything with the return value of that function.</li>
<li>more custom code in the tests increases the risk of a bug in that code</li>
</ul>

To solve this problem, we can rewrite the test by using <a href="http://sinonjs.org/">sinon</a>. Sinon is a library that offers an API to create spies, stubs, mocks and use them efficiently in your test code. We'll cover stubs and mocks in upcoming posts. For now, let's start with spies.

A spy is easy to explain. It basically, well, spies on a function and after its usage you can check if it was called, how many times was it called, with what arguments, etc. You can use a spy in two ways:
<ul>
<li>you can spy on an existing function without affecting its normal implementation.</li>
<li>you can create a spy without an existing function, then this spy acts as a normal function</li>
</ul>

In our case, we pass the bell function as a dependency so we don't have an actual implementation to spy upon. We'll go for the second approach and change our test like this:

```javascript
describe('Calculator', function() {
    describe('divide', function() {
        it('should ring the bell when dividing by zero', function() {
            // arrange
            var bell = sinon.spy();
            var calculator = new Calculator(bell);

            // act
            calculator.divide(4, 0);

            // assert
            expect(bell.called).to.be.true;
        });
    });
});
```

This is already improved. It's not using any custom variable names but it's using the sinon API. The assertion is more readable also.

Using sinon opens up more possibilities. For example, maybe it is important that the bell is only called one time. Sinon already has this out of the box, just replace <code>called</code> with <code>calledOnce</code> in the above example.

If the test fails, the error message is going to read "expected <code>false</code> to be <code>true</code>". We can improve this by using an additional library, <a href="https://github.com/domenic/sinon-chai">sinon-chai</a>. This is a plugin for chai that offers richer assertions targeted specific to sinon. (This is were using a dedicated assertion library like chai really shines. There are many plugins for chai, sinon-chai is just one of them.)

Compare the two styles:

```javascript
// with plain sinon
expect(bell.called).to.be.true;

// with sinon-chai
expect(bell).to.have.been.called;
```

The second one will give a friendlier message in case of failure, something like "expected bell to have been called".

One piece of advice here: when doing a refactoring of this type on your tests, make sure you don't end up accidentally in evergreen tests. It is possible to make a mistake during refactoring that will render your tests useless. Remember to check that your tests can still turn red, e.g. by introducing temporarily a bug in your code.

Let's add one extra feature to the calculator before finishing the discussion about spies. The requirements have changed and the bell must be called with a parameter that indicates the loudness of the sound. Let's modify the test first:

```javascript
it('should ring the bell when dividing by zero', function() {
    // arrange
    var bell = sinon.spy();
    var calculator = new Calculator(bell);

    // act
    calculator.divide(4, 0);

    // assert
    expect(bell).to.have.been.calledWith('loud');
});
```

That's all there is to it! Can you imagine how much more code we'd have to write without sinon?

The test of course will fail because we don't supply any parameters to the bell function. Let's fix the implementation as well:

```javascript
Calculator.prototype.divide = function(x, y) {
    if (y === 0) {
        this.bell('loud');
    }

    return x / y;
};
```

And we're done. In the next post, we'll add new requirements to the calculator and explore sinon stubs.
