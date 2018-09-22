---
layout: post
title: WCF, JSON and the DateTime
date: 2011-07-20 20:18:00.000000000 +02:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

I'm playing with a WCF service that works with JSON. If you haven't done this already, it's fairly easy. In the web.config, make sure your service is using the webHttpBinding binding. Also you'll need an endpoint behavior that looks like this:

```xml
<endpointBehaviors>
  <behavior name="MyBehavior">
    <webHttp />
  </behavior>
</endpointBehaviors>
```

Also, you'll need to annotate your operation methods with an attribute that tells WCF to use JSON (otherwise it uses XML):

```cs
[OperationContract]
[WebInvoke(
    Method = "POST",
    BodyStyle = WebMessageBodyStyle.Bare,
    RequestFormat = WebMessageFormat.Json,
    ResponseFormat = WebMessageFormat.Json)
]
```

That's it.

I had some problems however with the DateTime type. Unfortunately JSON doesn't have a standard for dates so Microsoft chose <a href="http://msdn.microsoft.com/en-us/library/bb299886.aspx#intro_to_json_sidebarb" target="_blank">its own way</a>. Basically it looks like "/Date(1224043200000)/"; the number represents the count of milliseconds since <a href="http://en.wikipedia.org/wiki/Unix_epoch" target="_blank">epoch</a>.  So when you're consuming your service, you'll have to deserialize this format yourself. You can find some suggestions <a href="http://stackoverflow.com/questions/206384/how-to-format-a-json-date" target="_blank">here</a>, I picked the simple:

```js
new Date(parseInt(jsonDate.substr(6)))
```

So if the date is represented by the count of milliseconds since epoch, what happens with older dates? This gave me a headache today, trying to figure out why my service wasn't returning anything... I had forgotten some DateTime set to its default value, which in .NET is 0000-00-00 00:00... I wasn't getting any error message whatsoever so I was troubleshooting blindly and the date was the last place to look. Usually it's some object referencing some other object that shouldn't or something like that...

Another promising solution is to use the <a href="http://james.newtonking.com/pages/json-net.aspx" target="_blank">Json.NET library</a> which offers a custom date time formatting which is more human readable, but I didn't try it out, I just made sure all my dates where properly set.

Hope this helps.
