---
layout: tag
permalink: /archives/tag/grunt-search/
title: Posts tagged with grunt-search
tag: grunt-search
post_count: 1
sort_index: 998-grunt-search
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
