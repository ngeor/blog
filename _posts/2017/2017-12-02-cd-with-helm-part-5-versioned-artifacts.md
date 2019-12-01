---
layout: post
title: 'CD with Helm part 5: versioned artifacts'
date: 2017-12-02 16:04:56.000000000 +01:00
series: CD with Helm
published: true
categories:
- continuous-delivery
tags:
- blog-helm-sample
- continuous delivery
- continuous integration
- Docker
- helm
- kubernetes
- TeamCity
---

In the previous post we created the Helm chart for our hello world <code>blog-helm</code> application. The Helm chart contains all the information we need to deploy our application to a Kubernetes cluster. But so far, we always deploy the latest version. In a CD setup, we'd like to be able to deploy any version, from any feature branch, at any given point in time, to any environment (DTAP). Let's start by looking at versioning.

<!--more-->

We have various versions that we need to control in our application:
<ul>
<li>The application version, as defined in <code>package.json</code>.</li>
<li>The version of the Docker image (or tag in Docker terms). We haven't used this so far.</li>
<li>The version of the Helm chart, as defined in <code>Chart.yaml</code>. One important point to remember is that the Helm chart references the desired Docker image version in <code>values.yaml</code>.</li>
</ul>

To keep our sanity, it makes sense to use a <strong>single version number</strong> to describe all three versioned components. We'll try out the following setup:
<ul>
<li>The version defined in <code>package.json</code> is leading. This way, we allow the version to come from Git and go under the same code review process, just like everything else.</li>
<li>The version of the Docker image and the Helm chart will be the same. It will be equal to the application version for the master branch. For feature branches, we'll use the application version with the git SHA as a suffix.</li>
</ul>

So for the master branch we'll have something like this:

<img src="{{ site.baseurl }}/assets/2017/helm1.png" />

With a small difference for feature branches:

<img src="{{ site.baseurl }}/assets/2017/helm2.png" />

To make all this happen, we need to write a bit of code in the commit stage.

We will need these commands:
<ul>
<li><code>git rev-parse HEAD</code> will output the git SHA ID</li>
<li><code>git rev-parse --abbrev-ref HEAD</code> will output the name of the current branch</li>
<li>and finally <code>cat package.json  | grep version | cut -d\" -f 4</code> is a little bit of bash kung-fu that will give us the version out of <code>package.json</code>
</li>
</ul>

Let's put these commands together in a small bash script:

```bash
GIT_SHA=$(git rev-parse HEAD)
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
APP_VERSION=$(cat package.json  | grep version | cut -d\" -f 4)

if [ "$GIT_BRANCH" = "master" ]; then
  IMAGE_TAG="$APP_VERSION"
else
  IMAGE_TAG="$APP_VERSION-$GIT_SHA"
fi

echo "Docker image tag will be $IMAGE_TAG"
```

It's a good idea to commit this script in our source code, so that we don't have large inline scripts within the build server. We can create a new folder, e.g. <code>ci-scripts</code>, and store it there as <code>version.sh</code>.

We'll need to <strong>share this unique version with the next steps</strong> of the build but also with the deployment stage (which we haven't seen yet). For the deployment stage, we can write the image tag in a small text file and publish it as an artifact. For the commit stage, it's possible to create an environment variable from within a build step. Each build server does this differently, e.g. Bamboo has a "Inject Variables" build step and Jenkins has something similar. TeamCity, which I'm using in this example, supports some special <code>echo</code> message during the build.

The final script looks like this (<a href="https://github.com/ngeor/blog-helm/tree/f36bb849a9a3d5dce87a4a397c75d48dc67fa217" target="_blank">browse code at this point</a>):

```bash
#!/bin/sh

set -x
set -e

GIT_SHA=$(git rev-parse HEAD)
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
APP_VERSION=$(cat package.json  | grep version | cut -d\" -f 4)

if [ "$GIT_BRANCH" = "master" ]; then
  IMAGE_TAG="$APP_VERSION"
else
  IMAGE_TAG="$APP_VERSION-$GIT_SHA"
fi

echo "Docker image tag will be $IMAGE_TAG"

# store image tag into a text file (artifact for deployment)
echo "$IMAGE_TAG" > image-tag.txt

# inject environment variable for next steps
echo "##teamcity[setParameter name='env.IMAGE_TAG' value='$IMAGE_TAG']"
```

Let's go over the TeamCity configuration at this point. We have one extra build step, 4 in total:

<img src="{{ site.baseurl }}/assets/2017/12/02/13_40_25-commit-stage-configuration-e28094-teamcity.png" />
<ol>
<li>Determine version. This runs the new script, <code>ci-scripts/version.sh</code>, which figures out the Docker image version (and Helm chart version) we will use.</li>
<li>Build CI image. This builds the Docker image which includes all dependencies, including devDependencies. The only change here is that I'm now using TeamCity's Docker Build native step, instead of using a Command Line step.</li>
<li>Run linting. No changes here, it uses the image built in the previous step to run linting. Notice that this image does not need to be versioned.</li>
<li>Build production Docker image. Here we're using the environment variable <code>IMAGE_TAG</code> that is injected by the first build step. It looks like this:
<img src="{{ site.baseurl }}/assets/2017/12/02/13_47_01-commit-stage-configuration-e28094-teamcity.png" />
</li>
</ol>

Now, we need to <strong>package the Helm chart</strong>. That's done with a simple command (which will become our fifth build step):

```bash
helm package --version $IMAGE_TAG ./helm/blog-helm
```

The command line utility helm will not be present on the build agent. As we discussed in <a href="{{ site.baseurl }}/2017/11/18/cd-with-helm-part-2-dockerize-the-build-plan.html" target="_blank">Dockerize the build plan</a>, we need to wrap helm into a Docker image so that we can use it. Luckily, someone else has already created a <a href="https://hub.docker.com/r/lachlanevenson/k8s-helm/" target="_blank">Docker image with helm</a>. The build step in TeamCity looks like this:

<img src="{{ site.baseurl }}/assets/2017/12/02/13_54_55-commit-stage-configuration-e28094-teamcity.png" />

The reason this works so seamlessly is that TeamCity mounts the current directory as a volume inside the Docker container. The integration is very nicely done by TeamCity, but it's still important to understand what happens under the hood.

One last touch is to <strong>configure our artifacts in TeamCity</strong>:

<img src="{{ site.baseurl }}/assets/2017/12/02/14_06_52-commit-stage-configuration-e28094-teamcity.png" />

The tgz file is the Helm chart and the txt file is the small text file that specifies the image version.

<em>Small but important note: at this point, it's not possible to override the Docker image tag during packaging of the Helm chart. There is an open <a href="https://github.com/kubernetes/helm/issues/3141" target="_blank">issue for that on GitHub</a>. We will be setting the correct image during deployment, but ideally the Helm chart should already be tied to the Docker image.</em>

<strong>Demo time!</strong> Let's see if everything works fine. First, I'll bump the version on master branch to 1.0.1 to trigger a build. The build creates this artifacts:

<img src="{{ site.baseurl }}/assets/2017/12/02/14_08_01-blog-helm-__-commit-stage-_-20-02-dec-17-13_05-_-artifacts-e28094-teamcity.png" />

If we download them, we'll see that <code>image-tag.txt</code> just contains "1.0.1". The tgz file can be unzipped and there we'll see that <code>Chart.yaml</code> has the correct version:

```
apiVersion: v1
description: A Helm chart for Kubernetes
name: blog-helm
version: 1.0.1
```

We can try with a feature branch too. Our hello world page is serving plain text so far. It would be great if we change it into an HTML page with a large heading. That's an easy change in <code>index.js</code>:

```javascript
app.get('/', (req, res) => res.send(`
<html>
<body>
  <h1>Hello, world!</h1>
</body>
</html>
`));
```

I'll also bump the version to 1.0.2. Here's the result in TeamCity:

<img src="{{ site.baseurl }}/assets/2017/12/02/14_18_37-blog-helm-__-commit-stage-_-21-02-dec-17-13_15-_-artifacts-e28094-teamcity.png" />

This time, we're on a feature branch, so both the Docker image and the Helm chart will have the git SHA in their version.

We made it this far, let's make one more step to <strong>deploy our app into Kubernetes using Helm from TeamCity</strong>. The TeamCity Agent will run a helm command, which talks to Tiller, which tells Kubernetes to do its job and run our dockerized app inside a pod.

For this to happen, Kubernetes needs to be able to find the Docker images that TeamCity builds during the commit stage. <strong>The best way would be to setup a Docker registry, which we'll do on a future post</strong>. I've taken a shortcut however: <strong>I'm running TeamCity inside Kubernetes and TeamCity Agent is using Docker on Docker</strong>. This means that the TeamCity Agent is a dockerized application itself, but it's using the Docker daemon of Kubernetes when it needs to runs docker (remember, we've dockerized the build plan). It's very confusing, especially when volumes come into play. It feels a bit like the movie Inception, wondering on which level are you running currently:

<img src="{{ site.baseurl }}/assets/2017/docker-inception.jpg" />

We start by creating a new build configuration called Deploy Stage. We'd like to <strong>consume the artifacts from the Commit Stage</strong>:

<img src="{{ site.baseurl }}/assets/2017/12/02/14_21_14-deploy-stage-configuration-e28094-teamcity.png" />

We don't have any dependency to the source code. All we need is the artifacts. We can deploy everything with one command:

```bash
helm upgrade --install blog-helm \
  ./blog-helm-${IMAGE_TAG}.tgz \
  --set image.tag=$IMAGE_TAG \
  --wait
```

We just need the <code>IMAGE_TAG</code> environment variable, which we'll populate from the <code>image-tag.txt</code> artifact:

```bash
IMAGE_TAG=$(cat image-tag.txt)
echo "Using version $IMAGE_TAG"

helm upgrade --install blog-helm \
  ./blog-helm-${IMAGE_TAG}.tgz \
  --set image.tag=$IMAGE_TAG \
  --wait
```

Here's how it looks like in TeamCity:

<img src="{{ site.baseurl }}/assets/2017/12/02/14_25_16-deploy-stage-configuration-e28094-teamcity.png" />

Let's explain a bit the command:
<ul>
<li><code>upgrade --install blog-helm</code> specifies that we're interested in the Helm release named <code>blog-helm</code>. Helm uses its server-side component, Tiller, to keep tabs on releases. The <code>upgrade --install</code> part is equivalent to create or update. If the release is already there, it will upgrade it, otherwise it will create it.</li>
<li>the next parameter points to the Helm chart, which in this case is the tgz artifact</li>
<li>the <code>--set image.tag=$IMAGE_TAG</code> will override the Docker image tag defined in <code>values.yaml</code> with our environment variable. Since this also as artifact of the Commit Stage, we're certain we're deploying the correct version.</li>
<li>the last part <code>--wait</code> is a nice feature of Helm, it waits until the new version is up and running.</li>
</ul>

<em>One more networking shortcut: for helm to be able to reach Tiller (from within the Docker container from within TeamCity from within Kubernetes) I had to punch a hole in the cluster using a NodePort service. We'll revisit this in a future post. Remember, Inception.
</em>

I can trigger a custom deployment to use my feature branch:

<img src="{{ site.baseurl }}/assets/2017/12/02/14_29_21-blog-helm-__-deploy-stage-_-overview-e28094-teamcity.png" />

After the deployment finishes, we can see the results in the Kubernetes dashboard:

<img src="{{ site.baseurl }}/assets/2017/12/02/14_31_12-blog-helm-blog-helm-kubernetes-dashboard.png" />

Notice how both the Helm chart version (indicated by the label "chart" in the top) and the Docker image tag (indicated in the replica set area) are aligned.

And, of course, the app is now sporting an H1 header:

<img src="{{ site.baseurl }}/assets/2017/12/02/14_35_22-mozilla-firefox.png" />

Perhaps it's worth to mention that you can use any other version strategy that makes sense. In this case, git leads. You can also turn it around and have the build server leading, ignoring what is specified in the code. Or you can mix and match, using for example the major.minor parts of semver from git and the patch from the build server. The important thing is to make sure you have one unique version identifier that you can use to link everything together.

To summarize, we've created a versioning scheme which allows us to deploy any feature branch we want. We also created a deployment stage in TeamCity, which deploys based solely on the build artifacts, which means we can deploy any older version we want to. So far, we have only one environment to deploy to. We'll see in the next post how to support multiple deployment environments, moving towards a DTAP.
