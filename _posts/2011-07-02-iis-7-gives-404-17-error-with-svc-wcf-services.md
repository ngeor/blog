---
layout: post
title: IIS 7 gives 404.17 error with svc WCF services
date: 2011-07-02 22:07:00.000000000 +02:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

If you try to access a svc service hosted in IIS and you get the following error:
<blockquote>

HTTP Error 404.17 - Not Found - The requested content appears to be script and will not be served by the static file handler.
</blockquote>

the cause is most likely misconfigured handler mappings for the svc file extension. The correct mapping for the svc file depends on the application pool's .NET version and managed pipeline mode.

There is an easy way to restore the correct mapping for the svc file extension. If you're using .NET 2.0 in your pool, you can run the command "<a href="http://msdn.microsoft.com/en-us/library/ms732012.aspx" target="_blank">ServiceModelReg.exe</a> -i" from the folder "C:WindowsMicrosoft.NETFrameworkv3.0Windows Communication Foundation". If you're using .NET 4.0, you can run the command "<a href="http://msdn.microsoft.com/en-us/library/k6h9cz8h%28v=VS.100%29.aspx" target="_blank">aspnet_regiis.exe</a> -i" from "C:WindowsMicrosoft.NETFrameworkv4.0.30319".

There's a catch here. If your IIS hosts both .NET 2.0 and .NET 4.0 sites, .NET 4.0 settings will disappear as soon as you run the ServiceModelReg.exe command and your .NET 4.0 site won't work anymore. If that's the case, make sure you run first the ServiceModelReg.exe command and after that's done run the aspnet_regiis.exe.
