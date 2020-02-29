---
layout: default
permalink: /archives/tag/nyc/
title: nyc
post_count: 1
sort_index: 998-nyc
---
<h1 class="page-heading">Posts tagged with nyc</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
