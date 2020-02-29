---
layout: post
title: Slim GitVersion Docker image
date: 2018-08-19 08:47:04.000000000 +02:00
published: true
tags:
- docker
- GitVersion
---

In a previous post, I wrote about <a href="{{ site.baseurl }}/2017/12/19/semantic-versioning-with-gitversion.html">GitVersion</a>. GitVersion is a tool which solves semantic versioning of a git repository in its own way. With GitVersion, the version of any git repository is a pure function of its state, derived by tags, branches and commit messages.

<!--more-->

GitVersion is built on .NET Framework (not .NET Core). Running it on a modern CI environment is possible, as a <a href="https://hub.docker.com/r/gittools/gitversion/">Docker image</a> is available. For example, to see the semantic version of a repo you can run:

```
docker run --rm \
    -v $(pwd):/repo \
    gittools/gitversion /showvariable SemVer
```

The only problem is that the official image is a bit large, weighing in at 493MB.

I've managed to slim that down significantly at 85MB, by installing only the necessary mono libraries (with some trial and error).

My fork is <a href="https://github.com/ngeor/GitVersion">here</a> and the Dockerfile is called <a href="https://github.com/ngeor/GitVersion/blob/master/Dockerfile-slim">Dockerfile-slim</a>. You can use my <a href="https://hub.docker.com/r/ngeor/gitversion/">slim GitVersion image</a> simply by replacing the "gittools" with "ngeor" in the above command:

```
docker run --rm \
    -v $(pwd):/repo \
    ngeor/gitversion /showvariable SemVer
```

This makes it a bit easier to use this tool. However, porting it to .NET Core might be a better solution overall.
