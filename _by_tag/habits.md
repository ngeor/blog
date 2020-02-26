---
layout: default
permalink: /archives/tag/habits/
title: habits
post_count: 1
sort_index: 00589-habits
---
<h1 class="page-heading">Posts tagged with habits</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
