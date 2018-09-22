---
layout: post
title: Announcing w3c-nant version 1.0.2 - now with FTP upload task!
date: 2012-03-04 11:54:00.000000000 +01:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

I added a new NAnt task in the <a href="https://sourceforge.net/projects/w3c-nant/" target="_blank">w3c-nant</a> library to allow FTP uploads. Using the same <a href="http://nant.sourceforge.net/release/0.91/help/types/fileset.html" target="_blank">fileset</a> mechanism as the <a href="http://nant.sourceforge.net/release/0.91/help/tasks/copy.html" target="_blank">copy</a> task, you can create powerful scripts to automate deploying in a remote FTP server. Or at least that's what I'm using it for!

True, it doesn't make much sense to add an FTP upload task in a library called W3C Validation Tasks, I know... but I didn't want to create another small project just for another small task. So the idea now is that the w3c-nant project will include various NAnt tasks. Not that I have plans for more NAnt tasks, but as long as they are simple enough, they'll end up in that assembly.

So, how to use this new task? Well, another new thing that comes with this release is online documentation! I managed to automate the generation of the <a href="http://w3c-nant.sourceforge.net/api/" target="_blank">api HTML docs</a> with <a href="http://shfb.codeplex.com/" target="_blank">SandCastle Help File Builder</a> and TeamCity. Also the binary release will now contain the CHM file for offline view of the HTML docs.

Although the FTP task is quite preliminary, it does the job. Hope this helps.
