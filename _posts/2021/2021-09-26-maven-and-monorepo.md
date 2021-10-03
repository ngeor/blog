---
layout: post
title: Maven and monorepo
date: 2021-09-26 07:47:00
tags:
  - maven
  - monorepo
---

In this post, I'm playing with releasing a subset of libraries
from a Maven monorepo.

Nothing simpler that a git repo that contains just one Maven project without Maven modules.
Everything is simple: versioning, releasing, creating the automatic CI/CD pipeline...
until the time when the second project comes.

If the second project is totally unrelated
to the first one, you might as well create a second git repository. Arguably, some copy pasting
will be annoying, e.g. copy pasting the CI/CD pipeline, setting up again the credentials
required to authenticate against the remote Maven repository. But it's not the end of the world.
Maybe with some tooling, you can even coordinate things like upgrading common non-functional
stuff like checkstyle.

On the other hand, if the second project depends on the first one, things are a bit more
difficult. The change cycle is longer. You need to first implement the change on the first project, publish it to the Maven repository, consume it on the second project. If a mistake
was made, you need to make a patch release on the first project. There's more ceremony.

A monorepo starts to sound like a better solution. Setup one and only one git repository
where all your Maven projects live, under a common parent Maven project. Life is good again,
all source code is at your fingertips and you can change multiple libraries in a single commit.

But then you need to publish your libraries to a remote Maven repository (because they're so awesome).
And now versioning becomes a bit more complicated.

Let's see what happens if we use the [maven release plugin](https://maven.apache.org/maven-release/maven-release-plugin/). Preparing the release with `mvn release:prepare` will
do the following:

- interactively ask for the next release version for each library
- interactively ask for the next snapshot version for each library
- interactively ask for the git tag
- create a commit with the release versions and tag it
- create a follow-up commit setting the snapshot versions

Performing the release with `mvn release:perform` will deploy the release versions to the
remote Maven repository.

The thing is, this will deploy _all_ of the libraries. If your monorepo contains
multiple libraries, which are all related (think of Spring for example, or Jackson), then
maybe this is perfect for you. Your libraries all form a logical product,
so it makes sense to release them all in one go, even if there haven't been any changes
to some of them. The versioning will probably be simple as well, one version number
for everything in the monorepo.

But in a monorepo where libraries are not necessarily related to each other,
this doesn't scale well.
You'll have to answer a lot of questions if you want to have control over the versions. You can also skip
the excessive interrogation with `-B` for batch mode, but then all versions will be
automatically chosen (if using SemVer policy, it will bump a minor version).

Deploying all of your libraries, even if they had no changes since their
last release, might be confusing to your users, who might be wondering why they
need to upgrade at all.

In my search for a better approach, I found two nice links:

- [Maven In A Google Style Monorepo](https://paulhammant.com/2017/01/27/maven-in-a-google-style-monorepo/)
- [Open Source Libs - Maven - Monorepo](https://opensourcelibs.com/lib/logiball-monorepo)

The motivation behind the first article is sparse checkouts and git performance when you're dealing with a huge monorepo
that tests the boundaries of git. But the trick we're using is the same: modify the parent pom file, keeping only a subset of
the modules we are interested in.

An interesting detail is that they don't commit `pom.xml` files at all into the monorepo, to avoid git noise.
They commit `pom.xml.template` files, which are used to auto-generate `pom.xml` files based on the desired
Maven modules and version numbers.

In [my repo](https://github.com/ngeor/java/tree/v1.10.0), I already have `pom.xml` files and I didn't want to remove them for now, but I think
the template approach they're taking is better.

I hacked together [some code](https://github.com/ngeor/java/tree/v1.10.0/apps/yak4j-cli) to automate this (works on my machine), but the principle is the following:

- Make a backup of the parent `pom.xml` in case things go wrong
- Make sure we're on the default branch and there aren't any pending changes
- Create a branch for the release
- Modify the parent `pom.xml`, keeping only the modules we want to release
- Commit the `pom.xml`
- Prepare the release with `mvn release:prepare`. This will create two commits, one with the release versions
  and one with the next snapshot versions. The first commit will be tagged and the command will
  push the tag to the remote git repository.
- Have a CI job pick up the pushed tag from the previous step and deploy to the remote Maven repository.
  When the job finishes, you have published your Maven artifacts.
- Modify again the parent `pom.xml`, putting back all the modules.
- Because the version of the parent `pom.xml` has changed, we need to fix that version in all
  child modules that were previously excluded from the parent pom (you might want to write
  some tooling for that).
- Commit the modified `pom.xml` files, merge the release branch into the default branch and delete it

Bonus: in the era of `gofmt`, `rustfmt`, etc, I like formatters that are opinionated and are _not_ configurable.
I keep `pom.xml` files sorted with a Maven plugin:

```sh
mvn com.github.ekryd.sortpom:sortpom-maven-plugin:sort \
  -Dsort.createBackupFile=false
```

How can this be improved further?

- First of all, dependencies. If a library has changed, it is probably a good idea
  to automatically publish any libraries that depend on it.
- Second, I shouldn't even have to tell it which libraries have changed. It should
  go through git history, since the previous release, and figure out what paths
  have changed.
- Finally, changelog. It should be possible to go over the git history and
  create a somewhat organized changelog, dividing the changes by affected library.
