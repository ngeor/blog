---
layout: post
title: 'Tip: Send to Programs Start Menu'
date: 2017-04-15 10:49:15.000000000 +02:00
published: true
categories:
- my-computer
tags:
- start menu
- Windows
---

When it comes to installing software on a Windows laptop, I often prefer portable apps compared to Windows installers. I am also looking currently into Chocolatey as a package manager solution. But also there, I prefer portable apps.<!--more-->

One reason is probably the traumatic experience of the old times where uninstalling an app would leave behind all sorts of debris and made software like <a href="https://en.wikipedia.org/wiki/Norton_CleanSweep" target="_blank">CleanSweep</a> a necessity.

A second reason is that at work we have a strict IT policy: we don't have admin rights on our laptops and we're only allowed to run approved software by IT. The only loophole is that we're allowed to run any software we want, as long as it lives on a magic folder ( C:\ecommerce ).

One extra step I need to do with a portable app is to add it to the Windows Start Menu. The Start Menu has gone through various transformations over the years and it's not as easy to add a shortcut there anymore. How I've been doing it so far:
<ul>
<li>create the shortcut for the app I want to add</li>
<li>open a Windows Explorer to %APPDATA%</li>
<li>navigate to Microsoft, Windows, Start Menu, Programs</li>
<li>paste the shortcut here</li>
<li>profit</li>
</ul>

<figure><img src="{{ site.baseurl }}/assets/2017/04/15/12_29_18-start-menu.png" /><figcaption>Start Menu folder</figcaption></figure>

<figure><img src="{{ site.baseurl }}/assets/2017/04/15/12_30_50-programs.png" /><figcaption>Programs folder inside Start Menu</figcaption></figure>

I found a better way so that I don't have to navigate to the Start Menu folder anymore.

First, create a shortcut to the Programs folder: <img src="{{ site.baseurl }}/assets/2017/04/15/12_32_16-start-menu.png" />

Rename the shortcut to "Copy shortcut to Start Menu":

<img src="{{ site.baseurl }}/assets/2017/04/15/12_33_26-start-menu.png" />

And move this shortcut to the Send To folder:<img src="{{ site.baseurl }}/assets/2017/04/15/12_34_16-sendto.png" />

This folder lives side by side with the Start Menu folder and it controls the Send To context menu. This way, you'll be able to right click on a shortcut and copy it to the Start Menu.

As an example, let's add the KeepassX to the start menu. First locate the executable (I used chocolatey to install it):

<img src="{{ site.baseurl }}/assets/2017/04/15/12_37_57-keepassx-2-0-3.png" />

Right click and create shortcut:

<img src="{{ site.baseurl }}/assets/2017/04/15/12_38_46-keepassx-2-0-3.png" />

Rename the shortcut to "KeePassX" and use the Send To menu to copy it directly to the Start Menu:

<img src="{{ site.baseurl }}/assets/2017/04/15/12_40_02.png" />

The shortcut gets copied to the %APPDATA%\Microsoft\Windows\Start Menu\Programs folder (so you can delete the shortcut in the KeePassX folder). This allows pressing the Windows key and typing "KeePassX" to find the app:<img src="{{ site.baseurl }}/assets/2017/04/15/12_43_21.png" />
