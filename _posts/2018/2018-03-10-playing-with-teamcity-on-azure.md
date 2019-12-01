---
layout: post
title: Playing with TeamCity on Azure
date: 2018-03-10 11:57:38.000000000 +01:00
published: true
categories:
- continuous-delivery
tags:
- ".NET"
- Azure
- Docker
- git
- MSBuild
- TeamCity
---

I spent the past two days playing with setting up TeamCity on Azure. This is just a poc more than anything else, but it's always fun to do something new. I had to fiddle about with some things that didn't work as expected, so here are some notes to remember what I did.

<!--more-->

Luckily, most of the installation is already automated. The journey starts at <a href="https://www.jetbrains.com/teamcity/download/">TeamCity's Download page</a>. Click on Azure and then on the big blue "Deploy to Azure" button. After a few questions, you end up with a CoreOS VM that runs TeamCity server and a local TeamCity agent. A managed MySQL database is also provided for storing TeamCity's data. And at this point basically you're set to go. You can login to TeamCity and create the admin user. It's really easy to get started.

The first problem I noticed is that e-mail notifications don't work, because there's no SMTP server. This is something perhaps that should be highlighted with a notification when you login to TeamCity, something like "SMTP configuration is incomplete".

My next task was to setup a <strong>Windows agent</strong>, because I have some .NET Framework projects that only work properly on Windows. I understand that it's possible to create some sort of template out of a VM, so that TeamCity can start more of these agents if there's need. I didn't follow this path because I don't have the experience and it would be an overkill for a poc. Instead, I just created a Windows VM and setup the TeamCity agent there.

Setting up the Windows VM was also a challenge for me, because I haven't really setup server-side Windows since... well it's probably more than 10 years ago. I picked first "Windows Server, version 1709". To my surprise, this is some stripped down version of Windows that doesn't have a Start Menu or anything high tech like that. It just boots you into a command prompt. So it's like Linux, only I have no idea what I'm doing :-) I quickly killed that VM and opted for a more traditional "Windows Server 2012 R2 Datacenter".

The next challenge was to install the <strong>build tools for .NET</strong>. I think it's not very straightforward, due to renaming of software components over the years. These days it seems it's called <a href="https://www.microsoft.com/en-us/download/details.aspx?id=55168">.NET Framework Developer Pack</a> (instead of SDK). And that one doesn't come bundled with the latest MSBuild, which you have to download separately, but not via MSBuild, but via <a href="https://aka.ms/vs/15/release/vs_buildtools.exe">Visual Studio's build tools installer</a>. I think Microsoft could do a better job here, I had to dig out this information from an article named <a href="https://docs.microsoft.com/en-us/visualstudio/install/build-tools-container">Install Build Tools into a Container</a>.

The cool thing is that after I installed the correct tools, TeamCity Agent recognized them without me having to configure anything else. At this point, I could build traditional .NET Framework projects on the Windows agent.

The next surprise came from the built-in Linux agent when I tried to <strong>build a Docker image</strong>. The agent had the specified capability but it couldn't connect to the Docker socket. I ssh-ed to the machine and saw that both server and agent were running as Docker containers themselves:

```
core@teamcity ~ $ docker ps
CONTAINER ID        IMAGE                                COMMAND   CREATED             STATUS              PORTS                  NAMES
73739a97b83a        jetbrains/teamcity-agent:2017.2.2    "/run-services.sh"   21 hours ago        Up 21 hours         9090/tcp               teamcity-agent
3809474fdcbf        jetbrains/teamcity-server:2017.2.2   "/run-services.sh"   45 hours ago        Up 45 hours         0.0.0.0:80->8111/tcp   teamcity-server
```

I tried to run docker myself from within the TeamCity Agent container, and it failed. I noticed that indeed the <code>/var/run/docker.sock</code> socket was not mounted.

At this point I had to perform the first customization. I modified the systemd script of the TeamCity Agent to mount the <code>/var/run/docker.sock</code> as a volume.

I added this line:

```
  -v /var/run/docker.sock:/var/run/docker.sock \
```

and this is the entire file:

{% raw %}
```
core@teamcity /etc/systemd/system $ cat teamcity-agent.service
[Unit]
Description=TeamCity Agent
After=teamcity-server.service coreos-metadata.service teamcity-update.service
Requires=teamcity-server.service coreos-metadata.service teamcity-update.service

[Service]
EnvironmentFile=/etc/teamcity/version
TimeoutStartSec=1200s
EnvironmentFile=/run/metadata/coreos
ExecStartPre=/bin/sh -c "docker images --filter 'before=jetbrains/teamcity-agent:${TEAMCITY_VERSION}' --format '{{.ID}} {{.Repository}}' | grep 'jetbrains/teamcity-agent' | grep -Eo '^[^ ]+' | xargs -r docker rmi"
ExecStart=/usr/bin/docker run \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /mnt/data/teamcity-agent/logs:/opt/buildagent/logs \
  -v /mnt/data/teamcity-agent/plugins:/opt/buildagent/plugins \
  -v /mnt/data/teamcity-agent/system:/opt/buildagent/system \
  -v /mnt/resource/teamcity-agent/temp:/opt/buildagent/temp \
  -v /mnt/resource/teamcity-server/temp:/opt/teamcity/temp \
  -v /mnt/data/teamcity-agent/tools:/opt/buildagent/tools \
  -e SERVER_URL=${COREOS_AZURE_IPV4_DYNAMIC} \
  -e AGENT_NAME=Default \
  --name teamcity-agent \
  jetbrains/teamcity-agent:${TEAMCITY_VERSION}
ExecStop=-/usr/bin/docker exec teamcity-agent /opt/buildagent/bin/agent.sh stop
ExecStopPost=-/usr/bin/docker stop teamcity-agent
ExecStopPost=-/usr/bin/docker rm teamcity-agent
Restart=always

[Install]
WantedBy=multi-user.target
```
{% endraw %}

I have no idea why this was missing in the first place. With this change, I restarted the teamcity-agent service and I could build and push Docker images to Azure's Container Registry.

One extra customization I had to do on the Linux agent was to convince it to <strong>trust the host key of GitHub and Bitbucket</strong>. This is <strong>not</strong> needed for TeamCity to clone SSH repositories, that works fine. This is needed when I'm trying to use git commands inside build steps.

```
$ docker exec -it teamcity-agent /bin/bash
# ssh-keyscan -H github.com >> /etc/ssh/ssh_known_hosts
# ssh-keyscan -H bitbucket.org >> /etc/ssh/ssh_known_hosts
```

What I'm trying to do in a nutshell:
<ul>
<li>use semantic versioning, deriving the build number from the source code</li>
<li>if that version already exists as a git tag, break the build (but only for the master branch)</li>
<li>when the build succeeds, tag the build (only for the master branch) using VCS Labeling feature of TeamCity</li>
</ul>

To accomplish step 2, I need to run <code>git fetch -t</code> because TeamCity doesn't always fetch all tags... so essentially it's a workaround for TeamCity's cloning/pulling strategy. It would be awesome if they put in the VCS configuration a checkbox that says "Always fetch all tags".

Having worked mostly with TeamCity and Bamboo, it's surprising to see that CI servers do their own little bit of magic in how they manage git working directories. It's safe to say that you're in for some surprises if you assume that things will work because they work on your local computer's git working directory.

And this concludes my TeamCity on Azure adventure so far!
