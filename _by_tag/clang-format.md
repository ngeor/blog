---
layout: default
permalink: /archives/tag/clang-format/
title: clang-format
post_count: 1
sort_index: 00589-clang-format
---
<h1 class="page-heading">Posts tagged with clang-format</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
