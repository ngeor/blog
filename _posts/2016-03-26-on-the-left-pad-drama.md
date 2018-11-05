---
layout: post
title: On the left-pad drama
date: 2016-03-26 07:33:06.000000000 +01:00
published: true
categories:
- Tech Notes
tags:
- dependencies
- JavaScript
- left-pad
- Nexus
- npm
---

This week the internet exploded in drama after <a href="http://www.theregister.co.uk/2016/03/23/npm_left_pad_chaos" target="_blank">11 lines of code got unpublished from npm</a>. If you didn't read about it, the summary is that the developer of left-pad removed his package from npm, after npm renamed another package of his because of some name conflict with some other company's trademark or so. Lots of other packages broke because of this due to the missing dependency. What is interesting here, is that this removed left-pad package consists of a single function (only 11 lines of code). How can that tiny package break the internet?<!--more-->

Reinventing the wheel is definitely a bad practice and I prefer standing on the shoulder of giants any day. I want to implement only the code that is really necessary, the code that I'm really being paid for. Many times, I've seen developers over-engineer things and write code for the pleasure of writing something beautiful, yet unnecessary. It is also easier to write something from scratch than investigate and evaluate the existing solutions, scoring them on how they perform on various criteria and so on. It is also easier to write code than read code.

Every line of code should be considered a liability. Many developers don't understand this, but the work is not done when that line of code has been written. It needs to be code reviewed, it needs to be tested. It will need to be read many times in the future when modifying that code. Less is more when it comes to writing your own code. One of my favourite quotes here is by <a href="https://en.wikipedia.org/wiki/Edsger_W._Dijkstra" target="_blank">E.W. Dijkstra</a>: <a href="https://www.cs.utexas.edu/~EWD/transcriptions/EWD10xx/EWD1036.html" target="_blank">if we wish to count lines of code, we should not regard them as "lines produced" but as "lines spent": the current conventional wisdom is so foolish as to book that count on the wrong side of the ledger</a>.

Having said all that, I definitely stand in awe when I look the state of JavaScript today. I would never add a package like left-pad in my dependencies (or even worse, the isArray package). A function is not a package (read also this nice blog post: <a href="http://www.haneycodes.net/npm-left-pad-have-we-forgotten-how-to-program/" target="_blank">NPM & left-pad: Have we forgotten how to program</a>?). If you need a package to check if a variable is an array or not, then you're definitely doing it wrong. You should rely on the language features directly for simple things like that. You can also evaluate bigger packages that offer more that just one function, like <a href="http://underscorejs.org/" target="_blank">underscorejs</a> or <a href="https://lodash.com/" target="_blank">loadash</a> for example.

<figure><img src="{{ site.baseurl }}/assets/2016/cevnsglxiaanrzx.jpg" /><figcaption>The current state of JavaScript programming, by @yogthos</figcaption></figure>

I can imagine that JavaScript as a language has contributed to this. Just the fact that we need a book like <a href="http://www.amazon.com/JavaScript-Good-Parts-Douglas-Crockford/dp/0596517742" target="_blank">JavaScript: The Good Parts</a> is enough to say that it's not the most well thought language. Then again you can write bad code in any language. I think that with browsers maturing on the client-side and with the language itself becoming stronger with ES6, it looks like JavaScript will not need all these libraries for a long time. As it grows and matures, people won't be afraid to use it directly. Packages like jQuery are great, but they only rose to prominence because JavaScript in the browsers was so awfully broken.

But, even in a perfect world, accidents can happen. We depend on other people's packages. Hopefully important packages and not one-liners. What happens when somebody unpublishes his package? What if the company that is hosting the packages goes bankrupt or suffers some network outage?

We had a similar issue at work with Java and Maven. An open-source service called <a href="http://www.javaworld.com/article/2892227/open-source-tools/codehaus-the-once-great-house-of-code-has-fallen.html" target="_blank">Codehaus got discontinued</a> and suddenly we couldn't download our dependencies. The solution here is to install and use an intermediate repository service, like Nexus from Sonatype. This acts more or less as a mirror for the open source packages you depend on. Additionally, you can publish your own private packages. We're currently using Nexus at work for Maven dependencies. It's not limited to Java, I've used it at home for NuGet and I can imagine <a href="http://www.sonatype.org/nexus/2016/03/25/npm-gate-lessons-learned-again/" target="_blank">it supports npm packages too</a>.

Of course, if a package is killed, you'll eventually have to remove it from your dependencies and replace it with something else. You can't go on for ever with an unsupported library. But at least with Nexus you can plan when you'd like to do that, instead of sudden death; which according to Murphy's law will happen that day when you want to deploy the hotfix to production.

There were a lot of funny comments about this drama, but my favourite is that somebody went and created a <a href="http://left-pad.io/" target="_blank">functional microservice</a> (the new trending buzzword) to replace left-pad:

```
$ curl https://api.left-pad.io/?str=hi&len=10
{"str":"        hi"}

$ curl https://api.left-pad.io/?str=hi&len=5
{"str":"   hi"}
```

Looking forward to microservice dependency hell in the near future :)

