---
layout: tag
permalink: /archives/tag/hypes/
title: Posts tagged with hypes
tag: hypes
post_count: 1
sort_index: 998-hypes
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
