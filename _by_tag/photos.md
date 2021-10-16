---
layout: tag
permalink: /archives/tag/photos/
title: Posts tagged with photos
tag: photos
post_count: 1
sort_index: 998-photos
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
