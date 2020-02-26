---
layout: default
permalink: /archives/tag/david/
title: david
post_count: 1
sort_index: 00589-david
---
<h1 class="page-heading">Posts tagged with david</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
