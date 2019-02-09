---
layout: post
title: On versioning
date: 2017-12-18 19:20:55.000000000 +01:00
published: true
categories:
- notes
tags:
- GitVersion
- versioning
- notes
---

According to <a href="https://en.wiktionary.org/wiki/version" target="_blank" rel="noopener">Wiktionary</a>, the word version means "a specific form of variation of something". In computing, it's "a particular revision of something" (e.g. software). The word has French and Latin roots. The Greek translation, <em>έκδοση</em>, can also be translated as <em>publication</em>.

<!--more-->

If we examine the history of Microsoft Windows, we can see many examples of versions. We can see numeric versions, like Windows 3.11 and Windows 95 but also text versions like Windows XP. These versions are <strong>customer facing</strong>, but they have corresponding <strong>internal versions</strong> (e.g. Windows 7 is really NT 6.1) and even <strong>build numbers</strong>.

Ubuntu's versions are derived from the <strong>release schedule</strong>. Version 17.04 for instance was released on April 2017. The versioning is accompanied by a playful adjective-noun description, e.g. 17.04 is nicknamed Zesty Zapus.

I can't remember if it was Chrome or Firefox, but it was one of these browsers that changed the version into something the customer shouldn't care about. By having frequent updates and adding features quickly, <strong>the version became a technicality</strong>, something you should only care about if things go wrong. You just run Chrome, latest and greatest. That was dubbed the "evergreen browser".

When can see something similar to that when we talk about <strong>agile and continuous delivery</strong>. We talk about fast iterations that add a little bit of value to the customer. It's important to be able to implement and test business ideas fast, before they become irrelevant. If we think about web applications, versioning is even more concealed. What version of Facebook or BBC News are you running now?

From the developer's point of view, versions are still very relevant. When developing an application or a website, you depend on 3rd party libraries which need to have a proper versioning strategy. When developing a library for others, you need to be communicating clearly if there are new features or breaking changes.

<strong>SemVer</strong> (semantic versioning) is a nice effort to standardize the way we talk about versions. SemVer defines a version as a sequence of three numbers (or components): major.minor.patch. You change major for big features and breaking changes, minor for regular or small features and patch for bugfixes. If done correctly, this allows people to upgrade their libraries responsibly, knowing that if they just upgrade to the latest minor upgrade, nothing will be broken. In reality, this depends on how diligently each library maintainer adheres to SemVer. It's not unusual to have unexpected breaking changes by a minor upgrade. This doesn't mean SemVer is wrong, it just means we need to be careful when we have the role of a library maintainer.

Branches make versioning a bit more complicated. Essentially <strong>a branch is an extra dimension</strong> in the product's lifeline, a product from a parallel universe. If you want to offer a branch to the customer, you'll need to be able to version that too. When practicing GitHub Flow, we should take each feature branch to production. If the release is successful, we merge to master; if it fails, we rollback by redeploying master. SemVer takes care of this need with pre-release versions and metadata. In a <a href="{{ site.baseurl }}/2017/12/02/cd-with-helm-part-5-versioned-artifacts.html" target="_blank" rel="noopener">recent post</a>, we implemented this with using major.minor.patch for the master branch and major.minor.patch-gitSHA for the feature branches.

The question of <strong>how to implement versioning</strong> is an interesting one. I had mentioned some ways in <a href="{{ site.baseurl }}/2016/08/20/automatic-versioning-of-npm-packages.html" target="_blank" rel="noopener">an old post</a>, but I'll rewrite it here a bit better with some more ideas.

Option 1: <strong>use a version file</strong>. In this case, the version is stored in Git in a special file. This can be an existing file, specific to the technology you're using, e.g. <code>package.json</code>, <code>AssemblyInfo.cs</code>, <code>pom.xml</code>. It can also be a simple text file. Developers need to manually bump the version when they work on a new feature. This can slow things down on a fast delivery environment, giving people annoying merge conflicts on the version file, but it gives full control.

Option 2: <strong>use an automatically generated sequence by the CI server</strong>. In this case, the CI server generates a build number for each build. Most build servers allow you to use a custom sequence, like 1.1.NNN. The downside here is that if you want to bump the major or minor version, you need to reconfigure the build plan. This is more suitable for customer facing products (e.g. a website) with rapid deployments, where the version makes little difference. The upside is that the developer doesn't have to do anything.

Option 3: <strong>mix and match of the two options above</strong>. In this setup, the version file drives the important things (major and minor version), while the CI server's build number sequence is used to fill-in the patch component. In this setup, you can bump the version when you feel you need to, but it's on autopilot otherwise.

Option 4: <strong>derive the SemVer from the source code's history</strong>. This is a declarative approach, where we can use a tool named <a href="https://github.com/GitTools/GitVersion" target="_blank" rel="noopener">GitVersion</a> to calculate the correct version for us. GitVersion uses only git elements such as tags, commit messages and branch names to do its calculation, which means it can be applied to any repository (although it's rather .NET oriented). I'll show this in details in a next post.

When picking your versioning strategy, make sure it fits your needs. I'm typically talking about web applications and GitHubFlow, but that might not work if you need to support multiple versions of the same product (e.g. a library or a desktop application).

Pay also attention to the way developers are using it. If it's causing unnecessary commits like "bumping version", you should reconsider if it's working out. And of course, you need one and only one version that identifies all your artifacts consistently, without having to doubt which version is where.
