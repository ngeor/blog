---
layout: post
title: w3c-nant version 1.1.1 released
date: 2012-06-23 09:31:00.000000000 +02:00
published: true
categories:
- tech
tags: []
---

Short after releasing version 1.1.0, a new bug-fix version is been released.

What is fixed:
<ul>
<li>The FTP upload task should work again. Uploading would hang because the code wasn't closing the FTP stream properly.</li>
<li>The FTP upload task correctly supports single file upload.</li>
</ul>

What is new:
<ul>
<li>a new NAnt task, ftpDelete, that allows deleting a single file on an FTP server</li>
</ul>

You can download the latest version from the <a href="http://w3c-nant.sourceforge.net/">project's page on SourceForge</a>.
