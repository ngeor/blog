---
layout: post
title: Bash case insensitive auto completion
date: 2017-08-30 17:51:48.000000000 +02:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags:
- bash
author: Nikolaos Georgiou
---

I added these two lines in my <code>.bashrc</code>:

```

bind "set completion-ignore-case on"

bind "set show-all-if-ambiguous on"

```

This little trick makes my life a bit easier when working on the terminal. It makes auto completion be case insensitive. This means I can type <code>cd proj</code>, hit the Tab key, and auto completion works its magic changing it into <code>cd Projects</code>. Without this trick, I have to capitalize <code>proj</code> as <code>Proj</code>. This is annoying because I have to be aware of whether I'm working on Windows (case insensitive) or Mac/Linux (case sensitive). With this trick, I just hit Tab.

