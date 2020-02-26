---
layout: default
permalink: /archives/tag/retro/
title: retro
post_count: 1
sort_index: 00589-retro
---
<h1 class="page-heading">Posts tagged with retro</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
