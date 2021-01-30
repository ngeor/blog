---
layout: post
title: 'CD with Helm part 8: DTAP'
date: 2017-12-09 12:33:12.000000000 +01:00
series: CD with Helm
published: true
tags:
- blog-helm-sample
- docker
- helm
- kubernetes
- TeamCity
---

In the series so far, we have build a CI pipeline that produces a Docker image and a Helm chart. They are linked together with a unique version, allowing us to use Helm to deploy any feature branch we want. Now we'll see how to implement a traditional DTAP and use Helm to deploy whatever, wherever.

<!--more-->

When we deploy the Helm chart, it is possible to provide an additional <code>values.yaml</code> file. The values on that file will override the values defined inside the Helm chart. We can use this feature to model our <strong>environment-specific</strong> configuration.

Let's create a file named <code>values-test.yaml</code> side by side with <code>values.yaml</code>:

```
# Values for the test environment.
ingress:
  hosts:
    - test.blog-helm.local
```

This file contains the environment-specific configuration of the test environment. We only need to override the host. All other values are the same, so we don't need to define them.

We repeat this for acceptance, creating <code>values-acc.yaml</code>:

```
# Values for the acceptance environment.
ingress:
  hosts:
    - acc.blog-helm.local
```

For production, we could do the same, but another approach is to treat the default values file, <code>values.yaml</code>, as the production values. In any case, we will need a <code>values-prod.yaml</code> to make the deployment logic a bit simpler.

To use these environment-specific files during deployment, we need to <strong>publish them as artifacts</strong> in our build plan. We need to add in the artifact definitions the line <code>helm/blog-helm/values-*.yaml</code>:

<figure><img src="{% link /assets/2017/05-artifacts.png %}" /><figcaption>Artifact definition in Commit Stage</figcaption></figure>

and the build will publish them:

<figure><img src="{% link /assets/2017/06-artifacts.png %}" /><figcaption>Published artifacts</figcaption></figure>

Now we need to <strong>consume them in the Deploy Stage</strong>, so let's update the Artifact Dependency to have the line <code>values-*.yaml</code>:

<figure><img src="{% link /assets/2017/07-artifacts.png %}" /><figcaption>Artifact dependencies in deployment</figcaption></figure>

Let's revise now our deployment script. So far it looks like this:

```
IMAGE_TAG=$(cat image-tag.txt)
echo "Using version $IMAGE_TAG"

helm upgrade --install blog-helm \
  ./blog-helm-${IMAGE_TAG}.tgz \
  --set image.tag=$IMAGE_TAG \
  --wait
```

The <code>helm</code> supports a <code>--values</code> argument, which we need to provide e.g. <code>--values ./values-acc.yaml</code> for acceptance.

An important thing is that we'll also need to change the release name, which currently is <code>blog-helm</code>. This also needs to be environment specific, as each release will model a different environment.

The easiest way to do this in TeamCity is to make our Deploy Stage parametric. We add a new configuration parameter named <code>env</code> (it can be any name we want):

<figure><img src="{% link /assets/2017/08-env.png %}" /><figcaption>Adding the 'env' configuration parameter</figcaption></figure>

To make sure the user who deploys must choose an environment, we configure the spec of this parameter to be a Prompt. We also make it a bit more user friendly by providing a list of allowed values:

<figure><img src="{% link /assets/2017/09-env-spec.png %}" /><figcaption>Setting the spec of the parameter</figcaption></figure>

With this in place, we <strong>revise our deployment script</strong> to use the <code>env</code> configuration parameter:

```
IMAGE_TAG=$(cat image-tag.txt)
echo "Using version $IMAGE_TAG"

helm upgrade --install blog-helm-%env% \
  ./blog-helm-${IMAGE_TAG}.tgz \
  --set image.tag=$IMAGE_TAG \
  --values ./values-%env%.yaml \
  --debug \
  --wait
```

We changed the release name to be <code>blog-helm-%env%</code>, which will use the file <code>values-%env%.yaml</code>. The extra flag

When we try to deploy, we get a popup asking us to select the environment:

<figure><img src="{% link /assets/2017/11-env-select.png %}" /><figcaption>Deploying to a specific environment</figcaption></figure>

If we deploy to all environments, one by one, we'll end up with these deployments in Kubernetes:

<figure><img src="{% link /assets/2017/12-deployments.png %}" /><figcaption>Kubernetes deployments, managed by Helm</figcaption></figure>

Some cleanup work is needed: we still have the old release, <code>blog-helm</code>. We can remove it with this command:

```
$ helm delete --purge blog-helm
release "blog-helm" deleted
```

<em>Small sidenote: TeamCity is not strictly speaking a deployment tool. It doesn't have features like deployment environments, promoting a deployment to a different environment, approving/rejecting deployments, etc. It is however possible to model a deployment in a better way than what I did here, e.g. with snapshot dependencies and project templates.</em>

To be able to access our environments, we need a small update on the <code>/etc/hosts</code> file:

```
192.168.99.100 test.blog-helm.local
192.168.99.100 acc.blog-helm.local
192.168.99.100 blog-helm.local
```

All our hostnames point to the cluster and then Ingress knows which application to use.

A small problem with our hello-world application is that it just says "Hello, world!". So we can't be sure which version we're looking at, or that the environments are setup correctly. Let's modify it so that it prints the version found in <code>package.json</code>:

```js
/* eslint-disable no-console */
const express = require('express');
const packageJson = require('./package.json');

const app = express();
app.get('/', (req, res) => res.send(`
<html>
  <head>
    <title>blog-helm</title>
  </head>
  <body>
<h1>Hello world!</h1>
package.json version: ${packageJson.version}

  </body>
</html>
`));
app.listen(
  3000,
  () => console.log('Example app listening on port 3000!'),
);
/* eslint-enable no-console */
```

We can deploy to the test environment. Let's double check the versions in the Kubernetes dashboard:

<figure><img src="{% link /assets/2017/13-test-on-1-2-0.png %}" /><figcaption>After deploying to test</figcaption></figure>

Our test environment is on the latest and greatest. Now the change is visible on the browser:

<figure><img src="{% link /assets/2017/14-test-vs-acc.png %}" /><figcaption>Test and Acceptance side by side</figcaption></figure>

The test environment on the left has the latest code but acceptance still has the old version.

What if we want to know on which environment we're running the application? We can set an environment variable using the Helm chart. We need to define it in the <code>deployment.yaml</code> template:

{% raw %}
```yml
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: {{ .Values.service.internalPort }}
          env:
            - name: APP_ENV
              value: {{ .Values.env }}
```
{% endraw %}

and we'll need to set this in all <code>values-*.yaml</code> files accordingly, e.g. for acceptance in <code>values-acc.yaml</code>:

```yml
# Values for the acceptance environment.
ingress:
  hosts:
    - acc.blog-helm.local
env: acc
```

Printing it in the application is easy:

```

Environment: ${process.env.APP_ENV}

```

Let's deploy again, this time to all environments:

<figure><img src="{% link /assets/2017/15-print-env.png %}" /><figcaption>Environment aware applications</figcaption></figure>

This time, we can see that the environments are setup correctly.

One final experiment has to do about feature branches. If you remember our <a href="{% post_url 2017/2017-12-02-cd-with-helm-part-5-versioned-artifacts %}">versioning strategy</a>, we compose an image tag based on the version in <code>package.json</code> and the git SHA. We can use an environment variable for this too:

{% raw %}
```yml
          env:
            - name: APP_ENV
              value: {{ .Values.env }}
            - name: IMAGE_TAG
              value: {{ .Values.image.tag }}
```
{% endraw %}

and we can print it in <code>index.js</code>:

```
<h1>Hello world!</h1>
package.json version: ${packageJson.version}

Docker image tag: ${process.env.IMAGE_TAG}

Environment: ${process.env.APP_ENV}

```

<figure><img src="{% link /assets/2017/16-print-docker-tag.png %}" /><figcaption>Deploying feature branch</figcaption></figure>

This final experiment proves we can truly deploy whatever, wherever: any feature branch in any environment. With this milestone, we can wrap up this series of posts. We have achieved various goals:
<ul>
<li><a href="{% post_url 2017/2017-11-15-cd-with-helm-part-1-dockerize-it %}">we dockerized an application</a></li>
<li><a href="{% post_url 2017/2017-11-18-cd-with-helm-part-2-dockerize-the-build-plan %}">we dockerized the build plan of the application</a>, while keeping user friendly elements like test reports</li>
<li>we included the infrastructural configuration of the application (<a href="{% post_url 2017/2017-11-27-cd-with-helm-part-4-helm-intro %}">Helm chart</a>) in the code repository. This allows us to change the application and its infrastructure configuration in a single pull request.</li>
<li><a href="{% post_url 2017/2017-12-02-cd-with-helm-part-5-versioned-artifacts %}">we defined and implemented a versioning strategy</a> which ties together the application with its infrastructure, allowing us to use Helm as a deployment tool, for any branch</li>
<li>we modeled a DTAP by using Helm releases and isolated the environment-specific configuration in separate files containing the bare minimum.</li>
</ul>

This is actually enough for a continuous deployment pipeline using Helm. From here you can add all sorts of bells and whistles:
<ul>
<li>explore namespaces in Kubernetes</li>
<li>automate deployments for certain branches</li>
<li>add linting and testing for Helm charts</li>
<li>dynamically create environments</li>
<li>use a Helm repository</li>
<li>think about application configuration vs infrastructure configuration</li>
<li>implement the CI pipeline as code</li>
</ul>

But the bare minimum is to be able to deploy whatever, wherever. And that's complete!
