---
layout: tag
permalink: /archives/tag/habits/
title: Posts tagged with habits
tag: habits
post_count: 1
sort_index: 998-habits
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
