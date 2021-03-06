---
layout: post
title: Removing the image-tag.txt artifact
date: 2017-12-29 09:37:12.000000000 +01:00
published: true
tags:
- blog-helm-sample
- TeamCity
excerpt: Small update on replacing the image-tag.txt artifact with the implicit build.number
  parameter.
---

In the post about <a href="{% post_url 2017/2017-12-02-cd-with-helm-part-5-versioned-artifacts %}">versioned artifacts</a>, I was using a custom text file named <code>image-tag.txt</code> to share the image tag between build configurations. The commit stage evaluates the image tag and produces the <code>image-tag.txt</code> artifact, which just contains the version e.g. <code>1.3.0</code>.

After the post <a href="{% post_url 2017/2017-12-20-one-script-to-version-all %}">about the versioning script</a>, the build number of the commit stage and the image tag where identical and they were following semantic versioning.

In a more recent post, I've configured a <a href="{% post_url 2017/2017-12-27-build-chains-in-teamcity %}">build chain</a> in TeamCity, in which all build configurations share the build number of the Commit Stage. This means that all build configurations have the correct image tag information implicitly, as their build number. This makes the <code>image-tag.txt</code> artifact <strong>obsolete</strong>.

I have therefore removed the <code>image-tag.txt</code> artifact and I'm using the implicit configuration parameter <code>%build.number%</code> wherever I need it.
