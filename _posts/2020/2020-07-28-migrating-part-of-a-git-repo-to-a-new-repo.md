---
layout: post
title: Migrating part of a git repo to a new repo
date: 2020-07-28 08:07:50 +02:00
tags:
  - git
---

I had created some tools inside a monorepo and I wanted to move them out
to their own repo, preserving the full commit history.

The repo has just one branch (master branch), which makes things a bit simpler,
and the project I want to move out is contained in its own folder.

## Step 1 - Clone the old repo

The old repo is called `monorepo` and the new one will be called `fancy-tool`.
Coincidentally, that is also the name of the subfolder where the code lives.

I'm cloning it out of my local working directory:

```
git clone monorepo fancy-tool
```

The local working directory will appear as the origin:

```
$ git remote -v
origin  C:/Users/ngeor/Projects/github/monorepo (fetch)
origin  C:/Users/ngeor/Projects/github/monorepo (push)
```

And I'm removing the origin with `git remote remove origin` to make sure I don't accidentally
push something at this point.

## Step 2 - Filter history

The following command needs to be run against the new local repo (`fancy-tool`). It will
rewrite the git history, keeping only the information that is relevant to the subfolder
`fancy-tool`. Additionally, that subfolder will become the root folder.

```
git filter-branch --prune-empty --tag-name-filter cat --subdirectory-filter fancy-tool -- --all
```

## Step 3 - Delete tags that are irrelevant

I didn't have any branches, other than the master branch, but I did have some tags.
I had to go over them to make sure I delete tags that are not relevant anymore (with `git tag -d`).

At this point I also run `git gc && git prune` (because the internet said so,
not 100% sure if it's needed).

## Step 4 - Push to new remote

The repo is ready, time to share it with the world. I created a new repo in
GitHub. The important thing here is to make sure it gets created with no
commits (i.e. opt out of the README file when creating the repo).

```
git remote add origin repo-url
git push -u origin master
git push --tags
```

## Step 5 - Remove from original repo

Now that the `fancy-tool` repo has its own home, I wanted to remove it from
its old place in the `monorepo`. This requires rewriting the history of an
existing public repo, which would have been difficult on the other users,
had there been any.

```
git filter-branch --tree-filter "rm -rf fancy-tool" --prune-empty HEAD
git push --force-with-lease
```

As before, I had to get rid of the irrelevant tags, but this time I also had
to remove them from origin (so not only `git tag -d` but also `git push --delete origin`).
