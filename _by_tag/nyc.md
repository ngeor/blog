---
layout: tag
permalink: /archives/tag/nyc/
title: Posts tagged with nyc
tag: nyc
post_count: 1
sort_index: 998-nyc
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
