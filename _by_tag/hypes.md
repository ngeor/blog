---
layout: default
permalink: /archives/tag/hypes/
title: hypes
post_count: 1
sort_index: 00589-hypes
---
<h1 class="page-heading">Posts tagged with hypes</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
