---
layout: post
title: Batch editing WordPress posts
date: 2018-01-04 09:08:39.000000000 +01:00
published: true
categories:
- automation
tags:
- oauth
- python
- wordpress
---

TL;DR: I had some fun hacking a tiny tool to batch edit posts in my blog in order to fix syntax highlighting of code blocks.

<!--more-->

<strong>Background and motivation</strong>

My blog has had various incarnations over time. It's been on WordPress.com, on my own server with Jekyll and on my own server with WordPress. At some point I went full circle and returned to WordPress.com. The end result is that the various code snippets I include in my posts are not very readable. This is how old code snippets look like:

<figure><img src="{{ site.baseurl }}/assets/2018/01/04/08_16_46-extending-nunit_-nunit-companion-e28093-ngeor-wordpress-com.png" /><figcaption>Old code snippets</figcaption></figure>

It's not very readable compared to the more recent posts:

<figure><img src="{{ site.baseurl }}/assets/2018/01/04/08_20_01-adding-webdriverio-tests-e28093-ngeor-wordpress-com.png" /><figcaption>New code snippets</figcaption></figure>

The reason has to do with the underlying markup. The old posts were using HTML like:

```
<pre class="prettyprint">
code goes here
</pre>
```

The new posts use <a href="https://en.support.wordpress.com/code/posting-source-code/">code shortcodes</a> (normally without the extra spaces):

```
[ code ]
code goes here
[ /code ]
```

To fix this, I'd have to go through all the posts, find all code snippets, and replace the old markup with the new. Sounds like a job for a machine!

<strong>New Year Resolutions</strong>

Learning new things is always fun. I wanted to do a bit more Python this year, even though I never wrote anything with Python professionally. It's a language I found interesting but never had the chance to use it. The Python 2 vs 3 schism was also a deterrent. It's still annoying that search results on google take you to Python 2 results. I had the same problem when I was trying to do a hello world project with Angular, where search results appear for the old AngularJS. But, I gave it a try and I managed to put together what I wanted to achieve without much effort. I called the tool <a href="https://github.com/ngeor/wpbot">wpbot</a> and it's available on GitHub.

<strong>WordPress.org vs WordPress.com</strong>

Googling was confusing in this case too. Just like with Python 2 vs Python 3, I was trying to understand how to connect to the REST API of WordPress, but I got results applicable to self-hosted sites (.org). For my blog, which is on WordPress.com, there's different <a href="https://developer.wordpress.com/docs/">documentation</a>.

<strong>OAuth</strong>

The most difficult part was setting up OAuth (partly due to the confusion between WordPress.org and WordPress.com). The first step is to create a new <a href="https://developer.wordpress.com/apps/">WordPress.com application</a>. This will provide you with a client ID and a client secret. With the client ID and secret, it's possible to authorize the app to edit posts:

<figure><img src="{{ site.baseurl }}/assets/2018/01/04/08_49_38-authorize-wpbot.png" /><figcaption>Authorizing my app</figcaption></figure>

WordPress will then redirect to the URL of the application. Since this is a CLI tool, I launch a small web server from the tool which listens on localhost:3000 to intercept the OAuth code.

<strong>Lessons</strong>

I found that most of the things I used are provided by Python's standard library. I really liked the <a href="https://docs.python.org/3/library/argparse.html">argparse</a> module which is great for building CLI tools. I used also <a href="https://docs.python.org/3/library/http.server.html">http.server</a> for listening to the OAuth response and <a href="https://docs.python.org/3/library/webbrowser.html">webbrowser</a> to start the default browser on the authorization URL, all provided by the standard library.

I used two external modules: <a href="http://docs.python-requests.org/en/master/">requests</a> in order to call the REST API and <a href="http://requests-oauthlib.readthedocs.io/en/latest/">requests_oauthlib</a> for OAuth. I don't know if the standard library has something built-in, coding with nodeJS for so long has conditioned me to googling for a community library instead of looking at what's provided with the package :)

All in all, I had fun writing this tool. Visual Studio Code helps with pylint to catch obvious errors and I even had a look at writing my first unit test in Python.
