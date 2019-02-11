---
layout: post
title: First Umbraco experience
date: 2010-08-15 17:40:00.000000000 +02:00
published: true
categories:
- programming
tags: []
---

Today I played a bit with Umbraco for the first time. I mostly focused on its multilingual support, which is a feature I usually expect from a CMS.

<strong>Friendly URLs</strong>

These days it seems that if your URL has a file extension, such as .html or .aspx, it's a sin. I don't get why an extension matters so much for SEO but I'll play along. Umbraco supports this out of the box, by modifying the <strong>web.config</strong> file. In <strong>appSettings</strong>, find the property <strong>umbracoUseDirectoryUrls</strong> and set it to true. That will give you the popular extensionless URLs.

<strong>Multilingual Support</strong>

Being a noob in Umbraco, I googled around a lot to find information about its multilingual support. Most of what I did is based <a href="http://umbraco.org/documentation/books/multilingual-11-sites" target="_blank">on this article</a>. The basic approach is to indicate the language in the query string. I'm going to do the same thing, but I'll use friendly URLs by modifying the configuration file <strong>UrlRewriting.config</strong>, which is in the conifg folder. I added the following rewrite rule:

```
<add name="languageRewrite"
    virtualUrl="^~/(en|el|nl)/([0-9a-z/]+)"
    rewriteUrlParameter="ExcludeFromClientQueryString"
    destinationUrl="~/$2?lang=$1"
    ignoreCase="true" />
```

with this rewrite rule, I get virtual URLs in the form: http://mysite/language/originalurl that will be translated to http://mysite/originalurl?lang=language without the user seeing this translation. This is the way I have organized the URLs in my own website and I like it, but in my case they're not virtual; I have to create them individually. One good enough reason for my to migrate my site to Umbraco :-)

<strong>Using the querystring parameter</strong>

Now all I need is my templates to be aware of this new query string parameter. In the tutorial I consulted I got lost in the XSLT magic, so for the time being I'm using the very simple approach of ASP.NET. Inside my page template:

```
<% if (Request.QueryString["lang"] == "el") { %>
    <umbraco:Item field="message_el" runat="server"></umbraco:Item>
<% } else { %>
    <umbraco:Item field="message" runat="server"></umbraco:Item>
<% } %>
```

It's ugly, but it works and it looks familiar to the ASP.NET developer. If the language on the query string is Greek (the code is el), use the message_el field. Otherwise, fallback to the default (English) message field.

<strong>Overall experience</strong>

I also played with Media and I managed to display my images (it wasn't as straight forward as I would expect). I had a first taste of XSLTs, Macros and the usual CMS stuff, Document Types, Contents and Templates. XSLT in particular seems to be the way you can do powerful stuff with Umbraco, but I haven't gone there yet. For the next time, I'll try to use the Dictionaries for localized text, in combination with what I have already and try to make the ASP.NET template more reusable.
