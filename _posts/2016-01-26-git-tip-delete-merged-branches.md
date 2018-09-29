---
layout: post
title: 'git tip: Delete merged branches'
date: 2016-01-26 21:06:02.000000000 +01:00
parent_id: '0'
published: true
categories:
- Code
tags:
- bash
- git
author: Nikolaos Georgiou
---

If you want to delete your local branches that have already been merged to master remotely, run this in a bash shell:

```
$ git branch -D `git branch --merged | grep -v '*' | xargs`
```

This deletes all branches that are merged, except the currently checked out branch (that's the part with the start). So you should better run this <strong>while you've got the master branch checked out</strong>.

<strong>Update 2018-08-25</strong>: Powershell equivalent:

```

PS> git branch --merged | ? { $_ -notmatch '\*' } | ForEach-Object { git branch -d $_.Trim() }

```

A different way for bash:

```

$ git branch --merged | grep -v '*' | xargs git branch -d

```

Note that if you squash & merge (a popular option in GitHub and Bitbucket), then <code>git branch --merged</code> will not return these branches. In that case, try <code>git branch -l</code> but with the extra risk you might delete a branch you were still working on.

