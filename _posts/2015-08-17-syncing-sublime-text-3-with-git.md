---
layout: post
title: Syncing Sublime Text 3 with Git
date: 2015-08-17 16:36:00.000000000 +02:00
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

I use Sublime Text 3 at home and at work. I use it on many computers and platforms. In this kind of setup, maintaining a consistent configuration across multiple installations can be a challenge. It just doesn’t feel right, when you switch to work on a different laptop and suddenly some package is missing here or some setting is different there. You want to simply have the same settings everywhere, without spending too much time on configuration.<!--more-->

To solve this problem, I thought of storing the entire Packages folder of Sublime in a git repository and adding third-party packages as git submodules. You can find my repository <a href="https://github.com/ngeor/sublime-packages">here</a>. Next time I sit behind a fresh Sublime Text 3 installation, all I have to do to in order to configure it exactly as I want it is:
<ul>
<li>locate and delete the Packages folder</li>
<li>do a git clone (recursive, so that it fetches the submodules as well) of my repo and use it in place of that Packages folder</li>
</ul>

The packages folder can live in various locations, depending on the platform and whether you’re using a standard or a portable version of Sublime. A little googling around will help you. On Windows, it’s somewhere inside the %APPDATA% folder (%APPDATA%RoamingSublime Text 3Packages).

At this moment, cloning my repo provides me the following:
<ul>
<li>my user settings (e.g. trim whitespace on save, ensure new line at end of file, etc)</li>
<li>some code snippets for Javascript</li>
<li>several third-party packages:
<ul>
<li>SublimeLinter and a few linters to go along with it (jscs, jshint, scss-lint)</li>
<li>sass support</li>
<li>some color themes</li>
</ul>
</li>
</ul>

And if I add more or change anything, I can commit it to my repository and then I can update any installation I have with a simple git pull.
