---
layout: tag
permalink: /archives/tag/smashing/
title: Posts tagged with smashing
tag: smashing
post_count: 2
sort_index: 997-smashing
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
