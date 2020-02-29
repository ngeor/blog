---
layout: post
title: Using wget to detect broken links
date: 2016-01-24 09:43:45.000000000 +01:00
published: true
tags:
- broken links
- wget
- meta
---

To make sure I didn't forget any images in the <a href="/2016/01/23/migrated-back-to-wordpress.html">blog migration</a>, I used wget to detect broken links. Better safe than sorry! Simply run:

```
wget -r -nv --spider http://ngeor.net/ -o log.txt
```

And you get the report of the broken links in log.txt.

Turns out I had to adjust a couple of permalinks after all.

If you're on a Mac, use HomeBrew to install wget.
