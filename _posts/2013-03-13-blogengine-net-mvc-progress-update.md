---
layout: post
title: BlogEngine.NET MVC - Progress update
date: 2013-03-13 08:39:00.000000000 +01:00
parent_id: '0'
published: true
categories:
- Code
tags: []
author: Nikolaos Georgiou
---

Here's a short update on what I've been working on. Time is a bit limited but I like to hack around in this project and that's what it's all about!
<ul>
<li>Implemented Category and Tag pages</li>
<li>Initial implementation for RSS feed</li>
<li>Showing comments in the post page</li>
<li>Implemented Add, Edit, Delete, Restore and Purge actions for Posts and Pages</li>
<li>Started working on a blog settings page</li>
</ul>

I'm thinking of perhaps setting up an issue tracker to maintain a log of what needs to be done and what has already been done. I don't think I can do that in CodePlex, because that would have to be a tracker just for my branch and I don't think that's supported. Or maybe set up some rough goals like milestones of the project. I'll see how it goes...

One comment on the Restore and Purge actions: in BlogEngine.NET, when you delete a post or a page it doesn't get completely deleted. It is marked as deleted, but the post file is still there (if you're using the default file based storage). To really delete it, you need to empty the recycle bin in the admin UI. I have taken a different approach in the pages that show lists of posts (homepage, category page, tag page, etc):
<ul>
<li>you see all the posts (or pages) you're allowed to based on your permissions</li>
<li>that includes deleted posts too!</li>
<li>unpublished and deleted items are presented with a small text label that indicates their status</li>
</ul>

I find this view a bit simpler, at least for now... of course the recycle bin concept is probably better (you delete a post for a reason, you don't want to see it in your face all the time) but that will come later.

Things to come up next:
<ul>
<li>pagination for homepage and similar pages</li>
<li>submitting comments</li>
<li>uploading images to a post (I want to use <a href="http://imageresizing.net/">ImageResizing.Net</a> here)</li>
<li>implement contact form</li>
<li>implement blog settings page (only settings that are used).</li>
<li>support markdown formatting in posts and pages</li>
</ul>

and more, much more!
