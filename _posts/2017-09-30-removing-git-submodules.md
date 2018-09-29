---
layout: post
title: Removing git submodules
date: 2017-09-30 10:36:39.000000000 +02:00
parent_id: '0'
published: true
categories:
- Tech Notes
tags:
- git
- submodules
author: Nikolaos Georgiou
---

Submodules is an advanced git feature. It allows you to have a folder inside your repository which serves as a link to a different repository. Working with submodules is more complicated and I haven't had a real need for it so far. Last week I had to deal with a codebase which was doing heavy usage of submodules, but without a good reason, so I got rid of them.

<!--more-->

First of all, what was wrong with the usage of those submodules? The main repository, together with its submodules, was essentially a single piece of software, it was a single website, a single unit. The submodules represented different parts of the website, sure. But these submodules weren't and couldn't be reused in other git repositories. The division into submodules didn't add value over a division into regular folders.

Features could span across multiple submodules as well. This means that a single feature (e.g. migrate from http to https) needed multiple pull requests (one per submodule). Think about the poor developer who'd have to create and maintain all these PRs. Verifying the feature was also cumbersome, let alone what would happen if you would have to revert one of the pull requests.

The build system also had to be more convoluted. Each submodule was defining a similar (almost identical) build system, consisting of basic things like linting and unit testing. Configuring the build server also meant configuring as many build plans as the submodules.

Sometimes, more than often I'm afraid, developers overcomplicate things. They also tend to defend their work based on emotion, not reason. We're all guilty of that I suppose.

Luckily, this gordian knot was not too difficult to cut. This <a href="https://github.com/jeremysears/scripts/blob/master/bin/git-submodule-rewrite" target="_blank" rel="noopener">handy bash script</a> takes the history of the submodule's mainline branch (e.g. master) and integrates it into the parent repository. The folder structure does not change at all, so for the developer (and for the build & deployment scripts) nothing changes at first sight. But what was once a submodule becomes a regular folder. History is preserved (for the mainline branch only).

One extra complication had to do with old branches. The whole setup in this particular case was favouring long standing branches sitting in isolation. Migrating only the mainline branch from each submodule means that those old branches were left behind. In general, long standing branches is an invitation to trouble, but this was multiplied by the number of submodules. What I found as a solution was to temporarily add the submodules as remotes to the main repo and cherry-pick from the old branches. It worked better than I hoped, so history was preserved in this case as well.

This small change brings great gains in productivity. The code base became unified under a single repo. The developer now can just create a single branch and a single PR. No need to commit SHAs, no need to coordinate multiple PRs and make sure they all get merged at the same time. No need to explain all this information to a new developer. The build system can get simpler as well. Imagine doing npm install on 1 folder instead of 5, maintaining one grunt file instead of 5, and so on.

How can developers work with such a bureaucratic system? Well, people get used to things. If you work for something for a long time, you get a used to it and you no longer see it as a problem. It's just a human thing, not exclusive to developers. Developers' lack of skills might also be a reason. Another reason can be the culture within a company regarding change, ownership, initiative. I find that non technical reasons are often the real case for technical problems.

So when should you use submodules? In all honesty, I do not know and I haven't thought of it. I haven't worked in a project that justifies the complexity. Git has a lot of advanced features, but we need to remember that Git was created to fit the needs of the Linux kernel. It might be that your project is simpler.

If you really need to break down a monolith project into pieces, that's fine. Think about dependencies between them, think about deployment and think about how often each piece is expected to change. In any case, instead of submodules, think about creating versioned packaged dependencies (npm for nodeJS, NuGet for .NET, etc). That might be a better, simpler solution.

Keep it simple, stupid.

