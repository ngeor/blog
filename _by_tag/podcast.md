---
layout: tag
permalink: /archives/tag/podcast/
title: Posts tagged with podcast
tag: podcast
post_count: 3
sort_index: 996-podcast
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
