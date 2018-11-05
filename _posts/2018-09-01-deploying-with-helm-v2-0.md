---
layout: post
title: Deploying with Helm v2.0
date: 2018-09-01 08:00:48.000000000 +02:00
published: true
categories:
- Code
tags:
- continuous delivery
- Helm
- Kubernetes
---

In the series with Helm and Continuous Delivery nine months ago, I used <a href="{{ site.baseurl }}/2017/12/02/cd-with-helm-part-5-versioned-artifacts.html">helm to deploy the application to the kubernetes cluster</a>. To be able to do that from the CI server, I had to make a workaround. I had punched a hole in the cluster with a NodePort service for Tiller. This allows pretty much anyone to reach Tiller (the server side component of Helm) and interact with it. Great for a demo blog post, but not so great for security.

<!--more-->

Here is a different way to reach Tiller. Helm works with the same configuration of kubectl. That configuration is in the <code>~/.kube/config</code> file. We can copy the contents of that file, base64 encode it, and store it in a secure environment variable in the CI server. During deployment, we can do the reverse: base64 decode the variable and write it into the file where kubectl and Helm expect it.

One small caveat is that the file might contain references to other files and certificates. To avoid dealing with multiple files, kubectl offers a handy command that exports the entire configuration as a single file: <code>kubectl config view --flatten</code>

Together with base64, in a bash command line (with <code>-w0</code> to avoid issues with new lines):

```
kubectl config view --flatten | base64 -w0
```

Copy paste that value and save it in the CI server as a secure environment variable under the name <code>KUBECTL_CONFIG</code> (or any other name you like).

And in the deployment script, you can use it like this:

```
mkdir -p ~/.kube
base64 -d "$KUBECTL_CONFIG" > ~/.kube/config
```

