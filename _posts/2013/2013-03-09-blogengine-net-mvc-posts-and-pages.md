---
layout: post
title: BlogEngine.NET MVC - Posts and Pages
date: 2013-03-09 09:18:00.000000000 +01:00
published: true
categories:
- pet-projects
tags: []
---

In the latest commit on BlogEngine.NET MVC, which is <a href="https://blogengine.codeplex.com/SourceControl/network/forks/NikolaosGeorgiou/blogenginemvc">always available here</a>, the following have been added:

<ul>
<li>Page controller. Pages have URLs like http://localhost/page/my-page or http://localhost/secondary-blog/page/my-page if it's on a secondary blog</li>
<li>Post controller. Post URLs are similar to pages, but the URL segment 'page' changes into 'post'. In addition, BlogEngine.NET supports two versions of URLs: simple (the ones we just described) and timestamped, where the post slug is prefixed by the date of the post. The latter looks like http://localhost/post/2013/03/09/my-post. This preference is set in blog settings and it's already been taken into account in BlogEngine.NET MVC! Depending on the preference, the correct post URL will be generated. Also, the 'incorrect' URL will redirect to the correct one to ensure we don't end up with duplicate URLs (for SEO reasons).</li>
<li>Stub Archive, Contact and Feed views, so that all the URLs of the homepage point to somewhere.</li>
</ul>
<h3>Mapping the post URL</h3>

Mapping the post route is quite simple:

```
// map posts, with timestamped links
MapBlogRoute(routes,
    name: "PostWithTimestamp",
    url: "post/{year}/{month}/{day}/{slug}/{action}",
    defaults: new { controller = "Post", action = "Index" },
    constraints: new { year = @"dddd", month = @"[0-1]d", day = @"[0-3]d" }
    );
```

MapBlogRoute is a helper method that maps the route twice, once for the primary blog and once for the secondary blogs. The constraints make sure we match only numerical values for year, month and day. For month and day, we also make sure the first digit is in the expected range. So if someone tries to access http://localhost/post/2013/20/01/my-post, MVC won't even bother to find the post because no route will match the URL.

We also need to map the post URL without the timestamp. This is the same situation we saw with the blog name parameter: because the date parameters are in the middle of the URL, they can't be simply ignored.

```
// map posts, without timestamped links
MapBlogRoute(routes,
    name: "PostWithoutTimestamp",
    url: "post/{slug}/{action}",
    defaults: new { controller = "Post", action = "Index" }
    );
```

Simple enough!
<h3>Generating URLs to posts</h3>

In the views, we'll be generating links to posts. We want a simple way of passing a post and getting a URL to that post. Plus, the URL should respect the blog settings regarding whether the user wants timestamped post URLs or plain URLs. This is best done in a view helper. Here's the method that does the trick. It's inside HtmlHelpers/UrlHelpers, were more extension methods like these can be put:

```
/// <summary>
/// Gets the URL of a post.
/// </summary>
/// <remarks>
/// <see cref="BlogSettings.TimeStampPostLinks"/> controls if the URL
/// will contain the date of the post or not.
/// </remarks>
/// <param name="urlHelper">The url helper.</param>
/// <param name="post">The post.</param>
/// <returns>The URL of the post.</returns>
public static string PostUrl(this UrlHelper urlHelper, Post post)
{
    BlogSettings blogSettings = BlogSettings.GetInstanceSettings(post.Blog);
    object defaults;
    if (blogSettings.TimeStampPostLinks)
    {
        defaults = new
        {
            blogName = BlogNameInRoute(post.Blog),
            year = post.DateCreated.ToString("yyyy"),
            month = post.DateCreated.ToString("MM"),
            day = post.DateCreated.ToString("dd"),
            slug = post.Slug
        };
    }
    else
    {
        defaults = new
        {
            blogName = BlogNameInRoute(post.Blog),
            slug = post.Slug
        };
    }

    return urlHelper.Action("Index", "Post", defaults);
}
```

To use this helper, we need to import it in the view. It's just an extension method, so basically you just need to import the namespace. Here it is in action inside the updated homepage view:

```
@using BlogEngine.Core
@using BlogEngine.Mvc.Helpers
@{
    ViewBag.Title = BlogSettings.Instance.Name;
}

<h2>@ViewBag.Title</h2>
<ul>
    @foreach (Post post in ViewBag.Posts)
    {
        <li><a href="@Url.PostUrl(post)">@post.Title</a></li>
    }
</ul>
```

What's next? Since we have posts and pages and <a href="/2013/03/blogengine-net-mvc-login-time">we're able to login</a>, maybe next time we can edit a post...
