---
layout: default
permalink: /archives/tag/singleton/
title: singleton
post_count: 1
sort_index: 998-singleton
---
<h1 class="page-heading">Posts tagged with singleton</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
