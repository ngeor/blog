---
layout: default
permalink: /archives/tag/pair-programming/
title: pair programming
post_count: 1
sort_index: 998-pair programming
---
<h1 class="page-heading">Posts tagged with pair programming</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
