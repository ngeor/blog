---
layout: post
title: w3c-nant version 1.1.0 released
date: 2012-06-17 09:58:00.000000000 +02:00
published: true
tags:
  - pet project
  - w3c-nant
  - NAnt
  - ".NET"
---

A new version for w3c-nant was released today. What is new in this version:

<ul>
<li>The project is now targeting .NET 4 instead of .NET 3.5. That is the reason why this version is 1.1.0 and not 1.0.3.</li>
<li>There are now two DLLs, W3CValidationTasks.dll and a new one called W3CValidationTasks.Core.dll. The new DLL contains most of the logic but without requiring NAnt. The old DLL is now a thinner layer, exposing that logic as NAnt tasks.</li>
<li>A bug was fixed in the ftpUpload task, where uploading would fail if the target folder didn't already exist. Now the ftpUpload task will first ensure that the necessary folders exist (or otherwise it will create them) and then it will upload the files.</li>
</ul>

You can download the latest version from the
<a href="http://w3c-nant.sourceforge.net/">project's page on SourceForge</a>.
