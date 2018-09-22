---
layout: post
title: SystemWebCompanion
date: 2011-03-19 18:10:00.000000000 +01:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

In many ASP.NET web applications, there are some small bits of code that you have to write over and over again. They're too small so you never bother to refactor them out as a reusable dll. After all they are so small that it's very fast to create from scratch again. They end up as a Utils.cs file somewhere in your project, probably repeated in all your projects in one form or another.

Suffering from the same disease, I decided to create a small project for that. Its name is SystemWebCompanion. Its goal to create various small conveniences that ASP.NET web applications usually need.

The following features are currently included (version 1.1.0):
<ul>
<li>Extension method to get the application path terminated with a slash (how many times have you coded this one?)</li>
<li>Extension method to log an exception using log4net (and the inner exceptions too)</li>
<li>Common page title prefix for every page in the application. Useful for apps where every page's title begins with some common text, such as the site's title.</li>
<li>Web control to render the Google Analytics script, with the ability to turn it off for local development.</li>
</ul>

Not much, but at least you'll never have to code them again!

The project is <a href="http://sourceforge.net/projects/syswebcompanion/" target="_blank">hosted at SourceForge</a>. If you use NuGet, you can already <a href="http://nuget.org/List/Packages/SystemWebCompanion" target="_blank">search for SystemWebCompanion in the online gallery</a>.

Let's see some examples on how to use the forementioned features.

The methods to get the application path terminated with a slash:

```cs
// bring extension methods in scope
using System.Web.Companion;

// get the application path. "/" for sites, "/myapp/" for virtual directories.
string path = Request.SlashedAppPath();

// get the absolute application path. "http://mysite/" for sites,
// "http://mysite/myapp/" for virtual directories.
string absolutePath = Request.AbsoluteAppPath();
```

To use the common title prefix, you need to use a master page and derive from the CompanionMasterPage class:

```cs
using System.Web.Companion;

[SiteTitlePrefix("My Web Site", " - ")]
public class MyMasterPage : CompanionMasterPage {
}
```

To use the Google Analytics web control:

```html
<swc:GoogleAnalytics runat="server" SiteId="UA-1234-123" />

// by default it will not render on localhost. If you want it:
<swc:GoogleAnalytics runat="server" SiteId="UA-1234-123"
    ShowOnLocalhost="true" />
```

Note that swc tag prefix. It stands for SystemWebCompanion. If you install via NuGet, your web.config will be modified automatically to register the swc prefix.

Hope this helps.
