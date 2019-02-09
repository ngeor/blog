---
layout: post
title: My local TeamCity setup
date: 2017-12-26 20:46:29.000000000 +01:00
published: true
categories:
- continuous-delivery
tags:
- docker
- TeamCity
---

In my recent blog posts I've played a lot with TeamCity. Often, when I want to blog about something, I end up doing some irrelevant yak shaving, which sometimes is also interesting. In this post I'll show how I'm currently setting up TeamCity locally on my laptop.

<!--more-->

My setup is on a Windows laptop, running Windows 10 Home. This means I have to use <strong>Docker Toolbox</strong>, which runs docker inside a virtual machine and not hyper-v. This is an additional layer that makes things a little bit more complicated.

I'm using <strong>docker compose</strong> to bring up TeamCity Server and Agent, as well as a custom Docker Registry. The configuration, together with some utility scripts, is <a href="https://github.com/ngeor/teamcity-playground">available on GitHub</a>. All volumes are stored under a common subfolder named <code>data</code> (so it's easy to add only one folder in <code>.gitignore</code>).

Here's my <code>docker-compose.yaml</code> file:

```
version: '2'
services:
  server:
    image: "jetbrains/teamcity-server:2017.2.1"
    ports:
    - "8111:8111"
    volumes:
    - ./data/server/data:/data/teamcity_server/datadir
    - ./data/server/logs:/opt/teamcity/logs
    - ./data/git:/git
  agent:
    image: "jetbrains/teamcity-agent:2017.2.1"
    volumes:
    - ./data/agent/conf:/data/teamcity_agent/conf
    - /opt/buildagent/work:/opt/buildagent/work
    - /opt/buildagent/system/git:/opt/buildagent/system/git
    - /opt/buildagent/temp:/opt/buildagent/temp
    - /var/run/docker.sock:/var/run/docker.sock
    - ./data/git:/git
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
    - ./data/registry:/var/lib/registry
    - ./data/certs:/certs
    environment:
    - REGISTRY_HTTP_TLS_CERTIFICATE=/certs/registry.local.crt
    - REGISTRY_HTTP_TLS_KEY=/certs/registry.local.key
```

I have three services, server (TeamCity Server), agent (TeamCity Agent) and registry (Docker Registry). The most straightforward one is the server. There's no customization whatsoever over what is mentioned <a href="https://hub.docker.com/r/jetbrains/teamcity-server/">in the docker hub for this image</a>: port and volume mapping. The only custom thing is the <code>git</code> volume. I use it to store my experimental local git repositories. I will soon change this to be a separate service instead of a local file system.

My TeamCity Agent setup is a bit more interesting:
<ul>
<li>It has a custom agent name (AgentSmith) so it will appear like that in the agent list.</li>
<li>It is linked to the server (that's the <code>links</code> element), which allows us to reference the server by the URL http://server:8111/ without any DNS hacks.</li>
<li>It's re-using the docker daemon of the host, using the <code>/var/run/docker.sock</code> volume. This is great, because otherwise we'd have another virtualization layer inside the first one.</li>
<li>Some volumes like <code>/opt/buildagent/work</code> are not mounted into local folders under <code>./data</code> but as absolute paths of the same name. I'll explain this one in a moment.</li>
</ul>

The last service is the Docker Registry, but there's nothing special going on here, just following <a href="https://docs.docker.com/registry/insecure/#use-self-signed-certificates">documentation</a>.

I'd like to explain a bit the <code>/opt/buildagent/work:/opt/buildagent/work</code> volume mapping. Since I'm running Docker Toolbox, that folder is inside the virtual machine and not directly on my laptop. This is the root folder in which the TeamCity Agent checks out code and runs the builds.

When TeamCity runs a step which uses a Docker image, it offers the current directory as a volume, so that the Docker image will have access to the current working directory. However, I'm running Docker on Docker. That means that in the end these volumes will be resolved by the docker host (in my case, that's the virtual machine of Docker Toolbox). If I don't expose the <code>/opt/buildagent/work</code> volume to the outside world, TeamCity will be mounting a non existing volume and the dockerized build steps will find an empty directory instead of the currently checked out code. It's a bit complicated, but it's important to understand that in the end volumes are resolved at the docker daemon's host.

Finally, I also have a few custom scripts that help me make the setup complete. The <a href="https://github.com/ngeor/teamcity-playground/blob/master/docker-toolbox-provision.sh">first one</a> uses <code>docker-machine</code>. It modifies <code>/etc/hosts</code> so that <code>registry.local</code> points to my IP and it convinces docker to trust my self-generated SSL certificate. <del datetime="2017-12-27T07:46:21+01:00">The <a href="https://github.com/ngeor/teamcity-playground/blob/master/provision-teamcity-agent.sh">second script</a> runs against the TeamCity Agent container and it convinces the agent to trust <code>github.com</code>. Without this, build steps that call git directly fail complaining about host key verification.</del>

<strong>Update:</strong> I removed the need for the second script by building a custom Docker image for the TeamCity Agent:

```
FROM jetbrains/teamcity-agent:2017.2.1

RUN mkdir -p /etc/ssh
RUN ssh-keyscan -H github.com > /etc/ssh/ssh_known_hosts
```
