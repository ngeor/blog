---
layout: post
title: Functional Testing - Reducing Code Duplication
date: 2016-07-02 07:53:51.000000000 +02:00
published: true
series: Functional Tests
tags:
- functional tests
- javascript
- mocha
- WebdriverIO
---

Let's <a href="{% post_url 2016/2016-06-25-functional-testing-hello-world %}">continue our functional testing</a> examples by adding a few more tests. This will demonstrate why we need to start thinking about the structure of our tests and why we should be developing a framework that will allow us to write less code.
<!--more-->
Let's add one more test. We already have a test that verifies Google's homepage title. We'll do the same for Yahoo's homepage. By the way, maybe it goes without saying, but normally you would be verifying your own site, during development and CI.

```javascript
var expect = require('chai').expect;

describe('Example Functional Test', function() {
    it('should verify the title of Google', function() {
        var webdriverio = require('webdriverio');
        var options = {
            desiredCapabilities: {
                browserName: 'firefox'
            }
        };

        return webdriverio
            .remote(options)
            .init()
            .url('http://www.google.com')
            .getTitle().then(function(title) {
                expect(title).to.equal('Google');
            })
            .end();
    });

    it('should verify the title of Yahoo', function() {
        var webdriverio = require('webdriverio');
        var options = {
            desiredCapabilities: {
                browserName: 'firefox'
            }
        };

        return webdriverio
            .remote(options)
            .init()
            .url('http://www.yahoo.com')
            .getTitle().then(function(title) {
                expect(title).to.equal('Yahoo');
            })
            .end();
    });
});
```

There's an awful lot of repetition in here. Just to add a simple new test, similar to the one we already had, we had to add almost 20 lines of code. Copy pasting code around never scales well in a project and you'll end up with a lot of technical debt to refactor.

Both tests are made up of four distinct parts:
<ul>
<li><strong>initializing</strong> WebDriverIO with the specified options (which are hardcoded and inlined on both tests, they could be coming from a common place)</li>
<li><strong>navigating</strong> to Google's homepage with the <code>url</code> method</li>
<li><strong>examining</strong> the page and<strong> </strong>performing<strong> assertions</strong></li>
<li><strong>terminating</strong> WebDriverIO (with the <code>end</code> method)</li>
</ul>

A small side note: other tests will often have also an extra step after navigating:
<ul>
<li><strong>interacting</strong> with the page (e.g. clicking a button)</li>
</ul>

Back to our tests: duplication is only one of the problems. The other problem is performance. Initializing the WebDriverIO object is something we can just do once, we don't have to do it over and over. The navigating part is also expensive because it depends on how fast the target web page will load. Tests should be grouped in such a way so that we don't perform unnecessary web page loads. This is important especially in the context of a large set of tests run during CI. An unoptimized test suite will slow you down and this is a cost that accumulates over time.

To avoid duplication, we can use mocha's before and after hooks. Our goal is also to avoid performance penalties, that's why we have to try to avoid the <code>beforeEach</code> and <code>afterEach</code> hooks; we need to use the <code>before</code> and <code>after</code> hooks that run only once before all tests.

```javascript
var expect = require('chai').expect;

describe('Example Functional Test', function() {
    var browser;

    before(function() {
        var webdriverio = require('webdriverio');
        var options = {
            desiredCapabilities: {
                browserName: 'firefox'
            }
        };

        browser = webdriverio
            .remote(options)
            .init();
        return browser;
    });

    it('should verify the title of Google', function() {
        return browser.url('http://www.google.com')
            .getTitle().then(function(title) {
                expect(title).to.equal('Google');
            });
    });

    it('should verify the title of Yahoo', function() {
        return browser.url('http://www.yahoo.com')
            .getTitle().then(function(title) {
                expect(title).to.equal('Yahoo');
            });
    });

    after(function() {
        return browser.end();
    });
});
```

We've added a before and after hook. The same basic rule of promises applies here as well: <strong>always return the promise</strong>. We also added a variable called <code>browser</code> in which we store the initialized WebDriverIO API. The <code>before</code> hook initializes the WebDriverIO API. The tests are now much shorter. The <code>after</code> hook just terminates the WebDriverIO session.

We can shorten this even further by making our first steps towards building our framework. The common plumbing of the <code>before</code> and <code>after</code> hooks can move into a separate library file and all our tests can reuse it. We'll do that in a next post. Another thing we'll examine is the usage of <code>chai-as-promised</code> plugin to make our assertions more fluent. Finally, we'll start looking at more tests and selectors to get elements on the page.
