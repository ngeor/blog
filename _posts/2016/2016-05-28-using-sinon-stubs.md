---
layout: post
title: Using sinon stubs
date: 2016-05-28 08:34:49.000000000 +02:00
published: true
series: Unit Tests
tags:
- javascript
- mocha
- sinon
- unit tests
---

In the previous post we had a look at <a href="{{ site.baseurl }}/2016/05/21/using-sinon-spies.html">sinon spies</a>. With spies, we are able to determine if a specific function was called or not. Usually the dependencies between units are more interesting, they involve units co-operating, exchanging data and so on. Spies do not suffice. Let's have a look at another technique, using stubs.<!--more-->

A stub is <strong>pre-programmed function</strong>. You define the expected input and output and the stub complies happily. If you call the stub in an unexpected way, it will typically return a default value (<code>undefined</code>). In code, this looks something like that:

```
// create a stub
var stub = sinon.stub();

// prints 'undefined', nothing programmed so far
console.log(stub());

// program the stub to return hello
stub.returns('hello');

// prints 'hello'
console.log(stub());

// program the stub to return hello world for specific arguments
stub.withArgs('world').returns('hello world');

// prints 'hello world'
console.log(stub('world'));
```

Let's see how we can use a stub in our Calculator example. We are going to add a new dependency, a battery. The calculator will offer a new feature that will check the battery's charge level. If it's above zero, then the calculator will report that it is ready to work.

Before we start writing the unit test, we already know that the <code>Battery</code> will be implemented as an object that has a method called <code>getLevel</code>. The method returns a number between 0 and 100. That's the interface (or contract) of the Battery.

The first unit test looks like this:

```
it('should be ready when the battery is charged', function() {
    // arrange
    var bell = sinon.spy();
    var battery = {
        getLevel: sinon.stub()
    };

    battery.getLevel.returns(100);
    var calculator = new Calculator(bell, battery);

    // act
    var isReady = calculator.isReady();

    // assert
    expect(isReady).to.be.true;
});
```

The <code>Calculator</code> constructor now takes a second parameter, the battery. The bell is not really used in this test, but we should pass a parameter. In the act step, you can see the new method of the calculator, <code>isReady</code>, which is expected to return <code>true</code> in this test.

The setup of the test shows that the battery is a simple object with a function called <code>getLevel</code>. Then we stub that function to return the value 100.

The implementation of the <code>Calculator</code> changes like this:

```
// changed: new parameter for the battery
function Calculator(bell, battery) {
    this.bell = bell;
    this.battery = battery;
}

// new method: isReady
Calculator.prototype.isReady = function() {
    return this.battery.getLevel() > 0;
};
```

Are we done? Not really. First of all, we only added one unit test that proves the calculator reports it is ready when the battery is charged. We should cover the opposite case as well: the calculator should report it's not ready when the battery is empty. Note that even if we don't cover this case, code coverage will be reported as 100% (remember how <a href="{{ site.baseurl }}/2016/05/07/what-is-code-coverage.html">code coverage doesn't say anything about the quality of your tests</a>).

To cover the negative test case, we could copy paste the test we already wrote and change it slightly:

```
it('should not be ready when the battery is empty', function() {
    // arrange
    var bell = sinon.spy();
    var battery = {
        getLevel: sinon.stub()
    };

    battery.getLevel.returns(0);
    var calculator = new Calculator(bell, battery);

    // act
    var isReady = calculator.isReady();

    // assert
    expect(isReady).to.be.false;
});
```

This works, but we can avoid some copy pasting by moving some of the common arrange steps into a shared step. Mocha offers <strong>hooks that you can run before or after</strong> all tests. Let's see both tests together with this technique:

```
describe('isReady', function() {
    var battery;
    var calculator;

    beforeEach(function() {
        // arrange
        var bell = sinon.spy();
        battery = {
            getLevel: sinon.stub()
        };

        calculator = new Calculator(bell, battery);
    });

    it('should be ready when the battery is charged', function() {
        // arrange
        battery.getLevel.returns(100);

        // act
        var isReady = calculator.isReady();

        // assert
        expect(isReady).to.be.true;
    });

    it('should not be ready when the battery is empty', function() {
        // arrange
        battery.getLevel.returns(0);

        // act
        var isReady = calculator.isReady();

        // assert
        expect(isReady).to.be.false;
    });
});
```

All the common setup parts are moved into a <code>beforeEach</code> function. This is a hook offered my mocha and it is executed before any unit test within the same <code>describe</code> scope. Mocha also offers a <code>before</code> hook that runs once at the beginning of the <code>describe</code> scope. <code>before</code> runs only once, <code>beforeEach</code> runs once per unit test. There are also their counterparts, <code>after</code> and <code>afterEach</code> that run after the unit tests have run.

Moving the setup parts into a hook is a good practice because <strong>it isolates the plumbing that doesn't change</strong>. The Calculator is always going to use the Battery (and the Bell) in the same way, that doesn't change. What changes per unit test is the battery's state. This also makes the unit tests very clear, in which the arrange step is a one liner.

A subtle yet important difference of these examples, compared to the spies examples, is that the assertion step is done on the calculator itself, our SUT (system under test). In the previous post, the assertion was checking that the spy was called. In these examples, the assertion is checking that the Calculator returned the correct value. We don't really care what the Calculator is doing behind the scenes. All we care is that, given a full battery (the part we stub), the Calculator will report it is ready (and vice versa).

Why didn't we do it like this in the previous post with the bell? Well, the bell did not return any values. In functional programming, this is called a <strong>side effect</strong>: all the bell does is interact with the outside world, but it doesn't return a value. A similar example is a function that writes something to the console or to a disk file. For these cases, the unit test has to use a spy to verify that the implementation is called. This goes against the principle of <strong>testing behavior and not implementation</strong>, but for side-effects there is no alternative. For the battery example however, we just test the behavior. We don't care about the implementation, we don't care if the <code>getLevel</code> function is called or not.

Finally, let's see a different way of using the stub. This can come in handy if you already have an implementation of the Battery class:

```
// instead of this
battery = {
    getLevel: sinon.stub()
};

// you can do this
battery = require('./BatteryImplementation');
sinon.stub(battery, 'getLevel');
```

This has an extra benefit: if the contract of the Battery is modified (e.g. the method is renamed to getChargeLevel) then the unit test will break because sinon will complain that it can't stub a non existing function. This is another layer of safety. Even if you don't have concrete implementations, it's a good idea to separate your definitions into separate files.

In the next post, we'll have a look at the final technique from sinon, mocks, and we'll see how they're different to stubs.
