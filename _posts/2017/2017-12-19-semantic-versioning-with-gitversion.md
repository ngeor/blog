---
layout: post
title: Semantic versioning with GitVersion
date: 2017-12-19 21:07:41.000000000 +01:00
published: true
tags:
  - blog-helm-sample
  - GitVersion
  - TeamCity
  - semantic versioning
  - versioning
---

I recently stumbled upon a tool called
<a href="https://github.com/GitTools/GitVersion" target="_blank">GitVersion</a>
which takes a different approach on versioning. I already mentioned some
<a href="{{ site.baseurl }}/2017/12/18/on-versioning.html" target="_blank">options
regarding versioning</a>, but all of them require you to actively specify the
version somewhere. GitVersion instead is able to calculate it based on the state
of your git repository.

<!--more-->

This requires some getting used to, but GitVersion is like a pure function that
calculates the semantic version of any given commit based on three things:

<ul>
<li>the nearest tag</li>
<li>the commit messages between this commit and the nearest tag</li>
<li>the name of the branch</li>
</ul>

It can be configured with a yaml file and it supports branching models like
GitFlow and GitHubFlow. I will only discuss GitHubFlow here. Before going into
technical details, I'll show some examples of how GitVersion calculates the
semantic version.

Our starting point is the <strong>master branch</strong>, which is already
tagged as v1.2.3. If we run GitVersion, it will see we're on a tag, so its job
is done. It will report that the semantic version on that commit is 1.2.3.

Let's say that we want to <strong>work on a new ticket</strong>. We branch out
of master, which is tagged as v1.2.3. The branch name is BH-42-add-header. We
start working and we commit to the branch with a message like "BH-42 adding
header for blog-helm project" (always add ticket numbers to your commit
messages). GitVersion now needs to traverse history to find the nearest tag,
which is 1.2.3. The next version should be 1.2.4, but we're on a feature branch,
so GitVersion gives something like <code>1.2.4-BH-42-add-header.1</code>. This
is the next version plus the branch name plus the number of commits from the
tag.

What if we want to <strong>change the minor or major version</strong>? This is
done by adding special text in the commit message (or messages). By default,
that's <code>+semver: major</code> for bumping the major version and
<code>+semver: minor</code> for the minor version. If we add a new commit with a
message like "BH-42 making the header responsive +semver: minor", then
GitVersion will report the version <code>1.3.0-BH-42-add-header.1</code>.

What happens if we <strong>merge this feature branch</strong>? Assuming we don't
corrupt the commit messages during some rebase/squash/other, everything should
be fine. GitVersion will traverse master's history up to the tag 1.2.3 and
determine that the version is 1.3.0 (without the branch suffix, as that's only
for feature branches).

It's important to <strong>tag</strong> once we have a successful build in the
master branch. You're probably doing this already anyway. It makes the life of
GitVersion easier, because it has less commits to traverse in order to evaluate
the version.

Let's do some hands on work. I'll modify
<a href="https://github.com/ngeor/blog-helm" target="_blank">blog-helm</a>, the
project I used in the
<a href="{{ site.baseurl }}/cd-with-helm.html" target="_blank">CD with Helm
series</a>, to use GitVersion. First, in order to install GitVersion you can use
chocolatey (<code>choco install GitVersion.Portable</code>) or brew (<code>brew
install gitversion</code>). It is written in .NET so it will pull in mono on
your Mac. On TeamCity, I'll be using the Docker image
<code>gittools/gitversion</code>.

Once it's installed, we need to configure the repo with <code>gitversion
init</code>, which offers a configuration wizard (this is only needs to happen
the first time you introduce GitVersion):

```
PS [master ≡]> gitversion init
Which would you like to change?

0) Save changes and exit
1) Exit without saving

2) Run getting started wizard

3) Set next version number
4) Branch specific configuration
5) Branch Increment mode (per commit/after tag) (Current: )
6) Assembly versioning scheme (Current: )
7) Setup build scripts

> 2

The way you will use GitVersion will change a lot based on your branching strategy. What branching strategy will you be using:

1) GitFlow (or similar)
2) GitHubFlow
3) Unsure, tell me more

> 2

By default GitVersion will only increment the version when tagged

What do you want the default increment mode to be (can be overriden per branch):

1) Follow SemVer and only increment when a release has been tagged (continuous delivery mode)
2) Increment based on branch config every commit (continuous deployment mode)
3) Skip

> 2

Questions are all done, you can now edit GitVersion's configuration further
Which would you like to change?

0) Save changes and exit
1) Exit without saving

2) Run getting started wizard

3) Set next version number
4) Branch specific configuration
5) Branch Increment mode (per commit/after tag) (Current: ContinuousDeployment)
6) Assembly versioning scheme (Current: )
7) Setup build scripts

> 0
```

This generates a configuration file <code>GitVersion.yml</code> which looks like
this:

```
mode: ContinuousDeployment
branches: {}
ignore:
  sha: []
```

To evaluate the semantic version, I just run <code>gitversion</code> in the
repo. It spits out a large json object:

```
C:\Users\ngeor\Projects\GitHub\blog-helm [master ≡ +1 ~0 -0 !]> gitversion
{
  "Major":1,
  "Minor":0,
  "Patch":7,
  "PreReleaseTag":"ci.6",
  "PreReleaseTagWithDash":"-ci.6",
  "PreReleaseLabel":"ci",
  "PreReleaseNumber":6,
  "BuildMetaData":"",
  "BuildMetaDataPadded":"",
  "FullBuildMetaData":"Branch.master.Sha.58e23dbe5d5541a5ff7ce440de57317d1325637c",
  "MajorMinorPatch":"1.0.7",
  "SemVer":"1.0.7-ci.6",
  "LegacySemVer":"1.0.7-ci6",
  "LegacySemVerPadded":"1.0.7-ci0006",
  "AssemblySemVer":"1.0.7.0",
  "FullSemVer":"1.0.7-ci.6",
  "InformationalVersion":"1.0.7-ci.6+Branch.master.Sha.58e23dbe5d5541a5ff7ce440de57317d1325637c",
  "BranchName":"master",
  "Sha":"58e23dbe5d5541a5ff7ce440de57317d1325637c",
  "NuGetVersionV2":"1.0.7-ci0006",
  "NuGetVersion":"1.0.7-ci0006",
  "CommitsSinceVersionSource":6,
  "CommitsSinceVersionSourcePadded":"0006",
  "CommitDate":"2017-12-09"
}
```

But what I really care is to get the SemVer field:

```
PS> gitversion /showvariable SemVer
1.0.7-ci.6
```

With the configuration we got from the wizard, the master branch behaves a bit
weird when it's not tagged. Non tagged commits in master will have an extra
suffix "ci". To fix this, change the <code>GitVersion.yml</code> file into this:

```
mode: ContinuousDeployment
continuous-delivery-fallback-tag: ''
branches: {}
ignore:
  sha: []
```

Now the tool spits out the expected values for the master branch, even if it's
not tagged yet:

```
PS> gitversion /showvariable SemVer
1.0.7
```

There are more configuration options documented
<a href="http://gitversion.readthedocs.io/en/stable/configuration/" target="_blank">here</a>.

To use it in TeamCity, I'll rewrite the bash script `version.sh` which used to
look like this and relied on <code>package.json</code> to determine the version:

```bash
#!/bin/sh

set -x
set -e

GIT_SHA=$(git rev-parse HEAD)
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
APP_VERSION=$(cat package.json  | grep version | cut -d\" -f 4)

if [ "$GIT_BRANCH" = "master" ]; then
  IMAGE_TAG="$APP_VERSION"
else
  IMAGE_TAG="$APP_VERSION-$GIT_SHA"
fi

echo "Docker image tag will be $IMAGE_TAG"

# store image tag into a text file (artifact for deployment)
echo "$IMAGE_TAG" > image-tag.txt

# inject environment variable for next steps
echo "##teamcity[setParameter name='env.IMAGE_TAG' value='$IMAGE_TAG']"

```

into this:

```bash
#!/bin/sh

set -e

# make sure we have master branch and tags
git fetch --tags origin

GITTOOLS_GITVERSION_TAG=${GITTOOLS_GITVERSION_TAG:-v4.0.0-beta.12}
docker pull gittools/gitversion:$GITTOOLS_GITVERSION_TAG
IMAGE_TAG=$(docker run --rm \
  -u $(id -u):$(id -g) \
  -v /opt/buildagent/system/git:/opt/buildagent/system/git \
  -v $(pwd):/repo \
  gittools/gitversion:$GITTOOLS_GITVERSION_TAG \
  /showvariable SemVer)

echo "Docker image tag will be $IMAGE_TAG"

# store image tag into a text file (artifact for deployment)
echo "$IMAGE_TAG" > image-tag.txt

# inject environment variable for next steps
echo "##teamcity[setParameter name='env.IMAGE_TAG' value='$IMAGE_TAG']"

# set build number of TeamCity (better UX)
echo "##teamcity[buildNumber '$IMAGE_TAG']"
```

The important bit is the <code>docker run</code> command but it has quite some
tricks:

<ul>
<li><code>--rm</code> removes the container once the command exits</li>
<li><code>-u $(id -u):$(id -g)</code> runs this as the regular TeamCity user and not root. GitVersion adds some cache files in the current directory, which, if added as root, will prevent TeamCity from cleaning up.</li>
<li><code>-v /opt/buildagent/system/git:/opt/buildagent/system/git</code> seems to be needed otherwise GitVersion dies with (<code>ERROR: error: object directory /opt/buildagent/system/git/git-3566BB37.git/objects does not exist; check .git/objects/info/alternates.</code>). This is specific to TeamCity and actually specific to how TeamCity uses git internally.</li>
<li><code>-v $(pwd):/repo</code> mounts the current directory as the <code>/repo</code> directory inside the Docker container.</li>
<li><code>gittools/gitversion:$GITTOOLS_GITVERSION_TAG</code> is the image we're using.</li>
<li><code>/showvariable SemVer</code> is the parameter we saw earlier, asking GitVersion to simply print the semantic version.</li>
</ul>

The extra <code>git fetch</code> command is a countermeasure for some
optimization that TeamCity does, in which case we might not have the master
branch available at all. This can confuse GitVersion.

The last bit also overrides the build number of TeamCity, which improves UX
because we see the semantic version as the build number:

<img src="{{ site.baseurl }}/assets/2017/12/19/20_35_20-blog-helm-__-commit-stage-_-branches-e28094-teamcity.png" />

We can see that consecutive commits change the build number:

<img src="{{ site.baseurl }}/assets/2017/12/19/20_41_33-blog-helm-__-commit-stage-_-overview-e28094-teamcity.png" />

If we re-run a branch, it won't have an effect to its build number. The build
number is now derived from the semantic version and the semantic version is
calculated solely based on the git history.

We should also have TeamCity tag the master branch automatically:

<img src="{{ site.baseurl }}/assets/2017/12/19/19_07_58-commit-stage-configuration-e28094-teamcity.png" />

Now, let's try to create a minor feature. As before, we create a feature branch
out of master. But this time, in the commit message we specify the magic string
<code>+semver: minor</code>. The version gets adjusted automatically:

<img src="{{ site.baseurl }}/assets/2017/12/19/20_59_12-blog-helm-__-commit-stage-_-overview-e28094-teamcity.png" />

When this gets merged, master will get version 1.1.0.

GitVersion offers an interesting approach to versioning. It can be applied to
all projects, regardless of technology. It uses native git elements and it can
support multiple branching models. The only downside I can think of is that if
your repository already has a convention for storing the version (e.g.
<code>package.json</code> for nodeJS projects), that might cause surprise and
perhaps some confusion.

### Update 2019-10-24

This week I revisited this pipeline and also ported it to Jenkins. Regarding
GitVersion, I made the following changes:

- Use this Docker image:
  `gittools/gitversion:5.0.2-linux-ubuntu-18.04-netcoreapp3.0`
- Add the flags `/nocache`, `/nonormalize` and `/nofetch`

When invoking Docker directly:

```sh
IMAGE_TAG=$(docker run --rm \
      -u $(id -u):$(id -g) \
      -v $(pwd):/repo \
      gittools/gitversion:5.0.2-linux-ubuntu-18.04-netcoreapp3.0 \
      /repo /showvariable SemVer /nocache /nonormalize /nofetch)
```

When running within a Docker container:

```sh
IMAGE_TAG=$(dotnet /app/GitVersion.dll /showvariable SemVer /nocache /nonormalize /nofetch)
```

Example of a Jenkins declarative pipeline stage:

```groovy
stage("Versioning") {
  agent {
    docker {
      image "gittools/gitversion:5.0.2-linux-ubuntu-18.04-netcoreapp3.0"
      args "--entrypoint=''"
    }
  }

  steps {
    script {
      version = sh(script: "./ci-scripts/version.sh", returnStdout: true).trim()
    }
    buildName version
  }
}
```
