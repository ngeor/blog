---
layout: post
title: Valid HTML and Valid CSS
date: 2011-03-12 12:15:00.000000000 +01:00
type: post
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

This blog (and this site in general) has two nice image buttons at the end of the page, saying that the HTML and CSS are valid. Are they really?

Well I figured out several days ago that they weren't valid. I must've been really bored and I actually clicked the images. Both the HTML and the CSS were invalid. Today I had some time to fix this.

The HTML is now again valid. The tiny problem was caused by BlogEngine itself: an ampersand wasn't encoded. I'm now using a modified dll and I submitted <a href="http://blogengine.codeplex.com/SourceControl/network/Forks/NikolaosGeorgiou/MinifyJavascriptInvalidHTML" target="_blank">my code changes</a> (all 4 keystrokes of them) to their source code where they're waiting to be approved.

As for the CSS, I think the W3C validator has some bug. It chokes on the border-radius property, which is valid CSS3. I see that some other person has <a href="http://www.w3.org/Bugs/Public/show_bug.cgi?id=11975" target="_blank">already filed this as a bug</a> last week, so I guess I'll just have to wait.

In any case, I think it's interesting to explore how this validation can become a part of the build process; otherwise you just have two images there that don't mean anything. I didn't find anything ready on the web so I created it myself: NAnt tasks that use the W3C online validation services to validate urls of a site.

The project is called <a href="https://sourceforge.net/projects/w3c-nant/" target="_blank">w3c-nant</a> and it contains a <a href="http://sourceforge.net/projects/w3c-nant/files/v1.0.0/W3CValidationTasks.dll/download" target="_blank">single dll with two NAnt tasks</a>: validateHtml and validateCss. The names are self descriptive I think. To use them, first copy the dll into the bin folder of NAnt. In your NAnt build file you can now write instructions like:

```
<validateHtml url="http://www.mysite.com/" />
<validateCss url="http://www.mysite.com/" />
```

Note that by default the build will fail if the W3C reports validation errors. If you don't want that to happen, you can set the attribute failonerror to false:

```
<validateHtml url="http://www.mysite.com" failonerror="false" />
```

NAnt will then consider this a non-fatal error: it will be logged as an error but the build will still be successful.

Also, these tasks will only validate the url that they are given; they don't perform any crawling of any kind. So they don't guarantee that 100% of the site's pages are valid. My suggestion is to use a few urls that you think are representative enough - or you can write some crawler task and integrate it with the validator :-)

Hope this helps.
