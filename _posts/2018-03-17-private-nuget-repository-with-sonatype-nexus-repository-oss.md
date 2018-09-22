---
layout: post
title: Private NuGet repository with Sonatype Nexus Repository OSS
date: 2018-03-17 07:00:38.000000000 +01:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags:
- Nexus
- NuGet
author: Nikolaos Georgiou
---

In this post, I'm setting up a private NuGet repository using <a href="https://www.sonatype.com/nexus-repository-oss">Sonatype Nexus Repository OSS</a>.

<!--more-->

I did this setup using a dedicated VM running Ubuntu 16.04 LTS. Some additional prerequisites:
<ul>
<li>Java is a requirement, so I installed the openjdk 8 JRE, which, although it's not officially supported by Sonatype, worked fine for me.</li>
<li>My username in that VM is already <code>nexus</code>.</li>
</ul>

First things first, I downloaded the <code>tar.gz</code> file from the <a href="https://help.sonatype.com/display/NXRM3/Download">Downloads</a> page and unzip it under <code>/opt</code>, e.g.:

```
sudo chown nexus:nexus /opt
wget https://download.sonatype.com/nexus/3/latest-unix.tar.gz
mv latest-unix.tar.gz /opt/
tar -zxf latest-unix.tar.gz
```

This gives two folders under <code>/opt</code>:

```
drwxrwxr-x  9 nexus nexus      4096 Mar  9 07:36 nexus-3.9.0-01/
drwxrwxr-x  3 nexus nexus      4096 Mar  9 07:36 sonatype-work/
```

What I like to do is to create a symbolic link to the specific version, so that I can upgrade and rollback in a safe way without changing other configuration files:

```
ln -s nexus-3.9.0-01 nexus
```

which gives me this layout:

```
lrwxrwxrwx  1 nexus nexus        14 Mar  9 07:46 nexus -> nexus-3.9.0-01/
drwxrwxr-x  9 nexus nexus      4096 Mar  9 07:36 nexus-3.9.0-01/
drwxrwxr-x  3 nexus nexus      4096 Mar  9 07:36 sonatype-work/
```

The next step is to install Nexus as a systemd service. All I had to do was copy <a href="https://help.sonatype.com/display/NXRM3/Run+as+a+Service">the example from the documentation</a> with no changes at all (since my username is already <code>nexus</code> and my installation directory is effectively <code>/opt/nexus</code>).

At this point, it is possible to access the UI at port 8081 (assuming no firewall is blocking it) and <strong>login to Nexus</strong> with the default admin credentials which are <a href="https://help.sonatype.com/display/NXRM3/Accessing+the+User+Interface">admin and admin123</a>.

After logging in, I did two things:
<ul>
<li>change the admin's password</li>
<li>disable anonymous access to the server (Security -> Anonymous -> Allow anonymous users to access the server)</li>
</ul>

On a side note, the UX/UI of Nexus has improved since version 2, but it's still a bit old fashioned in my personal opinion.

Out of the box, Nexus has a ready to use NuGet repository, so I don't have to configure anything there. The repository's feed is available at <code>http://your-nexus-server:8081/repository/nuget-hosted/</code>.

In order to <strong>publish to this NuGet repository</strong>, we need to get an API Key. The API key belongs to a user, so it is available under Account -> NuGet API Key -> Access API Key.

An important thing is that the key won't work if you don't activate the NuGet API Key Security Realm. This is mentioned in the <a href="https://help.sonatype.com/display/NXRM3/Accessing+your+NuGet+API+Key">documentation</a> but it's not intuitive (i.e. why do you get a NuGet repository out of the box, but it's effectively read-only?). To enable it, simply go to Security -> Realms and add the <em>NuGet API Key Security Realm</em> to the list of Active realms.

<strong>Reading packages</strong> from the NuGet repository does not use the API Key but your regular credentials. This might be great for personal use, but it becomes tricky in CI, especially if we are restoring packages inside a Docker container.

The solution I ended up using is to create a <code>NuGet.Config</code> file in the project where I want to use my private NuGet packages. NuGet will take this file into account. In that file, I specify my private feed source:

```
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" protocolVersion="3" />
    <add key="nexus" value="http://my-server:8081/repository/nuget-hosted/" />
  </packageSources>
  <packageRestore>
    <add key="enabled" value="True" />
    <add key="automatic" value="True" />
  </packageRestore>
  <bindingRedirects>
    <add key="skip" value="False" />
  </bindingRedirects>
  <packageManagement>
    <add key="format" value="0" />
    <add key="disabled" value="False" />
  </packageManagement>
  <disabledPackageSources />
  <packageSourceCredentials>
    <nexus>
      <add key="Username" value="viewer" />
      <add key="ClearTextPassword" value="unfortunately it is not encrypted" />
    </nexus>
  </packageSourceCredentials>
</configuration>
```

Unfortunately, the password needs to be unencrypted. NuGet supports encryption, but only for Windows. If you try to use the encrypted password on a Linux build agent (or inside Docker), you get a helpful error message telling you that encryption is at the moment only supported in Windows. When life gives you lemons, you improvise I guess. So my solution here is to create a dedicated user in Nexus (named 'viewer' in this example) that only has the minimum rights needed to read from the NuGet feed. The advantage is that everyone who has access to the source code can instantly access the private NuGet feed without any extra configuration.
