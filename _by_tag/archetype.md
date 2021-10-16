---
layout: tag
permalink: /archives/tag/archetype/
title: Posts tagged with archetype
tag: archetype
post_count: 2
sort_index: 997-archetype
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
