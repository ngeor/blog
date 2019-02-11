---
layout: post
title: Playing with MonoMac
date: 2010-11-07 09:26:00.000000000 +01:00
published: true
categories:
- programming
tags: []
---

Yesterday I played a bit with <a href="http://www.mono-project.com/MonoMac" target="_blank">MonoMac</a>, a new framework for Mono that you can use in order to create .NET applications that have a native look and feel in Mac OS X. I have never done any Mac related development in the past so I had to read up on how Apple builts its UIs. My experiments made their way to <a href="http://sourceforge.net/projects/resxtranslator/" target="_blank">ResxTranslator</a>'s code base, so I intend that ResxTranslator will have three separate UIs: WinForms, GTK# and now Cocoa via MonoMac!<!--more-->

In order to play with MonoMac you'll have to do the following things:
<ul>
<li>Get and compile the code from modules <a href="https://github.com/mono/maccore" target="_blank">maccore</a> and <a href="https://github.com/mono/monomac" target="_blank">monomac</a>. They should end up in directories on the same level, so there should be a parent folder containing folders maccore and monomac. Then, from the folder monomac simply run make. In a terminal you could type something like this:

```
git clone https://github.com/mono/monomac.git
git clone https://github.com/mono/maccore.git
cd monomac
make
```

</li>
<li>Add a repository in MonoDevelop: http://addins.monodevelop.com/Alpha/Mac/2.4/main.mrep<img src="{{ site.baseurl }}/assets/2010/repository.png" /></li>
<li>A new add-in will be available: MonoMac development under category Mac Development<img src="{{ site.baseurl }}/assets/2010/addin.png" /></li>
</ul>

MonoMac is not done yet, so I had some problems:
<ul>
<li>The Info.plist file specifies the minimum OS version to 10.6, but I still use Leopard so my app wouldn't run. I had to manually change the number to 10.5.</li>
<li>MonoDevelop cannot launch the application, complaining that there's no Info.plist file: "No Info.plist file in application bundle or no NSPrincipalClass in the Info.plist file, exiting". The only workaround I found by experimenting was to switch to the folder "bin/Debug/ResxTranslatorMac.app/Contents/MacOS" and from there launch the executable. Then the application will launch.</li>
<li>Sometimes, the application would crash with this message: "Non-aligned pointer being freed". Pretty scary for somebody who's been coding without worrying about memory management and pointers for a very long time! I guess it's something the MonoMac team is working on?</li>
</ul>

It's very nice to see that you can code a Mac OS X app without needing to learn Objective C. I hope that MonoMac will soon be a standard add-in in MonoDevelop.
