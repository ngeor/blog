---
layout: post
title: Functional Testing - Hiding Async
date: 2016-08-06 09:00:31.000000000 +02:00
parent_id: '0'
published: true
categories:
- Code
series:
- Functional Tests
tags:
- chai
- chai-as-promised
- ES6 generators
- functional tests
- JavaScript
- mocha
- promises
- WebdriverIO
author: Nikolaos Georgiou
---

In the previous post, we explored the Page Object pattern and rewrote our tests to use this technique. Sometimes, it can be that the tests appear to be a bit verbose due to the usage of promises. Additionally, promises and asynchronous programming in general can be somewhat confusing to developers. Let's see some ways of making the tests shorter and easier to read.

<!--more-->

First of all, we're working with promises. There's a nice chai plugin, <a href="https://github.com/domenic/chai-as-promised">chai-as-promised</a>, that can help us our here. Let's install it with <code>npm install --save-dev chai-as-promised</code>.

In order to use it, we'd have to include it and tell chai about it. This is done with <code>chai.use(require('chai-as-promised'));</code>. The question is, where should we do that? We could do it on the test file, but we'll be repeating that in every test file we'd like to use it. To avoid repetition, we can put this statement on the top of our <code>WebDriverHelper</code> class, since this is a class that all of our tests will be including:

```
var chai = require('chai');
chai.use(require('chai-as-promised'));
```

Now this plugin is available in all of our tests. Let's use it for the simple test that checks the title of the homepage:

```
it('should verify the title of Google', function() {
        return expect(page.getTitle()).to.eventually.equal('Google');
    });
```

The test is reduced to a readable one-liner. It's almost an English sentence: "I expect that the page title will eventually equal to Google". The most important word here is <strong>eventually</strong>. The developer(s) of this plugin picked a very accurate name here. It describes exactly what promises are about. Call the function and it will return you the value, <strong>eventually</strong>, once the asynchronous operation has completed.

The first thing to note is that we are returning the whole thing. The usage of <code>eventually</code> is also a <strong>promise that needs to be returned</strong>. This is very important as a common source of problems with functional tests is forgetting to return a promise.

Second, the argument of <code>expect</code> <strong>needs to be a promise</strong>. If you get an error message like <code>argument is not a thenable</code>, then it means you're trying to combine <code>eventually</code> with something that is not a promise. In this case, the <code>getTitle</code> method returns a promise so we're good to go.

Finally, the assertion. What can we use after the <code>.to.eventually.</code> part? The answer is, <strong>you can still use all of chai's assertions</strong>. This plugin intelligently discovers the available assertions that chai offers and extends them. So everything mentioned by <a href="http://chaijs.com/api/bdd/">chai</a> can still be used. As an example, let's see the test that verifies we have a search text box:

```
it('should have a text search box', function() {
        return expect(page.searchTextBox.isVisible()).to.eventually.be.true;
    });
```

Here we used the <code>.be.true</code> assertion. Again, the test was reduced to an one-liner. You might end up with quite long lines, so it's okay to break them down into multiple lines for readability.

There is another way we can write our tests. We can use <a href="https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Statements/function*">ES6 Generators</a>. This changes significantly the style of the tests and makes them look more like they're synchronous code. Let's see the test that performs the search, written with this style:

```
it('should search for pokemon', function * () {
        yield page.searchTextBox.setValue('Pokemon');
        yield page.searchButton.click();
        var text = yield page.searchResults.getText();
        expect(text).to.equal('Ongeveer 330.000.000 resultaten (0,37 seconden)', 'unexpected search result message');
    });
```

Two obvious things: there are <code>yield</code> keywords all over the place and there is a star in the first line. What's up with that?

The star ( <code>function * ()</code> ) indicates that this is a <strong>generator function</strong>: a function that can be exited and later re-entered. This fits well with the promises: exit the function and re-enter it once the promise has been resolved.

The <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/yield"><code>yield</code> keyword</a> works inside a generator function and it allows for pausing and resuming the execution. This allows us to yield promises and collect their values when they're done. On the first line, we just yield the promise that sets the value of the text field, so we don't care about a return value. Same on the second line, we just click the button. Next line though, we have an ordinary variable that collects the result of the <code>getText</code> method. And finally, a regular assertion, without the <code>eventually</code> plugin.

One gotcha: mocha does not support this out of the box. If you try to run this, you'll actually get evergreen tests. I'm not sure if they plan to support it. In the mean time, there are some <a href="http://stackoverflow.com/questions/23024847/override-mocha-it-to-support-yield-using-suspend">workarounds</a>. I've tried the <a href="https://github.com/vdemedes/mocha-generators">mocha-generators</a> package and it seems to work.

This coding style looks quite strange at first. If you've done any .NET programming with <a href="https://msdn.microsoft.com/en-us/library/mt674882.aspx">async/await</a>, you can probably relate to that. Which style should you use? Let's see them side by side:

<img src="{{ site.baseurl }}/assets/2016/diff.png" />

Using generators is perhaps a bit alien. However, the code is much shorter. If you get used to it, it starts to feel like synchronous programming. It doesn't save you from the danger of not returning promises. You can easily forget to add a <code>yield</code> keyword. Any style you pick, you have to make sure that the developers are async-savvy and aware of what they're doing.

In my current project at work, we had decided to not use generators for a couple of reasons:
<ul>
<li>we had already a big code base with many functional tests written in a specific style: returning promises and using chai-as-promised whenever it makes the code shorter. Having two (or more) ways of writing the tests could be confusing to the developers and create unmaintainable code.</li>
<li>allowing to use ES6 features would open up the appetite for more experienced developers to start using more of these features. As our developer expertise levels vary, this would be a problem to the junior developers and in the end to the project and the code base as a whole.</li>
<li>lack of confidence that the mocha-generators patch solution will cover all cases. Maybe some test stays evergreen even after applying that package's fix?</li>
<li>at that point, WebDriverIO team were working on version 4 of their product, which would bring a different way of writing tests that look more like synchronous code.</li>
</ul>

I've left for last one more technique, that involves using the <a href="http://webdriver.io/guide/testrunner/gettingstarted.html">integrated test runner</a> of WebDriverIO. We'll have a look at that on the next post.
