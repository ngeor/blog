---
layout: post
title: Atom Keyboard Shortcuts
date: 2016-02-27 13:52:24.000000000 +01:00
published: true
categories:
- tech
tags:
- atom
- keyboard shortcuts
- productivity
---

It doesn't matter if you're using a simple editor or a full blown IDE, if you want to be more productive you have to spend time to learn some keyboard shortcuts. Here's a few keyboard shortcuts I use frequently when I work with Atom.<!--more-->

Most of the time, I work on Windows. Sometimes I switch to a Mac. The shortcuts tend to stay the same, the only difference is that you use the Command key (⌘) instead of Ctrl. But, unfortunately, there are exceptions. When I'm not mentioning otherwise, Ctrl should be replaced by Command on a Mac.
<h3><strong>General</strong></h3>
<ul>
<li><strong>Open your settings</strong> (Ctrl + ,)</li>
<li><strong>Open Command Palette</strong> (Ctrl + Shift + P). I often find myself typing Ctrl + Shift + P and then "invisible" to find the command "Toggle invisibles".</li>
</ul>
<h3><strong>Files</strong></h3>
<ul>
<li><strong>Close active tab</strong> (Ctrl + W)</li>
<li><strong>Open file</strong> (Ctrl + O)</li>
<li><strong>Open folder</strong> (Ctrl + Shift + O)</li>
</ul>
<h3><strong>Navigation</strong></h3>

I think these are the most useful ones, because they are the most frequently used when working on a project.
<ul>
<li><strong>Find file in project</strong> (Ctrl + P). Type Ctrl + P and then start typing the file name. Much faster than navigating using the tree. Every editor and IDE has this functionality these days.</li>
<li><strong>Find text in project</strong> (Ctrl + Shift + F).</li>
<li><strong>Find symbol in file</strong> (Ctrl + R). If you're editing for example a JavaScript file, a symbol can be a function. Typing Ctrl + R and the function name will take you to the definition of the function.</li>
<li><strong>Go to next linter error</strong> (Alt + Shift + .). This one requires the linter plugin and you can use it to fix linter errors one by one.</li>
<li><strong>Select all occurrences of symbol</strong> (Alt + F3 on Windows, Ctrl + ⌘ + G on Mac). Poor man's rename tool, it will select all occurrences of the selected symbol (e.g. variable name) within the active editor and as you start typing it will apply the new text everywhere.</li>
<li><strong>Reveal file in tree view</strong> (Ctrl + Shift + ). It will expand the tree view so that you can see the active file.</li>
<li><strong>Find modified file</strong> (Ctrl + Shift + B). This one is great. It works just like Ctrl + P but limits the search to the files you've modified (i.e. changed but not committed).</li>
</ul>
<h3><strong>Other</strong></h3>
<ul>
<li><strong>Toggle blame </strong>(Ctrl + B on both Windows and Mac). Requires the blame plugin and basically shows on the gutter of the editor who's to blame (or praise for that matter) for each line of code in the active file.</li>
<li><strong>Sort lines</strong> (F5). It requires the sort-lines plugin. Functionality I really missed in Atom but it's provided out of the box in Sublime Text, it just sorts the lines in the active editor (or selection).</li>
<li><strong>Run mocha tests</strong> (Ctrl + Alt + M on both Windows and Mac). Using the mocha-test-runner plugin, you can run your mocha tests without leaving the editor. Tip: If the cursor is on a single unit test line, it will only run that test.</li>
</ul>

Hope this helps!
