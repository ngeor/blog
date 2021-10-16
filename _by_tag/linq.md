---
layout: tag
permalink: /archives/tag/linq/
title: Posts tagged with linq
tag: linq
post_count: 1
sort_index: 998-linq
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
