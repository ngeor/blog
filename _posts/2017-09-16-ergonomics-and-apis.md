---
layout: post
title: Ergonomics and APIs
date: 2017-09-16 08:55:13.000000000 +02:00
published: true
categories:
- Tech Notes
tags:
- ergonomics
---

According to my Google search, ergonomics is the study of people's efficiency in their working environment. The developer's working environment consists of the physical world but also the virtual world. In the physical world you desire a quiet office, good desk and chair, proper lighting, the best tools your budget can buy, etc. In the virtual world, you have software tools, IDEs, etc. But when writing code, the working environment also consists of the APIs you code against, as well as the code you have written for yourself.

<!--more-->

I'll start with a small example. I was writing a unit test. The class I was testing had two dependencies that I had to mock, a downloader and a parser. So somewhere in my setup code I had:

```

_mockDownloader = new Mock<IDownloader>();

_mockParser = new Mock<IParser>();

```

Looks good right? Well, if you take ergonomics into account, this version is better:

```

_downloaderMock = new Mock<IDownloader>();

_parserMock = new Mock<IParser>();

```

Why is this better? On modern IDEs and code editors, you have an autocomplete feature. As you start typing, the editor offers a list of suggestions, trying to predict what you want to type. In the first case, I have more characters that I need to type before autocomplete narrows down the results to one, because all variables have the same prefix. In the second case, I need fewer keystrokes to go there.

This is just a simple example, and it might not sound like a big deal. But over time, these keystrokes accumulate. To quote Scott Hanselman:
<blockquote>
<em><a href="http://keysleft.com/" target="_blank" rel="noopener">You have a finite number of keystrokes left in your hands before you die</a>.</em></blockquote>

Another example has to do with organizing classes into namespaces. It make sense to group classes into namespaces based on the functionality the fulfill. For example in .NET you have <code>System.IO</code> for IO related functionality, <code>System.Text</code> for text processing and encoding, etc. Regular expressions could definitely fit inside <code>System.Text</code> from a concept point of view. They have to do with text. However, they go into their own namespace, <code>System.Text.RegularExpressions</code>. If a namespace has too many classes, autocomplete becomes less helpful.

One final example is the <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import" target="_blank" rel="noopener">import</a> statement in ES6 JavaScript. The syntax is:

```

import { member1, member2 , ... } from 'module-name';

```

The members you want to import from a module come before the module name. This means that you can't have autocomplete, as the IDE doesn't know what module you are trying to import from. This is an example of bad design. In retrospect, this syntax would've been much better from ergonomics point of view:

```

from 'module-name' import { member1, member2, ... };

```

When designing an API, take these considerations into account. It's similar with writing code with readability in mind: you write the code once, but it's going to be read many more times. Design the API from the API user's point of view (which by the way is also the unit test's point of view) and take ergonomics into account as well.

