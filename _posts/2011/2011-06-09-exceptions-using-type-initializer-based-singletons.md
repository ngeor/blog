---
layout: post
title: Exceptions using type initializer based singletons
date: 2011-06-09 21:59:00.000000000 +02:00
published: true
tags:
  - singleton
  - ".NET"
  - C#
---

A popular web page describing how to implement a singleton in C# is
<a href="http://www.yoda.arachsys.com/csharp/singleton.html" target="_blank">this
one</a>, where several ways to implement a singleton are discussed. I usually
pick the last option, which, according to the author of that page, has the most
benefits. The author goes on to mention some problems that can occur if an
exception is thrown in the constructor, but I never paid attention to that until
recently.

In our project at work, we implemented a small singleton based on that last
option, the one using type initializers. The purpose of the singleton was to
fetch some records from the database (around 200 of them) and cache them in
memory. The call to fetch the records from the database was done in the
constructor of the singleton, so our code looked more or less like this:

```cs
public sealed class Singleton
{
    private Dictionary cache;

    Singleton()
    {
        // access database
        cache = RetrieveData();
    }

    public string GetValue(string key)
    {
        return cache[key];
    }

    private Dictionary RetrieveData()
    {
        // access the heavy database query
        return data;
    }

    public static Singleton Instance
    {
        get
        {
            return Nested.instance;
        }
    }

    class Nested
    {
        // Explicit static constructor to tell C# compiler
        // not to mark type as beforefieldinit
        static Nested()
        {
        }

        internal static readonly Singleton instance = new Singleton();
    }
}
```

Most of the above code is the boilerplate singleton code. Notice that in the
constructor of the Singleton class, the database is been accessed.

What will happen is the database is out of reach temporarily? We were
experiencing some SQL timeouts. I thought that once the SQL problems had been
resolved, .NET would be able to create the singleton normally. I found however
that this isn't the case. Once an exception is thrown in the type
initialization, the exception just stays there and gets thrown for ever and
ever. The exception never goes away. Our database logs got many error rows about
the same exception, which kind of gave it away. Since the singleton was accessed
in the URL rewriter of our site, it basically made the entire site give the 500
page until somebody restarted IIS. Ouch.

The bug however didn't occur that often. First of all, we didn't have that many
database problems. Secondly, the database problem would have to occur at the
same time when the singleton was initialized. In the entire life span of the web
application (and therefore the singleton), that's a bit improbable. Yet, it
happened. Twice. But it got noticed so here's what I did to solve this.

This is a different way to write the class. The same singleton pattern is used
while the class doesn't suffer from this problem:

```cs
public sealed class Singleton
{
    private Dictionary cache;
    <strong>private object cacheLock = new object();</strong>

    Singleton()
    {
    }

    public string GetValue(string key)
    {
        <strong>EnsureData();</strong>

        return cache[key];
    }
<strong>
    private void EnsureData()
    {
        if (cache == null)
        {
            lock (cacheLock)
            {
                if (cache == null)
                {
                    cache = RetrieveData();
                }
            }
        }
    }</strong>

    private Dictionary RetrieveData()
    {
        // access the heavy database query
        return data;
    }

    public static Singleton Instance
    {
        get
        {
            return Nested.instance;
        }
    }

    class Nested
    {
        // Explicit static constructor to tell C# compiler
        // not to mark type as beforefieldinit
        static Nested()
        {
        }

        internal static readonly Singleton instance = new Singleton();
    }
}
```

What did we change? The constructor is now empty. That means that the singleton
pattern is now responsible only for one thing: initializing the singleton in a
thread safe way. Nothing more, so nothing can go wrong with the type
initialization. So we got rid of the "permanent" exception problem.

We still need to load the cache in a thread safe way. That is been done with the
EnsureData method. If the cache hasn't been populated yet, we lock on the helper
cacheLock object to ensure only one thread can continue from there on. We check
again that the cache is still null and then we access the database. This
technique is called the
<a href="http://en.wikipedia.org/wiki/Double-checked_locking" target="_blank">Double-checked
locking</a>. With this implementation, SQL timeouts will end up to the 500 page
as expected, but once the database is back online the site will resume working
normally.

If you would like to see it in action, you can paste the following code in a
demo web application. In your Default.aspx Page_Load, access the
Singleton.Instance.Greet method. See that "DateTime.Now.Minutes < 30" line?
Change it to something that will throw an exception, so if the time is 11:47,
make it for instance "DateTime.Now.Minutes < 50". When you load the
Default.aspx, you will get an exception with the date time as an error message.
Loading the page over and over again will still show the same date and time when
the exception first occurred and the exception will keep on occurring, even
after the time has passed 11:50.

```cs
public sealed class Singleton
{
    private Dictionary cache;

    Singleton()
    {
        if (DateTime.Now.Minutes < 30)
        {
            throw new Exception(DateTime.Now.ToString());
        }
    }

    public string Greet()
    {
        return "Hello world";
    }

    public static Singleton Instance
    {
        get
        {
            return Nested.instance;
        }
    }

    class Nested
    {
        // Explicit static constructor to tell C# compiler
        // not to mark type as beforefieldinit
        static Nested()
        {
        }

        internal static readonly Singleton instance = new Singleton();
    }
}
```

It's a tricky situation, one of those .NET features that you probably only get
to know the hard way. Hope this helps.
