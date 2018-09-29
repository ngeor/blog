---
layout: post
title: Getting the client's timezone in ASP.NET
date: 2010-12-01 20:03:00.000000000 +01:00
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

The client (browser) doesn't send any information to the server regarding the client's timezone. It's just not supported. One might try to guess the timezone from the culture or even try to guess it from this new geo-location feature. Maybe in the future there will be a new header like "X-Client-Timezone: UTC+1" but for the time being a good approach is the following.

We'll use three different pages in this example:
<ul>
<li>Default.aspx, the page where the client's timezone is needed</li>
<li>DetectTimezone.aspx, the page that will output javascript code that will retrieve the client's timezone client-side and send it back to the server.</li>
<li>SetTimezone.aspx, the page that the javascript code from DetectTimezone.aspx will redirect to and the page that stores the client's timezone in the Session or in a Cookie.</li>
</ul>

The flow is:
<ol>
<li>User requests Default.aspx (1st request)</li>
<li>In Default.aspx Page_Load, the page checks if the timezone is already set in the Session or in a Cookie. If not, we need to detect it and for that purpose it issues a Server.Transfer to DetectTimezone.aspx and ends the response. Note that Server.Transfer is preferred over Response.Redirect to avoid another hit from the client to the server.</li>
<li>DetectTimezone.aspx loads. This page doesn't have any server-side logic. It only outputs javascript code that will calculate the client's timezone and redirect client-side to SetTimezone.aspx using the client's timezone as a query string parameter.</li>
<li>Javascript redirects to SetTimezone.aspx?timezone=[client timezone] (2nd request)</li>
<li>SetTimezone.aspx loads. It retrieves the timezone from the query string and saves it in the Session or in a Cookie. SetTimezone.aspx redirects to Default.aspx with Response.Redirect.</li>
<li>User requests Default.aspx (3rd request). Timezone is set in Session or Cookie, page loads normally.</li>
</ol>

The javascript code in DetectTimezone.aspx is the following:

```
location.href = 'SetTimezone.aspx?timezone=' + new Date().getTimezoneOffset().toString();
```

It's a simple script that redirects to SetTimezone.aspx, passing as the 'timezone' parameter the timezone offset of the client's timezone. That value is equal to the offset of the client's timezone from UTC expressed in minutes. So UTC+1 is -60, UTC+2 is -120, etc. I find it a bit strange that UTC+1 is -60, I expected that UTC+1 would be +60, but I didn't worry too much about it.

While the basic idea is quite simple, there are many things that you might want to consider in an actual implementation. Here's some of them.
<h2>UI Experience</h2>

DetectTimezone.aspx loads very fast because it doesn't have any server-side logic. That means that the page's output will be visible to the user until Default.aspx does its normal load (on the 3rd request). If Default.aspx is a slow loading page, it would be a better user experience to show a message in DetectTimezone.aspx that informs the user that his page will load shortly (maybe together with an animated progress gif). Perhaps even set DetectTimezone.aspx to use the same master page and look and feel as the Default.aspx.
<h2>Generic Handler instead of ASP.NET Page</h2>

SetTimezone.aspx doesn't produce any output whatsoever, so you might want to use a Generic Handler instead of a ASP.NET Page (so SetTimezone.ashx instead of SetTimezone.aspx).
<h2>Google Analytics</h2>

You can also avoid using a separate SetTimezone.aspx page and just use Default.aspx instead. That will reduce the user's requests to 2:
<ul>
<li>Javascript redirects to Default.aspx?timezone=[client timezone] instead of SetTimezone.aspx?timezone=[client timezone] (2nd request)</li>
<li>Default.aspx sets the timezone in a cookie or the session.</li>
<li>Default.aspx proceeds execution</li>
</ul>

The reason I like the first approach is:
<ul>
<li>Default.aspx logic is simpler</li>
<li>For traffic analysis (i.e. Google Analytics) it provides clean results since only Default.aspx appears and not all the 'Default.aspx?timezone=' variations.</li>
</ul>
<h2>Fallback plan</h2>

This is important: if something goes wrong with the auto-detection or simply if javascript is turned off at the user's browser, Default.aspx will never ever load because it will keep on transferring the response to DetectTimezone.aspx. You need to create an extra cookie or session value that will hold a boolean value indicating whether an attempt to auto detect the client's timezone has already been made. Just before transferring the response from Default.aspx to DetectTimezone.aspx, set this value server side to true. With this extra safeguard, if the auto-detection fails a following attempt will not be made and Default.aspx will load. Of course in this case the client's timezone is unknown and we need to fall back to something reasonable (I guess UTC is good enough).
<h2>Support for more pages</h2>

SetTimezone.aspx should be able to redirect to the page where the original request came from. Either use the HTTP_REFERER header or pass an extra parameter to the query string.
<h2>Code Organization</h2>

The bulk of the code that makes this method work should not be in the code-behind of some ASPX page, so that it can be reused and so that the ASPX pages are less cluttered by this kind of code.

My favorite approach would be to create a separate static class with extension methods that will encapsulate the logic of persisting the user's timezone. Something like TimezoneUtils.GetClientTimezone, TimezoneUtils.SetClientTimezone, TimezoneUtils.IsAutoDetectAttempted, TimezoneUtils.SetAutoDetectAttempted. Use extension methods extending Page and IHttpHandler for example and you'll be able to use this feature from any Page or Generic Handler while the code will be abstracted away in the static class.

You could do it in a more old school OOP way by putting the logic in a base Page class. Personally I consider this functionality as a nice add-in but not important enough to pollute my objects with it in a more formal way.
<h2>Summary</h2>

That's it! The idea is not ASP.NET specific of course. The basic concept can be applied to any web framework: use a dummy page (DetectTimezone.aspx) that will use javascript to send back to the server the client's timezone and store it somewhere (session or cookie). Make sure that you have a fallback plan in case javascript is off or doesn't work as expected, consider the URLs and HTTP requests your approach will generate and you're done! Hope this helps.
