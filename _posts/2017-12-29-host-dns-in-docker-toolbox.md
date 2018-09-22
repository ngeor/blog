---
layout: post
title: Host DNS in Docker Toolbox
date: 2017-12-29 08:01:14.000000000 +01:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags:
- blog-helm-sample
- DNS
- Docker
- Docker Toolbox
author: Nikolaos Georgiou
excerpt: How to configure Docker Toolbox so that it uses your laptop's hosts file.
---

When playing locally on a developer's laptop, it's handy or needed to modify your laptop's hosts file to fake some DNS entries. That's <code>C:\Windows\System32\drivers\etc\hosts</code> on Windows and <code>/etc/hosts</code> on Mac/Linux. By default, Docker Toolbox won't see these custom DNS entries. Here's how to change that.

<!--more-->

In my Windows laptop, I have a custom hosts file which, among others, has the line: <code>192.168.99.100 teamcity.local</code>. If I open a regular Windows command prompt, I can ping that address:

```
> ping teamcity.local

Pinging teamcity.local [192.168.99.100] with 32 bytes of data:
Reply from 192.168.99.100: bytes=32 time<1ms TTL=64
Reply from 192.168.99.100: bytes=32 time<1ms TTL=64
```

From within docker machine, I can't:

```
ngeor@ENVY170124 MINGW64 ~
$ docker-machine ssh
Boot2Docker version 17.12.0-ce, build HEAD : 378b049 - Wed Dec 27 23:39:20 UTC 2017
Docker version 17.12.0-ce, build c97c6d6
docker@default:~$ ping teamcity.local
ping: bad address 'teamcity.local'
```

What about from within a container?

```
$ docker run -it ubuntu bash
# apt update
# apt install iputils-ping
# ping teamcity.local
ping: unknown host teamcity.local
```

To fix that, we need to modify the virtual machine that powers Docker Toolbox. According to the <a href="https://www.virtualbox.org/manual/ch09.html#nat-adv-dns" target="_blank">documentation</a>, what we're experiencing is the default behavior. We need to configure the VM to pass all DNS requests through the host, which will pick up the custom hosts file as well.

First, we need to shut down the virtual machine with <code>docker-machine stop</code>. Then, we modify Docker Toolbox's VM, which by default is named "default":

```
C:\Program Files\Oracle\VirtualBox>VBoxManage modifyvm "default" --natdnshostresolver1 on
```

We can start Docker Toolbox again and try to ping the custom host. First, from within docker machine:

```
$ docker-machine ssh
Boot2Docker version 17.12.0-ce, build HEAD : 378b049 - Wed Dec 27 23:39:20 UTC 2017
Docker version 17.12.0-ce, build c97c6d6
docker@default:~$ ping teamcity.local
PING teamcity.local (192.168.99.100): 56 data bytes
64 bytes from 192.168.99.100: seq=0 ttl=64 time=0.035 ms
```

and then we can also try from within a container:

```
$ docker run -it ubuntu bash
# apt update
# apt install iputils-ping
# ping teamcity.local
PING teamcity.local (192.168.99.100) 56(84) bytes of data.
64 bytes from teamcity.local (192.168.99.100): icmp_seq=1 ttl=64 time=0.028 ms
64 bytes from teamcity.local (192.168.99.100): icmp_seq=2 ttl=64 time=0.036 ms
```

Both cases worked fine. Now the custom hosts file on the laptop is taken into account.
