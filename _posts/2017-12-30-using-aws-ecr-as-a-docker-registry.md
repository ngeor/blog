---
layout: post
title: Using AWS ECR as a Docker registry
date: 2017-12-30 14:31:03.000000000 +01:00
published: true
categories:
- Code
tags:
- AWS
- AWS ECR
- blog-helm-sample
- Docker
- Helm
- Kubernetes
- TeamCity
---

In this post, I'll modify the pipeline from the previous posts to use a Docker registry powered by AWS ECR (Amazon Elastic Container Registry).

<!--more-->

<strong>Creating AWS ECR repositories</strong>

First, we need to enable ECR in Amazon and create our repositories. We have two images that we need to publish, <code>blog-helm</code> and <code>blog-helm-ci</code>, so we need two repositories.

<figure><img src="{{ site.baseurl }}/assets/2017/12/30/08_43_50-amazon-ecs.png" /><figcaption>Enable ECR</figcaption></figure>

<figure><img src="{{ site.baseurl }}/assets/2017/12/30/08_50_43-amazon-ecs.png" /><figcaption>Create the blog-helm repository</figcaption></figure>

<figure><img src="{{ site.baseurl }}/assets/2017/12/30/08_58_05-amazon-ecs.png" /><figcaption>Success!</figcaption></figure>

The second repository is created in the same way.

<strong>Getting Docker credentials</strong>

To be able to use this registry, we need to login with <code>docker login</code>. The AWS CLI offers a command which prints the necessary <code>docker login</code> command we need to run:

```

> aws ecr get-login --no-include-email --region eu-west-1
docker login -u AWS -p *** https://830988624223.dkr.ecr.eu-west-1.amazonaws.com

```

<strong>TeamCity changes</strong>

TeamCity in theory supports connecting to a Docker registry as a build feature. However, when I tried to setup the connection it complained that the password is too long (it is 1868 characters, so, yeah that's long), so that didn't work. This means that we need to do some extra work.

First, we'll create a few parameters on the project level:

<figure><img src="{{ site.baseurl }}/assets/2017/12/30/13_21_50-blog-helm-project-_-parameters-e28094-teamcity.png" /><figcaption>Configuration Parameters for the Docker registry</figcaption></figure>

With this in place, I need to add two new build steps:
<ul>
<li>Before pushing to or pulling from the Docker registry, we need to be logged in. This is an extra step that will run <code>docker login -u %docker.username% -p %docker.password% %docker.server%</code>.</li>
<li>After the registry is no longer required, I'd like to be logged out. This is an extra step that will run <code>docker logout %docker.server%</code>.</li>
</ul>

Since I have my <a href="{{ site.baseurl }}/2017/12/25/build-configurations-as-code-with-teamcity.html">build pipeline in code</a>, I can inject these steps easily wherever I need:

```
        script {
            name = "Login to Docker registry"
            scriptContent = "docker login -u %docker.username% -p %docker.password% %docker.server%"
        }
        script {
            name = "Push Docker production image"
            scriptContent = "docker push %docker.registry%/blog-helm:%env.IMAGE_TAG%"
        }
        script {
            name = "Push Docker CI image"
            scriptContent = "docker push %docker.registry%/blog-helm-ci:%env.IMAGE_TAG%"
        }
        script {
            name = "Logout from Docker registry"
            scriptContent = "docker logout %docker.server%"
            executionMode = BuildStep.ExecutionMode.ALWAYS
        }
```

Notice that in the logout step, I've configured the execution mode to be <code>Always</code>. This means that it will always run, even if some other step failed before. It's a nice setting to have for cleanup tasks like these.

It might be interesting to see how the password is stored. Having defined the parameter as a password, TeamCity does not commit its actual value into the code repository. Instead, it commits some reference value:

```
        password("docker.password", "credentialsJSON:175b2d15-2353-475e-ab70-571d1e5843e9", label = "Docker registry password")
```

When I change the password via the UI, TeamCity commits a patch file that updates this reference value:

```
changeProject("d3c230cf-b4cd-4a9e-8017-4b4b945b3a3c") {
    params {
        expect {
            password("docker.password", "credentialsJSON:6a39fd43-0513-4ba4-a446-14843fa7c355", label = "Docker registry password")
        }
        update {
            password("docker.password", "credentialsJSON:175b2d15-2353-475e-ab70-571d1e5843e9", label = "Docker registry password")
        }
    }
}
```

<strong>Results in AWS ECR</strong>

With this in place, I'm able to publish the images to AWS ECR:

<figure><img src="{{ site.baseurl }}/assets/2017/12/30/13_39_36-amazon-ecs.png" /><figcaption>Production Image (blog-helm)</figcaption></figure>

<figure><img src="{{ site.baseurl }}/assets/2017/12/30/13_40_19-amazon-ecs.png" /><figcaption>CI Image (blog-helm-ci)</figcaption></figure>

You can see that the production image is much smaller than the ci image, because the latter contains dev dependencies and <a href="{{ site.baseurl }}/2017/12/29/adding-webdriverio-tests.html">it's not based on alpine, due to PhantomJS</a>.

I also had a mistake in my <code>.dockerignore</code>, I should have excluded the <code>ci-scripts</code> folder from the Docker context; this unfortunately was creating a different CI image on every build. This is why the CI image has so many different tags compared to the production image.

<strong>Using the image in Kubernetes</strong>

My minikube needs to be able to pull from the AWS ECR too. First, I need to create a secret with the <code>kubectl</code> CLI tool:

```
$ kubectl create secret docker-registry myaws \
    --docker-username=AWS \
    --docker-password=*** \
    --docker-email=*** \
    --docker-server=830988624223.dkr.ecr.eu-west-1.amazonaws.com
secret "myaws" created
```

This will create a new secret named <code>myaws</code>. To use it, I need to modify the deployment template of my Helm chart:

{% raw %}
```yml
    spec:
      imagePullSecrets:
        - name: myaws
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
```
{% endraw %}

and of course I need to specify the new registry in the <code>values.yaml</code>:

```yml
replicaCount: 1
image:
  repository: 830988624223.dkr.ecr.eu-west-1.amazonaws.com/blog-helm
  tag: latest
  pullPolicy: IfNotPresent
```

And that's it! Now my local Kubernetes is able to pull images from the AWS ECR as well.

<strong>AWS Limits and Lifecycle Policy</strong>

In the AWS UI, there's a prominent warning: <em>Amazon ECR limits the number of images to 1,000 per repository</em>. Since we're publishing an image on every commit, I can imagine that this limit is easy to reach. Let's say 5 devs are working on a project (repository) and they each make 10 commits a day. In 20 working days, the limit is met.

Luckily AWS offers a cleanup policy. It can delete images based on their age or their count. Images are selected based on the tag prefix. Unfortunately we don't have a specific catch-all prefix in the current setup, as the image tag is following semver. It would be perhaps interesting to implement a tag scheme that has a different prefix for feature branches and different for the master branch (e.g. prod-1.2.3 for master and feat-1.2.4-some-feature-branch.1 for the feature branches). It would be also great if AWS allowed for a regex match. In any case, since my code is at the moment on major version 2, I can setup a rule for all images starting with "2." and specify I want to keep the 5 most recent:

<figure><img src="{{ site.baseurl }}/assets/2017/12/30/14_18_17-amazon-ecs.png" /><figcaption>Creating a lifecycle policy</figcaption></figure>

These are the 7 images currently available:

<figure><img src="{{ site.baseurl }}/assets/2017/12/30/14_19_59-amazon-ecs.png" /><figcaption>Images sorted by date</figcaption></figure>

If I do a dry-run on the rule, it correctly identifies the two oldest that will be deleted with this policy:

<figure><img src="{{ site.baseurl }}/assets/2017/12/30/14_19_15-amazon-ecs.png" /><figcaption>Termination candidates</figcaption></figure>
