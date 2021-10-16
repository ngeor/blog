---
layout: tag
permalink: /archives/tag/retro/
title: Posts tagged with retro
tag: retro
post_count: 1
sort_index: 998-retro
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
