---
layout: tag
permalink: /archives/tag/clang-format/
title: Posts tagged with clang-format
tag: clang-format
post_count: 1
sort_index: 998-clang-format
---
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.tag" -%}
{%- include post-list.html -%}
