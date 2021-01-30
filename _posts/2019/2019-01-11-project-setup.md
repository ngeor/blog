---
layout: post
title: Project Setup
date: 2019-01-11
tags:
  - reference
  - pet project
---

Setting up a project, creating a pipeline, automatic deployments, etc.

## Getting all projects

If you work with multiple repositories, you can use [clone-all] to clone all the
missing repositories in one go.

Example:

```sh
# get all public repositories from GitHub
clone-all -p github --username ngeor
# get all private repositories from Bitbucket Cloud
clone-all -p bitbucket --owner acme --username user --password secret
```

To get latest version of all repositories in a folder, you can use [dirloop] in
this style:

```sh
dirloop git pull
```

## Creating a project checklist

- Create the project on GitHub. Select the appropriate `.gitignore` template and
  license (typically MIT).
- Clone the project. Also possible with `clone-all`.
- Travis
  - Enable Travis with `travis enable` CLI.
  - Add the Travis badge to the project's readme file.
  - Configure `.travis.yml`.
- Coveralls
  - Enable Coveralls via the UI.
  - Add the Coveralls badge to the project's readme file.
- Add a common `.editorconfig` file.

### Creating npm libraries

- Run the yeoman generator `@ngeor/generator-npm`.
- Run `travis setup npm` to setup npm deployment.
- Add the npm badge
- Add David badges for dependencies and devDependencies

Example `.travis.yml`:

```yml
language: node_js
sudo: false
node_js:
  - lts/*
after_success:
  - npm run coveralls
cache:
  directories:
    - node_modules
deploy:
  provider: npm
  email: Nikolaos.Georgiou@gmail.com
  api_key:
    secure: secret
  on:
    tags: true
    repo: ngeor/clone-all
```

### Creating Python libraries (deploy on PyPI)

[Travis documentation for PyPI](https://docs.travis-ci.com/user/deployment/pypi/)

Add the PyPI password with:

`travis encrypt your-password-here --add deploy.password`

Example `.travis.yml`:

```yml
language: python
python:
  - "3.6"
script:
  - python -m pytest
  - python setup.py sdist
deploy:
  provider: pypi
  user: ngeor
  password:
    secure: secret password
  on:
    tags: true
  skip_cleanup: true
```

Add the PyPI badge.

## Bumping version

There are two deployment options:

- Deploy on tag
- Deploy on master

### Manual workflow (deploy on tag)

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

The tooling here should assist the keeper and prevent him/her from making
mistakes.

### Automatic workflow (deploy on master)

In this workflow, a **bot** automatically pushes a tag after a green build has
occurred on the master branch. This means that the version in the project files
needs to be corrected before merging the pull request.

<img src="{{ site.baseurl }}/assets/wiki/automatic-version-flow.png" />

#### Example

- `pom.xml` and latest git tag both point to version 1.4.0
- The developer creates a branch out of master
- The developer bumps the version in `pom.xml` to 1.5.0, indicating the intended
  next version
- After the work is complete, a PR is created and merged
- On master, the bot reads the version from `pom.xml` and tags master

**Important**

In this case, it is important that pushing a tag does not trigger a build,
otherwise we'll be in an infinite build loop. It's worth mentioning that the
default pipeline in Bitbucket Pipelines doesn't run on tags.

#### Tooling

The tooling here should prevent merging PRs where the version hasn't been bumped
properly. Additionally, it should push a new tag once the master is green.

### Comparison

| Manual                                        | Automatic                                         |
| --------------------------------------------- | ------------------------------------------------- |
| Requires a privileged human to push versions  | Requires a bot to tag master                      |
| Not all merges needs to be deployed instantly | Every merge becomes a deployment                  |
| Developers aren't allowed to bump version     | Developers need to bump version in advance        |
| The trigger for a deployment is the tag       | The trigger for the deployment is merge to master |
| Tagging happens at a developer's computer     | Tagging happens during CI (after a green build)   |

## Tooling for versioning

### Manual workflow (deploy on tag)

#### Bumping version with npm

`npm version minor` and `npm version patch` are useful commands that ensure that
there are no gaps in SemVer. They create a separate commit for the version bump,
together with a tag. It is possible to combine it with a `postversion` npm
script which will push the tag (e.g. `git push --follow-tags`)

#### Bumping version with yart

[yart](https://github.com/ngeor/kamino/tree/trunk/yart) tries to mimic `npm version`, but for
Maven projects.

### Automatic workflow (deploy on master)

#### Tagging master with Maven

[yak4j-bitbucket-maven-plugin](https://github.com/ngeor/kamino/tree/trunk/java/yak4j-bitbucket-maven-plugin)
supports Maven projects. It breaks the build if the tag already exists and it is
able to push a tag to Bitbucket after a successful green build on master.

[clone-all]: https://github.com/ngeor/kamino/tree/trunk/clone-all
[dirloop]: https://github.com/ngeor/kamino/tree/trunk/dirloop
