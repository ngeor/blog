---
layout: post
title: Dockerize the build plan v2.0
date: 2018-08-26 09:18:49.000000000 +02:00
published: true
categories:
- continuous-delivery
tags:
- continuous integration
- docker
---

Back in 2017, I wrote a series of articles about using Helm for Continuous Delivery. One year later, I want to look back on some things I wrote and offer some alternative solutions. The most interesting thing is about the article <a href="{{ site.baseurl }}/2017/11/18/cd-with-helm-part-2-dockerize-the-build-plan.html">CD with Helm part 2: Dockerize the build plan</a>.

<!--more-->

This is the approach I had used back then:
<ul>
<li>We have a sample application called <a href="https://github.com/ngeor/blog-helm">blog-helm</a>. It can greet you with "Hello world!" on port 3000. It is written in nodeJS/<a href="https://expressjs.com/">express</a>.</li>
<li><code>npm</code> is used for dependency management.</li>
<li>The <code>Dockerfile</code> of the application packages the production image (only production dependencies).</li>
<li>A separate Dockerfile named <code>Dockerfile-ci</code> is used to "dockerize the build plan". All dependencies (including dev dependencies) are installed in the image, creating a highly specialized Docker image for the app.</li>
</ul>

So the <code>Dockerfile</code> looked like this:

```
FROM node:alpine
EXPOSE 3000
RUN mkdir /app
WORKDIR /app
ADD . /app
RUN npm install --only=production
CMD ["node", "index.js"]
```

and the <code>Dockerfile-ci</code> looked like this:

```
FROM node:8.9-alpine
RUN mkdir -p /app
ADD package.json /app
ADD package-lock.json /app
WORKDIR /app
RUN npm install
ADD . /app
```

After the introduction of <a href="{{ site.baseurl }}/2017/12/29/adding-webdriverio-tests.html">WebdriverIO testing</a>, the <code>Dockerfile-ci</code> changed further into this:

```
# phantomJS does not work with alpine
FROM node:8-slim

# dependencies
RUN apt-get update && apt-get install -y \
    bzip2 \
    libfontconfig1 \
 && rm -rf /var/lib/apt/lists/*

# install phantom
RUN curl -L https://github.com/Medium/phantomjs/releases/download/v2.1.1/phantomjs-2.1.1-linux-x86_64.tar.bz2 | tar jx
RUN mv phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/ \
    && rm -rf phantomjs-2.1.1-linux-x86_64

RUN mkdir -p /app
ADD package.json /app
ADD package-lock.json /app
WORKDIR /app
RUN npm install
ADD . /app
```

One big advantage of this approach is that the time consuming <code>npm install</code> step will be <strong>cached</strong>, thanks to Docker's powerful caching.

It's <em>not</em> however the approach I'm currently using. The CI systems I'm currently using are:
<ul>
<li><a href="https://travis-ci.org/">Travis</a> for my open source/hobby projects</li>
<li><a href="https://bitbucket.org/product/features/pipelines">Bitbucket Pipelines</a> at work</li>
</ul>

They both have great support for using Docker in your build pipeline <strong>transparently</strong> and they deal with caching of npm dependencies (or anything heavy for that matter) in a different way.

To explain what I mean by "using Docker transparently", let's take a trip down the memory lane. <strong>Before Docker</strong>, your build steps would run directly on the build agent. So you would run <code>npm install</code> and <code>npm test</code> directly on the agent. This had several problems:
<ul>
<li>the necessary tooling needed to be installed on the build agent (which has typically a dependency with the system administrator team that need to sign off any modifications to the shared company infrastructure)</li>
<li>multiple versions of the same tools might be required (e.g. one team on nodeJS 8 and another on bleeding edge)</li>
<li>multiple technologies might be required (e.g. one team on nodeJS and another one on Java)</li>
</ul>

This was not fun for anyone. Docker brought a great solution to this problem. Build steps in modern build servers, like Bitbucket Pipelines, are in fact <em>always</em> running within a Docker container.

However, a great build server should also <strong>hide away</strong> the fact that we are using Docker. This makes the learning curve smoother and promotes separation of concerns. So it would be great if my build steps are still <code>npm install</code> and <code>npm test</code>, with a small note somewhere that these run within the Docker image <code>node:8-slim</code> (for example). The Docker image is thus a small almost invisible implementation detail, a <strong>transparent glue</strong> if you like, between the build server and the build plan.

Which leaves us with caching of the <code>npm</code> dependencies. Both Travis and Bitbucket Pipelines offer caching as a first class citizen in their build definition language. This removes the last argument for my original, highly specialized, project-specific, <code>Dockerfile-ci</code> image.

In the approach I'm currently using, I <strong>always try to find first an existing Docker image</strong> at the Docker Hub that meets my requirements without being too bloated. It's like finding the right shoe. Examples:
<ul>
<li>For an Angular project, I needed an image that can run Karma tests and Protractor end to end tests, with Chrome headless browser. I found <a href="https://hub.docker.com/r/weboaks/node-karma-protractor-chrome">this one</a>, it worked fine for many months now.</li>
<li>For deployment projects that use Helm, I needed an image that supports <code>kubectl</code> and <code>helm</code>. I found <a href="https://hub.docker.com/r/dtzar/helm-kubectl">this one</a>, fantastic.</li>
<li>For deployment projects that use the AWS CLI and the AWS ElasticBeanstalk CLI... I didn't find an image. I created <a href="https://github.com/ngeor/awscli-docker-image">one myself</a> and published it to the Docker Hub.</li>
</ul>

Some criteria for picking an existing image: is it well documented? Is it still maintained? Does it have its Dockerfile on GitHub somewhere? How popular is it (downloads and stars)? Does it have automatic builds?

So, to wrap it up:
<ul>
<li>in my current projects, there is no <code>Dockerfile-ci</code>.</li>
<li>My build plan consists of simple step definitions, whose only relationship with Docker is that they indicate which Docker image they will be executed into (it might even be that different steps use different Docker images).</li>
<li>Docker images are off the shelf images from Docker Hub.</li>
<li>If a suitable image does not exist, then I would have to create one, but I would do that in a separate repository, so that the lifecycle of that image is separated from the project that is using it.</li>
<li>Last, but most definitely not least, caching of npm/maven/whatever dependencies is handled by the CI server (so the CI server must support this!).</li>
</ul>
