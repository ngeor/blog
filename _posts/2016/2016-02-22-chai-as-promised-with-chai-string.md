---
layout: post
title: Chai as promised with Chai string
date: 2016-02-22 21:12:53.000000000 +01:00
published: true
tags:
- functional tests
- chai
- chai-as-promised
- chai-string
- javascript
---

Here's a small tip that puzzled us at work the other day for a while. How do you use chai-as-promised together with chai-string?<!--more-->

<a href="http://chaijs.com/plugins/chai-as-promised/" target="_blank">chai-as-promised</a> is a plugin for <a href="http://chaijs.com/" target="_blank">Chai</a> that makes working with promises a bit prettier. Instead of saying:

```
it('should have the expected title', function() {
    return browser.getTitle().then(function(title) {
        expect(title).to.equal('Chai is cool');
    });
});
```

you can write it a bit more concisely:

```
it('should have the expected title', function() {
    return expect(browser.getTitle()).to
        .eventually.equal('Chai-as-promised is even cooler!');
});
```

<a href="http://chaijs.com/plugins/chai-string/" target="_blank">chai-string</a> is also a plugin for Chai that offers some frequently needed assertions regarding strings. For instance, you can assert that a string is equal to another string ignoring case:

```
expect('aaa').to.equalIgnoreCase('AAA');
```

That one in particular can be handy when you're writing browser tests and you don't know (or don't care) how the text is going to be rendered. Intuitively you might not expect this, but CSS rules will affect the way strings are seen by the test, especially the text-transform style. Even if a text exists as lowercase in the DOM, if the CSS rule renders it as uppercase, that's what the browser test will see. Sounds like a good use case for the equalIgnoreCase assertion.

But how to use chai-as-promised together with chai-string?

It is important that you load chai-as-promised <strong>after</strong> chai-string. Otherwise it doesn't work. This is how the test will look:

```
// order of chai.use is important!
chai.use(require('chai-string'));
chai.use(require('chai-as-promised'));

it('should render hello', function() {
    return expect(browser.getTitle()).to
        .eventually.equalIgnoreCase('hello');
});
```

If you think about these plugins probably work behind the scenes, it makes sense that the order has to be like that. Such a plugin goes and enriches chai with more functionality. chai-as-promised adds this 'eventually' feature. What goes after 'eventually' is whatever this plugin discovers at the time it is being loaded. If you have already loaded chai-string, then it will also discover the chai-string methods and it will extend 'eventually' with them. If you haven't loaded chai-string yet, there's no way for chai-as-promised to see that these methods exist.

Hope this helps!
