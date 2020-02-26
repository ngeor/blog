---
layout: post
title: Inline quote in HTML
date: 2011-04-10 07:21:00.000000000 +02:00
published: true
categories:
- tech
tags: []
---

It's amazing when you work for many many years with a technology and stumble upon something new. I stumbled upon an HTML tag that I had never used before, the <a href="http://www.w3.org/TR/html401/struct/text.html#h-9.2.2" target="_blank">Q tag</a>.

With the Q tag, you can quote some text inside a paragraph without breaking the line. The browser is supposed to render that text in quotes, so you don't have to add them yourself.

Let's see it in action:

```

Quoting with the Q tag is <q>sweet</q>.
```

The above HTML snippet will render like this:

Quoting with the Q tag is <q>sweet</q>.

And with CSS you can style just the Q tag, making for example all of your quoted text also bold or italics. Of course you could do the same thing by misusing some span or em tag, possibly with a separate CSS class name, but I think this approach is cleaner and more semantic friendly.

Hope this helps.
