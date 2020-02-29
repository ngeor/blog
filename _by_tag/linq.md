---
layout: default
permalink: /archives/tag/linq/
title: linq
post_count: 1
sort_index: 998-linq
---
<h1 class="page-heading">Posts tagged with linq</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
