---
layout: post
title: Functional Testing Hello World
date: 2016-06-25 08:54:35.000000000 +02:00
published: true
series: Functional Tests
tags:
- functional tests
- javascript
- mocha
- promises
- WebdriverIO
---

Let's have a look at a first example of writing and running a functional test. This is going to be a very basic hello world example, but still it gives an opportunity of looking at the bare minimum usage of WebDriverIO and a first taste of asynchronous programming with promises.<!--more-->

First, we have to add the <a href="http://webdriver.io/">webdriverio</a> dependency to our repo with <code>npm install -D webdriverio</code>. This is the client library that can connect to WebDriver protocol servers like Selenium, PhantomJS, etc.

We are going to take the hello world example from the <a href="http://webdriver.io/guide.html">WebdriverIO page</a>:

```javascript
var webdriverio = require('webdriverio');
var options = {
    desiredCapabilities: {
        browserName: 'firefox'
    }
};

webdriverio
    .remote(options)
    .init()
    .url('http://www.google.com')
    .getTitle().then(function(title) {
        console.log('Title was: ' + title);
    })
    .end();
```

and try to run it with mocha.

Before we start, some observations on the code:
<ul>
<li>it defines a set of options to initialize the WebdriverIO object with. The available options are documented <a href="http://webdriver.io/guide/getstarted/configuration.html">here</a>. For example, you can fine-tune your timeouts for how much WebdriverIO should wait for something to load on your site before giving up.</li>
<li>Then, it initializes the WebdriverIO client with the <code>remote</code> and <code>init</code> methods</li>
<li>It navigates to the homepage of Google with the <code>url</code> method</li>
<li>It requests the page's title with the <code>getTitle</code> method</li>
<li>It prints that title to the console</li>
<li>It terminates the session with the <code>end</code> method</li>
</ul>

All these methods are documented in the <a href="http://webdriver.io/api.html">API section</a> of WebDriverIO. The coding style may look strange at first. Instead of having one function call per line, we have chained functions operating on top of the previous function's result. The reason is that we're dealing with an <strong>asynchronous</strong> API that uses <strong>promises</strong>. A promise is a way of returning something that will <strong>eventually</strong> return a value. Common pitfalls in writing functional tests originate by not properly chaining promises together.

So, our first attempt is to wrap this code in a unit test:

```javascript
var expect = require('chai').expect;

describe('Example Functional Test', function() {
    it('should work', function() {
        var webdriverio = require('webdriverio');
        var options = {
            desiredCapabilities: {
                browserName: 'firefox'
            }
        };

        webdriverio
            .remote(options)
            .init()
            .url('http://www.google.com')
            .getTitle().then(function(title) {
                expect(title).to.equal('Google');
            })
            .end();
    });
});
```

In order to run this, you need to have Selenium or PhantomJS listening, otherwise the test will fail. To use phantom, run it with <code>phantom --webdriver=4444</code> which is the default port for webdriver.

If you run this test, it will work and the test will pass. But, it is actually broken. If you modify the assertion and demand that the title equals to 'Yahoo', the test will still pass! This is a <strong>broken, evergreen test</strong>.

The reason is that WebdriverIO is based on asynchronous code and promises. The unit test executes before the asynchronous code has completed its job. We have to tell mocha about this so that it can wait properly for the asynchronous code to finish.

There are two ways of doing that:
<ul>
<li>add a <code>done</code> parameter to the unit test and make sure that that parameter gets called before the test exits. This way is rather verbose.</li>
<li>have the unit test return the promise so that mocha can wait for it. This is the easy way.</li>
</ul>

Let's have a look at these two ways separately. Note that the first way, using the <code>done</code> parameter, is more verbose and I don't recommend it, because the other way is much simpler.

First, the usage of the <code>done</code> parameter in the unit test:

```javascript
it('should work', function(done) {
```

Note that the function that runs the test has a parameter. Mocha will understand that the test will be complete only when somebody calls that <code>done</code> function. We therefore have to do that at the end of the test:

```javascript
getTitle().then(function(title) {
    expect(title).to.equal('Yahoo');
})
.end()
.then(function() {
    done();
}, function(err) {
    done(err);
});
```

After the <code>end</code> call, we have attached another promise that calls the done function. If the test succeeds, it calls the <code>done</code> without arguments. If the test fails, it calls the <code>done</code> function with the error that happened. This allows mocha to correctly report the test's status.

This is a bit too verbose. A much easier way is to simply <strong>return the promise</strong> and not use the done function at all. Mocha does the rest for us:

```javascript
var expect = require('chai').expect;

describe('Example Functional Test', function() {
    it('should work', function() {
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
});
```

We took out the <code>done</code> parameter completely. Notice that now the promise chain is being returned from the unit test. This is all mocha needs in order to tie the loop together and make sure we don't have an evergreen test.

In the next post we'll add a second test and start working towards giving some structure to these tests, taking advantage of mocha's before and after hooks.
