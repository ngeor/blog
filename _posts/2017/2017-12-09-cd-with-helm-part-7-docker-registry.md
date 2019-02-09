---
layout: post
title: 'CD with Helm part 7: Docker registry'
date: 2017-12-09 09:50:43.000000000 +01:00
series: CD with Helm
published: true
categories:
- continuous-delivery
tags:
- blog-helm-sample
- docker
- helm
- kubernetes
- TeamCity
---

In a previous post, we had taken a shortcut: we had TeamCity running inside Kubernetes, sharing its Docker daemon. That trick allowed Kubernetes to access the Docker images produced by our builds. In this post, we'll setup our own Docker registry and publish Docker images there.

<!--more-->

We'll follow the instructions <a href="https://docs.docker.com/registry/insecure/#use-self-signed-certificates" target="_blank">here</a> about setting up a registry with a self-signed certificate. The certificate will need a hostname, we'll be using <code>registry.local</code>.

First, we create a folder named <code>certs</code> and <strong>generate the certificate</strong> there:

```
$ mkdir certs
$ openssl req \
  -newkey rsa:4096 -nodes -sha256 -keyout certs/registry.local.key \
  -x509 -days 365 -out certs/registry.local.crt

Generating a 4096 bit RSA private key
..........++
.......................................................................++
writing new private key to 'certs/registry.local.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:NL
State or Province Name (full name) [Some-State]:Noord Holland
Locality Name (eg, city) []:Amsterdam
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Nikolaos Georgiou
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:registry.local
Email Address []:
```

The important part is the Common Name field, which needs to match the hostname of the registry.

We'll now setup TeamCity outside Kubernetes (so it won't be able to share its Docker anymore) and create the Docker registry. We can use docker compose to put everything together. Here's the <code>docker-compose.yaml</code> we can use:

```
version: '2'
services:
  server:
    image: "jetbrains/teamcity-server:2017.2"
    ports:
    - "8111:8111"
    volumes:
    - ./server/data:/data/teamcity_server/datadir
    - ./server/logs:/opt/teamcity/logs
  agent:
    image: "jetbrains/teamcity-agent:2017.2"
    volumes:
    - ./agent/conf:/data/teamcity_agent/conf
    - /opt/buildagent/work:/opt/buildagent/work
    - /opt/buildagent/temp:/opt/buildagent/temp
    - /var/run/docker.sock:/var/run/docker.sock
    environment:
    - AGENT_NAME=AgentSmith
    - SERVER_URL=http://server:8111/
    links:
    - server
  registry:
    image: "registry:2"
    ports:
    - "5000:5000"
    volumes:
    - ./registry:/var/lib/registry
    - ./certs:/certs
    environment:
    - REGISTRY_HTTP_TLS_CERTIFICATE=/certs/registry.local.crt
    - REGISTRY_HTTP_TLS_KEY=/certs/registry.local.key
```

In this example the <code>docker-compose.yaml</code> file should live side by side with the <code>certs</code> folder. We have quite a few mounted volumes, that's for TeamCity to persist its configuration and data. To avoid setting up our build configuration from scratch, we can backup the old configuration and restore it in the brand new instance. In any case, we can now launch all our services by running <code>docker-compose up -d</code>.

The next step is to <strong>change the build configuration</strong> in TeamCity so that it will publish the Docker image to the new Docker registry. We'll create a configuration property to avoid repeating the <code>registry.local:5000</code> all over the place:

<img src="{{ site.baseurl }}/assets/2017/03-param.png" />

We need to <strong>tag the image</strong>, which is easily done with the native Docker Build runner:

<img src="{{ site.baseurl }}/assets/2017/01-tag-image.png" />

and we need to <strong>push the image</strong> to our registry, which requires a new custom step:

<img src="{{ site.baseurl }}/assets/2017/02-push-image.png" />

We also need to <strong>change the Helm chart</strong> to indicate that the image comes from <code>registry.local:5000/blog-helm</code> and that it should pull the image if it doesn't exist locally. That's in <code>values.yaml</code>:

```
image:
  repository: registry.local:5000/blog-helm
  tag: latest
  pullPolicy: IfNotPresent
```

The remaining parts are actually <em>workarounds</em>, compensating for the fact we're using locally hosted services and self-signed certificates. Let's start with the hostname <code>registry.local</code>. TeamCity now runs on the host's docker, so we can edit <code>/etc/hosts</code> and point <code>registry.local</code> to <code>127.0.0.1</code> (localhost). From Kubernetes's point of view however, localhost won't work, because it will resolve to the internal network of Kubernetes. Here's a quick way of figuring out what IP to use:

```
$ minikube ip
192.168.99.100
$ ifconfig | grep 192.168.99
          inet addr:192.168.99.1  Bcast:192.168.99.255  Mask:255.255.255.0
```

Since minikube's IP is on the 192.168.99.0/24 network, we need to figure out what is the IP of our host on that network. Turns out that's 192.168.99.1 and that's how Kubernetes can reach the registry.

Here's the additions to the hosts file on the host:

```
# custom Docker registry
127.0.0.1 registry.local

# to be able to access the blog-helm hello world app with Ingress
192.168.99.100 blog-helm.local
```

and here's the hosts file inside minikube:

```
192.168.99.1 registry.local
```

The final step is to convince minikube's Docker to <strong>trust our self-signed certificate</strong>. Essentially we need to copy the certificate inside minikube in the folder <code>/etc/docker/certs.d/<em>host:port</em>/ca.crt</code>. We don't need to restart Docker after this:

```
$ minikube ssh
$ mkdir -p /etc/docker/certs.d/registry.local:5000
$ cp /hosthome/ngeor/Projects/teamcity/certs/registry.local.crt ca.crt
```

We're all done, now we can build and deploy using the brand new Docker registry. Here's a pod using the image of the new registry:

<img src="{{ site.baseurl }}/assets/2017/04-dashboard.png" />

Introducing a Docker registry brings out setup one step closer to a more realistic setup. A Docker registry is the authority point where you push (during build) and pull (during deployment) images. In a next post, we'll use AWS and implement a secure Docker registry there. But before that, we'll explore how we can model our DTAP.
