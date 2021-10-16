---
layout: tag
permalink: /archives/tag/immutables/
title: Posts tagged with immutables
tag: immutables
post_count: 1
sort_index: 998-immutables
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
