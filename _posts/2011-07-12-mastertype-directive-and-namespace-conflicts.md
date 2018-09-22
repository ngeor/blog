---
layout: post
title: MasterType directive and namespace conflicts
date: 2011-07-12 21:25:00.000000000 +02:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

Let me start by saying that I hope you won't run into this one and that you probably won't.

In ASP.NET you can use the <a href="http://msdn.microsoft.com/en-us/library/ms228274.aspx" target="_blank">MasterType</a> directive in your pages to have a strongly typed reference to your master page class. So if you add this directive on top of your page:

```
<%@ MasterType VirtualPath="~/MyMasterPage.master" %>
```

You page now has a strongly typed reference to your master page. The Master property has been overriden and now you can access your master page's properties and methods directly:

```
protected void Page_Load(object sender, EventArgs e)
{
  // assuming our master page has a property called MySiteName
  Title = Master.MySiteName + " - Home Page";
}
```

Behind the scenes, it's the automatically generated designer code that makes this possible. The MasterType directive causes the Master property to be overriden in the aspx.designer.cs file:

```
public new MyWebApp.MyMasterPage Master
{
  get
  {
    return (MyWebApp.MyMasterPage)base.Master;
  }
}
```

So far so good. There's one rare scenario that can break this nice setup. If the root namespace element is repeated somewhere inside the namespace of the master page, the automatically generated code doesn't compile anymore. I think an example is probably needed here to see what I am talking about.

If your fully qualified type name of your master page is for example MyWebApp.Templates.MyWebApp.MyMasterPage, the code doesn't compile anymore because of the automatically generated code:

```
public new MyWebApp.Templates.MyWebApp.MyMasterPage Master
{
  get
  {
    return (MyWebApp.Templates.MyWebApp.MyMasterPage)base.Master;
  }
}
```

This doesn't compile anymore, because the "MyWebApp" will be interpreted as "MyWebApp.Templates.MyWebApp" and it is actually trying to find MyWebApp.Templates.MyWebApp.Templates.MyWebApp.MyMasterPage ! Amazing. Had the auto generating tool emitted a simple "global::" in front of the type, this would have worked.

Technically, we can blame the auto generated code. The big question is why would you want to setup your namespaces like that and I have no answer to that. I can only say that I've seen this one too.

You might think you can win this hopeless situation by using the variation of the MasterType directive with the TypeName attribute.

```
<%@ MasterType TypeName="MyWebApp.Templates.MyWebApp.MyMasterPage" %>
```

instead of specifying the virtual path, we specify the type of our master page. This doesn't make the situation any different. But you might try to specify the global prefix or the correct type yourself:

```
<%@ MasterType TypeName="global::MyWebApp.Templates.MyWebApp.MyMasterPage" %>
```

or

```
<%@ MasterType TypeName="MyWebApp.MyMasterPage" %>
```

Surprisingly, this will get your code to compile! The TypeName attribute gets copied as-is directly to the designer code file so both these options pass compilation. However, now the page will throw an exception at run time, complaining that the type can't be found... it's a lose lose situation. Just don't set-up your namespaces like that, not just because of this problem, but for sanity's sake.
