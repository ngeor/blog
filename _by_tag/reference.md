---
layout: tag
permalink: /archives/tag/reference/
title: Posts tagged with reference
tag: reference
post_count: 7
sort_index: 992-reference
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
