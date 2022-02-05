---
layout: post
title: My Maven release workflow
date: 2022-02-05 07:33:40
tags:
    - maven
    - GitHub Actions
    - changelog
    - ci tooling
---

In this post I'm describing my current setup regarding releasing
a versioned library into Maven central repository.

## Initiating the release

The release starts from the default branch. There shouldn't be any
pending changes. The version in the `pom.xml` must be a snapshot version.
To trigger the release, I **create and push** a new branch named `release-x.y.z`,
where `x.y.z` is the version that I want to release. This branch pattern
is picked up by a dedicate GitHub Actions workflow which does the work.

To create and push the branch, I use a Python script (`release.py`) which
I also to perform and finalize the release. So for this first step, I run
something like `./scripts/release.py initialize --version x.y.z`.

## Performing the release

The release is done through a GitHub Action. The custom `release.py` script
does all the work, which is a lot:

- **Determine the release version**. It checks the environment variables
  `GITHUB_REF_TYPE`, which must be set to `branch`, and `GITHUB_REF_NAME`,
  which must follow the pattern `release-x.y.z`.
- **Import a GPG key**. In order to publish to the central Maven repository,
  there's a process which I have long forgotten (not as easy as publishing
  to npm), which involves having your own GPG key. I store the key as a file
  in the repo in a secure way. To import and use the key, I need to configure
  two secrets in GitHub: `GPG_KEY` and `GPG_PASSPHRASE`. This also needs the
  `gpg` binary to be present on the system.
- **Configure git identity**. Since we're going to be making a few commits,
  `git` needs to know who we are. The script just runs `git config user.name "My name"`
  and `git config user.email "My email"`.
- **Preparing the release**. This uses the Maven release plugin and runs the `release:prepare`
  goal. I am passing `-DreleaseVersion=x.y.z` to use the version I indicated when I created
  the release branch. Also, `-DpushChanges=false`, because the plugin has some difficulty
  pushing when running through GitHub Actions which I didn't want to dive into. When this step
  finishes, there are new commits on the current branch and a new git tag. The first commit
  switches from snapshot to release version (e.g. from `1.2.3-SNAPSHOT` to `1.2.3`) and then
  the next switches to the snapshot version of the next iteration (e.g. `1.3.0-SNAPSHOT`).
- **Update the changelog**. I use [git cliff][] to automatically generate a changelog stored in the
  git repo as `CHANGELOG.md`. This is a good opportunity to do so, as we just got a fresh tag
  and we haven't pushed the changes yet. I install git cliff in an eariler step of the
  GitHub Action by curling the latest release and extracting it somewhere in the `PATH`. Another
  important point, for git cliff to work, the checkout action needs to fetch all commits
  with `fetch-depth: 0`, otherwise the changelog will be empty.
- **Push changes** to the current branch. This is apparently supported out of the box in GitHub Actions,
  a pleasant surprise. It also doesn't result in an some infinite loop of workflows being executed.
  Simply run `git push --follow-tags` (to also push the tag created by the Maven release plugin).
- **Perform the release**. This uses again the Maven release plugin but this time runs the `release:perform` goal. The script creates dynamically a Maven `settings.xml` file which
  contains my credentials for the Maven central repository server (stored also as GitHub secrets)
  and the GPG secrets as properties `gpg.keyname` and `gpg.passphrase`. The server id in the `settings.xml` needs to match the server id in my `pom.xml`'s `distributionManagement` section,
  as well as the `nexus-staging-maven-plugin` `serverId` property. I pass `-DlocalCheckout=true`
  to the `release` plugin so that it doesn't attempt to clone anything from GitHub.
- **Clean up**: delete the GPG key.

## Finalizing the release

Meanwhile, on my computer, I just wait for the pipeline to finish. I get
an e-mail from Sonatype saying that it has analyzed my release and hasn't
found any vulnerabilities. At this point, my release is done. I need to
merge the release branch and delete it. I use the same `release.py` script
for it and run `./scripts/release.py finalize`.

## Show me the code

- [release.py](https://github.com/ngeor/java/blob/v3.1.1/scripts/release.py)
  The custom Python script to orchestrate all the above.
- [release.yml](https://github.com/ngeor/java/blob/v3.1.1/.github/workflows/release.yml)
  The GitHub Action workflow.
- [pom.xml](https://github.com/ngeor/java/blob/v3.1.1/pom.xml)

## Painpoints

Some of the complexity probably comes from Maven's notion of snapshot and release
versions, but I wanted to follow that convention.

One obvious problem is that it's very easy to make a mistake in the version, e.g. push a branch like `release-30.0.0` instead of `release-3.0.0`.

Furthermore, this probably only works for a team of one. It's fine for me and my hobby
project, but if you have two people, it doesn't offer any protection from two people
accidentally trying to create a release (one person thinking they should be pushing version `1.2.3`
as a hotfix and another person thinking they should be pushing version `1.3.0` as a minor version).
Essentially, the choice of the version number is outside the approval process. The person who initiates the release can do so if they have the right to push a branch, without double checking
with someone else.

[git cliff]: https://github.com/orhun/git-cliff
