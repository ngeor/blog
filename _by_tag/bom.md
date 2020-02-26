---
layout: default
permalink: /archives/tag/bom/
title: bom
post_count: 1
sort_index: 00589-bom
---
<h1 class="page-heading">Posts tagged with bom</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
