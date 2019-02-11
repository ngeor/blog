---
layout: post
title: Compiling Mono and XSP on Ubuntu
date: 2013-10-19 13:12:00.000000000 +02:00
published: true
categories:
- programming
tags: []
---

For future reference, this is what you need to do in order to install <a href="http://www.mono-project.com/">Mono</a> and <a href="http://www.mono-project.com/ASP.NET">XSP</a> on <a href="http://www.ubuntu.com/download/server">Ubuntu Server 12.04.3 LTS x64</a>. This is about a completely blank installation, where only the SSH server role was selected during the installation of the OS.

You'll need the following commands to set up mono in /usr/local. Keep in mind that <code>apt-get install</code> and <code>make install</code> are going to need root privileges:

```
apt-get install git
apt-get install build-essential pkg-config
apt-get install autoconf automake libtool gettext

git clone git://github.com/mono/mono.git

cd mono
./autogen.sh --prefix=/usr/local
make get-monolite-latest
make
make install
```

And these for XSP:

```
git clone git://github.com/mono/xsp.git
cd xsp
./autogen.sh
./configure --prefix=/usr/local
make
make install
```

And that's it!

References: <a href="http://www.mono-project.com/Compiling_Mono_From_Git">1</a> <a href="http://askubuntu.com/questions/178906/how-to-install-mono-from-source">2</a> <a href="http://www.integratedwebsystems.com/2011/08/install-mono-2-10-3-on-ubuntu-using-bash-script/">3</a>

<strong>Update, 2013-10-27</strong>: Here's a <a href="http://blog.erikd.org/2013/03/17/run-asp-dot-net-mvc4-on-ubuntu-12-dot-10/">related excellent article</a>, which covers additionally the installation of libgdiplus.
