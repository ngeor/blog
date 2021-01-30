---
layout: post
title: Functional Testing - Page Object Pattern
date: 2016-07-30 09:00:56.000000000 +02:00
published: true
series: Functional Tests
tags:
- functional tests
- javascript
- page object pattern
- WebdriverIO
---

So far, we've seen how to write functional tests using the WebDriverIO API directly. Let's see what problems we may encounter with that and how the page object pattern comes to rescue.
<!--more-->
Our example functional tests work against Google's homepage. One test verifies that the search text box exists and it's visible. Another test types something into that search text box and performs the search. In order to identify the text box, we use the same <a href="{% post_url 2016/2016-07-16-functional-testing-selectors %}">selector</a>, <code>input[name=q]</code>. The problem starts here and it's not unique to functional tests: it's copy pasting around magic strings.

If our implementation changes and the text field is no longer identified by the name 'q', then we'll have to replace it at potentially many places.

Another risk is that we may be using multiple different selectors to reference the same element. One developer may have used a different selector, e.g. <code>input[type=text]</code>. Why? Simply because he didn't notice that there was another selector referencing the same element.

Finally, using these selectors directly produces code that will be difficult to read and maintain. If the selector is simple enough, e.g. <code>#resultsDiv</code>, then perhaps it's straightforward what the selector points to. But what happens if the selector is something like <code>.main > .nav > li:nth-child(2)</code> ? Good luck remembering what that is supposed to retrieve.

This is where the Page Object pattern can be helpful. The Page Object pattern encapsulates our interactions with WebDriverIO API into classes that model our pages and components. In our example, the homepage is an object which has 3 components: the search text box, the search button and the search results. The selectors that are used to identify these, should be hidden away. The tests should not use them directly, the tests should only use the page objects. Then, the test code can be more readable:

```javascript
it('should verify the title of Google', function() {
    return page
        .getTitle()
        .then(function(title) {
            expect(title).to.equal('Google');
        });
});

it('should have a text search box', function() {
    return page.searchTextBox
        .isVisible()
        .then(function(visible) {
            expect(visible).to.be.true;
        });
});
```

The <code>page</code> variable (we'll see it in a moment) is the page object that represents the Google homepage. It has a field called <code>searchTextBox</code> that is a page object that represents the text box of that page. Notice how the <code>isVisible</code> method call no longer has a selector argument. The selector is hidden away in the implementation of the page object. This solves the problems mentioned earlier and it makes the code more readable and maintainable.

Let's start working on that page object class. The first thing being called is the <code>getTitle</code> method and coincidentally it's the easiest to implement:

```javascript
var WebDriverHelper = require('./webdriver_helper');

function PageObject() {}

PageObject.prototype.getBrowser = function() {
    return WebDriverHelper.browser;
};

PageObject.prototype.getTitle = function() {
    return this.getBrowser().getTitle();
};

module.exports = PageObject;
```

We have a new class named <code>PageObject</code>. It uses our <code>WebDriverHelper</code> class and it's in the same folder. It has two methods so far:
<ul>
<li>the <code>getBrowser</code> is a helper method that provides access to the WebDriverIO API instance. It's handy to have it.</li>
<li>the <code>getTitle</code> is the method that gets, as a promise, the title of the current page. It just calls the corresponding <code>getTitle</code> method of the WebDriverIO API.</li>
</ul>

It gets more interesting when we start hiding away our selectors. We'll implement a new class, named <code>SelectorPageObject</code>, that will represent a page object that is bound to a selector:

```javascript
var PageObject = require('./page_object');

function SelectorPageObject(selector) {
    this.selector = selector;
}

SelectorPageObject.prototype = Object.create(PageObject.prototype);

module.exports = SelectorPageObject;
```

We started by just defining the class as a sub-class of the <code>PageObject</code> (so that it can reuse the <code>getBrowser</code> method). The interesting part is in the constructor: it expects a selector argument. With that in mind, let's implement the <code>isVisible</code> method:

```javascript
SelectorPageObject.prototype.isVisible = function() {
    return this.getBrowser().isVisible(this.selector);
};
```

It just calls the <code>isVisible</code> method of the WebDriverIO API, using the selector that this object was instantiated with. The rest of the methods we have in our tests so far can be implemented in the same fashion:

```javascript
SelectorPageObject.prototype.setValue = function(value) {
    return this.getBrowser().setValue(this.selector, value);
};

SelectorPageObject.prototype.click = function() {
    return this.getBrowser().click(this.selector);
};

SelectorPageObject.prototype.getText = function() {
    return this.getBrowser().getText(this.selector);
};
```

Now, we will put these classes together to good use and we'll model our Google homepage page object. We will place this class in a different folder in our code, called <code>page_objects</code>. The previous two classes were generic, framework-like code, that are not specific to our project, so it makes sense to keep them in the <code>lib</code> folder (or promote them to a separate npm package and use them as a dependency). The homepage class is quite specific to the site we're testing, so it should be in a separate folder.

```javascript
var PageObject = require('../lib/page_object');
var SelectorPageObject = require('../lib/selector_page_object');

function GoogleHomepage() {
    this.searchTextBox = new SelectorPageObject('input[name=q]');
    this.searchButton = new SelectorPageObject('input[value*=Google]');
    this.searchResults = new SelectorPageObject('#resultStats');
}

GoogleHomepage.prototype = Object.create(PageObject.prototype);

module.exports = GoogleHomepage;
```

There we go! The class inherits from <code>PageObject</code> so that we can use the <code>url</code> and <code>getTitle</code> methods. The constructor takes care of instantiating the components. This is the only place where we see these selectors. They're tucked away in this implementation, so it's the one place we'd have to change them. The functional tests don't need to know about them.

So, how do our tests look like with these new classes? Let's have a look one step at a time:

```javascript
var expect = require('chai').expect;
var WebDriverHelper = require('../lib/webdriver_helper');
var GoogleHomepage = require('../page_objects/google_homepage');

describe('Google', function() {
    var page = new GoogleHomepage();
    WebDriverHelper.setupBrowser();

    before(function() {
        return page.url('http://www.google.com');
    });

    // tests follow ...
});
```

We are using the <code>GoogleHomepage</code> class we created earlier. We still need the <code>setupBrowser</code> call from the <code>WebDriverHelper</code> so that stays. The <code>before</code> hook has changed: it is now using our page object.

Let's see the title test:

```javascript
it('should verify the title of Google', function() {
    return page
        .getTitle()
        .then(function(title) {
            expect(title).to.equal('Google');
        });
});
```

It also uses the <code>page</code> variable, just like the <code>before</code> hook. Other than that, it's just the same.

The test that checks we have the search text box in the page:

```javascript
it('should have a text search box', function() {
    return page.searchTextBox
        .isVisible()
        .then(function(visible) {
            expect(visible).to.be.true;
        });
});
```

This one is the first test where we were using selectors. The selector is hidden away in the page object and we reference the <code>searchTextBox</code> field instead. It's the responsibility of the page object to figure out what selector identifies it.

The test that performs the search is a bit more interesting:

```javascript
it('should search for pokemon', function() {
    return page.searchTextBox.setValue('Pokemon')
        .then(function() {
            return page.searchButton.click();
        })
        .then(function() {
            return page.searchResults.getText();
        })
        .then(function(text) {
            expect(text).to.equal('Ongeveer 330.000.000 resultaten (0,37 seconden)', 'unexpected search result message');
        });
});
```

This has actually become a bit more verbose. The original test was chaining a series of promises, without all these <code>then</code> statements. The reason this worked before is that previously all the promises were chained on top of the same instance, the <code>browser</code> variable that pointed to the WebDriverIO API. This is no longer the case. Each function of our page objects returns a promise which can be chained upon, but it points to the <code>browser</code> variable we've hidden inside the <code>WebDriverHelper</code> class.

In the next post, we'll see some ways of shortening our tests.
