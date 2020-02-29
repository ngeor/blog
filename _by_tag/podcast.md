---
layout: default
permalink: /archives/tag/podcast/
title: podcast
post_count: 3
sort_index: 996-podcast
---
<h1 class="page-heading">Posts tagged with podcast</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
