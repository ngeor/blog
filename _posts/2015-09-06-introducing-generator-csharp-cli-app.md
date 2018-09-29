---
layout: post
title: Introducing generator-csharp-cli-app
date: 2015-09-06 07:30:00.000000000 +02:00
parent_id: '0'
published: true
categories:
- Code
tags:
- generator-csharp-cli-app
- pet project
- yeoman
author: Nikolaos Georgiou
---

In the weekend I experimented with <a href="http://yeoman.io/">Yeoman</a> and I created my first generator. This is also the first time I publish a package to the official npm repository, so double fun.<!--more-->

Yeoman is a nice Javascript framework for scaffolding. There are several generators out there, but it is relatively easy to create your own, as they provide good documentation.

My generator creates a Visual Studio solution for a console app, together with a class library for the unit tests. The following animation shows it in action:

<img src="{{ site.baseurl }}/assets/2015/09/generator-csharp-cli-app-in-action.gif" />

It is already discoverable if you search in Yeoman:

<img src="{{ site.baseurl }}/assets/2015/09/yeoman-generator-csharp-cli-app.png" />

and of course also in npm:

<img src="{{ site.baseurl }}/assets/2015/09/npm-generator-csharp-cli-app.png" />

