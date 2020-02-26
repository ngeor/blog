---
layout: post
title: A closer look to a basic unit test
date: 2016-04-23 08:41:59.000000000 +02:00
published: true
categories:
- tech
series: Unit Tests
tags:
- chai
- javascript
- mocha
- unit tests
---

In the <a href="/2016/04/what-is-a-unit-test-and-why-should-i-care/">previous post</a> we started writing a basic Calculator class and added the first unit test. Let's have a closer look at that unit test and extend our calculator with more features.

<!--more-->

This is how our unit test looked like (remember, everything is in JavaScript):

```
it('should add 2+2 and give 4', function() {
    var calculator = new Calculator();
    var result = calculator.add(2, 2);
    expect(result).to.equal(4);
});
```

Let's start with that "<code>it</code>" call. Where is this coming from? This is a function, provided by the <strong>testing framework</strong>. A testing framework provides a DSL (domain specific language) in which you write the tests. This way, the testing framework can then execute the tests and give you the test results. I use mocha, but jasmine provides a compatible DSL.

So, the "<code>it</code>" function is part of the testing framework's DSL and it's used to define a unit test. The first argument is the name of the unit test. The second argument is the test's code, the function that the testing framework will execute for this unit test.

I like to write the name of the unit test in a way that when combined together with the "it" function it gives a proper english sentence. In this example: "<em>it should add 2+2 and give 4</em>". I like this freedom, whereas in .NET/Java you're limited to using method names for your tests. ShouldAdd2_2_And_Give4 is not as easy to read.

Inside the test function, we have three lines of code. The first instantiates a new <code>Calculator</code> object. The second calls the <code>add</code> method and saves the result. The final line verifies the result by calling the <code>expect</code> function. More on that in a moment. This very basic unit test, with just three lines of code, demonstrates the basic pattern that you'll see in any unit test, the<strong> 3A: Arrange, Act, Assert.</strong>

In every unit test, you'll have to first go through the Arrange phase. In there, you configure your SUT (system under test) in its initial conditions, mock its dependencies, etc. This often is a tedious phase and there are libraries to make your life a bit easier. We don't have any dependencies (yet) so in our case we just instantiate the SUT.

Next, you'll have to Act. What are you testing? In our case we're testing that we can add two numbers. Well, in the Act phase, you add the two numbers. Simple.

Finally, the Assert phase. Here you verify that your expectations are met. In our test, we're calling a function named <code>expect</code>. This is a different DSL, provided by the <strong>assertion library</strong>. The assertion library offers a DSL in which you can express your expectations in a way that both you and the testing framework understand. Not only is it readable to you, but the testing framework is aware of it so that, in case of a failed test, it can report back useful information about what went wrong (e.g. expected 'hello' to include 'world', instead of just 'test failed').

Now, most testing frameworks come bundled with an assertion library as a convenience. You don't necessarily need to install a separate library for your assertions. However, there might be some advantages in choosing a separate assertion library. I use Chai, because it is specialized in assertions and it has some nice plugins that make it even more powerful. Also, Chai is compatible with any testing framework. This means that I can re-use my tests (and my invested knowledge in Chai's DSL) even if I am forced to switch to a different testing framework.

Note that the assertion library can help you verify more than just equality of two numbers. You can compare strings, objects, object hierarchies, partial object hierarchies, regular expressions, arrays, etc. It's a good practice to <strong>only have a single assertion per unit test</strong>. This way, when the unit test breaks, you'll know exactly what went wrong. If you have multiple assertions, you won't know which one caused it to break and you won't know if the following assertions would have passed or not, as the test stops running on the first failed assertion.

Now that we covered the 3A pattern, let's go back to our test. If we run the Calculator test, it gives back a report like:

```
√ should add 2+2 and give 4
```

Now that we only have one unit, we know what this refers to. But if we have many units and many unit tests, we won't remember that this is about the Calculator. It's good to <strong>structure out tests</strong> a bit to reflect the units being tested as well. We'll change the test like this:

```
describe('Calculator', function() {
    it('should add 2+2 and give 4', function() {
        var calculator = new Calculator();
        var result = calculator.add(2, 2);
        expect(result).to.equal(4);
    });
});
```

If we run the tests now the report is a bit different:

```
Calculator
  √ should add 2+2 and give 4
```

which is great. The <code>describe</code> function we added is also part of the testing framework's DSL. It helps add some structure to the tests and, together with some other functions, it offers the ability to run code before and after the tests are run.

The nice thing with the <code>describe</code> is that you can nest them as much as you like. This is another thing that I find liberating compared to .NET and Java. Paving the road for the second method of the <code>Calculator</code> class, let's add one more <code>describe</code>:

```
describe('Calculator', function() {
    describe('add', function() {
        it('should add 2+2 and give 4', function() {
            var calculator = new Calculator();
            var result = calculator.add(2, 2);
            expect(result).to.equal(4);
        });
    });
});
```

The report now will look like this:

```
Calculator
  add
    √ should add 2+2 and give 4
```

In this pattern, the outer <code>describe</code> corresponds to a class and the inner <code>describe</code> corresponds to the method being tested. For simple classes, this is a pattern that works. However, the testing framework doesn't care and doesn't know anything about the meaning you chose to assign to the <code>describe</code> scopes. It's just a convention. For more complicated tests, you may want to come up with something better (e.g. perhaps another <code>describe</code> that represents a specific initial scenario).

Now we should be ready to write the second method for the <code>Calculator</code> class. Let's subtract some numbers:

```
Calculator.prototype.subtract = function(x, y) {
    return x - y;
};
```

And behold our unit test:

```
describe('Calculator', function() {
    describe('add', function() {
        it('should add 2+2 and give 4', function() {
            // arrange
            var calculator = new Calculator();

            // act
            var result = calculator.add(2, 2);

            // assert
            expect(result).to.equal(4);
        });
    });

    describe('subtract', function() {
        it('should subtract 2 from 5 and give 3', function() {
            // arrange
            var calculator = new Calculator();

            // act
            var result = calculator.subtract(5, 2);

            // assert
            expect(result).to.equal(3);
        });
    });
});
```

If we run these tests, the report should look like this:

```
Calculator
  add
    √ should add 2+2 and give 4
  subtract
    √ should subtract 2 from 5 and give 3
```

Next time, let's add some multiplication capabilities to the Calculator while we explore test driven development (TDD).
