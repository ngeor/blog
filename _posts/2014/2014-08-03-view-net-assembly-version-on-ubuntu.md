---
layout: post
title: View .NET assembly version on Ubuntu
date: 2014-08-03 06:32:00.000000000 +02:00
published: true
tags:
  - ".NET"
  - ubuntu
  - mono
---

When you want to view the assembly version of a .NET assembly in Windows, you
just right click the DLL and view its properties. Or, you just hover the mouse
over the file and the version number will be shown in the tooltip. In Linux,
things aren’t as easy.<!--more-->

Since this is something I do very rarely, I never remember the command I have to
run. Googling brings me to the
<a href="http://stackoverflow.com/questions/3946368/how-to-get-the-assemblyversion-of-a-net-file-in-linux">correct
stackoverflow answer</a> which indicates I have to run this command:

```
monodis --assembly file.dll | grep Version
```

And indeed this does the trick. But I won’t remember it next time. So this time,
I created a nautilus script to be able to right click on the file. The script
looks like this:

```
#!/bin/bash

VERSION=`monodis --assembly "$@" | grep Version`
zenity --info --text="$VERSION"
```

I’ve saved this script as “Show assembly version” in the directory
<code>~/.local/share/nautilus/scripts</code>. The file manager picks this up and
creates a new menu item which is available by right clicking on a file,
selecting Scripts and then “Show assembly version”:

<img src="{% link /assets/2014/show-assembly-version.png %}" />

The assembly version will be displayed on a popup dialog. Note that the
<code>zenity</code> command is responsible for creating the dialog, so it needs
to be present in the system.

<img src="{% link /assets/2014/show-assembly-version-dialog1.png %}" />

I am using Ubuntu 14.04 but the same should be possible on any desktop running
nautilus as a file manager. Hope this helps.
