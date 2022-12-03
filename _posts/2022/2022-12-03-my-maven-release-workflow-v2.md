---
layout: post
title: My Maven release workflow v2
date: 2022-12-03 07:53:17
tags:
    - maven
    - GitHub Actions
    - changelog
    - ci tooling
---

An update on my Maven release workflow, in other words, how I release
Maven libraries into the Maven central repository.

This is a followup from the [previous post]({% post_url 2022/2022-02-05-my-maven-release-workflow %}).

I haven't updated the blog a lot lately but also I haven't been coding much in something new, so
there isn't much to update. The most coding I did at home was in Rust, and that was trying to
refactor some parts in [rusty-basic](https://github.com/ngeor/rusty-basic), no new features.

However, I did make some changes in how I (seldom) release my Java libraries into the Maven
central repository.

- Instead of using a specially named branch as the CI pipeline trigger, I use a tag.
  So instead of a branch named `release-x.y.z`, the release starts with a tag `vx.y.z`.
- Not using the Maven release plugin anymore. I find it a bit difficult to work with,
  so I've stopped using it. I wrote a [custom tool](https://github.com/ngeor/krt) to
  replace it, which switches from snapshot to release version, generates the changelog
  with [git-cliff](https://github.com/orhun/git-cliff), pushes the tag, and finally
  switches back to the snapshot version. The tool supports also npm and python projects
  (then again, like I said, I haven't been using the tool a lot lately).
  When deploying to the Maven central, I just run `mvn deploy`.

The previous approach with the release branch would run all the release ceremony on the CI server,
while with this the release is kicked off on a local laptop.

In terms of running commands, in the previous approach it would be something like:

```
git checkout -b release-1.2.3
git push -u origin HEAD
```

and then wait until the release is magically done on the CI server.

In the new approach, using the custom tool I mentioned before:

```
krt --type=maven minor
```

which will prepare the release (changelog, changing the `pom.xml`, creating the git tag) locally and then
push to the remote where the CI pipeline on the tag will deploy to Maven central.

The downside is that it requires some tooling to be present on the local machine (git-cliff and the krt tool)
but on the positive side the CI pipeline is less complicated.

I still have a Python script copy pasted across every single Java library project which performs
the release on the tag pipeline, which I would like one day to move to a central point to avoid duplication.
