---
layout: post
title: What is code coverage?
date: 2016-05-07 08:30:49.000000000 +02:00
published: true
categories:
- tech
series: Unit Tests
tags:
- code coverage
- unit tests
---

Last time we had a look at <a href="/2016/04/what-is-test-driven-development/">test driven development</a> and our calculator learned how to do multiplication. In this post, we'll add division and talk a bit about code coverage and unit test quality.

<!--more-->

We'll implement division TDD style of course, so let's write the test first:

```
describe('Calculator', function() {
    describe('add', function() { /* the add unit tests */ });
    describe('subtract', function() { /* the subtract unit tests */ });
    describe('multiply', function() { /* the multiply unit tests */ });
    describe('divide', function() {
        it('should divide 4 by 2 and give 2', function() {
            var calculator = new Calculator();
            var result = calculator.divide(4, 2);
            expect(result).to.equal(2);
        });
    });
});
```

the test of course fails as no method by that name exists. We just have to implement it:

```
Calculator.prototype.divide = function(x, y) {
    return x / y;
};
```

and that's it, our calculator knows how to divide numbers.

Or does it? More on that in a moment. First, let's talk about code coverage.

Code coverage is a useful metric that tells you how much of your code is being covered by your unit tests. If your unit tests are the safety net, code coverage tells you about any holes in that net.

How does it work? Code coverage is performed by a tool that runs the unit tests, but modifies the executed code while doing so, in order to keep track of which lines of code are being called. There are probably various tools out there, personally I've used cobertura (for Java), istanbul (for JavaScript) and OpenCover/dotCover (for .NET).

In the example of the <code>divide</code> method, you can imagine that behind the scenes it would modify the code into something like this:

```
Calculator.prototype.divide = function(x, y) {
    trackCoverage('Calculator.divide', 'line1');
    var result = x / y;
    trackCoverage('Calculator.divide', 'line2');
    return result;
};
```

In this example, <code>trackCoverage</code> is a hypothetical function that the code coverage tool would inject in the code on the fly. As the unit tests run, they execute these calls as well, thus allowing the code coverage tool to know that the code is being covered.

Our unit test would hit both lines of the method, so that gives us 100% <strong>line coverage</strong>. Another important type of coverage is <strong>branch coverage</strong>. When the executing code can take different paths, for example in an <code>if-else</code> statement, you have multiple branches. In that context, branch coverage indicates how many of the possible execution paths you're covering. Going on a higher level, you have <strong>method/function coverage</strong>: how many methods are you covering? Going even higher, you'd have <strong>class coverage</strong> and<strong> package/namespace coverage.</strong>

Code coverage should be part of your CI. You don't want to accept commits that open up holes in your safety net and you don't want to be checking for that manually. You can also set different targets per type of code coverage, for example 70% for line code coverage and 90% for class code coverage. Going from lower organization to higher, from line, to branch, to function, to class, it makes some sense to have higher standards too. Missing an entire class sounds worse than missing a single line (then again, Murphy's law says it's that line that will hurt).

It might not be possible to reach 100% code coverage. For example, it is difficult to unit test code that interacts directly with an external resource, like a database or a web service. In cases like these, you want to create an interface, let's call it <code>WebServiceClient</code>, and code against the interface. Coding against interfaces is a good practice anyway, but in this context it helps to keep your code testable. However, the concrete implementation of that interface will still need to talk to the web service, so you won't be able to unit test that and it will have to appear as uncovered in the code coverage report. You have two options: one option is to just lower the bar and say that you're targeting for a code coverage of 70 or 80%. The other option is to fine tune your code coverage configuration by excluding one by one the code files that you know won't be covered. Either way has pros and cons.

Now, I mentioned that code coverage is telling you if your safety net has any holes. However, <strong>it doesn't tell you anything about the strength of your net</strong>. The quality of your unit tests is something you have to check for yourself. Consider the following modification to our unit test:

```
describe('Calculator', function() {
    describe('add', function() { /* the add unit tests */ });
    describe('subtract', function() { /* the subtract unit tests */ });
    describe('multiply', function() { /* the multiply unit tests */ });
    describe('divide', function() {
        it('should divide 4 by 2 and give 2', function() {
            var calculator = new Calculator();
            var result = calculator.divide(4, 2);
            expect(result).to.be.ok;
        });
    });
});
```

This too will give 100% code coverage. Remember, all the code coverage tool does is to instrument your code and keep tabs on which lines are visited and which lines aren't. We still call every line of our code, so it has 100% coverage. However, the test is poor because it just checks that the result is okay. Another example would be a unit test in which it doesn't even check the result at all. Mistakes like these can happen to the best of us. That's why it's important to start with a red unit test and pay attention during code reviews.

Another variation of this example is having the unit extended with extra functionality that doesn't break the tests:

```
Calculator.prototype.divide = function(x, y) {
    var result = x / y;
    this.display.show(result);
    return result;
};
```

Here, someone extended the calculator with a display screen. This is initialized somewhere in the constructor and the test still happily works. Since all lines are still covered, we still have 100% code coverage. But, there is no unit test whatsoever that says "it should display the result of the division on the screen". This might be a feature that has no unit test assurance or it might be a bug that we failed to detect. We don't know; but our code coverage is still 100%.

So, code coverage is an important metric, but the quality of the unit tests is still something subjective. Back to the division example, do we have quality? I find this joke very spot on:
<blockquote>
A QA engineer walks into a bar. Orders a beer. Orders 0 beers. Orders 999999999 beers. Orders a lizard. Orders -1 beers. Orders a sfdeljknesv.</blockquote>

In this joke, the QA engineer tests the system. First, with the happy flow (orders one beer). Then, with various requests that are testing the behavior of the system in extreme cases that perhaps the developer hasn't thought of. Zero beers? Too many beers? What if you order something different? Something that doesn't make sense? Something of a wrong type?

In our simple division example, the most obvious thing we could ask is, what happens if you divide by zero?

Well, you could try it out. But there's no unit test against that and we don't want to try edge cases manually. We want quality, built in, automated. So, yes, our calculator knows how to divide numbers. But we don't really know what happens on the edge cases.

As it turns out, we want the calculator to make a noise when a division by zero happens. Let's continue next time with adding dependencies to the calculator class.
