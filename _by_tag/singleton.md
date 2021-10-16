---
layout: tag
permalink: /archives/tag/singleton/
title: Posts tagged with singleton
tag: singleton
post_count: 1
sort_index: 998-singleton
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
