---
layout: post
title: Custom progress indicator for UpdatePanel
date: 2011-04-10 07:43:00.000000000 +02:00
published: true
categories:
- programming
tags: []
---

In ASP.NET the UpdatePanel can help you create an AJAX experience very fast and easy. It is typical to provide some visual element in the page that indicates that the AJAX request is been processed. This can be an animated image, a simple text message, a pretty modal box with a nice shadow effect - anything that does the trick and tells the user that the page is not broken but it's busy.

The UpdateProgress control in ASP.NET can handle showing a simple message, but for something more sophisticated, you'll have to do it yourself.<!--more-->

In this example, we'll use an animated loading image to indicate progress when a user sorts a GridView. The animated loading image will appear within the table header that the user clicked on in order to sort. This way the user will definitely see the image, since it appears exactly where he clicked. We're aiming at something like the next screenshot:
<img src="{{ site.baseurl }}/assets/2011/ajax-progress-in-cell.png" />

First we attach a javascript handler that will be called when an AJAX request is initiated:

```js
function onInit(sender, args) { }

Sys.WebForms.PageRequestManager.getInstance().add_initializeRequest(onInit);
```

We need to see if the postback is caused by an element within a table header. If that's the case, we append the HTML markup that renders the loading image to the inner HTML of the table header:

```js
function onInit(sender, args) {
  var element = args.get_postBackElement();
  if (element && element.parentNode && element.parentNode.tagName == "TH") {
    element.parentNode.innerHTML = element.parentNode.innerHTML +
      ' <img src="img/progress.gif" />';
  }
}
```

This is enough, but we can do a bit better. With this code, if you click very fast on the table header, you'll end up with more loading images shown. What we can do to fix this is to cancel the new request if an existing one is still been processed.

```js
function onInit(sender, args) {
  var status = Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack();
  if (status) {
    args.set_cancel(true);
  } else {
    var element = args.get_postBackElement();
    if (element && element.parentNode && element.parentNode.tagName == "TH") {
      element.parentNode.innerHTML = element.parentNode.innerHTML +
        ' <img src="img/progress.gif" />';
    }
  }
}
```

That's it! If you add this script to your page, all GridViews (or any other table for that matter) inside UpdatePanels will show the animated loading image within the table header when the user sorts the table.

Hope this helps.
