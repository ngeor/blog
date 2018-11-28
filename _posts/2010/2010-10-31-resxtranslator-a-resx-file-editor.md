---
layout: post
title: 'ResxTranslator: a resx file editor'
date: 2010-10-31 12:43:00.000000000 +01:00
published: true
categories:
- Code
tags:
- pet project
- ResxTranslator
---

<a href="https://sourceforge.net/projects/resxtranslator/" target="_blank">ResxTranslator</a> is an open source project that facilitates easy translation of resx files. Resx files are XML files that .NET uses to store localizable strings. Visual Studio offers a built-in designer but MonoDevelop currently doesn't offer support for resx files. In addition to that, ResxTranslator is able to open multiple files in the same window, so that a user can translate strings while looking at the original text at the same time. Oh, and it is at this moment developed only by me when I have some time to spare :-)<!--more-->

At this moment ResxTranslator offers two separate UIs: one for Windows only, built using Windows Forms and one for Mac OS X and Linux, built using Gtk#. The project is in alpha version but it should offer basic capabilities. The following screenshots demonstrate the usage of ResxTranslator, shown in Ubuntu 10.10:

<img src="{{ site.baseurl }}/assets/2010/resxtranslatorgtk-empty.png" />

This is the initial view of the Gtk UI of ResxTranslator, in Ubuntu 10.10. Clicking the open button opens up the standard file open dialog, shown in the following screenshot:

<img src="{{ site.baseurl }}/assets/2010/resxtranslatorgtk-two-files.png" />

Two files are selected: the default resources (labels.resx) and the greek translation (labels.el.resx). By the way these are the actual resx files of the BlogEngine.NET project.

<img src="{{ site.baseurl }}/assets/2010/resxtranslatorgtk-open-dialog.png" />

In the following screenshot the two files are loaded and displayed in parallel for easy translation.

<img src="{{ site.baseurl }}/assets/2010/resxtranslatorgtk-editing.png" />

The "action" resource has not been yet translated to Greek. Clicking on the cell switches to edit mode where it is possible to fill-in the translated value:

Clicking the Save button will save the changes to disk.

So far only this simple editing is supported; there is no support yet for adding new keys. Also, the Gtk version needs to be compiled from its sources, there is no binary package available at this time.
