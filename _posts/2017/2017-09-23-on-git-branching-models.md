---
layout: post
title: On git branching models
date: 2017-09-23 09:26:34.000000000 +02:00
published: true
categories:
- notes
tags:
- branching model
- continuous integration
- developers
- git
- Git Flow
- GitHub Flow
- notes
---

Usually, when you work with a version control system like git, development happens in multiple branches. It's funny to see people's faces when you tell them that the author of Continuous Delivery, Dave Farley, advocates "no branches". I had that same surprised face myself the first time I heard that concept. But, so far, I haven't really worked somewhere where no branches were used.

<!--more-->

There are two popular branching models out there: the Git Flow and the GitHub Flow. They are unfortunately similarly named but they're quite different (also, for a lot of people, GitHub and Git are synonymous, a testimony to GitHub's success).

A branching model is a process that should answer questions like:
<ul>
<li>in which branch does the latest production code live?</li>
<li>where should a developer work for a regular feature? Meaning, where does he/she branch off, what should that branch's name be, how to merge that branch back so it goes to production, etc</li>
<li>how to release to DTAP? Are there separate branches for this?</li>
<li>how to deal with emergencies (hotfix, roll-back, roll-forward)?</li>
</ul>

Let me stop right here for a public service announcement: <strong>please, do not invent a branching model</strong>. Just pick one of these two. I seriously doubt that you are special enough to justify inventing your own branching model. If you are, I will apologize as soon as your branching model reaches the same popularity to Git Flow and GitHub Flow. Please, use a standard branching model, one that a junior developer will actually benefit from learning and that a senior developer will already know.

By inventing your own branching model, I also mean things like: "we use Git Flow, <strong>but</strong>, ...". As any fan of Game of Thrones can tell you, <em>everything before the word "but" is horseshit</em>. It is common with young developers to want to reinvent wheels, because it's fun to do so. It might also be the case that with a custom branching model, you're trying to work around organizational inflexibilities, which have nothing to do with software, which brings us back to Conway's Law. That can be much harder to fix than dealing with overenthusiastic developers.

Now, back to the two popular branching models. What's the difference and which one should you pick? The main difference has to do with releases. In <strong>Git Flow</strong>, the release is a strong concept, which deserves its own branch. Cutting a release means branching out of the mainline branch and doing all sorts of things there to get the release to production, while development work continues in the mainline branch. If you are familiar with continuous integration, your spider sense might be tingling. Branches are equivalent to isolation, the opposite of integration. Having long standing open branches is an invitation to merge conflicts and confusion.

In <strong>GitHub flow</strong>, life is simpler. There are no release branches. The mainline branch (typically called master in Git) is all there is. If you want to release to production, there's master. If you want to start working on something, branch out of master, merge back to master. It's a very simple model.

Why would someone then prefer Git Flow over GitHub Flow? Well, let's go back to the reason you typically want to have a release branch. The typical reason has to do with confidence, or the lack thereof. You want a frozen release branch so that you take your time to validate that all the features in there work as expected on various environments. Maybe the process of putting the code on these environments is cumbersome and has also manual configuration steps which are not part of the code. Maybe manual testing is required. Maybe the code is actually spread over various code repositories that need to be aligned. Maybe you need to login to production to perform some manual step before/after deployment. <strong>In that sense, Git Flow is a workaround for other things that are missing or broken</strong>.

GitHub Flow on the other hand works best when you've solved these problems first. GitHub Flow works best when you have a delivery pipeline that includes several confidence checks, such as linting, unit testing, code coverage, integration testing, performance testing, error log monitoring, etc. It works when each feature you want to deploy is atomically contained within the feature branch: code and configuration. This has further implications that you have the proper tooling to apply the configuration to all necessary environments, predictably and without human intervention. <strong>The reason GitHub Flow is so simple is because the investment in automation to make it work is so big</strong>. But once you have that investment in place, you can have a junior developer write a feature and send it to production on his/her first day at work. No release trains, no merge conflicts.

Going back to the "no branches" idea by Dave Farley. It definitely sounds scary and he admits it's the most controversial thing in his book. However, with the previous comparison of the branching models, you could argue that working directly on master branch is a natural evolution of GitHub flow. You could argue that the complexity of the branching model is inversely proportional to the confidence of the delivery pipeline. As the confidence reaches infinity, the branching model collapses to zero.

Of course, there's always room for improvement to reach infinite confidence. But there are other aspects around accepting code into the mainline branch, aspects that an automated delivery pipeline can't possibly detect and humans are therefore needed: does the code fit in the architecture? Is it well documented? Is it elegant? To answer that, you need a branch and a code review. I can imagine that, without branches, you'd have to do a peer code review before committing, probably also do some pair programming to have early agreement on how to tackle a problem, and finally do small commits. Maybe in order to reach "no branches", you need to master not only a perfect delivery pipeline, but also a perfect development team, at least in terms of collaboration and possibly also in terms of skills.
