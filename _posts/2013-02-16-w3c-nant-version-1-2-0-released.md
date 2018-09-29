---
layout: post
title: w3c-nant version 1.2.0 released
date: 2013-02-16 16:14:00.000000000 +01:00
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

Version 1.2.0 of w3c-nant was released today. This version contains some improvements submitted by Rob Richardson:
<ul>
<li>ability to store the status code of an FTP task in a property, using the new resultproperty attribute</li>
<li>better handling of exceptions</li>
<li>ftpUpload task exposes the overwritecondition attribute, which was previously only available through the core API. This way you can control when remote file will be overwritten during upload.</li>
<li>less messages in the log file, unless verbose is turned on</li>
</ul>

Also a small bug was fixed regarding the Never value of overwrite condition: instead of uploading only files that don't exist remotely, this mode would instead always overwrite remote files and never upload new ones.
