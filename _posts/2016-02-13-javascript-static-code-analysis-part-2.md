---
layout: post
title: JavaScript Static Code Analysis, part 2
date: 2016-02-13 07:09:15.000000000 +01:00
published: true
categories:
- Code
tags:
- code review
- continuous integration
- esprima
- grunt
- grunt-filenames
- grunt-search
- javascript
- jscs
- maintainability
- readability
- static code analysis
---

In the <a href="s">previous post, I talked about static code analysis</a> and how it can be useful in enforcing and maintaining a consistent coding style, but also in catching subtle bugs and code smells. The focus was on two tools, jscs and jshint. What other tools and techniques can you use?<!--more-->

Another problem you can encounter is <strong>inconsistent file names</strong>. Just like code elements, there are many ways to name a file. Developers with different backgrounds have different habits, so before you know it, you can end up with a file structure like this:

```
- lib
  |-- Utilities.js
  |-- factory.js
- Controllers
  |-- home_controller.js
  |-- Products.js
  |-- pricesController.js
```

That's not pretty to look at and it's definitely not fun to work with. Luckily, there are tools out there to save the day. Our build system at work is based on <a href="http://gruntjs.com/" target="_blank">grunt</a>, so it was easy to add <a href="https://github.com/bahmutov/grunt-filenames" target="_blank">grunt-filenames</a> in the pipeline. That tool allows you to specify regular expression rules and overrides tailored to your needs. In the example above, you can specify for example:
<ul>
<li>all folders must be lowercase</li>
<li>all files must be PascalCase</li>
<li>all files inside the Controllers folder must end in Controller.js</li>
</ul>

and any violation will make the build break. No need to check for these things during code reviews any more.

Back to the content of the files. What can you do beyond jscs and jshint?

A simple approach is to <strong>search for a text pattern</strong> that you don't want people to use in the code. As a use case, consider unit tests. We use <a href="http://chaijs.com/" target="_blank">chai</a> at work as an assertion library. Chai has two flavors: <a href="http://chaijs.com/api/bdd/" target="_blank">expect</a> and <a href="http://chaijs.com/api/assert/" target="_blank">assert</a>. If you decide to use one, it's best to avoid using the other (again because of readability and maintainability of the code base). You can use a tool like <a href="https://github.com/benkeen/grunt-search" target="_blank">grunt-search</a> and break the build if your unit tests contain the patterns "assert(" or "assert.". It's a bit of a blunt knife, but it can do the trick and it can search in any type of text file.

When it comes to JavaScript though, you can try to build something more sophisticated. One frequent comment I leave during code reviews is that all unit test names must start with the word 'should'. Let's see it in code:

```
// valid
it('should calculate the sum of two numbers', function() {});

// invalid
it('calculates the sum of two numbers', function() {});

// invalid (uppercase Should)
it('Should calculate the sum of two numbers', function() {});
```

You might've guessed why: readability and maintainability. When you get back the full report of the unit tests that failed, you'll find it easier to read when they're written in the same style.

For only a fraction of the time I spend in code reviews, I developed two prototypes to automatically detect this issue. They both work with tools that parse the JavaScript code and provide you the <strong>syntax tree</strong> to play with. You should be hearing the voice in your head: "Power! Unlimited power!"

The first one is built with <a href="http://esprima.org/" target="_blank">esprima</a> and it's <a href="https://github.com/ngeor/sca-esprima" target="_blank">here</a>. The second one is built as a <a href="https://github.com/jscs-dev/node-jscs/wiki/Plugin-API" target="_blank">jscs plugin</a> and you can see it <a href="https://github.com/ngeor/jscs-custom-plugin-example" target="_blank">here</a>.

We rolled out the jscs plugin solution at work yesterday and it works fine. Why did we go for the jscs plugin approach? Because it's always best to stand on the shoulders of giants.

jscs will call your custom plugin. Guess who else calls jscs? Your text editors. I tried it out in Atom, Sublime Text, IntelliJ. I have to say, it was very satisfying to see all these editors highlight the code as invalid with my error message. And as far as fail fast feedback goes, there's nothing faster than <strong>seeing it fail as you type</strong>.

<img src="{{ site.baseurl }}/assets/2016/jscs-custom-rule.png" />

You don't have to change anything else in your build pipeline either. Your plugin is part of jscs, which makes it <strong>part of your build process</strong>.

Finally, you always want to be able to tell the machine that you're still in control (well, for now). In other words, you need to <strong>be able to disable the rule</strong> if you have to. When you build your custom validation as a jscs plugin, you can override it with inline comments, just like you would do with any jscs rule.

One last tip: consider prefixing your custom rules' names to avoid any clashes. Depending on how psyched you are with all this, you may want to write a custom rule that validates your custom rules are prefixed!

With this simple custom rule in place, a door has been opened. The obvious change is that we no longer have to worry about this convention in the code reviews. The less obvious change remains to be seen: will this small new feature tempt other team members to build on top of it and further <strong>change their mindset, from manual towards automated</strong>? Let's see.
