---
layout: tag
permalink: /archives/tag/pair-programming/
title: Posts tagged with pair programming
tag: pair programming
post_count: 1
sort_index: 998-pair programming
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
