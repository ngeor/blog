---
layout: tag
permalink: /archives/tag/david/
title: Posts tagged with david
tag: david
post_count: 1
sort_index: 998-david
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
