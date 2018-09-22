---
layout: post
title: DOSBox configuration file
date: 2017-08-26 07:59:27.000000000 +02:00
type: post
parent_id: '0'
published: true
categories:
- Tech Notes
tags:
- DOSBox
author: Nikolaos Georgiou
---

I did the following changes to my DOSBox configuration file:
<ul>
<li>fulldouble=true (it probably doesn't hurt, it's supposed to reduce flickering)</li>
<li>windowresolution=1900x1024 (because on my high DPI laptop screen DOSBox by default launches in a teeny tiny window I can barely read)</li>
<li>output=opengl (works in combination with the previous setting)</li>
</ul>

And in the autoexec section, these two commands:
<ul>
<li>mount c c:\users\ngeor\dosbox</li>
<li>c:</li>
</ul>

This mounts my dosbox folder as the C drive and switches to that drive, so I'm ready to launch GWBasic :-)

