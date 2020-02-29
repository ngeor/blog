---
layout: post
title: Compiling Mono and friends on Ubuntu, v2
date: 2014-07-19 18:00:00.000000000 +02:00
published: true
tags:
  - mono
  - ".NET"
  - ubuntu
---

This is an updated guide on how to compile mono from source on Ubuntu. This
time, it’s about Ubuntu 14.04 (trusty tahr). This post covers:

<ul>
<li>mono</li>
<li>xsp</li>
<li>libgdiplus</li>
<li>nuget</li>
<li>nant</li>
<li>mod_mono</li>
<li>gtksharp</li>
<li>vb.net</li>
</ul>

<!--more-->
<h2 id="assumptions">Assumptions</h2>
<ul>
<li>For simplicity, I’ve ommitted the ‘sudo’ from the parts where it is needed.</li>
<li>The source code is going to be checked out under <code>/usr/local/src</code>.</li>
<li>Installation is going to be made in <code>/usr/local</code>.</li>
</ul>
<h2 id="prerequisites">Prerequisites</h2>

These are the basic requirements for a build environment. Remember that
<code>apt-get install</code> is supposed to be run as root.

```
apt-get install git build-essential pkg-config autoconf automake libtool gettext
```

We’ll be checking out the code in <code>/usr/local/src</code>, so lets go and
create that directory:

```
mkdir /usr/local/src
```

After everything is installed you can delete it to save some disk space.
Personally I keep it around in case I want to fetch the latest code again from
upstream and rebuild.

<h2 id="mono">mono</h2>

First, mono itself:

```
cd /usr/local/src
git clone git://github.com/mono/mono.git
cd mono
./autogen.sh --prefix=/usr/local
make get-monolite-latest
make
make install
```

<h2 id="xsp">xsp</h2>

XSP is a web server:

```
cd /usr/local/src
git clone git://github.com/mono/xsp.git
cd xsp
./autogen.sh --prefix=/usr/local
make
make install
```

<h2 id="libgdiplus">libgdiplus</h2>

libgdiplus is needed for drawing and stuff:

```
cd /usr/local/src
git clone https://github.com/mono/libgdiplus.git
cd libgdiplus
git checkout 2.10.8
```

It has some extra prerequisites:

```
apt-get install libglib2.0-dev libjpeg-dev libtiff5-dev libpng12-dev libgif-dev libexif-dev libx11-dev libxrender-dev libfreetype6-dev libfontconfig1-dev
```

Now this is going to be tricky. On Ubuntu 14.04, <strong>it no longer builds
without some editing of the source code</strong>. There are just two files to
edit:

<ul>
<li><code>src/gdiplus-private.h</code></li>
<li><code>tests/Makefile.am</code></li>
</ul>

First, edit <code>src/gdiplus-private.h</code>. Instead of including the
file<code>freetype/tttables.h</code>, you need to include
<code>ft2build.h</code> and <code>FT_TRUETYPE_TABLES_H</code>. This is shown in
the following diff:

```
ngeor@mini:/usr/local/src/libgdiplus$ git diff src
diff --git a/src/gdiplus-private.h b/src/gdiplus-private.h
index 59edf9e..283280d 100644
--- a/src/gdiplus-private.h
+++ b/src/gdiplus-private.h
@@ -30,7 +30,9 @@
 #include <stdio.h>
 #include <math.h>
 #include <glib.h>
-#include <freetype/tttables.h>
+#include <ft2build.h>
+#include FT_TRUETYPE_TABLES_H
+
```

Then, edit the second file that is causing problems,
<code>tests/Makefile.am</code>. You need to add a LIBS dependency, as shown in
the following diff:

```
diff --git a/tests/Makefile.am b/tests/Makefile.am
index 5b8c67c..b07da64 100644
--- a/tests/Makefile.am
+++ b/tests/Makefile.am
@@ -1,4 +1,5 @@
 ## Makefile.am for libgdiplus/tests
+LIBS = $(GDIPLUS_LIBS)

 INCLUDES =
        -I$(top_srcdir)
```

This should be enough to make libgdiplus compile with the usual incantation:

```
./autogen.sh --prefix=/usr/local
make
make install
```

<h2 id="nuget-certificates">nuget certificates</h2>

For every user that is going to be using NuGet, you need to import some
certificates with:

```
mozroots --import --sync
```

This needs to be run only once but it should be run for every user that needs
nuget. That’s also the user that is running your continuous integration builds.

<h2 id="nuget">nuget</h2>

And now, nuget itself. Why not create a script so that nuget can be easily
accessible from the command line?

First, download <code>nuget.exe</code> and copy it to /usr/local/bin/. Then,
create the following script:

```sh
#!/bin/sh
exec mono $MONO_OPTIONS $(dirname $0)/nuget.exe $*
```

and save it as <code>/usr/local/bin/nuget</code>. Don’t forget to grant it
execute permissions.

<h2 id="nant">nant</h2>

I always have some problems when it comes to <code>nant</code>. Usually
something goes wrong with <code>pkg-config</code> or sometimes it defaults to
using .NET 2.0. I tried two approaches here. The first one was to download the
latest tarball and try to install it. The second one was to get the latest
source and build it. I believe that <strong>the second option</strong> is better
in the end. Here are both of them:

<h3 id="first-option-use-the-latest-tarball">first option: use the latest tarball</h3>

Download the latest tarball and extract it into <code>/usr/local/lib</code>. So

Create a shell script named <code>nant</code> and place it in
<code>/usr/local/bin</code>:

```
#!/bin/sh
exec mono $MONO_OPTIONS /usr/local/lib/nant-0.92/bin/NAnt.exe $*
```

you might need to invoke it with <code>MONO_OPTIONS=--runtime=v4.0</code>

You’ll probably need to modify <code>NAnt.exe.config</code> too.

<ul>
<li>set mono-4.5 the default

```
<platform name="unix" default="mono-4.5">
```

</li>
<li>add mono-4.5 definition based on 4.0

```
<framework
              name="mono-4.5"
              family="mono"
              version="4.5"
              description="Mono 4.5 Profile"
              sdkdirectory="${toolDirectory}"
              frameworkdirectory="${toolDirectory}"
              frameworkassemblydirectory="${path::combine(prefix, 'lib/mono/4.5')}"
              clrversion="4.0.30319"
              clrtype="Desktop"
              vendor="Mono"
              >
              <runtime>
                  <probing-paths>
                      <directory name="lib/mono/4.5" />
                      <directory name="lib/mono/neutral" />
                      <directory name="lib/common/4.5" />
                      <directory name="lib/common/neutral" />
                  </probing-paths>
                  <modes>
                      <auto>
                          <engine program="${path::combine(prefix, 'bin/mono')}" />
                      </auto>
                      <strict>
                          <engine program="${path::combine(prefix, 'bin/mono')}">
                              <arg value="--runtime=v4.0.30319" />
                          </engine>
                      </strict>
                  </modes>
              </runtime>
              <reference-assemblies basedir="${path::combine(prefix, 'lib/mono/4.5')}">
                  <include name="*.dll" />
              </reference-assemblies>
              <reference-assemblies basedir="${path::combine(prefix, 'lib/mono/4.0')}">
                  <include name="*.dll" />
              </reference-assemblies>
              <reference-assemblies basedir="${path::combine(prefix, 'lib/mono/3.5')}">
                  <include name="*.dll" />
              </reference-assemblies>
              <reference-assemblies basedir="${path::combine(prefix, 'lib/mono/3.0')}">
                  <include name="*.dll" />
              </reference-assemblies>
              <reference-assemblies basedir="${path::combine(prefix, 'lib/mono/2.0')}">
                  <include name="*.dll" />
              </reference-assemblies>
              <task-assemblies>
                  <!-- include Mono version-neutral assemblies -->
                  <include name="extensions/mono/neutral/**/*.dll" />
                  <!-- include Mono 2.0 specific assemblies -->
                  <include name="extensions/mono/2.0/**/*.dll" />
                  <!-- include .NET 2.0 specific assemblies -->
                  <include name="extensions/common/2.0/**/*.dll" />
              </task-assemblies>
              <tool-paths>
                  <directory name="${toolDirectory}" />
                  <directory name="${path::combine(prefix, 'lib/mono/3.5')}" />
                  <directory name="${path::combine(prefix, 'lib/mono/2.0')}" />
                  <directory name="${path::combine(prefix, 'lib/mono/1.0')}" />
                  <!-- unmanaged tools -->
                  <directory name="${prefix}/bin" />
              </tool-paths>
              <project>
                  <if test="${not pkg-config::exists('mono')}">
                      <fail>Unable to locate 'mono' module using pkg-config. Download the Mono development packages from http://www.mono-project.com/downloads/.</fail>
                  </if>
                  <property name="resgen.supportsexternalfilereferences" value="false" />
                  <property name="prefix" value="${pkg-config::get-variable('mono', 'prefix')}" />
                  <property name="toolDirectory" value="${path::combine(prefix, 'lib/mono/4.5')}" />
              </project>
              <tasks>
                  <task name="al">
                      <attribute name="managed">true</attribute>
                  </task>
                  <task name="csc">
                      <attribute name="exename">mcs</attribute>
                      <attribute name="managed">true</attribute>
                      <attribute name="langversion">linq</attribute>
                      <attribute name="supportspackagereferences">true</attribute>
                      <attribute name="supportsnowarnlist">true</attribute>
                      <attribute name="supportsdocgeneration">true</attribute>
                      <attribute name="supportskeycontainer">true</attribute>
                      <attribute name="supportskeyfile">true</attribute>
                      <attribute name="supportsdelaysign">true</attribute>
                      <attribute name="supportslangversion">true</attribute>
                  </task>
                  <task name="jsc">
                      <attribute name="exename">mjs</attribute>
                      <attribute name="managed">strict</attribute>
                  </task>
                  <task name="vbc">
                      <attribute name="exename">vbnc</attribute>
                      <attribute name="managed">true</attribute>
                  </task>
                  <task name="resgen">
                      <attribute name="managed">true</attribute>
                      <attribute name="supportsexternalfilereferences">true</attribute>
                  </task>
                  <task name="delay-sign">
                      <attribute name="exename">sn</attribute>
                      <attribute name="managed">true</attribute>
                  </task>
                  <task name="license">
                      <attribute name="hascommandlinecompiler">false</attribute>
                  </task>
                  <task name="ilasm">
                      <attribute name="managed">true</attribute>
                  </task>
              </tasks>
          </framework>
```

</li>
</ul>
<h3 id="second-option-build-from-source">second option: build from source</h3>

The following commands might be just enough to install nant:

```
git clone https://github.com/nant/nant.git
cd nant
make install MONO='mono --runtime=v4.0' prefix=/usr/local/ TARGET=mono-4.0
```

Notice the extra parameters trying to convince nant it should use .NET 4.

<h2 id="apache2-modmono">apache2 mod_mono</h2>

If you want to host ASP.NET websites with Apache, you can use mod_mono.

Prerequisites:

```
apt-get install apache2-dev
```

Installation:

```
git clone https://github.com/mono/mod_mono.git
cd mod_mono
./autogen.sh --prefix=/usr/local --with-mono-prefix=/usr/local
make
make install
```

Note that the module configuration is installed in
<code>/etc/apache2/mod_mono.conf</code>. However, the <code>a2enmod</code>
utility is looking for module configurations in the directory
<code>/etc/apache2/mods-available</code>. If you want to use
<code>a2enmod</code>, you should link <code>mod_mono.conf</code> inside the
expected directory. Or, you can just include the module configuration inside
your site configuration as needed. For example:

```
<VirtualHost *:80>
    ServerName my.site.that.runs.mono.com
    DocumentRoot /var/www/
    Include mod_mono.conf
</VirtualHost>
```

<h2 id="gtksharp">gtksharp</h2>

gtksharp is currently building against gtk3. If you need gtk2 support, you can
checkout the latest tag that supports gtk2 and build that. You can also build
both of them and install them side by side.

<h3 id="gtk3">gtk3</h3>

First the prerequisites:

```
apt-get install libgtk-3-dev
```

And then the usual build:

```
git clone https://github.com/mono/gtk-sharp.git
cd gtk-sharp
./autogen.sh --prefix=/usr/local
make
make install
```

<h3 id="gtk2">gtk2</h3>

Prerequisites:

```
apt-get install libgtk2.0-dev libpango1.0-dev libglade2-dev
```

And the build (notice we’re building the tag 2.12.22):

```
git clone https://github.com/mono/gtk-sharp.git gtk-sharp-2
cd gtk-sharp-2
git checkout 2.12.22
./bootstrap-2.12 --prefix=/usr/local
make
make install
```

<h2 id="vbnet">vb.net</h2>

This one goes pretty fast:

```
git clone https://github.com/mono/mono-basic.git
cd mono-basic
./configure --prefix=/usr/local
make
make install
```

<h2 id="summary">Summary</h2>

The above will give you mono (latest and greatest!) and more or less anything
related to it. One thing that is missing is monodevelop, the IDE. Perhaps I’ll
cover that in a future post, together with the programming language boo.
