---
layout: page
title: Project Setup
---

Setting up a project, creating a pipeline, automatic deployments, etc.

Creating a project
------------------

Simply create the project on GitHub. Select the appropriate `.gitignore`
template and license (typically MIT).

Add a common `.editorconfig` file.

Enable the project via the Travis UI.

Deployment options
------------------

There are two deployment options:

- Deploy on tag
- Deploy on master

Bumping version
---------------

### Manual workflow

In this workflow, one or more team members have the **keeper** role. The keeper
has the extra privilege of being able to push directly (i.e. without a pull
request) a commit to the master branch and of being able to push a tag.

As with any workflow that involves a human, it is error prone and it creates a
dependency.

In this workflow, the team works on a repository and merges changes into the
master branch. When the keeper decides, he/she creates a new version. Creating a
new version consists of creating a tag and updating the version in the project
files that reference it (e.g. `package.json`, `pom.xml`).

The tag triggers the deployment to production.

Only the keeper is allowed to update the version in project files.

<img src="{{ site.baseurl }}/assets/wiki/manual-version-flow.png" />

#### Example

- `pom.xml` and latest git tag both point to version 1.4.0
- The developer creates a branch out of master
- After the work is complete, a PR is created and merged
- More PRs might be merged
- The keeper bumps the version (e.g. to 1.5.0) in `pom.xml` and pushes the tag
- The tag causes the deployment to production (e.g. publish to Nexus or npm)

#### Tooling

The tooling here should assist the keeper and prevent him/her from making mistakes.

### Automatic workflow

In this workflow, a **bot** automatically pushes a tag after a green build has
occurred on the master branch. This means that the version in the project files
needs to be corrected before merging the pull request.

<img src="{{ site.baseurl }}/assets/wiki/automatic-version-flow.png" />

#### Example

- `pom.xml` and latest git tag both point to version 1.4.0
- The developer creates a branch out of master
- The developer bumps the version in `pom.xml` to 1.5.0, indicating the intended next version
- After the work is complete, a PR is created and merged
- On master, the bot reads the version from `pom.xml` and tags master

**Important**

In this case, it is important that pushing a tag does not trigger a build,
otherwise we'll be in an infinite build loop. It's worth mentioning that the default
pipeline in Bitbucket Pipelines doesn't run on tags.

#### Tooling

The tooling here should prevent merging PRs where the version hasn't been bumped
properly. Additionally, it should push a new tag once the master is green.

### Comparison

| Manual                                        | Automatic                                         |
|-----------------------------------------------|---------------------------------------------------|
| Requires a privileged human to push versions  | Requires a bot to tag master                      |
| Not all merges needs to be deployed instantly | Every merge becomes a deployment                  |
| Developers aren't allowed to bump version     | Developers need to bump version in advance        |
| The trigger for a deployment is the tag       | The trigger for the deployment is merge to master |
| Tagging happens at a developer's computer     | Tagging happens during CI (after a green build)   |

Tooling for versioning
----------------------

### Bumping version with npm

`npm version minor` and `npm version patch` are useful commands that ensure that
there are no gaps in SemVer. They create a separate commit for the version bump,
together with a tag. It is possible to combine it with a `postversion` npm
script which will push the tag (e.g. `git push --follow-tags`)

### Bumping version with yart

[yart](https://github.com/ngeor/yart) tries to mimic `npm version`, but for Maven projects.

### Tagging master with Maven

[yak4j-bitbucket-maven-plugin](https://github.com/ngeor/yak4j-bitbucket-maven-plugin) is able to push a tag to Bitbucket after a successful green build on master.
