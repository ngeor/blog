---
layout: default
permalink: /archives/tag/statistics/
title: statistics
post_count: 1
sort_index: 00589-statistics
---
<h1 class="page-heading">Posts tagged with statistics</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
