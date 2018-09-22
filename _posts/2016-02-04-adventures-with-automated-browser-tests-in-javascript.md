---
layout: post
title: Adventures with automated browser tests in JavaScript
date: 2016-02-04 20:49:24.000000000 +01:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags:
- automated tests
- chai
- es6
- JavaScript
- mocha
- page object pattern
- phantomjs
- selenium
- technical debt
- WebdriverIO
author: Nikolaos Georgiou
---

This is a long post, be advised! It goes through the adventures we have had at work with automated browser tests in JavaScript. It has been a journey full of challenges and knowledge build up, a journey that still goes on!<!--more-->

For the past months, we've been working on a big rewrite project at work. Part of the rewrite puts emphasis on quality and predictability. That's why we invest heavily in automated tests. Since this is about websites, we definitely need browser tests too (call me selenium, phantomjs, webdriverIO, I treat them as synonyms).

The main project is in JavaScript, so we picked JavaScript for the browser tests too to keep it simple. The problem is that nobody in the team had experience with JavaScript in that particular area. There was going to be a learning curve and so it happened. Over time, we gained knowledge and the way we write tests became better and better.

Initially, we just wrote a PoC using <a href="https://mochajs.org/" target="_blank">mocha</a>, <a href="http://chaijs.com/" target="_blank">chai</a>, and <a href="http://webdriver.io/" target="_blank">webdriverio</a>. You could run your tests locally using Selenium. In CI, tests were running against SauceLabs, a SaaS solution that we were already subscribed to.

The PoC was very simple. There was no testing framework in place or anything like that. Think of the hello world of webdriver.io (I'll copy paste it here actually):

```
var webdriverio = require('webdriverio');
var options = { desiredCapabilities: { browserName: 'chrome' } };
var client = webdriverio.remote(options);

client
    .init()
    .url('https://duckduckgo.com/')
    .setValue('#search_form_input_homepage', 'WebdriverIO')
    .click('#search_button_homepage')
    .getTitle().then(function(title) {
        console.log('Title is: ' + title);
        // outputs: "Title is: WebdriverIO (Software) at DuckDuckGo"
    })
    .end();
```

In combination with mocha and chai, this became something like that:

```
describe(function() {
    it('should have the correct title', function() {
        var webdriverio = require('webdriverio');
        var options = { desiredCapabilities: { browserName: 'chrome' } };
        var client = webdriverio.remote(options);

        client
            .init()
            .url('https://duckduckgo.com/')
            .setValue('#search_form_input_homepage', 'WebdriverIO')
            .click('#search_button_homepage')
            .getTitle().then(function(title) {
                expect(title).equals('WebdriverIO (Software) at DuckDuckGo');
            })
            .end();
    });
});
```

We soon took out the initialization and clean up and moved it in a utility file, let's call it 'helper' here, which exists even today:

```
describe(function() {
    var browser;

    before(function(done) {
        browser = require('helper').init();
        browser.call(done);
    });

    after(function(done) {
        require('helper').end(done);
    });

   it('should have the correct title', function(done) {
        browser
            .url('https://duckduckgo.com/')
            .setValue('#search_form_input_homepage', 'WebdriverIO')
            .click('#search_button_homepage')
            .getTitle().then(function(title) {
                expect(title).equals('WebdriverIO (Software) at DuckDuckGo');
            })
            .call(done);
    });
});
```

As you can see, this also meant that we switched to the async flavor of mocha (that's the done parameter). Having the test divided across asynchronous methods meant we had to use the 'done' as synchronization points for the asynchronous code to meet. Otherwise you ended up with timeouts, red tests or, even worse, evergreen tests that could never turn red.

Soon, we dived into the world of <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise" target="_blank">promises</a>. Some of us were familiar with it, some others were familiar with similar concepts in other programming languages (for instance I could relate to the async/await Task in C#), some others struggled a bit more.

While the knowledge level around promises was still low and growing, a different and pressing need emerged. Our tests were not reusable and the implementation details were being repeated all over the place. The most common example is the selectors we use to target elements on the page. These CSS selectors were duplicated in all of the tests. Or, even worse, different tests would use different CSS selectors to target the same element. If a frontender decided to change a CSS class, we'd have to make sure it gets changed everywhere. That's when we introduced the <a href="http://martinfowler.com/bliki/PageObject.html" target="_blank">PageObject pattern</a>.

But, nobody had implemented the PageObject pattern in async JavaScript. Some people had experience with Java, but in a simple synchronous API.

Initially, I implemented a PoC that was a bit ambitious. My idea was that the API should not <a href="http://www.joelonsoftware.com/articles/LeakyAbstractions.html" target="_blank">leak abstractions</a> to the outside world and I considered promises to be such an abstraction. It's similar to how an ORM shouldn't really expose database nuts and bolts to the outside world. It's an implementation detail and it should stay within the box. Anyhow, that's what I was trying to do. It worked, but we had some problems. First, the PageObjects were difficult to implement and understand, because the core point of hiding the promises meant maintain the chain of promises internally in the page objects. Second, you couldn't call any webdriverIO method unless you exposed it from the PageObject (in my mind that was actually a feature). It looked something like this (I've removed a bit of code from the previous example):

```
/**
 * Base page object
 */
function PageObject(currentPromise) {
    this.lastPromise = currentPromise;
}

PageObject.prototype.url = function(url) {
    this.lastPromise = this.lastPromise.url(url);
    return this;
}

PageObject.prototype.call = function(fn) {
    this.lastPromise = this.lastPromise.call(fn);
    return this;
}

PageObject.prototype.then = function(fn) {
    this.lastPromise = this.lastPromise.then(fn);
    return this;
}

PageObject.prototype.getTitle = function() {
    this.lastPromise = this.lastPromise.getTitle();
    return this;
}

PageObject.prototype.searchButton = function() {
    return new Button(this.lastPromise, '#search_button_homepage');
}

/**
 * Generic button
 */
function Button(currentPromise, selector) {
    PageObject.call(currentPromise);
    this.selector = selector;
}

Button.prototype = Object.create(PageObject.prototype);

Button.prototype.click = function() {
    this.lastPromise = this.lastPromise.click(selector);
    return this;
}

/**
 * Usage in test
 */
describe(function() {
    var browser;

    before(function(done) {
        browser = require('helper').init();
        browser.call(done);
    });

    after(function(done) {
        require('helper').end(done);
    });

   it('should have the correct title', function(done) {
        var page = new PageObject();
        page
            .url('https://duckduckgo.com/')
            .searchButton()
            .click()
            .then(function() {
                page.getTitle().then(function(title) {
                    expect(title).equals('WebdriverIO (Software) at DuckDuckGo');
                })
            })
            .call(done);
    });
});
```

As you can see, the page objects maintain internally the last known promise. When we started mixing multiple page objects in a single scenario, this needed rework because every object ended up keeping track of a different variable and the tests didn't synchronize anymore.

These shortcomings, exacerbated by frustrated team members visiting my desk to express their hatred to the implementation, led me to rewrite it like this:

```
/**
 * Base page object
 */
function PageObject() {
}

PageObject.prototype.url = function(url) {
    return this.getBrowser().url(url);
}

PageObject.prototype.getTitle = function() {
    return this.getBrowser().getTitle();
}

PageObject.prototype.searchButton = function() {
    return new Button('#search_button_homepage');
}

PageObject.prototype.getBrowser = function() {
    return require('helper').getOrCreateBrowser();
}

/**
 * Generic button
 */
function Button(selector) {
    PageObject.call(currentPromise);
    this.selector = selector;
}

Button.prototype = Object.create(PageObject.prototype);

Button.prototype.click = function() {
    return this.getBrowser().click(this.selector);
}

/**
 * Usage in test
 */
describe(function() {
    var browser;

    before(function(done) {
        browser = require('helper').init();
        browser.call(done);
    });

    after(function(done) {
        require('helper').end(done);
    });

   it('should have the correct title', function(done) {
        var page = new PageObject();
        page
            .url('https://duckduckgo.com/')
            .then(function() {
                return page.searchButton().click();
            })
            .then(function() {
                page.getTitle().then(function(title) {
                    expect(title).equals('WebdriverIO (Software) at DuckDuckGo');
                })
            })
            .call(done);
    });
});
```

The page object implementation became much shorter and simple. Tracking the browser instance became responsibility of the helper class we introduced early on. However, the new challenge is that you don't know if the page object methods return a new page object (like in 'searchButton') or a promise (like in 'click'). Also, when you call a method that returns a promise (like 'url' above), you lose the ability to keep on chaining page object methods; you need to chain it verbosely with a 'then'.

This version was also not perfect but it worked better than the previous one and people were able to use it. We wrote many tests and a lot of page objects. We organized the page objects into pages, components (areas in a page) and elements (generic HTML elements). We organized the tests by the user's point of view (e.g. home page, checkout page, etc).

While we're having all this fun, we were experiencing some problems with SauceLabs. We couldn't resolve them, so we switched to <a href="http://phantomjs.org/download.html" target="_blank">phantomjs</a>. Until this day, we're paying for SauceLabs without using it, because the official line is that phantomjs is a temporary workaround. phantomjs was no picknick either. The latest official binary for Linux (which is what our CI runs on) was 1.9, which was old and choked on some of our client-side JavaScript. We ended up compiling phantom 2.0 from source code ourselves on the CI server. I just hope I have a backup of the compiled binary somewhere. (Hey, I just noticed that they have a binary for 2.1 for Linux, hurray!!!)

Meanwhile, another problem was that some people were using the '<a href="http://chaijs.com/api/assert/" target="_blank">assert</a>' and some others the '<a href="http://chaijs.com/api/bdd/" target="_blank">expect</a>' flavor of chai assertions. Paralysis by choice, one might say. We failed to understand that free choice would become an issue later on, we allowed people to pick what they like. However, as a writer you would pick one, stick with it, become fluent in it. And then you'd struggle as a reader when you'd have to edit/review/reuse somebody else's code that was using the other style of assertions. In the end we settled on 'expect' but we still haven't moved the old 'assert' tests to use 'expect'.

Similarly, we still have a lot of tests that don't use the page object pattern at all. This is a kind of technical debt that we have to pay up at some point.

With experience growing, we found more ways to make our tests shorter. We figured out that mocha was smart and you didn't need to call done; you could return the promise instead and mocha would tie up the loose ends in a "don't call us, we'll call you" fashion:

```
// we're calling done
it('should do it', function(done) {
    pageObject.click().call(done);
});

// we're returning the promise, mocha will sort it out
it('should do it', function() {
    return pageObject.click();
});
```

This subtle change meant less keystrokes. But in the mean time a lot of people had gotten used to the old way. So, it caused some confusion: when do I need done? When do I need to return? People might omit done and omit to return at the same time, which led to evergreen tests that never turned red because they never really run.

Another finding was a chai plugin, <a href="http://chaijs.com/plugins/chai-as-promised" target="_blank">chai-as-promised</a>. This one offered a syntax that made the expectation to look a bit more synchronous:

```
it('should have the title', function() {
    return expect(pageObject.getTitle()).to.eventually.equal('My Site');
});
```

Up to recently, the state was a state of controlled mess. We knew that the mess existed, but the knowledge was shared and understood by our teams. They knew the do's and don'ts for the most part. The tower of babel is written in multiple styles:
<ul>
<li>without page objects (the really old tests)</li>
<li>with 'done'</li>
<li>without 'done'</li>
<li>with chai-as-promised</li>
</ul>

and probably combinations of the above.

It should not be a surprise that when we scaled up to two new teams, they struggled, and still struggle, to understand which template they had to follow. But that's the price of moving forward without cleaning up your stuff.

The most recent development came today. One of our test engineers who has been getting up to speed with all this came to me and asked if there's a way to get rid of all these 'then' chains. Filling in a billing form for example can take a toll on your eyes:

```
before(function() {
        return billingForm
            .lastName().setValue('Georgiou')
            .then(function() {
                return billingForm
                    .firstName().setValue('Nikolaos');
            })
            .then(function() {
                return billingForm
                    .phone().setValue('12345678');
            });
    })
```

and of course this list in reality is 3 times longer. Coincidentally, I was exploring last night some ES6 features. We sat together and in 1 hour we had a working prototype that changed the above indentation roller coaster into this beauty:

```
before(function* () {
        yield billingForm.lastName().setValue('Georgiou');
        yield billingForm.firstName().setValue('Nikolaos');
        yield billingForm.phone().setValue('12345678');
    });
```

(the other test engineer was yelling "it's beautiful! it's beautiful!" so I think he liked it too)

I am very new to this, but one must admit the second version looks way more readable. It looks like you're reading synchronous code (looks exactly like the async/await of C#). Notice the extra star after the function. This marks it as a generator function. I invite you to read more at the <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function*" target="_blank">documentation</a>, it has some nice examples too. Like I said, this is going to be my next learning adventure.

We intend to roll this out to the teams from next week, unless somebody objects. Additionally, we're thinking of starting cleaning up our existing tests: if you touch a file, you have to rewrite the entire thing in the new way. We'll see how that flies, you have to start paying up the debt sooner or later!

