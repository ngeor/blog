---
layout: post
title: BlogEngine.NET MVC
date: 2013-03-06 13:16:00.000000000 +01:00
published: true
categories:
- Code
tags: []
---

Finally, I got to play with ASP.NET MVC for a real project at work. I really enjoyed it, but it lasted only for a few weeks.

I decided to dig into it a bit more, as a learning exercise at first. I started working on implementing BlogEngine.NET as an MVC project, keeping the same core but with a different frontend. I coded away a little bit during the weekend and made great progress fast.

I'll try to re-create that work publicly and extend it, on a fork available <a href="http://blogengine.codeplex.com/SourceControl/network/forks/NikolaosGeorgiou/blogenginemvc">on CodePlex</a>. As I add more code, I'll be blogging about it here.

The code committed so far contains pretty much nothing:
<ul>
<li>an empty MVC project</li>
<li>the solution upgraded to Visual Studio 2012 format</li>
<li>the existing web project using IIS Express</li>
<li>NuGet Package Restore enabled (to avoid committing all the package binaries)</li>
</ul>

In the end of this project, if it is successful, I'll use it to run my site (eat your own dogfood and all that).
