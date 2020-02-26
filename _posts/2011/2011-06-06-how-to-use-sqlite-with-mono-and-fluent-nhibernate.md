---
layout: post
title: How to use SQLite with Mono and Fluent NHibernate
date: 2011-06-06 20:35:00.000000000 +02:00
published: true
categories:
- tech
tags: []
---

So I have setup my project playing nice in Windows .NET 4.0 with SQLite and Fluent NHibernate. I opened it up from my Mac to see if it would still work and, big surprise, it didn't. It complained about System.Data.SQLite.dll not found, even though the dll was there.

I struggled a bit with this; the <a href="http://system.data.sqlite.org/" target="_blank">official page</a> is quite bad and what's more than that it doesn't offer precompiled dlls but some installer. Searching a bit more, I found that Mono has its own implementation at assembly Mono.Data.Sqlite. I removed the reference to System.Data.SQLite and referenced Mono's assembly... still nothing. The problem is that Fluent NHibernate was still trying to find System.Data.SQLite.dll. Apparently something was missing from this piece of my code:

```
private IPersistenceConfigurer ConfigureSQLite()
{
  return SQLiteConfiguration.Standard.UsingFile(DbFile);
}
```

Well I was very lucky at this point because I found <a href="http://intellect.dk/post/Why-I-love-frameworks-with-lots-of-extension-points.aspx" target="_blank">this article</a> that explains how to tell NHibernate to use Mono.Data.Sqlite. The first part, which is to include the small driver class MonoSqliteDriver that works with Mono.Data.Sqlite, stays the same. I still had to that. But with Fluent NHibernate the second part is done in code (and not configuration) like this:

```
private IPersistenceConfigurer ConfigureSQLite()
{
  return SQLiteConfiguration
      .Standard
      .Driver<MonoSqliteDriver>()
      .UsingFile(DbFile);
}
```

And that's it! Hope this helps.
