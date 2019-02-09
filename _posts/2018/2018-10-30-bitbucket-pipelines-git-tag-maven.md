---
layout: post
title: Publishing git tags for Maven projects in Bitbucket Pipelines
date: 2018-10-30
published: true
categories:
- ci-tooling
tags:
- git
- maven
- atlassian
- bash
- ci-tooling
---
> **Update 2018-11-24:** I've put together a maven plugin that can also publish
> git tags in Bitbucket Cloud, plus it checks there are no gaps in a semver
> sequence. It's available [here](https://github.com/ngeor/yak4j-bitbucket-maven-plugin).

I wrote a small script today that I wanted to share. It runs for Maven builds in
Bitbucket Pipelines and it creates a new git tag based on the version in the
`pom.xml`. I only run this in the master branch for projects that need
versioning (like parent poms and maven libraries).

First of all I need to read the version from the pom file. It would be great if
we had standard CLI tools, like grep and sed, which work with XML, JSON and YAML
files. Trying to extract the version of the pom file using bash kung fu is
probably not a good idea (although if you're determined enough you'll manage).
Instead, since this is a maven project anyway, I used a maven plugin. Here's the
bash function, filtering out some maven noise:

```bash
function getPomVersion {
    # Uses a maven plugin to print the version of the pom.
    # Filters out Download messages of maven and [INFO] log messages.
    mvn org.apache.maven.plugins:maven-help-plugin:2.1.1:evaluate -Dexpression=project.version | grep -v '\[' | grep -v 'Download'
}
```

Next, I'd like to check if the git tag already exists. The obvious solution is
to use the `git` CLI and run some commands. First of all, I'm running these
scripts inside Bitbucket Pipelines, which means I'm running them inside a Docker
image, which doesn't have the `git` program installed. But even if it did, I
have had some bad experience in the past trying to run `git` commands within a
CI server. The CI server (depends on the product of course) might not use git
the same default way a developer does. I have run into surprises in that area,
running commands only to find that they fail with weird error messages.

So, the `git` CLI is out of the question. Instead, I found that the Bitbucket
Pipelines REST API is easy to use (and `curl` is most of the time included in
Docker images).

Here's the code that checks if a tag exists:

```bash
function ensureGitTagDoesNotExist {
    # Ensures that the given tag does not exist in Bitbucket.
    TAG=$1
    OUTPUT=$(curl -s -u ${SUPER_SECRET} https://api.bitbucket.org/2.0/repositories/${BITBUCKET_REPO_OWNER}/${BITBUCKET_REPO_SLUG}/refs/tags?q=name+%3D+%22${TAG}%22 | tr -d '\r\n ')
    if [[ "$OUTPUT" == *"$TAG"* ]]; then
        echo "Tag $TAG already exists"
        exit 1
    else
        echo "Tag $TAG does not exist"
    fi
}
```

The variable `SUPER_SECRET` needs to contain the username and password
(separated by a colon) of a user who has access to create git tags in Bitbucket.
The `BITBUCKET_REPO_OWNER` and `BITBUCKET_REPO_SLUG` are default variables in
Bitbucket Pipelines.

The function gets all tags by the given name. If that name is present in the
JSON response, then the tag exists. If it's not there, we got back probably
some JSON like `values: []`, so we conclude the tag is missing.

Combined, we have this tiny script that will break the build if the pom version
already exists as a git tag:

```bash
POM_VERSION=$(getPomVersion)
ensureGitTagDoesNotExist v$POM_VERSION
```

Following the common convention, I prefix the git tags with the letter v. So if
the pom's version is 1.2.3, the git tag will be v1.2.3.

The last part is to actually create the tag. That's done with another API call:

```bash
curl https://api.bitbucket.org/2.0/repositories/${BITBUCKET_REPO_OWNER}/${BITBUCKET_REPO_SLUG}/refs/tags \
    -s -X POST -H "Content-Type: application/json" -u ${SUPER_SECRET} \
    -d "{ \"name\" : \"v${POM_VERSION}\", \"target\" : { \"hash\" : \"${BITBUCKET_COMMIT}\" } }"
```

In addition to the variables mentioned above, the `BITBUCKET_COMMIT` is a
built-in variable which contains the git commit id.

| Action                            | Branches           | When                    |
|-----------------------------------|--------------------|-------------------------|
| Ensure the git tag does not exist | All branches       | First step in the build |
| Publish a new git tag             | Only master branch | Last step in the build  |

Perhaps it's worth noting again that (at least for now) I only version things
that are dependencies of other projects: libraries and parent poms. I don't
version services, as nobody uses them as a version dependency.
