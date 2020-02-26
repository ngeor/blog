---
layout: post
title: Dynamic PNG Image Generation with ASP.NET
date: 2010-06-25 14:16:00.000000000 +02:00
published: true
categories:
- tech
tags: []
---

I had created a small web app in MonoDevelop that created a png image on the fly. Porting the app to Windows .NET 3.5 with Visual Studio 2008 was almost painless, but it did include two unexpected incident. The first one was... well the app didn't run anymore, showing the dreadful "A generic error occured in GDI+". A bit of a research lead to this article <a href="http://aspalliance.com/319">here</a>. Apparently the problem occurs only with PNG images. The stream that you write the generated image to needs to be seekable and I guess in Mono the Response.OutputStream is seekable but in .NET it's not. The solution is to use an intermediate MemoryStream to write the image to and then dump that stream on Response.OutputStream.

After that was fixed, I noticed that the fonts were appearing ugly, as shown in the following graphic:

<img src="{{ site.baseurl }}/assets/2010/png-ugly-fonts.png" />

The solution to that was to fill the background of the entire image with a colour (white in my case). I think it must be related with PNG transparency. If you observe the above screenshot, the text appears ugly only in the area that is not filled with colour.
