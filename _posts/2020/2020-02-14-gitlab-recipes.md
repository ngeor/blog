---
layout: post
title: GitLab recipes
date: 2020-02-14 06:12:15
categories:
  - tech
tags:
  - GitLab
  - YAML
---

Another year, another CI tool. Due to work changes, I'm exploring GitLab for the
first time. Here are some basic snippets I used recently and my first impression
of the tool.

A CI pipeline in GitLab consists of **stages** and **jobs**. A stage can contain
multiple jobs which run in parallel. Stages run sequentially (or, if you prefer,
jobs of a stage run after the jobs of the previous stage have completed). The
pipeline is defined in the file `.gitlab-ci.yml`.

## Hello, world

Here's a sample for a Maven project which runs `mvn verify`:

```yml
image: maven:3-jdk-11
stages:
  - verify_stage
verify_job:
  stage: verify_stage
  script:
    - mvn -B verify
```

Note that for such a simple configuration you don't even need to define stages.

## Caching

The next step will be to make the build a bit faster by caching the Maven
dependencies. For GitLab, the files to be cached need to be within the working
directory. For Maven, this isn't the case, as the dependencies are downloaded in
`~/.m2/repository`. We can change this however with an environment variable:

```yml
image: maven:3-jdk-11
variables:
  # Use this directory instead of ~/.m2, so that GitLab can cache it
  MAVEN_OPTS: "-Dmaven.repo.local=$CI_PROJECT_DIR/.m2/repository"
stages:
  - verify_stage
verify_job:
  stage: verify_stage
  cache:
    key: "$CI_JOB_NAME"
    paths:
      - .m2/repository/
  script:
    - mvn -B verify
```

With this modification, builds become faster because Maven dependencies are
cached instead of downloaded from the internet. The cache key plays an important
role, the
[documentation](https://docs.gitlab.com/ee/ci/caching/#good-caching-practices)
lists various examples. You can cache per branch, per job name, per combination
of those, etc.

## Using a service

Let's say that your integration tests need a MySQL database. This is not a
problem in the age of containers:

```yml
image: maven:3-jdk-11
variables:
  MYSQL_DATABASE: cool_db
  MYSQL_USER: cool_user
  MYSQL_PASSWORD: secret
  MYSQL_RANDOM_ROOT_PASSWORD: "1"
stages:
  - verify_stage
verify_job:
  stage: verify_stage
  services:
    - mysql:5
  script:
    - mvn -B verify
```

The database hostname will be `mysql`.

## Allowing a job to fail

Let's say we have a job that might fail but we don't want that to be a big deal,
but just a warning. For example, let's say that we have a job that performs a
SonarQube analysis and we don't want to break the build if it fails. That's done
with the `allow_failure` setting:

```yml
image: maven:3-jdk-11
stages:
  - verify_stage
  - sonar_stage
verify_job:
  stage: verify_stage
  script:
    - mvn -B verify
sonar_job:
  stage: sonar_stage
  script:
    - mvn -P sonar mvn verify sonar:sonar
  allow_failure: true
```

## Artifacts

You can specify the artifacts of your job:

```yml
image: maven:3-jdk-11
stages:
  - verify_stage
verify_job:
  stage: verify_stage
  script:
    - mvn -B verify
  artifacts:
    paths:
      - target/*.jar
    expire_in: "1 day"
```

## Conditional execution: branches and tags

It's possible to have a job executing only on certain conditions. The typical
example is that you only want to deploy your app on production from the `master`
branch, or publish your package from a tag.

```yml
image: maven:3-jdk-11
stages:
  - verify_stage
  - deploy_stage
verify_job:
  stage: verify_stage
  script:
    - mvn -B verify
deploy_job:
  stage: deploy_stage
  script:
    - mvn -B deploy
  only:
    refs:
      - master
```

For executing only on a tag, the `only` setting changes into:

```yml
only:
  - tags
```

## Extending jobs

Let's say that your git repository is a small monorepo that consists of two
Maven projects living side by side. These aren't modules of a common parent,
they are totally independent projects. The configuration can be something like:

```yml
image: maven:3-jdk-11
stages:
  - verify_stage
verify_foo_job:
  stage: verify_stage
  script:
    - cd foo && mvn -B verify
verify_bar_job:
  stage: verify_stage
  script:
    - cd bar && mvn -B verify
```

This is simple enough, but soon you need to add caching, perhaps archive the
same artifacts, and so on. To avoid repetition, you can define a template job
and extend it:

```yml
image: maven:3-jdk-11
stages:
  - verify_stage
.verify_job:
  stage: verify_stage
  script:
    - cd ${PROJECT_NAME} && mvn -B verify
verify_foo_job:
  extends: .verify_job
  variables:
    PROJECT_NAME: foo
verify_bar_job:
  extends: .verify_job
  variables:
    PROJECT_NAME: bar
```

Now, all improvements on `.verify_job` get inherited by both jobs.

## Conditional execution: changes

Now that we touched the monorepo, small as it may be, I'd like to show this
feature that I like: building a job only if certain paths have changed.

There is no point in verifying the app `foo`, if the commit touches only the app
`bar`. This is supported by GitLab:

```yml
image: maven:3-jdk-11
stages:
  - verify_stage
.verify_job:
  stage: verify_stage
  script:
    - cd ${PROJECT_NAME} && mvn -B verify
verify_foo_job:
  extends: .verify_job
  variables:
    PROJECT_NAME: foo
  only:
    changes:
      - foo
      - .gitlab-ci.yml
verify_bar_job:
  extends: .verify_job
  variables:
    PROJECT_NAME: bar
  only:
    changes:
      - bar
      - .gitlab-ci.yml
```

Notice that I add also the `.gitlab-ci.yml` as a safety measure. If I change the
pipeline definition, then I want everything to run, regardless of what has
changed.

This feature allows you to use a monorepo if you want to, but also have control
over what gets built and deployed, without having to write something custom
yourself.
