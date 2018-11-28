---
layout: post
title: Build chains in TeamCity
date: 2017-12-27 15:41:25.000000000 +01:00
published: true
categories:
- Code
tags:
- blog-helm-sample
- TeamCity
---

In a <a href="{{ site.baseurl }}/2017/12/09/cd-with-helm-part-8-dtap.html">previous post</a>, I had configured a deployment build configuration in TeamCity. I had mentioned back then that it's possible to set it up in a different way, which makes it is easier to visualize the deployment pipeline across all environments. In this post, I'll modify that deployment pipeline to use snapshot dependencies and project templates.

<!--more-->

First, I'll modify the artifacts so that they're all stored in a subfolder named <code>artifacts</code>. This allows to clear only that subfolder when clearing artifact paths. The inline script for deployment needs to be adjusted accordingly.

<figure><img src="{{ site.baseurl }}/assets/2017/12/27/13_27_40-deploy-stage-configuration-e28094-teamcity.png" /><figcaption>Using a subfolder for artifacts</figcaption></figure>

Then, I'll attach the project's VCS root to the Deploy Stage as well. This is necessary to allow for snapshot dependencies:

<figure><img src="{{ site.baseurl }}/assets/2017/12/27/13_34_21-deploy-stage-configuration-e28094-teamcity.png" /><figcaption>Attaching VCS root to deploy stage</figcaption></figure>

Note that we're still not using anything from the source code during deployment. We're only using the immutable artifacts generated during the commit stage. We just need to add the VCS root because TeamCity allows us then to use snapshot dependencies. Adding the snapshot dependency is the next step:

<figure><img src="{{ site.baseurl }}/assets/2017/12/27/14_13_09-deploy-stage-configuration-e28094-teamcity.png" /><figcaption>Adding snapshot dependency</figcaption></figure>

And configure the artifact dependency to use the artifacts from the same build chain:

<figure><img src="{{ site.baseurl }}/assets/2017/12/27/14_13_54-deploy-stage-configuration-e28094-teamcity.png" /><figcaption>Using artifacts from the same build chain</figcaption></figure>

This creates a build chain between the Commit Stage and Deploy Stage, which is visually more user friendly:

<figure><img src="{{ site.baseurl }}/assets/2017/12/27/14_26_44-view-build-chain-e28094-teamcity.png" /><figcaption>Visualizing build chain</figcaption></figure>

Now that this is done, I'd like to use one build configuration per DTAP environment. First, I'll change the environment configuration parameter so it's not a prompt anymore:

<figure><img src="{{ site.baseurl }}/assets/2017/12/27/14_35_38-deploy-stage-configuration-e28094-teamcity.png" /><figcaption>Changing the env parameter to normal instead of prompt</figcaption></figure>

I'll also change the build type into a deployment project:

<figure><img src="{{ site.baseurl }}/assets/2017/12/27/14_33_57-deploy-stage-configuration-e28094-teamcity.png" /><figcaption>Changing Deploy Stage into a Deployment build configuration</figcaption></figure>

Now I'll extract a project template out of this build configuration, so that I'll be able to reuse it for all environments of the DTAP:

<figure><img src="{{ site.baseurl }}/assets/2017/12/27/14_43_44-deploy-stage-configuration-e28094-teamcity.png" /><figcaption>Extract template out of Deploy Stage</figcaption></figure>

From there, I can rename the old "Deploy Stage" into "Deploy to Test" and set its <code>env</code> configuration parameter to <code>test</code>. I can further clone this build configuration for Acceptance and Production and set the <code>env</code> configuration parameter accordingly. In the end, I can see this screen on the Commit Stage of the build:

<figure><img src="{{ site.baseurl }}/assets/2017/12/27/15_04_06-blog-helm-__-commit-stage-_-1-3-16-27-dec-17-14_01-_-overview-e28094-teamcity.png" /><figcaption>Deployments of Commit Stage</figcaption></figure>

One more trick I like to do is to see the same build number across all build configurations. The Commit Stage is already configured to use <a href="{{ site.baseurl }}/2017/12/19/semantic-versioning-with-gitversion.html">SemVer</a>, so we'll re-use that number in the deploy configurations:

<figure><img src="{{ site.baseurl }}/assets/2017/12/27/15_07_09-deploy-template-template-e28094-teamcity.png" /><figcaption>Using the same build number across all deployments</figcaption></figure>

We can also configure Acceptance to depend on Test and Production to depend on Acceptance. This is done by adding additional snapshot dependencies, e.g. for production:

<figure><img src="{{ site.baseurl }}/assets/2017/12/27/15_21_55-deploy-to-production-configuration-e28094-teamcity.png" /><figcaption>Making Production depend on Acceptance</figcaption></figure>

This means we can't deploy to Production unless we have first deployed to Acceptance and we can't deploy to Acceptance unless we have first deployed to Testing. This has pros and cons, so you might want to think about before implementing it. In any case, it gives a nice build chain:

<figure><img src="{{ site.baseurl }}/assets/2017/12/27/15_22_35-blog-helm-__-commit-stage-_-build-chains-e28094-teamcity.png" /><figcaption>DTAP build chain</figcaption></figure>

So this is it, a different way to model the deployment pipeline using build chains. From here, we can add more build configurations between the deployments that perform automatic tests (e.g. integration tests) but we can also add build configurations that correspond to manual acceptance steps (e.g. manual QA acceptance or PO acceptance). I'll try to do that in a next post.
