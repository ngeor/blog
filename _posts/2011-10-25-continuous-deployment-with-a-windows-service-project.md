---
layout: post
title: Continuous Deployment with a Windows Service project
date: 2011-10-25 19:08:00.000000000 +02:00
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

For a long time now I had a long running process here at home implemented as a Windows Console application. The application was quite stable, but from time to time I had to fix a bug or add a new feature. Before deploying a new version, I would have to login to the deployment machine where the application was running and terminate it, otherwise deployment would fail trying to copy over the new files. Quite tedious. And then I would have to start it again, as soon as the deployment server had finished its job. I like to automate this kind of things.

Converting the application to a Windows Service is something I should have done in any case. But it turns out it also solves this particular problem too. Say hello to the <a href="http://nant.sourceforge.net/release/0.91/help/tasks/servicecontroller.html" target="_blank">servicecontroller</a> task in NAnt (which, in case you didn't notice, reached version 0.91 finally a couple of days ago). Using this task in your build script, you can start and stop any Windows Service you want. What I did was to modify my build script to stop my Windows Service just before it copies the files and then start it again when the copying is done. All of that done through the build server, no manual steps required.

Oh, by the way, I used <a href="http://www.icsharpcode.net/opensource/sd/" target="_blank">SharpDevelop</a> to create the Windows Service. I only have the free Express edition of Visual Studio at home and that one doesn't support Windows Service projects. Turns out that SharpDevelop supports that and has some nice features too that Visual Studio doesn't even support without Resharper, for instance easily running and debugging NUnit unit tests from within the IDE (ok to be fair you can attach the Visual Studio debugger to the NUnit GUI and debug your unit test, but not in the Express edition).

SharpDevelop also seems to support wix installers, but that's something I didn't try, perhaps some other time.
