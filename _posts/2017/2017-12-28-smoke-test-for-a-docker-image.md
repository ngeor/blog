---
layout: post
title: Smoke test for a Docker image
date: 2017-12-28 10:40:39.000000000 +01:00
published: true
categories:
- tech
tags:
- blog-helm-sample
- docker
- smoke test
- TeamCity
---

According to <a href="https://en.wikipedia.org/wiki/Smoke_testing_(software)">Wikipedia</a>, a smoke test is <em>a preliminary test that reveals simple failures severe enough to (for example) reject a prospective software release</em>. <em>The process of smoke testing aims to determine whether the application is so badly broken as to make further immediate testing unnecessary.</em> If we consider our dockerized blog-helm web application, a possible smoke test can be: can we pull the image from the registry? If we run the image, does the container stay alive or does it crash immediately? In this post, I'll implement this in an extra build configuration in TeamCity with a generic bash script doing the actual work.

<!--more-->

First we need to create the new build configuration:

<figure><img src="{{ site.baseurl }}/assets/2017/12/28/08_21_44-create-build-configuration-e28094-teamcity.png" /><figcaption>Adding a new build configuration for the Smoke Test</figcaption></figure>

Just like in the previous post, we need to make it part of the <a href="{{ site.baseurl }}/2017/12/27/build-chains-in-teamcity.html">build chain</a>, so it needs the VCS root:

<figure><img src="{{ site.baseurl }}/assets/2017/12/28/08_22_48-smoke-test-configuration-e28094-teamcity.png" /><figcaption>Attaching VCS root</figcaption></figure>

and the snapshot dependency. Note that the only artifact needed is the <code>image-tag.txt</code> file that contains the Docker image tag name.

<figure><img src="{{ site.baseurl }}/assets/2017/12/28/08_24_40-smoke-test-configuration-e28094-teamcity.png" /><figcaption>Configuring dependencies</figcaption></figure>

I'd like to smoke test all feature branches automatically on every commit, so I configure a Finished Build trigger:

<figure><img src="{{ site.baseurl }}/assets/2017/12/28/08_26_31-smoke-test-configuration-e28094-teamcity.png" /><figcaption>Automatically smoke test all green Commit Stage builds</figcaption></figure>

and I don't want to be able to deploy to the test environment unless the smoke test has passed, so I add another snapshot dependency to the Deploy to Test build configuration:

<figure><img src="{{ site.baseurl }}/assets/2017/12/28/08_29_16-deploy-to-test-configuration-e28094-teamcity.png" /><figcaption>Only deploy when smoke test passes</figcaption></figure>

With these changes we have a new build chain with the Smoke Test build configuration in between Commit Stage and Deploy to Test:

<figure><img src="{{ site.baseurl }}/assets/2017/12/28/08_52_34-blog-helm-__-commit-stage-_-build-chains-e28094-teamcity.png" /><figcaption>The new build chain</figcaption></figure>

Now the build pipeline is configured and we just need to write the script that performs the smoke test. The script is a bit long at 98 lines of Bash, so I'll just <a href="https://github.com/ngeor/blog-helm/blob/v1.5.1/ci-scripts/smoke-test-docker-image.sh">link to it</a> if you want to read it. Its logic is roughly as follows:
<ul>
<li>Pull the image from the custom docker registry</li>
<li>Start a container with this image in the background (so that the script can continue)</li>
<li>Wait until the container starts (it retries 5 times with 5 seconds sleep between each retry). If the container can't start at all, either it's completely wrong, or the host is too slow, or something else weird is going on.</li>
<li>Wait to verify that the container stays up (same retry rules as before). This is the actual substance of this smoke test. The container starts, but does it stay up? This is supposed to be a web application, so it should stay up to serve incoming HTTP requests.</li>
<li>Cleanup: stop the container, print its logs (useful for troubleshooting), remove the container.</li>
</ul>

Let's see an example build log of a successful smoke test:

<figure><img src="{{ site.baseurl }}/assets/2017/12/28/09_15_19-blog-helm-__-smoke-test-_-1-5-0-smoke-test-2-28-dec-17-08_09-_-build-log-e28094-te.png" /><figcaption>Build log of a passed smoke test</figcaption></figure>

You can see that the container starts and stays up. The script tried 5 times and the container didn't die inexplicably in between, so that's good enough as far this smoke test is concerned.

To get a red build out of this smoke test, I modified the <code>CMD</code> instruction in the <code>Dockerfile</code> so that it references a non-existing JavaScript file (<code>indexx.js</code> instead of <code>index.js</code>). This is the resulting build log:

<figure><img src="{{ site.baseurl }}/assets/2017/12/28/09_22_22-blog-helm-__-smoke-test-_-1-5-0-smoke-test-3-28-dec-17-08_21-_-build-log-e28094-te.png" /><figcaption>Build log of a failed smoke test</figcaption></figure>

The container starts successfully, but a few seconds later it dies. The smoke test script prints the container logs, so we can clearly see that nodeJS exited because it couldn't find the file <code>/app/indexx.js</code>.

This smoke test costs a bit more than 30'' when it is green and less when it is red. Including some overhead for preparing and starting the build, this means that, on the happy flow, we have almost an entire minute to wait before we can deploy our application. What are we buying with this minute to justify spending it?

The checks we're doing (Can we pull the image? Does the container stay up?) would be implicit in an integration test, because you have to start the container in order to do the integration test against the running application. The advantage with a separate smoke test is that it's easier to troubleshoot what went wrong. If you see a failed smoke test, you understand that there's nothing wrong with your integration tests but something more fundamental has gone wrong.
