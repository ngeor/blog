---
layout: post
title: Using controllers with the same name in ASP.NET MVC
date: 2013-12-17 14:18:36.000000000 +01:00
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---
<h2>Introduction</h2>

Let's consider the following ASP.NET MVC structure:

```
MvcSite
└ Controllers
    ├ HomeController
    └ NewsletterController
└ Models
    └ NewsletterModel
└ Views
    └ Home
        └ Index
    └ Newsletter
        └ Index
```

There's just a homepage, where the view includes a newsletter box rendered as a partial view by the newsletter controller. The newsletter box shows an e-mail and a label asking the user to subscribe to the newsletter.

Imagine that we want to extend the newsletter box functionality, allowing the user to type his name too. However, we don't want to modify the original controller. A possible use case for this is where you have access to the original code but you don't want to modify it, e.g. the code is from an open source application and you want to be able to update to new versions easier (well, it's never gonna be that easy, but ok).

We end up with the following scheme:

```
MvcSite
└ Controllers
    ├ HomeController
    └ NewsletterController
└ Models
    └ NewsletterModel
└ Views
    └ Home
        └ Index
    └ Newsletter
        └ Index
└ Special
    └ Controllers
        └ NewsletterController
    └ Models
        └ NewsletterModel
    └ Views
        └ Newsletter
            └ Index
```

There's a new folder, <code>Special</code>, that contains the familiar MVC structure. However, it only contains what we want to override.

Notice that there are now two controllers by the same name, <code>NewsletterController</code>. They are in the expected namespaces, <code>MvcSite.Controlers</code> and <code>MvcSite.Special.Controllers</code>. However, in ASP.NET MVC the significant identifier of a controller is just its name, not the full type name. Therefore, we have an ambiguity problem.
<h2>Routing</h2>

To fix this, we're going to modify the default route:

```
routes.MapRoute(
    name: "Default",
    url: "{controller}/{action}/{id}",
    defaults: new { controller = "Home", action = "Index", id = UrlParameter.Optional });
```

by <a href="http://stackoverflow.com/questions/5343053/namespaces-equivalent-in-asp-net-mvc">specifying the namespaces</a> it should use:

```
routes.MapRoute(
    name: "Default",
    url: "{controller}/{action}/{id}",
    defaults: new { controller = "Home", action = "Index", id = UrlParameter.Optional },
    namespaces: new[] { "MvcSite.Special.Controllers" });
```

The controllers we haven't overriden will still be picked up as fallback, so the home page, served by the <code>HomeController</code> will still work.

A different solution to the ambiguity problem is to implement an additional route that maps only the overriden controllers. This can be a route identical to the default, but with an extra constraint on the <code>controller</code> parameter. The constraint will check at runtime with reflection if there's a controller class under <code>MvcSite.Special.Controllers</code>.
<h2>View selection</h2>

Even though we're now using the correct controller, the view is still the old one. That's because the controller's action looks like this:

```
public override ActionResult Index()
{
    return PartialView("Index", new NewsletterModel { Reason = "best newsletter ever!" });
}
```

The default view engine is searching still on a path like <code>Views/Controller/Action</code> and the controller is still identified as <code>Newsletter</code>.

One way of solving it is by specifying an explicit file path in the controller action:

```
public override ActionResult Index()
{
    return PartialView("~/Special/Views/Newsletter/Index.cshtml", new NewsletterModel { Reason = "best newsletter ever!" });
}
```

But, arguably, this looks a bit ugly.

We can solve this in a different way, by <a href="http://weblogs.asp.net/imranbaloch/archive/2011/06/27/view-engine-with-dynamic-view-location.aspx">overriding the default view engine</a> in <code>Global.asax</code>:

```
ViewEngines.Engines.Clear();
ViewEngines.Engines.Add(new CustomViewEngine());
```

and the implementation of the <code>CustomViewEngine</code>:

```
public class CustomViewEngine : RazorViewEngine
{
    public CustomViewEngine()
    {
        ViewLocationFormats = new[]
            {
                "~/Special/Views/{1}/{0}.cshtml"
            }.Union(ViewLocationFormats).ToArray();

        PartialViewLocationFormats = new[]
            {
                "~/Special/Views/{1}/{0}.cshtml"
            }.Union(PartialViewLocationFormats).ToArray();
    }
}
```

So we're using a new view engine, based on the default <code>RazorViewEngine</code>, that will first check for view files into our <code>Special/Views</code> subfolder before diving into the default folders.

Note that you'll also need to copy the <code>web.config</code> of the regular Views folder into the Special/Views folder, otherwise compilation of the views <a href="http://stackoverflow.com/questions/6389055/the-name-model-does-not-exist-in-current-context-in-mvc3">won't work</a>.
