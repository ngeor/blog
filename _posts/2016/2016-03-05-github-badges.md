---
layout: post
title: GitHub badges
date: 2016-03-05 07:57:36.000000000 +01:00
published: true
categories:
- programming
tags:
- badges
- david
- GitHub
- JavaScript
- markdown
- nodejs
- open source
- shields.io
- travis
---

You may have noticed that a lot of GitHub projects have some badges in their homepage, showing for example the status of their latest build. For a node (JavaScript) project, you can use a few more badges to show the world that everything is in order.<!--more-->

Let's start with the <strong>build status badge</strong>. That badge is typically coming from <a href="https://travis-ci.org/" target="_blank">Travis</a> when we're talking about open source projects in GitHub. That's because Travis is a free CI service for open source projects and it has a very good integration with GitHub.

Here you can see my Travis homepage. It automatically connects to GitHub and picks up my projects. You can choose for which of your projects you'd like to enable Travis.

<img src="{{ site.baseurl }}/assets/2016/travis-projects.png" />

In the next screenshot, you can see an example of a failed build.

<img src="{{ site.baseurl }}/assets/2016/travis-failed-build.png" />

The badge I'm talking about sits on the top. It's next to the header and it says "build failing". That's pretty clear that something needs to be fixed in this project! <strong>Side note:</strong> this project is called <a href="/2015/09/introducing-generator-csharp-cli-app/" target="_blank">generator-csharp-cli-app</a> and I'll be using that name for the rest of the blog post <strong>just as a placeholder</strong>. Just replace it with your own project name.

How do we add this badge to the project's homepage in GitHub? That's typically done in the README.md file. Click the badge on the Travis page and a popup will appear. In there, select "Markdown". Markdown is the popular formatting language that GitHub also uses. Just copy paste that markdown code into your readme file, usually just below the title so that it appears on the top.

<img src="{{ site.baseurl }}/assets/2016/travis-markdown.png" />

Travis supports many technologies and languages, so this badge isn't really JavaScript specific. If you're using GitHub for your open source projects, I'd definitely recommend giving Travis a try and setting it up.

The next badge is specific to JavaScript projects: the <strong>node dependencies status badge</strong>. This one comes from a service called <a href="https://david-dm.org/" target="_blank">David</a>, a service that is watching your node.js dependencies. If your dependencies are up to date, you get a green badge. This badge is useful because it offers an indication of how well a project is being maintained.

Just like Travis, David integrates well with GitHub. The markdown code is also similar:

```
[![Dependency Status](https://david-dm.org/ngeor/generator-csharp-cli-app.svg)](https://david-dm.org/ngeor/generator-csharp-cli-app)
```

Clicking the badge takes you to David's page that tells you in details what's wrong with the dependencies:

<img src="{{ site.baseurl }}/assets/2016/david.png" />

The final badge is relevant to node.js projects that publish npm packages: the <strong>npm version badge</strong>. You'd like to tell the world perhaps what your current version is and link to the npm page as well?  You can use a service called <a href="http://shields.io/" target="_blank">shields.io</a> for that badge. It supports all sorts of other badges as well, but I haven't explored them yet. The markdown code for this badge would be:

```
[![npm version](https://img.shields.io/npm/v/generator-csharp-cli-app.svg)](https://npmjs.org/package/generator-csharp-cli-app)
```

Putting all these badges together, you get a nice homepage for your project:

<img src="{{ site.baseurl }}/assets/2016/readme.png" />

Hope this helps! Now, it looks like I have some red badges to fix :-)
