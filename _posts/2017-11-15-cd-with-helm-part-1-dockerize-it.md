---
layout: post
title: 'CD with Helm part 1: Dockerize it'
date: 2017-11-15 20:41:42.000000000 +01:00
parent_id: '0'
published: true
categories:
- Code
tags:
- blog-helm-sample
- continuous integration
- Docker
- Helm
- Kubernetes
author: Nikolaos Georgiou
---

In the previous post, we created the hello world application that we'll be using. Now it's time to dockerize the app. Dockerizing means to create a Docker image that can be used to run the app.

<!--more-->

Docker is a fairly new technology, going back just 4 years. It is similar to a virtual machine, in the sense that it allows running multiple apps inside the same physical host in isolation and it protects the apps from library/dependency conflicts introduced by the physical host. It solves these problems however with a significantly lower resource overhead, as a virtual machine emulates an entire operating system and therefore needs more resources from the physical host.

To create our Docker image, we need a <code>Dockerfile</code>. This file contains <strong>instructions</strong> that tell Docker how to build our image. Let's see the first version:

```
FROM node:alpine
EXPOSE 3000
RUN mkdir /app
WORKDIR /app
ADD . /app
RUN npm install --only=production
CMD ["node", "index.js"]
```

That's quite a lot for a first draft, but let's take it step by step.

Docker images can be built <strong>on top of existing images</strong>. This allows you to build on top of more generic images, which are publicly available, and provide popular requirements. In our case, we need a Docker image that already supports nodeJS. That's the <code>FROM</code> instruction. The image is <code>node</code>. We also specify an explicit tag (similar to a version) to use: <code>alpine</code>. A Docker image can have multiple tags (versions if you prefer). The <code>alpine</code> flavor is based on Alpine Linux, which is popular in the Docker community due to its lighter footprint. The nodeJS version is the LTS, which is currently 8.9.

The next instruction, <code>EXPOSE</code>, tells Docker that our app listens to port 3000. Pretty straightforward.

Now the fun begins. <strong>We need to put our application code inside the Docker image</strong>. First, we create a folder where the app should live with <code>RUN mkdir /app</code>. The <code>RUN</code> instruction runs commands during the build phase of the image. Our image is based on Alpine Linux, so we can run any command that is bundled in that OS. <code>mkdir /app</code> will create a new folder <code>/app</code> in the filesystem of the image. It's very important to understand that <strong>these commands are being executed inside the image</strong>.

The next instruction, <code>WORKDIR</code>, defines the working directory (or current directory if you prefer) as <code>/app</code>. Subsequent instructions will take this into account.

Now we add the code of the application into the Docker image with the <code>ADD</code> instruction. It adds everything from the current directory of the host (the computer we're using to build the Docker image) into the <code>/app</code> directory inside the Docker image.

Next step, install our <code>npm</code> dependencies. Our image is based on <code>node:alpine</code>, therefore the <code>npm</code> command is available. We just run it to install <strong>only our production dependencies</strong>. Dev dependencies shouldn't be bundled in a production image, because they aren't needed.

Last part: define what the image should do when someone tries to run it. That's the <code>CMD</code> instruction. It says the image should run <code>node index.js</code> (remember that the working directory is set to <code>/app</code>).

That's quite a lot for a small Dockerfile, but it can be improved further. More on that in a second.

To build this image, run:

```
docker build -t blog-helm .
```

This will build a Docker image named <code>blog-helm</code> and it will use the Dockerfile found in the current directory.

When the image is built, you can run it with:

```
docker run -p 3000:3000 blog-helm
```

Notice that even though we defined that the app listens at port 3000, we still need to explicitly map that port. At this point you can try http://localhost:3000/ and see the hello world message again, only this time coming from the Docker container (Docker <a href="https://docs.docker.com/glossary/?term=container" target="_blank">container</a>: a runtime instance of a Docker image).

How can we further improve this build process? First of all, we can avoid sending unnecessary files to the Docker daemon during build time. This can speed up the process. This is done by another file, <code>.dockerignore</code>. Similar concept as a <code>.gitignore</code> file, it contains filename patterns that should be excluded. In our case we can have a simple <code>.dockerignore</code> file:

```
node_modules
```

this small change will improve the build time of the image (at least locally, where we have a <code>node_modules</code> folder lying around).

An even more interesting optimization has to do with <strong>how Docker caching works</strong>. Every instruction in a Dockerfile is creating behind the scenes an intermediate image. Docker is smart and it is able to reuse intermediate images if it can. In our example, the first four instructions are not affected by files on the outside world, so Docker will happily cache and reuse them. It makes sense after all: the intermediate product of those instructions is a Docker image, based on nodeJS, listening to port 3000, with a folder <code>/app</code> as working directory. Nothing specific to our app.

The next instruction adds our code into the image. This is specific to our app and it has to do with our code. Any code change we do will invalidate the cache. Once the cache is invalidated, the next steps will also need to be re-run. Our next step is a time consuming one: installing npm dependencies.

Therefore, in our current setup, if we modify <code>index.js</code> (or add a new <code>css</code> file, whatever), we invalidate the cache, and Docker will need to install npm dependencies again. That's just a waste of time. We should only re-install npm dependencies if <code>package.json</code> has changed.

Well, we can change our Dockerfile to add the code in two steps: first, only add <code>package.json</code> (and its buddy <code>package-lock.json</code> of course). Then, install npm dependencies. And only after that, add the rest of the code. Something like this:

```
FROM node:alpine
EXPOSE 3000
RUN mkdir /app
WORKDIR /app
ADD package.json /app
ADD package-lock.json /app
RUN npm install --only=production
ADD . /app
CMD ["node", "index.js"]
```

This optimization is a life saver, as the costly part that installs npm dependencies will only be run when <code>package.json</code> changes <a href="https://github.com/ngeor/blog-helm/tree/ae0e9e6ecfcfc0f4b9d7e357bb97458ff7aca175" target="_blank">(browse code)</a>.

That was a lot for this post, but we're not quite done with Docker yet. We dockerized the app, but we forgot to test it (our testing range consists only of linting for this example app). We could just run <code>npm run lint</code>, but when we are configuring the CI server, we need to make sure it has the node version we want. Another team might need a different node version. Another team might need more and more dependencies, risking conflicts and increasing server management work. Well, we can also <strong>dockerize our build environment</strong>. The only requirement for the CI server will be that it needs to run docker. Each team then can define its own requirements independently. More on that on the next post, where we'll switch to looking things from the CI server's point of view.
