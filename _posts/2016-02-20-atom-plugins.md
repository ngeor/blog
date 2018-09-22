---
layout: post
title: Atom plugins
date: 2016-02-20 13:07:29.000000000 +01:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags:
- atom
- plugins
author: Nikolaos Georgiou
---

I've switched to Atom as my main editor for some time now. In this post, I want to go over some plugins I use.<!--more-->

The most useful ones revolve around linting, because they let me see immediately within the editor if I'm following the rules. The base plugin is called <strong>linter</strong>. It doesn't lint anything, it just provides the framework that all linters depend on. On top of it, you have all sorts of pluggable linters:
<ul>
<li><strong>linter-jscs</strong> and <strong>linter-jshint</strong> for JavaScript</li>
<li><strong>linter-scss-lint</strong> for Sass. This one uses the ruby version of sass. You can also use <strong>linter-sass-lint</strong> which is the pure node approach.</li>
<li><strong>linter-js-yaml</strong> for Yaml</li>
<li><strong>linter-jsonlint</strong> for JSON files</li>
<li><strong>linter-markdown</strong> for Markdown text.</li>
</ul>

Specifically for jscs, I want to mention also the<strong> jscs-fixer</strong> plugin. This one allows you to run jscs --fix on your files, autofixing most of the style issues.

In the area of formatting, there's also <strong>xml-formatter</strong>, that beautifies your XML files. This plugin isn't perfect. For example, I don't like that is squashes multilines comments into a single line. But it can be useful.

<strong>sort-lines</strong> and <strong>file-types</strong> provide some functionality that Sublime Text has but Atom doesn't. With sort-lines, you can sort the selected lines by pressing F5. With file-types, you're able to associate custom file extensions to a file type.

<strong>blame</strong> is a nice one, if you're working with git. It shows in the gutter of the editor who is responsible for the code changes. If you hover over, you can see also details about that git commit.

There's also <strong>todo-show</strong>, which does a good job collecting all of your inline comments marked as TODO, FIXME, HACK, etc and shows them on the right side.

Finally, I also have <strong>mocha-test-runner</strong> installed. This one can be a bit flaky on Windows currently. What it does? It runs mocha unit tests from within the editor. That can be useful, although perhaps you can be more productive with a terminal and a watch task that runs the unit tests automatically.
