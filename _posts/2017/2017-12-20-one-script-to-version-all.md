---
layout: post
title: One script to version all
date: 2017-12-20 20:55:35.000000000 +01:00
published: true
tags:
- blog-helm-sample
- GitVersion
- TeamCity
- tech
- versioning
---

This is just a fun hacking post. I put together a script that is able to handle all versioning strategies that I mentioned about in the <a href="{% post_url 2017/2017-12-18-on-versioning %}" target="_blank">post about versioning</a>.

<!--more-->

The script is a bit large at exactly 100 lines of bash so I'll just link to it <a href="https://github.com/ngeor/kamino/blob/trunk/blog-helm/ci-scripts/version.sh" target="_blank" rel="noopener">here</a>.

You can see here the 4 different ways it can be used to generate a version:

<img src="{{ site.baseurl }}/assets/2017/12/20/20_26_51-blog-helm-__-commit-stage-_-overview-e28094-teamcity.png" />

I'll take it from bottom to top:
<ul>
<li>GitVersion 1.3.1-demo.1</li>
<li>PackageJson 1.3.0-6d8348...</li>
<li>Hybrid 1.3.79</li>
<li>TeamCity 2.4.80</li>
</ul>

<strong>GitVersion</strong>

I covered <a href="{% post_url 2017/2017-12-19-semantic-versioning-with-gitversion %}" target="_blank">GitVersion in the previous post</a>, it uses the GitVersion tool to calculate the semantic version. The base tag was 1.3.0, so it bumped the version to 1.3.1, appended the branch name (demo) and the number of commits.

This is the default mode in the <code>version.sh</code> script.

<strong>PackageJson</strong>

This one gets the version from <code>package.json</code> and appends the git SHA when it's not on the master branch.

To use it, the <code>version.sh</code> script needs to be called with the <code>PackageJson</code> parameter.

<strong>Hybrid</strong>

Here the major and minor version comes from <code>package.json</code>, but the patch is the build counter of TeamCity.

The script needs to be called with two parameters: <code>Hybrid %build.counter%</code> (TeamCity will replace the actual value of the build counter).

<strong>TeamCity</strong>

This one simply takes the build number from TeamCity, no questions asked (I'll explain why it's 2.4.80 in a moment).

The script needs to be called with two parameters: <code>TeamCity %build.number%</code>.

It's useful here to clarify the difference between the build counter and the build number in TeamCity. Here's the initial settings of the build configuration. As you can see, by default the build number is equal to the build counter:

<img src="{{ site.baseurl }}/assets/2017/12/20/20_22_50-commit-stage-configuration-e28094-teamcity.png" />

To demonstrate the difference, I've changed the build number to <code>2.4.%build.counter%</code> (it can be obviously anything at all):

<img src="{{ site.baseurl }}/assets/2017/12/20/20_23_46-commit-stage-configuration-e28094-teamcity.png" />

that's why the build ended up to 2.4.80.

The build counter is a simple automatically incrementing positive integer number. The build number by default is equal to the build counter, but it can be overriden to be something more meaningful (e.g. the semantic version of the build). Even when the build number doesn't include the build counter (like in the GitVersion and PackageJson modes), the build counter still exists internally in TeamCity.
