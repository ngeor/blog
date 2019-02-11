---
layout: post
title: WCF and deferred execution - where is my Exception?
date: 2011-10-23 17:00:00.000000000 +02:00
published: true
categories:
- programming
tags: []
---

A long time ago, I blogged about <a href="/2010/09/deferred-linq-queries-in-wcf-services" target="_blank">WCF and deferred LINQ queries</a> and some surprises that combination may have. Back then, our WCF service would crash inexplicably when the returning type of an operation would contain an enumerable whose evaluation was deferred until after the WCF operation was out of scope.

Today I'll revisit the same problem with a different approach: the missing exception.

Consider this small WCF service implementation:

```
public class DemoService : IDemoService
{
    public IEnumerable<string> GetNames()
    {
        try
        {
            return DoGetNames();
        }
        catch (Exception ex)
        {
            // TODO: Log exception
            return Enumerable.Empty<string>();
        }
    }
}
```

The implementation is hidden in the DoGetNames method, which we'll see in a moment. I had a similar implementation in a project recently, and I thought that the try catch statement here would protect me from all unexpected exceptions that may occur in DoGetNames. However, that wasn't the case. Once again, the cause was deferred execution. Let's see a very basic implementation of DoGetNames that can cause this problem:

```
private IEnumerable<string> DoGetNames()
{
    yield return "Alice";
    yield return "Bob";
    throw new ApplicationException("I am throwing an exception");
}
```

Because DoGetNames is implemented with a deferred execution iterator, it really doesn't get invoked until after the execution leaves the try catch block. So not only our exception is not logged, but on top of that the client's call fails. I had spent some time wondering why on earth my exception was not been logged at all... until I thought to start searching for these kind of cases.

So if you're thinking that you've safe guarded your WCF operations with a simple try catch, make sure you haven't missed any sneaky LINQ statements or similar code that is lazily executed.

Hope this helps.
