---
layout: tag
permalink: /archives/tag/left-pad/
title: Posts tagged with left-pad
tag: left-pad
post_count: 1
sort_index: 998-left-pad
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
