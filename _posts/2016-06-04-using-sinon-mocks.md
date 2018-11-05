---
layout: post
title: Using sinon mocks
date: 2016-06-04 08:00:24.000000000 +02:00
published: true
categories:
- Code
series: Unit Tests
tags:
- JavaScript
- sinon
- unit tests
---

In the previous posts we had a look at sinon <a href="/2016/05/using-sinon-spies/">spies</a> and <a href="/2016/05/using-sinon-stubs/">stubs</a>. There is one more technique we can use in order to orchestrate our test dependencies: mocks.

<!--more-->

Let's start by breaking the Calculator's <code>isReady</code> method. That method was supposed to return <code>true</code> if the battery is charged, <code>false</code> otherwise:

```
Calculator.prototype.isReady = function() {
    return false;
};
```

We just broke it, so it always returns <code>false</code> without even checking the battery status. If we run the tests, we'll see that out of the two relevant tests, one is passing and one is failing:

```
x should be ready when the battery is charged

      ✓ should not be ready when the battery is empty
```

The test that succeeds is the one that proves that the calculator does not work when the battery is empty. The thing is, our calculator never works with this implementation. Luckily one test is breaking, so we are safe. But why did the other test pass?

We are using a stub in that test. Stubs are pre-programmed functions. If you call them, they will do as they have been programmed. But if you don't call them in the programmed way, or not at all, then nothing happens. This is actually a good thing, because the test shouldn't enforce any implementation details. We should test behavior and not implementation and that's what the stubs provide.

The mocks work in a different way. Let's see how that looks like:

```
describe('isReady', function() {
    var mockBattery;
    var calculator;

    beforeEach(function() {
        // arrange
        var bell = sinon.spy();
        var battery = {
            getLevel: function() {}
        };

        mockBattery = sinon.mock(battery);
        calculator = new Calculator(bell, battery);
    });

    it('should be ready when the battery is charged', function() {
        // arrange
        mockBattery.expects('getLevel').returns(100);

        // act
        var isReady = calculator.isReady();

        // assert
        expect(isReady).to.be.true;
        mockBattery.verify();
    });

    it('should not be ready when the battery is empty', function() {
        // arrange
        mockBattery.expects('getLevel').returns(0);

        // act
        var isReady = calculator.isReady();

        // assert
        expect(isReady).to.be.false;
        mockBattery.verify();
    });
});
```

Let's see the differences with the stubs:
<ul>
<li>The mock wraps the entire battery object. You need to have at least the definition, if not the actual implementation, of the <code>Battery</code> object in order to mock it. For the stub, that was not necessary, although it was nice to have there as well.</li>
<li>At the end of the test, the mock is verified. This arguably violates the "one assertion per unit test" rule but it is necessary.</li>
<li>Last and most important: the mock expectations that are defined upfront are not optional; every single expectation of the mock has to occur, otherwise the mock verification will fail the test.</li>
</ul>

If the <strong>stubs</strong> represent pre-programmed <strong>behaviors</strong>, the <strong>mocks</strong> represent pre-programmed <strong>behaviors but also expectations</strong>.

Running the tests like this we'll have two failures, because nobody is calling the <code>getLevel</code> method of the <code>battery</code> object:

```
ExpectationError: Expected getLevel([...]) once (never called)
```

You can read in <a href="http://martinfowler.com/articles/mocksArentStubs.html#TheDifferenceBetweenMocksAndStubs">this article by Martin Fowler</a> more about mocks vs stubs. Using mocks make the tests stricter, but that's because they enforce implementation details. The general rule is that tests should focus on <strong>behavior, not implementation</strong>. This means that you shouldn't use a mock, unless for some reason you can't avoid it. Stubs should be enough.

This post concludes this series of articles on unit tests. Coming up, we'll have a look at browser testing with webdriverIO.
