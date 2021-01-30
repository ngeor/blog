---
layout: post
title: BlogEngine.NET MVC - Login time
date: 2013-03-07 09:11:00.000000000 +01:00
published: true
tags:
- BlogEngine.NET MVC
- pet project
- ".NET"
- C#
---

It's not difficult to implement a basic login system. BlogEngine.NET comes with its own membership and roles providers, so all we need to do is create a controller that uses the standard Membership features of .NET.<!--more-->

To speed things up, I copy pasted the AccountController that is generated when you create a new MVC project in Visual Studio and select the template Internet Application. That controller actually does a whole lot more than what we need (e.g. authenticate via Facebook), so I removed the extra parts, keeping only the login functionality.

The login form does look a bit crappy, but I'm not interested in styling anything so far:

<img src="{{ site.baseurl }}/assets/2013/blogengine-mvc-login.png" />

And after logging in with admin admin (the default credentials of BlogEngine.NET), you get a nice welcome message in the homepage:

<img src="{{ site.baseurl }}/assets/2013/blogengine-mvc-logged-in.png" />

We're logged in!
<h3>But wait, there's more!</h3>

I added some HTML into the layout (it seems that's the name for master pages in ASP.NET MVC) of the site that is dependent on the current blog. That means that for every view that is been rendered, it is important we don't forget to set the Blog.InstanceIdOverride property, otherwise BlogEngine.NET will attempt to figure out the current blog on its own.

Now, we could go and make some base controller class that has that functionality as a method, but it's too soon to start building class hierarchies that we might later regret (although the base controller will probably come in handy later). Plus, ASP.NET MVC has a cool feature called <a href="http://www.asp.net/mvc/tutorials/older-versions/controllers-and-routing/understanding-action-filters-cs">action filters</a>. You can create a .NET attribute and decorate an action or even a controller and affect the executing action.

With that in mind, I implemented a SetCurrentBlogAttribute and I decorated my two controllers (HomeController and AccountController). The attribute intercepts each executing action and determines what the current blog is. The implementation is based on the GetBlog method we saw in the [previous post]. The whole attribute implementation looks like this:

```cs
[AttributeUsage(AttributeTargets.Class | AttributeTargets.Method, AllowMultiple = false, Inherited = true)]
public class SetCurrentBlogAttribute : ActionFilterAttribute
{
    public override void OnActionExecuting(ActionExecutingContext filterContext)
    {
        base.OnActionExecuting(filterContext);

        string blogName = null;
        if (filterContext.RouteData.Values.ContainsKey("blogName"))
        {
            blogName = filterContext.RouteData.Values["blogName"] as string;
        }

        Blog blog;
        if (string.IsNullOrWhiteSpace(blogName))
        {
            // we're loading the primary blog
            blog = Blog.Blogs.Find(b => b.IsActive && b.IsPrimary && !b.IsDeleted);
        }
        else
        {
            // we're loading a secondary blog
            blog = Blog.Blogs.Find(b => b.IsActive
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
    }
}
```

So, as long as there is a 'blogName' parameter in the route, the correct blog will be set as current blog and we'll be able to seamlessly use the standard BlogEngine.Core API.

Coming up next? Building up post and page links... stay tuned!

[previous post]: {% post_url 2013/2013-03-06-blogengine-net-mvc-hello-world %}
