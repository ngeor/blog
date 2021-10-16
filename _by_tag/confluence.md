---
layout: tag
permalink: /archives/tag/confluence/
title: Posts tagged with confluence
tag: confluence
post_count: 2
sort_index: 997-confluence
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
