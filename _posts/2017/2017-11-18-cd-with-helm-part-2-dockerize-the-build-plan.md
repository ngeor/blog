---
layout: post
title: 'CD with Helm part 2: Dockerize the build plan'
date: 2017-11-18 08:19:10.000000000 +01:00
series: CD with Helm
published: true
categories:
- continuous-delivery
tags:
- blog-helm-sample
- continuous integration
- docker
- helm
- kubernetes
---

With Docker, we can package our application in a Docker image and we have the assurance that it will run on any machine that has Docker. We can do the same with our build plan. Dockerizing the build environment means that the only dependency we have on the build server is that it supports Docker. This reduces the amount of work needed to manage the build server and enables teams to be more independent.

<!--more-->

<strong>Update 2018-08-26</strong> See also <a href="{{ site.baseurl }}/2018/08/26/dockerize-the-build-plan-v2-0.html">Dockerize the build plan v2.0</a>

To do that, we'll need to write a separate <code>Dockerfile</code>. Let's call it <code>Dockerfile-ci</code>. It looks similar to the main <code>Dockerfile</code> at first:

```
FROM node:8.9-alpine
RUN mkdir -p /app
ADD package.json /app
ADD package-lock.json /app
WORKDIR /app
RUN npm install
ADD . /app
```

It has some differences with the main <code>Dockerfile</code>:
<ul>
<li>it doesn't have an <code>EXPOSE</code> instruction, because we're not going to run the application.</li>
<li>it doesn't have a <code>CMD</code> instruction, because we'd like to run any command</li>
<li>it installs all dependencies, including dev dependencies, which will produce a larger image</li>
</ul>

To build the image we run:

```
docker build -t blog-helm-ci -f Dockerfile-ci .
```

This new image named <code>blog-helm-ci</code> contains the application code and all of its dependencies and it is ready to run <strong>any command we want</strong>.

We can use the image to run linting:

```
docker run blog-helm-ci npm run lint
```

This is the same as running <code>npm run lint</code>, but we don't need to install node on the build server, or having to worry about managing node versions, etc.

Since we're talking about build servers, when running this on a build server, we'd like to be able to see the linting results in a <strong>human friendly way</strong>, instead of trying to figure out what went wrong by diving into the build's log file. We can configure ESLint to generate an XML report with the problems it finds, using the ubiquitous jUnit XML report format.

To do that, we'll first configure an additional npm script to run ESLint with XML output. In <code>package.json</code>, we need to add the following in the scripts section:

```
    "lint-junit": "eslint -f junit -o test-reports/eslint.xml .",
```

This gives us a new npm script, <code>npm run lint-junit</code>, which will generate an XML report at <code>test-reports/eslint.xml</code> if there are any linting issues. If we configure the build server to read this file, we will get a friendly report with the problems we need to solve. Note that we can do the same with unit tests, we just use linting as a simpler example.

We'll need to rebuild the our docker image and then run the new script:

```
docker run blog-helm-ci npm run lint-junit
```

And... nothing happened! There is no <code>test-reports</code> folder at all. What went wrong?

Remember that the commands are running within a Docker container. They are running against the filesystem of that container. So the <code>test-reports</code> got created fine, but it was created inside the container, not on the physical host (e.g. personal laptop or build server).

Containers are ephemeral; to preserve data, we need to use a <strong>Docker volume</strong>. We'll need to define in <code>Dockerfile-ci</code> that the <code>test-reports</code> folder is a volume:

```
VOLUME [ "/app/test-reports" ]
```

This allows us to mount this folder. The run command looks like this:

```
docker run \
  -v $(pwd)/test-reports:/app/test-reports \
  blog-helm-ci \
  npm run lint-junit
```

One small side note regarding user permissions. When running on a Linux server, the test reports will be owned by the root user. This will break the builds, as the build server won't be able to clean the working directory. There are various ways to solve this, but I find that the least complicated one is to simply fix the permissions manually using our CI image:

```
docker run \
  -v $(pwd)/test-reports:/app/test-reports \
  blog-helm-ci \
  chown -R $(id -u):$(id -g) test-reports
```

This will set the correct permissions on the test reports and permit the build server to properly clean up its directories when needed.

There are other options as well, but it complicates the Dockerfile. An alternative that does not complicate code is to use Docker on Docker, which is off topic for this series.

Let's see how the build looks like in TeamCity:

<img src="{{ site.baseurl }}/assets/2017/teamcity-steps.png" />

The build is actually failing because I am using <code>console.log</code> which violates linting:

<img src="{{ site.baseurl }}/assets/2017/teamcity-failed.png" />

After I fix this linting issue, I get a green build:

<img src="{{ site.baseurl }}/assets/2017/teamcity-pass.png" />

The <a href="https://github.com/ngeor/blog-helm" target="_blank">code is available on GitHub</a> and you can browse the progress so far <a href="https://github.com/ngeor/blog-helm/tree/0a918f0e3e74a3d6b9cd1205a70f7dd10a822e4f" target="_blank">here</a>.

On the next post, we'll have a look at creating a Helm chart for this project.
