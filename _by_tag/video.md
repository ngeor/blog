---
layout: tag
permalink: /archives/tag/video/
title: Posts tagged with video
tag: video
post_count: 1
sort_index: 998-video
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
