---
layout: tag
permalink: /archives/tag/fitness/
title: Posts tagged with fitness
tag: fitness
post_count: 1
sort_index: 998-fitness
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
