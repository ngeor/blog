---
layout: post
title: BlogEngine.NET MVC - Hello world
date: 2013-03-06 15:02:00.000000000 +01:00
published: true
categories:
- pet-projects
tags:
- BlogEngine.NET MVC
- pet project
---

So, to share a bit more of my excitement, here's a screenshot of the classic ASP.NET and the MVC versions running side by side:

<img src="{{ site.baseurl }}/assets/2013/blogengine-mvc-side-by-side.png" />

So we got a homepage working! Hurray! Keep on reading for more in depth details.<!--more-->
<h3>Copy pasting from the website</h3>

Before we even start, we need to copy paste a few things from the website project into the MVC project:
<ol>
<li>copy pasted the App_Data folder into the MVC project. We have in this way the same start up sample data as the web site project.</li>
<li>modified the Web.config to have the necessary BlogEngine sections, the BlogEngine related app settings and the BlogEngine Membership and Roles providers.</li>
</ol>
<h3>Routing</h3>

For rendering the blog's homepage, we need to map two routes:
<ol>
<li>one route for the primary blog that corresponds to the root URL e.g. http://myhost/</li>
<li>one route for all the secondary blogs that correspond to URLs like http://myhost/myblog/</li>
</ol>

BlogEngine.NET supports multiple blogs (in fact my site is built with that feature) so we're going to support this feature. Unfortunately, the 'myblog' URL segment is in the beginning of the URL so, after a short investigation I did, it seems that optional URL parameters only work at the end of the URL.

The problem is clearer when you think of the URLs that we'll be building next, for instance the URLs of posts and pages. So http://myhost/page/mypage and http://myhost/myblog/page/myotherpage need to be two different routes:
<ol>
<li>page/{pageName}/{action} (primary blog's pages route)</li>
<li>{blogName}/page/{pageName}/{action} (secondary blog's pages route)</li>
</ol>

because the {blogName} parameter appears in the beginning of the URL.

Of course there's going to be only one controller handling this:

```cs
public class PageController
{

    public ActionResult Index(string blogName, string pageName)
    {
    }
```

I'll try again to see if it's possible to do it with a single route definition, but it's not really a problem, just an annoying detail of implementation.
<h3>Routing constraint</h3>

To make sure our secondary blog route doesn't collide with action names, we're going to use a custom routing constraint. Here's how the secondary blog's homepage is mapped:

```cs
routes.MapRoute(
    name: "SecondaryHome",
    url: "{blogName}/{action}",
    defaults: new { controller = "Home", action = "Index" },
    constraints: new { blogName = new BlogNameConstraint() }
    );
```

and here's the implementation of the constraint:

```cs
///
/// Routing constraint that matches a secondary blog name.
///
public class BlogNameConstraint : IRouteConstraint {
  public bool Match(HttpContextBase httpContext, Route route, string parameterName,   RouteValueDictionary values, RouteDirection routeDirection) {
    // match if the blog is active, not deleted, not primary and the name matches of course string blogName = (string)values[parameterName];
    return !string.IsNullOrWhiteSpace(blogName) && Blog.Blogs.Any( b => !b.IsDeleted && !b.IsPrimary && b.IsActive && string.Equals(b.Name, blogName, StringComparison.InvariantCultureIgnoreCase));
  }
}
```

With this constraint, the URL:

http://myhost/Feed will be interpreted as the primary blog's RSS feed (action = Feed).

but this URL:

http://myhost/blog will be interpreted as the secondary blog's homepage (action = Index), and not as the non-existing 'blog' action of the primary blog route.

Unless of course... you chose to name your secondary blog after an existing action of the HomeController. Let's say our HomeController has an action called Feed that renders the RSS feed of the blog (we're probably going to built it). If you call your secondary blog 'Feed', it will be impossible to determine if the URL:

http://myhost/Feed

is supposed to be the primary blog's RSS feed or the secondary blog's homepage.

So the conclusion is: you must not name your secondary blogs after actions of the homepage controller. Also, you shouldn't shoot yourself in the foot, but you already knew that.
<h3>Controller implementation</h3>

The controller's default implementation is very simple:

```cs
    public ActionResult Index(string blogName)
    {
        Blog blog = GetBlog(blogName);
        ViewBag.Blog = blog;
        ViewBag.Posts = Post.Posts.Take(BlogSettings.Instance.PostsPerPage).ToArray();
        return View();
    }
```

this should look familiar to a person who's used BlogEngine before. The important work is happening of course in that GetBlog method. Let's have a look:

```cs
    private Blog GetBlog(string blogName)
    {
        Blog blog;
        if (string.IsNullOrWhiteSpace(blogName))
        {
            // we're loading the primary blog
            blog = Blog.Blogs.FirstOrDefault(b => b.IsActive && b.IsPrimary && !b.IsDeleted);
        }
        else
        {
            // we're loading a secondary blog
            blog = Blog.Blogs.FirstOrDefault(b => b.IsActive
                    && !b.IsPrimary
                    && !b.IsDeleted
                    && string.Equals(blogName, b.Name, StringComparison.InvariantCultureIgnoreCase));
        }

        if (blog == null)
        {
            // TODO: return 404 instead
            throw new InvalidOperationException("Blog not found");
        }

        // important: this will make BlogEngine.Core use this blog as the 'current' blog
        // and don't make any assumptions using the URL etc
        Blog.InstanceIdOverride = blog.Id;
        return blog;
    }
```

So, like I said before, the blogName can indicate we're loading a secondary blog. If it's missing, then we're loading the primary blog of the site.

The BlogEngine API heavily relies on Blog.CurrentInstance, which indicates what the current blog is. When you're loading Posts, it is loading Posts for the current blog. When you're loading blog settings, it is loading the settings of the current blog, and so on. Figuring out what the current blog is, is something that is heavily intertwined with the current HttpContent, the URLs, the request, etc. We really don't want to use that plumbing, because it's not MVC and because we already know what the current blog is based on MVC routing. Luckily, there's an InstanceIdOverride property that we can use to tell BlogEngine.NET what the current blog is. If that property is set, the default logic that evaluates the current blog is never executed.

The code is <a href="https://blogengine.codeplex.com/SourceControl/network/forks/NikolaosGeorgiou/blogenginemvc">available on Codeplex</a>!
