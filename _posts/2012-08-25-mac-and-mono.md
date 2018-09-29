---
layout: post
title: Mac and Mono
date: 2012-08-25 08:33:00.000000000 +02:00
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

Some random steps on getting my Mac up to speed with Mono development.
<h3>Versions</h3>

I tried to download the latest MonoDevelop (3.0.3.5) but apparently it doesn't work anymore on Mac OS X Leopard, so, after <a href="http://stackoverflow.com/questions/10590268/how-to-download-older-version-of-monodevelop">searching a bit</a>, I used a <a href="http://download.xamarin.com/monodevelop/Mac/MonoDevelop-2.8.8.4.dmg">previous edition</a> (2.8.8.4).

The latest Mono version however works fine (2.10.9_11).
<h3>Environment</h3>

When I run a GTK app through MonoDevelop, it runs fine. When I tried via the command line, it crashed complaining it couldn't find glibsharpglue-2. The problem here was with missing environment variables. I modified /etc/profile like this (<strong>the second and third line are supposed to be on the same line without the dots, I only broke it down to fit the page</strong>):

```
export MONO_FRAMEWORK_PATH=/Library/Frameworks/Mono.framework/Versions/Current
export DYLD_FALLBACK_LIBRARY_PATH="$MONO_FRAMEWORK_PATH/lib:...
...$DYLD_FALLBACK_LIBRARY_PATH:/usr/local/lib:/lib:/usr/lib"
```

<h3>MonoMac</h3>

I created a blank MonoMac application and it would work great but when I tried to open it from Finder it said that this application isn't compatible with my Mac. The problem was that the application template sets a minimum version requirement to 10.6 (Snow Leopard). The solution is to modify Info.plist and set the value of the key LSMinimumSystemVersion to 10.5. Then it works fine also on Leopard.
<h3>Automatic build and TeamCity</h3>

Building through xbuild from the command line doesn't seem to work for MonoMac projects. It complains it can't import some Mono.MonoMac.targets. I used mdtool instead, it's MonoDevelop's command line tool. I created a build configuration in TeamCity with the following settings:
<ul>
<li>Runner Type: Command Line</li>
<li>Command executable: /Applications/MonoDevelop.app/Contents/MacOS/mdtool</li>
<li>Command parameters: build MySolution.sln</li>
</ul>

I also set-up an explicit agent requirement to only allow this build to be run on a Mac (otherwise even my Windows agent would be compatible):
<ul>
<li>system.os.name contains Mac OS X</li>
</ul>

The final step is to get the artifacts. The MonoMac project MyProject, if it builds successfully, it creates a Mac application in the bin/Debug folder. The Mac app is essentially another folder with a special structure and a .app file extension. So what I want is to package that folder in a zip file. To achieve that, I set up the following artifact mapping:
<ul>
<li>MyProject/bin/Debug/MyProject.app => MyProject.zip/MyProject.app</li>
</ul>

When the build is complete, I can download the entire app as a zip file. Double clicking that zip file gives me the app, which I can run or drag into the Applications folder of my Mac. Notice the right side of the artifact mapping, it also references the folder MyProject.app. If you don't include that, the root folder of the app will be missing and after expanding the zip file the contents won't be recognized as an app by Mac OS X.

Hope this helps.
