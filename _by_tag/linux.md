---
layout: tag
permalink: /archives/tag/linux/
title: Posts tagged with linux
tag: linux
post_count: 1
sort_index: 998-linux
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
