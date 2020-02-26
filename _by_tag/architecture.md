---
layout: default
permalink: /archives/tag/architecture/
title: architecture
post_count: 1
sort_index: 00589-architecture
---
<h1 class="page-heading">Posts tagged with architecture</h1>
{% assign posts = site.posts | where_exp: "item", "item.tags contains page.title" -%}
{%- include post-list.html -%}
