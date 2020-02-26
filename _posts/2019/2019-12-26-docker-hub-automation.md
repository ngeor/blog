---
layout: post
title: Docker Hub automation
date: 2019-12-26 03:37:42
categories:
  - tech
tags:
  - docker
  - Docker Hub
---

I have [a git repository](https://github.com/ngeor/dockerfiles) that contains
various Docker files. I hacked a script that builds and pushes the images (which
is straightforward enough) but also updates the description of the images on
Docker Hub.

The build script is
[here](https://github.com/ngeor/dockerfiles/blob/master/build.pl). Side note:
I'm playing a bit with Perl currently. In the words of Bjarne Stroustrup: "There
are only two kinds of languages: the ones people complain about and the ones
nobody uses.". End of side note. The structure of my repository is simple. Each
Docker image has its own folder. Building the images means looping over the
folders and running the docker build command.

Tagging is a bit difficult. Ideally the tag should convey some useful
information. For example, `python:alpine` tells you it's the latest Python
version on an Alpine Linux flavor. `maven:3.6-jdk-11-slim` means it's Maven 3.6
on JDK 11 using a slim version of Debian. A lot of my images are just glueing
tools together e.g. `python-helm-kubectl-terraform` is a Docker image that is
built on top of Python alpine and comes with [helm](https://helm.sh/),
[kubectl](https://kubernetes.io/docs/reference/kubectl/kubectl/) and
[terraform](https://www.terraform.io/) built in. In the past I experimented with
a tag that combines the versions of all the components e.g. `2.14_1.13_0.10`.
Now that I'm building more images, I opted for a simple approach of using the
timestamp as a build tag. It's not as meaningful but at least it can be applied
easily to all images.

Some git related improvements on this iteration:

- when on master, tag also the `latest` version.
- only build and push images if their folders have changes. If I make a
  modification on image X, CI shouldn't build and publish image Y because that
  one hasn't changed.

The last bit was the more difficult because I couldn't find any documentation
about it. When you publish a Docker image on Docker Hub, you can provide a
description so that people can read about the image. So far I was editing it
manually via the browser. After a lot of unsuccessful searching, I found
[one git repository](https://github.com/RyanTheAllmighty/Docker-Hub-API) that
implements a nodeJS API to talk to Docker Hub. I adapted it for my script and it
did the trick. This way all my Docker images have an up to date description with
a link to their Dockerfile back in GitHub. Additionally, if an image has a
`README.md` in its subfolder, that readme gets included in the description.
