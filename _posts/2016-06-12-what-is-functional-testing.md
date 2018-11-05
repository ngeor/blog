---
layout: post
title: What is functional testing?
date: 2016-06-12 20:50:05.000000000 +02:00
published: true
categories:
- Code
series: Functional Tests
tags:
- browser tests
- functional tests
- JavaScript
- WebdriverIO
---

In the previous series of posts, we've explored the basics of <a href="/unit-tests/">unit testing</a> and the principles around it. When developing websites, there is another important type of testing: functional testing (also known as browser testing).<!--more-->

Functional testing is an end to end type of test. Unlike unit tests, we're not testing the behavior of individual code units but we're testing the entire system as a whole. It involves writing a script against a browser, simulating a user interaction with the website, and verifying that the end result is what you would expect. This can be as easy as navigating to the homepage and verifying that the footer shows the copyright. But it can also involve more elaborate tests, like registering a new user, adding products to your shopping bag, performing an order, and so on.

Selenium WebDriver is perhaps the most known tool when it comes to functional testing. It operates as a server, implementing the WebDriver API, listening for commands and instrumenting any browser you want. The WebDriver API is so popular that there are even online services like SauceLabs that you can use. There is also PhantomJS, a headless browser (i.e. without any user interface) that implements the WebDriver API. When you're running your functional tests in your CI server, you typically can't launch an actual browser, so you can't use Selenium directly.

In the world of JavaScript, there's a nice library called WebDriverIO that interacts with anything that implements the WebDriver API. This means you can write your tests in JavaScript using WebDriverIO and connect to Selenium, PhantomJS, or an online service. In version 3, WebDriverIO was fully async using promises; they claim that in version 4 they've gone to a fully sync version to make the code easier to write, but I haven't tried that yet.

In the next posts, we'll start playing with functional tests. If possible, I'll try to use WebDriverIO 4 to avoid the extra complexity of async code. We'll also see how to use the Page Object pattern to make the tests readable and avoid duplication.
