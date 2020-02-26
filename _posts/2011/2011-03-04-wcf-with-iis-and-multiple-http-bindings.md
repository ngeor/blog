---
layout: post
title: WCF with IIS and multiple http bindings
date: 2011-03-04 19:05:00.000000000 +01:00
published: true
categories:
- tech
tags:
- ".NET"
- WCF
---

If you're writing a WCF service using .NET 3.5 and the service is hosted in IIS, there is a situation where you will get this strange error message:
<blockquote>
This collection already contains an address with scheme http.  There can be at most one address per scheme in this collection.
Parameter name: item</blockquote>

This will happen when the web site in IIS has multiple bindings for the http scheme. This is a common scenario for servers that host multiple sites, where different bindings are used to identify the site based on the host header.
If you can't get rid of the extra bindings in IIS, the following articles provide some insight on how to resolve this issue:
<ul>
<li><a href="http://stackoverflow.com/questions/561823/wcf-error-this-collection-already-contains-an-address-with-scheme-http" target="_blank">A link from Stack Overflow</a></li>
<li><a href="http://blogs.msdn.com/b/rampo/archive/2008/02/11/how-can-wcf-support-multiple-iis-binding-specified-per-site.aspx" target="_blank">A link from a blog at MSDN</a></li>
</ul>

I used these articles to resolve the same problem at work. I managed to solve it with changes to the web.config alone, but I couldn't get the WCF service to listen to both host headers. So, if my web site listens to both mydomain.com and www.mydomain.com, my WCF service can only be accessible from one of these host headers. For that specific problem, the solution was good enough.

Trying to reproduce this configuration at home was impossible. I got different error messages with the same configuration that had done the trick at work. In <a href="http://social.msdn.microsoft.com/forums/en-US/wcf/thread/9e248455-1c4d-4c5c-851c-79d9c1631e21/" target="_blank">another article</a>, I read that this behavior of WCF is "by design", which is enough for me to be just happy that I got it to work in that way and leave it there.

I guess Microsoft realized that this is a much needed feature that should work out of the box and this is how .NET 4.0 works. Supporting multiple bindings in IIS is just a boolean setting:

```xml

<serviceHostingEnvironment multipleSiteBindingsEnabled="true">
</serviceHostingEnvironment>

```

The setting is still false by default, but Visual Studio 2010 will explicitly set it to true in the web.config when creating a new Web Application.

Another good thing is that in .NET 4.0 the error message is more descriptive and helps you resolve the problem:
<blockquote>
This collection already contains an address with scheme http.  There can be at most one address per scheme in this collection. If your service is being hosted in IIS you can fix the problem by setting 'system.serviceModel/serviceHostingEnvironment/multipleSiteBindingsEnabled' to true or specifying 'system.serviceModel/serviceHostingEnvironment/baseAddressPrefixFilters'.
Parameter name: item</blockquote>

Hope this helps.
