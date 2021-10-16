---
layout: tag
permalink: /archives/tag/atom/
title: Posts tagged with atom
tag: atom
post_count: 2
sort_index: 997-atom
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
