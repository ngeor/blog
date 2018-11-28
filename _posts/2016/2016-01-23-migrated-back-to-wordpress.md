---
layout: post
title: Migrated back to Wordpress
date: 2016-01-23 19:58:16.000000000 +01:00
published: true
categories: []
tags:
- google analytics
- jekyll
- Metablog
- wordpress
---

I've just migrated my blog back to Wordpress. I had been using Jekyll for quite some time now.<!--more-->

The setup with Jekyll makes blogging a bit more difficult. You don't have a friendly editor. Editing and publishing are decoupled, as it is essentially a static site generator.

Jekyll does give you full power, but that can also lead to paralysis by choice. Instead of writing texts, you're thinking of code that you could hack into Jekyll to make it do something awesome.

Moving back was relatively easy. I had to tweak Jekyll to produce an RSS feed of all of my posts. Then I imported that RSS file into Wordpress. Several things are currently broken (e.g. no images are imported) but I'll fix them slowly over time. The good thing is that the permalinks are the same.

I'll close my first post for 2016 with a mini-rant: I was looking for a Google Analytics plugin for my new Wordpress installation. I tried these two:
<ul>
<li>Google Analytics Dashboard for WP. This one required to authenticate with my Google Account. Apparently it does way more that simply injecting the tracking code, so that got rejected.</li>
<li>Google Analytics by Yoast. Now this one is a disgrace. In addition to requiring authentication via my Google account, it displays advertisements while editing its settings, which it offers to hide if you purchase the premium version...</li>
</ul>

Luckily, I found one other plugin called "<a href="https://wordpress.org/plugins/super-simple-google-analytics/" target="_blank">Super Simple Google Analytics</a>", which just inserts the tracking code, nice and simple.
