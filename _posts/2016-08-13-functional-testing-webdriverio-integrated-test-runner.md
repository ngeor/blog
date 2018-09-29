---
layout: post
title: Functional Testing - WebDriverIO Integrated Test Runner
date: 2016-08-13 07:55:24.000000000 +02:00
parent_id: '0'
published: true
categories:
- Code
tags:
- functional tests
- JavaScript
- WebdriverIO
author: Nikolaos Georgiou
---

In the previous series of posts, we had a look at functional testing with WebDriverIO and mocha. We explored the page object pattern and saw the challenges of asynchronous programming with promises. We even saw some ways of mitigating those challenges. However, there is another approach to the same problems. Instead of running our tests with mocha, we can run them using the integrated test runner of WebDriverIO.
<!--more-->
From version 4 onwards, I'll quote from their site, "the integrated test runner allows you to write asynchronous commands in a synchronous way so that you don’t need to care about how to propagate a Promise to avoid racing conditions". If you're starting a new project, or if you don't have many tests to migrate, this is definitely an interesting approach. This combines a synchronous-like approach without using anything extra.

To use it, you'll have to first initialize it with a configuration file. There is a wizard that prepares it for you:

<code>./node_modules/.bin/wdio config</code>

It asks you a couple of questions, most importantly, where are the functional tests. You can also pick a testing framework (mocha is supported) and test reporters (junit is supported so we can consume the test results from a CI server).

Running the tests from the command line is done like this:

<code>./node_modules/.bin/wdio wdio.conf.js</code>

There are also plugins for grunt and gulp so that you can integrate this in your existing build pipeline.

Some important things change when you use this integrated test runner:
<ul>
<li>you get for free a variable named <code>browser</code> that gives you access to the WebDriverIO API. Session management is done by the test runner.</li>
<li>by default, tests are synchronous. No more promises.</li>
</ul>

At my current project at work, we use a custom solution and not the integrated test runner. Due to inexperience with the technology stack, we hadn't considered it as an option at the time (one year ago, when it was still in version 3). Being able to get rid of the promise-based code is a strong motivation to migrate, because that's what confuses most of the developers.

I have to say that I don't like that the promise-free feature is so tightly coupled with the test runner. It should be possible to activate just that feature, on a per test basis, without being forced to use a specific test runner. You need to find a new grunt/gulp plugin to integrate it in your pipeline. You need to make sure your editor (Atom, IntelliJ, other?) has support for this test runner.

When using the integrated test runner of WebDriverIO, it is still possible to have asynchronous promise-based tests. You just need to name the function of the test 'async' (which is a bit hacky arguably):

```
it('should support sync code', function() {
    browser.url('http://my-site.com');
    expect(browser.getTitle()).to.equal('My Site');
});

it('should still support promises', function async() {
    return browser.url('http://my-site.com').then(function() {
        return expect(browser.getTitle()).to.eventually.equal('My Site');
    });
});
```

But the biggest question is, how to migrate thousands of tests written using a custom browser management solution, like the one we developed in the previous series of posts. The browser variable is under the test runner's control.

It would be great if the promise-free code was something that we could programmatically activate, on a per-test basis, without being forced to use the integrated test runner. Something like this:

```
describe('some test', function() {
    before(function() {
        require('webdriver').sync();
    });

    after(function() {
        require('webdriver').noSync();
    });

    it('should support sync code', function() {
        // sync code
    });
});
```

This would be the best option in my opinion, in both giving independence from the integrated test runner and allowing you to gradually migrate your code base to synchronous code style.
