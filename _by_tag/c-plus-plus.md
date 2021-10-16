---
layout: tag
permalink: /archives/tag/c-plus-plus/
title: Posts tagged with C++
tag: C++
post_count: 2
sort_index: 997-c++
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
