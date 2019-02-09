---
layout: post
title: Fixing root permissions on Docker volume
date: 2017-12-16 19:07:48.000000000 +01:00
published: true
categories:
- continuous-delivery
tags:
- blog-helm-sample
- docker
- TeamCity
---

In a previous post, we saw <a href="{{ site.baseurl }}/2017/11/18/cd-with-helm-part-2-dockerize-the-build-plan.html" target="_blank">how to dockerize the build plan</a> of an application. Typically, you'll want the build to run tasks like linting and unit tests, and then publish the results of these operations as XML reports that the build server can consume and present in a human friendly way.

<!--more-->

Since these tasks now run within a Docker container, the XML reports will be generated within the container's filesystem. The build agent can't access that, unless we use a Docker volume. With the volume, the reports are accessible but they are owned by the root user. This is a problem because the build agent is not running as root (hopefully) and won't be able to delete these reports when it needs to cleanup (e.g. in order to run the next build in a clean workspace).

The easiest approach is what we did in the post about <a href="{{ site.baseurl }}/2017/11/18/cd-with-helm-part-2-dockerize-the-build-plan.html" target="_blank">dockerizing the build plan</a>, simply run the chown command after we use the image, to make sure permissions are back to normal.

Coincidentally, this is exactly what TeamCity does as well (so you don't need to do it yourself). From the <a href="https://confluence.jetbrains.com/display/TCD10/Docker%20Wrapper" target="_blank">documentation</a>:
<blockquote>

After the build step with the Docker wrapper, a build agent will run the chown command to restore access of the buildAgent user to the checkout directory. This mitigates a possible problem when the files from a Docker container are created with the 'root' ownership and cannot be removed by the build agent later.</blockquote>

If your CI server doesn't support this, you can also try another trick: use a custom entrypoint in the Docker image.

Let's see the old Dockerfile:

```
FROM node:8.9-alpine
RUN mkdir -p /app
ADD package.json /app
ADD package-lock.json /app
WORKDIR /app
RUN npm install
ADD . /app
```

Wouldn't it be great if the permissions got automatically fixed whenever we run a command with this image? We can do that with a custom entrypoint:

```
FROM node:8.9-alpine
RUN mkdir -p /app
ADD package.json /app
ADD package-lock.json /app
WORKDIR /app
RUN npm install
ADD . /app

ENV HOST_USER_ID=
ENV HOST_GROUP_ID=
ADD npm-entrypoint.sh /usr/local/bin/npm-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/npm-entrypoint.sh"]
CMD ["--help"]
```

And the entrypoint script itself looks like this:

```
#!/bin/sh
npm run $@
if [ -n "$HOST_USER_ID" -a -n "$HOST_GROUP_ID" ]; then
    chown -R $HOST_USER_ID:$HOST_GROUP_ID .
fi
```

And using the image changes into this:

```
docker run --rm \
    -e HOST_USER_ID=$(id -u) \
    -e HOST_GROUP_ID=$(id -g) \
    blog-helm-ci lint
```

(it used to be just <code>docker run --rm blog-helm-ci npm run lint</code>)

What's going on? We use the environment variables <code>HOST_USER_ID</code> and <code>HOST_GROUP_ID</code> to pass the user id and group id of the build agent into the Docker container. We retrieve these with <code>$(id -u)</code> and <code>$(id -g)</code>.

With the entrypoint, we're able to run the custom shell script <code>npm-entrypoint.sh</code> upon every usage of the Docker image. The script itself runs <code>npm run</code> with whatever extra arguments we pass and then it corrects the permissions on the current folder, setting the ownership to the user and group of the build agent's user. This will permit the build agent to clean up these files later.

This is a slightly more complicated approach than just running chown ourselves after using the image, but the advantage is that we don't need to worry about it, as the image itself now takes care of it. Additionally, we are able to lock down the image so that it only runs npm commands.
