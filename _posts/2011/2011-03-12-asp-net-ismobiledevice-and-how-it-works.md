---
layout: post
title: ASP.NET IsMobileDevice and how it works
date: 2011-03-12 08:09:00.000000000 +01:00
published: true
categories:
- Code
tags: []
---

In ASP.NET, you can use the <a href="http://msdn.microsoft.com/en-us/library/system.web.configuration.httpcapabilitiesbase.ismobiledevice.aspx" target="_blank">IsMobileDevice</a> property in the <a href="http://msdn.microsoft.com/en-us/library/system.web.httprequest.browser%28v=VS.100%29.aspx" target="_blank">Request.Browser</a> object of the current request to figure out if the user is calling your application using a mobile device.

I tried it with my old HTC phone and it didn't work, so I wondered why. Well, here's how it works.

Determining if the caller is a mobile device is based on the user agent string. The user agent is a header that the browser sends and it is a way of telling the server what is the browser, what is the browser's version, what is the operating system, etc. All browsers send this header by default. There are even browsers that falsely identify themselves as Internet Explorer, to trick sites that display messages "Works only with Internet Explorer".

Server side, ASP.NET gets this header and analyzes it based on <a href="http://stackoverflow.com/questions/1829089/how-does-ismobiledevice-work" target="_blank">browser definition files</a>. These files have a browser file extension and can be found in C:WindowsMicrosoft.NETFramework'91;your .NET version]ConfigBrowsers. These are the global browser definitions that apply to all applications; a web app can define its own app-specific browser definitions by placing browser files in App_Browsers.

A <a href="http://msdn.microsoft.com/en-us/library/ms228122.aspx" target="_blank">browser definition file</a> is an XML file that defines rules (regular expressions) to test against the user agent string. An example can look like this:

```
<browsers>
  <browser id="IE" parentID="Default">
    <identification>
      <userAgent match="Internet Explorer" />
    </identification>
    <capabilities>
        <capability name="browser" value="Internet Explorer" />
        <capability name="isMobileDevice" value="false" />
    </capabilities>
  </browser>
</browsers>
```

This is a browser definition that says "if the user agent contains 'Internet Explorer', then define the following capabilities: browser is 'Internet Explorer', isMobileDevice is 'false'". So the reason my phone didn't get recognized as a Mobile Device is that there wasn't an existing rule for it.

I used Opera Mini on my phone and I used a test page to figure out its user agent. It's something like "Opera blah blah (Opera Mini; Windows Mobile; blah blah)". Well, I think the "Windows Mobile" is a nice obvious hint to use.

I opened up the opera.browser file that already existed on my machine and added the following entry:

```
<browser id="Opera10_WindowsMobile" parentID="Opera10">
  <identification>
    <userAgent match="Windows Mobile" />
  </identification>
  <capabilities>
    <capability name="isMobileDevice" value="true" />
  </capabilities>
</browser>
```

I am deriving from the rule "Opera10" because that matches the version of Opera Mini on my phone. The regular expression I use it's pretty straight forward: if looks for "Windows Mobile". If it finds it, the browser is no longer identified as "Opera10" but as "Opera10_WindowsMobile", my new rule.

How do I tell ASP.NET to use my changes? Saving the browser file apparently is not enough and iisreset also didn't work, so it was time to RTFM, or its web2.0 equivalent, Google for it. I found out that for local browser definition files (the ones placed in App_Browsers) folder, saving the file is enough. For global files however, there's a special command line tool called <a href="http://msdn.microsoft.com/en-us/library/ms229858%28v=VS.100%29.aspx" target="_blank">aspnet_regbrowsers</a>. This is located at `C:\Windows\Microsoft.NETFramework[your .NET version]`. Running "aspnet_regbrowsers -i" will compile the browser files into an assembly called ASP.BrowserCapsFactory.dll and place it in the GAC.

After that, accessing the test page with my phone works and ASP.NET identifies it as a mobile browser!
